#!/usr/bin/env python3
"""
chromecdp-popup-handler.py - Smart popup detection and handling for Chrome CDP

This script connects to Chrome CDP and intelligently detects common blocking popups:
- Cookie consent banners
- Warning/alert dialogs
- Newsletter signup overlays
- Age verification gates
- Location permission requests
- Notification permission requests
"""

import asyncio
import json
import sys
import re
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass

# Try to import websockets, handle if not available
try:
    import websockets
except ImportError:
    print("Installing websockets...")
    import subprocess
    try:
        # Try user install first (safer for system Python)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "websockets", "-q"])
    except subprocess.CalledProcessError:
        # Fallback to system install with --break-system-packages if needed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets", "-q", "--break-system-packages"])
    import websockets

# Popup detection patterns (selectors and text content)
POPUP_PATTERNS = {
    "cookie_consent": {
        "selectors": [
            '[class*="cookie"]',
            '[class*="consent"]',
            '[id*="cookie"]',
            '[id*="consent"]',
            '.cc-banner',
            '.cc-window',
            '#onetrust-banner-sdk',
            '#CybotCookiebotDialog',
            '[data-testid="cookie-banner"]',
            '.gdpr-banner',
            '[aria-label*="cookie" i]',
        ],
        "text_patterns": [
            r"accept.*cookie",
            r"cookie.*consent",
            r"i accept",
            r"agree.*cookie",
            r"allow.*cookie",
            r"got it",
            r"ok,? i understand",
        ],
        "close_selectors": [
            'button:has-text("Accept")',
            'button:has-text("Got it")',
            'button:has-text("OK")',
            'button:has-text("Agree")',
            'button:has-text("Allow")',
            '.cc-allow',
            '.cc-accept',
            '[class*="accept"]',
        ],
    },
    "warning_alert": {
        "selectors": [
            '[role="alert"]',
            '[role="dialog"]',
            '.alert',
            '.warning',
            '.notification',
            '[class*="popup"]',
            '[class*="modal"]',
            '[class*="overlay"]',
        ],
        "text_patterns": [
            r"warning",
            r"alert",
            r"attention",
            r"important",
        ],
        "close_selectors": [
            'button:has-text("Close")',
            'button:has-text("Dismiss")',
            'button:has-text("Continue")',
            'button:has-text("OK")',
            '[class*="close"]',
            '[class*="dismiss"]',
            '[aria-label*="close" i]',
            '.modal-close',
        ],
    },
    "newsletter": {
        "selectors": [
            '[class*="newsletter"]',
            '[class*="subscribe"]',
            '[id*="newsletter"]',
            '[class*="signup"]',
        ],
        "text_patterns": [
            r"subscribe",
            r"newsletter",
            r"sign up.*email",
        ],
        "close_selectors": [
            'button:has-text("No thanks")',
            'button:has-text("Maybe later")',
            'button:has-text("Close")',
            '[class*="close"]',
            '[class*="dismiss"]',
        ],
    },
    "age_verification": {
        "selectors": [
            '[class*="age"]',
            '[class*="verify"]',
            '[id*="age"]',
        ],
        "text_patterns": [
            r"18.*older",
            r"age.*verify",
            r"enter.*birth",
            r"you must be",
        ],
        "close_selectors": [
            'button:has-text("Enter")',
            'button:has-text("Yes")',
            'button:has-text("I am 18")',
            'button:has-text("Confirm")',
        ],
    },
}


@dataclass
class DetectedPopup:
    popup_type: str
    confidence: float
    element_info: Dict
    close_recommendation: str


