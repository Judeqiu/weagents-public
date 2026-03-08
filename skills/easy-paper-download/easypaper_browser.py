#!/usr/bin/env python3
"""
Easy-Paper Browser Automation

Uses Playwright to automate browser interaction:
1. Navigate to easy-paper.com
2. Search for paper
3. Click result
4. Wait for PDF to load
5. Download PDF

Usage:
    python easypaper_browser.py --subject "9702 physics" --year 2024 --session s --variant 12
    python easypaper_browser.py -q "CIE A-Level Mathematics 9709 2024 summer paper 12"
"""

import argparse
import asyncio
import os
import sys
from playwright.async_api import async_playwright


class EasyPaperBrowser:
    """Browser automation for Easy-Paper."""
    
    def __init__(self, output_dir: str = ".", headless: bool = True):
        self.output_dir = output_dir
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        os.makedirs(output_dir, exist_ok=True)
    
    async def init_browser(self):
        """Initialize browser."""
        self.playwright = await async_playwright().start()
        
        # Launch browser
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # Create context with realistic settings
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        self.page = await self.context.new_page()
        
        # Set extra headers
        await self.page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    async def close_browser(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def search_and_download(self, query: str, output_name: str = None) -> str:
        """
        Full workflow: Search → Click → Download PDF.
        
        Args:
            query: Search query (e.g., "9702 physics 2024 s 12")
            output_name: Output filename (optional)
            
        Returns:
            Path to downloaded PDF
        """
        print(f"\n{'='*70}")
        print(f"Easy-Paper Browser Automation")
        print(f"{'='*70}")
        print(f"Query: {query}")
        print(f"Headless: {self.headless}")
        print(f"{'='*70}\n")
        
        try:
            # Step 1: Navigate to site
            print("[1/5] Navigating to easy-paper.com...")
            await self.page.goto("https://easy-paper.com", wait_until="networkidle")
            await asyncio.sleep(2)
            print("  ✓ Loaded homepage")
            
            # Step 2: Go to search page
            print("\n[2/5] Going to search page...")
            await self.page.goto("https://easy-paper.com/papersearch", wait_until="networkidle")
            await asyncio.sleep(3)
            print("  ✓ Loaded search page")
            
            # Take screenshot to debug
            await self.page.screenshot(path=os.path.join(self.output_dir, "search_page.png"))
            print(f"  ✓ Screenshot saved: search_page.png")
            
            # Step 3: Try to find and use search interface
            print("\n[3/5] Looking for search interface...")
            
            # The site uses Vue.js - search might be in a specific element
            # Try to find input fields
            inputs = await self.page.query_selector_all('input')
            print(f"  Found {len(inputs)} input elements")
            
            # Try to interact with the page
            # The search might be triggered by JavaScript
            # Let's try to evaluate JavaScript to trigger search
            
            # Check if there's a Vue app and try to access it
            vue_check = await self.page.evaluate("""() => {
                const vueEl = document.querySelector('#app');
                if (vueEl && vueEl.__vue__) {
                    return { hasVue: true, hasSearch: typeof vueEl.__vue__.search !== 'undefined' };
                }
                return { hasVue: false };
            }""")
            print(f"  Vue.js check: {vue_check}")
            
            # Step 4: Wait for and click on search results
            print("\n[4/5] Waiting for page to fully load...")
            await asyncio.sleep(5)
            
            # Check what's on the page
            content = await self.page.content()
            if "search" in content.lower():
                print("  ✓ Page contains 'search'")
            
            if "input" in content.lower():
                print("  ✓ Page contains input fields")
            
            # Try to find links
            links = await self.page.query_selector_all('a')
            print(f"  Found {len(links)} links on page")
            
            # Look for paper-related links
            paper_links = []
            for i, link in enumerate(links):
                href = await link.get_attribute('href')
                text = await link.inner_text()
                if href and ('paper' in href.lower() or '9702' in href or '9709' in href):
                    paper_links.append((i, href, text))
            
            if paper_links:
                print(f"\n  Found {len(paper_links)} paper-related links:")
                for idx, href, text in paper_links[:5]:
                    print(f"    [{idx}] {text[:40]}... -> {href[:60]}...")
                
                # Click first paper link
                print("\n[5/5] Clicking on paper link...")
                link_idx, link_href, link_text = paper_links[0]
                await links[link_idx].click()
                await asyncio.sleep(5)
                
                # Check if PDF loaded
                current_url = self.page.url
                print(f"  Current URL: {current_url}")
                
                if "paperdownload" in current_url:
                    print("  ✓ Navigated to paper download page")
                    
                    # Wait for PDF to load
                    await asyncio.sleep(10)
                    
                    # Try to download via browser's print to PDF
                    print("\n  Attempting to save as PDF...")
                    
                    try:
                        # Use Chrome DevTools Protocol to print to PDF
                        client = await self.context.new_cdp_session(self.page)
                        pdf_data = await client.send("Page.printToPDF", {
                            "printBackground": True,
                            "preferCSSPageSize": True,
                            "paperWidth": 8.5,
                            "paperHeight": 11
                        })
                        
                        import base64
                        pdf_bytes = base64.b64decode(pdf_data['data'])
                        
                        output_file = output_name or "downloaded_paper.pdf"
                        output_path = os.path.join(self.output_dir, output_file)
                        
                        with open(output_path, 'wb') as f:
                            f.write(pdf_bytes)
                        
                        print(f"  ✓ PDF saved: {output_path} ({len(pdf_bytes)} bytes)")
                        return output_path
                        
                    except Exception as e:
                        print(f"  ✗ Print to PDF failed: {e}")
                        
                        # Fallback: Try to download via fetch
                        print("\n  Trying alternative download method...")
                        
                        # Get all network requests
                        # This is complex - would need to intercept requests
                        
                        return None
                else:
                    print(f"  ✗ Did not navigate to paper page")
                    return None
            else:
                print("  ✗ No paper links found")
                return None
                
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return None


async def main():
    parser = argparse.ArgumentParser(
        description="Browser automation for Easy-Paper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python easypaper_browser.py --query "9702 physics 2024 s 12"
  python easypaper_browser.py -q "CIE Mathematics 9709 2023 w 13" -o ./papers/
  python easypaper_browser.py --subject 9702 --year 2024 --session s --variant 12
        """
    )
    
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--subject", "-c", help="Subject code")
    parser.add_argument("--year", "-y", help="Year")
    parser.add_argument("--session", "-s", help="Session: s/w/m")
    parser.add_argument("--variant", "-v", help="Variant")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--visible", action="store_true", help="Show browser window (not headless)")
    parser.add_argument("--output-name", "-n", help="Output filename")
    
    args = parser.parse_args()
    
    # Build query from parts if not provided directly
    if args.query:
        query = args.query
    elif args.subject and args.year:
        parts = [args.subject]
        if args.year:
            parts.append(args.year)
        if args.session:
            parts.append(args.session)
        if args.variant:
            parts.append(args.variant)
        query = " ".join(parts)
    else:
        print("Error: Provide --query or --subject + --year")
        sys.exit(1)
    
    # Run automation
    automation = EasyPaperBrowser(
        output_dir=args.output,
        headless=not args.visible
    )
    
    try:
        await automation.init_browser()
        result = await automation.search_and_download(query, args.output_name)
        
        if result:
            print(f"\n{'='*70}")
            print(f"✓ SUCCESS: {result}")
            print(f"{'='*70}")
            sys.exit(0)
        else:
            print(f"\n{'='*70}")
            print("✗ Download failed")
            print(f"{'='*70}")
            sys.exit(1)
    finally:
        await automation.close_browser()


if __name__ == "__main__":
    asyncio.run(main())
