---
name: chromecdp
description: "Browser automation with Chrome on virtual display :99 via port 9222. Use when the user wants to: open a website, browse the web, check a webpage, take a screenshot of a site, interact with web pages, fill forms, click buttons, scroll pages, handle popups/cookie banners, or automate any web-based task. This skill ONLY works with Chrome on port 9222 with VNC display :99. OBEY USER INSTRUCTIONS 100%."
version: 4.0.0
---

# Chrome CDP Browser Automation (Port 9222)

This skill provides browser automation using Chrome on a **virtual display with VNC access**.

## ⚠️ CRITICAL: User Commands Are Absolute

**When user gives an instruction, execute it exactly. Do not:**
- Ask for confirmation unless absolutely necessary
- Suggest alternatives unless asked
- Delay execution
- Second-guess the user

**When user says "execute", you execute. Immediately.**

## ⚠️ CRITICAL: CDP Port 9222 ONLY

This skill uses **ONLY**:
- **CDP Port**: `9222` (fixed)
- **Display**: `:99` (Xvfb virtual display)
- **VNC Port**: `5900` (for visual access)
- **Method**: CDP HTTP API and WebSocket — NOT browser tool

## ⚠️ FORBIDDEN

- ❌ OpenClaw `browser` tool (port 3011)
- ❌ `browser` action with `target: "host"`
- ❌ Any tool that connects to port 3011
- ❌ **Headless Chrome** (`--headless=new`, `--headless`, `ozone-platform=headless`) — **ABSOLUTELY FORBIDDEN**
- ❌ OpenClaw's built-in Chrome launch (defaults to headless)

**Why full-head only:** Chrome MUST be visible on VNC display :99 for seller center logins (Lazada, Shopee, TikTok Shop, Watsons) that require human handoff. Headless Chrome is invisible and breaks session-based workflows. The OpenClaw config (`~/.openclaw/openclaw.json`) has `"headless": false` set explicitly.

## Prerequisites (Must be running)

### 1. Xvfb Virtual Display

```bash
# Start Xvfb on display :99
Xvfb :99 -screen 0 1600x900x24 -ac &

# Verify
pgrep -f "Xvfb :99"
```

### 2. VNC Server (Optional - for visual debugging)

```bash
# Start x11vnc
x11vnc -display :99 -forever -noxdamage -rfbport 5900 &

# Connect with VNC client to port 5900
```

### 3. Chrome on Port 9222 (FULL-HEAD, NOT HEADLESS)

The skill will automatically start Chrome if not running. **It starts full-head GUI Chrome (visible on VNC), never headless.**

**Verify Chrome is running in full-head mode (NOT headless):**
```bash
# This should return NOTHING — if it returns results, Chrome is in headless mode
ps aux | grep chrome | grep headless

# Verify display :99 is active
ps aux | grep 'Xvfb :99' | grep -v grep

# Verify VNC is serving the display
ss -tlnp | grep 5900
```

**If Chrome is in headless mode, recover:**
```bash
killall chrome
bash ~/.openclaw/workspace/skills/chromecdp/scripts/chromecdp-start.sh
```

## Quick Start

### Start Chrome (Port 9222 only)

```bash
~/.openclaw/workspace/skills/chromecdp/scripts/chromecdp-start.sh
```

### Check Status

```bash
~/.openclaw/workspace/skills/chromecdp/scripts/chromecdp-status.sh
```

### Stop Chrome

```bash
~/.openclaw/workspace/skills/chromecdp/scripts/chromecdp-stop.sh
```

### Handle Popups

```bash
python3 ~/.openclaw/workspace/skills/chromecdp/scripts/chromecdp-popup-handler.py --auto-close
```

## Performance & Accuracy Tips

### Reuse WebSocket Connections
CDP uses persistent WebSockets. **Do NOT reconnect per action** — that adds ~50ms overhead each time.
Open one WebSocket, send multiple commands, then close:
```python
ws = websocket.create_connection(f"ws://127.0.0.1:9222/devtools/page/{target_id}")
# Send multiple commands on the SAME connection
ws.send(json.dumps({"id":1, "method":"Page.enable"}))
ws.recv()
ws.send(json.dumps({"id":2, "method":"Page.navigate", "params":{"url":"https://example.com"}}))
# ... more commands ...
ws.close()
```

