#!/bin/bash
# Chrome CDP Manager - Start, stop, and manage Chrome with remote debugging
#
# Usage:
#   ./chrome_manager.sh start
#   ./chrome_manager.sh stop
#   ./chrome_manager.sh status
#   ./chrome_manager.sh restart
#   ./chrome_manager.sh start --port 9223 --profile ~/.chrome-custom

set -e

# Default configuration
DEFAULT_PORT=9222
DEFAULT_PROFILE="${HOME}/.chrome-openclaw"
DEFAULT_DISPLAY=":99"
CHROME_BIN="${CHROME_BIN:-google-chrome}"
XVFB_DISPLAY="${DEFAULT_DISPLAY}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Help message
show_help() {
    cat << EOF
Chrome CDP Manager - Manage Chrome with remote debugging

Usage:
    $0 <command> [options]

Commands:
    start       Start Chrome with CDP
    stop        Stop Chrome and Xvfb
    status      Check Chrome CDP status
    restart     Restart Chrome
    version     Show Chrome version

Options:
    -p, --port PORT         CDP port (default: 9222)
    -d, --profile DIR       Chrome profile directory (default: ~/.chrome-openclaw)
    -h, --headless          Run in headless mode (no display)
    -w, --window WxH        Window size (default: 1920x1080)
    --no-sandbox            Disable sandbox (useful for Docker/containers)
    --vnc                   Start VNC server for remote viewing
    --vnc-port PORT         VNC port (default: 5900)
    --help                  Show this help

Examples:
    # Start Chrome with default settings
    $0 start

    # Start with custom port and profile
    $0 start --port 9223 --profile ~/.chrome-work

    # Start with VNC for remote viewing
    $0 start --vnc --vnc-port 5901

    # Check status
    $0 status

    # Stop Chrome
    $0 stop

Environment Variables:
    CHROME_CDP_URL      Default CDP URL for status checks
    CHROME_BIN          Chrome binary path (default: google-chrome)
EOF
}

# Log functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
parse_args() {
    PORT="${DEFAULT_PORT}"
    PROFILE="${DEFAULT_PROFILE}"
    HEADLESS=false
    WINDOW_SIZE="1920x1080"
    NO_SANDBOX=false
    START_VNC=false
    VNC_PORT=5900
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--port)
                PORT="$2"
                shift 2
                ;;
            -d|--profile)
                PROFILE="$2"
                shift 2
                ;;
            -h|--headless)
                HEADLESS=true
                shift
                ;;
            -w|--window)
                WINDOW_SIZE="$2"
                shift 2
                ;;
            --no-sandbox)
                NO_SANDBOX=true
                shift
                ;;
            --vnc)
                START_VNC=true
                shift
                ;;
            --vnc-port)
                VNC_PORT="$2"
                shift 2
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Check if Chrome is installed
check_chrome() {
    if ! command -v "$CHROME_BIN" &> /dev/null; then
        if command -v chromium-browser &> /dev/null; then
            CHROME_BIN="chromium-browser"
        elif command -v chromium &> /dev/null; then
            CHROME_BIN="chromium"
        else
            log_error "Chrome not found. Please install Google Chrome or Chromium."
            exit 1
        fi
    fi
    log_info "Using Chrome: $CHROME_BIN"
}

# Start Xvfb (virtual display)
start_xvfb() {
    if pgrep -f "Xvfb $XVFB_DISPLAY" > /dev/null; then
        log_info "Xvfb already running on $XVFB_DISPLAY"
        return
    fi
    
    log_info "Starting Xvfb on display $XVFB_DISPLAY..."
    
    # Parse window size
    WIDTH=$(echo "$WINDOW_SIZE" | cut -dx -f1)
    HEIGHT=$(echo "$WINDOW_SIZE" | cut -dx -f2)
    
    # Start Xvfb with 30-bit color for better quality
    nohup Xvfb "$XVFB_DISPLAY" -screen 0 "${WIDTH}x${HEIGHT}x30" -ac +extension GLX +render -noreset > /tmp/xvfb.log 2>&1 &
    sleep 2
    
    if pgrep -f "Xvfb $XVFB_DISPLAY" > /dev/null; then
        log_info "Xvfb started successfully"
        export DISPLAY="$XVFB_DISPLAY"
    else
        log_error "Failed to start Xvfb"
        exit 1
    fi
    
    # Start window manager
    if ! pgrep -f "openbox" > /dev/null; then
        log_info "Starting Openbox window manager..."
        nohup openbox > /tmp/openbox.log 2>&1 &
        sleep 1
    fi
}

# Start VNC server
start_vnc() {
    if pgrep -f "x11vnc.*:$VNC_PORT" > /dev/null; then
        log_info "VNC already running on port $VNC_PORT"
        return
    fi
    
    log_info "Starting VNC server on port $VNC_PORT..."
    
    # Ensure VNC password exists
    if [ ! -f ~/.vnc/passwd ]; then
        mkdir -p ~/.vnc
        log_warn "Creating default VNC password: 'openclaw'"
        echo "openclaw" | x11vnc -storepasswd - ~/.vnc/passwd 2>/dev/null || true
    fi
    
    # Parse window size for clip
    WIDTH=$(echo "$WINDOW_SIZE" | cut -dx -f1)
    HEIGHT=$(echo "$WINDOW_SIZE" | cut -dx -f2)
    
    # Start x11vnc
    nohup x11vnc -display "$XVFB_DISPLAY" -rfbport "$VNC_PORT" \
        -rfbauth ~/.vnc/passwd -forever -shared -repeat -xkb \
        -clip "${WIDTH}x${HEIGHT}+0+0" -noxinerama \
        > /tmp/x11vnc.log 2>&1 &
    
    sleep 2
    
    if pgrep -f "x11vnc.*:$VNC_PORT" > /dev/null; then
        log_info "VNC server started on port $VNC_PORT"
        log_info "Connect with: vncviewer localhost:$VNC_PORT"
    else
        log_warn "Failed to start VNC server"
    fi
}

