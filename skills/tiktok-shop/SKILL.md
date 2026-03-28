---
name: tiktok-shop
description: Access and operate TikTok Shop Seller Center (Singapore) for order management. Use when checking orders, viewing order details, or accessing TikTok Shop seller dashboard.
---

# TikTok Shop Seller Center

Access TikTok Shop Seller Center (SG) using Chrome CDP for order management.

## How It Works

1. Chrome runs continuously on the VPS with persistent profile
2. Human logs in once to TikTok Shop Seller Center via Chrome
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
3. Navigate to: https://seller-sg.tiktok.com/account/login
4. Log in with credentials
5. Keep Chrome running

## Quick Start

### Check Orders (To Ship)

```bash
cd /home/enraie/.openclaw/workspace/skills/tiktok-shop
python3 scripts/tiktok_orders.py --tab to_ship --check-orders
```

### Check All Order Tabs

```bash
# Check all orders
python3 scripts/tiktok_orders.py --tab all --check-orders

# Check in transit
python3 scripts/tiktok_orders.py --tab in_transit --check-orders

# Check delivered
python3 scripts/tiktok_orders.py --tab delivered --check-orders

# Check returns
python3 scripts/tiktok_orders.py --tab returns --check-orders
```

### Access Dashboard

```bash
python3 scripts/tiktok_orders.py --url "https://seller-sg.tiktok.com/homepage"
```

### Take Screenshot

```bash
python3 scripts/tiktok_orders.py --screenshot /tmp/tiktok_dashboard.png
```

## Available URLs

- Login: https://seller-sg.tiktok.com/account/login
- Dashboard: https://seller-sg.tiktok.com/homepage
- Orders (All): https://seller-sg.tiktok.com/order/m/order-list?tab=all
- Orders (To Ship): https://seller-sg.tiktok.com/order/m/order-list?tab=unfulfillable
- Orders (In Transit): https://seller-sg.tiktok.com/order/m/order-list?tab=in_transit
- Orders (Delivered): https://seller-sg.tiktok.com/order/m/order-list?tab=delivered

## Scripts

### tiktok_orders.py

Main script for accessing TikTok Shop Seller Center via Chrome CDP.

**Usage:**
```bash
python3 scripts/tiktok_orders.py \
  --url "https://seller-sg.tiktok.com/homepage" \
  --screenshot /tmp/tiktok.png
```

**Parameters:**
- `--url` - URL to access (default: dashboard)
- `--screenshot` - Path to save screenshot
- `--check-orders` - Extract order summary
- `--tab` - Go to specific order tab (all, to_ship, unfulfillable, in_transit, delivered, returns)
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
# Navigate to https://seller-sg.tiktok.com/account/login and log in
```
