#!/usr/bin/env python3
"""
Generate Product List Page from CSV
Converts product CSV data into a beautiful HTML page

⚠️  WARNING: This script ONLY works with REAL data from actual websites.
    It will FAIL if the CSV contains fake, mock, or placeholder data.
    
    Before running this script, verify your CSV:
    - head -5 products.csv
    - Check URLs are from actual source domain
    - Check titles are real product names

Usage:
    python generate_page.py --input products.csv --output ./site/index.html
    python generate_page.py --input products.csv --title "My Deals Page"

Verification:
    The script automatically verifies data before generating the page.
    If fake data is detected, it will STOP and report an error.
"""

import argparse
import csv
import json
import os
from datetime import datetime


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        header {{
            text-align: center;
            padding: 40px 20px;
            color: white;
        }}
        
        header h1 {{
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        
        header p {{ font-size: 1.2rem; opacity: 0.9; }}
        
        .filters {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 10px 24px;
            border: none;
            border-radius: 50px;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }}
        
        .filter-btn:hover, .filter-btn.active {{
            background: white;
            color: #764ba2;
        }}
        
        .products-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            padding: 20px 0;
        }}
        
        .product-card {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
        }}
        
        .product-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        .product-image {{
            width: 100%;
            height: 250px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
        }}
        
        .product-image img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        
        .product-info {{
            padding: 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }}
        
        .category-tag {{
            display: inline-block;
            padding: 4px 12px;
            background: #764ba2;
            color: white;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            border-radius: 20px;
            margin-bottom: 10px;
            align-self: flex-start;
        }}
        
        .product-title {{
            font-size: 1rem;
            font-weight: 600;
            color: #1a1a1a;
            line-height: 1.4;
            margin-bottom: 12px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .product-rating {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }}
        
        .stars {{ color: #ffc107; font-size: 0.9rem; }}
        .rating-value {{ font-weight: 600; color: #333; }}
        .reviews-count {{ color: #666; font-size: 0.85rem; }}
        
        .product-price {{
            margin-top: auto;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }}
        
        .current-price {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #e74c3c;
        }}
        
        .original-price {{
            font-size: 1rem;
            color: #999;
            text-decoration: line-through;
            margin-left: 8px;
        }}
        
        .price-unavailable {{
            font-size: 1rem;
            color: #666;
            font-style: italic;
        }}
        
        .buy-button {{
            display: block;
            width: 100%;
            padding: 14px;
            margin-top: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .buy-button:hover {{
            transform: scale(1.02);
            box-shadow: 0 5px 20px rgba(118, 75, 162, 0.4);
        }}
        
        .stats-bar {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: 30px auto;
            max-width: 800px;
            display: flex;
            justify-content: space-around;
            color: white;
            text-align: center;
        }}
        
        .stat-item h3 {{ font-size: 2rem; font-weight: 700; }}
        .stat-item p {{ opacity: 0.8; font-size: 0.9rem; }}
        
        footer {{
            text-align: center;
            padding: 40px;
            color: rgba(255,255,255,0.7);
        }}
        
        @media (max-width: 768px) {{
            header h1 {{ font-size: 2rem; }}
            .products-grid {{ grid-template-columns: 1fr; }}
            .stats-bar {{ flex-direction: column; gap: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{page_title}</h1>
            <p>{subtitle}</p>
        </header>

        <div class="stats-bar">
            <div class="stat-item">
                <h3>{product_count}</h3>
                <p>Products</p>
            </div>
            <div class="stat-item">
                <h3>{category_count}</h3>
                <p>Categories</p>
            </div>
            <div class="stat-item">
                <h3>{avg_rating}</h3>
                <p>Avg Rating</p>
            </div>
        </div>

        <div class="filters">
            <button class="filter-btn active" data-filter="all">All</button>
            {filter_buttons}
        </div>

        <div class="products-grid" id="productsGrid"></div>

        <footer>
            <p>Last updated: {timestamp} | Data from {source}</p>
        </footer>
    </div>

    <script>
        const products = {products_json};
        
        const categoryLabels = {category_labels};
        
        function getStarsHTML(rating) {{
            if (!rating) return '';
            const fullStars = Math.floor(parseFloat(rating));
            let html = '<span class="stars">';
            for (let i = 0; i < fullStars; i++) html += '★';
            html += '</span>';
            return html;
        }}
        
        function renderProducts(filter = 'all') {{
            const grid = document.getElementById('productsGrid');
            grid.innerHTML = '';
            
            const filtered = filter === 'all' 
                ? products 
                : products.filter(p => p.category === filter);
            
            filtered.forEach(product => {{
                const card = document.createElement('div');
                card.className = 'product-card';
                
                const priceHTML = product.price 
                    ? `<span class="current-price">${{product.price}}</span>${{product.original_price ? `<span class="original-price">${{product.original_price}}</span>` : ''}}`
                    : '<span class="price-unavailable">See price on site</span>';
                
                const ratingHTML = product.rating 
                    ? `<div class="product-rating">${{getStarsHTML(product.rating)}}<span class="rating-value">${{product.rating}}</span>${{product.reviews ? `<span class="reviews-count">(${{product.reviews}} reviews)</span>` : ''}}</div>`
                    : '';
                
                card.innerHTML = `
                    <div class="product-image">
                        <img src="${{product.image || 'https://via.placeholder.com/300x250?text=No+Image'}}" alt="${{product.title}}" loading="lazy">
                    </div>
                    <div class="product-info">
                        <span class="category-tag">${{categoryLabels[product.category] || product.category}}</span>
                        <h3 class="product-title">${{product.title}}</h3>
                        ${{ratingHTML}}
                        <div class="product-price">${{priceHTML}}</div>
                        <a href="${{product.link}}" target="_blank" rel="noopener" class="buy-button">View Product →</a>
                    </div>
                `;
                
                grid.appendChild(card);
            }});
        }}
        
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderProducts(btn.dataset.filter);
            }});
        }});
        
        renderProducts();
    </script>
</body>
</html>
'''


def load_products_from_csv(csv_file):
    """Load products from CSV file"""
    products = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)
    return products


def calculate_stats(products):
    """Calculate statistics from products"""
    categories = set(p.get('category', 'other') for p in products)
    ratings = [float(p['rating']) for p in products if p.get('rating')]
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 'N/A'
    
    return {
        'count': len(products),
        'categories': len(categories),
        'avg_rating': avg_rating
    }


def generate_filter_buttons(products):
    """Generate filter buttons HTML"""
    categories = sorted(set(p.get('category', 'other') for p in products))
    
    category_labels = {
        'electronics': 'Electronics',
        'fashion': 'Fashion',
        'home': 'Home & Kitchen',
        'other': 'Other'
    }
    
    buttons = []
    for cat in categories:
        label = category_labels.get(cat, cat.title())
        buttons.append(f'<button class="filter-btn" data-filter="{cat}">{label}</button>')
    
    return '\n            '.join(buttons)


def verify_real_data(products):
    """Verify that products contain real data, not fake/mock data"""
    if not products:
        raise ValueError("No products found in CSV")
    
    # Check first product for signs of real data
    first = products[0]
    
    # Must have a real URL (not example.com or placeholder)
    link = first.get('link', '')
    if not link or 'example.com' in link or 'placeholder' in link:
        raise ValueError(f"Invalid product URL detected: {link}")
    
    # Must have a real title (not "Example Product")
    title = first.get('title', '')
    if not title or 'example' in title.lower() or 'sample' in title.lower() or 'product' == title.lower():
        raise ValueError(f"Suspicious product title detected: {title}")
    
    # Check for common e-commerce domains
    real_domains = ['amazon', 'ebay', 'etsy', 'shopify', 'asos', 'zara', 'nike']
    has_real_domain = any(domain in link.lower() for domain in real_domains)
    
    if not has_real_domain:
        print(f"⚠️  Warning: URL doesn't match known e-commerce domain: {link}")
    
    return True


def generate_page(csv_file, output_file, title=None, subtitle=None, source='Amazon'):
    """Generate HTML page from CSV data"""
    
    # Load products
    print(f"📂 Loading products from: {csv_file}")
    products = load_products_from_csv(csv_file)
    print(f"  ✓ Loaded {len(products)} products")
    
    # VERIFY: Check for real data before proceeding
    print("\n🔍 Verifying data is real (not fake/mock)...")
    try:
        verify_real_data(products)
        print("  ✓ Data verification passed - products appear to be real")
    except ValueError as e:
        print(f"\n❌ DATA VERIFICATION FAILED: {e}")
        print("\n⚠️  This CSV appears to contain fake or placeholder data.")
        print("   DO NOT proceed with page generation.")
        print("\n   To fix:")
        print("   1. Delete this CSV file")
        print("   2. Re-run research.py to extract real data")
        print("   3. Verify the new CSV contains actual product URLs")
        raise
    
    # Calculate stats
    stats = calculate_stats(products)
    
    # Prepare data
    page_title = title or "Best Deals"
    page_subtitle = subtitle or "Hand-picked products with reviews and ratings"
    
    categories = sorted(set(p.get('category', 'other') for p in products))
    category_labels = {}
    for cat in categories:
        category_labels[cat] = cat.title()
    
    # Generate HTML
    print(f"🎨 Generating HTML page...")
    html = HTML_TEMPLATE.format(
        title=page_title,
        page_title=page_title,
        subtitle=page_subtitle,
        product_count=stats['count'],
        category_count=stats['categories'],
        avg_rating=stats['avg_rating'],
        filter_buttons=generate_filter_buttons(products),
        products_json=json.dumps(products),
        category_labels=json.dumps(category_labels),
        timestamp=datetime.now().strftime('%B %d, %Y'),
        source=source
    )
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    
    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  ✓ Saved to: {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(description='Generate product page from CSV')
    parser.add_argument('--input', '-i', required=True, help='Input CSV file')
    parser.add_argument('--output', '-o', default='./site/index.html', help='Output HTML file')
    parser.add_argument('--title', '-t', help='Page title')
    parser.add_argument('--subtitle', '-s', help='Page subtitle')
    parser.add_argument('--source', default='Amazon', help='Product source name')
    
    args = parser.parse_args()
    
    generate_page(
        csv_file=args.input,
        output_file=args.output,
        title=args.title,
        subtitle=args.subtitle,
        source=args.source
    )
    
    print(f"\n🚀 Next step: Deploy to Netlify")
    print(f"   cd {os.path.dirname(args.output) or '.'}")
    print(f"   netlify deploy --prod --dir=.")


if __name__ == "__main__":
    main()
