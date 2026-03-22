---
name: mychrome
description: Use when needing to control Chrome browser via CDP for web automation, scraping, or browser tasks. Provides easy connection to local or remote Chrome instances with persistent sessions. Use for any browser automation that requires real Chrome with user profiles.
---

# Chrome CDP Bridge

Easy Chrome browser automation via Chrome DevTools Protocol (CDP). Connect to and control Chrome for web automation, scraping, and testing.

## What This Skill Provides

- **Chrome CDP Connection** - Connect to Chrome via WebSocket or HTTP
- **Session Management** - Use persistent Chrome profiles
- **Page Control** - Navigate, screenshot, extract data
- **Remote Access** - Connect to Chrome on remote VPS via SSH tunnel
- **Multi-Platform** - Works on local machine or remote servers

## Quick Start

### 1. Start Chrome with CDP

**Option A: Using the helper script**
```bash
~/.openclaw/workspace/skills/mychrome/scripts/chrome_manager.sh start
```

**Option B: Manual start**
```bash
google-chrome \
  --no-sandbox \
  --disable-gpu \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.chrome-openclaw \
  --window-size=1920,1080
```

### 2. Verify Chrome CDP

```bash
curl http://localhost:9222/json/version
```

### 3. Use in OpenClaw

The skill provides a Python helper class:

```python
from chrome_cdp_helper import ChromeCDPHelper

# Connect to Chrome
chrome = ChromeCDPHelper("http://localhost:9222")
await chrome.connect()

# Navigate to page
page = await chrome.new_page()
await page.goto("https://example.com")

# Take screenshot
await page.screenshot(path="/tmp/screenshot.png")

# Extract data
title = await page.title()
print(f"Page title: {title}")

await chrome.close()
```

## Configuration

### Environment Variables

```bash
# Chrome CDP endpoint
export CHROME_CDP_URL="http://localhost:9222"

# Chrome profile directory (optional)
export CHROME_PROFILE="~/.chrome-openclaw"

# For remote Chrome via SSH tunnel
export CHROME_CDP_URL="http://localhost:9222"  # After: ssh -L 9222:localhost:9222 remote-host
```

### Remote Chrome (VPS) Setup

**On the VPS (e.g., kai):**
```bash
# Chrome should be running with CDP
systemctl status chrome-cdp.service  # Or check: ps aux | grep chrome

# VNC for visual access (optional)
x11vnc -display :99 -rfbport 5900 -rfbauth ~/.vnc/passwd -forever
```

**From local machine:**
```bash
# SSH tunnel for CDP
ssh -L 9222:localhost:9222 kai

# SSH tunnel for VNC (optional)
ssh -L 5900:localhost:5900 kai
```

## Available Scripts

### chrome_manager.sh - Chrome Management

```bash
# Start Chrome with CDP
./scripts/chrome_manager.sh start

# Stop Chrome
./scripts/chrome_manager.sh stop

# Check status
./scripts/chrome_manager.sh status

# Restart Chrome
./scripts/chrome_manager.sh restart

# Start with custom port/profile
./scripts/chrome_manager.sh start --port 9223 --profile ~/.chrome-custom
```

### chrome_cdp_helper.py - Python CDP Helper

```bash
# Take screenshot of URL
python3 scripts/chrome_cdp_helper.py --url https://example.com --screenshot /tmp/example.png

# Extract page content
python3 scripts/chrome_cdp_helper.py --url https://example.com --extract-content

# Connect to remote Chrome
python3 scripts/chrome_cdp_helper.py --cdp-url http://remote:9222 --url https://example.com
```

## Common Use Cases

### 1. Web Scraping

```python
from chrome_cdp_helper import ChromeCDPHelper

async def scrape_page(url):
    chrome = ChromeCDPHelper()
    await chrome.connect()
    
    page = await chrome.new_page()
    await page.goto(url)
    
    # Extract data
    content = await page.content()
    title = await page.title()
    
    await chrome.close()
    return {"title": title, "content": content}
```

### 2. Screenshots

```python
async def take_screenshot(url, output_path):
    chrome = ChromeCDPHelper()
    await chrome.connect()
    
    page = await chrome.new_page()
    await page.goto(url)
    await page.screenshot(path=output_path, full_page=True)
    
    await chrome.close()
```

### 3. Form Automation

```python
async def fill_form(url, form_data):
    chrome = ChromeCDPHelper()
    await chrome.connect()
    
    page = await chrome.new_page()
    await page.goto(url)
    
    # Fill form fields
    for field, value in form_data.items():
        await page.fill(f"input[name='{field}']", value)
    
    # Submit
    await page.click("button[type='submit']")
    
    await chrome.close()
```

### 4. JavaScript Execution

