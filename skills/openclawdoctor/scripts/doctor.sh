#!/bin/bash
# OpenClaw Doctor - Single Host Health Check and Auto-Fix
# Usage: ./doctor.sh <hostname> [auto|check-only]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="$1"
MODE="${2:-auto}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

if [ -z "$HOST" ]; then
    echo "Usage: $0 <hostname> [auto|check-only]"
    echo ""
    echo "Examples:"
    echo "  $0 spost              # Check and auto-fix"
    echo "  $0 enraie check-only  # Check only, no fixes"
    exit 1
fi

print_header() {
    echo ""
    echo "🔍 OpenClaw Doctor - Checking ${BLUE}$HOST${NC}"
    echo "=================================="
    echo ""
}

test_ssh() {
    if ! ssh -o ConnectTimeout=5 -o BatchMode=yes "$HOST" "echo 'connected'" >/dev/null 2>&1; then
        echo -e "${RED}❌ Cannot connect to $HOST via SSH${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ SSH connection OK${NC}"
    echo ""
}

run_diagnostics() {
    ssh "$HOST" '
        ISSUES=0
        WARNINGS=0
        FIXES=0
        MODE="'"$MODE"'"
        
        # Colors (for remote shell)
        R="\033[0;31m"
        G="\033[0;32m"
        Y="\033[1;33m"
        N="\033[0m"
        
        check_service() {
            echo "📋 Service Status:"
            if systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
                STATUS=$(systemctl --user show openclaw-gateway --property=ActiveState --value 2>/dev/null || echo "unknown")
                SINCE=$(systemctl --user show openclaw-gateway --property=ActiveEnterTimestamp --value 2>/dev/null | cut -d" " -f2-)
                ENABLED=$(systemctl --user is-enabled openclaw-gateway 2>/dev/null || echo "disabled")
                printf "   ${G}✅${N} Service: %s (since %s)\n" "$STATUS" "$SINCE"
                printf "   Auto-start: %s\n" "$ENABLED"
                return 0
            else
                printf "   ${R}❌${N} Service: STOPPED\n"
                ISSUES=$((ISSUES+1))
                return 1
            fi
        }
        
        check_processes() {
            echo ""
            echo "📊 Process Count:"
            GATEWAY_COUNT=$(ps aux | grep "openclaw-gateway" | grep -v grep | wc -l)
            BROWSER_COUNT=$(ps aux | grep "agent-browser-linux-x64" | grep -v grep | wc -l)
            CHROME_COUNT=$(ps aux | grep chrome | grep -v grep | wc -l)
            ZOMBIE_COUNT=$(ps aux | grep defunct | grep -v grep | wc -l)
            
            printf "   Gateway:      %d\n" "$GATEWAY_COUNT"
            printf "   agent-browser: %d" "$BROWSER_COUNT"
            [ "$BROWSER_COUNT" -gt 1 ] && printf " ${Y}⚠️ Multiple instances${N}" && WARNINGS=$((WARNINGS+1))
            printf "\n"
            
            printf "   Chrome:       %d\n" "$CHROME_COUNT"
            printf "   Zombies:      %d" "$ZOMBIE_COUNT"
            [ "$ZOMBIE_COUNT" -gt 0 ] && printf " ${Y}⚠️ Found zombies${N}" && WARNINGS=$((WARNINGS+1))
            printf "\n"
            
            if [ "$GATEWAY_COUNT" -eq 0 ]; then
                printf "   ${R}❌${N} No gateway process found\n"
            fi
        }
        
        check_resources() {
            echo ""
            echo "💾 Resources:"
            
            # Memory
            MEM_INFO=$(free | grep Mem)
            MEM_TOTAL=$(echo "$MEM_INFO" | awk '"'"'{print $2}'"'"')
            MEM_USED=$(echo "$MEM_INFO" | awk '"'"'{print $3}'"'"')
            MEM_PCT=$((MEM_USED * 100 / MEM_TOTAL))
            
            MEM_COLOR="$G"
            [ "$MEM_PCT" -gt 80 ] && MEM_COLOR="$Y" && WARNINGS=$((WARNINGS+1))
            [ "$MEM_PCT" -gt 90 ] && MEM_COLOR="$R" && ISSUES=$((ISSUES+1))
            printf "   Memory: ${MEM_COLOR}%d%%${N} used (%s / %s)\n" "$MEM_PCT" "$(echo $MEM_INFO | awk '"'"'{printf "%.1fG", $3/1024/1024}'"'"')" "$(echo $MEM_INFO | awk '"'"'{printf "%.1fG", $2/1024/1024}'"'"')"
            
            # Disk
            DISK_INFO=$(df / | tail -1)
            DISK_PCT=$(echo "$DISK_INFO" | awk '"'"'{print $5}'"'"' | sed '"'"'s/%//'"'"')
            DISK_AVAIL=$(echo "$DISK_INFO" | awk '"'"'{print $4}'"'"')
            
            DISK_COLOR="$G"
            [ "$DISK_PCT" -gt 80 ] && DISK_COLOR="$Y" && WARNINGS=$((WARNINGS+1))
            [ "$DISK_PCT" -gt 90 ] && DISK_COLOR="$R" && ISSUES=$((ISSUES+1))
            printf "   Disk:   ${DISK_COLOR}%d%%${N} used (%s free)\n" "$DISK_PCT" "$(echo $DISK_AVAIL | awk '"'"'{printf "%.1fG", $1/1024/1024}'"'"')"
            
            # Temp directories
            TEMP_COUNT=$(ls /tmp/agent-browser-chrome-* 2>/dev/null | wc -l)
            printf "   Temp dirs: %d" "$TEMP_COUNT"
            [ "$TEMP_COUNT" -gt 50 ] && printf " ${Y}⚠️ High count${N}" && WARNINGS=$((WARNINGS+1))
            printf "\n"
        }
        
        check_ports() {
            echo ""
            echo "🔌 Network Ports:"
            PORTS=$(ss -tlnp 2>/dev/null | grep -E "openclaw|chrome" || true)
            if [ -n "$PORTS" ]; then
                echo "$PORTS" | while read line; do
                    printf "   %s\n" "$line"
                done
            else
                printf "   ${Y}⚠️ No OpenClaw ports found${N}\n"
            fi
        }
        
        check_logs() {
            echo ""
            echo "📝 Recent Activity (last 10 min):"
            RECENT_LOGS=$(journalctl --user -u openclaw-gateway --since "10 minutes ago" --no-pager 2>/dev/null | tail -10 || echo "No logs available")
            if [ -n "$RECENT_LOGS" ]; then
                echo "$RECENT_LOGS" | while read line; do
                    # Highlight errors
                    if echo "$line" | grep -qi "error\|failed\|fatal"; then
                        printf "   ${R}%s${N}\n" "$line"
                    elif echo "$line" | grep -qi "warn"; then
                        printf "   ${Y}%s${N}\n" "$line"
                    else
                        printf "   %s\n" "$line"
                    fi
                done
            fi
        }
        
        apply_fixes() {
            [ "$MODE" != "auto" ] && return
            
            echo ""
            echo "🔧 Applying Auto-Fixes..."
            
            # Fix 1: Start service if stopped
            if ! systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
                printf "   🔄 Starting openclaw-gateway...\n"
                if systemctl --user start openclaw-gateway 2>/dev/null; then
                    sleep 3
                    if systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
                        printf "   ${G}✅ Service started${N}\n"
                        FIXES=$((FIXES+1))
                    else
                        printf "   ${R}❌ Service failed to start${N}\n"
                    fi
                else
                    printf "   ${R}❌ Failed to start service${N}\n"
                fi
            fi
            
            # Fix 2: Kill duplicate agent-browser processes
            AGENT_PIDS=$(ps aux | grep "agent-browser-linux-x64" | grep -v grep | awk '"'"'{print $2}'"'"')
            COUNT=$(echo "$AGENT_PIDS" | grep -c "^[0-9]" || echo "0")
            if [ "$COUNT" -gt 1 ]; then
                printf "   🧹 Cleaning %d agent-browser processes...\n" "$COUNT"
                NEWEST=$(echo "$AGENT_PIDS" | sort -n | tail -1)
                # Try graceful kill first
                echo "$AGENT_PIDS" | grep -v "^$NEWEST$" | xargs -r kill -15 2>/dev/null
                sleep 2
                # Force kill if still running
                REMAINING=$(ps aux | grep "agent-browser-linux-x64" | grep -v grep | awk '"'"'{print $2}'"'"' | grep -v "^$NEWEST$")
                if [ -n "$REMAINING" ]; then
                    echo "$REMAINING" | xargs -r kill -9 2>/dev/null
                fi
                printf "   ${G}✅ Kept PID %s, removed others${N}\n" "$NEWEST"
                FIXES=$((FIXES+1))
            fi
            
            # Fix 3: Clean zombie processes
            ZOMBIES=$(ps aux | grep defunct | grep -v grep | awk '"'"'{print $2}'"'"')
            if [ -n "$ZOMBIES" ]; then
                ZOMBIE_COUNT=$(echo "$ZOMBIES" | wc -l)
                printf "   💀 Cleaning %d zombie processes...\n" "$ZOMBIE_COUNT"
                echo "$ZOMBIES" | xargs -r kill -9 2>/dev/null
                printf "   ${G}✅ Zombies cleaned${N}\n"
                FIXES=$((FIXES+1))
            fi
            
            # Fix 4: Clean old temp directories
            OLD_TEMPS=$(find /tmp -maxdepth 1 -type d -name "agent-browser-chrome-*" -mmin +60 2>/dev/null)
            if [ -n "$OLD_TEMPS" ]; then
                TEMP_COUNT=$(echo "$OLD_TEMPS" | wc -l)
                printf "   🗑️  Cleaning %d old temp directories...\n" "$TEMP_COUNT"
                echo "$OLD_TEMPS" | xargs -r rm -rf 2>/dev/null
                printf "   ${G}✅ Old temp dirs cleaned${N}\n"
                FIXES=$((FIXES+1))
            fi
            
            printf "\n   Total fixes applied: ${G}%d${N}\n" "$FIXES"
        }
        
        # Run all checks
        check_service
        check_processes
        check_resources
        check_ports
        check_logs
        
        # Apply fixes
        apply_fixes
        
        # Summary
        echo ""
        echo "=================================="
        if [ "$ISSUES" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
            printf "${G}✅ Healthy - No issues found${N}\n"
        elif [ "$ISSUES" -eq 0 ]; then
            printf "${Y}⚠️  $WARNINGS warning(s)${N}\n"
        else
            printf "${R}❌ $ISSUES issue(s), $WARNINGS warning(s)${N}\n"
        fi
    '
}

# Main
print_header
test_ssh
run_diagnostics

echo ""
echo -e "${GREEN}✅ Check complete for $HOST${NC}"
