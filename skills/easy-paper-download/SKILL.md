# Easy-Paper Download Skill

Download CAIE past papers from easy-paper.com using Playwright browser automation.

## Status

**⚠️ Limited Success**: The site has sophisticated anti-automation protection that detects Playwright and serves a landing page instead of the search interface. This tool attempts multiple detection bypasses but may not work in all environments.

## Installation

```bash
cd /opt/agents/ono-assistant/workspace/skills/easy-paper-download
pip install playwright
playwright install chromium
```

For visible mode (if headless is blocked):
```bash
apt-get install xvfb
```

## Usage

### Try Automated Download

```bash
python3 easypaper.py -c 9702 -y 2024 -s s -p 12 -v 1
```

**Parameters:**
- `-c`: Subject code (9702=Physics, 9709=Math, 9701=Chem, etc.)
- `-y`: Year (2024, 2023, etc.)
- `-s`: Session (s=May/June, w=Oct/Nov, m=March)
- `-p`: Paper number (12, 22, 32, 42, 52)
- `-v`: Variant (1, 2, 3)
- `--visible`: Use visible browser with Xvfb

### Try with Visible Browser (Xvfb)

If headless mode is blocked:

```bash
xvfb-run -a python3 easypaper.py -c 9702 -y 2024 -s s -p 12
```

### Manual Method (Always Works)

If automation fails, use this manual method:

1. **Open browser** and go to https://easy-paper.com/papersearch
2. **Click on "Files" tab** (next to "Questions" and "Subjects")
3. **Search** for your paper (e.g., "9702 2024 s 12")
4. **Click** on the result to open PDF viewer
5. **Save PDF**: Press `Ctrl+P` → Select "Save as PDF" → Save

## Why Automation May Fail

The site uses multiple anti-automation techniques:

1. **Headless Detection**: Detects `navigator.webdriver` and other headless indicators
2. **JavaScript Fingerprinting**: Checks for browser plugins, screen size consistency
3. **Behavior Analysis**: Likely analyzes mouse movements and interaction patterns
4. **Token-based Access**: PDF URLs use encrypted, time-limited tokens

Even with:
- Stealth scripts
- Realistic user agents
- Virtual display (Xvfb)
- Persistent browser contexts

The site may still serve a landing page instead of the Vue.js search interface.

## Subject Codes

| Code | Subject |
|------|---------|
| 9702 | Physics |
| 9709 | Mathematics |
| 9701 | Chemistry |
| 9700 | Biology |
| 9618 | Computer Science |
| 9708 | Economics |
| 9990 | Psychology |

## File Structure

```
easy-paper-download/
├── SKILL.md              # This documentation
├── easypaper.py         # Main Playwright automation script
└── downloads/           # Default output directory
```

## Technical Details

### What the Script Does

1. Launches Chromium with anti-detection measures
2. Navigates to https://easy-paper.com/papersearch
3. Checks if Vue.js search interface loaded (vs landing page)
4. Clicks "Files" tab
5. Enters search query
6. Clicks first result
7. Captures PDF using browser print

### Detection Methods Attempted

The script tries:
- Disabling `navigator.webdriver`
- Adding fake plugins
- Setting realistic viewport and locale
- Using Xvfb for visible browser simulation
- Various stealth patches

### API Attempts

Direct API access is not possible because:
- Tokens are encrypted with unknown keys
- Server validates tokens against session
- No public API documentation

## Troubleshooting

### "ANTI-BOT DETECTED"
The site served the landing page. Try:
- Running with `--visible` flag and Xvfb
- Using manual method (see above)

### "Failed to launch browser"
Install dependencies:
```bash
apt-get install xvfb xauth
playwright install chromium
```

### Empty or small PDF
The PDF capture didn't work. Use manual method instead.

## Credits

Playwright-based automation for easy-paper.com.
