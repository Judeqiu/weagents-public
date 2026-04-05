#!/bin/bash
# chromecdp-start.sh - Launch Chrome on Xvfb virtual display (VISIBLE, port 9222)

set -e

# Configuration - FIXED to port 9222 and display :99
CHROME_USER_DATA_DIR="${CHROME_USER_DATA_DIR:-$HOME/.chromecdp-profile}"
CHROME_PORT="9222"
DISPLAY_NUM=":99"
RESOLUTION="1600x900x24"
LOG_FILE="${CHROMECDP_LOG:-/tmp/chromecdp.log}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[chromecdp]${NC} $1"; }
warn() { echo -e "${YELLOW}[chromecdp]${NC} $1"; }
error() { echo -e "${RED}[chromecdp]${NC} $1"; }

# Check if Chrome is already running on port 9222
check_existing() {
    if curl -s "http://127.0.0.1:$CHROME_PORT/json/version" > /dev/null 2>&1; then
        log "Chrome already running on port $CHROME_PORT"
        return 0
    fi
    return 1
}

# Verify Xvfb is running
check_xvfb() {
    if ! pgrep -f "Xvfb $DISPLAY_NUM" > /dev/null 2>&1; then
        error "Xvfb not running on $DISPLAY_NUM. Please start Xvfb first:"
        error "  Xvfb $DISPLAY_NUM -screen 0 $RESOLUTION -ac &"
        exit 1
    fi
    log "Xvfb detected on $DISPLAY_NUM"
}

# Kill existing Chrome instances on port 9222
kill_existing() {
    local pids=$(pgrep -f "chrome.*remote-debugging-port=$CHROME_PORT" 2>/dev/null || true)
    if [ -n "$pids" ]; then
        warn "Killing existing Chrome on port $CHROME_PORT..."
        echo "$pids" | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# Start Chrome on virtual display
start_chrome() {
    export DISPLAY="$DISPLAY_NUM"
    
    log "Starting VISIBLE Chrome on display $DISPLAY_NUM..."
    log "User data: $CHROME_USER_DATA_DIR"
    log "CDP port: $CHROME_PORT"
    
    # Ensure user data directory exists
    mkdir -p "$CHROME_USER_DATA_DIR"
    
    # Launch Chrome VISIBLE on Xvfb (NOT headless)
    nohup google-chrome \
        --no-sandbox \
        --disable-gpu \
        --disable-dev-shm-usage \
        --remote-debugging-port="$CHROME_PORT" \
        --remote-allow-origins='*' \
        --user-data-dir="$CHROME_USER_DATA_DIR" \
        --window-size=1600,900 \
        --start-maximized \
        --disable-extensions \
        --disable-background-networking \
        --disable-background-timer-throttling \
        --disable-backgrounding-occluded-windows \
        --disable-breakpad \
        --disable-component-extensions-with-background-pages \
        --disable-features=Translate,MediaRouter,InterestFeedContentSuggestions \
        --disable-features=TranslateUI \
        --disable-hang-monitor \
        --disable-ipc-flooding-protection \
        --disable-popup-blocking \
        --disable-prompt-on-repost \
        --disable-renderer-backgrounding \
        --force-color-profile=srgb \
        --metrics-recording-only \
        --no-first-run \
        --safebrowsing-disable-auto-update \
        --password-store=basic \
        --use-mock-keychain \
        --enable-features=NetworkService,NetworkServiceInProcess \
        --hide-scrollbars \
        "$@" \
        > "$LOG_FILE" 2>&1 &
    
    local chrome_pid=$!
    log "Chrome PID: $chrome_pid"
    echo "$chrome_pid" > /tmp/chromecdp.pid
    
    # Wait for Chrome to be ready
    local max_wait=30
    local waited=0
    
    while [ $waited -lt $max_wait ]; do
        if curl -s "http://127.0.0.1:$CHROME_PORT/json/version" > /dev/null 2>&1; then
            log "✅ Chrome is ready on port $CHROME_PORT (VISIBLE on display $DISPLAY_NUM)"
            curl -s "http://127.0.0.1:$CHROME_PORT/json/version" | head -3
            return 0
        fi
        sleep 1
        ((waited++))
        echo -n "."
    done
    
    error "Chrome failed to start within ${max_wait}s"
    error "Check log: $LOG_FILE"
    return 1
}

# Main execution
main() {
    log "Chrome CDP Launcher (Port 9222, Display :99)"
    
    if check_existing; then
        log "Using existing Chrome instance on port 9222"
        exit 0
    fi
    
    check_xvfb
    kill_existing
    start_chrome "$@"
}

main "$@"
