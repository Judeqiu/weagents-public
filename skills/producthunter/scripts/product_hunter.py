#!/usr/bin/env python3
"""
ProductHunter - E-commerce Product Information Extractor using Chrome CDP with lextok-search fallback.

This script extracts product information from e-commerce websites using Chrome
DevTools Protocol (CDP). When CDP is unavailable or extraction fails, it falls
back to lextok-search (Brave Search API) to find product information.

Requirements:
    - Chrome running with --remote-debugging-port=9222 (for CDP mode)
    - playwright: pip install playwright && playwright install chromium
    - OR Brave API key configured in lextok-search/config.json (for fallback mode)
"""

import argparse
import asyncio
import csv
import json
import os
import random
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, quote_plus

# Try to import playwright for CDP mode
try:
    from playwright.async_api import async_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Warning: playwright not installed. Will use lextok-search fallback only.")
    print("Run: pip install playwright && playwright install chromium for CDP mode")

# Import lextok-search for fallback
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lextok-search'))
    from search import LexTokSearchClient
    LEXTOK_AVAILABLE = True
except ImportError:
    LEXTOK_AVAILABLE = False

DEFAULT_CDP_URL = os.environ.get("CHROME_CDP_URL", "http://127.0.0.1:9222")
DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

STEALTH_SCRIPTS = [
    """() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); }""",
    """() => { Object.defineProperty(navigator, 'plugins', { get: () => [{name: "Chrome PDF Plugin"}, {name: "Chrome PDF Viewer"}] }); }""",
    """() => { window.chrome = { runtime: {}, loadTimes: () => {} }; }""",
]

PLATFORM_SELECTORS = {
    "amazon": {
        "single": {
            "title": "#productTitle, #title",
            "price": ".a-price .a-offscreen, #priceblock_dealprice",
            "original_price": ".a-text-price .a-offscreen",
            "rating": "[data-hook='average-star-rating'] .a-icon-alt",
            "review_count": "#acrCustomerReviewText",
            "availability": "#availability span",
            "brand": "#bylineInfo",
            "images": "#landingImage, #main-image",
            "description": "#feature-bullets ul",
        },
        "multiple": {
            "container": "[data-component-type='s-search-result']",
            "title": "h2 a span",
            "price": ".a-price .a-offscreen",
            "link": "h2 a",
            "image": ".s-image",
        }
    },
    "ebay": {
        "single": {
            "title": "h1.x-item-title-label",
            "price": ".notranslate",
            "images": "#icImg",
            "description": "#viTabs_0_is",
        },
        "multiple": {
            "container": ".s-item",
            "title": ".s-item__title",
            "price": ".s-item__price",
            "link": ".s-item__link",
            "image": ".s-item__image-img",
        }
    },
    "generic": {
        "single": {
            "title": "h1, .product-title",
            "price": ".price, .product-price",
            "rating": ".rating, .stars",
            "images": "img.product-image",
            "description": ".description, .product-description",
        },
        "multiple": {
            "container": ".product, .product-item",
            "title": ".title, h2, h3",
            "price": ".price",
            "link": "a",
            "image": "img",
        }
    }
}


