---
name: linktelegrambot
description: Configure OpenClaw Telegram bot for group discussions, fix common issues like requireMention, escaped wildcard keys, and group approval. Enable bot to respond to all messages without @mentions.
---

# Link Telegram Bot Skill

Configure OpenClaw Telegram bot for group chats and fix common configuration issues.

## Quick Start

### Basic Group Setup

```bash
ssh <your-host> << 'SETUP'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

# 1. Enable groups and set open policy
openclaw config set channels.telegram.groupPolicy "open"
openclaw config set channels.telegram.groupAllowFrom '["*"]'

# 2. Disable mention requirement for all groups (CRITICAL - fixes escaped key issue)
# Note: Use sed to fix the escaped wildcard key that openclaw CLI creates
openclaw config set channels.telegram.groups.'"*"'.requireMention false 2>/dev/null || true
sed -i 's/"\\"\*\\""/"*"/g' ~/.openclaw/openclaw.json

# 3. Add your specific group ID (replace with your actual group ID)
# Get group ID from logs: grep "chatId" /tmp/openclaw/openclaw-*.log
openclaw config set channels.telegram.groups.'-YOUR_GROUP_ID'.requireMention false

# 4. Restart gateway
systemctl --user restart openclaw-gateway

echo "✅ Telegram bot configured for group discussions"
SETUP
```

## Common Issues & Fixes

### Issue 1: Bot Doesn't Respond to @Mentions in Groups

**Symptom**: Bot works in DMs but not in groups, even when @mentioned.

**Check logs**:
```bash
ssh <your-host> "grep 'not-allowed' /tmp/openclaw/openclaw-*.log | tail -5"
```

**Fix - Add specific group ID**:
```bash
ssh <your-host> << 'FIX'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

# Get group ID from logs first
GROUP_ID=$(grep -o '"chatId":-[0-9]*' /tmp/openclaw/openclaw-*.log 2>/dev/null | head -1 | grep -o '-[0-9]*')
echo "Found group ID: $GROUP_ID"

# Add the specific group
openclaw config set channels.telegram.groups."$GROUP_ID".requireMention false

# Restart
systemctl --user restart openclaw-gateway
FIX
```

### Issue 2: Escaped Wildcard Key ("\"*\"")

**Symptom**: `requireMention: false` set but bot still requires mentions. Logs show `"reason":"no-mention"`.

**Root Cause**: OpenClaw CLI creates `"\"*\""` instead of `"*"` when setting wildcard groups.

**Fix**:
```bash
ssh <your-host> << 'FIX'
# Fix the escaped wildcard key
sed -i 's/"\\"\*\\""/"*"/g' ~/.openclaw/openclaw.json

# Verify
grep -A 5 '"groups"' ~/.openclaw/openclaw.json

# Restart
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"
systemctl --user restart openclaw-gateway
FIX
```

### Issue 3: Bot Sees Messages But Doesn't Respond

**Symptom**: Logs show messages arriving but bot stays silent.

**Check**: BotFather Group Privacy setting

**Fix**:
1. Message @BotFather
2. Send `/mybots`
3. Select your bot
4. Click **Bot Settings** → **Group Privacy**
5. Choose **Turn OFF**
6. **Remove bot from group and re-add it**

### Issue 4: Group Shows "not-allowed" in Logs

**Symptom**: Logs show `{"chatId":-12345,"reason":"not-allowed"}`

**Fix**: Group isn't approved. Set `groupPolicy: open`:
```bash
openclaw config set channels.telegram.groupPolicy "open"
openclaw config set channels.telegram.groupAllowFrom '["*"]'
```

## Full Configuration Example

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",
      "botToken": "YOUR_BOT_TOKEN",
      "groups": {
        "*": {
          "requireMention": false
        },
        "-5207554535": {
          "requireMention": false
        }
      },
      "allowFrom": ["1528188341"],
      "groupAllowFrom": ["*"],
      "groupPolicy": "open",
      "streaming": "partial"
    }
  }
}
```

## Troubleshooting Commands

### Check Current Config
```bash
ssh <your-host> << 'CHECK'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

echo "=== Groups Config ==="
grep -A 15 '"groups"' ~/.openclaw/openclaw.json

echo ""
echo "=== Group Policy ==="
openclaw config get channels.telegram.groupPolicy

echo ""
echo "=== Recent Group Messages ==="
tail -100 /tmp/openclaw/openclaw-*.log 2>/dev/null | grep -E "chatId|skipping|not-allowed|no-mention" | tail -10
CHECK
```

### Monitor Real-Time Logs
```bash
ssh <your-host> "tail -f /tmp/openclaw/openclaw-\$(date +%Y-%m-%d).log 2>/dev/null | grep -E 'telegram|group|chatId|skipping'"
```

### Get Group ID from Logs
```bash
ssh <your-host> "grep -o '\"chatId\":-[0-9]*' /tmp/openclaw/openclaw-*.log 2>/dev/null | sort -u"
```

### Validate Config
```bash
ssh <your-host> << 'VALIDATE'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

# Check for escaped wildcard
if grep -q '"\\\\"\*\\\\""' ~/.openclaw/openclaw.json; then
    echo "❌ Found escaped wildcard key - run: sed -i 's/\"\\\\\\\\\"\*\\\\\\\\\"\"/\"*\"/g' ~/.openclaw/openclaw.json"
else
    echo "✅ Wildcard key looks correct"
fi

# Validate
openclaw config validate
VALIDATE
```

## Complete Setup Script

```bash
#!/bin/bash
# save as: setup-telegram-group.sh
# usage: ./setup-telegram-group.sh <ssh-host> [group-id]

HOST=$1
GROUP_ID=$2

ssh "$HOST" << EOF
export PATH="\$HOME/.local/share/fnm:\$PATH"
eval "\$(fnm env --shell bash 2>/dev/null)"

echo "=== Setting up Telegram bot for groups ==="

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
    echo "❌ Config invalid - restoring backup"
    cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json 2>/dev/null
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
EOF
```

## Important Notes

1. **Escaped Wildcard Bug**: OpenClaw CLI has a bug where `openclaw config set channels.telegram.groups.'"*"'.requireMention false` creates `"\"*\""` instead of `"*"`. Always run the sed fix after setting wildcard groups.

2. **Group Privacy**: @BotFather Group Privacy must be OFF for bot to see all messages. After changing this, remove and re-add the bot to the group.

3. **Group IDs**: Always negative numbers (e.g., `-5207554535`). Get from logs using: `grep "chatId" /tmp/openclaw/openclaw-*.log`

4. **Wildcard vs Specific**: The wildcard `"*"` should match all groups, but sometimes specific group IDs are needed. Add both for safety.

5. **Config Validation**: Always validate after changes: `openclaw config validate`

## Related Documentation

- OpenClaw Telegram Docs: https://docs.openclaw.ai/channels/telegram
- BotFather: https://t.me/BotFather
- Group ID Bot: https://t.me/getidsbot
