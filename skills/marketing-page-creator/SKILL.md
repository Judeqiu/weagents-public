---
name: marketing-page-creator
description: Create professional marketing landing pages from natural language requests. Research REAL products from multiple sites (never simulated data), curate the best deals, design beautiful pages, and deploy to Netlify. Let the user describe what they want in plain English.
---

# Marketing Page Creator (Natural Language Driven)

Create complete marketing landing pages through conversation. No need to remember command syntax - just tell me what you want to build.

## 🚨 CRITICAL: REAL DATA ONLY - NO EXCEPTIONS

**This skill ONLY uses real data extracted from actual websites.**

### Absolute Rules:
- For most bot-protected e-commerce websites, use "mychrome" skill to fetch data
- Use mychrome and agent-browser skill to access the pages, it is possible that the page could block bots, don't panick, try different ways, don't stop untill you get the data.
- ✅ All products MUST be scraped from real e-commerce sites
- ✅ All URLs MUST point to actual product pages  
- ✅ All images MUST be from the source site's CDN
- ✅ All prices MUST be extracted (not invented)
- Don't use existing csv file, always fetch latest new data from web and create new csv file.
- NO FAKE DATA
- If you cannot find real data in CSV, stop and tell the truth
- You are not allow to create CSV with fake/sample data.
- You will be shutdown if you use fake data
- ❌ NEVER create mock, simulated, or placeholder data
- ❌ NEVER use "example.com" URLs
- ❌ NEVER proceed with fake data "just to have something"

### What Happens If Extraction Fails:
1. **STOP** - Do not proceed to page generation
2. **Report** the failure to the user
3. **Suggest** alternatives (different site, different search terms)
4. **DO NOT** create fake data to compensate

**Verification is MANDATORY before page generation. This is non-negotiable.**

## Quick Examples

**Simple request:**
> "Create a deals page for men's running shoes"

**Specific request:**
> "Find summer dresses on ASOS and John Lewis, show me the best 5 deals under £50, then make a nice landing page"

**Full workflow:**
> "I want to promote tech gadgets for Black Friday. Research Amazon and Currys, pick the top 10 deals with at least 30% off, create a dark-themed comparison page, and deploy it"

**CSV-to-Page Workflow:**
> "Research Amazon UK electronics deals, save to CSV, generate a product list page, and deploy to Netlify"

