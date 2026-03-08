# Manual PDF Download Guide for Easy-Paper

## Understanding the Flow

Based on HAR analysis, here's exactly what happens:

### The Two-Request System

```
┌─────────────────────────────────────────────────────────────────┐
│  YOUR BROWSER                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. You click/open:                                             │
│     https://server.easy-paper.com/paperdownload/pdf/?file=...   │
│                                                                 │
│     ↓                                                           │
│                                                                 │
│  2. Browser receives: PDF.js viewer HTML page                   │
│                                                                 │
│     ↓ (Automatic)                                               │
│                                                                 │
│  3. PDF.js viewer makes SECOND request:                         │
│     https://server.easy-paper.com/paperdownload/dir_v3/...      │
│                                                                 │
│     ↓                                                           │
│                                                                 │
│  4. Browser receives: Actual PDF data (application/pdf)         │
│                                                                 │
│  5. PDF.js renders the PDF for viewing                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Insight

The PDF is downloaded in **request #2**, not the initial URL! The initial URL just loads the viewer.

## Method 1: DevTools Network Tab (Easiest)

### Step-by-Step

1. **Open the PDF viewer URL** in your browser
   ```
   https://server.easy-paper.com/paperdownload/pdf/?file=...
   ```

2. **Open DevTools**
   - Press `F12` or `Ctrl+Shift+I` (Windows/Linux)
   - Press `Cmd+Option+I` (Mac)

3. **Setup Network Tab**
   - Click "Network" tab
   - Check ✅ "Preserve log" (top checkbox)
   - Clear any existing logs (click 🚫 button)

4. **Reload the Page**
   - Press `F5` or `Ctrl+R`
   - Wait for PDF to load and display

5. **Find the PDF Request**
   - Look for a request to `paperdownload/dir_v3/...`
   - Check the "Type" column - should say "application/pdf" or "pdf"
   - The "Size" column should show ~800KB (not a small number)

6. **Download the PDF**
   - **Option A**: Click on the request, then right-click → "Open in new tab"
   - **Option B**: Click on the request, go to "Headers" tab, find "Request URL", copy it, paste in new tab
   - **Option C**: Click on the request, go to "Response" tab, right-click → "Save as..."

7. **Save the File**
   - The browser will download the PDF
   - Save it with `.pdf` extension

## Method 2: URL Construction

If you have the viewer URL, you can construct the PDF URL:

### Step-by-Step

1. **Get the Viewer URL**
   ```
   Example: https://server.easy-paper.com/paperdownload/pdf/?file=%2Fpaperdownload%2Fdir_v3%2FABC123...
   ```

2. **Extract the File Parameter**
   - Find `?file=` in the URL
   - Copy everything after it
   - Example: `%2Fpaperdownload%2Fdir_v3%2FABC123...`

3. **URL Decode It**
   - `%2F` → `/`
   - `%25` → `%`
   - etc.
   - Result: `/paperdownload/dir_v3/ABC123...`

4. **Construct PDF URL**
   - Add `https://server.easy-paper.com` prefix
   - Result: `https://server.easy-paper.com/paperdownload/dir_v3/ABC123...`

5. **Open in Browser**
   - Paste the constructed URL
   - The PDF should download directly

### Python Helper

```python
import urllib.parse

viewer_url = "https://server.easy-paper.com/paperdownload/pdf/?file=%2Fpaperdownload%2Fdir_v3%2F..."

# Extract file parameter
parsed = urllib.parse.urlparse(viewer_url)
params = urllib.parse.parse_qs(parsed.query)
file_param = params['file'][0]

# Decode
decoded_path = urllib.parse.unquote(file_param)

# Construct PDF URL
pdf_url = f"https://server.easy-paper.com{decoded_path}"
print(pdf_url)
```

## Method 3: From HAR File

If you captured a HAR file while viewing the PDF:

### Step-by-Step

