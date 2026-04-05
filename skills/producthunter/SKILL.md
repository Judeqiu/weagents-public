---
name: producthunter
description: Hunt and extract product information from e-commerce websites using Chrome CDP with lextok-search fallback. Use when users need to fetch product details (title, description, price, photos, ratings, etc.) from any e-commerce site and save to CSV. Falls back to Brave Search API when Chrome CDP is unavailable or extraction fails.
---

# ProductHunter Skill

Extract product information from e-commerce websites using **Chrome CDP** with **lextok-search fallback**. When Chrome CDP is unavailable or extraction fails, the skill automatically falls back to Brave Search API to find product information.

## What It Does

ProductHunter automates e-commerce product research:

1. **Visits e-commerce sites** using Chrome CDP (Chrome DevTools Protocol)
2. **Falls back to search** when CDP is unavailable or extraction fails
3. **Extracts product details**: title, description, price, ratings, availability
4. **Handles pagination** for multiple products
5. **Saves data to CSV** for analysis
6. **Uses natural language** to drive extraction tasks

## When to Use

Use this skill when you need to:
- Extract product details from any e-commerce website
- Compare prices across products
- Build product catalogs from online stores
- Monitor product availability and pricing
- Research competitor products
- Gather product images and specifications

## Prerequisites

### Option 1: Chrome with Remote Debugging (Recommended)

For best results, use Chrome CDP. Start Chrome with remote debugging enabled:

```bash
# Start Chrome with CDP
google-chrome \
  --no-sandbox \
  --disable-gpu \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.chrome-producthunter \
  --window-size=1920,1080
```

**Verify CDP is working:**
```bash
curl http://127.0.0.1:9222/json/version
```

### Option 2: Brave API Key (Fallback Mode)

If Chrome is not available, configure Brave Search API key for fallback mode:

```bash
# Edit lextok-search config
vi ./skills/lextok-search/config.json
```

Set your Brave API key:
```json
{
  "brave_api_key": "YOUR_BRAVE_API_KEY_HERE"
}
```

Get a free API key at https://api.search.brave.com/

## Quick Start

### Extract Single Product (CDP Mode)

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com/product/123" \
  --output ./products.csv
```

### Extract Multiple Products (Search Results)

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com/search?q=laptop" \
  --multiple \
  --max-products 20 \
  --output ./products.csv
```

### Natural Language Request

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --request "Find wireless headphones under $100 on bestbuy.com" \
  --output ./headphones.csv
```

### Fallback Mode (No Chrome Required)

If Chrome CDP is not available, the skill automatically uses Brave Search API:

```bash
# This will work even without Chrome running
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://amazon.com/s?k=laptop" \
  --output ./laptops.csv
```

To disable fallback and require CDP only:
```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com/product/123" \
  --no-search-fallback \
  --output ./products.csv
```

## Core Workflows

### 1. Single Product Extraction

Extract detailed information from a single product page:

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://www.amazon.com/dp/B08N5WRWNW" \
  --fields title,price,description,rating,images \
  --output ./product.csv
```

**Extracted fields:**
- `title` - Product name/title
- `description` - Product description
- `price` - Current price
- `original_price` - Original/strikethrough price
- `currency` - Price currency
- `rating` - Average rating
- `review_count` - Number of reviews
- `availability` - Stock status
- `images` - Product image URLs (comma-separated)
- `brand` - Product brand
- `sku` - Product SKU/ID
- `category` - Product category
- `specifications` - Key specifications

### 2. Search Results Extraction

Extract multiple products from search/category pages:

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://www.amazon.com/s?k=laptop" \
  --multiple \
  --max-products 50 \
  --scroll \
  --output ./laptops.csv
```

**Options:**
- `--multiple` - Enable multi-product extraction mode
- `--max-products N` - Limit to N products (default: 50)
- `--scroll` - Scroll page to load more products
- `--scroll-pause 2` - Pause seconds between scrolls (default: 2)

### 3. Natural Language Driven Extraction

Describe what you want in natural language:

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --request "Get all iPhone 15 models with prices from apple.com" \
  --output ./iphones.csv
```

The skill will:
1. Parse your request
2. Navigate to the appropriate URL
3. Extract the requested products
4. Save to CSV

### 4. Batch Processing

Process multiple URLs from a file:

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --batch urls.txt \
  --output ./batch_products.csv
```

Where `urls.txt` contains one URL per line.

## Output Format

### CSV Structure

```csv
timestamp,source_url,title,description,price,original_price,currency,rating,review_count,availability,brand,sku,category,images,specifications
2024-01-15T10:30:00,https://...,Wireless Headphones,Noise cancelling...,79.99,99.99,USD,4.5,1234,In Stock,SoundMax,WH-1000,Electronics,https://img1.jpg|https://img2.jpg,Bluetooth 5.0|Battery 30h
```

### JSON Output (Optional)

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com/product/123" \
  --format json \
  --output ./product.json
```

## Advanced Usage

### Custom Field Selection

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com/products" \
  --fields title,price,rating,images \
  --multiple \
  --output ./products.csv
```

### Custom Selectors (for unsupported sites)

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com/product/123" \
  --title-selector "h1.product-name" \
  --price-selector "span.price" \
  --image-selector "img.product-image" \
  --output ./product.csv
```

### Proxy Support

