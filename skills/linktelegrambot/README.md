# Link Telegram Bot Skill

Configure OpenClaw Telegram bot for group discussions and fix common issues.

## Quick Start

```bash
# Setup bot for groups
./setup-telegram-group.sh aideal

# Or with specific group ID
./setup-telegram-group.sh aideal -5207554535
```

## Diagnose Issues

```bash
./diagnose.sh aideal
```

## Common Issues Fixed

1. **Escaped Wildcard Key**: CLI creates `"\"*\""` instead of `"*"`
2. **Group Not Allowed**: Logs show `"reason":"not-allowed"`
3. **Mention Required**: Bot ignores messages without @mention
4. **Group Privacy**: BotFather setting blocks message visibility

## Files

- `SKILL.md` - Full documentation and troubleshooting guide
- `setup-telegram-group.sh` - Automated setup script
- `diagnose.sh` - Diagnostic tool for troubleshooting

## Manual Quick Fix

```bash
ssh aideal << 'FIX'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

# Enable groups
openclaw config set channels.telegram.groupPolicy "open"
openclaw config set channels.telegram.groupAllowFrom '["*"]'
openclaw config set channels.telegram.groups.'"*"'.requireMention false

# Fix escaped key bug
sed -i 's/"\\"\*\\""/"*"/g' ~/.openclaw/openclaw.json

# Restart
systemctl --user restart openclaw-gateway
FIX
```