# Start Chrome with CDP
start_chrome() {
    local port=$1
    local profile=$2
    
    # Check if already running
    if pgrep -f "remote-debugging-port=$port" > /dev/null; then
        log_warn "Chrome with CDP port $port already running"
        return
    fi
    
    log_info "Starting Chrome with CDP on port $port..."
    
    # Create profile directory if needed
    mkdir -p "$profile"
    
    # Build Chrome arguments
    local chrome_args=(
        "--remote-debugging-port=$port"
        "--user-data-dir=$profile"
        "--window-size=$WINDOW_SIZE"
        "--window-position=0,0"
        "--no-first-run"
        "--no-default-browser-check"
        "--disable-web-security"
        "--force-color-profile=srgb"
        "--enable-features=ColorCorrectRendering"
    )
    
    if [ "$NO_SANDBOX" = true ] || [ "$HEADLESS" = true ]; then
        chrome_args+=("--no-sandbox")
    fi
    
    if [ "$HEADLESS" = true ]; then
        chrome_args+=("--headless=new")
    else
        chrome_args+=("--disable-gpu")
    fi
    
    # Export display for non-headless mode
    if [ "$HEADLESS" = false ]; then
        export DISPLAY="$XVFB_DISPLAY"
    fi
    
    # Start Chrome
    nohup "$CHROME_BIN" "${chrome_args[@]}" > /tmp/chrome.log 2>&1 &
    
    # Wait for Chrome to start
    log_info "Waiting for Chrome to start..."
    for i in {1..10}; do
        sleep 1
        if curl -s "http://localhost:$port/json/version" > /dev/null 2>&1; then
            log_info "Chrome started successfully!"
            log_info "CDP endpoint: http://localhost:$port"
            return
        fi
    done
    
    log_error "Chrome failed to start within 10 seconds"
    log_error "Check /tmp/chrome.log for details"
    exit 1
}

# Stop Chrome and related services
stop_services() {
    log_info "Stopping Chrome..."
    pkill -f "remote-debugging-port" 2>/dev/null || true
    sleep 1
    
    log_info "Stopping VNC..."
    pkill -f x11vnc 2>/dev/null || true
    
    log_info "Stopping Xvfb..."
    pkill -f "Xvfb" 2>/dev/null || true
    
    log_info "Services stopped"
}

# Check Chrome CDP status
check_status() {
    local port="${1:-$DEFAULT_PORT}"
    local cdp_url="http://localhost:$port"
    
    echo "========================================="
    echo "Chrome CDP Status"
    echo "========================================="
    
    # Check Chrome process
    if pgrep -f "remote-debugging-port=$port" > /dev/null; then
        echo -e "Chrome Process: ${GREEN}Running${NC}"
    else
        echo -e "Chrome Process: ${RED}Not Running${NC}"
    fi
    
    # Check CDP endpoint
    if curl -s "$cdp_url/json/version" > /dev/null 2>&1; then
        echo -e "CDP Endpoint:   ${GREEN}Accessible${NC} ($cdp_url)"
        
        # Get version info
        local version_info
        version_info=$(curl -s "$cdp_url/json/version" 2>/dev/null | grep -o '"Browser": "[^"]*"' | cut -d'"' -f4)
        if [ -n "$version_info" ]; then
            echo "Chrome Version: $version_info"
        fi
        
        # Count open pages
        local page_count
        page_count=$(curl -s "$cdp_url/json/list" 2>/dev/null | grep -c '"id":' || echo "0")
        echo "Open Pages:     $page_count"
    else
        echo -e "CDP Endpoint:   ${RED}Not Accessible${NC}"
    fi
    
    # Check Xvfb
    if pgrep -f "Xvfb" > /dev/null; then
        echo -e "Xvfb:           ${GREEN}Running${NC}"
    else
        echo -e "Xvfb:           ${YELLOW}Not Running${NC}"
    fi
    
    # Check VNC
    if pgrep -f x11vnc > /dev/null; then
        local vnc_port
        vnc_port=$(pgrep -a x11vnc | grep -oP '(?<=-rfbport )[0-9]+' | head -1)
        echo -e "VNC Server:     ${GREEN}Running${NC} (port ${vnc_port:-5900})"
    else
        echo -e "VNC Server:     ${YELLOW}Not Running${NC}"
    fi
    
    echo "========================================="
}

# Show Chrome version
show_version() {
    check_chrome
    "$CHROME_BIN" --version
}

# Main command handler
main() {
    local command="$1"
    shift || true
    
    case "$command" in
        start)
            parse_args "$@"
            check_chrome
            if [ "$HEADLESS" = false ]; then
                start_xvfb
            fi
            start_chrome "$PORT" "$PROFILE"
            if [ "$START_VNC" = true ]; then
                start_vnc
            fi
            check_status "$PORT"
            ;;
        stop)
            stop_services
            ;;
        status)
            check_status "$@"
            ;;
        restart)
            parse_args "$@"
            stop_services
            sleep 2
            check_chrome
            if [ "$HEADLESS" = false ]; then
                start_xvfb
            fi
            start_chrome "$PORT" "$PROFILE"
            if [ "$START_VNC" = true ]; then
                start_vnc
            fi
            check_status "$PORT"
            ;;
        version)
            show_version
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
