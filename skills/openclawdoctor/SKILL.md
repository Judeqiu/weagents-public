---
name: openclawdoctor
description: Automatically triage and fix remote OpenClaw agents via SSH. Diagnoses service status, resource usage, process conflicts, and auto-remediates common issues like stopped services, competing instances, zombie processes, and disk space problems.
---

# OpenClaw Doctor 🔧

Automated health diagnosis and repair tool for remote OpenClaw agents.

## When to Use

✅ **Use this skill when:**
- Remote OpenClaw agent stops responding
- Need to check health status of multiple VMs
- Agent has performance issues or crashes
- After system reboots to ensure services are running
- Routine maintenance and health checks

❌ **Don't use for:**
- Local OpenClaw issues (use direct systemctl commands)
- Network connectivity problems outside SSH reach
- Hardware failures

## Quick Start

### Check Single Host

```bash
# Full health check with auto-fix
./skills/openclawdoctor/scripts/doctor.sh <hostname>

# Example:
./skills/openclawdoctor/scripts/doctor.sh spost
./skills/openclawdoctor/scripts/doctor.sh enraie
```

### Check Multiple Hosts

```bash
# Check all configured SSH hosts
./skills/openclawdoctor/scripts/doctor-all.sh

# Check specific list
./skills/openclawdoctor/scripts/doctor-all.sh spost enraie oraora
```

### Quick Status Check

```bash
# Just status, no fixes
ssh <hostname> "systemctl --user status openclaw-gateway --no-pager 2>&1"

# Check if process running
ssh <hostname> "ps aux | grep openclaw-gateway | grep -v grep"
```

## What It Checks

### 1. Service Status
- Is `openclaw-gateway.service` running?
- When did it start/stop?
- Auto-restart enabled?

### 2. Process Health
- Multiple competing instances?
- Zombie/defunct processes?
- Resource usage (CPU, memory)

### 3. System Resources
- Disk space (critical if < 10%)
- Memory usage
- Swap usage
- /tmp directory buildup

### 4. Browser State
- Chrome processes running?
- agent-browser instances (should be ≤ 1)
- CDP port accessibility

### 5. Network
- Gateway port listening?
- Browser control port accessible?

## Auto-Fixes Applied

| Issue | Fix | Safety |
|-------|-----|--------|
| **Service stopped** | `systemctl --user start openclaw-gateway` | ✅ Safe |
| **Multiple agent-browser** | Kill duplicates, keep newest | ✅ Safe |
| **Zombie processes** | Kill with SIGTERM/SIGKILL | ✅ Safe |
| **Old temp dirs** | Remove /tmp/agent-browser-chrome-* older than 1 hour | ✅ Safe |
| **Service disabled** | Enable auto-start (optional, with --enable) | ⚠️ Config change |

## Detailed Commands

### Full Diagnostic

```bash
ssh <hostname> '
    echo "=== OpenClaw Health Report ==="
    echo ""
    
    # 1. Service Status
    echo "📋 Service Status:"
    systemctl --user status openclaw-gateway --no-pager 2>&1 || echo "   ❌ Service not found"
    echo ""
    
    # 2. Process Count
    echo "🔢 Process Count:"
    echo "   openclaw-gateway: $(ps aux | grep "openclaw-gateway" | grep -v grep | wc -l)"
    echo "   agent-browser: $(ps aux | grep "agent-browser-linux-x64" | grep -v grep | wc -l)"
    echo "   chrome processes: $(ps aux | grep chrome | grep -v grep | wc -l)"
    echo "   zombie processes: $(ps aux | grep defunct | grep -v grep | wc -l)"
    echo ""
    
    # 3. Resources
    echo "💾 Resources:"
    free -h | grep -E "^Mem:|^Swap:"
    df -h / | tail -1 | awk '"'"'{print "   Disk: " $5 " used (" $4 " free)"}'"'"'
    echo "   Temp dirs: $(ls /tmp/agent-browser-chrome-* 2>/dev/null | wc -l)"
    echo ""
    
    # 4. Ports
    echo "🔌 Ports:"
    ss -tlnp 2>/dev/null | grep -E "3000|18789|9222|18791" || echo "   No OpenClaw ports found"
    echo ""
    
    # 5. Recent Logs
    echo "📝 Recent Errors:"
    journalctl --user -u openclaw-gateway --since "1 hour ago" --no-pager 2>/dev/null | grep -i "error\|failed\|fatal" | tail -5 || echo "   No recent errors"
'
```

