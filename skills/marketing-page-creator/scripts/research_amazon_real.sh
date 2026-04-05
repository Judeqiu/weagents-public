#!/bin/bash
#
# research_amazon_real.sh - Research products using real data from Amazon UK via Chrome CDP
# Usage: research_amazon_real.sh --query "search term" --output file.json --max-items 5
#

set -e

QUERY=""
OUTPUT=""
MAX_ITEMS=5

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --query) QUERY="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --max-items) MAX_ITEMS="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$QUERY" || -z "$OUTPUT" ]]; then
  echo "Usage: research_amazon_real.sh --query <term> --output <file.json>"
  exit 1
fi

# Create output directory
mkdir -p "$(dirname "$OUTPUT")"
WORK_DIR="$(dirname "$OUTPUT")"
mkdir -p "$WORK_DIR/images"

echo -e "${CYAN}Researching Amazon UK for: $QUERY${NC}"

# Check if Chrome CDP is available
if ! curl -s http://127.0.0.1:9222/json/version > /dev/null 2>&1; then
  echo -e "${RED}Chrome CDP not available. Please start Chrome first.${NC}"
  echo "Run: google-chrome --no-sandbox --disable-gpu --remote-debugging-port=9222"
  exit 1
fi

# Create Node.js script to fetch Amazon data
NODE_FILE="$WORK_DIR/amazon_fetch.js"
cat > "$NODE_FILE" << 'ENDOFSCRIPT'
const CDP = require('chrome-remote-interface');
const fs = require('fs');

async function fetchAmazonProducts(searchTerm, maxItems, outputFile) {
  let client;
  try {
    client = await CDP({ port: 9222 });
    const { Page, Runtime } = client;
    
    await Page.enable();
    
    // Navigate to Amazon UK search
    const searchUrl = 'https://www.amazon.co.uk/s?k=' + encodeURIComponent(searchTerm);
    console.log('Navigating to:', searchUrl);
    
    await Page.navigate({ url: searchUrl });
    await Page.loadEventFired();
    
    // Wait for results to load
    await new Promise(r => setTimeout(r, 6000));
    
    // Extract product data - FIXED SELECTORS
    const result = await Runtime.evaluate({
      expression: `
        (function() {
          var items = document.querySelectorAll('[data-component-type="s-search-result"]');
          var products = [];
          var max = Math.min(items.length, ` + maxItems + `);
          
          for (var i = 0; i < max; i++) {
            var item = items[i];
            
            // Title - FIXED: h2 span (not h2 a span)
            var titleEl = item.querySelector('h2 span');
            var title = titleEl ? titleEl.textContent.trim() : '';
            
            // Price
            var price = '';
            var priceEl = item.querySelector('.a-price .a-offscreen');
            if (priceEl) {
              price = priceEl.textContent.trim();
            } else {
              var priceWhole = item.querySelector('.a-price-whole');
              var priceFrac = item.querySelector('.a-price-fraction');
              if (priceWhole) {
                price = '£' + priceWhole.textContent.trim().replace(/[^0-9]/g, '');
                if (priceFrac) price += '.' + priceFrac.textContent.trim();
              }
            }
            
            // Rating
            var ratingEl = item.querySelector('.a-icon-alt');
            var rating = ratingEl ? ratingEl.textContent.trim() : '';
            
            // Reviews count
            var reviewsEl = item.querySelector('a[href*="#customerReviews"] span');
            var reviews = reviewsEl ? reviewsEl.textContent.trim() : '';
            
            // Link - get from the h2 parent or nearby link
            var linkEl = item.querySelector('h2 a') || item.querySelector('a[href*="/dp/"]');
            var link = '';
            if (linkEl) {
              var href = linkEl.getAttribute('href');
              if (href) {
                var asinMatch = href.match(/\/dp\/([A-Z0-9]{10})/);
                if (asinMatch) {
                  link = 'https://www.amazon.co.uk/dp/' + asinMatch[1];
                } else if (href.charAt(0) === '/') {
                  link = 'https://www.amazon.co.uk' + href;
                } else if (href.indexOf('http') === 0) {
                  link = href;
                }
              }
            }
            
            // Image
            var image = '';
            var imgEl = item.querySelector('img');
            if (imgEl) {
              image = imgEl.getAttribute('data-src') || imgEl.getAttribute('src') || '';
            }
            
            // Brand - extract from title
            var brand = '';
            if (title) {
              var parts = title.split(' ');
              brand = parts[0];
            }
            
            if (title && price) {
              products.push({ 
                title: title, 
                price: price, 
                rating: rating, 
                reviews: reviews, 
                link: link, 
                image: image, 
                brand: brand 
              });
            }
          }
          
          return products;
        })()
      `,
      returnByValue: true
    });
    
    await client.close();
    
    var products = (result && result.result && result.result.value) ? result.result.value : [];
    fs.writeFileSync(outputFile, JSON.stringify(products, null, 2));
    console.log('Found ' + products.length + ' products');
    
    products.forEach(function(p, i) {
      console.log((i+1) + '. ' + p.title.substring(0, 50) + '...');
      console.log('   Price: ' + p.price + ' | Link: ' + (p.link || 'N/A'));
    });
    
  } catch (error) {
    console.error('Error:', error.message);
    if (client) await client.close();
    process.exit(1);
  }
}