```bash
export CHROME_CDP_URL="http://proxy-server:9222"

python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com/product" \
  --output ./product.csv
```

### With Screenshots

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com/product/123" \
  --screenshot ./product.png \
  --output ./product.csv
```

## Anti-Detection Measures

ProductHunter includes built-in stealth measures:

1. **WebDriver hiding** - navigator.webdriver is undefined
2. **Real browser profile** - Uses your Chrome profile
3. **Human-like delays** - Random delays between actions
4. **Viewport simulation** - Realistic window dimensions
5. **User-Agent consistency** - Matches Chrome version

### Rate Limiting

Add delays to avoid detection:

```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com/products" \
  --multiple \
  --delay 3 \
  --output ./products.csv
```

## Troubleshooting

### "Cannot connect to Chrome"

**Problem:** Chrome not running or CDP not enabled.

**Solution:**
```bash
# Check if Chrome is running
ps aux | grep chrome

# Start Chrome with CDP
google-chrome --remote-debugging-port=9222 --user-data-dir=~/.chrome-producthunter &

# Verify
curl http://127.0.0.1:9222/json/version
```

**Fallback:** If Chrome is unavailable, the skill will automatically use lextok-search if Brave API key is configured.

### "No products found"

**Problem:** Site structure not recognized or products loaded dynamically.

**Solution:**
- Use `--scroll` to load lazy-loaded products
- Increase `--wait` time for JavaScript rendering
- Check with `--screenshot` to see page state
- Use custom selectors with selector options

### "Access denied / CAPTCHA"

**Problem:** Site detected automation.

**Solution:**
- Ensure Chrome has valid session cookies
- Increase `--delay` between requests
- Use a residential proxy
- Check if site requires login

### "Timeout waiting for page"

**Problem:** Page takes too long to load.

**Solution:**
```bash
python3 ./skills/producthunter/scripts/product_hunter.py \
  --url "https://example.com" \
  --timeout 60000 \
  --output ./products.csv
```

## Command Reference

| Option | Description |
|--------|-------------|
| `--url` | Target URL to extract products from |
| `--request` | Natural language request description |
| `--output` | Output CSV/JSON file path |
| `--multiple` | Extract multiple products from page |
| `--max-products` | Maximum products to extract (default: 50) |
| `--fields` | Comma-separated list of fields to extract |
| `--format` | Output format: csv or json (default: csv) |
| `--scroll` | Scroll page to load more products |
| `--scroll-pause` | Seconds to pause between scrolls |
| `--delay` | Delay between requests in seconds |
| `--timeout` | Page load timeout in milliseconds |
| `--screenshot` | Save screenshot of page |
| `--batch` | File with URLs to process |
| `--cdp-url` | Chrome CDP URL (default: http://127.0.0.1:9222) |
| `--title-selector` | Custom CSS selector for title |
| `--price-selector` | Custom CSS selector for price |
| `--image-selector` | Custom CSS selector for images |
| `--wait` | Additional wait time after page load |
| `--no-search-fallback` | Disable lextok-search fallback |

## Supported E-commerce Platforms

ProductHunter includes optimized selectors for:

- Amazon (amazon.com, amazon.co.uk, etc.)
- eBay (ebay.com)
- Walmart (walmart.com)
- Target (target.com)
- Best Buy (bestbuy.com)
- Shopify stores (generic detection)
- WooCommerce stores (generic detection)
- Generic e-commerce sites (fallback selectors)

For unsupported sites, use custom selectors or the skill will attempt generic extraction.

## Best Practices

1. **Keep Chrome running** - Start Chrome once, use for multiple extractions
2. **Use delays** - Add `--delay` for sites with strict rate limiting
3. **Verify output** - Check first few extractions for accuracy
4. **Respect robots.txt** - Only extract data you have permission to access
5. **Batch processing** - Use `--batch` for multiple URLs
6. **Screenshots for debugging** - Use `--screenshot` when extraction fails

## Files

| File | Purpose |
|------|---------|
| `scripts/product_hunter.py` | Main extraction script (Chrome CDP + lextok-search fallback) |
| `SKILL.md` | This documentation |

## How Fallback Works

When Chrome CDP is unavailable or extraction fails:

1. **Automatic Detection**: Skill detects CDP connection failure
2. **Search Query Construction**: Converts URL to search query
3. **Brave Search**: Uses lextok-search to find product information
4. **Result Parsing**: Extracts product details from search results
5. **CSV Output**: Saves data in same format as CDP mode

### Fallback Limitations

Compared to CDP mode, fallback mode:
- ✓ Works without Chrome running
- ✓ Less likely to be blocked by anti-bot measures
- ✗ May have less detailed information
- ✗ No image URLs extracted
- ✗ No JavaScript-rendered content
- ✗ Limited to publicly indexed information

## Security Notes

- Chrome CDP provides full browser control - secure your system
- Product data may be copyrighted - check website terms of service
- Use responsibly and respect rate limits
- Session data is stored in Chrome profile

## Performance

| Task | Products | Time |
|------|----------|------|
| Single product | 1 | 5-10s |
| Search page | 20-50 | 30-60s |
| Category page | 100+ | 2-5 min |

## Future Enhancements

- Automatic pagination handling
- Product change detection
- Scheduled monitoring
- Price drop alerts
- Integration with product databases
- Enhanced fallback with more search sources
