---
name: watsons-seller
description: Access and operate Watsons Seller Center (ASCP) for order management, product listings, and店铺运营. Use when checking orders, managing inventory, or accessing Watsons seller dashboard.
---

# Watsons Seller Center

Access Watsons Seller Center (ASCP) using Chrome CDP for order management and店铺运营.

## How It Works

1. Chrome runs continuously on the VPS with persistent profile
2. Human logs in once to Watsons Seller Center via Chrome
3. Automation connects to Chrome via CDP and uses existing session

## Prerequisites

### Chrome Must Be Running

```bash
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

1. SSH to VPS with X11 forwarding: `ssh -X enraie`
2. Open Chrome: `google-chrome --user-data-dir=/home/enraie/.chrome-openclaw`
3. Navigate to: https://ascp-watsons.qragoracloud.com/ascp/login
4. Log in with credentials (requires username, password, and company code)
5. Keep Chrome running

## Quick Start

### Check Orders

```bash
cd /home/enraie/.openclaw/workspace/skills/watsons-seller
python3 scripts/access_watsons_chrome.py --check-orders
```

### Access Dashboard

```bash
python3 scripts/access_watsons_chrome.py --url "https://ascp-watsons.qragoracloud.com/ascp/index"
```

### Take Screenshot

```bash
python3 scripts/access_watsons_chrome.py --screenshot /tmp/watsons_dashboard.png
```

## Available URLs

- Login: https://ascp-watsons.qragoracloud.com/ascp/login
- Dashboard: https://ascp-watsons.qragoracloud.com/ascp/index
- Orders: https://ascp-watsons.qragoracloud.com/ascp/order/list
- Products: https://ascp-watsons.qragoracloud.com/ascp/product/list

## Scripts

### access_watsons_chrome.py

Main script for accessing Watsons Seller Center via Chrome CDP.

**Usage:**
```bash
python3 scripts/access_watsons_chrome.py \
  --url "https://ascp-watsons.qragoracloud.com/ascp/index" \
  --screenshot /tmp/watsons.png
```

**Parameters:**
- `--url` - URL to access (default: dashboard)
- `--screenshot` - Path to save screenshot
- `--check-orders` - Extract order summary
- `--cdp-url` - Chrome CDP URL (default: http://127.0.0.1:9222)

## Session Persistence

- Chrome profile stores all cookies
- Session lasts as long as Chrome keeps it
- If logged out, log in again manually via Chrome

## Troubleshooting

### "Cannot connect to Chrome"
Start Chrome with CDP enabled:
```bash
google-chrome \
  --no-sandbox \
  --disable-gpu \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/enraie/.chrome-openclaw &
```

### "Not logged in"
Log in manually via Chrome:
```bash
ssh -X enraie
google-chrome --user-data-dir=/home/enraie/.chrome-openclaw
# Navigate to https://ascp-watsons.qragoracloud.com/ascp/login and log in
```
