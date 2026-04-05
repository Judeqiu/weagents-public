#!/bin/bash
#
# deploy_to_netlify.sh - Deploy site to Netlify
# Usage: deploy_to_netlify.sh --dir ./site --site-name "my-site" --prod
#

set -e

DIR=""
SITE_NAME=""
PROD=false

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dir) DIR="$2"; shift 2 ;;
    --site-name) SITE_NAME="$2"; shift 2 ;;
    --prod) PROD=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$DIR" ]]; then
  echo "Usage: deploy_to_netlify.sh --dir <directory> [--site-name <name>] [--prod]"
  exit 1
fi

if [[ ! -d "$DIR" ]]; then
  echo -e "${RED}Error: Directory not found: $DIR${NC}"
  exit 1
fi

# Check for index.html
if [[ ! -f "$DIR/index.html" ]]; then
  echo -e "${YELLOW}Warning: No index.html found in $DIR${NC}"
fi

# Check Netlify CLI
if ! command -v netlify &> /dev/null; then
  echo -e "${RED}Error: Netlify CLI not found. Install with: npm install -g netlify-cli${NC}"
  exit 1
fi

# Check login status
if ! netlify status &> /dev/null; then
  echo -e "${RED}Error: Not logged in to Netlify. Run: netlify login${NC}"
  exit 1
fi

cd "$DIR"

# Deploy
if [[ -n "$SITE_NAME" ]]; then
  # Create new site or use existing
  if [[ "$PROD" == true ]]; then
    netlify deploy --create-site "$SITE_NAME" --dir=. --prod 2>&1
  else
    netlify deploy --create-site "$SITE_NAME" --dir=. 2>&1
  fi
else
  # Deploy to linked site or create new
  if [[ "$PROD" == true ]]; then
    netlify deploy --dir=. --prod 2>&1
  else
    netlify deploy --dir=. 2>&1
  fi
fi
