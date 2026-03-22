#!/bin/bash
# Fetch Screenshot - Smart screenshot capture using all available browser methods
#
# This script tries multiple browser automation methods in order:
# 1. agent-browser (local, fast, bundled Chromium)
# 2. mychrome (Chrome CDP with persistent sessions)
# 3. Browserless API (cloud fallback, always works)
#
# Usage: ./fetch_screenshot.sh --url https://example.com --output /tmp/screenshot.png

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
URL=""
OUTPUT="/tmp/screenshot.png"
FULL_PAGE=false
VERBOSE=false
METHOD=""  # auto, agent-browser, mychrome, browserless
TIMEOUT=45
WIDTH=1920
HEIGHT=1080

echo_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}

show_help() {
    cat << EOF
Fetch Screenshot - Smart browser screenshot capture

USAGE:
    $0 --url <url> --output <path> [options]

REQUIRED:
    --url <url>           URL to capture screenshot of
    --output <path>       Save screenshot to this path

OPTIONS:
    --full-page           Capture full page (not just viewport)
    --width <px>          Viewport width (default: 1920)
    --height <px>         Viewport height (default: 1080)
    --method <name>       Force specific method: agent-browser, mychrome, browserless
    --timeout <seconds>   Timeout per method attempt (default: 45)
    --verbose, -v         Show detailed progress
    --help, -h            Show this help

METHODS (tried in order):
    1. agent-browser    Local bundled Chromium (fastest)
    2. mychrome         Chrome CDP (persistent sessions)
    3. browserless      Cloud API (always works)

EXAMPLES:
    # Capture screenshot (auto-select best method)
    $0 --url https://example.com --output /tmp/screenshot.png

    # Full page screenshot
    $0 --url https://example.com --output /tmp/full.png --full-page

    # Force specific method
    $0 --url https://example.com --output /tmp/screenshot.png --method browserless

    # Custom viewport size
    $0 --url https://example.com --output /tmp/mobile.png --width 375 --height 812

ENVIRONMENT:
    AGENT_BROWSER_ARGS    Args for agent-browser (default: --no-sandbox)
    CHROME_CDP_URL        Chrome CDP endpoint (default: http://localhost:9222)
    BROWSERLESS_TOKEN     Browserless API token (pre-configured in skill)
    BROWSERLESS_REGION    Browserless region: sfo, lon, ams (default: sfo)

EXIT CODES:
    0    Success
    1    All methods failed
    2    Invalid arguments
EOF
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --url)
                URL="$2"
                shift 2
                ;;
            --output)
                OUTPUT="$2"
                shift 2
                ;;
            --full-page)
                FULL_PAGE=true
                shift
                ;;
            --width)
                WIDTH="$2"
                shift 2
                ;;
            --height)
                HEIGHT="$2"
                shift 2
                ;;
            --method)
                METHOD="$2"
                shift 2
                ;;
            --timeout)
                TIMEOUT="$2"
                shift 2
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                show_help
                exit 2
                ;;
        esac
    done

    if [ -z "$URL" ]; then
        echo -e "${RED}Error: --url is required${NC}"
        show_help
        exit 2
    fi

    if [ -z "$OUTPUT" ]; then
        echo -e "${RED}Error: --output is required${NC}"
        show_help
        exit 2
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Method 1: agent-browser
try_agent_browser() {
    echo_verbose "Trying agent-browser..."
    
    if ! command_exists agent-browser; then
        echo_verbose "agent-browser not installed"
        return 1
    fi
    
    # Set args for sandbox if needed
    export AGENT_BROWSER_ARGS="${AGENT_BROWSER_ARGS:---no-sandbox}"
    
    # Build screenshot options
    local options=""
    if [ "$FULL_PAGE" = true ]; then
        options="--full"
    fi
    
    # Try to take screenshot
    local temp_file=$(mktemp).png
    
    if timeout $TIMEOUT bash -c "
        agent-browser open '$URL' && \
        agent-browser screenshot $options '$temp_file' && \
        agent-browser close
    " 2>/dev/null; then
        
        if [ -f "$temp_file" ] && [ -s "$temp_file" ]; then
            echo_verbose "agent-browser succeeded"
            mv "$temp_file" "$OUTPUT"
            echo -e "${GREEN}✓ Screenshot saved via agent-browser${NC}"
            return 0
        fi
    fi
    
    rm -f "$temp_file"
    echo_verbose "agent-browser failed"
    return 1
}

