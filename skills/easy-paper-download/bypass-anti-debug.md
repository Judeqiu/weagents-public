# Bypassing Anti-Debug Protection on Easy-Paper

## Problem

Opening DevTools (F12) causes the page to enter "debug" mode and become unresponsive. This is intentional anti-debugging protection.

## Solutions

### Solution 1: Disable Debugger Statements (Fastest)

**Before opening DevTools:**

1. **Open Chrome DevTools Settings**:
   - Press `F12` (page will freeze, that's OK)
   - Click the gear icon (⚙️) in top right
   - OR press `F1` while DevTools is open

2. **Disable Debugger**:
   - Go to "Preferences" → "Sources"
   - **UNCHECK** "Enable JavaScript source maps"
   - **CHECK** "Disable JavaScript" (temporarily)
   - Close settings
   - Reload page
   - **UNCHECK** "Disable JavaScript" after reload

3. **Alternative - Disable Breakpoints**:
   - Go to "Sources" tab
   - Look for the "Deactivate breakpoints" button (⏸️ with a line through it)
   - Click it BEFORE the page loads

### Solution 2: Override Debugger Function

**In Console (paste quickly before page freezes):**

```javascript
// Disable debugger
window.debugger = function(){};
debugger = function(){};

// Disable console clearing
console.clear = function(){};

// Override the anti-debug function
setInterval(function(){
    Function.prototype.constructor = function(){};
}, 100);

console.log('Anti-debug disabled');
```

### Solution 3: Use Firefox Instead of Chrome

Firefox has less aggressive anti-debug detection:

1. Open Firefox
2. Press `F12` to open DevTools
3. The page may not freeze
4. Go to Network tab immediately
5. Check "Persist Logs" (equivalent to "Preserve log")

### Solution 4: Use a Browser Extension

**Install "Disable JavaScript" extension**:

1. Chrome Web Store → Search "Disable JavaScript"
2. Install extension
3. Enable it for easy-paper.com
4. Open DevTools
5. Disable the extension (re-enable JavaScript)

### Solution 5: Use mitmproxy or Charles (Bypass Browser Entirely)

Since the anti-debug is in the browser, use an external proxy:

```bash
# Install mitmproxy
pip install mitmproxy

# Run proxy
mitmweb --mode regular --listen-port 8080

# Configure browser to use proxy localhost:8080
# Capture traffic without opening DevTools
```

### Solution 6: ModHeader Extension (Capture Headers Without DevTools)

**If you just need to see request headers:**

1. Install "ModHeader" extension from Chrome Web Store
2. Open ModHeader (click icon)
3. Perform your actions on the site
4. ModHeader shows all request headers
5. No need to open DevTools!

### Solution 7: Disable DevTools Detection via Chrome Flags

**Chrome command line flags:**

```bash
# On macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --disable-blink-features=DevtoolsExperiments \
  --disable-features=IsolateOrigins,site-per-process

# On Windows
chrome.exe --disable-blink-features=DevtoolsExperiments
```

## Recommended Approach for Easy-Paper

### Quick Method (2 minutes):

1. **Open Chrome**
2. **Press `Ctrl+Shift+J`** (opens Console directly, bypassing some checks)
3. **Immediately paste** this and press Enter:
   ```javascript
   setInterval(()=>{debugger;}, 100);
   Function = function(){};
   ```
4. **Press `F12`** to open full DevTools
5. **Go to Sources tab**
6. **Click "Deactivate breakpoints"** (⏸️ with slash)
7. **Go to Network tab**
8. **Check "Preserve log"**
9. **Reload the page** (Ctrl+R)
10. **Perform your workflow**
11. **Right-click → "Save all as HAR"**

### Alternative: Firefox Method

Firefox's debugger detection is weaker:

1. Open Firefox
2. Press `F12`
3. If it freezes, press `F8` (resume execution)
4. Or click the "Resume script execution" button (▶️)
5. Go to Network tab
6. Check "Persist Logs"
7. Continue as normal

## If Page Still Freezes

### Force Resume:

1. Page is frozen with DevTools open
2. Press `F8` (Resume script execution)
3. OR click the blue "Resume" button (▶️)
4. May need to press multiple times
5. Once resumed, disable breakpoints:
   - Sources tab → "Deactivate breakpoints"

### Override Local Storage:

Some sites store debug state in localStorage. Clear it:

```javascript
// In Console (quickly paste before freeze)
localStorage.clear();
sessionStorage.clear();
```

## Capturing Without DevTools

### Method 1: Chrome Net-Export

1. Go to `chrome://net-export/`
2. Click "Start Logging to Disk"
3. Perform your actions
4. Click "Stop Logging"
5. Analyze the JSON log

### Method 2: Use cURL with Browser Cookies

1. Login/access the site normally
2. Use "EditThisCookie" extension to export cookies
3. Use curl with those cookies:
   ```bash
   curl -b cookies.txt "https://server.easy-paper.com/..."
   ```

## Success Indicators

✅ **DevTools is working if:**
- Network tab shows requests
- Console shows logs
- Page remains interactive

❌ **Still blocked if:**
- Page constantly pauses
- "Paused in debugger" message keeps appearing
- Cannot click anything

## Next Steps

Once you bypass the anti-debug:

1. **Go to Network tab immediately**
2. **Check "Preserve log"**
3. **Uncheck "Cache" (disable caching)**
4. **Clear existing logs** (🚫 button)
5. **Perform your workflow**
6. **Export HAR when done**

Share the HAR file and I can analyze the token flow!