### Smart Navigation Wait (Don't Use Fixed `sleep`)
Instead of `sleep 3` after navigation, listen for CDP events:
```python
ws.send(json.dumps({"id":1, "method":"Page.enable"}))
ws.recv()
ws.send(json.dumps({"id":2, "method":"Page.navigate", "params":{"url":"https://example.com"}}))
# Listen for load event instead of sleeping
while True:
    msg = json.loads(ws.recv())
    if msg.get("method") == "Page.loadEventFired":
        break
```
For SPAs, wait for a specific element instead:
```python
ws.send(json.dumps({"id":3, "method":"Runtime.evaluate",
    "params":{"expression":"document.querySelector('.result-list') !== null", "returnByValue":True}}))
```

### Fast Screenshots (Use JPEG + clip + optimizeForSpeed)
PNG screenshots are slow and large. Use JPEG with quality 80 + clip region:
```python
ws.send(json.dumps({
    "id": 1,
    "method": "Page.captureScreenshot",
    "params": {
        "format": "jpeg",       # ~3x faster than PNG, much smaller
        "quality": 80,          # 0-100, good balance
        "optimizeForSpeed": True, # faster encoding (zlib q1)
        "captureBeyondViewport": False  # viewport only, skip full-page scroll
    }
}))
```
For element-specific screenshots, use `DOM.getBoxModel` to get bounding box, then pass as `clip`:
```python
# Get element bounding box first
ws.send(json.dumps({"id":1, "method":"DOM.enable"}))
ws.recv()
ws.send(json.dumps({"id":2, "method":"DOM.getDocument"}))
doc = json.loads(ws.recv())
ws.send(json.dumps({"id":3, "method":"DOM.querySelector",
    "params":{"nodeId":doc["result"]["root"]["nodeId"], "selector":"#content"}}))
node = json.loads(ws.recv())
ws.send(json.dumps({"id":4, "method":"DOM.getBoxModel",
    "params":{"nodeId":node["result"]["nodeId"]}}))
box = json.loads(ws.recv())
# Then capture just that region
content = box["result"]["model"]["content"]
x, y = content[0], content[1]
width = content[2] - content[0]
height = content[7] - content[1]
ws.send(json.dumps({"id":5, "method":"Page.captureScreenshot",
    "params":{"format":"jpeg", "quality":80, "optimizeForSpeed":True,
              "clip":{"x":x,"y":y,"width":width,"height":height,"scale":1}}}))
```

### Block Unnecessary Resources for Speed
Block images, fonts, and analytics to speed up page loads 3-5x. **Use `Network.setBlockedURLs`** (preserves cache, unlike `setRequestInterception`):
```python
ws.send(json.dumps({"id":1, "method":"Network.enable"}))
ws.recv()
ws.send(json.dumps({"id":2, "method":"Network.setBlockedURLs",
    "params":{"urls":["*.png","*.jpg","*.jpeg","*.gif","*.svg","*.woff","*.woff2","*.ttf",
                     "*googletagmanager.com/*","*google-analytics.com/*","*doubleclick.net/*"]}}))
ws.recv()
# Now navigate — pages load much faster without these resources
```
**Important:** `Network.setBlockedURLs` preserves the browser cache. Do NOT use `Network.setRequestInterception` or `Fetch.enable` for simple blocking — they disable the cache.

### Use Accessibility Tree for Robust Element Finding
`Runtime.evaluate` with `document.querySelector` is brittle. Use CDP's `Accessibility.getFullAXTree` for semantic element finding:
```python
ws.send(json.dumps({"id":1, "method":"Accessibility.enable"}))
ws.recv()
ws.send(json.dumps({"id":2, "method":"Accessibility.getFullAXTree"}))
tree = json.loads(ws.recv())
# Find elements by role and name
for node in tree["result"]["nodes"]:
    if node.get("role",{}).get("value") == "button" and "Login" in node.get("name",{}).get("value",""):
        backend_node_id = node.get("backendDOMNodeId")
        # Use backendNodeId for stable interaction
```

