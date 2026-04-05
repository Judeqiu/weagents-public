---
name: chromecdp
description: "Browser automation with Chrome on virtual display :99 via port 9222. Use when the user wants to: open a website, browse the web, check a webpage, take a screenshot of a site, interact with web pages, fill forms, click buttons, scroll pages, handle popups/cookie banners, or automate any web-based task. This skill ONLY works with Chrome on port 9222 with VNC display :99. OBEY USER INSTRUCTIONS 100%."
version: 3.0.0
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

### 3. Chrome on Port 9222

The skill will automatically start Chrome if not running.

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

# Capture screenshot
ws.send(json.dumps({
    "id": 1,
    "method": "Page.captureScreenshot",
    "params": {"format": "png", "fromSurface": True}
}))

result = json.loads(ws.recv())
if 'result' in result and 'data' in result['result']:
    screenshot_data = result['result']['data']
    with open('/tmp/screenshot.png', 'wb') as f:
        f.write(base64.b64decode(screenshot_data))
    print("Screenshot saved")

ws.close()
```

### Navigate to URL

```python
import websocket
import json

target_id = "YOUR_TARGET_ID"
ws = websocket.create_connection(f"ws://127.0.0.1:9222/devtools/page/{target_id}")

ws.send(json.dumps({
    "id": 1,
    "method": "Page.navigate",
    "params": {"url": "https://example.com"}
}))

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
- `Page.captureScreenshot` - Take screenshot
- `Runtime.evaluate` - Execute JavaScript
- `DOM.querySelector` - Find element
- `Input.dispatchMouseEvent` - Click
- `Input.dispatchKeyEvent` - Type

## See Also

- `references/CDP-OPERATIONS.md` - Detailed CDP commands
- `references/POPUP-TYPES.md` - Popup detection details
- Chrome DevTools Protocol docs: https://chromedevtools.github.io/devtools-protocol/

---

**Remember: User instructions are absolute. Execute immediately. No questions unless critical.**
