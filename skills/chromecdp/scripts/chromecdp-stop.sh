#!/bin/bash
# chromecdp-stop.sh - Stop Chrome CDP instance on port 9222

set -e

CHROME_PORT="9222"
PID_FILE="/tmp/chromecdp.pid"

echo "[chromecdp] Stopping Chrome on port $CHROME_PORT..."

# Kill by PID file if exists
if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
        echo "[chromecdp] Killing Chrome PID: $pid"
        kill -9 "$pid" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
fi

# Kill any remaining Chrome instances on port 9222
pkill -f "chrome.*remote-debugging-port=$CHROME_PORT" 2>/dev/null || true

echo "[chromecdp] ✅ Chrome stopped on port 9222"