### Inject Scripts Before Page Load
Use `Page.addScriptToEvaluateOnNewDocument` to inject scripts that run before every page load. **Must call `Page.enable` first:**
```python
ws.send(json.dumps({"id":1, "method":"Page.enable"}))
ws.recv()
# Hide images via CSS before page loads (speeds up rendering)
ws.send(json.dumps({"id":2, "method":"Page.addScriptToEvaluateOnNewDocument",
    "params":{"source":"document.addEventListener('DOMContentLoaded',()=>{"
             "const s=document.createElement('style');"
             "s.textContent='img{visibility:hidden!important}';"
             "document.head.appendChild(s)})"}}))
ws.recv()
# Now navigate — images won't render, pages load faster
```

## Using the Skill — CDP Commands Only

### List Tabs

```bash
curl -s http://127.0.0.1:9222/json/list
```

### Open a Website (New Tab)

```bash
curl -s -X PUT "http://127.0.0.1:9222/json/new?https://example.com"
```

### Activate a Tab

```bash
curl -s "http://127.0.0.1:9222/json/activate/{targetId}"
```

### Close a Tab

```bash
curl -s "http://127.0.0.1:9222/json/close/{targetId}"
```

### Take Screenshot (via CDP WebSocket)

```python
import websocket
import json
import base64

target_id = "YOUR_TARGET_ID"
ws = websocket.create_connection(f"ws://127.0.0.1:9222/devtools/page/{target_id}")

# Fast JPEG screenshot (3x faster than PNG)
ws.send(json.dumps({
    "id": 1,
    "method": "Page.captureScreenshot",
    "params": {
        "format": "jpeg",
        "quality": 80,
        "fromSurface": True,
        "optimizeForSpeed": True
    }
}))

result = json.loads(ws.recv())
if 'result' in result and 'data' in result['result']:
    screenshot_data = result['result']['data']
    with open('/tmp/screenshot.jpg', 'wb') as f:
        f.write(base64.b64decode(screenshot_data))
    print("Screenshot saved")

ws.close()
```

### Navigate with Smart Wait (replaces `sleep 3`)

```python
import websocket
import json

target_id = "YOUR_TARGET_ID"
ws = websocket.create_connection(f"ws://127.0.0.1:9222/devtools/page/{target_id}")

# Enable Page events FIRST
ws.send(json.dumps({"id":1, "method":"Page.enable"}))
ws.recv()

# Navigate
ws.send(json.dumps({"id":2, "method":"Page.navigate",
    "params":{"url":"https://example.com"}}))

# Wait for load event (replaces sleep 3)
while True:
    msg = json.loads(ws.recv())
    if msg.get("method") == "Page.loadEventFired":
        break

# Now page is fully loaded — safe to interact
ws.close()
```

### Click on Element

```python
import websocket
import json

target_id = "YOUR_TARGET_ID"
ws = websocket.create_connection(f"ws://127.0.0.1:9222/devtools/page/{target_id}")

# Enable DOM
ws.send(json.dumps({"id": 1, "method": "DOM.enable"}))
ws.recv()

# Query selector and click
ws.send(json.dumps({
    "id": 2,
    "method": "Runtime.evaluate",
    "params": {"expression": "document.querySelector('button').click()"}
}))

ws.close()
```

### Get Page Content

```python
import websocket
import json

target_id = "YOUR_TARGET_ID"
ws = websocket.create_connection(f"ws://127.0.0.1:9222/devtools/page/{target_id}")

ws.send(json.dumps({
    "id": 1,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.body.innerText",
        "returnByValue": True
    }
}))

result = json.loads(ws.recv())
text = result['result']['result'].get('value', '')
print(text[:2000])  # First 2000 chars

ws.close()
```

## Complete Example

```bash
# Step 1: Ensure Chrome is running on port 9222
exec("bash ~/.openclaw/workspace/skills/chromecdp/scripts/chromecdp-start.sh")

# Step 2: Open URL via CDP
exec("curl -s -X PUT 'http://127.0.0.1:9222/json/new?https://www.lazada.sg'")

# Step 3: Wait for page load
exec("sleep 3")

# Step 4: Get page info
exec("curl -s http://127.0.0.1:9222/json/list")

# Step 5: Take screenshot via CDP (Python)
exec("""python3 << 'PYEOF'
import websocket, json, base64
ws = websocket.create_connection('ws://127.0.0.1:9222/devtools/page/TARGET_ID')
ws.send(json.dumps({'id':1,'method':'Page.captureScreenshot'}))
data = json.loads(ws.recv())['result']['data']
with open('/tmp/screenshot.png', 'wb') as f:
    f.write(base64.b64decode(data))
print('Screenshot saved to /tmp/screenshot.png')
ws.close()
PYEOF""")
```

