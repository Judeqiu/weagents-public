#!/usr/bin/env python3
"""
TikTok Shop Seller Center Chrome CDP Access Script

Access TikTok Shop Seller Center (Singapore) using Chrome DevTools Protocol.
Requires Chrome to be running with remote debugging enabled.
"""

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("[ERROR] playwright not installed. Run: pip install playwright")
    sys.exit(1)


DEFAULT_CDP_URL = "http://127.0.0.1:9222"
DEFAULT_URL = "https://seller-sg.tiktok.com/homepage"


async def connect_to_chrome(cdp_url: str):
    """Connect to Chrome via CDP."""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.connect_over_cdp(cdp_url)
    return playwright, browser


async def access_tiktok(url: str, cdp_url: str, screenshot_path: str = None, check_orders: bool = False, tab: str = None):
    """Access TikTok Shop Seller Center and optionally extract order info."""
    
    print(f"[INFO] Connecting to Chrome: {cdp_url}")
    
    try:
        playwright, browser = await connect_to_chrome(cdp_url)
    except Exception as e:
        print(f"[ERROR] Cannot connect to Chrome at {cdp_url}")
        print(f"[ERROR] {e}")
        return {"status": "error", "message": str(e)}
    
    # Get existing context
    contexts = browser.contexts
    if not contexts:
        print("[ERROR] No browser contexts found")
        await playwright.stop()
        return {"status": "error", "message": "No browser contexts"}
    
    context = contexts[0]
    page = context.pages[0] if context.pages else await context.new_page()
    
    # Build URL based on tab if specified
    if tab:
        tab_urls = {
            "all": "https://seller-sg.tiktok.com/order/m/order-list?tab=all",
            "unfulfillable": "https://seller-sg.tiktok.com/order/m/order-list?tab=unfulfillable",
            "to_ship": "https://seller-sg.tiktok.com/order/m/order-list?tab=unfulfillable",
            "in_transit": "https://seller-sg.tiktok.com/order/m/order-list?tab=in_transit",
            "delivered": "https://seller-sg.tiktok.com/order/m/order-list?tab=delivered",
            "returns": "https://seller-sg.tiktok.com/order/m/order-list?tab=returns",
        }
        url = tab_urls.get(tab, DEFAULT_URL)
    
    print(f"[INFO] Navigating to: {url}")
    
    # Use domcontentloaded instead of networkidle (TikTok is heavy)
    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    
    # Wait for page to load
    await asyncio.sleep(3)
    
    # Check if logged in
    page_title = await page.title()
    current_url = page.url
    print(f"[INFO] Page Title: {page_title}")
    print(f"[INFO] Current URL: {current_url}")
    
    is_logged_in = "login" not in current_url.lower() and "account" not in current_url.lower()
    
    # Take screenshot if requested
    if screenshot_path:
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"[SUCCESS] Screenshot saved: {screenshot_path}")
    
    result = {
        "status": "success" if is_logged_in else "not_logged_in",
        "url": current_url,
        "title": page_title,
    }
    
    if not is_logged_in:
        print("[WARNING] STATUS: Not logged in - session expired or needs manual login")
        print(f"[HINT] Please log in manually via Chrome at: https://seller-sg.tiktok.com/account/login")
        result["message"] = "Not logged in"
    else:
        print("[SUCCESS] STATUS: Successfully accessed TikTok Shop Seller")
        
        # Try to extract order info if requested
        if check_orders:
            try:
                # Get page text content
                text = await page.inner_text('body')
                
                # Look for order counts in the page
                order_data = {}
                
                # Extract order counts from dashboard cards
                # Pattern: "X orders" or "X" near status words
                patterns = [
                    (r'Unfulfilled[:\s]*(\d+)', 'unfulfilled'),
                    (r'To Ship[:\s]*(\d+)', 'to_ship'),
                    (r'In Transit[:\s]*(\d+)', 'in_transit'),
                    (r'Delivered[:\s]*(\d+)', 'delivered'),
                    (r'Returns[:\s]*(\d+)', 'returns'),
                    (r'(\d+)\s*order', 'total_orders'),
                ]
                
                for pattern, key in patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        order_data[key] = match.group(1)
                
                # Try to find numbers in dashboard cards
                cards = await page.query_selector_all('[class*="card"], [class*="stat"], [class*="count"], .value')
                for card in cards[:15]:
                    try:
                        card_text = await card.inner_text()
                        # Extract just numbers
                        numbers = re.findall(r'\d+', card_text)
                        if numbers and numbers[0] != '0':
                            # Determine which stat this is based on context
                            card_lower = card_text.lower()
                            if 'unfulfillable' in card_lower or 'to ship' in card_lower:
                                order_data['to_ship'] = numbers[0]
                            elif 'transit' in card_lower:
                                order_data['in_transit'] = numbers[0]
                            elif 'delivered' in card_lower:
                                order_data['delivered'] = numbers[0]
                            elif 'return' in card_lower:
                                order_data['returns'] = numbers[0]
                    except:
                        pass
                
                # Check for empty state ("No data")
                if "no data" in text.lower() or "no orders" in text.lower():
                    order_data["status"] = "empty"
                    # Set all to 0
                    order_data.setdefault('to_ship', '0')
                    order_data.setdefault('in_transit', '0')
                    order_data.setdefault('delivered', '0')
                    order_data.setdefault('returns', '0')
                    print("[INFO] No orders found - empty state")
                else:
                    # If we found some counts, use them; otherwise set to 0
                    order_data.setdefault('to_ship', '0')
                    order_data.setdefault('in_transit', '0')
                    order_data.setdefault('delivered', '0')
                    order_data.setdefault('returns', '0')
                
                result["orders"] = order_data
                print(f"[INFO] Order data found: {order_data}")
                
            except Exception as e:
                print(f"[WARNING] Could not extract order details: {e}")
    
    await playwright.stop()
    return result


def main():
    parser = argparse.ArgumentParser(description="Access TikTok Shop Seller Center via Chrome CDP")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL to access")
    parser.add_argument("--screenshot", help="Path to save screenshot")
    parser.add_argument("--check-orders", action="store_true", help="Extract order summary")
    parser.add_argument("--tab", choices=["all", "unfulfillable", "to_ship", "in_transit", "delivered", "returns"], help="Go to specific order tab")
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help="Chrome CDP URL")
    parser.add_argument("--wait", type=int, default=5, help="Wait time in seconds")
    
    args = parser.parse_args()
    
    # Run the async function
    result = asyncio.run(access_tiktok(
        url=args.url,
        cdp_url=args.cdp_url,
        screenshot_path=args.screenshot,
        check_orders=args.check_orders,
        tab=args.tab
    ))
    
    # Print result
    print("\n" + "=" * 80)
    print("TIKTOK SHOP SELLER CENTER RESULT")
    print("=" * 80)
    print(f"Status: {result.get('status')}")
    if "orders" in result:
        print(f"Orders: {result.get('orders')}")
    print("=" * 80)
    
    if result["status"] == "error":
        sys.exit(1)
    elif result["status"] == "not_logged_in":
        sys.exit(2)


if __name__ == "__main__":
    main()