### Fix Common Issues

```bash
ssh <hostname> '
    FIXED=0
    
    # Fix 1: Start service if stopped
    if ! systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
        echo "🔄 Starting openclaw-gateway..."
        systemctl --user start openclaw-gateway
        sleep 3
        if systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
            echo "   ✅ Service started"
            FIXED=$((FIXED+1))
        else
            echo "   ❌ Failed to start service"
        fi
    fi
    
    # Fix 2: Kill duplicate agent-browser processes
    AGENT_BROWSERS=$(ps aux | grep "agent-browser-linux-x64" | grep -v grep | awk '"'"'{print $2}'"'"')
    COUNT=$(echo "$AGENT_BROWSERS" | grep -c "^[0-9]")
    if [ "$COUNT" -gt 1 ]; then
        echo "🧹 Cleaning $COUNT agent-browser processes..."
        # Keep the newest (highest PID), kill others
        NEWEST=$(echo "$AGENT_BROWSERS" | sort -n | tail -1)
        echo "$AGENT_BROWSERS" | grep -v "^$NEWEST$" | xargs -r kill -15 2>/dev/null
        sleep 2
        # Force kill if still running
        echo "$AGENT_BROWSERS" | grep -v "^$NEWEST$" | xargs -r kill -9 2>/dev/null
        echo "   ✅ Kept PID $NEWEST, removed others"
        FIXED=$((FIXED+1))
    fi
    
    # Fix 3: Clean zombie processes
    ZOMBIES=$(ps aux | grep defunct | grep -v grep | awk '"'"'{print $2}'"'"')
    if [ -n "$ZOMBIES" ]; then
        echo "💀 Cleaning zombie processes..."
        echo "$ZOMBIES" | xargs -r kill -9 2>/dev/null
        echo "   ✅ Cleaned zombies"
        FIXED=$((FIXED+1))
    fi
    
    # Fix 4: Clean old temp directories
    OLD_TEMPS=$(find /tmp -maxdepth 1 -type d -name "agent-browser-chrome-*" -mmin +60 2>/dev/null)
    if [ -n "$OLD_TEMPS" ]; then
        COUNT=$(echo "$OLD_TEMPS" | wc -l)
        echo "🗑️  Cleaning $COUNT old temp directories..."
        echo "$OLD_TEMPS" | xargs -r rm -rf 2>/dev/null
        echo "   ✅ Cleaned old temp dirs"
        FIXED=$((FIXED+1))
    fi
    
    echo ""
    echo "Total fixes applied: $FIXED"
'
```

## Scripts

### doctor.sh - Single Host Diagnosis

