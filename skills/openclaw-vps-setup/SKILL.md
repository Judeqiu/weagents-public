---
name: openclaw-vps-setup
description: "Use when setting up OpenClaw on a new VPS or VM. Covers Node.js installation, OpenClaw CLI setup, agent workspace creation, model/token configuration, Telegram bot integration, and systemd service management. Works with Ubuntu/Debian servers."
---

# OpenClaw VPS Setup

Quickly deploy OpenClaw AI agent system on a fresh VPS or virtual machine.

## When to Use

✅ **Use this skill for:**
- Setting up OpenClaw on a new VPS (DigitalOcean, Linode, Vultr, etc.)
- Configuring OpenClaw on a development VM
- Migrating OpenClaw to a new server
- Setting up multiple OpenClaw instances
- Automating OpenClaw deployment

❌ **Don't use for:**
- Local workstation setup (use `openclaw configure` directly)
- Docker deployments (use Dockerfile instead)
- Kubernetes deployments (use Helm charts)

## Prerequisites

### VPS Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Ubuntu 20.04+ / Debian 11+ | Ubuntu 24.04 LTS |
| **RAM** | 2 GB | 4 GB+ |
| **Disk** | 20 GB | 40 GB+ |
| **CPU** | 1 core | 2+ cores |
| **Network** | Outbound HTTPS | Static IP optional |

### SSH Access

Ensure you have SSH access with key-based authentication:
```bash
ssh-copy-id user@your-vps-ip
```

Add to `~/.ssh/config`:
```
Host my-openclaw
    HostName your-vps-ip
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking accept-new
```

## Quick Start (5 Minutes)

### Step 1: Connect and Prepare

```bash
ssh my-openclaw
```

### Step 2: Run Automated Setup

```bash
# Download and run setup script
curl -fsSL https://openclaw.dev/setup-vps.sh | bash
```

Or manual setup (see Full Setup below).

### Step 3: Configure Model

```bash
export KIMI_API_KEY="your-kimi-api-key"
openclaw config set agents.defaults.model.primary "kimi-coding/k2p5"
```

### Step 4: Add Telegram (Optional)

```bash
# Add bot token to .env
echo 'TELEGRAM_BOT_TOKEN=your:bot_token' >> ~/.openclaw/.env

# Enable in config
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.botToken "your:bot_token"
```

### Step 5: Start Gateway

```bash
openclaw gateway install
systemctl --user start openclaw-gateway
```

## Full Setup Guide

### Phase 1: System Setup

#### 1.1 Install NVM (Node Version Manager)

```bash
# Install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Load NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

#### 1.2 Install Node.js 22.x

```bash
nvm install 22
nvm use 22
nvm alias default 22

# Verify
node -v  # Should show v22.x.x
npm -v
```

#### 1.3 Install pnpm

```bash
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Load pnpm
export PNPM_HOME="$HOME/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"

# Verify
pnpm -v
```

### Phase 2: OpenClaw Installation

#### 2.1 Install OpenClaw CLI

```bash
pnpm add -g openclaw

# Verify
openclaw --version
```

#### 2.2 Run Initial Setup

```bash
openclaw setup
```

This creates:
- `~/.openclaw/openclaw.json` - Main configuration
- `~/.openclaw/workspace/` - Default workspace
- `~/.openclaw/agents/main/sessions/` - Session storage

### Phase 3: Configuration

#### 3.1 Configure Gateway Mode

```bash
openclaw config set gateway.mode local
```

#### 3.2 Set Default Model

```bash
# Option A: Kimi (recommended)
openclaw config set agents.defaults.model.primary "kimi-coding/k2p5"

# Option B: Anthropic
openclaw config set agents.defaults.model.primary "anthropic/claude-3-opus-4-6"

# Option C: OpenAI
openclaw config set agents.defaults.model.primary "openai/gpt-4o"
```

#### 3.3 Add API Key

Create `~/.openclaw/.env`:
```bash
# Kimi
KIMI_API_KEY=sk-kimi-your-api-key

# Anthropic (optional)
ANTHROPIC_API_KEY=sk-ant-your-key

