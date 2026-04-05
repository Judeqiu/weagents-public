# OpenClaw Remote Setup & Kimi Tool Calling Fix

Complete guide for setting up OpenClaw on a remote VPS, configuring SSH access, installing dependencies, fixing Kimi tool calling issues, and onboarding users.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [SSH Configuration](#ssh-configuration)
3. [VPS Environment Setup](#vps-environment-setup)
4. [OpenClaw Installation](#openclaw-installation)
5. [Kimi Tool Calling Fix](#kimi-tool-calling-fix)
6. [Model Configuration](#model-configuration)
7. [User Onboarding](#user-onboarding)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- A VPS with Ubuntu 22.04+ (or similar Linux distribution)
- Root or sudo access
- Local machine with SSH client
- GitHub account (for OpenClaw OAuth)

---

## SSH Configuration

### Step 1: Generate SSH Key (Local Machine)

If you don't have an SSH key:

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519_openclaw

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519_openclaw
```

### Step 2: Add SSH Config Entry (Local Machine)

Edit `~/.ssh/config`:

```bash
nano ~/.ssh/config
```

Add the following entry:

```
Host openclaw-vps
    HostName YOUR_VPS_IP_ADDRESS
    User your-username
    IdentityFile ~/.ssh/id_ed25519_openclaw
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

Replace:
- `YOUR_VPS_IP_ADDRESS` with your VPS IP
- `your-username` with your VPS username (e.g., `enraie`)
- Adjust `IdentityFile` path if different

### Step 3: Copy SSH Key to VPS

```bash
ssh-copy-id -i ~/.ssh/id_ed25519_openclaw.pub openclaw-vps
```

### Step 4: Test Connection

```bash
ssh openclaw-vps
```

You should log in without a password prompt.

---

## VPS Environment Setup

### Step 1: Update System

```bash
ssh openclaw-vps

# Update package list
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    tmux \
    unzip \
    build-essential \
    python3 \
    python3-pip \
    jq
```

### Step 2: Install Node.js 24 (via FNM)

```bash
# Install fnm (Fast Node Manager)
curl -fsSL https://fnm.vercel.app/install | bash

# Reload shell
source ~/.bashrc

# Install Node.js 24
fnm install 24
fnm use 24
fnm default 24

# Verify
node --version  # Should show v24.x.x
npm --version
```

### Step 3: Install OpenClaw

```bash
# Install OpenClaw globally
npm install -g openclaw@2026.3.8

# Verify installation
openclaw --version
```

### Step 4: Create OpenClaw Directory Structure

```bash
# Create directories
mkdir -p ~/.openclaw/{workspace,agents/main/sessions,logs,cron,media/inbound}

# Initialize workspace
cd ~/.openclaw/workspace
git init  # Optional: for version control
```

### Step 5: Setup Systemd Service

Create service file:

```bash
mkdir -p ~/.config/systemd/user

nano ~/.config/systemd/user/openclaw-gateway.service
```

Add content:

```ini
[Unit]
Description=OpenClaw Gateway (v2026.3.8)
After=network.target

[Service]
Type=simple
ExecStart=%h/.local/share/fnm/node-versions/v24.14.0/installation/bin/node %h/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/index.js gateway --port 18789
Restart=always
RestartSec=5
Environment=PATH=%h/.local/share/fnm/node-versions/v24.14.0/installation/bin:/usr/bin:/bin

[Install]
WantedBy=default.target
```

Enable and start:

```bash
systemctl --user daemon-reload
systemctl --user enable openclaw-gateway
```

---

## OpenClaw Initial Setup

### Step 1: Run First-Time Setup

```bash
openclaw setup
```

Or manually create config:

```bash
# Create initial config
cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "meta": {
    "lastTouchedVersion": "2026.3.8",
    "lastTouchedAt": "2026-03-12T00:00:00.000Z"
  },
  "agents": {
    "defaults": {
      "workspace": "/home/USERNAME/.openclaw/workspace",
      "model": {
        "primary": "kimi-coding/k2p5"
      },
      "models": {
        "kimi-coding/k2p5": {
          "alias": "Kimi-K2.5"
        }
      }
    },
    "list": [
      {
        "id": "main",
        "workspace": "/home/USERNAME/.openclaw/workspace"
      }
    ]
  },
  "tools": {
    "profile": "coding",
    "web": {
      "search": {
        "enabled": true,
        "provider": "kimi"
      },
      "fetch": {
        "enabled": true
      }
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "botToken": "YOUR_TELEGRAM_BOT_TOKEN",
      "allowFrom": ["*"],
      "groupAllowFrom": ["*"],
      "groupPolicy": "open"
    }
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "GENERATE_A_RANDOM_TOKEN"
    }
  }
}
EOF
```

Replace:
- `USERNAME` with your actual username
- `YOUR_TELEGRAM_BOT_TOKEN` with your bot token from @BotFather
- `GENERATE_A_RANDOM_TOKEN` with a random string (e.g., `openssl rand -hex 20`)

### Step 2: Create Auth Profiles

```bash
cat > ~/.openclaw/auth-profiles.json << 'EOF'
{
  "default": {
    "provider": "kimi-coding",
    "apiKey": "sk-kimi-YOUR_API_KEY"
  },
  "kimi-coding": {
    "provider": "kimi-coding",
    "apiKey": "sk-kimi-YOUR_API_KEY"
  }
}
EOF
```

---

## Kimi Tool Calling Fix

### Problem

When using **Kimi (kimi-coding/k2p5)** as the model, the bot cannot execute tools. The model thinks about using tools but never actually calls them.

### Root Cause

OpenClaw 2026.3.8 has a bug where the `requiresOpenAiAnthropicToolPayload: true` flag is missing from kimi-coding configuration. This flag converts tool schemas from Anthropic format to OpenAI format, which kimi-coding's API expects.

### Solution

#### Quick Fix (One-liner)

```bash
for file in ~/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/{auth-profiles-UpqQjKB-.js,config-fNYFO3AL.js,daemon-cli.js,model-selection-C8ExQCsd.js,model-selection-Dovilo6b.js,model-selection-n7SaaZtn.js}; do
  if [ -f "$file" ]; then
    sed -i 's/contextWindow: KIMI_CODING_DEFAULT_CONTEXT_WINDOW,/contextWindow: KIMI_CODING_DEFAULT_CONTEXT_WINDOW,\n\t\t\tcompat: { requiresOpenAiAnthropicToolPayload: true },/' "$file" 2>/dev/null
    echo "Patched: $(basename $file)"
  fi
done
```

#### Manual Fix

Edit these 6 files and add `compat: { requiresOpenAiAnthropicToolPayload: true },` after `contextWindow`:

1. `~/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/auth-profiles-UpqQjKB-.js`
2. `~/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/config-fNYFO3AL.js`
3. `~/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/daemon-cli.js`
4. `~/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/model-selection-C8ExQCsd.js`
5. `~/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/model-selection-Dovilo6b.js`
6. `~/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/model-selection-n7SaaZtn.js`

Find `buildKimiCodingProvider()` and ensure it has:

```javascript
function buildKimiCodingProvider() {
  return {
    baseUrl: KIMI_CODING_BASE_URL,
    api: "anthropic-messages",
    models: [{
      id: KIMI_CODING_DEFAULT_MODEL_ID,
      name: "Kimi for Coding",
      reasoning: true,
      input: ["text", "image"],
      cost: KIMI_CODING_DEFAULT_COST,
      contextWindow: KIMI_CODING_DEFAULT_CONTEXT_WINDOW,
      compat: { requiresOpenAiAnthropicToolPayload: true },  // <-- THIS LINE
      maxTokens: KIMI_CODING_DEFAULT_MAX_TOKENS,
    }]
  };
}
```

### Restart After Fix

```bash
# Restart gateway
systemctl --user restart openclaw-gateway

# Check status
systemctl --user status openclaw-gateway

# Reset sessions (recommended)
cd ~/.openclaw/agents/main/sessions
rm -f *.jsonl
cat sessions.json | jq 'with_entries(select(.key | contains("telegram:direct") | not))' > /tmp/sessions.json
mv /tmp/sessions.json sessions.json
```

---

## Model Configuration

### Adding Kimi Provider

```bash
cat > /tmp/kimi-config.json << 'EOF'
{
  "baseUrl": "https://api.kimi.com/coding",
  "api": "anthropic-messages",
  "apiKey": "sk-kimi-YOUR_API_KEY",
  "models": [
    {
      "id": "k2p5",
      "name": "Kimi for Coding",
      "reasoning": true,
      "input": ["text", "image"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 262144,
      "maxTokens": 32768
    }
  ]
}
EOF

# Merge into config
cat ~/.openclaw/openclaw.json | jq '.models.providers += {"kimi-coding": '$(cat /tmp/kimi-config.json)'}' > /tmp/oc.json
mv /tmp/oc.json ~/.openclaw/openclaw.json
```

### Adding MiniMax Provider

```bash
cat > /tmp/minimax-config.json << 'EOF'
{
  "baseUrl": "https://api.minimaxi.com/anthropic",
  "api": "anthropic-messages",
  "apiKey": "YOUR_MINIMAX_API_KEY",
  "models": [
    {
      "id": "MiniMax-M2.5",
      "name": "MiniMax M2.5",
      "reasoning": true,
      "input": ["text"],
      "cost": {
        "input": 0.3,
        "output": 1.2,
        "cacheRead": 0.03,
        "cacheWrite": 0.12
      },
      "contextWindow": 200000,
      "maxTokens": 8192
    }
  ]
}
EOF

cat ~/.openclaw/openclaw.json | jq '.models.providers += {"minimax-cn": '$(cat /tmp/minimax-config.json)'}' > /tmp/oc.json
mv /tmp/oc.json ~/.openclaw/openclaw.json
```

### Setting Default Model

```bash
# Set Kimi as default
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model.primary = "kimi-coding/k2p5"' > /tmp/oc.json
mv /tmp/oc.json ~/.openclaw/openclaw.json

# Restart
systemctl --user restart openclaw-gateway
```

---

## User Onboarding

### Step 1: Start OpenClaw Gateway

Ensure the gateway is running:

```bash
systemctl --user start openclaw-gateway
systemctl --user status openclaw-gateway
```

### Step 2: Connect via Telegram

1. Find your bot on Telegram (the one you created with @BotFather)
2. Start a conversation with `/start`
3. The bot should respond with a welcome message

### Step 3: User Commands

Users can use these commands in Telegram:

| Command | Description |
|---------|-------------|
| `/new` | Start a new session |
| `/reset` | Reset current session |
| `/model <model-id>` | Switch to a different model |
| `/status` | Check current status |
| `/help` | Show help |

**Switching Models:**
```
/model kimi-coding/k2p5      # Use Kimi (with vision)
/model minimax-cn/MiniMax-M2.5  # Use MiniMax (text only)
```

**Testing Tool Calling:**
```
what time is it?
```
Expected: Bot executes `exec date` and returns current time.

### Step 4: First-Time User Setup

For each new user, they should:

1. **Read AGENTS.md** - Type:
   ```
   read AGENTS.md
   ```

2. **Read SOUL.md** - Type:
   ```
   read SOUL.md
   ```

3. **Check available tools** - Type:
   ```
   what tools do you have?
   ```

### Step 5: OAuth Setup (Optional)

If using GitHub OAuth for authentication:

```bash
# Run doctor to setup OAuth
openclaw doctor --fix

# Follow prompts to authenticate with GitHub
```

---

## Troubleshooting

### Gateway Won't Start

```bash
# Check logs
journalctl --user -u openclaw-gateway -n 50

# Common fix: config validation
openclaw doctor --fix
```

### Bot Not Responding

```bash
# Check if gateway is running
systemctl --user status openclaw-gateway

# Check Telegram webhook/polling
journalctl --user -u openclaw-gateway | grep telegram

# Reset sessions
rm -f ~/.openclaw/agents/main/sessions/*.jsonl
```

### Tools Not Working

1. **Check model:** Ensure you're using a model that supports tools
2. **Apply Kimi fix:** Run the patch command from [Kimi Tool Calling Fix](#kimi-tool-calling-fix)
3. **Restart gateway:** `systemctl --user restart openclaw-gateway`
4. **Reset session:** `/new` or delete session files

### "Model not found" Error

```bash
# Verify config
cat ~/.openclaw/openclaw.json | jq '.models.providers | keys'

# Check auth profiles
cat ~/.openclaw/auth-profiles.json
```

### Session Issues

```bash
# Reset all sessions
rm -f ~/.openclaw/agents/main/sessions/*.jsonl
cat ~/.openclaw/agents/main/sessions/sessions.json | jq 'with_entries(select(.key | contains("telegram:direct") | not))' > /tmp/sessions.json
mv /tmp/sessions.json ~/.openclaw/agents/main/sessions/sessions.json

# Restart
systemctl --user restart openclaw-gateway
```

---

## Quick Reference

### File Locations

| File | Path |
|------|------|
| Main Config | `~/.openclaw/openclaw.json` |
| Auth Profiles | `~/.openclaw/auth-profiles.json` |
| Session Store | `~/.openclaw/agents/main/sessions/sessions.json` |
| Session Logs | `~/.openclaw/agents/main/sessions/*.jsonl` |
| OpenClaw Source | `~/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/` |
| Service File | `~/.config/systemd/user/openclaw-gateway.service` |

### Common Commands

```bash
# Start/Stop/Restart
systemctl --user start openclaw-gateway
systemctl --user stop openclaw-gateway
systemctl --user restart openclaw-gateway

# View logs
journalctl --user -u openclaw-gateway -f

# Check version
openclaw --version

# Doctor (fix config)
openclaw doctor --fix

# View config
cat ~/.openclaw/openclaw.json | jq

# Edit config
nano ~/.openclaw/openclaw.json
```

---

## References

- OpenClaw Documentation: https://docs.openclaw.io
- Kimi API Docs: https://platform.moonshot.cn/docs
- MiniMax API Docs: https://www.minimaxi.com/documentation
- Telegram BotFather: https://t.me/botfather

---

**Last Updated:** 2026-03-12
**OpenClaw Version:** 2026.3.8
**Node.js Version:** 24.x
