#!/usr/bin/env python3
"""
Easy-Paper CLI - Download CAIE past papers from easy-paper.com

WARNING: This site has anti-automation measures that prevent headless browsers
from accessing the search interface. The automation may only work with:
1. Visible browser window (--visible flag)
2. Desktop environment (X11/Wayland)

For headless servers, use the HAR extraction method instead:
    python3 extract_from_har.py capture.har

Usage:
    python easypaper_cli.py -c 9702 -y 2024 -s s -p 12 -v 1 --visible
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

from playwright.async_api import async_playwright


class EasyPaperDownloader:
    def __init__(self, output_dir: str = "downloads", headless: bool = True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headless = headless
        
    async def search_and_download(self, query: str, filename: str = None, 
                                  target_year: str = None, target_paper: str = None) -> str:
        print(f"\n{'='*70}")
        print(f"Easy-Paper Downloader")
        print(f"{'='*70}")
        print(f"Search: {query}")
        if target_year:
            print(f"Target Year: {target_year}")
        if target_paper:
            print(f"Target Paper: {target_paper}")
        print(f"Headless: {self.headless}")
        print(f"{'='*70}\n")
        
        if self.headless:
            print("WARNING: Headless mode may not work due to anti-automation measures.")
            print("Consider using --visible flag or HAR extraction method.\n")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.headless,
                args=['--disable-blink-features=AutomationControlled'] if not self.headless else []
            )
            
            context = await browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                locale='zh-CN',
            )
            
            if not self.headless:
                await context.add_init_script(
                    'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                )
            
            page = await context.new_page()
            
            try:
                # Navigate
                print("[1/5] Loading search page...")
                await page.goto("https://easy-paper.com/papersearch", 
                               wait_until="networkidle", timeout=60000)
                await asyncio.sleep(5)
                
                # Check if we got the landing page instead of search page
                body_text = await page.evaluate('() => document.body.innerText')
                if "Learners Today" in body_text or "Leaders Tomorrow" in body_text:
                    print("\n✗ ANTI-AUTOMATION: Site served landing page instead of search interface")
                    print("  This happens when the site detects headless browser.")
                    print("  Solutions:")
                    print("    1. Use --visible flag (requires GUI)")
                    print("    2. Use HAR extraction method (recommended)")
                    print("       python3 extract_from_har.py capture.har")
                    return None
                
                await page.screenshot(path=self.output_dir / "_debug_1.png")
                
                # Click Files tab
                print("\n[2/5] Switching to Files tab...")
                await page.evaluate('''
                    () => {
                        const tabs = document.querySelectorAll('button, .el-tabs__item, [role="tab"]');
                        for (let tab of tabs) {
                            if (tab.textContent.includes('Files')) {
                                tab.click();
                                return true;
                            }
                        }
                        return false;
                    }
                ''')
                await asyncio.sleep(3)
                
                # Search
                print("\n[3/5] Searching...")
                search_input = await page.wait_for_selector('input[type="text"].el-input__inner', 
                                                            timeout=10000)
                await search_input.fill(query)
                await asyncio.sleep(0.5)
                await search_input.press("Enter")
                await asyncio.sleep(6)
                
                await page.screenshot(path=self.output_dir / "_debug_2.png")
                
                # Get results
                print("\n[4/5] Analyzing results...")
                
                results = await page.query_selector_all('[class*="file-item"], .el-card')
                print(f"  Found {len(results)} results")
                
                if not results:
                    print("  ✗ No results found")
                    return None
                
                # Show top results
                result_data = []
                for i, r in enumerate(results[:10]):
                    text = await r.inner_text()
                    if '.pdf' in text or '_' in text:
                        result_data.append({'element': r, 'text': text[:100]})
                        print(f"    [{i+1}] {text[:60]}")
                
                if not result_data:
                    print("  ✗ No valid PDF results")
                    return None
                
                # Click first result
                print(f"\n  Clicking result...")
                await result_data[0]['element'].click()
                
                print("  Waiting for PDF page...")
                try:
                    await page.wait_for_url("**/paperdownload/**", timeout=15000)
                except:
                    pass
                
                await asyncio.sleep(10)
                
                # Download
                print("\n[5/5] Saving PDF...")
                
                current_url = page.url
                if "paperdownload" not in current_url:
                    print(f"  ✗ Not on download page: {current_url}")
                    return None
                
                if not filename:
                    filename = f"{query.replace(' ', '_')}.pdf"
                
                output_path = self.output_dir / filename
                pdf_data = await page.pdf(format='A4', print_background=True)
                
                with open(output_path, 'wb') as f:
                    f.write(pdf_data)
                
                size = output_path.stat().st_size
                print(f"  ✓ Saved: {output_path} ({size:,} bytes)")
                
                await browser.close()
                return str(output_path)
                
            except Exception as e:
                print(f"\n✗ Error: {e}")
                import traceback
                traceback.print_exc()
                await page.screenshot(path=self.output_dir / "_debug_error.png")
                await browser.close()
                return None


def build_filename(args) -> str:
    if not args.subject:
        return None
    parts = [str(args.subject)]
    if args.year:
        parts.append(str(args.year))
    if args.session:
        parts.append(str(args.session))
    if args.paper:
        parts.append(str(args.paper))
    if args.variant:
        parts.append(str(args.variant))
    return f"{'_'.join(parts)}.pdf"


async def main():
    parser = argparse.ArgumentParser(
        description="Download CAIE past papers from easy-paper.com",
        epilog="""
Examples:
  python easypaper_cli.py -c 9702 -y 2024 -s s -p 12 -v 1 --visible
  python easypaper_cli.py -c 9702 --visible

Note: --visible flag is often required due to anti-automation measures.
For headless servers, use: python3 extract_from_har.py capture.har
        """
    )
    
    parser.add_argument("--subject", "-c", help="Subject code (e.g., 9702)")
    parser.add_argument("--year", "-y", help="Year (e.g., 2024)")
    parser.add_argument("--session", "-s", help="Session: s, w, m")
    parser.add_argument("--paper", "-p", help="Paper number (e.g., 12)")
    parser.add_argument("--variant", "-v", help="Variant (1, 2, 3)")
    parser.add_argument("--output", "-o", default="downloads", help="Output directory")
    parser.add_argument("--visible", action="store_true", 
                       help="Show browser window (often required)")
    parser.add_argument("--query", "-q", help="Raw search query")
    
    args = parser.parse_args()
    
    query = args.query or args.subject or ""
    if not query:
        print("Error: Provide --query or --subject")
        sys.exit(1)
        
    filename = build_filename(args) if not args.query else None
    
    downloader = EasyPaperDownloader(
        output_dir=args.output,
        headless=not args.visible
    )
    
    result = await downloader.search_and_download(
        query, filename,
        target_year=args.year,
        target_paper=args.paper
    )
    
    if result:
        print(f"\n{'='*70}")
        print(f"✓ SUCCESS: {result}")
        print(f"{'='*70}")
        sys.exit(0)
    else:
        print(f"\n{'='*70}")
        print("✗ Download failed")
        print("\nAlternative method:")
        print("  1. Manually search and open paper in browser")
        print("  2. Capture HAR file (DevTools → Network → Save HAR)")
        print("  3. Run: python3 extract_from_har.py capture.har")
        print(f"{'='*70}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
