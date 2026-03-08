# Browser Flow Recording Tools for Easy-Paper Analysis

This document describes tools that can capture the complete network and interaction flow when accessing easy-paper.com

## 1. Chrome DevTools - Built-in Recording

### Network Tab Recording

1. **Open DevTools**
   - Press `F12` or `Ctrl+Shift+I`

2. **Enable Network Recording**
   - Click "Network" tab
   - Click the record button (red circle) - it should be ON by default
   - Check "Preserve log" checkbox (to keep logs across page navigations)

3. **Export HAR File**
   - Right-click in the Network panel
   - Select "Save all as HAR with content"
   - Save the `.har` file

### What It Captures
- All HTTP requests and responses
- Request headers, cookies, tokens
- Response headers and bodies
- Timing information
- WebSocket traffic

### How to Share for Analysis

Send the HAR file, which can be analyzed using:
- Chrome DevTools (import)
- Online HAR viewers (e.g., https://www.softwareishard.com/har/viewer/)
- This Python script:

```python
import json

with open('capture.har', 'r') as f:
    har = json.load(f)

# Extract all requests
for entry in har['log']['entries']:
    url = entry['request']['url']
    method = entry['request']['method']
    
    # Look for tokens
    if 'web_sfapi' in url:
        print(f"Token request: {method} {url}")
        print(f"Response: {entry['response']['content'].get('text', 'N/A')[:100]}")
```

---

## 2. Chrome DevTools - Performance Tab

### Recording User Interactions

1. **Open Performance Tab**
   - Press `F12` → Click "Performance"

2. **Start Recording**
   - Click the record button (⏺️)
   - Perform the actions (search, click, open PDF)
   - Click stop (⏹️)

3. **Save Profile**
   - Right-click on the timeline
   - Select "Save Profile..."

### What It Captures
- JavaScript execution
- Network requests
- Rendering timeline
- Function calls
- Event handlers

---

## 3. Chrome DevTools Protocol (CDP) - Programmatic

### Using Playwright with Tracing

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    
    # Start tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    page = context.new_page()
    page.goto("https://server.easy-paper.com/paperdownload/pdf/?file=...")
    
    # Stop and save
    context.tracing.stop(path="trace.zip")
```

### Viewing the Trace
```bash
# Open in Playwright Trace Viewer
playwright show-trace trace.zip
```

---

## 4. Browser Extensions

### Requestly (Recommended)

**Install**: https://requestly.io/

**Features**:
- Intercept and modify requests
- Record network activity
- Export as HAR
- Modify headers, redirect URLs

**How to Use**:
1. Install Requestly extension
2. Click extension icon → "Network Traffic"
3. Enable recording
4. Navigate to the PDF
5. Export the session

### HTTP Archive Viewer

**Install**: Chrome Web Store

**Features**:
- View HAR files directly in browser
- Filter requests
- Inspect headers and bodies

---

## 5. Charles Proxy (External Tool)

**Website**: https://www.charlesproxy.com/

**Best For**: Capturing mobile app traffic

### Setup for Mobile App Analysis

1. **Install Charles** on your computer

2. **Configure Mobile Device**:
   - Connect phone to same WiFi as computer
   - Set phone's HTTP proxy to your computer's IP + port 8888
   - Install Charles SSL certificate on phone

3. **Capture Traffic**:
   - Open EasyPaper app on phone
   - Perform search and open PDF
   - Charles captures all requests

4. **Export Session**:
   - File → Export Session → HAR format

### What Makes This Special
- Can capture **mobile app traffic** (not just browser)
- Shows actual API calls the app makes
- Reveals the real search API endpoints
- Captures authentication headers

---

## 6. mitmproxy (Open Source Alternative)

**Website**: https://mitmproxy.org/

**Command Line Usage**:
```bash
# Install
pip install mitmproxy

# Run proxy
mitmproxy --mode regular --listen-port 8080

# Or capture to file
mitmdump -w capture.mitm

# Export to HAR (requires script)
```

### Advantages
- Free and open source
- Python scripting support
- Can modify traffic programmatically

---

## 7. Browser Console Session Recording

### Quick JavaScript Capture

Paste this in Console (F12 → Console) before starting:

```javascript
// Capture all network requests
window._networkLog = [];
const origFetch = window.fetch;
window.fetch = async (...args) => {
    const request = args[0];
    window._networkLog.push({
        type: 'fetch',
        url: typeof request === 'string' ? request : request.url,
        time: new Date().toISOString()
    });
    return origFetch(...args);
};

// Capture XHR
const origXHR = window.XMLHttpRequest.prototype.open;
window.XMLHttpRequest.prototype.open = function(method, url, ...args) {
    window._networkLog.push({
        type: 'xhr',
        method: method,
        url: url,
        time: new Date().toISOString()
    });
    return origXHR.call(this, method, url, ...args);
};

console.log('Network logging enabled');
```

After the flow completes:
```javascript
// Export the log
console.log(JSON.stringify(window._networkLog, null, 2));
// Copy the output
```

---

## Recommended Workflow for Easy-Paper

### Option A: If You Have Browser Access

1. **Open Chrome DevTools** (F12)
2. **Go to Network tab**
3. **Check "Preserve log"**
4. **Navigate through the flow**:
   - Go to easy-paper.com
   - Search for paper
   - Click result
   - Open PDF
5. **Right-click → "Save all as HAR with content"**
6. **Share the HAR file** for analysis

### Option B: If Using Mobile App (Best Option)

1. **Install Charles Proxy** on your computer
2. **Configure phone to use Charles as proxy**
3. **Open EasyPaper app on phone**
4. **Perform the full flow**:
   - Search
   - Tap result
   - View PDF
5. **In Charles: File → Export Session → HAR**
6. **Share the HAR file**

This will reveal:
- The actual search API endpoint
- How the app generates tokens
- The complete request/response cycle
- Any hidden authentication headers

---

## Analyzing the Captured Flow

Once you have the HAR file, here's how to extract useful information:

```python
import json

def analyze_har(har_file):
    with open(har_file, 'r') as f:
        har = json.load(f)
    
    print("=== Easy-Paper Flow Analysis ===\n")
    
    # Find token requests
    print("1. Token Requests (web_sfapi):")
    for entry in har['log']['entries']:
        url = entry['request']['url']
        if 'web_sfapi' in url:
            print(f"\n   URL: {url}")
            print(f"   Method: {entry['request']['method']}")
            
            # Check headers
            headers = entry['request']['headers']
            for h in headers:
                if h['name'].lower() in ['authorization', 'cookie', 'x-token']:
                    print(f"   Header: {h['name']}: {h['value'][:50]}...")
            
            # Check response
            content = entry['response']['content']
            if 'text' in content:
                print(f"   Response: {content['text'][:100]}...")
    
    # Find PDF requests
    print("\n2. PDF Requests:")
    for entry in har['log']['entries']:
        url = entry['request']['url']
        if 'paperdownload' in url:
            print(f"\n   URL: {url}")
            print(f"   Method: {entry['request']['method']}")
            print(f"   Status: {entry['response']['status']}")
            
            # Check cookies sent
            cookies = entry['request'].get('cookies', [])
            print(f"   Cookies sent: {len(cookies)}")
            
            # Check headers
            headers = {h['name']: h['value'] for h in entry['request']['headers']}
            if 'Referer' in headers:
                print(f"   Referer: {headers['Referer'][:80]}...")

# Usage
# analyze_har('capture.har')
```

---

## Quick Start: Record Now

**Easiest method for immediate use**:

1. Open your browser
2. Press `F12`
3. Click "Network" tab
4. Check "Preserve log"
5. Perform your workflow
6. Right-click in Network panel → "Save all as HAR with content"
7. Share the `.har` file
