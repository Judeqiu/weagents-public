---
name: lazada-browser
description: "Browser automation for Lazada Seller Center (sellercenter.lazada.sg) using real Chrome browser with CDP. Use when the user needs to access, scrape, or interact with Lazada Seller Center. Requires Chrome to be running with remote debugging enabled. Auto-sends email alerts on failure."
---

# Lazada Seller Center Browser - Chrome CDP Version

**⚠️ IMPORTANT: Data is extracted from HTML, NOT from screenshots!**

This skill uses programmatic HTML parsing to retrieve order numbers and other data. **Never analyze screenshots for data extraction** - screenshots are only for visual reference. All numerical data must be extracted from the page's HTML/DOM using regex or JavaScript.

## How It Works

1. **Chrome runs continuously** on the VPS with a persistent profile
2. **Human logs in once** to Lazada Seller Center via Chrome
3. **Automation connects** to Chrome via CDP and uses the existing session
4. **No cookie management needed** - cookies are stored in Chrome's profile

## ⚠️ Data Extraction Rules (IMPORTANT)

### How Order Numbers ARE Retrieved:
- **HTML Parsing**: The script fetches the page's HTML content using Playwright/CDP
- **Regex Patterns**: Order counts are extracted using regex patterns from the raw HTML
- **JavaScript Execution**: Can also execute JS to extract data from the DOM

Example from the code:
```python
# Parse order counts from the HTML
patterns = [
    (r'Orders\s*</div>\s*<div[^>]*>(\d+)', 'orders'),
    (r'Pending Pack\s*</div>\s*<div[^>]*>(\d+)', 'pending_pack'),
]
```

### How Order Numbers are NOT Retrieved:
- ❌ **Never** from analyzing screenshots
- ❌ **Never** from OCR (image text recognition)
- ❌ **Never** from visual inspection

### Why This Matters:
- **Prevents hallucination**: Data comes from actual page content, not interpretation
- **Accurate**: Numbers are extracted exactly as they appear in the HTML
- **Reliable**: Works regardless of screen resolution or display settings

**When reporting order counts to the user, always cite the JSON data from the script output, not visual analysis of screenshots.**

## ⚠️ Output Format (IMPORTANT)

When reporting results to the user, use this format:

1. **Natural language summary** - Brief human-readable summary
2. **Raw JSON** - Attach the full JSON output at the end

Example:
```
**Lazada Orders:**

| Status | Count |
|--------|-------|
| New Orders | 5 |
| Pending Pack | 2 |
| Pending Shipping | 3 |

```
{"status": "success", "orders": "5", "pending_pack": "2", ...}
```

This ensures transparency - user can see the exact data source.

## ⚠️ Failure Reporting (IMPORTANT)

If the script fails to retrieve data, **report the failure honestly**:

### Do:
- ✅ Report exact error messages (e.g., "Cannot connect to Chrome", "Session expired", "Timeout")
- ✅ Say "I couldn't retrieve the data" if extraction fails
- ✅ Suggest next steps (e.g., "You may need to log in again")

### Don't:
- ❌ Don't make up order numbers
- ❌ Don't guess or estimate
- ❌ Don't say "no orders" if you couldn't verify
- ❌ Don't hide errors

**Honest failure > False data**

## Prerequisites

### On the VPS (Enraie)

Chrome must be running with remote debugging enabled:

```bash
# Chrome should be started with these flags:
google-chrome \
  --no-sandbox \
  --disable-gpu \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/enraie/.chrome-openclaw \
  --window-size=1920,1080
```

**Check if Chrome is running:**
```bash
curl http://127.0.0.1:9222/json/version
```

### First-Time Setup (Manual Login)

1. **SSH to the VPS with X11 forwarding or use VNC:**
   ```bash
   ssh -X enraie  # or use VNC client
   ```

2. **Open Chrome and navigate to Lazada:**
   ```bash
   google-chrome --user-data-dir=/home/enraie/.chrome-openclaw
   ```

3. **Log in manually** to sellercenter.lazada.sg with your credentials

4. **Keep Chrome running** - the session will persist

## Quick Start

### Option 1: Use the Chrome CDP Script (Recommended)

```bash
python3 ~/.openclaw/workspace/skills/lazada-browser/scripts/lazada_browser_chrome.py --url "https://sellercenter.lazada.sg/#!/"
```

With screenshot:
```bash
python3 ~/.openclaw/workspace/skills/lazada-browser/scripts/lazada_browser_chrome.py --screenshot /tmp/lazada_dashboard.png
```

Check orders only:
```bash
python3 ~/.openclaw/workspace/skills/lazada-browser/scripts/lazada_browser_chrome.py --check-orders
```

Disable email alerts (for testing):
```bash
python3 ~/.openclaw/workspace/skills/lazada-browser/scripts/lazada_browser_chrome.py --no-alert
```

### Option 2: Connect to Remote Chrome from Local Machine

If you want to connect to Chrome on the VPS from your local machine:

```bash
# SSH tunnel to forward CDP port
ssh -L 9222:localhost:9222 enraie

