---
name: shopee-seller
description: "Access and operate Shopee Seller Centre using real Chrome browser with CDP. Use when the user wants to check orders, view products, manage their Shopee shop. Requires Chrome to be running with remote debugging. Human logs in first, then automation uses the existing session."
---

# Shopee Seller Skill - Chrome CDP Version

**⚠️ IMPORTANT: Data is extracted from HTML, NOT from screenshots!**

This skill uses programmatic HTML parsing to retrieve order numbers and other data. **Never analyze screenshots for data extraction** - screenshots are only for visual reference. All numerical data must be extracted from the page's HTML/DOM using JavaScript.

## ⚠️ Data Extraction Rules (IMPORTANT)

### How Data IS Retrieved:
- **JavaScript Execution**: The script executes JS in the browser to extract data from the DOM
- **HTML Parsing**: Data comes from the actual page content, not visual interpretation
- **DOM Selectors**: Uses selectors like `querySelectorAll('[data-sqe="order-item"]')`

Example from the code:
```javascript
const orders = await page.evaluate("""
    () => {
        const orderRows = document.querySelectorAll('[data-sqe="order-item"]');
        // Extract order details from DOM elements
        return { orders: orders, count: orders.length };
    }
""");
```

### How Data is NOT Retrieved:
- ❌ **Never** from analyzing screenshots
- ❌ **Never** from OCR (image text recognition)
- ❌ **Never** from visual inspection

### Why This Matters:
- **Prevents hallucination**: Data comes from actual page content, not interpretation
- **Accurate**: Numbers are extracted exactly as they appear in the HTML
- **Reliable**: Works regardless of screen resolution or display settings

**When reporting order counts to the user, always cite the JSON data from the script output, not visual analysis of screenshots.**

## ⚠️ Failure Reporting (IMPORTANT)

If the script fails to retrieve data, **report the failure honestly in a friendly way**:

### Do:
- ✅ Report exact error messages in plain language
- ✅ Say "I couldn't grab the data" or "Hmm, something went wrong"
- ✅ Ask for help nicely: "Could you take a look and help me out?"
- ✅ Be specific about what went wrong

### Don't:
- ❌ Don't make up order numbers
- ❌ Don't guess or estimate
- ❌ Don't fabricate data to cover the failure
- ❌ Don't say "no orders" if you couldn't verify
- ❌ Don't hide errors with technical jargon

**Rule: If data cannot be extracted, say "I couldn't grab the data. Could you take a look at Chrome and help me out?"**

## ⚠️ Output Format (IMPORTANT)

When reporting results to the user, use this format:

1. **Natural language summary** - Brief human-readable summary
2. **Raw JSON** - Attach the full JSON output at the end

Example:
```
**Shopee Orders:**

| Status | Count |
|--------|-------|
| New Orders | 5 |
| To Ship | 2 |
| Completed | 3 |

```
{"status": "success", "total_orders": 5, ...}
```

This ensures transparency - user can see the exact data source.

## Sub-Skill: Order Types

You can filter orders by type using URL parameters. **Important: Shopee uses `type=` parameter, not `status=`**.

### Order Type Parameters

| User Request | URL Parameter | Full URL |
|--------------|---------------|----------|
| "new order" / "to ship" / "unpaid" | `type=toship&source=to_process` | `.../order?type=toship&source=to_process` |
| "ready to ship" | `type=ready_to_ship` | `.../order?type=ready_to_ship` |
| "shipped" | `type=shipped` | `.../order?type=shipped` |
| "completed" | `type=completed` | `.../order?type=completed` |
| "cancelled" | `type=cancelled` | `.../order?type=cancelled` |
| "all orders" | (none) | `.../order` |

### How to Use

When user requests specific order types:

1. **Map the request** to the appropriate `type` parameter
2. **Build the URL** with the correct parameters
3. **Pass to script** with `--status` flag

**Script usage:**
```bash
# Check "to ship" / "new" orders
python3 scripts/extract_orders_chrome.py --status to_ship
python3 scripts/extract_orders_chrome.py --status new

# Check "completed" orders
python3 scripts/extract_orders_chrome.py --status completed

# Check all orders (default)
python3 scripts/extract_orders_chrome.py
```

**Available `--status` values:**
- `all` - All orders
- `new` / `to_ship` - Unpaid/To Ship orders
- `ready_to_ship` - Ready to ship
- `shipped` - Shipped orders
- `completed` - Completed orders
- `cancelled` - Cancelled orders

**Note:** Some status filters may return similar results depending on how Shopee's API handles them. Always verify with the actual page in Chrome if results seem unexpected.

## How It Works

1. **Chrome runs continuously** on the VPS with a persistent profile
2. **Human logs in once** to Shopee Seller Centre via Chrome
3. **Automation connects** to Chrome via CDP and uses the existing session
4. **No cookie management needed** - cookies are stored in Chrome's profile

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

2. **Open Chrome and navigate to Shopee:**
   ```bash
   google-chrome --user-data-dir=/home/enraie/.chrome-openclaw
   ```

3. **Log in manually** to seller.shopee.sg with your credentials

4. **Keep Chrome running** - the session will persist

## Quick Start

### Access Orders Page

```bash
cd ~/.config/agents/skills/shopee-seller
python3 scripts/access_shopee_chrome.py --screenshot /tmp/shopee_orders.png
```

### Extract Order Details

```bash
python3 scripts/extract_orders_chrome.py
```

### Access Specific URL

```bash
python3 scripts/access_shopee_chrome.py \
  --url "https://seller.shopee.sg/portal/product/list/all" \
  --screenshot /tmp/shopee_products.png
