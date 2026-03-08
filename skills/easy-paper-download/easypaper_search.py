#!/usr/bin/env python3
"""
Easy-Paper Search Automation

Automates the Vue.js search interface at easy-paper.com/papersearch
1. Waits for Vue app to render
2. Finds and fills search input
3. Triggers search
4. Clicks result
5. Downloads PDF

Usage:
    python easypaper_search.py --query "9702 physics 2024"
    python easypaper_search.py -q "CIE Mathematics 9709" -y 2024 -s s -p 12
"""

import argparse
import asyncio
import base64
import os
import sys
from playwright.async_api import async_playwright


class EasyPaperSearch:
    """Automates EasyPaper search and download."""
    
    def __init__(self, output_dir: str = ".", headless: bool = True):
        self.output_dir = output_dir
        self.headless = headless
        os.makedirs(output_dir, exist_ok=True)
    
    async def search_and_download(self, query: str, output_name: str = None) -> str:
        """Full workflow: Search → Click → Download PDF."""
        
        print(f"\n{'='*70}")
        print(f"Easy-Paper Search Automation")
        print(f"{'='*70}")
        print(f"Query: {query}")
        print(f"{'='*70}\n")
        
        async with async_playwright() as p:
            # Launch browser with more realistic settings
            browser = await p.chromium.launch(
                headless=self.headless,
                args=['--disable-web-security', '--disable-features=IsolateOrigins,site-per-process']
            )
            context = await browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='zh-CN'
            )
            page = await context.new_page()
            
            try:
                # Step 1: Navigate to search page
                print("[1/7] Loading search page...")
                
                # Enable console logging
                page.on("console", lambda msg: print(f"  [Console] {msg.type}: {msg.text}") if msg.type == "error" else None)
                
                await page.goto("https://easy-paper.com/papersearch", wait_until="networkidle")
                print("  Waiting for Vue to render...")
                await asyncio.sleep(8)  # Wait longer for Vue
                
                # Debug: Take screenshot
                await page.screenshot(path=os.path.join(self.output_dir, "page_loaded.png"))
                print("  ✓ Page loaded and screenshot saved")
                
                # Debug: Get full HTML
                print("\n[DEBUG] Analyzing page structure...")
                html = await page.content()
                
                # Check for Vue app
                has_vue = await page.evaluate("() => typeof window.Vue !== 'undefined' || typeof window.__VUE__ !== 'undefined'")
                print(f"  Vue.js detected: {has_vue}")
                
                # Look for search input in HTML
                if 'placeholder' in html and '搜索' in html:
                    print("  ✓ Found Chinese search placeholder in HTML")
                
                # Check for iframe
                frames = page.frames
                print(f"  Number of frames: {len(frames)}")
                
                # Step 2: Try to find and click on "Files" tab
                print("\n[2/7] Looking for Files tab...")
                
                tab_selectors = [
                    'text=Files',
                    'text=文件',
                    '[class*="tab"]:has-text("Files")',
                    '[class*="tab"]:has-text("文件")',
                ]
                
                files_tab = None
                for selector in tab_selectors:
                    try:
                        elem = await page.wait_for_selector(selector, timeout=3000)
                        if elem:
                            is_visible = await elem.is_visible()
                            if is_visible:
                                files_tab = elem
                                print(f"  ✓ Found Files tab: {selector}")
                                break
                    except:
                        continue
                
                if files_tab:
                    print("  Clicking Files tab...")
                    await files_tab.click()
                    await asyncio.sleep(3)
                
                # Step 3: Look for search input with more patience
                print("\n[3/7] Looking for search input...")
                
                # Wait and retry finding input
                search_input = None
                for attempt in range(3):
                    print(f"  Attempt {attempt + 1}/3...")
                    
                    # Get all inputs including in shadow DOM
                    inputs = await page.query_selector_all('input')
                    print(f"    Found {len(inputs)} input elements")
                    
                    for inp in inputs:
                        try:
                            is_visible = await inp.is_visible()
                            if not is_visible:
                                continue
                            placeholder = await inp.get_attribute('placeholder') or ''
                            type_attr = await inp.get_attribute('type') or ''
                            print(f"    Input: type={type_attr}, placeholder={placeholder[:40] if placeholder else 'None'}")
                            
                            if placeholder and ('搜索' in placeholder or 'search' in placeholder.lower()):
                                search_input = inp
                                print(f"    ✓ Found search input!")
                                break
                        except:
                            continue
                    
                    if search_input:
                        break
                    
                    await asyncio.sleep(2)
                
                if not search_input:
                    print("  Trying JavaScript evaluation...")
                    # Try to find input via JS
                    result = await page.evaluate("""
                        () => {
                            const inputs = document.querySelectorAll('input');
                            for (let inp of inputs) {
                                if (inp.placeholder && (inp.placeholder.includes('搜索') || inp.placeholder.includes('search'))) {
                                    return {
                                        found: true,
                                        placeholder: inp.placeholder,
                                        tagName: inp.tagName,
                                        className: inp.className,
                                        id: inp.id
                                    };
                                }
                            }
                            return { found: false, count: inputs.length };
                        }
                    """)
                    print(f"    JS search result: {result}")
                    
                    # Try to get input by class patterns
                    result2 = await page.evaluate("""
                        () => {
                            // Common Vue input classes
                            const selectors = ['.el-input__inner', '.ant-input', '.van-field__control', 'input[type="text"]'];
                            for (let sel of selectors) {
                                const el = document.querySelector(sel);
                                if (el) return { found: true, selector: sel, placeholder: el.placeholder };
                            }
                            // Check for any visible input
                            const allInputs = document.querySelectorAll('input');
                            for (let inp of allInputs) {
                                const rect = inp.getBoundingClientRect();
                                if (rect.width > 100 && rect.height > 20) {
                                    return { found: true, placeholder: inp.placeholder, rect: {width: rect.width, height: rect.height} };
                                }
                            }
                            return { found: false };
                        }
                    """)
                    print(f"    JS class search: {result2}")
                    
                    if result2.get('found'):
                        # Try to get the element
                        search_input = await page.query_selector('input[placeholder*="搜索"], input[placeholder*="search"], .el-input__inner, input[type="text"]')
                
                if not search_input:
                    print("  ✗ Could not find search input")
                    await page.screenshot(path=os.path.join(self.output_dir, "error_no_input.png"))
                    
                    # Save HTML for debugging
                    with open(os.path.join(self.output_dir, "page_debug.html"), 'w') as f:
                        f.write(html[:100000])  # First 100KB
                    print(f"  Saved debug HTML")
                    return None
                
                # Step 4: Type search query
                print(f"\n[4/7] Typing search query: '{query}'")
                await search_input.fill(query)
                await asyncio.sleep(0.5)
                print("  Submitting search (Enter)...")
                await search_input.press("Enter")
                await asyncio.sleep(5)
                
                # Step 5: Look for results
                print("\n[5/7] Looking for search results...")
                await page.screenshot(path=os.path.join(self.output_dir, "search_results.png"))
                
                # Check if there are results
                content = await page.content()
                if "暂无" in content or "empty" in content.lower():
                    print("  Page shows empty/no results")
                
                # Look for clickable results
                result_selectors = [
                    '.result-item',
                    '[class*="result"]',
                    '.paper-item',
                    'a[href*="paper"]',
                    'a[href*="pdf"]',
                    '.list-item',
                    '[class*="item"] a',
                ]
                
                results = []
                for selector in result_selectors:
                    items = await page.query_selector_all(selector)
                    if items:
                        # Filter visible items
                        visible_items = []
                        for item in items:
                            try:
                                if await item.is_visible():
                                    visible_items.append(item)
                            except:
                                pass
                        if visible_items:
                            results = visible_items
                            print(f"  ✓ Found {len(visible_items)} visible results")
                            break
                
                if not results:
                    print("  ✗ No search results found")
                    return None
                
                # Step 6: Click first result
                print(f"\n[6/7] Clicking first result...")
                first_result = results[0]
                
                # Get result info
                try:
                    text = await first_result.inner_text()
                    href = await first_result.get_attribute('href')
                    print(f"  Result: {text[:60]}...")
                    print(f"  Link: {href}")
                except:
                    print("  (Could not get result details)")
                
                await first_result.click()
                print("  Clicked, waiting for page to load...")
                await asyncio.sleep(10)
                
                # Step 7: Download PDF
                print("\n[7/7] Downloading PDF...")
                
                current_url = page.url
                print(f"  Current URL: {current_url}")
                
                if "paperdownload" in current_url:
                    print("  ✓ On paper download page")
                    await asyncio.sleep(10)
                    
                    # Use browser print to PDF
                    print("  Generating PDF...")
                    
                    try:
                        pdf_data = await page.pdf(
                            format='A4',
                            print_background=True,
                            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
                        )
                        
                        output_file = output_name or f"paper_{query.replace(' ', '_')}.pdf"
                        output_path = os.path.join(self.output_dir, output_file)
                        
                        with open(output_path, 'wb') as f:
                            f.write(pdf_data)
                        
                        size = os.path.getsize(output_path)
                        print(f"  ✓ PDF saved: {output_path} ({size} bytes)")
                        
                        await browser.close()
                        return output_path
                        
                    except Exception as e:
                        print(f"  ✗ Print to PDF failed: {e}")
                        await page.screenshot(path=os.path.join(self.output_dir, "paper_view.png"), full_page=True)
                        print(f"  Screenshot saved as fallback")
                        await browser.close()
                        return None
                else:
                    print(f"  ✗ Not on paper download page")
                    await browser.close()
                    return None
                    
            except Exception as e:
                print(f"\n✗ Error: {e}")
                import traceback
                traceback.print_exc()
                await page.screenshot(path=os.path.join(self.output_dir, "error.png"))
                await browser.close()
                return None


async def main():
    parser = argparse.ArgumentParser(
        description="Automate EasyPaper search and download",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python easypaper_search.py --query "9702 physics 2024"
  python easypaper_search.py -q "CIE Mathematics 9709" -y 2024 -s s -p 12
  python easypaper_search.py --subject 9702 --year 2024 --session s --variant 12 --visible
        """
    )
    
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--subject", "-c", help="Subject code")
    parser.add_argument("--year", "-y", help="Year")
    parser.add_argument("--session", "-s", help="Session (s/w/m)")
    parser.add_argument("--variant", "-v", help="Variant")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--output-name", "-n", help="Output filename")
    parser.add_argument("--visible", action="store_true", help="Show browser window")
    
    args = parser.parse_args()
    
    # Build query
    if args.query:
        query = args.query
    elif args.subject:
        parts = [args.subject]
        if args.year:
            parts.append(args.year)
        if args.session:
            parts.append(args.session)
        if args.variant:
            parts.append(args.variant)
        query = " ".join(parts)
    else:
        print("Error: Provide --query or --subject")
        sys.exit(1)
    
    # Run
    automation = EasyPaperSearch(
        output_dir=args.output,
        headless=not args.visible
    )
    
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


if __name__ == "__main__":
    asyncio.run(main())
