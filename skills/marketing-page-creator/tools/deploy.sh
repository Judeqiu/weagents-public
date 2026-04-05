#!/bin/bash
#
# deploy.sh - Deploy site to Netlify
# Usage: deploy.sh --dir ./site [--site-name "my-site"]
# Output: Deployment URL

set -e

DIR=""
SITE_NAME=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dir) DIR="$2"; shift 2 ;;
    --site-name) SITE_NAME="$2"; shift 2 ;;
    *) echo "Error: Unknown option $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$DIR" ]]; then
  echo "Error: --dir is required" >&2
  exit 1
fi

if [[ ! -d "$DIR" ]]; then
  echo "Error: Directory not found: $DIR" >&2
  exit 1
fi

if [[ ! -f "$DIR/index.html" ]]; then
  echo "Error: No index.html in $DIR" >&2
  exit 1
fi

# Check Netlify CLI
if ! command -v netlify &> /dev/null; then
  echo "Error: Netlify CLI not installed" >&2
  exit 1
fi

# Deploy
cd "$DIR"

if [[ -n "$SITE_NAME" ]]; then
  OUTPUT=$(netlify deploy --prod --dir=. --site="$SITE_NAME" 2>&1 || netlify deploy --prod --dir=. 2>&1)
else
  OUTPUT=$(netlify deploy --prod --dir=. 2>&1)
fi

# Extract URL
URL=$(echo "$OUTPUT" | grep -oE 'https://[a-zA-Z0-9-]+\.netlify\.app' | head -1)

if [[ -n "$URL" ]]; then
  echo "$URL"
else
  echo "Error: Deployment failed" >&2
  echo "$OUTPUT" >&2
  exit 1
fi