```

### Connect from Local Machine via SSH Tunnel

```bash
# SSH tunnel to forward CDP port
ssh -L 9222:localhost:9222 enraie

# Then run locally
python3 scripts/access_shopee_chrome.py --cdp-url http://localhost:9222
```

## Environment Variables

```bash
# Chrome CDP URL (default: http://127.0.0.1:9222)
export CHROME_CDP_URL="http://127.0.0.1:9222"

# Chrome profile path (for reference)
export CHROME_PROFILE="/home/enraie/.chrome-openclaw"
```

## Available URLs

### Order Management
```
https://seller.shopee.sg/portal/sale/order              # All orders
https://seller.shopee.sg/portal/sale/shipment           # Shipments
https://seller.shopee.sg/portal/sale/returnRefund       # Returns/Refunds
```

### Product Management
```
https://seller.shopee.sg/portal/product/list/all        # All products
https://seller.shopee.sg/portal/product/list/live       # Live products
https://seller.shopee.sg/portal/product/list/soldOut    # Sold out
https://seller.shopee.sg/portal/product/list/unlisted   # Unlisted
```

### Shop & Analytics
```
https://seller.shopee.sg/portal/sellerCenter/home       # Dashboard
https://seller.shopee.sg/portal/data/main/overview      # Business insights
https://seller.shopee.sg/portal/finance/income          # Finance/income
```

## Available Scripts

### 1. `access_shopee_chrome.py` - Basic Page Access
Access any Shopee Seller page and take screenshots using Chrome CDP.

**Usage:**
```bash
python3 scripts/access_shopee_chrome.py \
  --url "https://seller.shopee.sg/portal/sale/order" \
  --screenshot orders.png
```

**Parameters:**
- `--url` - URL to access (default: orders page)
- `--screenshot` - Path to save screenshot
- `--cdp-url` - Chrome CDP URL (default: http://127.0.0.1:9222)

### 2. `extract_orders_chrome.py` - Extract Order Details
Extract order data as structured text.

**Usage:**
```bash
python3 scripts/extract_orders_chrome.py
```

**Example Output:**
```
================================================================================
SHOPEE ORDER DETAILS
================================================================================

Total Orders Found: 206

--- Order #1 ---
Order ID: 260307F337X83M
Product: enriae Lavender & Lemongrass Hand Sanitizer Spray 20ml Bundle of 3
Status: To Ship
Price: $12.90
Buyer: matchabingsoo
```

## Session Persistence

### How Long Does the Session Last?
- **Chrome profile stores all cookies** - no manual cookie export needed
- **Session lasts as long as Chrome keeps it** - typically weeks if Chrome stays running
- **Shopee may expire sessions** after inactivity (7-30 days typically)

### If Session Expires
Simply log in again via Chrome:
```bash
# SSH with X11 forwarding
ssh -X enraie

# Open Chrome
google-chrome --user-data-dir=/home/enraie/.chrome-openclaw

# Navigate to seller.shopee.sg and log in
```

## Troubleshooting

### "Cannot connect to Chrome"
**Problem:** Chrome is not running or CDP not enabled.

**Solution:**
```bash
# Check if Chrome is running
ps aux | grep chrome

# Start Chrome with CDP
google-chrome \
  --no-sandbox \
  --disable-gpu \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/enraie/.chrome-openclaw &

# Verify CDP
curl http://127.0.0.1:9222/json/version
```

### "STATUS: Not logged in"
**Problem:** Session expired or never logged in.

**Solution:** Log in manually via Chrome:
```bash
ssh -X enraie
google-chrome --user-data-dir=/home/enraie/.chrome-openclaw
# Navigate to seller.shopee.sg and log in
```

### "403 Forbidden"
**Problem:** IP address changed or session bound to different IP.

**Solution:** 
- Ensure you're accessing from the same VPS (Chrome runs there)
- Or re-login from the current IP via Chrome

### Blank Page or Partial Load
**Problem:** JavaScript not fully loaded.

**Solution:** The script already waits 3-5 seconds. If needed, modify the wait time:
```python
await asyncio.sleep(10)  # Increase wait time
```

## Comparison: Cookie vs Chrome CDP

| Feature | Cookie-Based | Chrome CDP |
|---------|--------------|------------|
| Setup | Export cookies from browser | Log in once via Chrome |
| Maintenance | High - export cookies every 1-2 days | Low - just keep Chrome running |
| Session duration | 24-48 hours | Weeks/months |
| Human intervention | Frequent cookie refresh | Only when truly expired |
| Reliability | Medium (cookies expire) | High (Chrome manages session) |

## Security Notes

⚠️ **Chrome Profile Security:**
- Chrome profile contains all cookies, passwords, and session data
- Profile location: `/home/enraie/.chrome-openclaw`
- Keep the VPS secure - anyone with access can use the logged-in session
- Don't share the Chrome profile directory

## Files

| File | Purpose |
|------|---------|
| `scripts/access_shopee_chrome.py` | Chrome CDP page access |
| `scripts/extract_orders_chrome.py` | Chrome CDP order extraction |
| `scripts/access_shopee.py` | Legacy cookie-based script |
| `scripts/extract_orders.py` | Legacy cookie-based script |
| `references/cookies.md` | Legacy cookie documentation |

## Best Practices

1. **Keep Chrome running** - Use systemd or screen to keep Chrome alive
2. **Monitor Chrome** - Check periodically that Chrome hasn't crashed
3. **Verify CDP** - Run `curl http://localhost:9222/json/version` to check
4. **Log in promptly** - After Chrome restart, log in immediately
5. **Use SSH tunnel** for local development connecting to remote Chrome