# OpenAI (optional)
OPENAI_API_KEY=sk-openai-your-key
```

#### 3.4 Create Auth Profile

Create `~/.openclaw/auth-profiles.json`:
```json
{
  "default": {
    "provider": "kimi-coding",
    "apiKey": "sk-kimi-your-api-key"
  }
}
```

Set permissions:
```bash
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/.env
chmod 600 ~/.openclaw/auth-profiles.json
```

### Phase 4: Custom Agent Workspace (Optional)

#### 4.1 Create Agent Directory Structure

```bash
AGENT_NAME="my-agent"
mkdir -p ~/agents/$AGENT_NAME/{workspace/memory,data/{logs,sessions,cache},.config}
```

#### 4.2 Create Core Files

Create `~/agents/$AGENT_NAME/.env`:
```bash
OPENCLAW_AGENT_NAME=$AGENT_NAME
OPENCLAW_AGENT_ID=$(date +%s)
OPENCLAW_WORKSPACE=/home/$USER/agents/$AGENT_NAME/workspace
OPENCLAW_DEFAULT_MODEL=kimi-coding/k2p5
TZ=UTC
LOG_LEVEL=info
```

Create `~/agents/$AGENT_NAME/workspace/SOUL.md`:
```markdown
# SOUL.md - Who You Are

**Name:** Agent
**Full Identifier:** Agent, OpenClaw Assistant
**Creature:** AI agent / digital employee
**Vibe:** Helpful, competent, straightforward

## Core Truths

**Be genuinely helpful, not performatively helpful.**
Skip the filler. Just help.

**Have opinions.**
You're allowed to disagree and have preferences.

**Be resourceful before asking.**
Try to figure it out first.

**Be concise.**
Respect the user's time.

## Boundaries

- Private things stay private
- No personal info leaks
- When in doubt, ask
- Destructive operations require confirmation
```

Create other core files (IDENTITY.md, USER.md, MEMORY.md, TODO.md, TOOLS.md, AGENTS.md, HEARTBEAT.md).

#### 4.3 Update OpenClaw Config

Add to `~/.openclaw/openclaw.json`:
```json
{
  "agents": {
    "list": [
      {
        "id": "my-agent",
        "workspace": "/home/ubuntu/agents/my-agent/workspace"
      }
    ]
  }
}
```

### Phase 5: Telegram Integration

#### 5.1 Create Bot via @BotFather

1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow prompts to name your bot
4. Copy the HTTP API token

#### 5.2 Configure Telegram Channel

Add to `~/.openclaw/.env`:
```bash
TELEGRAM_BOT_TOKEN=your:bot_token_here
```

Update `~/.openclaw/openclaw.json`:
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "botToken": "your:bot_token_here",
      "allowFrom": ["your_telegram_user_id"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["your_telegram_user_id"],
      "streaming": "off",
      "ackReaction": "👀"
    }
  }
}
```

**Get your Telegram User ID:**
```bash
# After messaging your bot once:
curl -s "https://api.telegram.org/bot<token>/getUpdates" | grep -o '"id":[0-9]*' | head -1
```

### Phase 6: Start Gateway

#### 6.1 Install Systemd Service

```bash
openclaw gateway install
```

This creates `~/.config/systemd/user/openclaw-gateway.service`

#### 6.2 Start Service

```bash
# IMPORTANT: Enable linger first (keeps services running after SSH logout)
sudo loginctl enable-linger $USER

# Start now
systemctl --user start openclaw-gateway

# Enable on boot
systemctl --user enable openclaw-gateway

# Check status
systemctl --user status openclaw-gateway
```

#### 6.3 Verify Installation

```bash
# Health check
openclaw health

# Full status
openclaw status

# Check model
openclaw models list
```

## Access Dashboard

### Via SSH Tunnel (Recommended)

From your local machine:
```bash
# Create tunnel
ssh -L 18789:localhost:18789 my-openclaw -N

# Get dashboard URL with token
ssh my-openclaw 'export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && export PNPM_HOME="$HOME/.local/share/pnpm" && export PATH="$PNPM_HOME:$PATH" && openclaw dashboard --no-open'

# Open in browser
open http://localhost:18789/#token=YOUR_TOKEN
```

### Via Terminal UI

```bash
ssh my-openclaw
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
export PNPM_HOME="$HOME/.local/share/pnpm" && export PATH="$PNPM_HOME:$PATH"
openclaw tui
```

## Configuration Templates

### Template: Minimal Setup