class ProductHunter:
    ALL_FIELDS = [
        "timestamp", "source_url", "title", "description", "price", "original_price",
        "currency", "rating", "review_count", "availability", "brand", "images"
    ]
    
    def __init__(self, cdp_url: str = DEFAULT_CDP_URL, delay: float = 0, use_search_fallback: bool = True):
        self.cdp_url = cdp_url
        self.delay = delay
        self.use_search_fallback = use_search_fallback
        self.browser = None
        self.context = None
        self.playwright = None
        self.search_client = None
        
        # Initialize search client if available
        if LEXTOK_AVAILABLE and use_search_fallback:
            try:
                self.search_client = LexTokSearchClient()
                print("✓ LexTok search fallback enabled")
            except ValueError as e:
                print(f"⚠ Search fallback not available: {e}")
        
    def _detect_platform(self, url: str) -> str:
        domain = urlparse(url).netloc.lower()
        if "amazon" in domain:
            return "amazon"
        elif "ebay" in domain:
            return "ebay"
        else:
            return "generic"
    
    async def connect(self) -> bool:
        if not PLAYWRIGHT_AVAILABLE:
            print("Playwright not available. Will use lextok-search fallback.")
            return False
            
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.connect_over_cdp(self.cdp_url)
            
            contexts = self.browser.contexts
            if contexts:
                self.context = contexts[0]
            else:
                self.context = await self.browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent=DEFAULT_USER_AGENT
                )
            
            print(f"✓ Connected to Chrome at {self.cdp_url}")
            return True
        except Exception as e:
            print(f"⚠ Failed to connect to Chrome: {e}")
            if self.use_search_fallback and self.search_client:
                print("✓ Will use lextok-search fallback")
            else:
                print("Ensure Chrome is running with: --remote-debugging-port=9222")
                print("Or configure Brave API key in lextok-search/config.json")
            return False
    
    async def _apply_stealth(self, page):
        for script in STEALTH_SCRIPTS:
            await page.add_init_script(script)
    
    async def _random_delay(self):
        if self.delay > 0:
            await asyncio.sleep(self.delay + random.uniform(0.5, 1.5))
    
    def _extract_price(self, text: str) -> tuple:
        if not text:
            return None, None
        price_match = re.search(r'[\d,]+\.?\d*', text.replace(',', ''))
        if price_match:
            price = float(price_match.group().replace(',', ''))
            currency = None
            if '$' in text:
                currency = 'USD'
            elif '€' in text:
                currency = 'EUR'
            elif '£' in text:
                currency = 'GBP'
            return price, currency
        return None, None
    
    def _extract_rating(self, text: str) -> Optional[float]:
        if not text:
            return None
        match = re.search(r'(\d+\.?\d*)', text)
        if match:
            rating = float(match.group(1))
            if 0 <= rating <= 5:
                return rating
        return None
    
    async def _extract_single_product(self, page, url: str, screenshot: Optional[str] = None) -> Dict:
        platform = self._detect_platform(url)
        selectors = PLATFORM_SELECTORS.get(platform, PLATFORM_SELECTORS["generic"])["single"]
        
        product = {
            "timestamp": datetime.now().isoformat(),
            "source_url": url,
            "title": None, "description": None, "price": None,
            "original_price": None, "currency": None, "rating": None,
            "review_count": None, "availability": None, "brand": None, "images": None,
        }
        
        # Title
        try:
            el = await page.query_selector(selectors.get("title", "h1"))
            if el:
                product["title"] = (await el.inner_text()).strip()[:500]
        except:
            pass
        
        # Price
        try:
            el = await page.query_selector(selectors.get("price", ""))
            if el:
                text = await el.inner_text()
                price, currency = self._extract_price(text)
                product["price"] = price
                product["currency"] = currency
        except:
            pass
        
        # Original price
        try:
            el = await page.query_selector(selectors.get("original_price", ""))
            if el:
                text = await el.inner_text()
                price, _ = self._extract_price(text)
                product["original_price"] = price
        except:
            pass
        
        # Rating
        try:
            el = await page.query_selector(selectors.get("rating", ""))
            if el:
                text = await el.inner_text()
                product["rating"] = self._extract_rating(text)
        except:
            pass
        
        # Availability
        try:
            el = await page.query_selector(selectors.get("availability", ""))
            if el:
                product["availability"] = (await el.inner_text()).strip()[:200]
        except:
            pass
        
        # Images
        try:
            img_els = await page.query_selector_all(selectors.get("images", "img"))
            urls = []
            for img in img_els[:10]:
                src = await img.get_attribute("src")
                if src and src.startswith("http"):
                    urls.append(src)
            if urls:
                product["images"] = "|".join(list(dict.fromkeys(urls)))
        except:
            pass
        
        # Screenshot
        if screenshot:
            await page.screenshot(path=screenshot, full_page=True)
            print(f"Screenshot saved: {screenshot}")
        
        return product
    
    async def _extract_multiple_products(self, page, url: str, max_products: int = 50, scroll: bool = False, scroll_pause: float = 2.0) -> List[Dict]:
        platform = self._detect_platform(url)
        selectors = PLATFORM_SELECTORS.get(platform, PLATFORM_SELECTORS["generic"])["multiple"]
        
        products = []
        
        if scroll:
            for _ in range(5):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(scroll_pause)
        
        containers = await page.query_selector_all(selectors.get("container", ".product"))
        print(f"Found {len(containers)} product containers")
        
        for container in containers[:max_products]:
            try:
                product = {
                    "timestamp": datetime.now().isoformat(),
                    "source_url": url,
                    "title": None, "description": None, "price": None,
                    "original_price": None, "currency": None, "rating": None,
                    "review_count": None, "availability": None, "brand": None, "images": None,
                }
                
                # Title
                try:
                    el = await container.query_selector(selectors.get("title", "h2"))
                    if el:
                        product["title"] = (await el.inner_text()).strip()[:500]
                except:
                    pass
                
                # Price
                try:
                    el = await container.query_selector(selectors.get("price", ""))
                    if el:
                        text = await el.inner_text()
                        price, currency = self._extract_price(text)
                        product["price"] = price
                        product["currency"] = currency
                except:
                    pass
                
                # Link
                try:
                    el = await container.query_selector(selectors.get("link", "a"))
                    if el:
                        href = await el.get_attribute("href")
                        if href:
                            if href.startswith("http"):
                                product["source_url"] = href
                            else:
                                base = urlparse(url)
                                product["source_url"] = f"{base.scheme}://{base.netloc}{href}"
                except:
                    pass
                
                # Image
                try:
                    el = await container.query_selector(selectors.get("image", "img"))
                    if el:
                        src = await el.get_attribute("src")
                        if src:
                            product["images"] = src
                except:
                    pass
                
                if product["title"] or product["price"]:
                    products.append(product)
            except Exception as e:
                print(f"Warning: Error extracting product: {e}")
        
        return products
    
    async def extract_from_url(self, url: str, multiple: bool = False, max_products: int = 50,
                               screenshot: Optional[str] = None, scroll: bool = False,
                               scroll_pause: float = 2.0, wait: int = 0, timeout: int = 30000) -> List[Dict]:
        # If CDP is not connected, use search fallback
        if not self.context:
            if self.use_search_fallback and self.search_client:
                print(f"Using lextok-search fallback for: {url}")
                return await self._extract_from_search(url, max_products)
            else:
                print("Error: CDP not connected and search fallback not available")
                return []
        
        await self._random_delay()
        page = await self.context.new_page()
        
        try:
            await self._apply_stealth(page)
            print(f"Navigating to: {url}")
            await page.goto(url, wait_until="networkidle", timeout=timeout)
            
            if wait > 0:
                await asyncio.sleep(wait)
            
            if multiple:
                products = await self._extract_multiple_products(page, url, max_products, scroll, scroll_pause)
                print(f"Extracted {len(products)} products via CDP")
            else:
                product = await self._extract_single_product(page, url, screenshot)
                products = [product]
                print(f"Extracted: {product.get('title', 'Unknown')} via CDP")
            
            # If no products found and fallback is enabled, try search
            if not products and self.use_search_fallback and self.search_client:
                print("No products found via CDP. Trying lextok-search fallback...")
                return await self._extract_from_search(url, max_products)
            
            return products
        except Exception as e:
            print(f"Error extracting from {url} via CDP: {e}")
            # Fallback to search on error
            if self.use_search_fallback and self.search_client:
                print("Trying lextok-search fallback...")
                return await self._extract_from_search(url, max_products)
            return []
        finally:
            await page.close()
    
    async def _extract_from_search(self, url: str, max_products: int = 10) -> List[Dict]:
        """Extract product information using lextok-search as fallback."""
        if not self.search_client:
            print("Search client not available")
            return []
        
        try:
            # Extract domain/product info from URL for search query
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            # Build search query from URL components
            query_parts = []
            
            # Add site-specific keywords
            if "amazon" in domain:
                query_parts.append("site:amazon.com")
            elif "ebay" in domain:
                query_parts.append("site:ebay.com")
            elif "walmart" in domain:
                query_parts.append("site:walmart.com")
            elif "target" in domain:
                query_parts.append("site:target.com")
            elif "bestbuy" in domain:
                query_parts.append("site:bestbuy.com")
            
            # Extract product name from URL path
            # Remove common e-commerce path segments
            path_clean = re.sub(r'/(dp|gp/product|item|p|prod)/[^/]+', '', path)
            path_clean = re.sub(r'/(s|search|sch).*', '', path_clean)
            path_segments = [s for s in path_clean.split('/') if s and len(s) > 2]
            
            if path_segments:
                # Use the last meaningful path segment as product hint
                product_hint = path_segments[-1].replace('-', ' ').replace('_', ' ')
                query_parts.append(product_hint)
            
            # If URL has search params, extract them
            if parsed.query:
                search_match = re.search(r'[kq]=([^&]+)', parsed.query)
                if search_match:
                    search_term = search_match.group(1).replace('+', ' ').replace('%20', ' ')
                    query_parts.append(search_term)
            
            # Build final query
            if len(query_parts) <= 1 and parsed.query:
                # Fallback: use URL as hint for general product search
                search_query = f"product {domain}"
            else:
                search_query = ' '.join(query_parts)
            
            print(f"Search query: '{search_query}'")
            
            # Perform search with content fetching
            search_results = self.search_client.search(
                query=search_query,
                limit=min(max_products, 10),
                include_content=True
            )
            
            products = []
            for result in search_results.get("results", [])[:max_products]:
                product = self._parse_search_result_to_product(result, url)
                if product.get("title") or product.get("description"):
                    products.append(product)
            
            print(f"Extracted {len(products)} products via lextok-search")
            return products
            
        except Exception as e:
            print(f"Search fallback error: {e}")
            return []
    
    def _parse_search_result_to_product(self, result: Dict, source_url: str) -> Dict:
        """Parse a search result into product format."""
        product = {
            "timestamp": datetime.now().isoformat(),
            "source_url": result.get("url", source_url),
            "title": None,
            "description": None,
            "price": None,
            "original_price": None,
            "currency": None,
            "rating": None,
            "review_count": None,
            "availability": None,
            "brand": None,
            "images": None,
        }
        
        # Extract title
        title = result.get("title", "")
        if title:
            # Clean up common search result suffixes
            title = re.sub(r'\s*[-|]\s*(Amazon|eBay|Walmart|Target|Best Buy|Official Site).*$', '', title, flags=re.IGNORECASE)
            product["title"] = title[:500]
        
        # Extract description from snippet and content
        description = result.get("description", "")
        content = result.get("content", "")
        
        # Use content if available and description is short
        if content and len(description) < 100:
            # Extract first meaningful paragraph from content
            content_lines = [l.strip() for l in content.split('\n') if len(l.strip()) > 50]
            if content_lines:
                description = content_lines[0][:1000]
        
        product["description"] = description[:2000] if description else None
        
        # Try to extract price from title, description, or content
        price_text = f"{title} {description} {content}"
        price, currency = self._extract_price(price_text)
        if price:
            product["price"] = price
            product["currency"] = currency
        
        # Try to extract rating from content
        rating = self._extract_rating(content)
        if rating:
            product["rating"] = rating
        
        # Extract brand from title or source
        source = result.get("source", "")
        product["brand"] = source if source else None
        
        return product
    
    def save_to_csv(self, products: List[Dict], filepath: str, fields: List[str] = None):
        if not products:
            print("No products to save")
            return
        
        if fields is None:
            fields = self.ALL_FIELDS
        
        os.makedirs(os.path.dirname(os.path.abspath(filepath)) or ".", exist_ok=True)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(products)
        
        print(f"Saved {len(products)} products to: {filepath}")
    
    def save_to_json(self, products: List[Dict], filepath: str):
        if not products:
            print("No products to save")
            return
        
        os.makedirs(os.path.dirname(os.path.abspath(filepath)) or ".", exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(products)} products to: {filepath}")
    
    async def process_natural_language_request(self, request: str) -> tuple:
        request_lower = request.lower()
        
        platform = None
        if "amazon" in request_lower:
            platform = "amazon"
            base_url = "https://www.amazon.com"
        elif "ebay" in request_lower:
            platform = "ebay"
            base_url = "https://www.ebay.com"
        else:
            domain_match = re.search(r'(\w+\.(?:com|co\.\w+|org|net))', request_lower)
            if domain_match:
                base_url = f"https://www.{domain_match.group(1)}"
            else:
                base_url = "https://www.google.com/search"
        
        stop_words = ['find', 'get', 'search', 'for', 'on', 'from', 'with', 'under', 'over', 'price']
        words = request_lower.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        query = ' '.join(keywords[:5])
        
        if platform == "amazon":
            url = f"{base_url}/s?k={quote_plus(query)}"
        elif platform == "ebay":
            url = f"{base_url}/sch/i.html?_nkw={quote_plus(query)}"
        else:
            url = f"{base_url}?q={quote_plus(query)}"
        
        print(f"Parsed request: '{request}'")
        print(f"Detected platform: {platform or 'generic'}")
        print(f"Generated URL: {url}")
        
        return url, True
    
    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


