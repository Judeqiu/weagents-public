#!/bin/bash
# Fix common OpenClaw issues on remote host
# Usage: ./fix.sh <hostname> [service|browser|zombies|temp|all]

set -e

HOST="$1"
FIX_TYPE="${2:-all}"

if [ -z "$HOST" ]; then
    echo "Usage: $0 <hostname> [service|browser|zombies|temp|all]"
    echo ""
    echo "Fix types:"
    echo "  service  - Start/restart openclaw-gateway service"
    echo "  browser  - Clean duplicate agent-browser processes"
    echo "  zombies  - Kill zombie processes"
    echo "  temp     - Clean old temp directories"
    echo "  all      - Apply all fixes (default)"
    exit 1
fi

echo "🔧 OpenClaw Fix - $HOST"
echo "================================"
echo ""

# Test SSH
if ! ssh -o ConnectTimeout=5 "$HOST" "echo 'connected'" >/dev/null 2>&1; then
    echo "❌ Cannot connect to $HOST"
    exit 1
fi

ssh "$HOST" '
    FIX_TYPE="'"$FIX_TYPE"'"
    FIXES=0
    
    fix_service() {
        echo "📋 Checking service..."
        if ! systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
            echo "   Starting openclaw-gateway..."
            systemctl --user start openclaw-gateway
            sleep 3
            if systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
                echo "   ✅ Service started"
                FIXES=$((FIXES+1))
            else
                echo "   ❌ Failed to start service"
            fi
        else
            echo "   ✅ Service already running"
        fi
    }
    
    fix_browser() {
        echo "🧹 Checking agent-browser processes..."
        PIDS=$(ps aux | grep "agent-browser-linux-x64" | grep -v grep | awk '"'"'{print $2}'"'"')
        COUNT=$(echo "$PIDS" | grep -c "^[0-9]" || echo "0")
        
        if [ "$COUNT" -gt 1 ]; then
            echo "   Found $COUNT processes, cleaning duplicates..."
            NEWEST=$(echo "$PIDS" | sort -n | tail -1)
            echo "$PIDS" | grep -v "^$NEWEST$" | xargs -r kill -15 2>/dev/null
            sleep 2
            echo "$PIDS" | grep -v "^$NEWEST$" | xargs -r kill -9 2>/dev/null
            echo "   ✅ Kept PID $NEWEST"
            FIXES=$((FIXES+1))
        elif [ "$COUNT" -eq 1 ]; then
            echo "   ✅ Single instance OK"
        else
            echo "   ℹ️  No agent-browser processes found"
        fi
    }
    
    fix_zombies() {
        echo "💀 Checking zombie processes..."
        ZOMBIES=$(ps aux | grep defunct | grep -v grep | awk '"'"'{print $2}'"'"')
        if [ -n "$ZOMBIES" ]; then
            COUNT=$(echo "$ZOMBIES" | wc -l)
            echo "   Found $COUNT zombies, cleaning..."
            echo "$ZOMBIES" | xargs -r kill -9 2>/dev/null
            echo "   ✅ Cleaned"
            FIXES=$((FIXES+1))
        else
            echo "   ✅ No zombies found"
        fi
    }
    
    fix_temp() {
        echo "🗑️  Checking temp directories..."
        OLD_TEMPS=$(find /tmp -maxdepth 1 -type d -name "agent-browser-chrome-*" -mmin +60 2>/dev/null)
        if [ -n "$OLD_TEMPS" ]; then
            COUNT=$(echo "$OLD_TEMPS" | wc -l)
            echo "   Found $COUNT old directories, cleaning..."
            echo "$OLD_TEMPS" | xargs -r rm -rf 2>/dev/null
            echo "   ✅ Cleaned"
            FIXES=$((FIXES+1))
        else
            echo "   ✅ No old temp dirs found"
        fi
    }
    
    # Apply requested fixes
    case "$FIX_TYPE" in
        service)
            fix_service
            ;;
        browser)
            fix_browser
            ;;
        zombies)
            fix_zombies
            ;;
        temp)
            fix_temp
            ;;
        all)
            fix_service
            fix_browser
            fix_zombies
            fix_temp
            ;;
        *)
            echo "Unknown fix type: $FIX_TYPE"
            exit 1
            ;;
    esac
    
    echo ""
    echo "================================"
    echo "Total fixes applied: $FIXES"
'

echo ""
echo "✅ Done"
