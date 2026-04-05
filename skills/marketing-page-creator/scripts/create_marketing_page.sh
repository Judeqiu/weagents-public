#!/bin/bash
#
# create_marketing_page.sh - One-command marketing page creation with user confirmation
# Usage: create_marketing_page.sh --name "site-name" --topic "Topic" --sites "site1,site2" --deploy
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
SITE_NAME=""
TOPIC=""
SITES=""
TEMPLATE="deals"
ITEMS_PER_SITE=5
DEPLOY=false
PRIMARY_COLOR="#e94560"
WORK_DIR=""
SKIP_CONFIRMATION=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --name)
      SITE_NAME="$2"
      shift 2
      ;;
    --topic)
      TOPIC="$2"
      shift 2
      ;;
    --sites)
      SITES="$2"
      shift 2
      ;;
    --template)
      TEMPLATE="$2"
      shift 2
      ;;
    --items)
      ITEMS_PER_SITE="$2"
      shift 2
      ;;
    --color)
      PRIMARY_COLOR="$2"
      shift 2
      ;;
    --deploy)
      DEPLOY=true
      shift
      ;;
    --yes)
      SKIP_CONFIRMATION=true
      shift
      ;;
    --help)
      echo "Usage: create_marketing_page.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --name <name>        Site name (required)"
      echo "  --topic <topic>      Page topic/title (required)"
      echo "  --sites <sites>      Comma-separated sites (required)"
      echo "  --template <tpl>     Template: deals|comparison|showcase|review|minimal"
      echo "  --items <n>          Items per site (default: 5)"
      echo "  --color <hex>        Primary color (default: #e94560)"
      echo "  --deploy             Deploy to Netlify after creation"
      echo "  --yes                Skip user confirmation (auto-approve)"
      echo "  --help               Show this help"
      echo ""
      echo "Example:"
      echo "  create_marketing_page.sh --name \"mens-deals\" --topic \"Men's Clothing Deals\" --sites \"amazon,asos\" --deploy"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [[ -z "$SITE_NAME" || -z "$TOPIC" || -z "$SITES" ]]; then
  echo -e "${RED}Error: --name, --topic, and --sites are required${NC}"
  echo "Run with --help for usage information"
  exit 1
fi

# Create working directory
WORK_DIR="/tmp/marketing-page-${SITE_NAME}-$(date +%s)"
mkdir -p "$WORK_DIR"/{data,images,site}

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Marketing Page Creator - Full Workflow             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "  Site Name: $SITE_NAME"
echo "  Topic: $TOPIC"
echo "  Sites: $SITES"
echo "  Template: $TEMPLATE"
echo "  Items per site: $ITEMS_PER_SITE"
echo "  Deploy: $DEPLOY"
echo ""

# ============================================
# PHASE 1: RESEARCH
# ============================================
echo -e "${GREEN}▶ Phase 1: Researching products...${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call research script
if [[ -f "$SCRIPT_DIR/research_products.sh" ]]; then
  "$SCRIPT_DIR/research_products.sh" \
    --query "$TOPIC" \
    --sites "$SITES" \
    --max-items "$ITEMS_PER_SITE" \
    --include-images \
    --output "$WORK_DIR/data/products.json"
else
  # Fallback: Create sample data for demonstration
  echo -e "${YELLOW}  Research script not found, creating sample data...${NC}"
  cat > "$WORK_DIR/data/products.json" << EOF
{
  "meta": {
    "query": "$TOPIC",
    "sites": $(echo "$SITES" | tr ',' '\n' | jq -R . | jq -s .),
    "date": "$(date -I)",
    "template": "$TEMPLATE"
  },
  "products": [
    {
      "name": "Sample Product 1",
      "brand": "Brand A",
      "price": 49.99,
      "original_price": 79.99,
      "discount": "38%",
      "site": "amazon",
      "url": "https://www.amazon.co.uk",
      "image": "images/product1.jpg",
      "rating": 4.5,
      "reviews": 1200,
      "category": "Category A"
    },
    {
      "name": "Sample Product 2", 
      "brand": "Brand B",
      "price": 39.99,
      "original_price": 59.99,
      "discount": "33%",
      "site": "asos",
      "url": "https://www.asos.com",
      "image": "images/product2.jpg",
      "rating": 4.3,
      "reviews": 850,
      "category": "Category B"
    }
  ]
}
EOF
fi

if [[ ! -f "$WORK_DIR/data/products.json" ]]; then
  echo -e "${RED}✗ Research failed - no data generated${NC}"
  exit 1