## Troubleshooting

### Chrome not visible in VNC

Make sure Xvfb is running on :99:
```bash
pgrep -f "Xvfb :99" || Xvfb :99 -screen 0 1600x900x24 -ac &
```

### Port 9222 in use

Kill existing Chrome on port 9222:
```bash
pkill -f "chrome.*9222"
```

Then restart:
```bash
~/.openclaw/workspace/skills/chromecdp/scripts/chromecdp-start.sh
```

### Check what's running on port 9222

```bash
curl http://127.0.0.1:9222/json/version
curl http://127.0.0.1:9222/json/list
```

### WebSocket connection refused

Chrome must be started with `--remote-allow-origins=*` flag. The start script includes this.

## Natural Language Usage

When user says:
- **"Open [website]"** → Execute: `curl -s -X PUT "http://127.0.0.1:9222/json/new?[url]"`
- **"Go to [URL]"** → Execute: CDP `Page.navigate` via websocket
- **"Take a screenshot"** → Execute: CDP `Page.captureScreenshot` via websocket
- **"Click [element]"** → Execute: CDP `Input.dispatchMouseEvent` or JS click via `Runtime.evaluate`
- **"Scroll down"** → Execute: CDP `Input.synthesizeScrollGesture` or JS scroll
- **"Close popups"** → Execute: `python3 ~/.openclaw/workspace/skills/chromecdp/scripts/chromecdp-popup-handler.py --auto-close`

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `chromecdp-start.sh` | Start Chrome on port 9222, display :99 |
| `chromecdp-stop.sh` | Stop Chrome on port 9222 |
| `chromecdp-status.sh` | Check Chrome/Xvfb status |
| `chromecdp-popup-handler.py` | Detect/close popups on port 9222 |

## CDP API Reference

**HTTP Endpoints:**
- `GET /json/version` - Browser version info
- `GET /json/list` - List all tabs/targets
- `GET /json/new?[url]` - Open new tab
- `GET /json/activate/{id}` - Activate tab
- `GET /json/close/{id}` - Close tab

**WebSocket:**
- `ws://127.0.0.1:9222/devtools/page/{targetId}` - Connect to specific tab

**Common CDP Methods:**
- `Page.navigate` - Navigate to URL
- `Page.enable` - Subscribe to page events (REQUIRED before Page.loadEventFired or Page.addScriptToEvaluateOnNewDocument)
- `Page.loadEventFired` - Event: page finished loading (replaces `sleep 3`)
- `Page.captureScreenshot` - Take screenshot (use `format:"jpeg"`, `quality:80`, `optimizeForSpeed:true` for speed)
- `Page.addScriptToEvaluateOnNewDocument` - Inject JS before every page load (requires `Page.enable` first)
- `Runtime.evaluate` - Execute JavaScript
- `DOM.querySelector` - Find element
- `DOM.getBoxModel` - Get element bounding box (use with screenshot `clip`)
- `Accessibility.getFullAXTree` - Get accessibility tree for semantic element finding (robust against DOM changes)
- `Input.dispatchMouseEvent` - Click
- `Input.dispatchKeyEvent` - Type
- `Network.enable` - Enable network tracking (REQUIRED before Network.setBlockedURLs)
- `Network.setBlockedURLs` - Block resources by URL pattern (preserves cache, unlike setRequestInterception)

**Performance Method Comparison:**
| Method | Speed | Robustness | Best For |
|--------|-------|------------|----------|
| `Runtime.evaluate` | Slow (recomputes per element) | Low (DOM-dependent) | Quick one-off scripts |
| `DOM.querySelector` + `DOM.getBoxModel` | Fast | Medium (DOM-dependent) | Known DOM structure |
| `Accessibility.getFullAXTree` | Fastest for queries | High (semantic, survives DOM changes) | Production automation |
| CSS selectors via `Runtime.evaluate` | Fast (no snapshot) | Low (brittle) | Known DOM, skip snapshot overhead |

## See Also

- `references/CDP-OPERATIONS.md` - Detailed CDP commands
- `references/POPUP-TYPES.md` - Popup detection details
- Chrome DevTools Protocol docs: https://chromedevtools.github.io/devtools-protocol/

---

**Remember: User instructions are absolute. Execute immediately. No questions unless critical.**
