#!/bin/bash
# ProductHunter Example Workflows
# This script demonstrates common usage patterns for the producthunter skill

echo "====================================="
echo "ProductHunter - Example Workflows"
echo "====================================="
echo ""

# Check Chrome CDP connection
echo "1. Checking Chrome CDP connection..."
if curl -s http://127.0.0.1:9222/json/version > /dev/null; then
    echo "   Chrome CDP is running"
else
    echo "   WARNING: Chrome CDP not detected"
    echo "   Start Chrome with:"
    echo "   google-chrome --remote-debugging-port=9222 --user-data-dir=~/.chrome-producthunter &"
    echo ""
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$SKILL_DIR/scripts/product_hunter.py"

echo "2. Example Commands:"
echo ""

# Example 1: Single Product
echo "--- Example 1: Extract Single Product ---"
echo "python3 $SCRIPT \\"
echo "  --url \"https://www.amazon.com/dp/B08N5WRWNW\" \\"
echo "  --output ./single_product.csv"
echo ""

# Example 2: Multiple Products from Search
echo "--- Example 2: Extract Search Results ---"
echo "python3 $SCRIPT \\"
echo "  --url \"https://www.amazon.com/s?k=laptop\" \\"
echo "  --multiple \\"
echo "  --max-products 20 \\"
echo "  --output ./search_results.csv"
echo ""

# Example 3: Natural Language Request
echo "--- Example 3: Natural Language Request ---"
echo "python3 $SCRIPT \\"
echo "  --request \"Find wireless headphones on amazon\" \\"
echo "  --output ./headphones.csv"
echo ""

# Example 4: With Scrolling (for lazy-loaded content)
echo "--- Example 4: With Scrolling ---"
echo "python3 $SCRIPT \\"
echo "  --url \"https://www.ebay.com/sch/i.html?_nkw=iphone\" \\"
echo "  --multiple \\"
echo "  --scroll \\"
echo "  --scroll-pause 3 \\"
echo "  --max-products 50 \\"
echo "  --output ./ebay_products.csv"
echo ""

# Example 5: JSON Output
echo "--- Example 5: JSON Output ---"
echo "python3 $SCRIPT \\"
echo "  --url \"https://www.amazon.com/dp/B08N5WRWNW\" \\"
echo "  --format json \\"
echo "  --output ./product.json"
echo ""

# Example 6: Batch Processing
echo "--- Example 6: Batch Processing ---"
echo "# Create urls.txt with one URL per line"
echo "# cat urls.txt"
echo "# https://amazon.com/dp/..."
echo "# https://ebay.com/itm/..."
echo "python3 $SCRIPT \\"
echo "  --batch urls.txt \\"
echo "  --output ./batch_results.csv"
echo ""

# Example 7: With Screenshot
echo "--- Example 7: With Screenshot ---"
echo "python3 $SCRIPT \\"
echo "  --url \"https://www.amazon.com/dp/B08N5WRWNW\" \\"
echo "  --screenshot ./product_page.png \\"
echo "  --output ./product.csv"
echo ""

echo "====================================="
echo "Tips:"
echo "====================================="
echo "- Always ensure Chrome is running with CDP enabled"
echo "- Use --scroll for pages with infinite scroll"
echo "- Use --delay to avoid rate limiting"
echo "- Use --screenshot to debug extraction issues"
echo ""