fi

PRODUCT_COUNT=$(jq '.products | length' "$WORK_DIR/data/products.json")
echo -e "${GREEN}✓ Research complete: $PRODUCT_COUNT products found${NC}"
echo ""

# ============================================
# PHASE 2: USER CONFIRMATION
# ============================================
echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           📋 REVIEW EXTRACTED PRODUCTS                 ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Display products in a formatted table
echo -e "${YELLOW}Found $PRODUCT_COUNT products:${NC}"
echo ""
printf "${CYAN}%-4s %-30s %-15s %-10s %-12s %-10s${NC}\n" "#" "Product Name" "Brand" "Price" "Discount" "Site"
printf "${CYAN}%s${NC}\n" "─────────────────────────────────────────────────────────────────────────────────────────"

COUNTER=1
while IFS= read -r product; do
  name=$(echo "$product" | jq -r '.name')
  brand=$(echo "$product" | jq -r '.brand')
  price=$(echo "$product" | jq -r '.price')
  discount=$(echo "$product" | jq -r '.discount')
  site=$(echo "$product" | jq -r '.site')
  
  # Truncate long names
  if [[ ${#name} -gt 28 ]]; then
    name="${name:0:25}..."
  fi
  if [[ ${#brand} -gt 13 ]]; then
    brand="${brand:0:10}..."
  fi
  
  printf "%-4d %-30s %-15s £%-9.2f %-12s %-10s\n" "$COUNTER" "$name" "$brand" "$price" "$discount" "$site"
  ((COUNTER++))
done < <(jq -c '.products[]' "$WORK_DIR/data/products.json")

echo ""
printf "${CYAN}%s${NC}\n" "─────────────────────────────────────────────────────────────────────────────────────────"
echo ""

# Save product data path for external review
REVIEW_FILE="$WORK_DIR/data/products_review.txt"
echo "Marketing Page Product Review" > "$REVIEW_FILE"
echo "=============================" >> "$REVIEW_FILE"
echo "Topic: $TOPIC" >> "$REVIEW_FILE"
echo "Sites: $SITES" >> "$REVIEW_FILE"
echo "Total Products: $PRODUCT_COUNT" >> "$REVIEW_FILE"
echo "" >> "$REVIEW_FILE"
echo "Products:" >> "$REVIEW_FILE"
echo "--------" >> "$REVIEW_FILE"
jq -r '.products[] | "\nName: \(.name)\nBrand: \(.brand)\nPrice: £\(.price) (was £\(.original_price))\nDiscount: \(.discount)\nSite: \(.site)\nURL: \(.url)\nRating: \(.rating) (\(.reviews) reviews)"' "$WORK_DIR/data/products.json" >> "$REVIEW_FILE"

echo -e "${YELLOW}📄 Full product details saved to:${NC} $REVIEW_FILE"
echo ""

# User confirmation
if [[ "$SKIP_CONFIRMATION" == false ]]; then
  echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║              ⚠️  USER CONFIRMATION REQUIRED              ║${NC}"
  echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo -e "${YELLOW}Please review the products above.${NC}"
  echo ""
  echo -e "Options:"
  echo -e "  ${GREEN}[Y]${NC} - Yes, proceed to create the marketing page"
  echo -e "  ${RED}[N]${NC} - No, cancel and exit"
  echo -e "  ${YELLOW}[E]${NC} - Edit the product data (opens JSON file)"
  echo ""
  
  while true; do
    read -p "Do you want to proceed with these products? [Y/N/E]: " -n 1 -r
    echo ""
    case $REPLY in
      [Yy]*)
        echo -e "${GREEN}✓ User confirmed. Proceeding to page generation...${NC}"
        echo ""
        break
        ;;
      [Nn]*)
        echo -e "${RED}✗ Cancelled by user. Exiting...${NC}"
        echo ""
        echo -e "${YELLOW}Working directory preserved at:${NC} $WORK_DIR"
        exit 0
        ;;
      [Ee]*)
        echo -e "${YELLOW}Opening product data for editing...${NC}"
        echo "Edit file: $WORK_DIR/data/products.json"
        echo ""
        # Try to open with common editors
        if command -v nano &> /dev/null; then
          nano "$WORK_DIR/data/products.json"
        elif command -v vim &> /dev/null; then
          vim "$WORK_DIR/data/products.json"
        elif command -v vi &> /dev/null; then
          vi "$WORK_DIR/data/products.json"
        else
          echo -e "${YELLOW}No editor found. Please manually edit:${NC}"
          echo "$WORK_DIR/data/products.json"
          read -p "Press Enter when done editing..."
        fi
        
        # Reload product count after editing
        PRODUCT_COUNT=$(jq '.products | length' "$WORK_DIR/data/products.json")
        echo -e "${GREEN}✓ Product data updated. $PRODUCT_COUNT products remaining.${NC}"
        echo ""
        
        # Show updated summary
        echo -e "${YELLOW}Updated product list:${NC}"
        jq -r '.products[] | "  • \(.name) - £\(.price) (\(.site))"' "$WORK_DIR/data/products.json"
        echo ""
        
        # Ask again for confirmation
        continue
        ;;
      *)
        echo -e "${RED}Invalid option. Please enter Y, N, or E.${NC}"
        ;;
    esac
  done
else
  echo -e "${YELLOW}⚡ Skipping confirmation (--yes flag used)${NC}"
  echo ""
fi

# ============================================
# PHASE 3: GENERATE PAGE
# ============================================
echo -e "${GREEN}▶ Phase 3: Generating landing page...${NC}"

if [[ -f "$SCRIPT_DIR/generate_page.sh" ]]; then
  "$SCRIPT_DIR/generate_page.sh" \
    --input "$WORK_DIR/data/products.json" \
    --template "$TEMPLATE" \
    --title "$TOPIC" \
    --output "$WORK_DIR/site/index.html" \
    --primary-color "$PRIMARY_COLOR"
else
  # Fallback: Generate basic HTML
  echo -e "${YELLOW}  Generate script not found, creating basic page...${NC}"
  
  # Read products and generate HTML
  cat > "$WORK_DIR/site/index.html" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | Best Deals</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: {{PRIMARY_COLOR}}; --secondary: #16213e; --accent: #e94560; --gold: #f4d03f; --success: #27ae60; --text: #2c3e50; --text-light: #64748b; --bg: #f8fafc; --card-bg: #ffffff; --border: #e2e8f0; --shadow: 0 4px 6px -1px rgba(0,0,0,0.1); --shadow-lg: 0 20px 25px -5px rgba(0,0,0,0.1); }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
        header { background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); color: white; padding: 3rem 1rem; text-align: center; }
        .header-content { max-width: 800px; margin: 0 auto; }
        .badge { display: inline-block; background: var(--accent); color: white; padding: 0.5rem 1.5rem; border-radius: 50px; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin-bottom: 1.5rem; }
        h1 { font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; }
        .subtitle { font-size: 1.25rem; opacity: 0.9; margin-bottom: 2rem; }
        main { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
        .product-card { background: var(--card-bg); border-radius: 16px; overflow: hidden; box-shadow: var(--shadow); transition: all 0.3s; position: relative; }
        .product-card:hover { transform: translateY(-8px); box-shadow: var(--shadow-lg); }
        .discount-badge { position: absolute; top: 1rem; left: 1rem; background: linear-gradient(135deg, var(--accent), #d63d56); color: white; padding: 0.5rem 1rem; border-radius: 50px; font-weight: 800; font-size: 0.875rem; z-index: 10; }
        .product-image { height: 220px; background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); display: flex; align-items: center; justify-content: center; overflow: hidden; }
        .product-image img { width: 100%; height: 100%; object-fit: cover; }
        .product-info { padding: 1.5rem; }
        .brand { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--accent); margin-bottom: 0.5rem; }
        .product-name { font-size: 1.125rem; font-weight: 700; color: var(--primary); margin-bottom: 0.5rem; }
        .category { font-size: 0.875rem; color: var(--text-light); margin-bottom: 1rem; }
        .price-row { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
        .current-price { font-size: 1.5rem; font-weight: 800; color: var(--success); }
        .original-price { font-size: 1rem; color: var(--text-light); text-decoration: line-through; }
        .buy-btn { display: block; width: 100%; padding: 1rem; background: linear-gradient(135deg, var(--accent), #d63d56); color: white; text-align: center; text-decoration: none; border-radius: 12px; font-weight: 700; }
        footer { background: var(--primary); color: white; padding: 2rem; text-align: center; margin-top: 4rem; }
        @media (max-width: 768px) { h1 { font-size: 1.75rem; } .product-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <span class="badge">🔥 Limited Time Offers</span>
            <h1>{{TITLE}}</h1>
            <p class="subtitle">Best deals curated for you</p>
        </div>
    </header>
    <main>
        <div class="product-grid">
            {{PRODUCT_CARDS}}
        </div>
    </main>
    <footer>
        <p>&copy; {{YEAR}} {{TITLE}}. All rights reserved.</p>
    </footer>
</body>
</html>
HTMLEOF

  # Replace placeholders
  sed -i "s/{{TITLE}}/$TOPIC/g" "$WORK_DIR/site/index.html"
  sed -i "s/{{PRIMARY_COLOR}}/$PRIMARY_COLOR/g" "$WORK_DIR/site/index.html"
  sed -i "s/{{YEAR}}/$(date +%Y)/g" "$WORK_DIR/site/index.html"
  
  # Generate product cards from JSON
  PRODUCT_CARDS=""
  while IFS= read -r product; do
    name=$(echo "$product" | jq -r '.name')
    brand=$(echo "$product" | jq -r '.brand')
    price=$(echo "$product" | jq -r '.price')
    original=$(echo "$product" | jq -r '.original_price')
    discount=$(echo "$product" | jq -r '.discount')
    url=$(echo "$product" | jq -r '.url')
    image=$(echo "$product" | jq -r '.image')
    category=$(echo "$product" | jq -r '.category // "General"')
    
    CARD="<article class=\"product-card\">
                    <span class=\"discount-badge\">-$discount</span>
                    <div class=\"product-image\"><img src=\"$image\" alt=\"$name\"></div>
                    <div class=\"product-info\">
                        <div class=\"brand\">$brand</div>
                        <h3 class=\"product-name\">$name</h3>
                        <div class=\"category\">$category</div>
                        <div class=\"price-row\"><span class=\"current-price\">£$price</span><span class=\"original-price\">£$original</span></div>
                        <a href=\"$url\" class=\"buy-btn\" target=\"_blank\">View Deal</a>
                    </div>
                </article>"
    PRODUCT_CARDS="$PRODUCT_CARDS$CARD"
  done < <(jq -c '.products[]' "$WORK_DIR/data/products.json")
  
  # Replace product cards placeholder
  # Use a different delimiter for sed to avoid issues with HTML
  printf '%s\n' "$PRODUCT_CARDS" > /tmp/product_cards.txt
  sed -i '/{{PRODUCT_CARDS}}/r /tmp/product_cards.txt' "$WORK_DIR/site/index.html"
  sed -i 's/{{PRODUCT_CARDS}}//g' "$WORK_DIR/site/index.html"
fi

# Copy images to site directory
if [[ -d "$WORK_DIR/data/images" ]]; then
  cp -r "$WORK_DIR/data/images/"* "$WORK_DIR/site/images/" 2>/dev/null || true
fi

echo -e "${GREEN}✓ Page generated: $WORK_DIR/site/index.html${NC}"
echo ""

# ============================================
# PHASE 4: DEPLOY (Optional)
# ============================================
if [[ "$DEPLOY" == true ]]; then
  echo -e "${GREEN}▶ Phase 4: Deploying to Netlify...${NC}"
  
  if [[ -f "$SCRIPT_DIR/deploy_to_netlify.sh" ]]; then
    DEPLOY_OUTPUT=$("$SCRIPT_DIR/deploy_to_netlify.sh" --dir "$WORK_DIR/site" --site-name "$SITE_NAME" --prod 2>&1)
    DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -oP 'https://[^\s]+\.netlify\.app' | head -1)
  else
    # Fallback: Direct netlify deploy
    cd "$WORK_DIR/site"
    DEPLOY_OUTPUT=$(netlify deploy --prod --dir=. 2>&1)
    DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -oP 'https://[^\s]+\.netlify\.app' | head -1)
  fi
  
  if [[ -n "$DEPLOY_URL" ]]; then
    echo -e "${GREEN}✓ Deployment successful!${NC}"
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  🚀 Your marketing page is live!                       ║${NC}"
    echo -e "${GREEN}║                                                        ║${NC}"
    echo -e "${GREEN}║  $DEPLOY_URL${NC}"
    echo -e "${GREEN}║                                                        ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
  else
    echo -e "${RED}✗ Deployment failed${NC}"
    echo "$DEPLOY_OUTPUT"
    exit 1
  fi
else
  echo -e "${YELLOW}▶ Skipping deployment (use --deploy to deploy)${NC}"
  echo ""
  echo -e "${BLUE}Files created in: $WORK_DIR/${NC}"
  echo "  - Data: $WORK_DIR/data/products.json"
  echo "  - Site: $WORK_DIR/site/index.html"
  echo "  - Images: $WORK_DIR/images/"
fi

echo ""
echo -e "${BLUE}Workflow complete!${NC}"
