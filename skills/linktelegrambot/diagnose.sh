#!/bin/bash
# Diagnose Telegram bot group issues
# Usage: ./diagnose.sh <ssh-host>

HOST=$1

if [ -z "$HOST" ]; then
    echo "Usage: $0 <ssh-host>"
    exit 1
fi

echo "=== Telegram Bot Diagnostic for $HOST ==="

ssh "$HOST" << 'EOF'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

echo ""
echo "1. Gateway Status:"
systemctl --user is-active openclaw-gateway && echo "   ✅ Gateway is active" || echo "   ❌ Gateway is DOWN"

echo ""
echo "2. Groups Configuration:"
grep -A 15 '"groups"' ~/.openclaw/openclaw.json 2>/dev/null | head -20 || echo "   No groups config found"

echo ""
echo "3. Group Policy:"
openclaw config get channels.telegram.groupPolicy 2>/dev/null || echo "   Not set"

echo ""
echo "4. Checking for Escaped Wildcard Bug:"
if grep -q '"\\"\*\\""' ~/.openclaw/openclaw.json 2>/dev/null; then
    echo "   ❌ FOUND: Escaped wildcard key (\"\\\"*\\\"\")"
    echo "   Fix: sed -i 's/\"\\\\\\\\\"\*\\\\\\\\\"\"/\"*\"/g' ~/.openclaw/openclaw.json"
else
    echo "   ✅ Wildcard key looks correct"
fi

echo ""
echo "5. Recent Group-related Logs:"
tail -100 /tmp/openclaw/openclaw-*.log 2>/dev/null | grep -E "chatId|skipping|not-allowed|no-mention" | tail -10 || echo "   No group activity found"

echo ""
echo "6. Found Group IDs in Logs:"
grep -o '"chatId":-[0-9]*' /tmp/openclaw/openclaw-*.log 2>/dev/null | grep -o '-[0-9]*' | sort -u | while read gid; do
    echo "   Group ID: $gid"
done

echo ""
echo "7. Config Validation:"
openclaw config validate 2>&1 | head -5

echo ""
echo "=== Diagnostic Complete ==="
EOF
