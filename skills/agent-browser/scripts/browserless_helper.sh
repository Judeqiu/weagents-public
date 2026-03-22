#!/bin/bash
# Browserless API Helper Script
# Simple interface to Browserless REST API for screenshots, PDFs, and content extraction
# Usage: ./browserless_helper.sh [command] [options]
#
# Requires: BROWSERLESS_TOKEN environment variable
# Get token from: https://www.browserless.io/ (or ask your admin)

set -e

# Configuration
BROWSERLESS_TOKEN="${BROWSERLESS_TOKEN:-}"
BROWSERLESS_REGION="${BROWSERLESS_REGION:-sfo}"  # sfo, lon, ams
BROWSERLESS_BASE_URL="https://production-${BROWSERLESS_REGION}.browserless.io"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Help message
show_help() {
    cat << EOF
Browserless API Helper - Cloud browser automation

USAGE:
    $0 [command] [options]

COMMANDS:
    screenshot    Take a screenshot of a URL
    content       Extract page content/HTML
    pdf           Generate PDF from URL
    unblock       Advanced unblocking with options
    status        Check Browserless API status

ENVIRONMENT:
    BROWSERLESS_TOKEN    Your API token (required)
    BROWSERLESS_REGION   Region: sfo (default), lon, ams

EXAMPLES:
    # Set your token
    export BROWSERLESS_TOKEN="your-token-here"

    # Take screenshot
    $0 screenshot --url https://example.com --output screenshot.png

    # Extract content
    $0 content --url https://example.com

    # Generate PDF
    $0 pdf --url https://example.com --output page.pdf

    # Use different region
    BROWSERLESS_REGION=lon $0 screenshot --url https://example.com

REGIONS:
    sfo    US West (San Francisco) - default
    lon    Europe UK (London)
    ams    Europe (Amsterdam)

For full documentation: https://docs.browserless.io/
EOF
}

# Check token
check_token() {
    if [ -z "$BROWSERLESS_TOKEN" ]; then
        echo -e "${RED}Error: BROWSERLESS_TOKEN not set${NC}"
        echo ""
        echo "Get your token from https://www.browserless.io/ or ask your admin."
        echo "Then set it: export BROWSERLESS_TOKEN='your-token-here'"
        exit 1
    fi
}

# Check dependencies
check_deps() {
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}Error: curl is required but not installed${NC}"
        exit 1
    fi
}

# Screenshot command
cmd_screenshot() {
    local url=""
    local output="screenshot.png"
    local full_page="false"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --url)
                url="$2"
                shift 2
                ;;
            --output)
                output="$2"
                shift 2
                ;;
            --full-page)
                full_page="true"
                shift
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    if [ -z "$url" ]; then
        echo -e "${RED}Error: --url is required${NC}"
        echo "Usage: $0 screenshot --url https://example.com [--output screenshot.png]"
        exit 1
    fi

    echo -e "${GREEN}Taking screenshot of $url...${NC}"

    # Build JSON payload
    local json="{\"url\":\"$url\",\"options\":{\"fullPage\":$full_page,\"type\":\"png\"}}"

    # Make request
    curl -s -X POST \
        "${BROWSERLESS_BASE_URL}/screenshot?token=${BROWSERLESS_TOKEN}" \
        -H 'Content-Type: application/json' \
        -d "$json" \
        --output "$output"

    if [ -f "$output" ]; then
        echo -e "${GREEN}✓ Screenshot saved to: $output${NC}"
        ls -lh "$output"
    else
        echo -e "${RED}✗ Failed to save screenshot${NC}"
        exit 1
    fi
}

# Content command
cmd_content() {
    local url=""
    local output=""

    while [[ $# -gt 0 ]]; do
        case $1 in
            --url)
                url="$2"
                shift 2
                ;;
            --output)
                output="$2"
                shift 2
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    if [ -z "$url" ]; then
        echo -e "${RED}Error: --url is required${NC}"
        echo "Usage: $0 content --url https://example.com [--output content.html]"
        exit 1
    fi

    echo -e "${GREEN}Extracting content from $url...${NC}"

    local json="{\"url\":\"$url\"}"

    if [ -n "$output" ]; then
        curl -s -X POST \
            "${BROWSERLESS_BASE_URL}/content?token=${BROWSERLESS_TOKEN}" \
            -H 'Content-Type: application/json' \
            -d "$json" \
            --output "$output"
        echo -e "${GREEN}✓ Content saved to: $output${NC}"
    else
        curl -s -X POST \
            "${BROWSERLESS_BASE_URL}/content?token=${BROWSERLESS_TOKEN}" \
            -H 'Content-Type: application/json' \
            -d "$json"
        echo ""  # Newline after output
    fi
}

# PDF command
cmd_pdf() {
    local url=""
    local output="page.pdf"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --url)
                url="$2"
                shift 2
                ;;
            --output)
                output="$2"
                shift 2
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    if [ -z "$url" ]; then
        echo -e "${RED}Error: --url is required${NC}"
        echo "Usage: $0 pdf --url https://example.com [--output page.pdf]"
        exit 1
    fi

    echo -e "${GREEN}Generating PDF from $url...${NC}"

    local json="{\"url\":\"$url\",\"options\":{\"printBackground\":true,\"format\":\"A4\"}}"

    curl -s -X POST \
        "${BROWSERLESS_BASE_URL}/pdf?token=${BROWSERLESS_TOKEN}" \
        -H 'Content-Type: application/json' \
        -d "$json" \
        --output "$output"

    if [ -f "$output" ]; then
        echo -e "${GREEN}✓ PDF saved to: $output${NC}"
        ls -lh "$output"
    else
        echo -e "${RED}✗ Failed to save PDF${NC}"
        exit 1
    fi
}

# Status command
cmd_status() {
    echo "Browserless API Status Check"
    echo "============================"
    echo ""
    echo "Region: $BROWSERLESS_REGION"
    echo "Base URL: $BROWSERLESS_BASE_URL"
    echo ""

    if [ -z "$BROWSERLESS_TOKEN" ]; then
        echo -e "${RED}✗ Token not set${NC}"
        echo "Set BROWSERLESS_TOKEN environment variable"
        return 1
    fi

    echo -e "${GREEN}✓ Token is set${NC}"
    echo ""
    echo "Testing connection..."

    # Test with a simple request
    local response=$(curl -s -o /dev/null -w "%{http_code}" \
        "${BROWSERLESS_BASE_URL}/content?token=${BROWSERLESS_TOKEN}" \
        -X POST \
        -H 'Content-Type: application/json' \
        -d '{"url":"https://example.com"}' 2>/dev/null)

    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓ API is accessible${NC}"
    elif [ "$response" = "401" ] || [ "$response" = "403" ]; then
        echo -e "${RED}✗ Authentication failed (HTTP $response)${NC}"
        echo "Check your BROWSERLESS_TOKEN"
    else
        echo -e "${YELLOW}⚠ API returned HTTP $response${NC}"
    fi
}

# Main
main() {
    check_deps

    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    local command="$1"
    shift

    case $command in
        screenshot)
            check_token
            cmd_screenshot "$@"
            ;;
        content)
            check_token
            cmd_content "$@"
            ;;
        pdf)
            check_token
            cmd_pdf "$@"
            ;;
        status)
            cmd_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}Unknown command: $command${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
