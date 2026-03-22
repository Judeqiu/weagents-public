#!/bin/bash
# Fetch Content - Smart content retrieval using all available browser methods
#
# This script tries multiple browser automation methods in order:
# 1. agent-browser (local, fast, bundled Chromium)
# 2. mychrome (Chrome CDP with persistent sessions)
# 3. Browserless API (cloud fallback, always works)
#
# Usage: ./fetch_content.sh --url https://example.com [--output /tmp/content.html]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
URL=""
OUTPUT=""
VERBOSE=false
METHOD=""  # auto, agent-browser, mychrome, browserless
TIMEOUT=30

echo_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}

show_help() {
    cat << EOF
Fetch Content - Smart browser content retrieval

USAGE:
    $0 --url <url> [options]

REQUIRED:
    --url <url>           URL to fetch content from

OPTIONS:
    --output <path>       Save content to file (default: stdout)
    --method <name>       Force specific method: agent-browser, mychrome, browserless
    --timeout <seconds>   Timeout per method attempt (default: 30)
    --verbose, -v         Show detailed progress
    --help, -h            Show this help

METHODS (tried in order):
    1. agent-browser    Local bundled Chromium (fastest)
    2. mychrome         Chrome CDP (persistent sessions)
    3. browserless      Cloud API (always works)

EXAMPLES:
    # Fetch content (auto-select best method)
    $0 --url https://example.com

    # Save to file
    $0 --url https://example.com --output /tmp/page.html

    # Force specific method
    $0 --url https://example.com --method browserless

    # Verbose with custom timeout
    $0 --url https://example.com --verbose --timeout 60

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
    
    # Create temp file
    local temp_file=$(mktemp)
    
    # Try to fetch content
    if timeout $TIMEOUT bash -c "
        agent-browser open '$URL' && \
        agent-browser content > '$temp_file' && \
        agent-browser close
    " 2>/dev/null; then
        
        if [ -s "$temp_file" ]; then
            echo_verbose "agent-browser succeeded"
            if [ -n "$OUTPUT" ]; then
                mv "$temp_file" "$OUTPUT"
                echo -e "${GREEN}✓ Content saved via agent-browser${NC}"
            else
                cat "$temp_file"
                rm "$temp_file"
            fi
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
    
    # Try to fetch content using mychrome
    local temp_file=$(mktemp)
    
    if timeout $TIMEOUT bash -c "
        export PATH=\"\$HOME/.local/share/fnm:\$PATH\"
        eval \"\$(fnm env --shell bash 2>/dev/null)\"
        
        python3 '$skill_path/scripts/chrome_cdp_helper.py' \
            --cdp-url '$chrome_url' \
            --url '$URL' \
            --extract-content > '$temp_file' 2>/dev/null
    " 2>/dev/null; then
        
        if [ -s "$temp_file" ]; then
            echo_verbose "mychrome succeeded"
            if [ -n "$OUTPUT" ]; then
                # Extract content from JSON response
                cat "$temp_file" > "$OUTPUT"
                echo -e "${GREEN}✓ Content saved via mychrome${NC}"
            else
                cat "$temp_file"
            fi
            rm "$temp_file"
            return 0
        fi
    fi
    
    rm -f "$temp_file"
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
    
    # Try to fetch content
    local temp_file=$(mktemp)
    
    if timeout $TIMEOUT bash -c "
        '$helper' content --url '$URL' --output '$temp_file' 2>/dev/null
    " 2>/dev/null; then
        
        if [ -s "$temp_file" ]; then
            echo_verbose "Browserless succeeded"
            if [ -n "$OUTPUT" ]; then
                mv "$temp_file" "$OUTPUT"
                echo -e "${GREEN}✓ Content saved via Browserless API${NC}"
            else
                cat "$temp_file"
                rm "$temp_file"
            fi
            return 0
        fi
    fi
    
    rm -f "$temp_file"
    echo_verbose "Browserless failed"
    return 1
}

# Method 4: curl (simple HTTP fallback)
try_curl() {
    echo_verbose "Trying curl (simple HTTP)..."
    
    local temp_file=$(mktemp)
    
    if timeout $TIMEOUT curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "$URL" > "$temp_file" 2>/dev/null; then
        if [ -s "$temp_file" ]; then
            echo_verbose "curl succeeded"
            if [ -n "$OUTPUT" ]; then
                mv "$temp_file" "$OUTPUT"
                echo -e "${GREEN}✓ Content saved via curl${NC}"
            else
                cat "$temp_file"
                rm "$temp_file"
            fi
            return 0
        fi
    fi
    
    rm -f "$temp_file"
    echo_verbose "curl failed"
    return 1
}

# Main fetch logic
fetch_content() {
    echo "Fetching: $URL"
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
            curl)
                if try_curl; then
                    success_method="curl"
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
    
    if [ -z "$success_method" ]; then
        echo -e "${YELLOW}Trying curl (simple HTTP)...${NC}"
        if try_curl; then
            success_method="curl"
        fi
    fi
    
    # Report result
    echo ""
    if [ -n "$success_method" ]; then
        echo -e "${GREEN}✓ Success using: $success_method${NC}"
        if [ -n "$OUTPUT" ]; then
            echo "  Saved to: $OUTPUT"
            ls -lh "$OUTPUT" 2>/dev/null || true
        fi
        return 0
    else
        echo -e "${RED}✗ All methods failed${NC}"
        echo ""
        echo "Tried:"
        echo "  1. agent-browser (local Chromium)"
        echo "  2. mychrome (Chrome CDP)"
        echo "  3. Browserless API (cloud)"
        echo "  4. curl (simple HTTP)"
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
    fetch_content
}

main "$@"
