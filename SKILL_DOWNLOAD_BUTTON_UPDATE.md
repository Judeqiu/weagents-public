# EasyPaper PDF Finder Skill - Download Button Update

## Summary

Updated the `easypaper-pdf-finder` skill to use the **download button as the primary method** for downloading PDFs, with screenshot capture as fallback.

## Files Updated

### 1. SKILL.md (Documentation)
**Location:** `/Users/zhengqingqiu/.config/agents/skills/easypaper-pdf-finder/SKILL.md`

**Changes:**
- Updated overview to mention download button capability
- Added "Download Button Method (Primary)" section
- Documented screenshot fallback method
- Added comparison table (download vs screenshot)
- Updated file reference table
- Added pattern examples for download button method

### 2. capture_easypaper_pdf.py (Basic Script)
**Location:** `/Users/zhengqingqiu/.config/agents/skills/easypaper-pdf-finder/capture_easypaper_pdf.py`

**Changes:**
- Now tries download button **first**
- Falls back to screenshot method if download fails
- Returns tuple of `(file_path, method_used)`
- Method is either `'download'` or `'screenshot'`

**Key Function:**
```python
def download_easypaper_pdf(pdf_url, output_path) -> Tuple[str, str]:
    # 1. Try download button
    if _try_download_button(page, output_path):
        return output_path, 'download'
    
    # 2. Fallback to screenshots
    if _capture_by_screenshots(page, output_path, ...):
        return output_path, 'screenshot'
```

### 3. capture_easypaper_pdf_with_retry.py (Advanced Script)
**Location:** `/Users/zhengqingqiu/.config/agents/skills/easypaper-pdf-finder/capture_easypaper_pdf_with_retry.py`

**Changes:**
- Added `_try_download_button()` function
- Added `_capture_by_screenshots()` function
- `capture_single_pdf()` now tries download first
- Returns `method_used` in `CaptureResult`
- Includes fallback search capability

## How the Download Button Method Works

1. **Enable downloads** in Playwright context:
   ```python
   context = browser.new_context(
       accept_downloads=True,  # Required!
       ...
   )
   ```

2. **Make button visible** - Remove CSS class that hides it:
   ```javascript
   btn.classList.remove('hiddenMediumView');
   btn.style.display = 'block';
   btn.style.visibility = 'visible';
   ```

3. **Click and capture** download:
   ```python
   with page.expect_download(timeout=30000) as download_info:
       page.locator("button#download").first.click(force=True)
   
   download = download_info.value
   download.save_as(output_path)
   ```

## Method Comparison

| Aspect | Download Button | Screenshot Fallback |
|--------|-----------------|---------------------|
| **File size** | Smaller (e.g., 284 KB) | Larger (e.g., 3 MB) |
| **Quality** | Original, perfect | Good (image-based) |
| **Text layer** | Preserved (searchable) | Not preserved |
| **Speed** | ~20 seconds | ~55 sec (20 pages) |
| **Metadata** | Preserved | Lost |
| **Success rate** | High (most PDFs) | Universal fallback |

## Usage

### Basic Download
```bash
python capture_easypaper_pdf.py "<PDF_URL>" /tmp/output.pdf
```

### With Retry and Fallback
```bash
python capture_easypaper_pdf_with_retry.py "<PDF_URL>" /tmp/output.pdf
```

### Python API
```python
from capture_easypaper_pdf import download_easypaper_pdf

result_path, method = download_easypaper_pdf(
    pdf_url="https://server.easy-paper.com/paperdownload/pdf/?file=...",
    output_path="/tmp/my_paper.pdf",
    headless=True
)

print(f"Downloaded: {result_path}")
print(f"Method used: {method}")  # 'download' or 'screenshot'
```

## Verification

The skill has been tested and verified:

1. ✅ Download button method works (demonstrated multiple times)
2. ✅ Screenshot fallback works when download fails
3. ✅ Both scripts return method information
4. ✅ Documentation updated with new patterns
5. ✅ Files are properly sized (284 KB download vs 3 MB screenshot)

## Notes

- PDF URLs from EasyPaper expire quickly (session-based)
- Download button is hidden via CSS (`hiddenMediumView` class)
- Original PDFs are NOT encrypted (contrary to earlier documentation)
- Screenshot method preserves visual fidelity but loses text searchability
