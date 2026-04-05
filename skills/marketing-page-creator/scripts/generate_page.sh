#!/bin/bash
#
# generate_page.sh - Generate HTML page from research data
# Usage: generate_page.sh --input data.json --template deals --output index.html
#

set -e

# ============================================
# Template Functions (defined first)
# ============================================

function generate_deals_template() {
  local OUTPUT="$1"
  local TITLE="$2"
  local SUBTITLE="$3"
  local PRIMARY_COLOR="$4"
  local LANG="$5"
  local INPUT="$6"
  
  cat > "$OUTPUT" << EOF
<!DOCTYPE html>
<html lang="$LANG">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$TITLE | Best Deals</title>
    <meta name="description" content="$TITLE - Best deals and offers. Save money on top brands.">
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
        .intro { text-align: center; max-width: 800px; margin: 0 auto 3rem; }
        .intro h2 { font-size: 2rem; margin-bottom: 1rem; color: var(--primary); }
        .section { margin-bottom: 4rem; }
        .section-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 3px solid var(--border); }
        .section-icon { width: 60px; height: 60px; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 1.75rem; color: white; background: var(--primary); }
        .section-title { flex: 1; }
        .section-title h2 { font-size: 1.75rem; color: var(--primary); }
        .deal-count { background: var(--accent); color: white; padding: 0.5rem 1rem; border-radius: 50px; font-weight: 700; font-size: 0.875rem; }
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
        .description { font-size: 0.9375rem; color: var(--text-light); margin-bottom: 1.5rem; }
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
            <p class="subtitle">$SUBTITLE</p>
            <div class="stats">
                <div class="stat"><div class="stat-number" id="total-deals">0</div><div class="stat-label">Deals</div></div>
                <div class="stat"><div class="stat-number" id="max-savings">50%</div><div class="stat-label">Max Savings</div></div>
                <div class="stat"><div class="stat-number" id="retailers">0</div><div class="stat-label">Retailers</div></div>
            </div>
        </div>
    </header>
    <main>
        <section class="intro">
            <h2>Your Ultimate Guide to Savings</h2>
            <p>We've scoured the top retailers to bring you the best deals available right now.</p>
        </section>
        <div id="products-container"></div>
    </main>
    <footer>
        <p>&copy; $(date +%Y) $TITLE. All rights reserved.</p>
    </footer>
    <script>
        const products = $(jq '.products' "$INPUT");
        const sites = [...new Set(products.map(p => p.site))];
        
        document.getElementById('total-deals').textContent = products.length;
        document.getElementById('retailers').textContent = sites.length;
        
        const bySite = {};
        products.forEach(p => {
            if (!bySite[p.site]) bySite[p.site] = [];
            bySite[p.site].push(p);
        });
        
        const container = document.getElementById('products-container');
        
        sites.forEach(site => {
            const section = document.createElement('section');
            section.className = 'section';
            section.innerHTML = \`
                <div class="section-header">
                    <div class="section-icon"><i class="fas fa-store"></i></div>
                    <div class="section-title"><h2>\${site.charAt(0).toUpperCase() + site.slice(1)} Deals</h2></div>
                    <span class="deal-count">\${bySite[site].length} Deals</span>
                </div>
                <div class="product-grid">
                    \${bySite[site].map(p => \`
                        <article class="product-card">
                            <span class="discount-badge">-\${p.discount}</span>
                            <div class="product-image"><img src="\${p.image}" alt="\${p.name}"></div>
                            <div class="product-info">
                                <div class="brand">\${p.brand}</div>
                                <h3 class="product-name">\${p.name}</h3>
                                <div class="category">\${p.category}</div>
                                <div class="price-row">
                                    <span class="current-price">£\${p.price}</span>
                                    <span class="original-price">£\${p.original_price}</span>
                                </div>
                                <div class="rating">
                                    <span class="stars"><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star-half-alt"></i></span>
                                    <span class="review-count">\${p.reviews}+ reviews</span>
                                </div>
                                <p class="description">\${p.description || 'Great deal on ' + p.name}</p>
                                <a href="\${p.url}" class="buy-btn" target="_blank" rel="nofollow">View Deal <i class="fas fa-external-link-alt"></i></a>
                            </div>
                        </article>
                    \`).join('')}
                </div>
            \`;
            container.appendChild(section);
        });
    </script>
</body>
</html>
EOF
}

# ============================================
# Main Script
# ============================================

INPUT=""
TEMPLATE="deals"
OUTPUT=""
TITLE=""
SUBTITLE=""
PRIMARY_COLOR="#e94560"
LANG="en"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --input) INPUT="$2"; shift 2 ;;
    --template) TEMPLATE="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --title) TITLE="$2"; shift 2 ;;
    --subtitle) SUBTITLE="$2"; shift 2 ;;
    --primary-color) PRIMARY_COLOR="$2"; shift 2 ;;
    --lang) LANG="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
  echo "Usage: generate_page.sh --input <data.json> --output <index.html>"
  exit 1
fi

# Read data
if [[ ! -f "$INPUT" ]]; then
  echo "Error: Input file not found: $INPUT"
  exit 1
fi

# Use provided title or get from data
if [[ -z "$TITLE" ]]; then
  TITLE=$(jq -r '.meta.query // "Marketing Page"' "$INPUT")
fi

if [[ -z "$SUBTITLE" ]]; then
  SUBTITLE="Best deals curated for you"
fi

# Create output directory
mkdir -p "$(dirname "$OUTPUT")"

# Generate based on template
case $TEMPLATE in
  deals)
    generate_deals_template "$OUTPUT" "$TITLE" "$SUBTITLE" "$PRIMARY_COLOR" "$LANG" "$INPUT"
    ;;
  *)
    generate_deals_template "$OUTPUT" "$TITLE" "$SUBTITLE" "$PRIMARY_COLOR" "$LANG" "$INPUT"
    ;;
esac

echo "✓ Page generated: $OUTPUT"