```bash
#!/bin/bash
# minimal-setup.sh - Quick OpenClaw setup

set -e

# Install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node.js 22
nvm install 22 && nvm use 22 && nvm alias default 22

# Install pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh -
export PNPM_HOME="$HOME/.local/share/pnpm" && export PATH="$PNPM_HOME:$PATH"

# Install OpenClaw
pnpm add -g openclaw

# Setup
openclaw setup
openclaw config set gateway.mode local

# Enable linger (critical for VPS stability)
sudo loginctl enable-linger $USER

# Start gateway
openclaw gateway install
systemctl --user start openclaw-gateway

echo "✓ OpenClaw installed! Run: openclaw status"
```

### Template: Full Setup with Kimi + Telegram

```bash
#!/bin/bash
# full-setup.sh - Complete OpenClaw setup

set -e

# Configuration (edit these)
KIMI_API_KEY="${KIMI_API_KEY:-your-kimi-key}"
TELEGRAM_TOKEN="${TELEGRAM_TOKEN:-your-telegram-token}"
TELEGRAM_USER_ID="${TELEGRAM_USER_ID:-your-user-id}"

# Install dependencies
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 22 && nvm use 22 && nvm alias default 22

curl -fsSL https://get.pnpm.io/install.sh | sh -
export PNPM_HOME="$HOME/.local/share/pnpm" && export PATH="$PNPM_HOME:$PATH"

# Install OpenClaw
pnpm add -g openclaw

# Setup
openclaw setup

# Configure
openclaw config set gateway.mode local
openclaw config set agents.defaults.model.primary "kimi-coding/k2p5"

# Add credentials
cat > ~/.openclaw/.env << EOF
KIMI_API_KEY=$KIMI_API_KEY
TELEGRAM_BOT_TOKEN=$TELEGRAM_TOKEN
EOF
chmod 600 ~/.openclaw/.env

# Auth profile
cat > ~/.openclaw/auth-profiles.json << EOF
{
  "default": {
    "provider": "kimi-coding",
    "apiKey": "$KIMI_API_KEY"
  }
}
EOF
chmod 600 ~/.openclaw/auth-profiles.json

# Telegram config (if token provided)
if [ -n "$TELEGRAM_TOKEN" ]; then
  openclaw config set channels.telegram.enabled true
  openclaw config set channels.telegram.botToken "$TELEGRAM_TOKEN"
  if [ -n "$TELEGRAM_USER_ID" ]; then
    openclaw config set channels.telegram.allowFrom "[$TELEGRAM_USER_ID]"
  fi
fi

# Enable linger (critical: keeps services running after SSH logout)
sudo loginctl enable-linger $USER

# Start gateway
openclaw gateway install
systemctl --user start openclaw-gateway
systemctl --user enable openclaw-gateway

echo "✓ Setup complete!"
openclaw status
```

## Troubleshooting

### Gateway Won't Start

**Symptom:** `systemctl --user status openclaw-gateway` shows failed

**Fix:**
```bash
# Check logs
journalctl --user -u openclaw-gateway -n 50

# Common issues:
# 1. gateway.mode not set
openclaw config set gateway.mode local

# 2. Port conflict
openclaw config set gateway.port 18790  # Use different port

# Restart
systemctl --user restart openclaw-gateway
```

### Node.js Version Issues

**Symptom:** `openclaw: Node.js v22.12+ is required`

**Fix:**
```bash
nvm install 22
nvm use 22
nvm alias default 22
```

### Permission Denied on Credentials

**Symptom:** Security audit shows credential warnings

**Fix:**
```bash
chmod 700 ~/.openclaw
chmod 700 ~/.openclaw/credentials
chmod 600 ~/.openclaw/.env
chmod 600 ~/.openclaw/auth-profiles.json
chmod 600 ~/.openclaw/openclaw.json
```

### Telegram Not Receiving Messages

**Symptom:** Bot shows ON but no responses

**Fix:**
```bash
# Test bot token
curl -s "https://api.telegram.org/bot<token>/getMe"

# Check allowlist
cat ~/.openclaw/openclaw.json | grep -A 5 telegram

# Ensure your user ID is in allowFrom
openclaw config get channels.telegram.allowFrom

# Restart gateway
systemctl --user restart openclaw-gateway
```

