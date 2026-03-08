#!/usr/bin/env python3
"""
Easy-Paper Downloader - Playwright-based PDF download
"""

import argparse
import asyncio
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

from playwright.async_api import async_playwright, Request, Response


class EasyPaperDownloader:
    """Download papers from easy-paper.com using Playwright."""
    
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_url = None
        self.pdf_data = None
        
    async def download(self, subject: str, year: str = None, session: str = None, 
                       paper: str = None, variant: str = None, headless: bool = True) -> str:
        """
        Download a paper using browser automation.
        
        Args:
            subject: Subject code (e.g., "9702")
            year: Year (e.g., "2024")
            session: Session (s/w/m)
            paper: Paper number
            variant: Variant number
            headless: Run in headless mode
        """
        # Build search query
        query_parts = [subject]
        if year:
            query_parts.append(year)
        if session:
            query_parts.append(session)
        if paper:
            query_parts.append(paper)
        if variant:
            query_parts.append(variant)
        query = " ".join(query_parts)
        
        print(f"\n{'='*70}")
        print(f"Easy-Paper Downloader")
        print(f"{'='*70}")
        print(f"Search: {query}")
        print(f"{'='*70}\n")
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                ]
            )
            
            # Create context with realistic settings
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='Asia/Shanghai',
                permissions=['notifications'],
            )
            
            # Stealth scripts
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en', 'zh-CN'] });
                window.chrome = { runtime: {} };
            """)
            
            page = await context.new_page()
            
            # Track PDF downloads
            pdf_urls = []
            
            async def handle_route(route, request):
                """Intercept PDF requests."""
                url = request.url
                if 'paperdownload' in url or '.pdf' in url:
                    print(f"  [Intercept] PDF URL: {url[:80]}...")
                    pdf_urls.append(url)
                await route.continue_()
            
            await page.route("**/*", handle_route)
            
            try:
                # Step 1: Navigate to search page
                print("[1/6] Loading search page...")
                response = await page.goto(
                    "https://easy-paper.com/papersearch",
                    wait_until="load",
                    timeout=120000
                )
                print(f"  Status: {response.status}")
                
                # Wait for page to fully render
                await asyncio.sleep(8)
                
                # Check what we got
                body_text = await page.evaluate('() => document.body.innerText')
                if "Learners Today" in body_text:
                    print("  Note: Got landing page, waiting for redirect...")
                    await asyncio.sleep(5)
                
                await page.screenshot(path=self.output_dir / "_01_loaded.png")
                print("  ✓ Page loaded")
                
                # Step 2: Click on Files tab
                print("\n[2/6] Switching to Files tab...")
                
                # Try to find and click Files tab
                files_clicked = False
                for selector in ['text=Files', 'button:has-text("Files")', '.el-tabs__item:has-text("Files")']:
                    try:
                        tab = await page.wait_for_selector(selector, timeout=5000)
                        if tab and await tab.is_visible():
                            await tab.click()
                            files_clicked = True
                            print(f"  Clicked Files tab via: {selector}")
                            break
                    except:
                        continue
                
                if not files_clicked:
                    # Try JavaScript click
                    result = await page.evaluate("""
                        () => {
                            const elements = document.querySelectorAll('button, .el-tabs__item, [role="tab"]');
                            for (const el of elements) {
                                if (el.textContent.includes('Files')) {
                                    el.click();
                                    return { success: true, text: el.textContent };
                                }
                            }
                            return { success: false };
                        }
                    """)
                    if result.get('success'):
                        files_clicked = True
                        print(f"  Clicked Files tab via JS")
                    else:
                        print("  Warning: Could not find Files tab")
                
                await asyncio.sleep(3)
                await page.screenshot(path=self.output_dir / "_02_files_tab.png")
                
                # Step 3: Enter search query
                print("\n[3/6] Entering search query...")
                
                # Find search input
                search_input = None
                for attempt in range(3):
                    try:
                        # Try different selectors
                        for selector in [
                            'input[placeholder*="搜索"]',
                            'input[type="text"].el-input__inner',
                            '.search-input input',
                        ]:
                            search_input = await page.query_selector(selector)
                            if search_input:
                                is_visible = await search_input.is_visible()
                                is_enabled = await search_input.is_enabled()
                                if is_visible and is_enabled:
                                    print(f"  Found search input: {selector}")
                                    break
                            search_input = None
                        
                        if search_input:
                            break
                            
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"  Attempt {attempt + 1} failed: {e}")
                        await asyncio.sleep(2)
                
                if not search_input:
                    print("  ✗ Could not find search input")
                    await page.screenshot(path=self.output_dir / "_error_no_input.png")
                    return None
                
                # Clear and type query
                await search_input.fill("")
                await search_input.fill(query)
                print(f"  Typed: {query}")
                
                # Submit search
                await search_input.press("Enter")
                print("  Submitted search")
                
                await asyncio.sleep(6)
                await page.screenshot(path=self.output_dir / "_03_search_results.png")
                
                # Step 4: Find and click on result
                print("\n[4/6] Looking for results...")
                
                # Get all clickable items
                results = await page.query_selector_all('''
                    .file-item, 
                    [class*="file-item"],
                    .el-card,
                    [class*="result"],
                    .list-item
                ''')
                
                print(f"  Found {len(results)} result containers")
                
                # Filter for valid PDF results
                valid_results = []
                for i, result in enumerate(results):
                    try:
                        text = await result.inner_text()
                        if '.pdf' in text.lower() or '_' in text:
                            # Check visibility
                            is_visible = await result.is_visible()
                            if is_visible:
                                valid_results.append({
                                    'index': i,
                                    'element': result,
                                    'text': text.strip()[:100]
                                })
                    except:
                        pass
                
                print(f"  Found {len(valid_results)} valid PDF results")
                
                if not valid_results:
                    print("  ✗ No results found")
                    await page.screenshot(path=self.output_dir / "_error_no_results.png")
                    return None
                
                # Display results
                print("  Results:")
                for i, r in enumerate(valid_results[:10]):
                    print(f"    [{i+1}] {r['text'][:60]}")
                
                # Select best match based on criteria
                target = valid_results[0]
                
                if year or paper:
                    for r in valid_results:
                        text = r['text']
                        year_match = not year or year in text
                        paper_match = not paper or (paper in text or f"qp_{paper}" in text or f"ms_{paper}" in text)
                        if year_match and paper_match:
                            target = r
                            print(f"  Selected match: {r['text'][:60]}")
                            break
                
                # Click on the result
                print(f"\n  Clicking result...")
                
                # Try to find the clickable element within the result
                clickable = await target['element'].query_selector('a, button, [role="button"], .el-icon-arrow-right')
                if clickable:
                    await clickable.click()
                else:
                    await target['element'].click()
                
                print("  Waiting for PDF page to load...")
                
                # Wait for navigation
                try:
                    await page.wait_for_url("**/paperdownload/**", timeout=20000)
                    print("  Navigated to PDF page")
                except:
                    print(f"  Current URL: {page.url}")
                
                await asyncio.sleep(12)
                await page.screenshot(path=self.output_dir / "_04_pdf_page.png")
                
                # Step 5: Capture PDF
                print("\n[5/6] Capturing PDF...")
                
                current_url = page.url
                if "paperdownload" not in current_url:
                    print(f"  ✗ Not on paperdownload page: {current_url}")
                    await page.screenshot(path=self.output_dir / "_error_not_pdf.png")
                    return None
                
                # Method 1: Try to get PDF via browser print
                print("  Method 1: Browser print to PDF...")
                
                # Wait for PDF to fully render
                await asyncio.sleep(10)
                
                # Generate filename
                if year and session and paper:
                    filename = f"{subject}_{year}_{session}{paper}.pdf"
                else:
                    filename = f"{query.replace(' ', '_')}.pdf"
                
                output_path = self.output_dir / filename
                
                # Print to PDF
                pdf_bytes = await page.pdf(
                    format='A4',
                    print_background=True,
                    margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
                )
                
                # Check if PDF is valid (at least 10KB)
                if len(pdf_bytes) < 10000:
                    print(f"  Warning: PDF is small ({len(pdf_bytes)} bytes)")
                    print("  Trying alternative method...")
                    
                    # Method 2: Try to download directly from intercepted URL
                    if pdf_urls:
                        print(f"  Method 2: Download from intercepted URL...")
                        # Get the first PDF URL
                        pdf_url = pdf_urls[0]
                        print(f"  URL: {pdf_url[:80]}...")
                        
                        # Create new request with proper headers
                        cookies = await context.cookies()
                        cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                        
                        # Use page to fetch
                        response = await page.evaluate(f"""
                            async () => {{
                                const response = await fetch("{pdf_url}", {{
                                    method: 'GET',
                                    headers: {{
                                        'Cookie': '{cookie_str}',
                                        'Referer': '{current_url}'
                                    }}
                                }});
                                const blob = await response.blob();
                                return blob.size;
                            }}
                        """)
                        print(f"  Fetch response size: {response}")
                
                # Save PDF
                with open(output_path, 'wb') as f:
                    f.write(pdf_bytes)
                
                file_size = len(pdf_bytes)
                print(f"  ✓ Saved: {output_path} ({file_size:,} bytes)")
                
                await browser.close()
                return str(output_path)
                
            except Exception as e:
                print(f"\n✗ Error: {e}")
                import traceback
                traceback.print_exc()
                
                try:
                    await page.screenshot(path=self.output_dir / "_error.png")
                except:
                    pass
                    
                await browser.close()
                return None


async def main():
    parser = argparse.ArgumentParser(
        description="Download CAIE past papers from easy-paper.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python easypaper_download.py -c 9702 -y 2024 -s s -p 12 -v 1
  python easypaper_download.py -c 9709 -y 2023 -s w -p 42 -v 2
  python easypaper_download.py -c 9702 --visible

Subject Codes:
  9702 = Physics, 9709 = Mathematics, 9701 = Chemistry
  9700 = Biology, 9618 = Computer Science
        """
    )
    
    parser.add_argument("--subject", "-c", required=True, help="Subject code (e.g., 9702)")
    parser.add_argument("--year", "-y", help="Year (e.g., 2024)")
    parser.add_argument("--session", "-s", help="Session: s (May/June), w (Oct/Nov), m (March)")
    parser.add_argument("--paper", "-p", help="Paper number (e.g., 12, 22, 32, 42, 52)")
    parser.add_argument("--variant", "-v", help="Variant (1, 2, 3)")
    parser.add_argument("--output", "-o", default="downloads", help="Output directory")
    parser.add_argument("--visible", action="store_true", help="Show browser window")
    
    args = parser.parse_args()
    
    downloader = EasyPaperDownloader(output_dir=args.output)
    
    result = await downloader.download(
        subject=args.subject,
        year=args.year,
        session=args.session,
        paper=args.paper,
        variant=args.variant,
        headless=not args.visible
    )
    
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


if __name__ == "__main__":
    asyncio.run(main())
