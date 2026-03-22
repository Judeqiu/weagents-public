#!/usr/bin/env python3
"""
Chrome CDP Helper - Easy Chrome DevTools Protocol automation.

This module provides a simple interface for controlling Chrome via CDP.
Can be used as a library or CLI tool.

Examples:
    # As CLI
    python3 chrome_cdp_helper.py --url https://example.com --screenshot /tmp/example.png
    
    # As library
    from chrome_cdp_helper import ChromeCDPHelper
    
    async with ChromeCDPHelper() as chrome:
        page = await chrome.new_page()
        await page.goto("https://example.com")
        await page.screenshot(path="/tmp/screenshot.png")
"""

import argparse
import asyncio
import json
import os
import sys
from contextlib import asynccontextmanager
from typing import Optional, Any, List
from urllib.parse import urljoin

# Check for playwright
try:
    from playwright.async_api import async_playwright, Page, Browser, BrowserContext
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright")
    print("Then: playwright install chromium")
    sys.exit(1)


class ChromeCDPHelper:
    """
    Helper class for Chrome DevTools Protocol automation.
    
    Simplifies connecting to Chrome CDP and performing common operations.
    
    Usage:
        async with ChromeCDPHelper() as chrome:
            page = await chrome.new_page()
            await page.goto("https://example.com")
            await page.screenshot(path="/tmp/screenshot.png")
    """
    
    DEFAULT_CDP_URL = "http://localhost:9222"
    
    def __init__(self, cdp_url: Optional[str] = None):
        """
        Initialize Chrome CDP Helper.
        
        Args:
            cdp_url: Chrome CDP endpoint URL. Defaults to CHROME_CDP_URL env var or http://localhost:9222
        """
        self.cdp_url = cdp_url or os.environ.get("CHROME_CDP_URL", self.DEFAULT_CDP_URL)
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self._playwright = None
        
    async def connect(self) -> "ChromeCDPHelper":
        """
        Connect to Chrome via CDP.
        
        Returns:
            self for method chaining
            
        Raises:
            ConnectionError: If cannot connect to Chrome CDP
        """
        self._playwright = await async_playwright().start()
        
        try:
            self.browser = await self._playwright.chromium.connect_over_cdp(self.cdp_url)
            
            # Use existing context or create new one
            contexts = self.browser.contexts
            if contexts:
                self.context = contexts[0]
            else:
                self.context = await self.browser.new_context(
                    viewport={"width": 1920, "height": 1080}
                )
            
            print(f"✓ Connected to Chrome at {self.cdp_url}")
            return self
            
        except Exception as e:
            await self._playwright.stop()
            raise ConnectionError(f"Failed to connect to Chrome at {self.cdp_url}: {e}")
    
    async def close(self):
        """Close browser connection and cleanup."""
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()
        print("✓ Chrome connection closed")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    def new_page(self) -> asyncio.Future[Page]:
        """
        Create a new page in the browser context.
        
        Returns:
            Future that resolves to a new Page
        """
        if not self.context:
            raise RuntimeError("Not connected. Call connect() first.")
        return self.context.new_page()
    
    async def goto(self, url: str, wait_until: str = "load", timeout: int = 30000) -> Page:
        """
        Navigate to a URL in a new page.
        
        Args:
            url: URL to navigate to
            wait_until: When to consider navigation complete (load, domcontentloaded, networkidle)
            timeout: Navigation timeout in milliseconds
            
        Returns:
            The page object
        """
        page = await self.new_page()
        await page.goto(url, wait_until=wait_until, timeout=timeout)
        return page
    
    async def screenshot(
        self, 
        url: str, 
        output_path: str, 
        full_page: bool = False,
        wait_time: int = 2
    ) -> str:
        """
        Take a screenshot of a URL.
        
        Args:
            url: URL to screenshot
            output_path: Path to save the screenshot
            full_page: Whether to capture full page or just viewport
            wait_time: Additional wait time after page load (seconds)
            
        Returns:
            Path to the saved screenshot
        """
        page = await self.goto(url, wait_until="networkidle")
        
        if wait_time > 0:
            await asyncio.sleep(wait_time)
        
        await page.screenshot(path=output_path, full_page=full_page)
        await page.close()
        
        print(f"✓ Screenshot saved to: {output_path}")
        return output_path
    
    async def extract_content(self, url: str, selector: Optional[str] = None) -> dict:
        """
        Extract content from a URL.
        
        Args:
            url: URL to extract content from
            selector: Optional CSS selector to extract specific element content
            
        Returns:
            Dictionary with title, url, and content
        """
        page = await self.goto(url, wait_until="networkidle")
        
        await asyncio.sleep(1)  # Wait for dynamic content
        
        result = {
            "url": page.url,
            "title": await page.title(),
        }
        
        if selector:
            element = await page.query_selector(selector)
            if element:
                result["content"] = await element.inner_html()
                result["text"] = await element.inner_text()
            else:
                result["error"] = f"Selector '{selector}' not found"
        else:
            result["content"] = await page.content()
            # Extract main text content
            result["text"] = await page.evaluate("""() => {
                const main = document.querySelector('main, article, [role="main"], .content');
                return main ? main.innerText : document.body.innerText;
            }""")
        
        await page.close()
        return result
    
    async def evaluate(self, url: str, script: str) -> Any:
        """
        Execute JavaScript on a page and return result.
        
        Args:
            url: URL to navigate to
            script: JavaScript code to execute
            
        Returns:
            Result of the JavaScript execution
        """
        page = await self.goto(url)
        result = await page.evaluate(script)
        await page.close()
        return result
    
    async def get_cdp_version(self) -> dict:
        """Get Chrome CDP version information."""
        import aiohttp
        
        version_url = urljoin(self.cdp_url, "/json/version")
        async with aiohttp.ClientSession() as session:
            async with session.get(version_url) as response:
                return await response.json()
    
    async def list_pages(self) -> List[dict]:
        """List all open pages in Chrome."""
        import aiohttp
        
        list_url = urljoin(self.cdp_url, "/json/list")
        async with aiohttp.ClientSession() as session:
            async with session.get(list_url) as response:
                return await response.json()


