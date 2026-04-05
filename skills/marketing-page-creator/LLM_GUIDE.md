# LLM Quick Reference Guide

Quick guide for using the marketing-page-creator skill effectively.

## When to Use Each Tool

### 1. research_site.sh
**Use when:** User mentions one or more specific sites

```bash
# Single site
./tools/research_site.sh --site amazon --query "wireless headphones" --max-items 5

# For sites known to block bots (force browser)
./tools/research_site.sh --site amazon --query "shoes" --max-items 5 --use-browser
```

**Output:** `{"site": "...", "query": "...", "used_browser": true/false, "products": [...]}`

---

### 2. research_parallel.sh
**Use when:** User wants multiple sites AND speed matters

```bash
# Research 3 sites in parallel
./tools/research_parallel.sh --sites "amazon,asos,johnlewis" --query "summer dresses" --max-items 5
```

**Output:** `{"query": "...", "sites": [...], "total_products": N, "products": [...]}`

**When to use parallel:**
- ✅ User wants 3+ sites
- ✅ Speed is important
- ❌ Don't use for 1-2 sites (overhead not worth it)

---

### 3. fetch_product_page.sh
**Use when:** User provides a specific product URL

```bash
./tools/fetch_product_page.sh --url "https://www.amazon.co.uk/dp/B08XYZ123"
```

**Output:** `{"url": "...", "source": "smart_fetch", "title": "...", "content_length": N}`

---

### 4. filter_products.sh
**Use when:** Need to refine product selection

```bash
# Pipe products JSON to filter
cat products.json | ./tools/filter_products.sh --max-items 5 --sort-by discount

# Filter by price and rating
cat products.json | ./tools/filter_products.sh --max-price 100 --min-rating 4.0

# Multiple filters
cat products.json | ./tools/filter_products.sh \
  --min-discount 20 \
  --max-price 80 \
  --sort-by rating \
  --max-items 8
```

**Options:**
- `--min-discount N` - Minimum % discount
- `--max-price N` - Maximum price
- `--min-rating N` - Minimum star rating
- `--max-items N` - Limit results
- `--sort-by` - `discount`, `price`, or `rating`

---

### 5. generate_page.sh
**Use when:** Products are approved and ready for page creation

```bash
# Basic usage
cat products.json | ./tools/generate_page.sh --title "My Deals Page"

# With options
cat products.json | ./tools/generate_page.sh \
  --title "Summer Dress Deals" \
  --template deals \
  --output-dir ./my-site \
  --primary-color "#ff6b6b"
```

**Templates:** `deals` (default), `comparison`, `showcase`, `minimal`

**Output:** Path to generated `index.html`

---

### 6. deploy.sh
**Use when:** User confirms deployment

```bash
# Deploy directory
./tools/deploy.sh --dir ./my-site

# With custom name
./tools/deploy.sh --dir ./my-site --site-name "my-deals-page"
```

**Output:** Live URL (e.g., `https://my-deals-page-123.netlify.app`)

---

## Typical Workflows

### Workflow 1: Simple Deals Page
```
User: "Create a deals page for men's shoes"

1. Research popular sites
   research_site.sh --site amazon --query "men's shoes"
   research_site.sh --site asos --query "men's shoes"

2. Combine and filter
   (combine JSON arrays) | filter_products.sh --max-items 6 --sort-by discount

3. Present to user for approval

4. Generate and deploy
   generate_page.sh | deploy.sh
```

### Workflow 2: Specific Requirements
```
User: "I need tech gadgets under £50 with 4+ stars from Amazon and Currys"

1. Parallel research (faster)
   research_parallel.sh --sites "amazon,currys" --query "tech gadgets"

2. Filter strictly
   filter_products.sh --max-price 50 --min-rating 4.0 --sort-by rating

3. Present filtered results

4. Generate comparison page
   generate_page.sh --template comparison
```

### Workflow 3: Anti-Bot Site
```
User: "Find products on Amazon" (Amazon blocks bots)

1. Research with automatic fallback
   research_site.sh --site amazon --query "products"
   → Automatically detects blocking
   → Falls back to agent-browser skill
   → Returns real data

2. Continue as normal
```

---

## Handling Edge Cases

### Site Returns Empty
```
research_site.sh returns: {"products": [], "extraction_failed": true}

Action:
- Tell user: "[Site] isn't responding. Trying [alternative]..."
- Research alternative site
- Or use mock data with disclaimer
```

### Agent-Browser Not Available
```
If agent-browser skill not found:
- curl attempt only
- If blocked → mock data fallback
- Tell user: "Using simulated data for [site]"
```

### User Provides URL
```
User: "Add this product: https://amazon.co.uk/dp/..."

Action:
fetch_product_page.sh --url "https://amazon.co.uk/dp/..."
→ Extracts product info
→ Add to selection
```

---

## JSON Data Format

### Product Object
```json
{
  "name": "Product Name",
  "brand": "Brand Name",
  "price": 49.99,
  "original_price": 79.99,
  "discount": "37%",
  "site": "amazon",
  "url": "https://www.amazon.co.uk/...",
  "rating": 4.5,
  "reviews": 1200,
  "category": "search query"
}
```

### Combined Results
```json
{
  "query": "search term",
  "sites": ["amazon", "asos"],
  "total_products": 10,
  "products": [...]
}
```

---

## Anti-Bot Status Reference

| Site | Level | Method Usually Used |
|------|-------|---------------------|
| Amazon | 🔴 High | Browser automation |
| ASOS | 🟡 Medium | curl → browser fallback |
| John Lewis | 🟢 Low | curl usually works |
| Currys | 🟡 Medium | curl → browser fallback |
| Next | 🟡 Medium | curl → browser fallback |
| Argos | 🟢 Low | curl usually works |

---

## Best Practices

1. **Always present before deploying**
   - Show product summary table
   - Ask for confirmation
   - Offer edits

2. **Use parallel research for 3+ sites**
   - Much faster than sequential
   - Better user experience

3. **Handle failures gracefully**
   - One site fails? Continue with others
   - All fail? Use mock data + disclaimer

4. **Filter intelligently**
   - "Best deals" → sort by discount
   - "Top rated" → sort by rating
   - "Budget options" → filter by price

5. **Let user customize**
   - "Remove item 3"
   - "Add more from Nike"
   - "Only under £50"