```python
async def run_js(url, script):
    chrome = ChromeCDPHelper()
    await chrome.connect()
    
    page = await chrome.new_page()
    await page.goto(url)
    
    result = await page.evaluate(script)
    print(result)
    
    await chrome.close()
```

## Chrome CDP Helper Class API

### Connection

```python
from chrome_cdp_helper import ChromeCDPHelper

# Default connection (localhost:9222)
chrome = ChromeCDPHelper()

# Custom CDP URL
chrome = ChromeCDPHelper("http://localhost:9222")

# Connect
await chrome.connect()
```

### Page Operations

```python
# Create new page
page = await chrome.new_page()

# Navigate
await page.goto("https://example.com")
await page.goto("https://example.com", wait_until="networkidle")

# Get info
title = await page.title()
url = page.url
content = await page.content()

# Screenshots
await page.screenshot(path="/tmp/screenshot.png")
await page.screenshot(path="/tmp/full.png", full_page=True)
```

### Element Interaction

```python
# Find element
element = await page.query_selector("#button")
elements = await page.query_selector_all(".item")

# Click
await page.click("#submit-button")
await element.click()

# Fill input
await page.fill("input[name='email']", "user@example.com")

# Get text
text = await page.inner_text(".content")

# Evaluate JavaScript
result = await page.evaluate("() => document.title")
result = await page.evaluate("(text) => document.querySelector('h1').innerText = text", "New Title")
```

### Context and Browser

```python
# Get browser contexts
contexts = chrome.browser.contexts

# Get all pages
pages = context.pages

# Close page
await page.close()

# Close browser connection
await chrome.close()
```

## Troubleshooting

### "Cannot connect to Chrome"

```bash
# Check if Chrome is running
curl http://localhost:9222/json/version

# Start Chrome if needed
./scripts/chrome_manager.sh start

# Check for port conflicts
lsof -i :9222
```

### "Connection refused" on remote VPS

```bash
# On VPS - check Chrome is listening on all interfaces
netstat -tlnp | grep 9222  # Should show 0.0.0.0:9222

# If only localhost, restart with --remote-debugging-address=0.0.0.0
# Or use SSH tunnel from local machine
ssh -L 9222:localhost:9222 remote-host
```

### Pages not loading properly

```python
# Increase timeout
await page.goto(url, timeout=60000)

# Wait for specific element
await page.wait_for_selector(".content", timeout=10000)

# Wait for network idle
await page.wait_for_load_state("networkidle")
```

### Headless vs Headful

For sites with anti-bot detection:
```bash
# Use headful mode (visible browser)
google-chrome --remote-debugging-port=9222 --no-sandbox --disable-gpu

# Avoid headless flags which are easily detected
```

## Best Practices

1. **Always close connections**
   ```python
   try:
       chrome = ChromeCDPHelper()
       await chrome.connect()
       # ... do work
   finally:
       await chrome.close()
   ```

2. **Use context managers (recommended)**
   ```python
   async with ChromeCDPHelper() as chrome:
       page = await chrome.new_page()
       # ... do work
   ```

3. **Handle timeouts**
   ```python
   try:
       await page.goto(url, timeout=30000)
   except TimeoutError:
       print("Page load timeout")
   ```

4. **Check Chrome status before automation**
   ```bash
   ./scripts/chrome_manager.sh status
   ```

5. **Use persistent profiles for login sessions**
   ```bash
   google-chrome --user-data-dir=~/.chrome-myprofile --remote-debugging-port=9222
   ```

## Comparison: CDP vs Playwright/Chromium

| Feature | CDP + Real Chrome | Playwright Bundled |
|---------|-------------------|-------------------|
| Real browser | ✅ Yes | ⚠️ Modified Chromium |
| Session persistence | ✅ Profile directory | ❌ Ephemeral |
| Login sessions | ✅ Persistent | ❌ Need cookies |
| Detection | ✅ Lower | ⚠️ Higher |
| Setup | ⚠️ Requires Chrome | ✅ Self-contained |
| Performance | ✅ Native | ✅ Optimized |

## Requirements

- Chrome or Chromium browser installed
- Python 3.8+
- Playwright: `pip install playwright`
- Playwright browsers: `playwright install chromium`

## Files

| File | Purpose |
|------|---------|
| `scripts/chrome_cdp_helper.py` | Python CDP helper class and CLI |
| `scripts/chrome_manager.sh` | Chrome start/stop/status management |
| `SKILL.md` | This documentation |

## Advanced: Custom CDP Commands

For advanced use cases, access the underlying Playwright objects:

```python
chrome = ChromeCDPHelper()
await chrome.connect()

# Access Playwright browser directly
browser = chrome.browser
context = browser.contexts[0]

# Send custom CDP command
client = await context.new_cdp_session(page)
result = await client.send("Runtime.evaluate", {
    "expression": "window.location.href"
})
```