async def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Chrome CDP Helper - Web automation via Chrome DevTools Protocol"
    )
    parser.add_argument("--cdp-url", "-c", 
                       default=os.environ.get("CHROME_CDP_URL", "http://localhost:9222"),
                       help="Chrome CDP URL (default: http://localhost:9222)")
    parser.add_argument("--url", "-u", help="URL to navigate to")
    parser.add_argument("--screenshot", "-s", help="Take screenshot and save to path")
    parser.add_argument("--full-page", "-f", action="store_true",
                       help="Capture full page screenshot")
    parser.add_argument("--extract-content", "-e", action="store_true",
                       help="Extract page content")
    parser.add_argument("--selector", help="CSS selector for extraction")
    parser.add_argument("--evaluate", "-j", help="Execute JavaScript and return result")
    parser.add_argument("--wait", "-w", type=int, default=2,
                       help="Wait time after page load (seconds)")
    parser.add_argument("--version", "-v", action="store_true",
                       help="Show Chrome CDP version")
    parser.add_argument("--list-pages", "-l", action="store_true",
                       help="List all open pages")
    
    args = parser.parse_args()
    
    # Check Chrome CDP connection first
    if args.version:
        helper = ChromeCDPHelper(args.cdp_url)
        try:
            version = await helper.get_cdp_version()
            print(json.dumps(version, indent=2))
        except Exception as e:
            print(f"✗ Cannot connect to Chrome: {e}")
            print(f"\nTroubleshooting:")
            print(f"1. Check Chrome is running: curl {args.cdp_url}/json/version")
            print(f"2. Start Chrome with: google-chrome --remote-debugging-port=9222")
            sys.exit(1)
        return
    
    if args.list_pages:
        helper = ChromeCDPHelper(args.cdp_url)
        try:
            pages = await helper.list_pages()
            for i, page in enumerate(pages, 1):
                print(f"\n[{i}] {page.get('title', 'N/A')}")
                print(f"    URL: {page.get('url', 'N/A')}")
                print(f"    Type: {page.get('type', 'N/A')}")
        except Exception as e:
            print(f"✗ Error: {e}")
            sys.exit(1)
        return
    
    if not args.url:
        parser.print_help()
        print("\nError: --url is required (unless using --version or --list-pages)")
        sys.exit(1)
    
    # Execute requested action
    async with ChromeCDPHelper(args.cdp_url) as chrome:
        if args.screenshot:
            await chrome.screenshot(
                args.url, 
                args.screenshot, 
                full_page=args.full_page,
                wait_time=args.wait
            )
        
        elif args.extract_content:
            content = await chrome.extract_content(args.url, args.selector)
            print(json.dumps(content, indent=2, ensure_ascii=False))
        
        elif args.evaluate:
            result = await chrome.evaluate(args.url, args.evaluate)
            print(json.dumps(result, indent=2, ensure_ascii=False) if isinstance(result, (dict, list)) else result)
        
        else:
            # Just navigate and show basic info
            page = await chrome.goto(args.url)
            await asyncio.sleep(args.wait)
            
            info = {
                "url": page.url,
                "title": await page.title(),
            }
            print(json.dumps(info, indent=2))
            
            await page.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✓ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
