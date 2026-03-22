#!/bin/bash
# Fetch Content - Smart content retrieval using all available browser methods
#
# This script tries multiple browser automation methods in order:
# 1. agent-browser (local, fast, bundled Chromium)
# 2. mychrome (Chrome CDP with persistent sessions)
# 3. Browserless API (cloud fallback, always works)
# 4. Search engine fallback (when --search-fallback is enabled)
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
SEARCH_FALLBACK=false  # Use search as last resort

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
    --search-fallback     Use search engine as last resort (DuckDuckGo)
    --verbose, -v         Show detailed progress
    --help, -h            Show this help

METHODS (tried in order):
    1. agent-browser    Local bundled Chromium (fastest)
    2. mychrome         Chrome CDP (persistent sessions)
    3. browserless      Cloud API (always works)
    4. curl             Simple HTTP request
    5. search           Search engine fallback (if --search-fallback)

EXAMPLES:
    # Fetch content (auto-select best method)
    $0 --url https://example.com

    # Save to file
    $0 --url https://example.com --output /tmp/page.html

    # Force specific method
    $0 --url https://example.com --method browserless

    # Verbose with custom timeout
    $0 --url https://example.com --verbose --timeout 60

    # Use search fallback when all methods fail
    $0 --url https://example.com --search-fallback

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
            --search-fallback)
                SEARCH_FALLBACK=true
                shift
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
            rm -f "$temp_file"
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

