#!/usr/bin/env python3
"""
Shopee Seller Centre Automation Script - Chrome CDP Version
Uses real Chrome browser with persistent profile via CDP connection.
Human logs in first, then automation uses the existing session.

IMPORTANT: Data is extracted from HTML, NOT from screenshots.
Output includes JSON for transparency.
"""

import asyncio
import json
import sys
import os
import requests
import argparse
from playwright.async_api import async_playwright

# Chrome CDP Configuration
CHROME_CDP_URL = os.environ.get("CHROME_CDP_URL", "http://127.0.0.1:9222")
CHROME_PROFILE = os.environ.get("CHROME_PROFILE", "/home/enraie/.chrome-openclaw")


async def check_chrome_connection():
    """Check if Chrome is running and accessible via CDP."""
    try:
        response = requests.get(f"{CHROME_CDP_URL}/json/version", timeout=5)
        if response.status_code == 200:
            version_info = response.json()
            print(f"[INFO] Connected to Chrome: {version_info.get('Browser', 'Unknown')}")
            return True
    except Exception as e:
        print(f"[ERROR] Cannot connect to Chrome at {CHROME_CDP_URL}: {e}", file=sys.stderr)
        print("[HINT] Make sure Chrome is running with --remote-debugging-port=9222", file=sys.stderr)
    return False


async def access_shopee(url="https://seller.shopee.sg/portal/sale/order", screenshot=None):
    """Access Shopee Seller using Chrome CDP connection."""
    
    # Check Chrome connection first
    if not await check_chrome_connection():
        print(f"[ERROR] Cannot connect to Chrome at {CHROME_CDP_URL}", file=sys.stderr)
        return None
    
    async with async_playwright() as p:
        # Connect to existing Chrome via CDP
        try:
            browser = await p.chromium.connect_over_cdp(CHROME_CDP_URL)
            print(f"[INFO] Connected to Chrome via CDP")
        except Exception as e:
            print(f"[ERROR] Failed to connect to Chrome CDP: {e}", file=sys.stderr)
            return None
        
        # Get existing context or create new one
        contexts = browser.contexts
        if contexts:
            context = contexts[0]
            print(f"[INFO] Using existing browser context with stored cookies")
        else:
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
            print(f"[INFO] Created new browser context")
        
        page = await context.new_page()
        
        try:
            print(f"[INFO] Navigating to: {url}")
            await page.goto(url, timeout=30000)
            await asyncio.sleep(3)
        except Exception as e:
            print(f"[ERROR] Navigation failed: {e}", file=sys.stderr)
            await browser.close()
            return None
        
        print(f"Page URL: {page.url}")
        print(f"Page Title: {await page.title()}")
        
        # Save page HTML first
        content = await page.content()
        
        # Build output data
        output_data = {
            "status": "success",
            "url": page.url,
            "title": await page.title(),
            "html_length": len(content)
        }
        
        # Check login status
        if "login" in page.url.lower():
            print("\nLooks like we're not logged in!")
            print("The session might have expired - happens sometimes.")
            print(f"Could you log in via Chrome at: {url}")
            print(f"Chrome profile: {CHROME_PROFILE}\n")
            
            output_data = {
                "status": "login_required",
                "url": page.url,
                "title": await page.title(),
                "user_action_required": "Not logged in. Please log in via Chrome and let me know when done?"
            }
        else:
            print("[SUCCESS] Got it! Shopee Seller is accessible.\n")
            output_data = {
                "status": "success",
                "url": page.url,
                "title": await page.title(),
                "html_length": len(content)
            }
        
        # Take screenshot if requested
        if screenshot:
            await page.screenshot(path=screenshot, full_page=True)
            print(f"Screenshot saved: {screenshot}")
            output_data["screenshot"] = screenshot
        
        # Output JSON at the end
        print(f"\n{json.dumps(output_data, indent=2)}")
        
        # Close page but keep browser connection
        await page.close()
        
        return content


def main():
    parser = argparse.ArgumentParser(description='Access Shopee Seller Centre - Chrome CDP Version')
    parser.add_argument('--url', default='https://seller.shopee.sg/portal/sale/order', 
                        help='URL to access (default: orders page)')
    parser.add_argument('--screenshot', help='Path to save screenshot')
    parser.add_argument('--cdp-url', default='http://127.0.0.1:9222', help='Chrome CDP URL')
    
    args = parser.parse_args()
    
    # Set global CDP URL
    global CHROME_CDP_URL
    CHROME_CDP_URL = args.cdp_url
    
    asyncio.run(access_shopee(args.url, args.screenshot))


if __name__ == "__main__":
    main()
