#!/bin/bash
# chromecdp-status.sh - Check Chrome CDP status on port 9222

CHROME_PORT="9222"
DISPLAY_NUM=":99"

echo "=== Chrome CDP Status (Port $CHROME_PORT) ==="
echo ""

# Check Xvfb
echo "Xvfb Display ($DISPLAY_NUM):"
if pgrep -f "Xvfb $DISPLAY_NUM" > /dev/null 2>&1; then
    echo "  ✅ Running"
else
    echo "  ❌ Not running"
fi
echo ""

# Check Chrome CDP on port 9222
echo "Chrome CDP (port $CHROME_PORT):"
if curl -s "http://127.0.0.1:$CHROME_PORT/json/version" > /dev/null 2>&1; then
    echo "  ✅ Running"
    echo ""
    echo "Version Info:"
    curl -s "http://127.0.0.1:$CHROME_PORT/json/version" | grep -E '"Browser"|"Protocol-Version"|"User-Agent"' | sed 's/^/  /'
else
    echo "  ❌ Not running"
fi
echo ""

# Check VNC
echo "VNC Access (port 5900):"
if pgrep -f "x11vnc.*5900" > /dev/null 2>&1; then
    echo "  ✅ Available on port 5900"
else
    echo "  ❌ Not running"
fi
echo ""

# List open tabs
echo "Open Tabs:"
if curl -s "http://127.0.0.1:$CHROME_PORT/json/list" > /dev/null 2>&1; then
    curl -s "http://127.0.0.1:$CHROME_PORT/json/list" | grep -o '"title":"[^"]*"' | head -5 | sed 's/"title":"/  - /;s/"$//'
else
    echo "  (Chrome not running)"
fi