### Can't Access Dashboard

**Symptom:** `http://localhost:18789/` shows "Not Found"

**Fix:**
```bash
# Dashboard requires token in URL
openclaw dashboard --no-open
# Use the full URL with #token=...
```

### Service Keeps Restarting (Rapid Restart Loop)

**Symptom:** 
- `systemctl --user status openclaw-gateway` shows service restarting every 10-30 seconds
- Different PID every time you check
- Telegram bot stops responding intermittently
- Logs show `signal SIGTERM received` followed by clean shutdown

**Root Cause:** 
SSH connection instability causes systemd user session to cycle. When all user sessions end (due to SSH disconnect), systemd activates `exit.target` which stops all user services including `openclaw-gateway`.

**Evidence in logs:**
```bash
# Journal shows session cycling
journalctl --user -u openclaw-gateway | grep -E 'Started|Stopping'
# Mar 08 13:52:22 systemd: Stopping openclaw-gateway.service
# Mar 08 13:52:26 systemd: Started openclaw-gateway.service
# Mar 08 13:52:38 systemd: Stopping openclaw-gateway.service

# System logs show session closure
journalctl | grep 'session closed for user'
# Mar 08 13:52:22 pam_unix: session closed for user jude

# Systemd activates exit.target
journalctl --user | grep exit.target
# Mar 08 13:52:22 systemd: Activating special unit exit.target
```

**Solution:**

**Step 1: Enable Linger (Critical)**
```bash
# This allows services to keep running after logout
sudo loginctl enable-linger $USER

# Verify
loginctl show-user $USER | grep Linger
# Should show: Linger=yes
```

**Step 2: Verify Fix**
```bash
# Check service is stable (PID should remain constant)
ps aux | grep openclaw-gateway

# Monitor for 1 minute
watch -n 5 'ps aux | grep openclaw-gateway'

# Check no recent restarts
journalctl --user -u openclaw-gateway --since '5 minutes ago' | grep -c 'Started'
# Should return 1 (only initial start)
```

**Prevention:**
Always enable linger during VPS setup:
```bash
# Add to setup script
sudo loginctl enable-linger $USER
```

**Note:** This is NOT related to root vs non-root user. The issue is systemd's default behavior of stopping user services when all sessions close.

## Maintenance Commands

```bash
# Check status
openclaw status

# View logs
openclaw logs --follow
journalctl --user -u openclaw-gateway -f

# Restart gateway
systemctl --user restart openclaw-gateway

# Stop gateway
systemctl --user stop openclaw-gateway

# Update OpenClaw
pnpm update -g openclaw

# Backup config
tar czf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw

# Restore config
tar xzf openclaw-backup-YYYYMMDD.tar.gz -C ~
```

## Security Best Practices

1. **Use allowlists, not wildcards**
   ```json
   "allowFrom": ["123456789"]  // Your Telegram ID
   ```

2. **Secure credentials directory**
   ```bash
   chmod 700 ~/.openclaw/credentials
   ```

3. **Use SSH tunnel for dashboard access**
   ```bash
   ssh -L 18789:localhost:18789 my-openclaw
   ```

4. **Keep tokens in .env, not in config**
   ```bash
   # .env
   TELEGRAM_BOT_TOKEN=secret
   ```

5. **Regular backups**
   ```bash
   # Backup before updates
   cp -r ~/.openclaw ~/.openclaw.backup.$(date +%Y%m%d)
   ```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `openclaw status` | Check everything |
| `openclaw health` | Quick health check |
| `openclaw models list` | Show available models |
| `openclaw config get <key>` | Get config value |
| `openclaw config set <key> <value>` | Set config value |
| `openclaw gateway status` | Gateway service status |
| `openclaw gateway run` | Run in foreground (debug) |
| `openclaw tui` | Terminal UI |
| `openclaw dashboard` | Open web dashboard |

## Files Reference

| File | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main configuration |
| `~/.openclaw/.env` | Environment variables (secrets) |
| `~/.openclaw/auth-profiles.json` | API key profiles |
| `~/.openclaw/workspace/` | Default agent workspace |
| `~/.openclaw/credentials/` | Secure credential storage |
| `~/.openclaw/logs/` | Log files |
| `~/.config/systemd/user/openclaw-gateway.service` | Systemd service |