*This uses the proven workflow: research → CSV → HTML → deploy*
> 1. Extract products to CSV with `workflows/csv-to-page/research.py`
> 2. Generate HTML page with `workflows/csv-to-page/generate_page.py`
> 3. Deploy with `workflows/csv-to-page/deploy.sh`
>
> Result: A live product page like [this example](https://clawpilot-landing-1773064086.netlify.app)

## How It Works

This skill uses **natural language orchestration**. Instead of rigid scripts, you describe your goal and I:

1. **Understand** what you're looking for
2. **Research** across multiple sites
3. **Curate** the best options
4. **Show you** what I found for approval
5. **Design** and deploy the page

## Available Tools

These are the tools I can use on your behalf:

| Tool | Purpose | When I Use It |
|------|---------|---------------|
| `research_site.sh` | Research products from one site | When you mention a specific retailer |
| `research_parallel.sh` | Research multiple sites at once | When speed matters, parallel execution |
| `fetch_product_page.sh` | Fetch specific product page | When you want details from a URL |
| `filter_products.sh` | Filter and sort products | To find the "best" deals based on your criteria |
| `generate_page.sh` | Create HTML page | After you approve the products |
| `deploy.sh` | Deploy to Netlify | When you're ready to go live |

### Anti-Bot Protection 🛡️

The `research_site.sh` tool automatically handles sites that block bots:

1. **First attempt:** Fast curl request
2. **If blocked:** Automatically falls back to agent-browser skill
3. **Agent-browser tries:** Local Chromium → Chrome CDP → Browserless API (cloud)
4. **Result:** Real product data even from protected sites

You can also force browser automation:
```bash
# For sites known to block bots
research_site.sh --site amazon --query "shoes" --use-browser
```

## Workflow

### Step 1: Understand Your Goal

When you make a request, I'll ask clarifying questions if needed:

- **What products?** (be specific: "wireless headphones" not just "electronics")
- **Which sites?** (I'll suggest popular ones if you don't specify)
- **How many items?** (default: 5-8 for good visual balance)
- **Any filters?** (price range, minimum discount, brand preferences)
- **Template style?** (deals grid, comparison table, showcase - I'll pick based on your goal)

### Step 2: Research

I'll research each site you mentioned:

```
User: "Find Nike shoes on Amazon and ASOS"
→ I'll run:
   research_site.sh --site amazon --query "Nike shoes"
   research_site.sh --site asos --query "Nike shoes"
```

**Anti-Bot Handling:**
If a site blocks automated access (Amazon, ASOS, etc.), I'll automatically:
1. Detect the blocking (CAPTCHA, JavaScript requirements, etc.)
2. Switch to agent-browser skill with real browser automation
3. Try multiple methods: local Chromium → Chrome CDP → Browserless API
4. Extract real product data even from protected sites

If a site fails or returns few results, I'll:
- Try alternative sites (suggest Zalando if ASOS fails)
- Adjust the search terms
- Use browser automation for stubborn sites
- Let you know what happened

### Step 3: Curate & Present

I'll combine all results and filter based on your criteria:

```
User: "Show me the best deals under £80"
→ I'll run:
   filter_products.sh --max-price 80 --sort-by discount
```

Then I'll present a summary:

> **Found 12 products across 2 sites:**
> 
> | Product | Price | Was | Discount | Site |
> |---------|-------|-----|----------|------|
> | Nike Air Zoom | £65 | £95 | 32% | Amazon |
> | Nike React | £72 | £110 | 35% | ASOS |
> | ... | ... | ... | ... | ... |

### Step 4: Your Approval

**I'll always ask before proceeding:**

> These 5 products look good for your page. Should I:
> - **[Proceed]** → Generate the page
> - **[Add more sites]** → Research additional retailers
> - **[Change filters]** → Adjust price range or minimum discount
> - **[Pick specific items]** → Let you choose from the full list
> - **[Manual edit]** → Open the data for you to edit

### Step 5: Generate & Deploy

Once you approve:

```
→ generate_page.sh --title "Your Title" --template deals
→ deploy.sh --dir ./site
```

I'll return the live URL: `https://your-page-123.netlify.app`

## Natural Language Patterns

### Product Research
| You Say | What I Do |
|---------|-----------|
| "Find [product] on [site]" | Research that specific site |
| "Check Amazon, ASOS, and John Lewis" | Research all three |
| "Wherever has the best deals" | Research 3-4 popular sites |
| "UK fashion retailers" | Suggest ASOS, John Lewis, Next, M&S |

### Filtering
| You Say | What I Do |
|---------|-----------|
| "Best deals" | Sort by highest discount |
| "Under £50" | Filter by max price |
| "Top rated" | Sort by rating, minimum 4 stars |
| "At least 30% off" | Filter by min discount |
| "Top 5" | Limit to 5 items |

### Design
| You Say | Template I Use |
|---------|----------------|
| "Deals page" / "Sale page" | `deals` - Grid of discount cards |
| "Compare" / "Side by side" | `comparison` - Comparison table |
| "Showcase" / "Featured" | `showcase` - Hero + featured products |
| "Simple" / "Clean" | `minimal` - Clean list |

### Deployment
| You Say | What Happens |
|---------|--------------|
| "Deploy it" | Deploy to Netlify with auto-generated name |
| "Deploy as [name]" | Deploy with specific site name |
| "Just save it" | Skip deployment, return local file path |
| "Show me first" | Open the HTML locally for preview |

## Example Conversations

### Example 1: Simple Deal Finder

**User:** "Create a page for summer dress deals"

**Agent:**
> I'll help you create a deals page for summer dresses. Let me research popular UK fashion sites.
> 
> Researching: ASOS, John Lewis, Next...
> 
> **Found 15 dresses:**
> - ASOS: 6 items (discounts 20-45%)
> - John Lewis: 5 items (discounts 15-35%)
> - Next: 4 items (discounts 10-30%)
>
> **Top 5 by discount:**
> 1. Floral Maxi Dress - £35 (was £65, 46% off) - ASOS
> 2. Linen Midi Dress - £28 (was £50, 44% off) - John Lewis
> ...
>
> Should I create the page with these 5, or would you like to adjust?

**User:** "Add a couple more and make it 7"

**Agent:**
> Done. Added 2 more - now have 7 dresses ranging from £25-45.
> 
> Generating your deals page... ✓
> Deploying to Netlify... ✓
> 
> **Your page is live:** https://summer-dresses-2025.netlify.app

---

### Example 2: Specific Requirements

**User:** "I need a tech comparison page for wireless headphones under £100, only items with 4+ stars. Check Amazon and Currys."

**Agent:**
> Got it. Researching wireless headphones under £100 with good ratings.
>
> Researching Amazon... ✓ Found 8 products
> Researching Currys... ✓ Found 6 products
>
> **Filtered (price ≤ £100, rating ≥ 4.0, sorted by rating):**
> 
> | Headphones | Price | Rating | Reviews | Site |
> |------------|-------|--------|---------|------|
> | Sony WH-CH720N | £89 | 4.6 | 2,340 | Amazon |
> | JBL Tune 760NC | £65 | 4.5 | 1,890 | Currys |
> | ... | ... | ... | ... | ... |
>
> These 6 meet your criteria. Create comparison page?

**User:** "Yes, but put Sony first"

**Agent:**
> Done - Sony is featured at the top.
>
> Generating comparison table layout... ✓
> Deploying... ✓
>
> **Live:** https://wireless-headphones-compare.netlify.app

---

### Example 3: Iterative Refinement

**User:** "Make a deals page for men's trainers"

**Agent:**
> Researching men's trainers across popular sites...
> 
> **Found 20 trainers:** [shows summary]
> 
> Here's my suggested selection of 6. Any adjustments?

**User:** "Remove the white ones, add something from Nike"

**Agent:**
> Removed 2 white trainers. Searching specifically for Nike...
> 
> Found: Nike Air Force 1 - £75 (was £95) - adding to selection.
> 
> **Updated list:** [shows new list]
> 
> Proceed?

**User:** "Perfect, deploy it as 'mens-trainers-march'"

**Agent:**
> Deploying as 'mens-trainers-march'... ✓
> 
> **Live:** https://mens-trainers-march.netlify.app

## Supported Sites

I can research these sites (availability may vary):

| Site | Category | Anti-Bot Level | Notes |
|------|----------|----------------|-------|
| Amazon UK | General | 🔴 High | Automatically uses browser automation |
| ASOS | Fashion | 🟡 Medium | May require browser fallback |
| John Lewis | Premium | 🟢 Low | Usually accessible directly |
| Currys | Electronics | 🟡 Medium | Browser fallback if needed |
| Argos | General | 🟢 Low | Usually accessible directly |
| Next | Fashion | 🟡 Medium | May require browser fallback |
| Marks & Spencer | Premium | 🟡 Medium | Browser fallback if needed |
| Zalando | Fashion | 🟡 Medium | May require browser fallback |

**Anti-Bot Legend:**
- 🟢 Low - Simple HTTP requests work
- 🟡 Medium - Sometimes requires browser automation
- 🔴 High - Always requires browser automation

### How Anti-Bot Protection Works

When you request products from a site like Amazon:

1. **First attempt:** Fast curl request (0.5s)
2. **If blocked:** Auto-detect CAPTCHA/JS requirements
3. **Fallback:** Use agent-browser skill
   - Try local Chromium (bundled)
   - Try Chrome CDP (if available)
   - Try Browserless API (cloud, always works)
4. **Result:** Real product data even from protected sites

This happens automatically - you don't need to do anything special. Just ask for the products you want!

## Tips for Best Results

1. **Be specific about products**
   - ❌ "Electronics" → Too broad
   - ✅ "Wireless earbuds under £50" → Focused

2. **Mention price ranges**
   - "Show me options between £30-60"
   - "Nothing over £100"

3. **Specify quantity**
   - "Just the top 3 best deals"
   - "I want variety - maybe 8-10 items"

4. **Tell me the purpose**
   - "For my blog's Black Friday post"
   - "Affiliate marketing page"
   - "Personal shopping list"

## Error Handling

If something goes wrong, I'll tell you clearly:

| Situation | What I'll Do |
|-----------|--------------|
| Site is down | "ASOS isn't responding. Try John Lewis instead?" |
| Site blocks bots | "Amazon requires browser automation - using fallback..." |
| No products found | "No results for 'XYZ'. Try different keywords?" |
| Filter too strict | "No items match 'under £10'. Raise the limit?" |
| Deploy fails | "Netlify error: [message]. Try different site name?" |

### Anti-Bot Troubleshooting

**Problem:** "Amazon is showing CAPTCHA"
- **Solution:** Already handled! I automatically switch to browser automation
- **Fallback chain:** Chromium → Chrome CDP → Browserless API
- **Result:** You still get the products

**Problem:** "All browser methods failed"
- **Solution:** I'll report the error and suggest alternatives
- **No fake data:** This skill NEVER returns simulated/mock data

**Problem:** "Agent-browser skill not found"
- **Solution:** Research will fail - agent-browser is REQUIRED for real data extraction
- **To enable:** Install agent-browser skill

## File Structure

```
marketing-page-creator/
├── SKILL.md                  # This file - natural language guide
├── REFACTOR_SUMMARY.md       # Before/after comparison
├── workflows/                # Proven reusable workflows
│   └── csv-to-page/          # CSV → HTML → Netlify workflow
│       ├── research.py       # Product extraction script
│       ├── generate_page.py  # HTML generator
│       ├── deploy.sh         # Netlify deploy script
│       └── README.md         # Workflow documentation
├── tools/                    # Tools I use (don't call directly)
│   ├── research_site.sh      # Research single site with anti-bot
│   ├── research_parallel.sh  # Research multiple sites in parallel
│   ├── fetch_product_page.sh # Fetch specific product URL
│   ├── filter_products.sh    # Filter and sort products
│   ├── generate_page.sh      # Generate HTML page
│   └── deploy.sh             # Deploy to Netlify
├── templates/                # HTML templates (internal)
├── examples/                 # Example outputs
└── references/               # Documentation
```

### 🌐 Browser Strategy for E-Commerce Sites

**For most e-commerce sites, ALWAYS use `mychrome` skill first to access Chrome via CDP.**

#### Recommended Browser Stack for E-Commerce:

```
Priority 1: MYCHROME (Chrome CDP) ⭐ RECOMMENDED FOR E-COMMERCE
- Uses real Chrome instance via Chrome DevTools Protocol
- Best anti-bot protection for Amazon, eBay, Shopify, etc.
- Requires: Chrome running with --remote-debugging-port=9222
- Start with: ~/start-chrome.sh on remote host

Priority 2: Agent-Browser (Chromium)  
- Uses bundled Chromium with stealth flags
- Good fallback if mychrome unavailable
- Automatic installation, no external dependencies

Priority 3: Browserless (Cloud API)
- Cloud-based browser automation
- Use when local browser fails
- Requires: BROWSERLESS_API_KEY environment variable

Priority 4: curl (HTTP requests)
- Fast but easily blocked by anti-bot
- Only works for simple sites without JS/CAPTCHA
- If fails → DO NOT use mock data, try browser methods above
```

#### Why mychrome for E-Commerce?

E-commerce sites (Amazon, eBay, Walmart, etc.) have sophisticated anti-bot detection:

| Detection Method | curl | Chromium | mychrome |
|-----------------|------|----------|----------|
| Headless detection | ❌ Blocked | ⚠️ Sometimes | ✅ Passes |
| Fingerprinting | ❌ Blocked | ⚠️ Sometimes | ✅ Passes |
| CAPTCHA triggers | ❌ Always | ⚠️ Often | ✅ Rarely |
| JavaScript requirements | ❌ Fails | ✅ Works | ✅ Works |
| Rate limiting | ❌ Fast | ⚠️ Medium | ✅ Stealth |

**Rule of thumb:**
- 🛍️ **E-commerce sites** → Use `mychrome` first
- 📰 **Simple blogs/news** → Can try curl
- 🔒 **Protected sites** → Use mychrome or Browserless

#### How to Use mychrome

```python
# Example: Using mychrome skill for Amazon research
from mychrome import ChromeDebugger

chrome = ChromeDebugger(host="spost", port=9222)
chrome.connect()

# Navigate and extract
data = chrome.navigate("https://amazon.com/s?k=laptops")
products = chrome.extract_products()
```

Or via CLI:
```bash
# Start Chrome with CDP on remote host
ssh spost "export DISPLAY=:99 && ~/start-chrome.sh"

# Then use mychrome skill to connect and scrape
```

---

### ⚠️ REAL DATA ONLY - NO EXCEPTIONS:
- **NEVER** use mock, simulated, or fake data under any circumstances
- **NEVER** create placeholder products or "example" data
- **NEVER** proceed with page generation if real data cannot be extracted
- If extraction fails → Report failure and STOP
- If partial data → Only use verified real data, discard fake entries
- **MUST** verify all data comes from actual website extraction

**Verification Checkpoints:**
1. Before generating page: Confirm all products have real URLs from target site
2. Before generating page: Verify images are from actual product pages
3. Before generating page: Confirm prices were extracted (not invented)
4. Before deploying: Review CSV to ensure no placeholder data exists

**Requirements:**
- agent-browser skill is **optional** but recommended
- **Without it**: Uses curl only - if curl fails, report failure (NO mock data)
- **With it**: Full anti-bot protection with real browser automation
- **Fallback chain**: curl → local Chromium → Chrome CDP → Browserless API
- **If all methods fail**: STOP and report error to user

## 🚨 REAL DATA MANDATORY - NO FAKE DATA ALLOWED

**THIS SKILL NEVER USES MOCK, SIMULATED, OR FAKE DATA.**

Every product displayed must be:
- ✅ Extracted from a real website via browser automation
- ✅ Have a valid URL pointing to actual product page
- ✅ Have real image URLs from the source site
- ✅ Have prices that were scraped (not invented)

**If you cannot extract real data:**
- STOP and report the failure
- DO NOT create placeholder products
- DO NOT use "example" data
- DO NOT proceed with page generation

---

## Proven Workflow: CSV → Product Page → Netlify

This is a battle-tested workflow for creating product list pages from e-commerce sites:

### Phase 1: Research & Extract to CSV

```python
# Example: Amazon UK Product Research
import asyncio
import csv
from playwright.async_api import async_playwright
from datetime import datetime

async def research_products():
    """
    Extract product data and save to CSV
    Columns: title, price, original_price, rating, reviews, link, image, category
    """
    products = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate to target site
        await page.goto("https://www.amazon.co.uk/s?k=deals")
        await page.wait_for_selector('[data-component-type="s-search-result"]')
        
        # Extract product data
        items = await page.query_selector_all('[data-component-type="s-search-result"]')
        
        for item in items:
            product = {
                'title': await extract_title(item),
                'price': await extract_price(item),
                'original_price': await extract_original_price(item),
                'rating': await extract_rating(item),
                'reviews': await extract_reviews(item),
                'link': await extract_link(item),
                'image': await extract_image(item),
                'category': 'electronics'  # or detected category
            }
            products.append(product)
        
        await browser.close()
    
    # Save to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"amazon_deals_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'title', 'price', 'original_price', 'rating', 
            'reviews', 'link', 'image', 'category'
        ])
        writer.writeheader()
        writer.writerows(products)
    
    return filename, products
```

**Key Points:**
- Always extract: `title`, `price`, `original_price` (for discounts), `rating`, `reviews`, `link`, `image`, `category`
- Handle missing data gracefully (null/empty values)
- Use stealth techniques for anti-bot sites (Amazon, ASOS, etc.)
- Save with timestamp to avoid overwriting

### 🔍 Phase 1.5: VERIFY DATA BEFORE PROCEEDING

**MANDATORY - Check before continuing:**

```
□ All products have valid URLs (not placeholder.com)
□ All images are from actual source domain (not placeholder images)
□ Prices were extracted from page (not invented like "$99.99")
□ At least 50% of products have real data extracted
□ NO products have titles like "Example Product" or "Sample Item"
□ CSV file size > 1KB (indicates real data, not empty template)
```

**If verification fails:**
- STOP - Do not proceed to Phase 2
- Try different search terms
- Try different site
- Report extraction failure to user

**Verification Command:**
```bash
# Check CSV has real data
head -5 products.csv
# Should show actual product titles and amazon.co.uk URLs
# NOT example.com or placeholder text
```

### Phase 2: Generate HTML Product Page

```html
<!-- Modern Product Grid Template -->
<!DOCTYPE html>
<html>
<head>
    <title>Best Deals</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Key CSS Features */
        - CSS Grid for responsive product cards
        - Gradient backgrounds
        - Hover animations (transform: translateY, box-shadow)
        - Category filter buttons
        - Star rating display
        - Price styling (current + original/strikethrough)
    </style>
</head>
<body>
    <!-- Structure -->
    - Header with title and description
    - Stats bar (product count, categories, avg rating)
    - Filter buttons (All, Electronics, Fashion, etc.)
    - Product grid with cards
    - Footer with timestamp
    
    <!-- JavaScript -->
    - Product data embedded as JSON array
    - Filter function to show/hide by category
    - Dynamic star generation for ratings
    - Lazy loading for images
</body>
</html>
```

**Design Principles:**
- Clean, modern UI with purple/blue gradient theme
- Card-based layout with hover effects
- Category filtering for better UX
- Responsive grid (1 col mobile, 3 col desktop)
- Direct links to product pages

### Phase 3: Deploy to Netlify

```bash
# 1. Create site directory
mkdir -p site/
cp index.html site/

# 2. Deploy to Netlify
cd site/
netlify deploy --prod --dir=. --json

# Output includes:
# - site_id
# - deploy_url (preview)
# - url (production)
```

**Deployment Options:**
- **New site:** `netlify deploy --dir=.` (creates random URL)
- **Named site:** `netlify sites:create --name my-deals-page` then deploy
- **Existing site:** `netlify deploy --prod --site=SITE_ID`

### Complete Example Session

```
User: "Create a deals page for Amazon UK electronics"

→ Phase 1: Research
  - Scrape Amazon UK electronics category
  - Extract 20+ products with full details
  - Save to: amazon_uk_deals_20260324_212800.csv

→ Phase 2: Generate Page
  - Read CSV data
  - Generate responsive HTML with filtering
  - Include: product cards, ratings, prices, images
  - Output: site/index.html

→ Phase 3: Deploy
  - Deploy to Netlify
  - Result: https://clawpilot-landing-1773064086.netlify.app
```

### File Structure

```
marketing-page-creator/
├── SKILL.md                  # This documentation
├── workflows/                # Proven workflow templates
│   ├── csv-to-page/         # CSV → HTML → Netlify
│   │   ├── research.py      # Product research script
│   │   ├── template.html    # HTML template
│   │   └── README.md        # Workflow guide
│   └── single-page/         # Direct page creation
├── tools/                    # CLI tools
├── templates/                # HTML templates
└── examples/                 # Example outputs
```

## Version

2.3.0 - Added CSV→Page→Netlify Proven Workflow

### Changelog

**2.4.0** (2025-03-25)
- **CRITICAL:** Enforced REAL DATA ONLY policy across all workflows
- Added mandatory data verification checkpoints before page generation
- Scripts now FAIL if fake/mock data is detected (non-negotiable)
- Updated all documentation with strict warnings against fake data

**2.3.0** (2025-03-24)
- Added proven workflow: Research → CSV → Product Page → Netlify
- Documented anti-bot techniques for Amazon UK and similar sites
- Added responsive product grid template with filtering
- Included complete code examples for all three phases

**2.2.0** (2025-03-24)
- **BREAKING:** Removed all mock/simulated data generation
- Research tools now ONLY return real extracted product data
- If real data cannot be extracted, tools return errors
- Improved HTML extraction with site-specific patterns
- Added Python-based extraction for better accuracy

**2.1.0** (2025-03-24)
- Added automatic anti-bot handling via agent-browser skill
- Added parallel research tool for faster multi-site research
- Added product page fetcher for specific URLs
- Updated all tools to gracefully handle blocked sites

**2.0.0** (2025-03-24)
- Complete rewrite to natural language driven approach
- Replaced complex orchestration scripts with simple tools
- LLM now orchestrates workflow instead of bash scripts
- Added user confirmation checkpoints
- Simplified tool interface