async def main():
    parser = argparse.ArgumentParser(
        description="ProductHunter - Extract product info using Chrome CDP with lextok-search fallback"
    )
    parser.add_argument("--url", help="Target URL to extract products from")
    parser.add_argument("--request", help="Natural language request")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--multiple", action="store_true", help="Extract multiple products")
    parser.add_argument("--max-products", type=int, default=50, help="Max products to extract")
    parser.add_argument("--fields", help="Comma-separated fields to extract")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Output format")
    parser.add_argument("--scroll", action="store_true", help="Scroll to load more products")
    parser.add_argument("--scroll-pause", type=float, default=2.0, help="Pause between scrolls")
    parser.add_argument("--delay", type=float, default=0, help="Delay between requests")
    parser.add_argument("--timeout", type=int, default=30000, help="Page load timeout")
    parser.add_argument("--screenshot", help="Save screenshot path")
    parser.add_argument("--batch", help="File with URLs to process")
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help="Chrome CDP URL")
    parser.add_argument("--wait", type=int, default=0, help="Wait time after page load")
    parser.add_argument("--no-search-fallback", action="store_true", 
                        help="Disable lextok-search fallback when CDP fails")
    
    args = parser.parse_args()
    
    if not args.url and not args.request and not args.batch:
        parser.print_help()
        print("Error: Must provide --url, --request, or --batch")
        sys.exit(1)
    
    use_fallback = not args.no_search_fallback
    hunter = ProductHunter(cdp_url=args.cdp_url, delay=args.delay, use_search_fallback=use_fallback)
    
    try:
        cdp_connected = await hunter.connect()
        
        if not cdp_connected and not (use_fallback and hunter.search_client):
            print("\n❌ Failed to connect to Chrome and search fallback not available")
            print("Options:")
            print("1. Start Chrome with: google-chrome --remote-debugging-port=9222")
            print("2. Configure Brave API key in lextok-search/config.json")
            sys.exit(1)
        
        all_products = []
        
        # Process batch file
        if args.batch:
            with open(args.batch, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            for url in urls:
                products = await hunter.extract_from_url(url, args.multiple, args.max_products)
                all_products.extend(products)
        # Process natural language request
        elif args.request:
            url, is_multiple = await hunter.process_natural_language_request(args.request)
            products = await hunter.extract_from_url(url, is_multiple, args.max_products, 
                                                      args.screenshot, args.scroll, args.scroll_pause,
                                                      args.wait, args.timeout)
            all_products.extend(products)
        # Process single URL
        else:
            products = await hunter.extract_from_url(args.url, args.multiple, args.max_products,
                                                      args.screenshot, args.scroll, args.scroll_pause,
                                                      args.wait, args.timeout)
            all_products.extend(products)
        
        # Save results
        if all_products:
            fields = args.fields.split(',') if args.fields else None
            if args.format == "json":
                hunter.save_to_json(all_products, args.output)
            else:
                hunter.save_to_csv(all_products, args.output, fields)
            
            # Print summary
            print(f"\n{'='*50}")
            print(f"Extraction complete!")
            print(f"Total products: {len(all_products)}")
            print(f"Output: {args.output}")
            print(f"{'='*50}")
        else:
            print("No products extracted")
            sys.exit(1)
            
    finally:
        await hunter.close()


if __name__ == "__main__":
    asyncio.run(main())
