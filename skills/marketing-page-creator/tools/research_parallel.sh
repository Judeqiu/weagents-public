#!/bin/bash
#
# research_parallel.sh - Research REAL products from MULTIPLE sites in parallel
# Usage: research_parallel.sh --sites "site1,site2,site3" --query "search term"
# Output: Combined JSON from all sites
#
# This tool uses parallel execution for faster research across multiple sites.
# NEVER returns simulated/mock data - only real extracted data.

set -e

SITES=""
QUERY=""
MAX_ITEMS=5

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --sites) SITES="$2"; shift 2 ;;
    --query) QUERY="$2"; shift 2 ;;
    --max-items) MAX_ITEMS="$2"; shift 2 ;;
    *) echo '{"error": "Unknown option: '$1'"}' >&2; exit 1 ;;
  esac
done

if [[ -z "$SITES" || -z "$QUERY" ]]; then
  echo '{"error": "Missing required args: --sites and --query"}' >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create temp directory for parallel results
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Convert sites to array
IFS=',' read -ra SITE_ARRAY <<< "$SITES"

# Research each site in parallel
PIDS=()
for site in "${SITE_ARRAY[@]}"; do
  site=$(echo "$site" | xargs) # trim whitespace
  OUTPUT_FILE="$TEMP_DIR/${site}.json"
  
  # Run research in background
  "$SCRIPT_DIR/research_site.sh" \
    --site "$site" \
    --query "$QUERY" \
    --max-items "$MAX_ITEMS" \
    > "$OUTPUT_FILE" 2>/dev/null &
  
  PIDS+=($!)
done

# Wait for all background jobs to complete
for pid in "${PIDS[@]}"; do
  wait "$pid" 2>/dev/null || true
done

# Combine all results
COMBINED_PRODUCTS="[]"
SUCCESSFUL_SITES=()
FAILED_SITES=()

for site in "${SITE_ARRAY[@]}"; do
  site=$(echo "$site" | xargs)
  OUTPUT_FILE="$TEMP_DIR/${site}.json"
  
  if [[ -f "$OUTPUT_FILE" ]]; then
    # Check if the result contains an error
    if jq -e '.error' "$OUTPUT_FILE" >/dev/null 2>&1; then
      FAILED_SITES+=("$site")
    else
      # Extract products and add to combined array
      SITE_PRODUCTS=$(jq -r '.products // []' "$OUTPUT_FILE" 2>/dev/null || echo "[]")
      if [[ "$SITE_PRODUCTS" != "[]" && "$SITE_PRODUCTS" != "null" ]]; then
        COMBINED_PRODUCTS=$(echo "$COMBINED_PRODUCTS" "$SITE_PRODUCTS" | jq -s 'add')
        SUCCESSFUL_SITES+=("$site")
      fi
    fi
  else
    FAILED_SITES+=("$site")
  fi
done

# Count total products
TOTAL_COUNT=$(echo "$COMBINED_PRODUCTS" | jq 'length')

# Build final result
RESULT=$(jq -n \
  --arg query "$QUERY" \
  --arg sites "$SITES" \
  --arg successful "$(IFS=,; echo "${SUCCESSFUL_SITES[*]}")" \
  --arg failed "$(IFS=,; echo "${FAILED_SITES[*]}")" \
  --argjson total "$TOTAL_COUNT" \
  --argjson products "$COMBINED_PRODUCTS" \
  '{
    query: $query,
    sites_requested: ($sites | split(",") | map(gsub("^\\s+|\\s+$"; ""))),
    sites_successful: (if $successful == "" then [] else ($successful | split(",")) end),
    sites_failed: (if $failed == "" then [] else ($failed | split(",")) end),
    total_products: $total,
    products: $products
  }')

echo "$RESULT"

# Exit with error if no products found
if [[ "$TOTAL_COUNT" -eq 0 ]]; then
  exit 1
fi
