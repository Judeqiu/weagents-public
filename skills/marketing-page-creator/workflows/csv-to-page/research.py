#!/usr/bin/env python3
"""
Product Research Script
Extracts REAL product data from e-commerce sites and saves to CSV

⚠️  WARNING: This script ONLY extracts real data from actual websites.
    NEVER use mock, simulated, or fake data.
    
    If extraction fails, the script will report failure - 
    DO NOT manually create fake data to replace it.

🌐  NOTE FOR E-COMMERCE SITES:
    For Amazon, eBay, and other e-commerce sites, use `mychrome` skill first:
    1. Start Chrome with CDP: ssh spost "export DISPLAY=:99 && ~/start-chrome.sh"
    2. Use mychrome skill or connect via CDP for best anti-bot protection
    3. This script uses Playwright which works well, but mychrome/CDP is stealthier

Usage:
    python research.py --site amazon --query "electronics deals" --max-items 20
    python research.py --site amazon --category "fashion" --output ./products.csv

Verification:
    After running, check the CSV contains real URLs from the source site:
    head -5 products_*.csv
"""

import argparse
import asyncio
import csv
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright


class ProductResearcher:
    """Research products from e-commerce sites"""
    
    def __init__(self):
        self.products = []
        
    async def research_amazon_uk(self, query, max_items=20):
        """Research products from Amazon UK"""
        print(f"🔍 Researching Amazon UK: '{query}'")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--window-size=1920,1080',
                ]
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            
            page = await context.new_page()
            
            try:
                # Navigate to search results
                search_term = query.replace(' ', '+')
                url = f"https://www.amazon.co.uk/s?k={search_term}&s=price-desc-rank"
                
                print(f"  → Loading: {url}")
                await page.goto(url, wait_until='domcontentloaded', timeout=60000)
                
                # Wait for products
                await page.wait_for_selector(
                    '[data-component-type="s-search-result"]', 
                    timeout=30000
                )
                await page.wait_for_timeout(2000)
                
                # Extract products
                products = await page.query_selector_all(
                    '[data-component-type="s-search-result"]'
                )
                print(f"  ✓ Found {len(products)} products")
                
                for i, product in enumerate(products[:max_items]):
                    try:
                        item = await self._extract_amazon_product(product)
                        if item and item['title'] and item['title'] != 'N/A':
                            self.products.append(item)
                            print(f"    [{len(self.products)}] {item['title'][:50]}...")
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"  ✗ Error: {e}")
            finally:
                await browser.close()
        
        return self.products
    
    async def _extract_amazon_product(self, product):
        """Extract data from an Amazon product element"""
        item = {}
        
        # Title
        title = "N/A"
        for selector in ['h2 a span', 'h2 span', '.a-size-medium.a-color-base']:
            elem = await product.query_selector(selector)
            if elem:
                text = await elem.inner_text()
                if text and len(text.strip()) > 5:
                    title = text.strip()
                    break
        item['title'] = title
        
        # Link
        link = "N/A"
        elem = await product.query_selector('h2 a')
        if elem:
            href = await elem.get_attribute('href')
            if href:
                link = f"https://www.amazon.co.uk{href}" if href.startswith('/') else href
        item['link'] = link
        
        # Price
        price = "N/A"
        price_elem = await product.query_selector('.a-price .a-offscreen')
        if price_elem:
            price = await price_elem.inner_text()
        item['price'] = price.strip() if price != "N/A" else ""
        
        # Original price
        original_price = ""
        orig_elem = await product.query_selector('.a-text-price .a-offscreen')
        if orig_elem:
            original_price = await orig_elem.inner_text()
        item['original_price'] = original_price.strip()
        
        # Rating
        rating = ""
        rating_elem = await product.query_selector('.a-icon-alt')
        if rating_elem:
            text = await rating_elem.inner_text()
            match = re.search(r'([\d.]+)', text)
            if match:
                rating = match.group(1)
        item['rating'] = rating
        
        # Reviews
        reviews = ""
        reviews_elem = await product.query_selector(
            'a.a-link-normal[href*="#customerReviews"] span'
        )
        if reviews_elem:
            text = await reviews_elem.inner_text()
            reviews = text.strip('()').replace(',', '')
        item['reviews'] = reviews
        
        # Image
        image = ""
        img_elem = await product.query_selector('.s-image')
        if img_elem:
            image = await img_elem.get_attribute('src')
        item['image'] = image
        
        # Category detection
        item['category'] = self._detect_category(title)
        
        return item
    
    def _detect_category(self, title):
        """Detect product category from title"""
        title_lower = title.lower()
        categories = {
            'electronics': ['headphone', 'watch', 'phone', 'laptop', 'camera', 'speaker', 'case'],
            'fashion': ['dress', 'shirt', 'shoe', 'bag', 'handbag', 'coat', 'jacket', 'fashion'],
            'home': ['vacuum', 'kitchen', 'cooker', 'cleaner', 'furniture', 'home', 'bed']
        }
        
        for category, keywords in categories.items():
            if any(kw in title_lower for kw in keywords):
                return category
        return 'other'
    
    def save_to_csv(self, filename=None):
        """Save products to CSV file"""
        if not self.products:
            print("No products to save")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"products_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'title', 'price', 'original_price', 'rating', 
                'reviews', 'link', 'image', 'category'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.products)
        
        print(f"\n✓ Saved {len(self.products)} products to: {filename}")
        return filename


async def main():
    parser = argparse.ArgumentParser(description='Research products from e-commerce sites')
    parser.add_argument('--site', default='amazon', help='Site to research (amazon)')
    parser.add_argument('--query', required=True, help='Search query')
    parser.add_argument('--max-items', type=int, default=20, help='Max items to extract')
    parser.add_argument('--output', help='Output CSV filename')
    
    args = parser.parse_args()
    
    researcher = ProductResearcher()
    
    if args.site == 'amazon':
        await researcher.research_amazon_uk(args.query, args.max_items)
    else:
        print(f"Site '{args.site}' not yet supported")
        return
    
    if researcher.products:
        filename = researcher.save_to_csv(args.output)
        
        # Also save JSON for reference
        json_file = args.output.replace('.csv', '.json') if args.output else None
        if not json_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_file = f"products_{timestamp}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(researcher.products, f, indent=2, ensure_ascii=False)
        print(f"✓ Also saved JSON to: {json_file}")
        
        # Verification output
        print("\n" + "="*60)
        print("🔍 DATA VERIFICATION - Check before proceeding:")
        print("="*60)
        print(f"   File: {filename}")
        print(f"   Products: {len(researcher.products)}")
        print(f"\n   First product:")
        first = researcher.products[0]
        print(f"   - Title: {first.get('title', 'N/A')[:50]}...")
        print(f"   - URL: {first.get('link', 'N/A')[:60]}...")
        print(f"   - Image: {first.get('image', 'N/A')[:50]}...")
        print("\n   ✓ Ensure URLs are from actual source domain")
        print("   ✓ Ensure images are from actual source domain")
        print("   ✗ DO NOT proceed if data looks fake/placedholder")
        print("="*60)
    else:
        print("\n❌ FAILED: No products extracted")
        print("   DO NOT create fake data manually.")
        print("   Try different search terms or check site availability.")


if __name__ == "__main__":
    asyncio.run(main())
