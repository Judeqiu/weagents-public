#!/bin/bash
#
# generate_page.sh - Generate HTML page from product data
# Usage: cat products.json | generate_page.sh --title "Page Title" --template deals
# Input: JSON array of products from stdin
# Output: Path to generated HTML file

set -e

TITLE="Marketing Page"
TEMPLATE="deals"
OUTPUT_DIR=""
PRIMARY_COLOR="#e94560"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --title) TITLE="$2"; shift 2 ;;
    --template) TEMPLATE="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --primary-color) PRIMARY_COLOR="$2"; shift 2 ;;
    *) echo "Error: Unknown option $1" >&2; exit 1 ;;
  esac
done

# Create output directory
if [[ -z "$OUTPUT_DIR" ]]; then
  OUTPUT_DIR=$(mktemp -d)
fi
mkdir -p "$OUTPUT_DIR"

# Read products from stdin
PRODUCTS=$(cat)

# Count products
PRODUCT_COUNT=$(echo "$PRODUCTS" | jq 'length')

if [[ "$PRODUCT_COUNT" -eq 0 ]]; then
  echo "Error: No products provided" >&2
  exit 1
fi

# Generate HTML based on template
generate_deals_page() {
  cat << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$TITLE</title>
    <meta name="description" content="$TITLE - Best deals and offers">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: $PRIMARY_COLOR; --secondary: #16213e; --accent: #e94560; --gold: #f4d03f; --success: #27ae60; --text: #2c3e50; --text-light: #64748b; --bg: #f8fafc; --card-bg: #ffffff; --border: #e2e8f0; --shadow: 0 4px 6px -1px rgba(0,0,0,0.1); --shadow-lg: 0 20px 25px -5px rgba(0,0,0,0.1); }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
        header { background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); color: white; padding: 3rem 1rem; text-align: center; }
        .header-content { max-width: 800px; margin: 0 auto; }
        .badge { display: inline-block; background: var(--accent); color: white; padding: 0.5rem 1.5rem; border-radius: 50px; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin-bottom: 1.5rem; }
        h1 { font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; }
        .subtitle { font-size: 1.25rem; opacity: 0.9; margin-bottom: 2rem; }
        .stats { display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-top: 2rem; }
        .stat { text-align: center; }
        .stat-number { font-size: 2.5rem; font-weight: 800; color: var(--gold); }
        .stat-label { font-size: 0.875rem; opacity: 0.8; }
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
        .rating { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }
        .stars { color: var(--gold); }
        .review-count { font-size: 0.875rem; color: var(--text-light); }
        .buy-btn { display: block; width: 100%; padding: 1rem; background: linear-gradient(135deg, var(--accent), #d63d56); color: white; text-align: center; text-decoration: none; border-radius: 12px; font-weight: 700; transition: all 0.3s; }
        .buy-btn:hover { transform: scale(1.02); box-shadow: 0 8px 20px rgba(233,69,96,0.4); }
        footer { background: var(--primary); color: white; padding: 3rem 1rem; text-align: center; margin-top: 4rem; }
        @media (max-width: 768px) { h1 { font-size: 1.75rem; } .product-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <span class="badge">🔥 Limited Time Offers</span>
            <h1>$TITLE</h1>
            <p class="subtitle">Best deals curated for you</p>
            <div class="stats">
                <div class="stat"><div class="stat-number">$PRODUCT_COUNT</div><div class="stat-label">Deals</div></div>
                <div class="stat"><div class="stat-number" id="max-discount">-</div><div class="stat-label">Max Savings</div></div>
            </div>
        </div>
    </header>
    <main>
        <div class="product-grid">
            {{PRODUCT_CARDS}}
        </div>
    </main>
    <footer>
        <p>&copy; $(date +%Y) $TITLE. All rights reserved.</p>
    </footer>
    <script>
        const products = {{PRODUCTS_JSON}};
        const maxDiscount = Math.max(...products.map(p => parseInt(p.discount)));
        document.getElementById('max-discount').textContent = maxDiscount + '%';
    </script>
</body>
</html>
EOF
}

# Generate product cards HTML
PRODUCT_CARDS=""
while IFS= read -r product; do
  name=$(echo "$product" | jq -r '.name')
  brand=$(echo "$product" | jq -r '.brand')
  price=$(echo "$product" | jq -r '.price')
  original=$(echo "$product" | jq -r '.original_price')
  discount=$(echo "$product" | jq -r '.discount')
  url=$(echo "$product" | jq -r '.url')
  rating=$(echo "$product" | jq -r '.rating')
  reviews=$(echo "$product" | jq -r '.reviews')
  category=$(echo "$product" | jq -r '.category // "General"')
  
  # Generate stars based on rating
  full_stars=$(echo "$rating" | cut -d. -f1)
  half_star=$(echo "$rating" | cut -d. -f2)
  STARS=""
  for ((i=0; i<full_stars; i++)); do STARS="$STARS<i class='fas fa-star'></i>"; done
  if [[ "$half_star" -ge 5 ]]; then STARS="$STARS<i class='fas fa-star-half-alt'></i>"; fi
  
  CARD="
            <article class=\"product-card\">
                <span class=\"discount-badge\">-$discount</span>
                <div class=\"product-image\">
                    <img src=\"https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400&h=400&fit=crop\" alt=\"$name\">
                </div>
                <div class=\"product-info\">
                    <div class=\"brand\">$brand</div>
                    <h3 class=\"product-name\">$name</h3>
                    <div class=\"category\">$category</div>
                    <div class=\"price-row\">
                        <span class=\"current-price\">£$price</span>
                        <span class=\"original-price\">£$original</span>
                    </div>
                    <div class=\"rating\">
                        <span class=\"stars\">$STARS</span>
                        <span class=\"review-count\">$reviews reviews</span>
                    </div>
                    <a href=\"$url\" class=\"buy-btn\" target=\"_blank\">View Deal <i class=\"fas fa-external-link-alt\"></i></a>
                </div>
            </article>"
  PRODUCT_CARDS="$PRODUCT_CARDS$CARD"
done < <(echo "$PRODUCTS" | jq -c '.[]')

# Generate full HTML
HTML=$(generate_deals_page)

# Write product cards to temp file for replacement
CARDS_FILE=$(mktemp)
echo "$PRODUCT_CARDS" > "$CARDS_FILE"

# Write products JSON to temp file
JSON_FILE=$(mktemp)
echo "$PRODUCTS" | jq -c . > "$JSON_FILE"

# Replace placeholders using awk
OUTPUT_FILE="$OUTPUT_DIR/index.html"
awk -v cards_file="$CARDS_FILE" -v json_file="$JSON_FILE" '
  /{{PRODUCT_CARDS}}/ {
    while ((getline line < cards_file) > 0) print line
    close(cards_file)
    next
  }
  /{{PRODUCTS_JSON}}/ {
    while ((getline line < json_file) > 0) printf "%s", line
    close(json_file)
    next
  }
  { print }
' <<< "$HTML" > "$OUTPUT_FILE"

# Clean up temp files
rm -f "$CARDS_FILE" "$JSON_FILE"

# Output the file path
echo "$OUTPUT_FILE"