# Method 5: Search engine fallback (last resort)
try_search_fallback() {
    echo_verbose "Trying search engine fallback..."
    
    local search_query="$URL"
    echo_verbose "Search query: $search_query"
    
    local temp_file=$(mktemp)
    local output_file=$(mktemp)
    local python_script=$(mktemp)
    
    # Try DuckDuckGo HTML
    echo_verbose "Trying DuckDuckGo..."
    local encoded_query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$search_query'))" 2>/dev/null || echo "$search_query" | tr ' ' '+')
    
    local search_success=false
    if timeout $TIMEOUT curl -s -L \
        -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
        "https://html.duckduckgo.com/html/?q=$encoded_query" > "$temp_file" 2>/dev/null; then
        
        if [ -s "$temp_file" ] && (grep -q "result__" "$temp_file" 2>/dev/null || grep -q "web-result" "$temp_file" 2>/dev/null); then
            search_success=true
            echo_verbose "DuckDuckGo search succeeded"
        fi
    fi
    
    # Write Python script to generate HTML
    cat > "$python_script" << 'PYTHON_EOF'
import re
import html as html_module
import sys
import os

temp_file = os.environ.get('_SEARCH_TEMP_FILE', '')
url = os.environ.get('_SEARCH_URL', '')
search_success = os.environ.get('_SEARCH_SUCCESS', 'false') == 'true'

results = []

if search_success and temp_file and os.path.exists(temp_file):
    try:
        with open(temp_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Parse DuckDuckGo results
        result_blocks = re.findall(r'<div class="result[^"]*"[^>]*>.*?<\/div>\s*<\/div>\s*<\/div>', content, re.DOTALL)
        
        for block in result_blocks[:10]:
            title_match = re.search(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.DOTALL)
            if title_match:
                result_url = html_module.unescape(title_match.group(1))
                title = re.sub(r'<[^>]+>', '', title_match.group(2))
                title = html_module.unescape(title).strip()
                
                snippet_match = re.search(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', block, re.DOTALL)
                snippet = ""
                if snippet_match:
                    snippet = re.sub(r'<[^>]+>', '', snippet_match.group(1))
                    snippet = html_module.unescape(snippet).strip()
                
                # Decode DuckDuckGo redirect URL
                if 'uddg=' in result_url:
                    import urllib.parse
                    try:
                        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(result_url).query)
                        if 'uddg' in parsed:
                            result_url = parsed['uddg'][0]
                    except:
                        pass
                
                if title and result_url:
                    results.append({'title': title, 'url': result_url, 'snippet': snippet})
    except Exception as e:
        pass

# Generate HTML output
print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print(f"    <title>Search Results for: {html_module.escape(url)}</title>")
print("    <meta charset='UTF-8'>")
print("    <style>")
print("        body { font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }")
print("        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 8px; margin-bottom: 30px; }")
print("        .header h1 { margin: 0 0 10px 0; font-size: 1.4em; }")
print("        .header p { margin: 5px 0; opacity: 0.9; font-size: 0.95em; word-break: break-all; }")
print("        .result { margin: 20px 0; padding: 15px; border-left: 4px solid #0066cc; background: #f8f9fa; border-radius: 0 8px 8px 0; }")
print("        .result-title { font-size: 1.1em; font-weight: 600; margin-bottom: 5px; }")
print("        .result-title a { color: #0066cc; text-decoration: none; }")
print("        .result-title a:hover { text-decoration: underline; }")
print("        .result-url { color: #006600; font-size: 0.85em; margin: 5px 0; word-break: break-all; }")
print("        .result-snippet { color: #555; margin-top: 8px; line-height: 1.5; }")
print("        .notice { background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 25px; border: 1px solid #ffc107; }")
print("        .notice.error { background: #f8d7da; border-color: #f5c6cb; }")
print("        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 0.85em; }")
print("        .search-links { margin: 20px 0; }")
print("        .search-links a { display: inline-block; margin: 5px 10px 5px 0; padding: 8px 15px; background: #0066cc; color: white; text-decoration: none; border-radius: 4px; font-size: 0.9em; }")
print("        .search-links a:hover { background: #0052a3; }")
print("        .url-box { background: #e9ecef; padding: 12px; border-radius: 4px; word-break: break-all; font-family: monospace; font-size: 0.9em; margin-top: 10px; }")
print("    </style>")
print("</head>")
print("<body>")
print("    <div class='header'>")
print("        <h1>Search Fallback Results</h1>")
print(f"        <p><strong>Original URL:</strong> {html_module.escape(url)}</p>")
print("    </div>")

if results:
    print("    <div class='notice'>")
    print("        <strong>Note:</strong> Direct access to the website failed. These are search engine results for the requested URL.")
    print("    </div>")
    print("    <div class='results'>")
    for r in results:
        print("        <div class='result'>")
        print(f"            <div class='result-title'><a href='{html_module.escape(r['url'])}' target='_blank' rel='noopener'>{html_module.escape(r['title'])}</a></div>")
        print(f"            <div class='result-url'>{html_module.escape(r['url'])}</div>")
        if r['snippet']:
            print(f"            <div class='result-snippet'>{html_module.escape(r['snippet'])}</div>")
        print("        </div>")
    print("    </div>")
else:
    print("    <div class='notice error'>")
    print("        <strong>Direct Access Failed</strong>")
    print("        <p>All browser automation methods failed to access this URL. The search engine fallback was also blocked (common for VPS/cloud IPs).</p>")
    print("    </div>")
    
    print("    <h3>Try These Alternative Ways to Access:</h3>")
    print("    <div class='search-links'>")
    encoded = html_module.escape(url)
    print(f"        <a href='https://www.google.com/search?q={encoded}' target='_blank' rel='noopener'>Google Search</a>")
    print(f"        <a href='https://webcache.googleusercontent.com/search?q=cache:{encoded}' target='_blank' rel='noopener'>Google Cache</a>")
    print(f"        <a href='https://web.archive.org/web/*/{encoded}' target='_blank' rel='noopener'>Wayback Machine</a>")
    print(f"        <a href='https://www.bing.com/search?q={encoded}' target='_blank' rel='noopener'>Bing Search</a>")
    print("    </div>")
    
    print("    <div style='margin-top: 25px;'>")
    print("        <p><strong>URL that was attempted:</strong></p>")
    print(f"        <div class='url-box'>{encoded}</div>")
    print("    </div>")

print("    <div class='footer'>")
if results:
    print(f"        <p>{len(results)} results from DuckDuckGo</p>")
else:
    print("        <p>No search results available. Try the alternative links above.</p>")
print("        <p><small>Generated by agent-browser skill • Search Fallback</small></p>")
print("    </div>")
print("</body>")
print("</html>")
PYTHON_EOF
    
    # Run Python script with environment variables
    export _SEARCH_TEMP_FILE="$temp_file"
    export _SEARCH_URL="$URL"
    export _SEARCH_SUCCESS="$search_success"
    
    if python3 "$python_script" > "$output_file" 2>/dev/null; then
        rm -f "$temp_file" "$python_script"
        
        if [ -s "$output_file" ]; then
            if [ -n "$OUTPUT" ]; then
                mv "$output_file" "$OUTPUT"
                if [ "$search_success" = true ]; then
                    echo -e "${GREEN}✓ Content saved via search fallback${NC}"
                else
                    echo -e "${YELLOW}✓ Search fallback page created (no results - alternative links provided)${NC}"
                fi
            else
                cat "$output_file"
                rm "$output_file"
            fi
            return 0
        fi
    fi
    
    rm -f "$temp_file" "$output_file" "$python_script"
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
            search)
                if try_search_fallback; then
                    success_method="search"
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
    
    if [ -z "$success_method" ] && [ "$SEARCH_FALLBACK" = true ]; then
        echo -e "${YELLOW}Trying search engine fallback...${NC}"
        if try_search_fallback; then
            success_method="search"
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
        if [ "$SEARCH_FALLBACK" = true ]; then
            echo "  5. search engine fallback"
        fi
        echo ""
        echo "Possible issues:"
        echo "  - URL is not accessible"
        echo "  - Network connectivity issues"
        echo "  - Site blocks all automation methods"
        if [ "$SEARCH_FALLBACK" = false ]; then
            echo ""
            echo "Tip: Use --search-fallback to try search engine as last resort"
        fi
        return 1
    fi
}

# Main
main() {
    parse_args "$@"
    fetch_content
}

main "$@"
