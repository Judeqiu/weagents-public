#!/usr/bin/env python3
"""
Easy-Paper Downloader

Automates PDF downloads from easy-paper.com using Playwright.

NOTE: The site has sophisticated anti-automation measures. This tool tries
multiple strategies but may not work in all environments.

Requirements:
  - Playwright: pip install playwright
  - Browser: playwright install chromium

Usage:
  # Try automated download (may not work due to anti-bot protection)
  python easypaper.py -c 9702 -y 2024 -s s -p 12
  
  # Manual method (always works)
  1. Open https://easy-paper.com/papersearch in your browser
  2. Search for your paper (e.g., "9702 2024 s 12")
  3. Click on result to open PDF
  4. Press Ctrl+P (or Cmd+P) → "Save as PDF"
"""

import argparse
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright


class EasyPaperDownloader:
    """Download papers using Playwright browser automation."""
    
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    async def download(self, query: str, filename: str = None, headless: bool = True) -> str:
        """
        Download paper using browser automation.
        
        Returns:
            Path to downloaded file or None on failure
        """
        print(f"\n{'='*70}")
        print(f"Easy-Paper Downloader")
        print(f"{'='*70}")
        print(f"Search: {query}")
        print(f"Mode: {'Headless' if headless else 'Visible (Xvfb)'}")
        print(f"{'='*70}\n")
        
        async with async_playwright() as p:
            # Launch browser with anti-detection measures
            args = [
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
            
            try:
                browser = await p.chromium.launch(headless=headless, args=args)
            except Exception as e:
                print(f"✗ Failed to launch browser: {e}")
                if not headless:
                    print("  Try: apt-get install xvfb")
                    print("  Then: xvfb-run python easypaper.py ...")
                return None
            
            # Create context with realistic settings
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='Asia/Shanghai',
            )
            
            # Inject stealth scripts
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en', 'zh-CN'] });
                window.chrome = { runtime: {} };
                delete navigator.__proto__.webdriver;
            """)
            
            page = await context.new_page()
            
            try:
                # Step 1: Load page
                print("[1/5] Loading search page...")
                await page.goto('https://easy-paper.com/papersearch', 
                               wait_until='load', timeout=120000)
                await asyncio.sleep(8)
                
                # Check if we got the Vue app or landing page
                body_text = await page.evaluate('() => document.body.innerText')
                
                if '请输入你想要搜索' not in body_text:
                    print("✗ ANTI-BOT DETECTED: Site served landing page instead of search")
                    print("  The website detects automated browsers.")
                    await page.screenshot(path=self.output_dir / '_anti_bot_detected.png')
                    await browser.close()
                    return None
                
                print("  ✓ Search interface loaded")
                
                # Step 2: Click Files tab
                print("\n[2/5] Switching to Files tab...")
                await page.evaluate("""
                    () => {
                        const tabs = document.querySelectorAll('button, .el-tabs__item');
                        for (const el of tabs) {
                            if (el.textContent.includes('Files')) {
                                el.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)
                await asyncio.sleep(3)
                print("  ✓ Switched to Files")
                
                # Step 3: Search
                print(f"\n[3/5] Searching for: {query}")
                search_input = await page.wait_for_selector('input[type="text"]', timeout=10000)
                await search_input.fill(query)
                await search_input.press('Enter')
                await asyncio.sleep(6)
                print("  ✓ Search submitted")
                
                # Step 4: Find and click result
                print("\n[4/5] Looking for results...")
                
                results = await page.query_selector_all('.file-item, .el-card')
                valid_results = []
                
                for r in results:
                    try:
                        text = await r.inner_text()
                        if '.pdf' in text.lower() and await r.is_visible():
                            valid_results.append({'element': r, 'text': text.strip()})
                    except:
                        pass
                
                print(f"  Found {len(valid_results)} PDF files")
                
                if not valid_results:
                    print("  ✗ No results")
                    await browser.close()
                    return None
                
                # Show top results
                print("  Top results:")
                for i, r in enumerate(valid_results[:5]):
                    print(f"    [{i+1}] {r['text'][:60]}")
                
                # Click first result
                print(f"\n  Clicking: {valid_results[0]['text'][:50]}...")
                await valid_results[0]['element'].click()
                
                # Wait for navigation
                try:
                    await page.wait_for_url('**/paperdownload/**', timeout=20000)
                except:
                    pass
                
                await asyncio.sleep(12)
                
                # Step 5: Download PDF
                print("\n[5/5] Capturing PDF...")
                
                current_url = page.url
                if 'paperdownload' not in current_url:
                    print(f"  ✗ Not on PDF page: {current_url}")
                    await browser.close()
                    return None
                
                # Wait for PDF to render
                await asyncio.sleep(10)
                
                # Generate filename
                if not filename:
                    filename = f"{query.replace(' ', '_')}.pdf"
                
                output_path = self.output_dir / filename
                
                # Save as PDF
                pdf_data = await page.pdf(format='A4', print_background=True)
                
                with open(output_path, 'wb') as f:
                    f.write(pdf_data)
                
                size = len(pdf_data)
                print(f"  ✓ Saved: {output_path} ({size:,} bytes)")
                
                await browser.close()
                return str(output_path)
                
            except Exception as e:
                print(f"\n✗ Error: {e}")
                try:
                    await page.screenshot(path=self.output_dir / '_error.png')
                except:
                    pass
                await browser.close()
                return None


async def main():
    parser = argparse.ArgumentParser(
        description='Download CAIE past papers from easy-paper.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python easypaper.py -c 9702 -y 2024 -s s -p 12 -v 1
  python easypaper.py -c 9709 -y 2023 -s w -p 42
  
Subject Codes:
  9702 = Physics, 9709 = Mathematics, 9701 = Chemistry
  9700 = Biology, 9618 = Computer Science

Note: The site has anti-bot protection. Automation may not work.
If it fails, use the manual method described in the documentation.
        '''
    )
    
    parser.add_argument('--subject', '-c', required=True, help='Subject code (e.g., 9702)')
    parser.add_argument('--year', '-y', help='Year (e.g., 2024)')
    parser.add_argument('--session', '-s', help='Session: s, w, m')
    parser.add_argument('--paper', '-p', help='Paper number (e.g., 12)')
    parser.add_argument('--variant', '-v', help='Variant (1, 2, 3)')
    parser.add_argument('--output', '-o', default='downloads', help='Output directory')
    parser.add_argument('--visible', action='store_true', 
                       help='Use visible browser (requires X11 or xvfb)')
    
    args = parser.parse_args()
    
    # Build search query
    parts = [args.subject]
    if args.year:
        parts.append(args.year)
    if args.session:
        parts.append(args.session)
    if args.paper:
        parts.append(args.paper)
    if args.variant:
        parts.append(args.variant)
    query = ' '.join(parts)
    
    # Build filename
    filename = '_'.join(parts) + '.pdf'
    
    # Download
    downloader = EasyPaperDownloader(output_dir=args.output)
    
    result = await downloader.download(query, filename, headless=not args.visible)
    
    if result:
        print(f"\n{'='*70}")
        print(f"✓ SUCCESS: {result}")
        print(f"{'='*70}")
        sys.exit(0)
    else:
        print(f"\n{'='*70}")
        print("✗ Download failed")
        print("\nThe website has anti-automation protection.")
        print("\nManual method (guaranteed to work):")
        print("  1. Open https://easy-paper.com/papersearch in Chrome/Firefox")
        print("  2. Search for your paper (e.g., \"9702 2024 s 12\")")
        print("  3. Click on result to open PDF viewer")
        print("  4. Press Ctrl+P (or Cmd+P) → Select \"Save as PDF\"")
        print(f"{'='*70}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
