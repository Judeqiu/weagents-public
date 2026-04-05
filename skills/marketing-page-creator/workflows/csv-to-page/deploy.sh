#!/bin/bash
# Deploy product page to Netlify
# Usage: ./deploy.sh [site_directory] [--prod]

set -e

SITE_DIR="${1:-./site}"
PROD_FLAG=""

# Check for --prod flag
if [[ "$2" == "--prod" || "$1" == "--prod" ]]; then
    PROD_FLAG="--prod"
fi

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found. Please install:"
    echo "   npm install -g netlify-cli"
    exit 1
fi

# Check if directory exists
if [[ ! -d "$SITE_DIR" ]]; then
    echo "❌ Directory not found: $SITE_DIR"
    exit 1
fi

# Check if index.html exists
if [[ ! -f "$SITE_DIR/index.html" ]]; then
    echo "❌ index.html not found in $SITE_DIR"
    exit 1
fi

echo "🚀 Deploying to Netlify..."
echo "   Directory: $SITE_DIR"
echo "   Production: $([[ -n "$PROD_FLAG" ]] && echo 'Yes' || echo 'No (draft)')"
echo ""

# Deploy
cd "$SITE_DIR"

if [[ -n "$PROD_FLAG" ]]; then
    echo "Deploying to production..."
    netlify deploy --prod --dir=. --json | tee /tmp/deploy-result.json
else
    echo "Creating draft deploy..."
    netlify deploy --dir=. --json | tee /tmp/deploy-result.json
fi

# Extract URL from result
if command -v jq &> /dev/null; then
    DEPLOY_URL=$(jq -r '.url // .deploy_url' /tmp/deploy-result.json)
    echo ""
    echo "✅ Deploy successful!"
    echo ""
    echo "🌐 Live URL: $DEPLOY_URL"
else
    echo ""
    echo "✅ Deploy successful!"
    echo "   (Install jq to see URL automatically)"
fi
