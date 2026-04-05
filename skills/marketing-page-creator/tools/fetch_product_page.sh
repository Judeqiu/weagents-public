#!/bin/bash
#
# fetch_product_page.sh - Fetch a specific product page with anti-bot handling
# Usage: fetch_product_page.sh --url "https://..." [--extract "price,title,rating"]
# Output: JSON with extracted product data
#
# Uses agent-browser's smart_fetch for maximum compatibility

set -e

URL=""
EXTRACT_FIELDS="title,price,image,rating,reviews"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --url) URL="$2"; shift 2 ;;
    --extract) EXTRACT_FIELDS="$2"; shift 2 ;;
    *) echo '{"error": "Unknown option: '$1'"}' >&2; exit 1 ;;
  esac
done

if [[ -z "$URL" ]]; then
  echo '{"error": "Missing required arg: --url"}' >&2
  exit 1
fi

# Check for agent-browser skill
AGENT_BROWSER_SKILL="${AGENT_BROWSER_SKILL_PATH:-$HOME/.openclaw/workspace/skills/agent-browser}"

if [[ -f "$AGENT_BROWSER_SKILL/scripts/smart_fetch.py" ]]; then
  # Use smart_fetch with browser force for product pages
  TEMP_FILE=$(mktemp)
  
  if python3 "$AGENT_BROWSER_SKILL/scripts/smart_fetch.py" \
       --url "$URL" \
       --output "$TEMP_FILE" \
       --force-browser \
       2>/dev/null; then
    
    # Try to extract product data from the fetched content
    CONTENT=$(cat "$TEMP_FILE" 2>/dev/null || echo "")
    rm -f "$TEMP_FILE"
    
    # Simple extraction patterns (could be enhanced with more sophisticated parsing)
    TITLE=$(echo "$CONTENT" | grep -oP '<title>\K[^<]+' | head -1 || echo "")
    
    echo '{
      "url": "'$URL'",
      "source": "smart_fetch",
      "title": "'$(echo "$TITLE" | sed 's/"/\\"/g')'",
      "content_length": '$(echo "$CONTENT" | wc -c)',
      "extracted": false
    }'
    exit 0
  fi
  
  rm -f "$TEMP_FILE"
fi

# Fallback to fetch_content.sh
if [[ -f "$AGENT_BROWSER_SKILL/scripts/fetch_content.sh" ]]; then
  TEMP_FILE=$(mktemp)
  
  if "$AGENT_BROWSER_SKILL/scripts/fetch_content.sh" \
       --url "$URL" \
       --output "$TEMP_FILE" \
       2>/dev/null; then
    
    CONTENT=$(cat "$TEMP_FILE" 2>/dev/null || echo "")
    rm -f "$TEMP_FILE"
    
    TITLE=$(echo "$CONTENT" | grep -oP '<title>\K[^<]+' | head -1 || echo "")
    
    echo '{
      "url": "'$URL'",
      "source": "fetch_content",
      "title": "'$(echo "$TITLE" | sed 's/"/\\"/g')'",
      "content_length": '$(echo "$CONTENT" | wc -c)',
      "extracted": false
    }'
    exit 0
  fi
  
  rm -f "$TEMP_FILE"
fi

# All methods failed
echo '{
  "url": "'$URL'",
  "error": "Failed to fetch product page",
  "content": null
}'
exit 1
