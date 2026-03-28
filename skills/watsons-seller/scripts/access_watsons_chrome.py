#!/usr/bin/env python3
"""
Watsons Seller Center Chrome CDP Access Script

Access Watsons Seller Center (ASCP) using Chrome DevTools Protocol.
Requires Chrome to be running with remote debugging enabled.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("[ERROR] playwright not installed. Run: pip install playwright")
    sys.exit(1)


DEFAULT_CDP_URL = "http://127.0.0.1:9222"
DEFAULT_URL = "https://ascp-watsons.qragoracloud.com/ascp/index"


async def connect_to_chrome(cdp_url: str):
    """Connect to Chrome via CDP."""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.connect_over_cdp(cdp_url)
    return playwright, browser


async def login_and_access(url: str, cdp_url: str, screenshot_path: str = None, check_orders: bool = False, username: str = None, password: str = None):
    """Access Watsons Seller Center, optionally log in, and extract order info."""
    
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
    
    print(f"[INFO] Navigating to: {url}")
    await page.goto(url, wait_until="networkidle", timeout=30000)
    
    # Wait for page to load
    await asyncio.sleep(2)
    
    current_url = page.url
    print(f"[INFO] Current URL: {current_url}")
    
    # Check if on login page
    if "login" in current_url.lower() and username and password:
        print(f"[INFO] Attempting to log in with username: {username}")
        
        try:
            # Try to find and fill username field
            # Common selectors for username
            username_selectors = [
                'input[name="username"]',
                'input[name="user"]',
                'input[id="username"]',
                'input[id="user"]',
                'input[type="text"]',
                'input[placeholder*="user"]',
                'input[placeholder*="User"]',
                '#username',
                '#user'
            ]
            
            username_filled = False
            for selector in username_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=3000)
                    await page.fill(selector, username)
                    username_filled = True
                    print(f"[INFO] Filled username using selector: {selector}")
                    break
                except:
                    continue
            
            if not username_filled:
                # Try generic input
                inputs = await page.query_selector_all('input[type="text"], input[type="email"]')
                for inp in inputs:
                    try:
                        await inp.fill(username)
                        username_filled = True
                        print(f"[INFO] Filled username")
                        break
                    except:
                        continue
            
            # Try to find and fill password field
            password_selectors = [
                'input[name="password"]',
                'input[name="pwd"]',
                'input[id="password"]',
                'input[id="pwd"]',
                'input[type="password"]',
                '#password',
                '#pwd'
            ]
            
            password_filled = False
            for selector in password_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=3000)
                    await page.fill(selector, password)
                    password_filled = True
                    print(f"[INFO] Filled password using selector: {selector}")
                    break
                except:
                    continue
            
            if not password_filled:
                # Try generic password input
                inputs = await page.query_selector_all('input[type="password"]')
                for inp in inputs:
                    try:
                        await inp.fill(password)
                        password_filled = True
                        print(f"[INFO] Filled password")
                        break
                    except:
                        continue
            
            # Take screenshot after filling
            if screenshot_path:
                await page.screenshot(path=screenshot_path, full_page=True)
                print(f"[SUCCESS] Screenshot saved: {screenshot_path}")
            
            # Try to click submit button
            submit_selectors = [
                'button[type="submit"]',
                'button[name="submit"]',
                'button[id="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign In")',
                'button:has-text("login")',
                'button:has-text("sign in")',
                '.login-btn',
                '#loginBtn',
                '#submitBtn'
            ]
            
            for selector in submit_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=2000)
                    await page.click(selector)
                    print(f"[INFO] Clicked submit button: {selector}")
                    break
                except:
                    continue
            
            # Wait for navigation after login
            await asyncio.sleep(3)
            
            current_url = page.url
            print(f"[INFO] URL after login attempt: {current_url}")
            
        except Exception as e:
            print(f"[WARNING] Login attempt failed: {e}")
    
    # Check login status
    page_title = await page.title()
    is_logged_in = "login" not in current_url.lower()
    
    # Take final screenshot
    if screenshot_path:
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"[SUCCESS] Screenshot saved: {screenshot_path}")
    
    result = {
        "status": "success" if is_logged_in else "not_logged_in",
        "url": current_url,
        "title": page_title,
    }
    
    if not is_logged_in:
        print("[WARNING] STATUS: Not logged in")
    else:
        print("[SUCCESS] STATUS: Logged in to Watsons Seller")
        
        # Try to extract order info if requested
        if check_orders:
            try:
                order_data = await page.evaluate("""() => {
                    const results = {};
                    
                    // Look for order-related text
                    const bodyText = document.body.innerText;
                    
                    // Common order status patterns
                    const patterns = [
                        /To Ship.*?(\d+)/i,
                        /To Pack.*?(\d+)/i,
                        /Pending.*?(\d+)/i,
                        /Orders.*?(\d+)/i,
                        /(\d+).*?order/i
                    ];
                    
                    patterns.forEach((pattern, idx) => {
                        const match = bodyText.match(pattern);
                        if (match) {
                            results['pattern_' + idx] = match[0];
                        }
                    });
                    
                    return results;
                }""")
                
                result["orders"] = order_data
                print(f"[INFO] Order data found: {order_data}")
                
            except Exception as e:
                print(f"[WARNING] Could not extract order details: {e}")
    
    await playwright.stop()
    return result


def main():
    parser = argparse.ArgumentParser(description="Access Watsons Seller Center via Chrome CDP")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL to access")
    parser.add_argument("--screenshot", help="Path to save screenshot")
    parser.add_argument("--check-orders", action="store_true", help="Extract order summary")
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help="Chrome CDP URL")
    parser.add_argument("--username", default="Enriae", help="Username for login")
    parser.add_argument("--password", help="Password for login")
    parser.add_argument("--wait", type=int, default=5, help="Wait time in seconds")
    
    args = parser.parse_args()
    
    # Run the async function
    result = asyncio.run(login_and_access(
        url=args.url,
        cdp_url=args.cdp_url,
        screenshot_path=args.screenshot,
        check_orders=args.check_orders,
        username=args.username,
        password=args.password
    ))
    
    # Print result
    print("\n" + "=" * 80)
    print("WATSONS SELLER CENTER RESULT")
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