class PopupHandler:
    def __init__(self, cdp_url: str = "http://127.0.0.1:9222"):
        # FIXED: Always use port 9222
        self.cdp_url = "http://127.0.0.1:9222"
        self.ws_url = None
        
    async def get_websocket_url(self) -> str:
        """Get WebSocket debugger URL from Chrome CDP"""
        import urllib.request
        with urllib.request.urlopen(f"{self.cdp_url}/json/list") as response:
            pages = json.loads(response.read())
            if not pages:
                raise RuntimeError("No pages found in Chrome")
            # Use the first non-background page
            for page in pages:
                if page.get("type") == "page":
                    return page["webSocketDebuggerUrl"]
            return pages[0]["webSocketDebuggerUrl"]
    
    async def execute_js(self, ws, script: str) -> any:
        """Execute JavaScript in the page via CDP"""
        cmd = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": script,
                "returnByValue": True
            }
        }
        await ws.send(json.dumps(cmd))
        response = json.loads(await ws.recv())
        
        if "result" in response and "result" in response["result"]:
            return response["result"]["result"].get("value")
        return None
    
    async def click_element(self, ws, selector: str) -> bool:
        """Click an element by selector"""
        script = f"""
            (function() {{
                const el = document.querySelector('{selector}');
                if (el) {{
                    el.click();
                    return true;
                }}
                return false;
            }})()
        """
        return await self.execute_js(ws, script)
    
    def calculate_confidence(self, popup_type: str, selectors_found: List[str], text_matches: bool) -> float:
        """Calculate confidence score for popup detection"""
        confidence = 0.0
        
        # Base confidence from selectors
        selector_weight = min(len(selectors_found) * 0.2, 0.6)
        confidence += selector_weight
        
        # Text match bonus
        if text_matches:
            confidence += 0.3
        
        # Specific popup type adjustments
        if popup_type == "cookie_consent" and len(selectors_found) >= 2:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    async def detect_popups(self, ws) -> List[DetectedPopup]:
        """Detect popups in the current page"""
        detected = []
        
        for popup_type, patterns in POPUP_PATTERNS.items():
            # Check for selectors
            selectors_js = json.dumps(patterns["selectors"])
            script = f"""
                (function() {{
                    const selectors = {selectors_js};
                    const found = [];
                    for (const sel of selectors) {{
                        try {{
                            const el = document.querySelector(sel);
                            if (el && el.offsetParent !== null) {{
                                found.push({{
                                    selector: sel,
                                    text: el.innerText?.substring(0, 100) || '',
                                    visible: el.offsetParent !== null
                                }});
                            }}
                        }} catch(e) {{}}
                    }}
                    return found;
                }})()
            """
            
            elements = await self.execute_js(ws, script)
            
            if elements and len(elements) > 0:
                # Check text patterns
                text_matches = False
                page_text = await self.execute_js(ws, "document.body?.innerText?.substring(0, 2000) || ''")
                
                if page_text:
                    text_lower = page_text.lower()
                    for pattern in patterns["text_patterns"]:
                        if re.search(pattern, text_lower, re.IGNORECASE):
                            text_matches = True
                            break
                
                confidence = self.calculate_confidence(popup_type, elements, text_matches)
                
                if confidence >= 0.4:  # Threshold for detection
                    # Find best close button
                    close_js = json.dumps(patterns["close_selectors"])
                    close_script = f"""
                        (function() {{
                            const selectors = {close_js};
                            for (const sel of selectors) {{
                                try {{
                                    const el = document.querySelector(sel);
                                    if (el && el.offsetParent !== null) {{
                                        return sel;
                                    }}
                                }} catch(e) {{}}
                            }}
                            return null;
                        }})()
                    """
                    close_selector = await self.execute_js(ws, close_script)
                    
                    detected.append(DetectedPopup(
                        popup_type=popup_type,
                        confidence=confidence,
                        element_info=elements[0],
                        close_recommendation=close_selector or "Manual intervention needed"
                    ))
        
        return detected
    
    async def handle_popup(self, ws, popup: DetectedPopup, auto_close: bool = False) -> bool:
        """Handle a detected popup"""
        print(f"🎯 Detected: {popup.popup_type} (confidence: {popup.confidence:.0%})")
        print(f"   Element: {popup.element_info.get('selector', 'unknown')}")
        print(f"   Close with: {popup.close_recommendation}")
        
        if auto_close and popup.close_recommendation != "Manual intervention needed":
            success = await self.click_element(ws, popup.close_recommendation)
            if success:
                print(f"   ✅ Closed automatically")
                return True
            else:
                print(f"   ❌ Failed to close")
        
        return False
    
    async def scan_and_handle(self, auto_close: bool = False, verbose: bool = True) -> Dict:
        """Main entry point - scan page and handle popups"""
        try:
            self.ws_url = await self.get_websocket_url()
            
            async with websockets.connect(self.ws_url) as ws:
                if verbose:
                    print(f"🔌 Connected to Chrome CDP")
                
                # Detect popups
                popups = await self.detect_popups(ws)
                
                if not popups:
                    if verbose:
                        print("✅ No blocking popups detected")
                    return {"detected": [], "handled": []}
                
                print(f"\n🚨 Found {len(popups)} popup(s):\n")
                
                handled = []
                for popup in sorted(popups, key=lambda p: p.confidence, reverse=True):
                    success = await self.handle_popup(ws, popup, auto_close)
                    handled.append({
                        "type": popup.popup_type,
                        "confidence": popup.confidence,
                        "closed": success
                    })
                    print()
                
                return {"detected": popups, "handled": handled}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"error": str(e)}


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Smart popup detection for Chrome CDP")
    parser.add_argument("--auto-close", action="store_true", help="Automatically close detected popups")
    parser.add_argument("--cdp-url", default="http://127.0.0.1:9222", help="Chrome CDP URL")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    
    args = parser.parse_args()
    
    handler = PopupHandler(cdp_url=args.cdp_url)
    result = asyncio.run(handler.scan_and_handle(
        auto_close=args.auto_close,
        verbose=not args.quiet
    ))
    
    if "error" in result:
        sys.exit(1)
    
    # Exit code based on whether popups were found
    if result["detected"]:
        sys.exit(2)  # Popups detected
    sys.exit(0)  # No popups


if __name__ == "__main__":
    main()