```bash
#!/bin/bash
# skills/openclawdoctor/scripts/doctor.sh

HOST="$1"
FIX="${2:-auto}"

if [ -z "$HOST" ]; then
    echo "Usage: $0 <hostname> [auto|check-only]"
    echo ""
    echo "Examples:"
    echo "  $0 spost          # Check and auto-fix"
    echo "  $0 enraie check-only  # Check only, no fixes"
    exit 1
fi

echo "🔍 OpenClaw Doctor - Checking $HOST"
echo "=================================="
echo ""

# Test SSH connectivity
if ! ssh -o ConnectTimeout=5 "$HOST" "echo 'connected'" >/dev/null 2>&1; then
    echo "❌ Cannot connect to $HOST via SSH"
    exit 1
fi

echo "✅ SSH connection OK"
echo ""

# Run diagnostics
ssh "$HOST" '
    ISSUES=0
    WARNINGS=0
    
    check_service() {
        if systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
            STATUS=$(systemctl --user show openclaw-gateway --property=ActiveState --value)
            SINCE=$(systemctl --user show openclaw-gateway --property=ActiveEnterTimestamp --value | cut -d" " -f2-)
            echo "✅ Service: $STATUS (since $SINCE)"
            return 0
        else
            echo "❌ Service: STOPPED"
            return 1
        fi
    }
    
    check_processes() {
        GATEWAY_COUNT=$(ps aux | grep "openclaw-gateway" | grep -v grep | wc -l)
        BROWSER_COUNT=$(ps aux | grep "agent-browser-linux-x64" | grep -v grep | wc -l)
        CHROME_COUNT=$(ps aux | grep chrome | grep -v grep | wc -l)
        ZOMBIE_COUNT=$(ps aux | grep defunct | grep -v grep | wc -l)
        
        echo "📊 Processes:"
        echo "   Gateway: $GATEWAY_COUNT"
        echo "   agent-browser: $BROWSER_COUNT"
        echo "   Chrome: $CHROME_COUNT"
        echo "   Zombies: $ZOMBIE_COUNT"
        
        [ "$GATEWAY_COUNT" -eq 0 ] && ISSUES=$((ISSUES+1))
        [ "$BROWSER_COUNT" -gt 1 ] && WARNINGS=$((WARNINGS+1))
        [ "$ZOMBIE_COUNT" -gt 0 ] && WARNINGS=$((WARNINGS+1))
    }
    
    check_resources() {
        echo "💾 Resources:"
        MEM_USED=$(free | grep Mem | awk '"'"'{printf "%.0f", $3/$2 * 100}'"'"')
        DISK_USED=$(df / | tail -1 | awk '"'"'{print $5}'"'"' | sed '"'"'s/%//'"'"')
        
        echo "   Memory: ${MEM_USED}%"
        echo "   Disk: ${DISK_USED}%"
        
        [ "$MEM_USED" -gt 90 ] && ISSUES=$((ISSUES+1))
        [ "$DISK_USED" -gt 90 ] && ISSUES=$((ISSUES+1))
    }
    
    check_ports() {
        echo "🔌 Ports:"
        ss -tlnp 2>/dev/null | grep -E "3000|18789" | while read line; do
            echo "   $line"
        done
    }
    
    apply_fixes() {
        [ '"'"'$FIX'"'"' != "auto" ] && return
        
        echo ""
        echo "🔧 Applying fixes..."
        
        # Start service if stopped
        if ! systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
            echo "   🔄 Starting service..."
            systemctl --user start openclaw-gateway
            sleep 3
            if systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
                echo "   ✅ Service started"
            else
                echo "   ❌ Failed to start"
            fi
        fi
        
        # Clean duplicate agent-browser
        AGENT_PIDS=$(ps aux | grep "agent-browser-linux-x64" | grep -v grep | awk '"'"'{print $2}'"'"')
        COUNT=$(echo "$AGENT_PIDS" | grep -c "^[0-9]")
        if [ "$COUNT" -gt 1 ]; then
            echo "   🧹 Cleaning duplicate agent-browser..."
            NEWEST=$(echo "$AGENT_PIDS" | sort -n | tail -1)
            echo "$AGENT_PIDS" | grep -v "^$NEWEST$" | xargs -r kill -9 2>/dev/null
            echo "   ✅ Kept PID $NEWEST"
        fi
    }
    
    # Run checks
    check_service
    check_processes
    check_resources
    check_ports
    
    # Apply fixes if requested
    apply_fixes
    
    echo ""
    echo "=================================="
    echo "Summary: $ISSUES issues, $WARNINGS warnings"
'

echo ""
echo "✅ Check complete for $HOST"
```

### doctor-all.sh - Multiple Hosts

