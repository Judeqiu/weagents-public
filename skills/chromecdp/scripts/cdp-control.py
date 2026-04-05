#!/usr/bin/env python3
"""Simple CDP controller for Chrome on port 9222"""
import asyncio
import json
import sys
import urllib.request

try:
    import websockets
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "websockets", "-q"])
    import websockets

CDP_URL = "http://127.0.0.1:9222"

async def get_ws_url():
    """Get WebSocket debugger URL"""
    with urllib.request.urlopen(f"{CDP_URL}/json/list") as resp:
        pages = json.loads(resp.read())
        for p in pages:
            if p.get("type") == "page" and not p.get("parentId"):
                return p["webSocketDebuggerUrl"]
    return None

async def navigate(url):
    """Navigate to URL"""
    ws_url = await get_ws_url()
    if not ws_url:
        print("No page found")
        return
    
    async with websockets.connect(ws_url) as ws:
        # Enable page
        await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
        await ws.recv()
        
        # Navigate
        await ws.send(json.dumps({
            "id": 2, 
            "method": "Page.navigate",
            "params": {"url": url}
        }))
        
        # Wait for response
        while True:
            msg = json.loads(await ws.recv())
            if msg.get("id") == 2:
                print(f"Navigated to: {url}")
                break
            if msg.get("method") == "Page.loadEventFired":
                print("Page loaded!")
                break

async def scroll_down():
    """Scroll down the page"""
    ws_url = await get_ws_url()
    if not ws_url:
        return
    
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": "window.scrollBy(0, 800)"}
        }))
        await ws.recv()
        print("Scrolled down")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cdp-control.py <command> [args]")
        print("Commands: navigate <url>, scroll")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "navigate" and len(sys.argv) > 2:
        asyncio.run(navigate(sys.argv[2]))
    elif cmd == "scroll":
        asyncio.run(scroll_down())
    else:
        print(f"Unknown command: {cmd}")
