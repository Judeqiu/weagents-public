#!/bin/bash
#
# filter_products.sh - Filter and sort products based on criteria
# Usage: cat products.json | filter_products.sh --min-discount 20 --max-items 10
# Input: JSON array of products from stdin
# Output: Filtered JSON array to stdout
#
# This is a TOOL script - called by LLM to curate products

set -e

MIN_DISCOUNT=0
MAX_PRICE=999999
MIN_RATING=0
MAX_ITEMS=999999
SORT_BY="discount"  # discount, price, rating

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --min-discount) MIN_DISCOUNT="$2"; shift 2 ;;
    --max-price) MAX_PRICE="$2"; shift 2 ;;
    --min-rating) MIN_RATING="$2"; shift 2 ;;
    --max-items) MAX_ITEMS="$2"; shift 2 ;;
    --sort-by) SORT_BY="$2"; shift 2 ;;
    *) echo '{"error": "Unknown option: '$1'"}' >&2; exit 1 ;;
  esac
done

# Read products from stdin
PRODUCTS=$(cat)

# Validate input
if ! echo "$PRODUCTS" | jq -e '. | arrays' >/dev/null 2>&1; then
  echo '{"error": "Invalid input: expected JSON array"}' >&2
  exit 1
fi

# Filter and sort
FILTERED=$(echo "$PRODUCTS" | jq --argjson min_discount "$MIN_DISCOUNT" \
  --argjson max_price "$MAX_PRICE" \
  --argjson min_rating "$MIN_RATING" \
  --argjson max_items "$MAX_ITEMS" \
  --arg sort_by "$SORT_BY" '
  map(select(
    (.discount // "0%" | sub("%"; "") | tonumber) >= $min_discount and
    (.price // 999999) <= $max_price and
    (.rating // 0) >= $min_rating
  )) |
  sort_by(
    if $sort_by == "discount" then -((.discount // "0%" | sub("%"; "") | tonumber))
    elif $sort_by == "price" then .price
    elif $sort_by == "rating" then -.rating
    else -((.discount // "0%" | sub("%"; "") | tonumber))
    end
  ) |
  .[:$max_items]
')

echo "$FILTERED"
