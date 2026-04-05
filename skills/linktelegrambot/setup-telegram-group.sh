#!/bin/bash
# Setup Telegram bot for group discussions
# Usage: ./setup-telegram-group.sh <ssh-host> [group-id]

set -e

HOST=$1
GROUP_ID=$2

if [ -z "$HOST" ]; then
    echo "Usage: $0 <ssh-host> [group-id]"
    echo "Example: $0 aideal -5207554535"
    exit 1
fi

ssh "$HOST" << EOF
export PATH="\$HOME/.local/share/fnm:\$PATH"
eval "\$(fnm env --shell bash 2>/dev/null)"

echo "=== Setting up Telegram bot for groups ==="

# Backup config
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.pre-telegram-fix 2>/dev/null || true

# Enable groups
openclaw config set channels.telegram.groupPolicy "open"
openclaw config set channels.telegram.groupAllowFrom '["*"]'

# Set wildcard requireMention (this creates escaped key, we'll fix it)
openclaw config set channels.telegram.groups.'"*"'.requireMention false 2>/dev/null || true

# Fix escaped wildcard key
sed -i 's/"\\\\"\*\\\\""/"*"/g' ~/.openclaw/openclaw.json

# Add specific group if provided
if [ -n "$GROUP_ID" ]; then
    openclaw config set channels.telegram.groups.'$GROUP_ID'.requireMention false
    echo "✅ Added group $GROUP_ID"
fi

# Validate
if openclaw config validate > /dev/null 2>&1; then
    echo "✅ Config valid"
else
    echo "❌ Config invalid - check manually"
    exit 1
fi

# Restart
systemctl --user restart openclaw-gateway
sleep 3

# Check status
if systemctl --user is-active openclaw-gateway > /dev/null; then
    echo "✅ Gateway active"
else
    echo "❌ Gateway failed to start"
    exit 1
fi

echo ""
echo "=== Current Groups Config ==="
grep -A 10 '"groups"' ~/.openclaw/openclaw.json | head -15

echo ""
echo "=== Setup Complete ==="
echo "Bot should now respond to all messages in allowed groups"
echo ""
echo "Troubleshooting:"
echo "  - Check logs: tail -f /tmp/openclaw/openclaw-\$(date +%Y-%m-%d).log"
echo "  - Get group IDs: grep -o '\"chatId\":-[0-9]*' /tmp/openclaw/openclaw-*.log | sort -u"
EOF