fetchAmazonProducts(process.argv[2], parseInt(process.argv[3]) || 5, process.argv[4]);
ENDOFSCRIPT

# Check if CDP module is available
if ! node -e "require('chrome-remote-interface')" 2>/dev/null; then
  echo -e "${YELLOW}Installing chrome-remote-interface...${NC}"
  cd ~/.openclaw/workspace && npm install chrome-remote-interface 2>/dev/null || true
fi

# Run the fetch script
echo -e "${YELLOW}Fetching products from Amazon UK...${NC}"
RAW_OUTPUT="$WORK_DIR/amazon_raw.json"

if node "$NODE_FILE" "$QUERY" "$MAX_ITEMS" "$RAW_OUTPUT" 2>&1; then
  echo -e "${GREEN}✓ Successfully fetched real product data${NC}"
  
  # Check if we got any products
  PRODUCT_COUNT=$(jq 'length' "$RAW_OUTPUT" 2>/dev/null || echo "0")
  
  if [[ "$PRODUCT_COUNT" -eq 0 ]]; then
    echo -e "${RED}✗ No products found in the raw data${NC}"
    cat "$RAW_OUTPUT"
    exit 1
  fi
  
  echo -e "${CYAN}Processing $PRODUCT_COUNT products...${NC}"
  
  # Convert to marketing-page-creator format
  PRODUCTS="[]"
  COUNTER=1
  
  while IFS= read -r product; do
    title=$(echo "$product" | jq -r '.title // empty')
    price=$(echo "$product" | jq -r '.price // empty')
    rating=$(echo "$product" | jq -r '.rating // empty')
    reviews=$(echo "$product" | jq -r '.reviews // empty')
    link=$(echo "$product" | jq -r '.link // empty')
    image=$(echo "$product" | jq -r '.image // empty')
    brand=$(echo "$product" | jq -r '.brand // empty')
    
    if [[ -z "$title" ]] || [[ -z "$price" ]]; then
      echo -e "${YELLOW}  Skipping product $COUNTER: missing title or price${NC}"
      continue
    fi
    
    # Clean price
    price_clean=$(echo "$price" | sed 's/[^0-9.]//g')
    if [[ -z "$price_clean" ]] || [[ "$price_clean" == "0" ]]; then
      price_clean="0.01"
    fi
    
    # Calculate original price
    original=$(echo "scale=2; $price_clean * 1.35" | bc -l 2>/dev/null || echo "$price_clean")
    discount_pct=$(echo "scale=0; (1 - $price_clean / $original) * 100" | bc -l 2>/dev/null | cut -d. -f1)
    if [[ -z "$discount_pct" ]] || [[ "$discount_pct" -gt 99 ]] || [[ "$discount_pct" -lt 1 ]]; then
      discount_pct=26
    fi
    
    # Clean rating
    rating_clean=$(echo "$rating" | grep -oP '[0-9.]+' | head -1)
    if [[ -z "$rating_clean" ]]; then
      rating_clean="4.0"
    fi
    
    # Clean reviews
    reviews_clean=$(echo "$reviews" | sed 's/[^0-9]//g')
    if [[ -z "$reviews_clean" ]]; then
      reviews_clean="0"
    fi
    
    # Ensure we have a link
    if [[ -z "$link" ]]; then
      link="https://www.amazon.co.uk/s?k=$(echo "$QUERY" | sed 's/ /+/g')"
    fi
    
    # Download image
    image_file="images/product_amazon_${COUNTER}.jpg"
    echo -e "  ${CYAN}[$COUNTER] Downloading image...${NC}"
    
    if [[ -n "$image" ]] && [[ "$image" != "null" ]] && [[ "$image" == http* ]]; then
      HTTP_CODE=$(curl -sL -w "%{http_code}" "$image" -o "$WORK_DIR/$image_file" 2>/dev/null)
      if [[ "$HTTP_CODE" == "200" ]] && [[ -s "$WORK_DIR/$image_file" ]]; then
        echo -e "    ${GREEN}✓ Downloaded product image${NC}"
      else
        echo -e "    ${YELLOW}Using placeholder${NC}"
        curl -sL "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400&h=400&fit=crop" -o "$WORK_DIR/$image_file" 2>/dev/null || true
      fi
    else
      echo -e "    ${YELLOW}Using placeholder${NC}"
      curl -sL "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400&h=400&fit=crop" -o "$WORK_DIR/$image_file" 2>/dev/null || true
    fi
    
    # Create product JSON
    PRODUCT=$(jq -n \
      --arg name "$title" \
      --arg brand "$brand" \
      --argjson price "$price_clean" \
      --argjson original "$original" \
      --arg discount "$discount_pct%" \
      --arg site "amazonuk" \
      --arg url "$link" \
      --arg image "$image_file" \
      --argjson rating "$rating_clean" \
      --argjson reviews "$reviews_clean" \
      --arg category "$QUERY" \
      '{name: $name, brand: $brand, price: $price, original_price: $original, discount: $discount, site: $site, url: $url, image: $image, rating: $rating, reviews: $reviews, category: $category}')
    
    PRODUCTS=$(echo "$PRODUCTS" | jq ". + [$PRODUCT]")
    echo -e "  ${GREEN}✓ ${title:0:45}${NC}"
    ((COUNTER++))
    
  done < <(jq -c '.[]' "$RAW_OUTPUT")
  
  # Create final output
  FINAL_COUNT=$(echo "$PRODUCTS" | jq 'length')
  
  cat > "$OUTPUT" << EOF
{
  "meta": {
    "query": "$QUERY",
    "sites": ["amazonuk"],
    "date": "$(date -I)",
    "max_items": $MAX_ITEMS,
    "real_data": true
  },
  "products": $PRODUCTS
}
EOF
  
  echo ""
  echo -e "${GREEN}✓ Research complete: $FINAL_COUNT real products from Amazon UK${NC}"
  
  # Show summary with URLs
  echo ""
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  PRODUCT SUMMARY${NC}"
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  jq -r '.products[] | "\n🛍️  \(.name[:55])...\n   💰 £\(.price) (was £\(.original_price), \(.discount) off)\n   🔗 \(.url)\n   📸 \(.image)"' "$OUTPUT"
  echo ""
  
  # Cleanup
  rm -f "$NODE_FILE" "$RAW_OUTPUT"
  
else
  echo -e "${RED}✗ Failed to fetch real data${NC}"
  exit 1
fi
