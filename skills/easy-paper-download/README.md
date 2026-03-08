# Easy-Paper PDF Download - Complete Guide

## ⚠️ Important: Session Expiration

**The PDF URLs expire quickly (within minutes)!** You must complete the download process immediately after opening the paper in the mobile app.

## How It Works (Based on HAR Analysis)

### The Two-Step Process

```
Step 1: Mobile App
   ↓
Search and open paper → App generates session token
   ↓
Copy/Share the viewer URL

Step 2: Browser (within 1-2 minutes!)
   ↓
Open viewer URL → PDF.js loads
   ↓
Browser fetches actual PDF data
   ↓
Save via Print → PDF
```

## Method 1: Manual Browser Download (Recommended)

### Prerequisites
- EasyPaper mobile app installed
- Paper you want to download
- Desktop/laptop browser

### Steps

#### Part 1: Mobile App (30 seconds)

1. **Open EasyPaper app**
2. **Search for your paper** (e.g., "AP Human Geography 2019")
3. **Tap the result** to open it
4. **Wait for PDF to load** in the app viewer
5. **Tap "Share" or browser icon** (usually top-right)
6. **Copy the link** (looks like: `https://server.easy-paper.com/paperdownload/pdf/?file=...`)
7. **Quickly send to yourself** (email, messaging, AirDrop, etc.)

#### Part 2: Desktop Browser (30 seconds)

**⚡ You have ~1-2 minutes! Act fast!**

8. **Open the link in your browser immediately**
9. **Wait for PDF to display** (you should see the content)
10. **Press `Ctrl+P` (Windows/Linux) or `Cmd+P` (Mac)**
11. **Select "Save as PDF" as the printer**
12. **Click Save**
13. **Done!** ✅

### If It Fails (Session Expired)

If you see:
- "Enter password to open this PDF"
- "File broken"
- "Invalid PDF"

**Solution**: Go back to the mobile app, close and re-open the paper, copy the new link, try again.

---

## Method 2: DevTools Network Tab (For Tech Users)

If you want to grab the direct PDF URL:

1. **Open the viewer URL in browser**
2. **Press F12** (before the session expires!)
3. **Go to Network tab**
4. **Check "Preserve log"**
5. **Reload page** (F5)
6. **Look for request to:**
   - URL contains `paperdownload/dir_v3/`
   - Type: `application/pdf` or `pdf`
   - Size: ~800KB (large, not small)
7. **Click that request**
8. **Right-click → "Open in new tab"**
9. **PDF downloads directly**

---

## Method 3: From HAR File

If you captured a HAR while viewing:

1. **Open HAR file** in text editor
2. **Find entry with:**
   - `"mimeType": "application/pdf"`
   - Large `"size"` (~800KB+)
3. **Extract the `"text"` field** (base64 encoded)
4. **Decode and save:**

```python
import base64

har_text = "..."  # The base64 string
pdf_bytes = base64.b64decode(har_text)

with open('paper.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

---

## Method 4: Automated Script (Experimental)

Use the provided script (but session will likely expire):

```bash
python download_pdf.py "https://server.easy-paper.com/paperdownload/pdf/?file=..." output.pdf
```

**Note**: The script constructs the correct URL but cannot bypass the session expiration. You need a fresh URL.

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "Password prompt" appears | Session expired | Get fresh URL from mobile app |
| "File broken" error | Session expired | Get fresh URL from mobile app |
| PDF shows "loading" forever | Session expired while loading | Refresh page or get new URL |
| Can't find search in web | Web is app-promotional | Use mobile app for search |
| DevTools triggers anti-debug | Site protection | Press F8 to resume, or use Firefox |

---

## Technical Details

### URL Structure

**Viewer URL** (what you get from app):
```
https://server.easy-paper.com/paperdownload/pdf/?file=%2Fpaperdownload%2Fdir_v3%2F...
```

**PDF URL** (where the actual file is):
```
https://server.easy-paper.com/paperdownload/dir_v3/...
```

### Session Mechanism

From HAR analysis:
- ✅ **Not cookie-based** - No session cookies required
- ✅ **Not password-protected** - No password needed
- ✅ **Token-based via URL** - The encoded filename IS the token
- ⚠️ **Time-sensitive** - Token expires quickly
- 🔒 **Referer-checked** - Must come from viewer page

### What Works

The server returns `Content-Disposition: attachment` header with the PDF, meaning it's designed to be downloaded when accessed correctly.

---

## Quick Checklist

Before you start:
- [ ] Mobile app installed and paper found
- [ ] Desktop browser ready
- [ ] Method to quickly transfer URL (clipboard, messaging)
- [ ] 2-3 minutes of uninterrupted time

During the process:
- [ ] Open paper in app → Copy link (quick!)
- [ ] Send to desktop → Open in browser (quick!)
- [ ] PDF displays → Ctrl+P → Save as PDF
- [ ] Verify the downloaded file opens correctly

If it fails:
- [ ] Don't wait - immediately retry with fresh link
- [ ] Practice the workflow once to get fast

---

## Example Success

Your HAR file analysis shows this workflow:

1. **Entry #1**: Viewer page loaded (21KB HTML)
2. **Entries #2-24**: PDF.js resources loaded
3. **Entry #25**: PDF data downloaded (812KB, `Content-Type: application/pdf`)
4. **PDF rendered**: Viewable in browser
5. **Print → Save**: Creates local copy

The PDF was successfully captured in your HAR at entry #25!

---

## Files in This Skill

- `README.md` - This guide
- `download_pdf.py` - Automation script (for fresh URLs)
- `manual-download-guide.md` - Detailed manual steps
- `SKILL.md` - Original skill documentation
- `bypass-anti-debug.md` - DevTools bypass techniques
- `flow-recording-tools.md` - Tools for capturing flows

---

**Good luck! The key is speed - get the URL from the app and into your browser's Print dialog as fast as possible!**