```bash
#!/bin/bash
# skills/openclawdoctor/scripts/doctor-all.sh

HOSTS="${@:-$(grep -E "^Host " ~/.ssh/config | grep -v "[*?]" | awk '"'"'{print $2}'"'"')}"

if [ -z "$HOSTS" ]; then
    echo "No hosts specified and no Host entries found in ~/.ssh/config"
    exit 1
fi

echo "🔍 OpenClaw Doctor - Batch Check"
echo "================================"
echo ""
echo "Hosts to check: $HOSTS"
echo ""

for HOST in $HOSTS; do
    echo "----------------------------------------"
    ./skills/openclawdoctor/scripts/doctor.sh "$HOST" auto
    echo ""
done

echo "================================"
echo "✅ All checks complete"
```

## Common Issues & Solutions

### Issue: Service Not Running

```bash
# Symptom: "Service: STOPPED"
# Fix:
ssh <hostname> "systemctl --user start openclaw-gateway"

# To auto-start on boot:
ssh <hostname> "systemctl --user enable openclaw-gateway"
```

### Issue: Multiple agent-browser Instances

```bash
# Symptom: agent-browser count > 1
# Fix: Kill all but the newest
ssh <hostname> '
    ps aux | grep "agent-browser-linux-x64" | grep -v grep | 
    awk '"'"'{print $2}'"'"' | sort -n | head -n -1 | xargs -r kill -9
'
```

### Issue: Disk Space Critical

```bash
# Symptom: Disk usage > 90%
# Fix: Clean up
ssh <hostname> '
    # Clean old temp files
    find /tmp -type f -atime +7 -delete 2>/dev/null
    # Clean old logs
    find ~/.openclaw/logs -type f -mtime +30 -delete 2>/dev/null
    # Clean package cache
    sudo apt-get clean 2>/dev/null
'
```

### Issue: WebSocket Handshake Timeouts

```bash
# Symptom: "[ws] handshake timeout" in logs
# Cause: Network issues or service overloaded
# Fix: Restart service
ssh <hostname> "systemctl --user restart openclaw-gateway"
```

## Report Generation

### Generate Health Report

```bash
ssh <hostname> '
    REPORT_FILE="/tmp/openclaw-health-$(date +%Y%m%d-%H%M%S).txt"
    
    {
        echo "OpenClaw Health Report"
        echo "Generated: $(date)"
        echo "Hostname: $(hostname)"
        echo "================================"
        echo ""
        
        echo "Service Status:"
        systemctl --user status openclaw-gateway --no-pager 2>&1
        
        echo ""
        echo "Process Summary:"
        ps aux | grep -E "openclaw|agent-browser|chrome" | grep -v grep
        
        echo ""
        echo "Resource Usage:"
        free -h
        df -h /
        
        echo ""
        echo "Recent Errors (last hour):"
        journalctl --user -u openclaw-gateway --since "1 hour ago" --no-pager 2>/dev/null | tail -20
        
    } > "$REPORT_FILE"
    
    echo "Report saved to: $REPORT_FILE"
    cat "$REPORT_FILE"
'
```

## Monitoring Integration

### Schedule Regular Checks

```bash
# Add to crontab for daily checks at 8 AM
0 8 * * * /path/to/skills/openclawdoctor/scripts/doctor-all.sh >> /var/log/openclaw-doctor.log 2>&1
```

### Alert on Issues

```bash
# Check and alert if service down
ssh <hostname> "systemctl --user is-active openclaw-gateway" || \
    echo "ALERT: OpenClaw down on <hostname>" | mail -s "OpenClaw Alert" admin@example.com
```

## Safety Notes

- ✅ **Safe operations**: Starting services, killing duplicates, cleaning temp files
- ⚠️ **Review first**: Restarting services during active sessions
- ❌ **Never**: Delete `.openclaw/` config directory or credentials
- 🔒 **Always**: Test on one host before batch operations

## Related Skills

- `ssh-vm-lister` - List available SSH hosts
- `remote-ops` - General remote operations
- `provisionclaw` - Full OpenClaw installation