1. **Open HAR file** in text editor or HAR viewer

2. **Find the PDF Request**
   - Look for entry with `"mimeType": "application/pdf"`
   - Usually has large `"size"` (800KB+)

3. **Extract the Content**
   - Find `"content"` → `"text"` field
   - This is base64-encoded PDF data

4. **Decode and Save**
   ```python
   import base64
   
   har_text = "..."  # The base64 string from HAR
   pdf_bytes = base64.b64decode(har_text)
   
   with open('paper.pdf', 'wb') as f:
       f.write(pdf_bytes)
   ```

## Troubleshooting

### "File broken" or "Password prompt" appears

**Cause**: Session expired

**Solution**:
1. Go back to the mobile app
2. Re-open the paper (generates new session)
3. Copy the new URL
4. Try again immediately

### Can't find the PDF request in Network tab

**Cause**: Network log was cleared or not preserved

**Solution**:
1. Check "Preserve log" BEFORE reloading
2. Look for requests to `server.easy-paper.com`
3. Filter by "XHR" or "Doc" type

### PDF URL returns error

**Cause**: URL was not constructed correctly

**Solution**:
- Make sure to fully URL-decode the path
- Check for special characters like `%25` (which becomes `%`)

## Quick Reference

| What You Have | What You Need | Action |
|--------------|---------------|--------|
| Mobile app with PDF open | Browser download | Tap "Share" → "Copy Link" → Open in browser → DevTools → Find PDF request |
| Viewer URL (`?file=...`) | Direct PDF URL | Extract `file` param → URL decode → Prepend `https://server.easy-paper.com` |
| HAR file | PDF file | Find entry with `application/pdf` → Extract base64 text → Decode |
| Browser with PDF open | Saved PDF | `Ctrl+P` → "Save as PDF" (easiest!) |

## Example URLs from Analysis

### Viewer URL (what you click):
```
https://server.easy-paper.com/paperdownload/pdf/?file=%2Fpaperdownload%2Fdir_v3%2FHiYYXq50kXzUTCQLfRiFguzv9GuTLKVsiqjm3wSttMo7pGX4c8cTo74bT9fLT3lQwwhg4rYkCP1TQE%2525fo%2540~%255BC.4L1.ZDcpgycU2XSFzoxPlyNYqhRaokSULO7%2525fo%2540~%255BC.4L1.ZDcpZlhrD3XsqszPgTydG0jarzuoDMo9wUH35lClmW7qe8r1KCHHHJyWsez%252BJeTLEJTdqB1850Uzq8HW%252BtdWt6wXs67vhwEDUCAEggdX2o0AIgD7ubn9J8goLvGncP2lwQtX6x%2525fo%2540~%255BC.4L1.ZDcpGSEmxAux6tlP42zMXQ
```

### PDF URL (where the file is):
```
https://server.easy-paper.com/paperdownload/dir_v3/HiYYXq50kXzUTCQLfRiFguzv9GuTLKVsiqjm3wSttMo7pGX4c8cTo74bT9fLT3lQwwhg4rYkCP1TQE%25fo%40~%5BC.4L1.ZDcpgycU2XSFzoxPlyNYqhRaokSULO7%25fo%40~%5BC.4L1.ZDcpZlhrD3XsqszPgTydG0jarzuoDMo9wUH35lClmW7qe8r1KCHHHJyWsez%2BJeTLEJTdqB1850Uzq8HW%2BtdWt6wXs67vhwEDUCAEggdX2o0AIgD7ubn9J8goLvGncP2lwQtX6x%25fo%40~%5BC.4L1.ZDcpGSEmxAux6tlP42zMXQ
```

## Important Headers

The browser sends these headers (from HAR analysis):
- `Referer: https://server.easy-paper.com/paperdownload/pdf/?file=...`
- `Origin: https://easy-paper.com`
- `User-Agent: Mozilla/5.0...`

**No special cookies needed!**
