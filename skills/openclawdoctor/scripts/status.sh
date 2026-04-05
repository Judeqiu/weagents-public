#!/bin/bash
# Quick status check for OpenClaw on remote host
# Usage: ./status.sh <hostname>

HOST="$1"

if [ -z "$HOST" ]; then
    echo "Usage: $0 <hostname>"
    exit 1
fi

# Quick check - just the essentials
ssh "$HOST" '
    # Service status
    if systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
        STATUS="✅ Running"
        UPTIME=$(systemctl --user show openclaw-gateway --property=ActiveEnterTimestamp --value 2>/dev/null | cut -d" " -f2-)
    else
        STATUS="❌ Stopped"
        UPTIME="N/A"
    fi
    
    # Process counts
    GATEWAY=$(ps aux | grep "openclaw-gateway" | grep -v grep | wc -l)
    BROWSERS=$(ps aux | grep "agent-browser-linux-x64" | grep -v grep | wc -l)
    
    # Memory
    MEM=$(free | grep Mem | awk '"'"'{printf "%.0f%%", $3/$2 * 100}'"'"')
    
    # Quick summary
    echo "OpenClaw Status: $STATUS"
    [ "$UPTIME" != "N/A" ] && echo "Running since: $UPTIME"
    echo "Gateway processes: $GATEWAY"
    echo "Agent-browser processes: $BROWSERS"
    echo "Memory usage: $MEM"
'
