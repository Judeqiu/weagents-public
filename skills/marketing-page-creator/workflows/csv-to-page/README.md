# CSV to Product Page Workflow

A proven 3-phase workflow for creating product list pages from e-commerce sites.

## ⚠️ CRITICAL: REAL DATA ONLY

**THIS WORKFLOW NEVER USES FAKE, MOCK, OR SIMULATED DATA.**

### Rules:
- ✅ All products MUST be extracted from real websites
- ✅ All URLs MUST point to actual product pages
- ✅ All images MUST be from the source site
- ✅ All prices MUST be scraped (not invented)

### If Extraction Fails:
- ❌ STOP - Do not proceed
- ❌ DO NOT create placeholder data
- ❌ DO NOT use "example" products
- ✅ Report failure and try different approach

**NEVER proceed to Phase 2 with fake data. This is non-negotiable.**

## Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Phase 1   │ →  │   Phase 2   │ →  │   Phase 3   │
│   Research  │    │   Generate  │    │   Deploy    │
│  (CSV Data) │    │  (HTML Page)│    │  (Netlify)  │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🌐 Browser Setup for E-Commerce Sites

**For e-commerce sites (Amazon, eBay, etc.), ALWAYS use `mychrome` skill with Chrome CDP.**

### Why mychrome for E-Commerce?

E-commerce sites have sophisticated anti-bot detection. Using a real Chrome instance via CDP provides the best stealth:

```bash
# Step 1: Start Chrome with CDP on your remote host
ssh spost "export DISPLAY=:99 && ~/start-chrome.sh"

# Step 2: Use mychrome skill to connect
# Chrome will be available at localhost:9222 (via SSH tunnel)

# Step 3: Run research with Chrome CDP
python research.py --query "laptops" --use-chrome-cdp
```

### SSH Tunnel for CDP (Recommended)

```bash
# Create SSH tunnel to access Chrome remotely
ssh -L 9222:localhost:9222 spost

# Now Chrome CDP is available locally at http://localhost:9222
# Use mychrome skill or connect your research script to localhost:9222
```

### Alternative: Direct Playwright with CDP

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Connect to Chrome via CDP
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    page = context.pages[0] if context.pages else context.new_page()
    
    # Navigate to e-commerce site
    page.goto("https://amazon.com/s?k=laptops")
    
    # Extract products...
```

**⚠️ DO NOT use simple HTTP requests (curl) for e-commerce sites - you will be blocked.**

## Quick Start

```bash
# Phase 1: Research products and save to CSV
python research.py --query "electronics deals" --max-items 20

# Phase 2: Generate HTML page from CSV
python generate_page.py --input products_20260324_123456.csv --title "My Deals Page"

# Phase 3: Deploy to Netlify
./deploy.sh ./site --prod
```

## Phase 1: Research Products

### Amazon UK Example

```bash
python research.py \
  --site amazon \
  --query "best sellers electronics" \
  --max-items 20 \
  --output ./my_products.csv
```

### Output CSV Format

| Column | Description | Example |
|--------|-------------|---------|
| `title` | Product name | "Wireless Headphones" |
| `price` | Current price | "£49.99" |
| `original_price` | List/original price | "£79.99" |
| `rating` | Star rating | "4.5" |
| `reviews` | Review count | "1.2K" |
| `link` | Product URL | "https://amazon.co.uk/..." |
| `image` | Image URL | "https://m.media-amazon.com/..." |
| `category` | Auto-detected category | "electronics" |

### Features

- ✅ Automatic category detection (electronics, fashion, home)
- ✅ Anti-bot stealth techniques
- ✅ Handles missing data gracefully
- ✅ Saves both CSV and JSON formats

---

## 🔍 VERIFICATION STEP (Between Phase 1 & 2)

**BEFORE running Phase 2, you MUST verify:**

```bash
# 1. Check CSV file exists and has content
ls -lh products_*.csv

# 2. View first few rows - MUST show real product data
head -5 products_20260324_123456.csv

# 3. Verify URLs are from actual source (NOT example.com)
grep -c "amazon.co.uk" products_*.csv

