#!/usr/bin/env python3
"""
Extract Shopee order details from the orders page - Chrome CDP Version
Uses real Chrome browser with persistent profile.

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
    return False


async def extract_orders(url="https://seller.shopee.sg/portal/sale/order"):
    """Extract order details from Shopee using Chrome CDP."""
    
    if not await check_chrome_connection():
        print("[ERROR] Chrome not accessible. Is Chrome running with --remote-debugging-port=9222?", file=sys.stderr)
        return
    
    async with async_playwright() as p:
        # Connect to existing Chrome via CDP
        try:
            browser = await p.chromium.connect_over_cdp(CHROME_CDP_URL)
            print(f"[INFO] Connected to Chrome via CDP")
        except Exception as e:
            print(f"[ERROR] Failed to connect to Chrome CDP: {e}", file=sys.stderr)
            return
        
        # Get existing context
        contexts = browser.contexts
        if contexts:
            context = contexts[0]
        else:
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
        
        page = await context.new_page()
        
        await page.goto(url, timeout=30000)
        await asyncio.sleep(8)  # Wait longer for orders to load
        
        print(f"Page URL: {page.url}")
        print(f"Page Title: {await page.title()}")
        
        # Check if we're logged in
        if "login" in page.url.lower():
            print("\nLooks like we're not logged in!")
            print("The session might have expired - happens sometimes.")
            print(f"Could you log in via Chrome at: {url}")
            print(f"Chrome profile: {CHROME_PROFILE}\n")
            
            output_data = {
                "status": "login_required",
                "error": "Not logged in - redirected to login page",
                "url": page.url,
                "user_action_required": "Please check Chrome - you are on the login page. Need to log in."
            }
            print(f"\n{json.dumps(output_data, indent=2)}")
            await browser.close()
            return
        
        # Check for "No Orders Found"
        page_text = await page.evaluate("""() => document.body.innerText""")
        
        if "No Orders Found" in page_text or "no orders" in page_text.lower():
            print("\nNo orders found for this status.\n")
            output_data = {
                "status": "success",
                "total_orders": 0,
                "orders": [],
                "message": "No orders found for this filter"
            }
            print(f"{json.dumps(output_data, indent=2)}")
            await browser.close()
            return
        
        # Extract order data using text content parsing
        orders_data = await page.evaluate("""
            () => {
                const orders = [];
                const text = document.body.innerText;
                
                // Split by "Order ID" to find order blocks
                const orderBlocks = text.split('Order ID');
                
                for (let i = 1; i < orderBlocks.length; i++) {
                    const block = orderBlocks[i];
                    
                    // Skip if block is too small
                    if (block.length < 20) continue;
                    
                    // Extract order ID (first 10-15 chars after "Order ID")
                    const orderIdMatch = block.match(/[A-Z0-9]{8,15}/);
                    const orderId = orderIdMatch ? orderIdMatch[0] : '';
                    
                    // Extract lines from block
                    const lines = block.split('\\n').filter(l => l.trim() && l.length < 100);
                    
                    // Find product: line before price ($) that doesn't start with x
                    let product = '';
                    let price = '';
                    for (let j = 0; j < lines.length; j++) {
                        const line = lines[j].trim();
                        // Look for price line
                        if (line.match(/\\$[0-9]/)) {
                            price = line;
                            // Product should be 1-3 lines before price
                            if (j >= 2) {
                                product = lines[j-2].trim();
                                // Skip if it's just x1, x2 etc
                                if (product.match(/^x[0-9]+$/)) {
                                    product = lines[j-3] ? lines[j-3].trim() : '';
                                }
                            }
                            break;
                        }
                    }
                    
                    // Extract status
                    let status = '';
                    if (block.includes('Delivered')) status = 'Delivered';
                    else if (block.includes('Order Received')) status = 'Order Received';
                    else if (block.includes('Completed')) status = 'Completed';
                    else if (block.includes('To Ship')) status = 'To Ship';
                    else if (block.includes('Cancelled')) status = 'Cancelled';
                    
                    // Extract buyer - look for username after "Rate" or "Check Details"
                    let buyer = '';
                    const rateMatch = block.match(/Rate\\n([^\\n]+)/);
                    if (rateMatch && rateMatch[1]) {
                        const potential = rateMatch[1].trim();
                        // Skip if it contains certain keywords
                        if (!potential.includes('Invoice') && !potential.includes('Details') && potential.length < 25) {
                            buyer = potential;
                        }
                    }
                    
                    if (orderId && product) {
                        orders.push({
                            index: orders.length + 1,
                            orderId: 'Order ID ' + orderId,
                            product: product.substring(0, 80),
                            status: status,
                            price: price,
                            buyer: buyer,
                            date: ''
                        });
                    }
                }
                
                return { orders: orders, count: orders.length };
            }
        """)
        
        # Prepare output data
        output_data = {
            "status": "error",
            "error": "Unknown error",
            "user_action_required": None
        }
        
        print("\n" + "="*80)
        print("SHOPEE ORDER DETAILS")
        print("="*80)
        
        # Check if we're logged in
        if "login" in page.url.lower():
            print("\n[WARNING] Not logged in! Please log in manually via Chrome first.")
            print(f"[HINT] Chrome profile: {CHROME_PROFILE}")
            output_data = {
                "status": "login_required",
                "error": "Not logged in - redirected to login page",
                "url": page.url,
                "user_action_required": "Please check Chrome - you are on the login page. Need to log in."
            }
            print(f"\n{json.dumps(output_data, indent=2)}")
            await browser.close()
            return
        
        if isinstance(orders_data, dict) and 'orders' in orders_data and len(orders_data['orders']) > 0:
            order_count = orders_data['count']
            print(f"\nTotal Orders Found: {order_count}\n")
            
            # Build structured output
            order_summary = {
                "status": "success",
                "total_orders": order_count,
                "orders": orders_data['orders'][:20]  # First 20
            }
            
            for order in orders_data['orders'][:20]:  # Show first 20
                print(f"\n--- Order #{order['index']} ---")
                print(f"Order ID: {order['orderId']}")
                print(f"Product: {order['product']}")
                print(f"Status: {order['status']}")
                print(f"Price: {order['price']}")
                print(f"Buyer: {order['buyer']}")
                print(f"Date: {order['date']}")
                print("-" * 40)
            
            # Output JSON at the end
            print(f"\n{json.dumps(order_summary, indent=2)}")
        else:
            # Data extraction failed - report honestly, don't fabricate
            print("\nHmm, I couldn't grab the order data from this page.")
            print("The Shopee layout might have changed, or there might be a connection issue.")
            print("Could you take a look at Chrome and help me out?\n")
            
            output_data = {
                "status": "extraction_failed",
                "error": "Could not extract orders from page DOM",
                "page_url": page.url,
                "page_title": await page.title(),
                "user_action_required": "I couldn't extract the data. Please check Chrome and help?"
            }
            
            print(f"\n{json.dumps(output_data, indent=2)}")
        
        # Also save full HTML for analysis
        html = await page.content()
        output_path = "/tmp/shopee_orders_source.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html[:50000])  # First 50KB
        
        print(f"\nFull HTML saved to: {output_path}")
        
        await page.close()


def main():
    parser = argparse.ArgumentParser(description='Extract Shopee order details - Chrome CDP Version')
    parser.add_argument('--url', default='https://seller.shopee.sg/portal/sale/order', 
                        help='URL to access')
    parser.add_argument('--status', 
                        choices=['all', 'to_ship', 'ready_to_ship', 'processed', 'shipped', 'completed', 'cancelled', 'new'],
                        default='all',
                        help='Order status filter: all, to_ship (new), ready_to_ship, shipped, completed, cancelled')
    parser.add_argument('--cdp-url', default='http://127.0.0.1:9222', help='Chrome CDP URL')
    
    args = parser.parse_args()
    
    global CHROME_CDP_URL
    CHROME_CDP_URL = args.cdp_url
    
    # Build URL with status parameter
    base_url = "https://seller.shopee.sg/portal/sale/order"
    
    # Shopee uses 'type' parameter, not 'status'
    status_map = {
        'all': '',
        'new': 'type=toship&source=to_process&sort_by=confirmed_date_desc',
        'to_ship': 'type=toship&source=to_process&sort_by=confirmed_date_desc',
        'ready_to_ship': 'type=ready_to_ship&source=to_process&sort_by=confirmed_date_desc',
        'processed': 'type=toship&source=processed&sort_by=confirmed_date_desc',
        'shipped': 'type=shipped&sort_by=confirmed_date_desc',
        'completed': 'type=completed&sort_by=confirmed_date_desc',
        'cancelled': 'type=cancelled&sort_by=confirmed_date_desc'
    }
    
    status_param = status_map.get(args.status, '')
    if status_param:
        url = f"{base_url}?{status_param}"
    else:
        url = base_url
    
    print(f"[INFO] Fetching orders with status: {args.status}")
    print(f"[INFO] URL: {url}\n")
    
    asyncio.run(extract_orders(url))


if __name__ == "__main__":
    main()