# Method 2: mychrome (Chrome CDP)
try_mychrome() {
    echo_verbose "Trying mychrome..."
    
    local chrome_url="${CHROME_CDP_URL:-http://localhost:9222}"
    local skill_path="$HOME/.openclaw/workspace/skills/mychrome"
    
    # Check if mychrome skill exists
    if [ ! -d "$skill_path" ]; then
        echo_verbose "mychrome skill not found"
        return 1
    fi
    
    # Check if Chrome is accessible
    if ! curl -s "$chrome_url/json/version" > /dev/null 2>&1; then
        echo_verbose "Chrome CDP not accessible at $chrome_url"
        return 1
    fi
    
    # Try to take screenshot using mychrome
    if timeout $TIMEOUT bash -c "
        export PATH=\"\$HOME/.local/share/fnm:\$PATH\"
        eval \"\$(fnm env --shell bash 2>/dev/null)\"
        
        python3 '$skill_path/scripts/chrome_cdp_helper.py' \
            --cdp-url '$chrome_url' \
            --url '$URL' \
            --screenshot '$OUTPUT' 2>/dev/null
    " 2>/dev/null; then
        
        if [ -f "$OUTPUT" ] && [ -s "$OUTPUT" ]; then
            echo_verbose "mychrome succeeded"
            echo -e "${GREEN}✓ Screenshot saved via mychrome${NC}"
            return 0
        fi
    fi
    
    echo_verbose "mychrome failed"
    return 1
}

# Method 3: Browserless API (always works as last resort)
try_browserless() {
    echo_verbose "Trying Browserless API..."
    
    local skill_path="$HOME/.openclaw/workspace/skills/agent-browser"
    local helper="$skill_path/scripts/browserless_helper.sh"
    
    # Check if helper exists
    if [ ! -f "$helper" ]; then
        echo_verbose "Browserless helper not found"
        return 1
    fi
    
    # Build options
    local options=""
    if [ "$FULL_PAGE" = true ]; then
        options="--full-page"
    fi
    
    # Try to take screenshot
    if timeout $TIMEOUT bash -c "
        '$helper' screenshot --url '$URL' --output '$OUTPUT' $options 2>/dev/null
    " 2>/dev/null; then
        
        if [ -f "$OUTPUT" ] && [ -s "$OUTPUT" ]; then
            echo_verbose "Browserless succeeded"
            echo -e "${GREEN}✓ Screenshot saved via Browserless API${NC}"
            return 0
        fi
    fi
    
    echo_verbose "Browserless failed"
    return 1
}

# Main fetch logic
fetch_screenshot() {
    echo "Capturing screenshot: $URL"
    echo "Output: $OUTPUT"
    if [ "$FULL_PAGE" = true ]; then
        echo "Mode: Full page"
    else
        echo "Viewport: ${WIDTH}x${HEIGHT}"
    fi
    echo ""
    
    local success_method=""
    
    # If specific method requested, try only that
    if [ -n "$METHOD" ]; then
        case $METHOD in
            agent-browser)
                if try_agent_browser; then
                    success_method="agent-browser"
                fi
                ;;
            mychrome)
                if try_mychrome; then
                    success_method="mychrome"
                fi
                ;;
            browserless)
                if try_browserless; then
                    success_method="browserless"
                fi
                ;;
            *)
                echo -e "${RED}Unknown method: $METHOD${NC}"
                exit 2
                ;;
        esac
        
        if [ -z "$success_method" ]; then
            echo -e "${RED}✗ Method '$METHOD' failed${NC}"
            exit 1
        fi
        return 0
    fi
    
    # Auto mode: try all methods in order
    echo -e "${YELLOW}Trying agent-browser (local Chromium)...${NC}"
    if try_agent_browser; then
        success_method="agent-browser"
    fi
    
    if [ -z "$success_method" ]; then
        echo -e "${YELLOW}Trying mychrome (Chrome CDP)...${NC}"
        if try_mychrome; then
            success_method="mychrome"
        fi
    fi
    
    if [ -z "$success_method" ]; then
        echo -e "${YELLOW}Trying Browserless API (cloud)...${NC}"
        if try_browserless; then
            success_method="browserless"
        fi
    fi
    
    # Report result
    echo ""
    if [ -n "$success_method" ]; then
        echo -e "${GREEN}✓ Success using: $success_method${NC}"
        echo "  Saved to: $OUTPUT"
        ls -lh "$OUTPUT" 2>/dev/null || true
        return 0
    else
        echo -e "${RED}✗ All methods failed${NC}"
        echo ""
        echo "Tried:"
        echo "  1. agent-browser (local Chromium)"
        echo "  2. mychrome (Chrome CDP)"
        echo "  3. Browserless API (cloud)"
        echo ""
        echo "Possible issues:"
        echo "  - URL is not accessible"
        echo "  - Network connectivity issues"
        echo "  - Site blocks all automation methods"
        return 1
    fi
}

# Main
main() {
    parse_args "$@"
    fetch_screenshot
}

main "$@"