# 4. Verify images are real (not placeholder)
grep -c "m.media-amazon.com" products_*.csv
```

**Checklist:**
- [ ] CSV contains > 5 real products
- [ ] All URLs point to actual product pages
- [ ] Images are from source domain
- [ ] Prices look realistic (not all identical)
- [ ] NO placeholder text like "Example Product"

**If verification fails → STOP. Do NOT proceed to Phase 2.**

---

## Phase 2: Generate HTML Page

### Basic Usage

```bash
python generate_page.py --input products.csv
```

### With Custom Title

```bash
python generate_page.py \
  --input products.csv \
  --title "Amazon UK Best Deals" \
  --subtitle "Hand-picked electronics and fashion" \
  --source "Amazon UK"
```

### Page Features

- **Responsive Design**: Works on mobile, tablet, desktop
- **Category Filtering**: Click to filter by category
- **Product Cards**: Image, title, price, rating, reviews
- **Hover Effects**: Smooth animations
- **Stats Bar**: Product count, categories, avg rating
- **Direct Links**: Click through to product pages

### Output Structure

```
site/
└── index.html    # Complete standalone page
```

## Phase 3: Deploy to Netlify

### Prerequisites

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login (one-time)
netlify login
```

### Deploy Commands

```bash
# Draft deploy (preview URL)
./deploy.sh ./site

# Production deploy
./deploy.sh ./site --prod

# Or use netlify directly
cd site && netlify deploy --prod --dir=.
```

### Deployment Output

```
✅ Deploy successful!

🌐 Live URL: https://clawpilot-landing-12345678.netlify.app
```

## Complete Workflow Example

```bash
# 1. Create working directory
mkdir my-deals-page && cd my-deals-page

# 2. Copy workflow scripts
cp /path/to/skill/workflows/csv-to-page/* .

# 3. Research products
python research.py \
  --query "deals fashion" \
  --max-items 15 \
  --output fashion_deals.csv

# 4. Generate page
python generate_page.py \
  --input fashion_deals.csv \
  --title "Fashion Deals UK" \
  --subtitle "Best fashion deals from Amazon"

# 5. Deploy
./deploy.sh ./site --prod
```

## Customization

### Modify Product Extraction

Edit `research.py` → `_extract_amazon_product()` method:

```python
# Add custom fields
item['brand'] = await self._extract_brand(product)
item['discount'] = self._calculate_discount(price, original_price)
```

### Modify Page Template

Edit `generate_page.py` → `HTML_TEMPLATE`:

```html
<!-- Add custom CSS -->
<style>
    .custom-badge { background: #ff6b6b; }
</style>

<!-- Add custom HTML sections -->
<div class="custom-section">
    <h2>Special Offers</h2>
</div>
```

### Add New Sites

Extend `research.py` with new site methods:

```python
async def research_asos(self, query, max_items=20):
    """Research products from ASOS"""
    # Implementation
    pass
```

## Anti-Bot Tips

For heavily protected sites (Amazon, ASOS, etc.):

1. **Use Playwright with stealth args** (already included)
2. **Add delays between requests**
3. **Rotate user agents**
4. **Use residential proxies** (if available)

```python
# Add delay between page loads
await asyncio.sleep(random.uniform(2, 5))
```

## Troubleshooting

### No products found
- Check if site structure changed
- Try increasing timeout
- Check if IP is blocked

### Missing images
- Some sites use lazy loading
- Try scrolling before extraction
- Use placeholder fallback

### Deployment fails
- Ensure `index.html` exists in site directory
- Check Netlify CLI is logged in: `netlify status`
- Try manual deploy via Netlify web UI

## File Structure

```
csv-to-page/
├── research.py          # Product extraction script
├── generate_page.py     # HTML generator
├── deploy.sh            # Netlify deploy script
├── README.md            # This documentation
└── example/
    ├── products.csv     # Sample data
    └── site/
        └── index.html   # Sample output
```

## Dependencies

```bash
# Install Python dependencies
pip install playwright
playwright install chromium

# Install Node.js dependencies
npm install -g netlify-cli
```

## Version

1.0.0 - Initial workflow release