# Then run locally
python3 scripts/lazada_browser_chrome.py --cdp-url http://localhost:9222
```

## Environment Variables

```bash
# Chrome CDP URL (default: http://127.0.0.1:9222)
export CHROME_CDP_URL="http://127.0.0.1:9222"

# Chrome profile path (for reference)
export CHROME_PROFILE="/home/enraie/.chrome-openclaw"

# Email alerts (Brevo API)
export BREVO_API_KEY="xkeysib-your-api-key"
export EMAIL_FROM="ono@lextok.com"
export FROM_NAME="Enraie Bot"

# Telegram alerts
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="-1003848052058"
```

## Important Notes

### Session Persistence
- **Chrome profile stores all cookies** - no manual cookie export needed
- **Session lasts as long as Chrome keeps it** - typically weeks if Chrome stays running
- **If logged out**, simply log in again via Chrome manually

### Chrome Must Be Running
- The script connects to an **already running** Chrome instance
- If Chrome is not running, you'll see: `Cannot connect to Chrome at http://127.0.0.1:9222`
- Start Chrome with the remote debugging flag first

### Display/Headless
- Chrome runs with virtual display (`DISPLAY=:99` with OpenBox)
- Or can run on real display if connected via VNC/RDP
- The automation works regardless - CDP connects to the browser process

## Auto-Alert Feature

### What It Does
If the script fails to access Lazada due to authentication issues, it **automatically sends alerts to:**
1. **Email** (david@lextok.com by default)
2. **Telegram Group** (BusinessBotEval)

### Failure Scenarios That Trigger Alerts
- Session expired / redirected to login page
- Access denied (403/401 errors)
- Page content too small (indicates redirect)
- Chrome not accessible (CDP connection failed)
- Page load timeouts

### Alert Content
- Timestamp and URL attempted
- Error details
- Instructions to re-login via Chrome

## Common URLs

- Dashboard: `https://sellercenter.lazada.sg/#!/`
- Products: `https://sellercenter.lazada.sg/products`
- Marketing: `https://sellercenter.lazada.sg/marketing`
- Order Management: `https://sellercenter.lazada.sg/apps/order/list`
- Shipping Orders: `https://sellercenter.lazada.sg/apps/order/list?status=shipping`
- All Orders: `https://sellercenter.lazada.sg/apps/order/list?tab=all`

## Data Available on Dashboard

The main dashboard shows:
- **Task List**: Orders, Pending Pack, Pending Shipping, Pending Return/Refund counts
- **Business Advisor**: Revenue Today, Orders, Visitors, Conversion Rate
- **Products**: Out of Stock, QC Issues counts
- **Marketing Center**: Campaigns and promotions
- **Growth Center**: Chat response rate, ship on time rate

## Troubleshooting

### "Cannot connect to Chrome at http://127.0.0.1:9222"
**Solution:** Chrome is not running or not started with remote debugging.

```bash
# Check if Chrome is running
ps aux | grep chrome

# Start Chrome with CDP
google-chrome \
  --no-sandbox \
  --disable-gpu \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/enraie/.chrome-openclaw &

# Verify CDP is accessible
curl http://127.0.0.1:9222/json/version
```

### "STATUS: Not logged in - session expired"
**Solution:** The Lazada session has expired. You need to log in again manually.

```bash
# Connect to VPS with display
ssh -X enraie

# Open Chrome
google-chrome --user-data-dir=/home/enraie/.chrome-openclaw

# Navigate to sellercenter.lazada.sg and log in manually
```

### Chrome Profile Issues
If Chrome behaves strangely or crashes:
```bash
# Backup and reset profile
mv /home/enraie/.chrome-openclaw /home/enraie/.chrome-openclaw.backup

# Chrome will create a new profile on next start
# You'll need to log in again
```

## Files

| File | Purpose |
|------|---------|
| `scripts/lazada_browser_chrome.py` | Main Chrome CDP automation script |
| `scripts/lazada_browser.py` | Legacy cookie-based script (kept for reference) |
| `scripts/daily_report.py` | Daily report generator (use `lazada_browser_chrome.py` instead) |

## Comparison: Cookie vs Chrome CDP

| Feature | Cookie-Based | Chrome CDP |
|---------|--------------|------------|
| Setup | Export cookies manually | Log in once via Chrome |
| Cookie expiration | 24-48 hours | Weeks/months (Chrome keeps session) |
| Maintenance | High (frequent re-export) | Low (just keep Chrome running) |
| Reliability | Medium | High |
| Human intervention | Every 1-2 days | Only when session expires |

## Best Practices

1. **Keep Chrome running** - Use systemd or screen/tmux to keep Chrome alive
2. **Monitor Chrome** - Check periodically that Chrome hasn't crashed
3. **Check CDP port** - Verify `curl http://localhost:9222/json/version` works
4. **Set up alerts** - Configure email/Telegram for auth failures
5. **Use SSH tunnel** for local development connecting to remote Chrome
