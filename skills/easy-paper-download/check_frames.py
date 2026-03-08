#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1366, 'height': 768})
        
        await page.goto("https://easy-paper.com/papersearch", wait_until="networkidle")
        await asyncio.sleep(5)
        
        print(f"Number of frames: {len(page.frames)}")
        
        for i, frame in enumerate(page.frames):
            try:
                url = frame.url
                title = await frame.title() if frame != page.main_frame else "(main)"
                print(f"\nFrame {i}: {url[:80] if url else 'no url'}")
                
                # Count inputs in this frame
                inputs = await frame.query_selector_all('input')
                print(f"  Inputs: {len(inputs)}")
                
                for inp in inputs[:3]:
                    try:
                        ph = await inp.get_attribute('placeholder') or ''
                        print(f"    - placeholder: {ph[:40] if ph else 'None'}")
                    except:
                        pass
                        
            except Exception as e:
                print(f"  Error: {e}")
        
        await browser.close()

asyncio.run(check())
