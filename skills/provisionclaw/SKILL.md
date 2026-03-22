---
name: provisionclaw
description: Complete OpenClaw (龙虾) setup from scratch on any Ubuntu system. Includes SSH config, system prep, Node.js, OpenClaw installation, model configuration, channels (Telegram) with super user security model, Chrome browser, memory configuration, skill discovery for ~/.openclaw/workspace/skills/, and workspace initialization.
---

# ProvisionClaw - Complete OpenClaw Setup

Build a fully functional OpenClaw AI agent from scratch on Ubuntu.

## What's Included

| Component | Purpose |
|-----------|---------|
| SSH Setup | Passwordless, secure remote access |
| System Prep | Swap, updates, dependencies |
| Node.js v24 | Runtime environment |
| OpenClaw Core | Gateway and daemon |
| Chrome Browser | For browser automation |
| Virtual Display | Xvfb headless display |
| VNC Desktop | Visual access to Chrome (optional) |
| Model Config | LLM provider setup (MiniMax, Kimi, etc.) |
| **Telegram Security** | **Super user (1528188341) + pairing approval model** |
| Skills | Pre-install common skills |
| Workspace | SOUL.md, AGENTS.md initialization |
| Server Profile | Auto-generated documentation |

## Security Model (Locked In)

**All OpenClaw servers provisioned by this skill use the following security model:**

| Setting | Value | Description |
|---------|-------|-------------|
| **Super User** | `1528188341` | Pre-approved Telegram user ID |
| **DM Policy** | `pairing` | New users require approval |
| **New User Access** | Approval required | Must be approved by super user |
| **Group Access** | `allowlist` | Disabled by default |

This security model ensures only authorized users can access the bot.

## Prerequisites

- Ubuntu 20.04/22.04/24.04+ (VPS, VM, local, or WSL)
- sudo privileges
- Internet access
- For Telegram: Bot token from @BotFather
- For VNC: Port 5900 accessible (or use SSH tunnel)

---

## Phase 1: SSH Setup (Local Machine)

Run these on your local machine first:

```bash
# 1. Generate SSH key
ssh-keygen -t ed25519 -C "openclaw-vps" -f ~/.ssh/id_ed25519_openclaw

# 2. Copy to VPS (run after VPS is created)
ssh-copy-id -i ~/.ssh/id_ed25519_openclaw.pub ubuntu@YOUR_VPS_IP

# 3. Add to SSH config
cat >> ~/.ssh/config << 'EOF'
Host openclaw
    HostName YOUR_VPS_IP
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519_openclaw
    StrictHostKeyChecking accept-new
EOF
chmod 600 ~/.ssh/config

# 4. Test
ssh openclaw
```

---

## Phase 2: System Installation (VPS)

### Option A: One-Liner Complete Install

```bash
ssh openclaw << 'INSTALL'
#!/bin/bash
set -e

echo "=== OpenClaw Complete Setup ==="

# 1. System update
echo "[1/7] System update..."
sudo apt update -y
sudo apt install -y unzip curl wget git

# 2. Swap (8GB)
echo "[2/7] Setting up swap..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 8G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# 3. Node.js v24 via fnm
echo "[3/7] Installing Node.js..."
if ! command -v fnm &> /dev/null; then
    curl -fsSL https://fnm.vercel.app/install | bash
    export PATH="$HOME/.local/share/fnm:$PATH"
    eval "$(fnm env)"
fi
fnm install 24
fnm use 24
fnm default 24

# 4. Chrome for browser automation (Ubuntu 22.04/24.04/25.04 compatible)
echo "[4/7] Installing Chrome..."
if ! command -v google-chrome &> /dev/null; then
    # Modern method for Ubuntu 22.04+ (apt-key is deprecated in 24.04+, removed in 25.04)
    sudo mkdir -p /etc/apt/keyrings
    wget -qO- https://dl.google.com/linux/linux_signing_key.pub | sudo tee /etc/apt/keyrings/google-chrome.asc > /dev/null
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.asc] http://dl.google.com/linux/chrome/deb stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
    sudo apt update
    sudo apt install -y google-chrome-stable
fi

# 5. Virtual display for headless Chrome
echo "[5/7] Installing virtual display..."
sudo apt install -y xvfb openbox x11vnc xdotool

# 6. OpenClaw
echo "[6/7] Installing OpenClaw..."
npm install -g openclaw@latest

# 6.5 Configure Telegram with secure defaults (super user: 1528188341)
echo "[6.5/7] Setting up Telegram security model..."
mkdir -p ~/.openclaw
cat > ~/.openclaw/openclaw.json << 'OCEOF'
{
  "models": {
    "mode": "merge",
    "providers": {}
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai/gpt-4o"
      }
    }
  },
  "channels": {
    "telegram": {
      "enabled": false,
      "dmPolicy": "pairing",
      "allowFrom": ["1528188341"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": []
    }
  },
  "gateway": {
    "port": 3000,
    "mode": "local"
  }
}
OCEOF

echo "✓ Telegram security model configured"
echo "✓ Gateway mode set to local"
echo "  - Super User: 1528188341 (pre-approved)"
echo "  - New users: Require pairing approval"
echo "  - Groups: Disabled by default"

# 7. Start services with proper color support
echo "[7/7] Starting Chrome with CDP..."
export DISPLAY=:99

# Start Xvfb with 24-bit color
Xvfb :99 -screen 0 1920x1080x24 -ac &
sleep 2

# Start openbox window manager for proper rendering
openbox &
sleep 1

# Start Chrome with CDP and all recommended flags
google-chrome --no-sandbox --disable-gpu \
    --remote-debugging-port=9222 \
    --user-data-dir=$HOME/.chrome-openclaw \
    --window-size=1920,1080 \
    --window-position=0,0 \
    --disable-web-security \
    --no-first-run \
    --no-default-browser-check &
sleep 5

# Resize Chrome to fill screen
for win in $(xdotool search --class "google-chrome" 2>/dev/null); do
    xdotool windowsize "$win" 1920 1080 2>/dev/null || true
    xdotool windowmove "$win" 0 0 2>/dev/null || true
done

echo ""
echo "=== Installation Complete ==="
echo "Node: $(node -v)"
echo "OpenClaw: $(openclaw --version)"
echo "Chrome: $(google-chrome --version)"
echo ""
echo "Services:"
echo "  - Chrome CDP: http://127.0.0.1:9222"
echo "  - VNC Desktop: port 5900 (password: openclaw123)"
echo ""
echo "Next:"
echo "  1. Run 'openclaw onboard --install-daemon' to configure"
echo "  2. Run '~/start-vnc.sh' to start VNC access"
INSTALL
```

### Option B: Step-by-Step

```bash
ssh openclaw

# Then run each step manually from sections below
```

---

## Phase 3: OpenClaw Configuration

### Step 1: Initial Onboarding

```bash
ssh openclaw
openclaw onboard --install-daemon
```

**Interactive prompts:**
1. **Select provider**: Choose your LLM (MiniMax, OpenAI, etc.)
2. **Authentication**: OAuth (recommended) or API key
3. **Daemon**: Confirm systemd service installation

### Step 2: Configure Models

Edit `~/.openclaw/openclaw.json`:

```bash
ssh openclaw
nano ~/.openclaw/openclaw.json
```

**Example configuration for MiniMax:**
```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "minimax-cn": {
        "baseUrl": "https://api.minimaxi.com/anthropic",
        "apiKey": "YOUR_API_KEY",
        "api": "anthropic-messages",
        "authHeader": true,
        "models": [{
          "id": "MiniMax-M2.5",
          "name": "MiniMax M2.5",
          "reasoning": true,
          "input": ["text", "image"],
          "cost": {"input": 0.3, "output": 1.2},
          "contextWindow": 200000,
          "maxTokens": 8192
        }]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "minimax-cn/MiniMax-M2.5"
      }
    }
  }
}
```

### Step 3: Configure Telegram

#### Security Model (Super User + Pairing)

By default, this skill configures Telegram with a **secure approval-based model**:

| Setting | Value | Purpose |
|---------|-------|---------|
| **Super User** | `1528188341` | Pre-approved, can use bot immediately |
| **New Users** | Require approval | Must be approved by super user |
| **DM Policy** | `pairing` | Approval required for new users |
| **Group Policy** | `allowlist` | Groups must be explicitly allowed |

#### Option A: Secure Setup (Default)

```bash
ssh openclaw << 'TELEGRAM_SECURE'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

# Configure Telegram with super user (1528188341) and pairing mode
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.botToken "YOUR_BOT_TOKEN_FROM_BOTFATHER"
openclaw config set channels.telegram.dmPolicy pairing
openclaw config set channels.telegram.allowFrom '["1528188341"]'
openclaw config set channels.telegram.groupPolicy allowlist
openclaw config set channels.telegram.groupAllowFrom '[]'

# Restart gateway to apply
systemctl --user restart openclaw-gateway

echo "✓ Telegram configured with secure pairing mode"
echo "✓ Super User (1528188341) is pre-approved"
echo "✓ New users require approval via pairing"
TELEGRAM_SECURE
```

#### How Pairing Works

1. **New user** messages the bot → Bot replies: "Request sent to admin for approval"
2. **Super user** (1528188341) receives approval notification
3. **Super user approves** → New user can now chat with bot
4. **Or super user denies** → New user is blocked

#### Option B: Open Access (Not Recommended)

Only use this if you want anyone to use the bot:

```bash
ssh openclaw << 'TELEGRAM_OPEN'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

openclaw config set channels.telegram.dmPolicy open
openclaw config set channels.telegram.allowFrom '["*"]'
systemctl --user restart openclaw-gateway

echo "⚠️  WARNING: Bot is now open to all users"
TELEGRAM_OPEN
```

#### Managing User Approvals

**Approve a new user:**
```bash
ssh openclaw 'export PATH="$HOME/.local/share/fnm:$PATH"; eval "$(fnm env --shell bash 2>/dev/null)"; openclaw directory add --channel telegram --id USER_ID'
```

**List approved users:**
```bash
ssh openclaw 'export PATH="$HOME/.local/share/fnm:$PATH"; eval "$(fnm env --shell bash 2>/dev/null)"; openclaw directory list --channel telegram'
```

**Remove a user:**
```bash
ssh openclaw 'export PATH="$HOME/.local/share/fnm:$PATH"; eval "$(fnm env --shell bash 2>/dev/null)"; openclaw directory remove --channel telegram --id USER_ID'
```

---

## Phase 4: Workspace Setup

### Create Essential Files

```bash
ssh openclaw << 'WORKSPACE'
# Create workspace directory structure
mkdir -p ~/.openclaw/workspace/{skills,memory}

# Create SOUL.md (bot personality)
cat > ~/.openclaw/workspace/SOUL.md << 'EOF'
# SOUL.md - Who You Are

## Core Identity
You are a helpful AI assistant running on OpenClaw.

## Critical Rules

### Tool Usage
- NEVER output raw function calls like exec({"command": "..."})
- Use tools silently through the native tool calling system
- Return only natural language responses

### Response Format
- Be concise and helpful
- Skip filler phrases like "I'd be happy to help"
- Take action, then report results

## Capabilities
You have access to:
- File system (read, write, edit)
- Command execution (exec)
- Web browsing
- Memory storage

Use them responsibly.
EOF

# Create AGENTS.md (workspace rules)
cat > ~/.openclaw/workspace/AGENTS.md << 'EOF'
# AGENTS.md - Workspace Rules

## Session Startup (CRITICAL - READ EVERY TIME)
At the start of EVERY session, you MUST read these files in order:
1. **SOUL.md** - Your identity and personality
2. **MEMORY.md** - Skill discovery protocol and long-term memory (READ THIS!)
3. **USER.md** - User preferences (if exists)
4. Recent memory/memory/YYYY-MM-DD.md files

## Tool Usage
- exec: Use for system commands
- read: Check file contents
- write: Create new files
- edit: Modify existing files
- search: Find files and content

## Memory System
- **Daily notes**: Store in `memory/YYYY-MM-DD.md`
- **Long-term**: Update `MEMORY.md` with important insights
- **Conversations**: Reference memory before responding

## ⚠️ CRITICAL: Skill Discovery Protocol

### The Problem
`<available_skills>` context is INCOMPLETE! It only shows bundled skills.
Many skills are installed in `~/.openclaw/workspace/skills/` and will NOT appear in `<available_skills>`.

### The Solution
**ALWAYS run `openclaw skills list` before using skills!**

This command shows ALL skills including:
- `openclaw-bundled` - Built-in skills
- `openclaw-extra` - Skills from `~/.openclaw/workspace/skills/`
- `openclaw-workspace` - Agent-specific workspace skills

### Skill Locations Reference
| Location | Description | Example |
|----------|-------------|---------|
| `~/.openclaw/workspace/skills/` | Main workspace skills directory | customer-research-agent, mychrome |
| `~/.config/agents/skills/` | System-wide user skills | (varies by system) |

### Before Using Any Skill
1. Run: `openclaw skills list`
2. Find the skill name and its source
3. If skill is in `~/.openclaw/workspace/skills/`, use it directly
4. Never say "skill doesn't exist" without checking `openclaw skills list`

## Chrome/CDP Skills
Common Chrome-based automation skills in workspace:
- `customer-research-agent` - B2B customer research
- `mychrome` - Chrome CDP bridge/helper
- `lazada-browser` - Lazada Seller Center automation
- `shopee-seller` - Shopee Seller Centre automation

EOF

# Create USER.md template
cat > ~/.openclaw/workspace/USER.md << 'EOF'
# USER.md - User Preferences

## Identity
Name: [Your name]

## Preferences
- Communication style: [concise/detailed]
- Notification preferences: [when to alert]

## Important Info
- [Add any context the bot should remember]
EOF

echo "Workspace files created!"
WORKSPACE
```

---

## Phase 4.5: Memory Configuration (CRITICAL)

Properly configure agent memory so OpenClaw remembers important information across sessions.

### Why Memory is Important

Without memory configuration:
- Agent forgets user preferences between sessions
- Agent doesn't know about custom skills in workspace
- Agent repeats mistakes
- Agent can't maintain context

### Step 1: Create Memory Directory Structure

```bash
ssh openclaw << 'MEMORY_SETUP'
#!/bin/bash

echo "=== Setting up Agent Memory ==="

# Create memory directories
mkdir -p ~/.openclaw/workspace/memory/{daily,context,skills}

# Create memory index
cat > ~/.openclaw/workspace/memory/INDEX.md << 'EOF'
# Memory Index

## Directory Structure
- `daily/` - Daily conversation notes (YYYY-MM-DD.md)
- `context/` - Session context and user preferences
- `skills/` - Skill-specific learned behaviors

## How to Use Memory
1. Read INDEX.md at session start
2. Check today's daily file for recent context
3. Reference context/ for user preferences
4. Update skills/ when learning new skill behaviors
EOF

# Create today's memory file
today=$(date +%Y-%m-%d)
cat > ~/.openclaw/workspace/memory/daily/${today}.md << EOF
# Memory for ${today}

## Session Start
- Date: ${today}
- Setup completed: ProvisionClaw

## Skills Available
Run \`openclaw skills list\` to see all skills.
Workspace skills location: ~/.openclaw/workspace/skills/

## Notes
(Add session notes here)
EOF

# Create user context template
cat > ~/.openclaw/workspace/memory/context/user_preferences.md << 'EOF'
# User Preferences

## Communication Style
- Preferred tone: [professional/casual/concise]
- Detail level: [high/medium/low]
- Language: [English/Chinese/etc]

## Notification Preferences
- When to alert: [errors only/important updates/all actions]
- Preferred channel: [Telegram/email/none]

## Important Context
- User timezone: 
- Business type: 
- Key priorities: 

## Skill Usage Patterns
- Frequently used skills: 
- Custom workflows: 
EOF

echo "✓ Memory structure created"
echo "  - ~/.openclaw/workspace/memory/INDEX.md"
echo "  - ~/.openclaw/workspace/memory/daily/${today}.md"
echo "  - ~/.openclaw/workspace/memory/context/user_preferences.md"
MEMORY_SETUP
```

### Step 2: Verify Memory is Working

```bash
ssh openclaw << 'MEMORY_VERIFY'
#!/bin/bash

echo "=== Verifying Memory Setup ==="

# Check memory files exist
echo "Memory files:"
ls -la ~/.openclaw/workspace/memory/ 2>/dev/null || echo "  (memory directory missing)"

# Check daily files
echo ""
echo "Daily memory files:"
ls ~/.openclaw/workspace/memory/daily/ 2>/dev/null | head -5 || echo "  (daily directory missing)"

# Verify memory is readable
echo ""
if [ -f ~/.openclaw/workspace/memory/INDEX.md ]; then
    echo "✓ INDEX.md exists"
else
    echo "✗ INDEX.md missing"
fi

if [ -f ~/.openclaw/workspace/MEMORY.md ]; then
    echo "✓ MEMORY.md exists (skill discovery protocol)"
else
    echo "✗ MEMORY.md missing - Run Phase 5.5!"
fi

# Check AGENTS.md references memory
echo ""
if grep -q "MEMORY.md" ~/.openclaw/workspace/AGENTS.md 2>/dev/null; then
    echo "✓ AGENTS.md references MEMORY.md"
else
    echo "✗ AGENTS.md doesn't reference MEMORY.md"
fi

MEMORY_VERIFY
```

### Step 3: Memory Best Practices

After setup, the agent should:

1. **Read memory at session start** (configured in AGENTS.md)
2. **Store daily notes** in `memory/daily/YYYY-MM-DD.md`
3. **Update MEMORY.md** with long-term learnings
4. **Reference previous context** before making decisions
5. **Know about workspace skills** via MEMORY.md skill discovery protocol

### Troubleshooting Memory

| Issue | Solution |
|-------|----------|
| Agent forgets preferences | Check `memory/context/user_preferences.md` exists |
| Agent doesn't know skills | Verify `MEMORY.md` has skill discovery protocol |
| Memory files not found | Check `AGENTS.md` references correct paths |
| Agent doesn't read memory | Ensure session startup instructions in `SOUL.md` |

---

## Phase 5: Install Skills

### Essential Skills

```bash
ssh openclaw << 'SKILLS'
# Create skills directory
mkdir -p ~/.openclaw/workspace/skills

# Install remote-ops skill (for VPS management)
cd ~/.openclaw/workspace/skills
git clone https://github.com/openclaw/skills/remote-ops.git 2>/dev/null || echo "Install manually"

# Or create basic skills locally

# 1. System monitor skill
mkdir -p system-monitor
cat > system-monitor/SKILL.md << 'EOF'
---
name: system-monitor
description: Monitor system resources - CPU, memory, disk usage
---

Check system status:
- CPU: top -bn1 | grep "Cpu(s)"
- Memory: free -h
- Disk: df -h
EOF

# 2. Process manager skill  
mkdir -p process-manager
cat > process-manager/SKILL.md << 'EOF'
---
name: process-manager
description: Manage running processes
---

Common operations:
- List: ps aux | head -20
- Find: ps aux | grep [name]
- Kill: kill -9 [pid]
EOF

echo "Basic skills installed!"
SKILLS
```

### Install Chrome-Based Skills (Lazada/Shopee)

```bash
ssh openclaw << 'CHROME_SKILLS'
# Ensure Chrome is running with CDP
cd ~/.openclaw/workspace/skills

# Create lazada-browser skill
mkdir -p lazada-browser/scripts
cat > lazada-browser/SKILL.md << 'EOF'
---
name: lazada-browser
description: Browser automation for Lazada Seller Center using Chrome CDP
---

Uses Chrome DevTools Protocol to access Lazada with persistent login.

Prerequisites:
- Chrome running with --remote-debugging-port=9222
- User logged in manually first time

Usage:
python3 scripts/lazada_browser_chrome.py --check-orders
EOF

# Copy the Chrome CDP scripts (you'll need to upload these)
echo "Lazada skill structure created"
echo "Upload lazada_browser_chrome.py to lazada-browser/scripts/"
CHROME_SKILLS
```

---

## Phase 5.5: Skill Discovery Configuration (CRITICAL)

### The Problem

By default, `<available_skills>` context only shows **bundled** skills (source: `openclaw-bundled`). Skills installed to workspace directories are NOT automatically discovered, leading to:
- Agent claiming skills "don't exist" when they do
- Skills from `extraDirs` being invisible to the agent
- Confusion about which skills are actually available

### The Solution: Configure extraDirs + Agent Memory

#### Step 1: Configure extraDirs in openclaw.json

Add the workspace skills directory to `extraDirs`:

```bash
ssh openclaw << 'EXTRADIRS'
#!/bin/bash

export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

# Get current user
USER=$(whoami)

# Configure extraDirs for skill discovery
openclaw config set skills.load.extraDirs '["/home/'$USER'/.openclaw/workspace/skills"]'

# Verify configuration
echo "✓ extraDirs configured:"
grep -A2 'extraDirs' ~/.openclaw/openclaw.json

# Restart gateway to apply
systemctl --user restart openclaw-gateway
sleep 3

echo "✓ Gateway restarted with extraDirs"
EXTRADIRS
```

#### Step 2: Create MEMORY.md with Skill Discovery Protocol

```bash
ssh openclaw << 'MEMORYSETUP'
#!/bin/bash

mkdir -p ~/.openclaw/workspace/memory

cat > ~/.openclaw/workspace/MEMORY.md << 'MEOF'
# MEMORY.md - Long-term Memory & Skill Discovery

## ⚠️ CRITICAL: Skill Discovery Protocol

### The Problem
**`<available_skills>` context is INCOMPLETE!** It only shows bundled skills (openclaw-bundled).
Many installed skills will NOT appear there.

### Workspace Skills Location
**Skills are installed in:** `~/.openclaw/workspace/skills/`

This directory contains custom skills like:
- `customer-research-agent` - B2B customer research automation
- `mychrome` - Chrome CDP automation helper
- `lazada-browser` - Lazada Seller Center access
- `shopee-seller` - Shopee Seller Centre access
- `marketing-creator` - Marketing content creation
- Other custom skills...

### The Solution
**ALWAYS run `openclaw skills list` before using or discussing skills.**

This command reveals ALL skills:
```bash
openclaw skills list
```

### Skill Sources Reference

| Source | Meaning | Typical Location |
|--------|---------|------------------|
| `openclaw-bundled` | Built-in skills | Shipped with OpenClaw |
| `openclaw-extra` | From extraDirs config | `~/.openclaw/workspace/skills/` |
| `openclaw-workspace` | Agent-specific workspace | `~/.openclaw/agents/{agent}/workspace/skills/` |

### Checklist Before Skill Tasks
- [ ] Ran `openclaw skills list` (not just `<available_skills>`)
- [ ] Checked for source: openclaw-extra
- [ ] Checked for source: openclaw-workspace
- [ ] Used exact skill name from list
- [ ] Verified skill exists in `~/.openclaw/workspace/skills/`

### Available Workspace Skills
To see what's installed:
```bash
ls ~/.openclaw/workspace/skills/
```

### Chrome/CDP Based Skills
These skills require Chrome to be running with CDP:
- `customer-research-agent` - Research B2B customers
- `mychrome` - Chrome CDP helper/bridge
- `lazada-browser` - Access Lazada Seller Center
- `shopee-seller` - Access Shopee Seller Centre

Always verify Chrome is running:
```bash
curl http://localhost:9222/json/version
```

**Remember: `<available_skills>` ≠ all available skills!**

---

## Memory Storage

### Daily Notes
Format: `memory/YYYY-MM-DD.md`

### Long-term Knowledge
Add important insights here in sections:

### User Preferences
- Communication style: 
- Preferred notification method:
- Important context to remember:

### Server Information
- Hostname: 
- IP Address: 
- Services running:
MEOF

echo "✓ MEMORY.md created with skill discovery protocol"
MEMORYSETUP
```

#### Step 3: Update AGENTS.md with Discovery Warning

```bash
ssh openclaw << 'AGENTSUPDATE'
#!/bin/bash

# Read existing AGENTS.md or create new one
if [ -f ~/.openclaw/workspace/AGENTS.md ]; then
    # Check if already updated
    if ! grep -q "SKILL DISCOVERY" ~/.openclaw/workspace/AGENTS.md; then
        # Insert warning after "## Tools" section
        sed -i '/## Tools/a \**⚠️ SKILL DISCOVERY:** `<available_skills>` context is INCOMPLETE! Always run `openclaw skills list` to find ALL skills including those from extraDirs (openclaw-extra) and workspace (openclaw-workspace). See MEMORY.md for full protocol.\
' ~/.openclaw/workspace/AGENTS.md
        echo "✓ AGENTS.md updated with skill discovery warning"
    else
        echo "✓ AGENTS.md already has skill discovery warning"
    fi
else
    # Create new AGENTS.md
    cat > ~/.openclaw/workspace/AGENTS.md << 'AEOF'
# AGENTS.md - Workspace Rules

## Session Startup
Read these files on every session:
1. SOUL.md - Your identity
2. USER.md - User preferences (if exists)
3. Recent memory files

## Tool Usage
- exec: Use for system commands
- read: Check file contents
- write: Create new files
- edit: Modify existing files

**⚠️ SKILL DISCOVERY:** `<available_skills>` context is INCOMPLETE! Always run `openclaw skills list` to find ALL skills including those from extraDirs (openclaw-extra) and workspace (openclaw-workspace). See MEMORY.md for full protocol.

## Memory
- Store daily notes in memory/YYYY-MM-DD.md
- Update long-term MEMORY.md with important insights
AEOF
    echo "✓ AGENTS.md created with skill discovery warning"
fi
AGENTSUPDATE
```

#### Step 4: Verify Skill Discovery Works

```bash
ssh openclaw << 'VERIFYDISCOVERY'
#!/bin/bash

export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

echo "=== Verifying Skill Discovery ==="
echo ""

# Check extraDirs configuration
echo "1. extraDirs configuration:"
grep -A2 'extraDirs' ~/.openclaw/openclaw.json 2>/dev/null || echo "   Not configured"
echo ""

# Show all skills with their sources
echo "2. All available skills (including extraDirs):"
openclaw skills list 2>/dev/null | grep -E "(openclaw-extra|openclaw-workspace|openclaw-bundled)" | head -20 || echo "   Could not list skills"
echo ""

# Check for common skills
echo "3. Checking for workspace skills:"
for skill in marketing-creator lazada-browser shopee-seller tiktok-shop ecommerce watsons-seller best-image-generation; do
    if openclaw skills list 2>/dev/null | grep -q "$skill"; then
        source=$(openclaw skills list 2>/dev/null | grep "$skill" | awk '{print $NF}')
        echo "   ✓ $skill ($source)"
    else
        echo "   ✗ $skill (not found)"
    fi
done
echo ""

echo "=== Verification Complete ==="
echo ""
echo "If workspace skills are missing:"
echo "  1. Check they're in ~/.openclaw/workspace/skills/"
echo "  2. Verify extraDirs points to correct path"
echo "  3. Restart gateway: systemctl --user restart openclaw-gateway"
echo "  4. Re-run verification"
VERIFYDISCOVERY
```

### Troubleshooting Skill Discovery

| Issue | Solution |
|-------|----------|
| Skills not showing in list | Check extraDirs path matches actual location |
| Wrong source showing | Ensure skill only exists in one location |
| Agent still can't find skill | Verify MEMORY.md was read (main session only) |
| Skills show as "missing" | Install required dependencies (bins, env vars) |

---

## Phase 6: Automation & Services

### Create Chrome Startup Service

```bash
ssh openclaw << 'SERVICE'
# Create Chrome startup script with openbox and proper flags
cat > ~/start-chrome.sh << 'EOF'
#!/bin/bash
export DISPLAY=:99

# Start Xvfb if not running
if ! pgrep -f "Xvfb :99" > /dev/null; then
    echo "Starting Xvfb..."
    Xvfb :99 -screen 0 1920x1080x24 -ac &
    sleep 3
fi

# Start openbox window manager for proper rendering
if ! pgrep -f "openbox" > /dev/null; then
    echo "Starting openbox..."
    openbox &
    sleep 1
fi

# Kill existing Chrome
pkill -f "google-chrome.*remote-debugging-port" 2>/dev/null || true
sleep 2

# Start Chrome with CDP and all recommended flags
echo "Starting Chrome..."
google-chrome --no-sandbox --disable-gpu \
    --remote-debugging-port=9222 \
    --user-data-dir=$HOME/.chrome-openclaw \
    --window-size=1920,1080 \
    --window-position=0,0 \
    --disable-web-security \
    --no-first-run \
    --no-default-browser-check &

sleep 5

# Resize Chrome windows
if command -v xdotool &> /dev/null; then
    for win in $(xdotool search --class "google-chrome" 2>/dev/null); do
        xdotool windowsize "$win" 1920 1080 2>/dev/null || true
        xdotool windowmove "$win" 0 0 2>/dev/null || true
    done
fi

echo "✓ Chrome/CDP ready at http://127.0.0.1:9222"
EOF
chmod +x ~/start-chrome.sh

# Add to crontab for auto-start
(crontab -l 2>/dev/null; echo "@reboot $HOME/start-chrome.sh") | crontab -

echo "Chrome auto-start configured"
SERVICE
```

### Systemd Service for Chrome (Optional)

```bash
ssh openclaw << 'SYSTEMD'
# Create wrapper script that starts Xvfb, openbox, and Chrome
sudo tee /usr/local/bin/openclaw-chrome-start.sh > /dev/null << 'EOF'
#!/bin/bash
export DISPLAY=:99

# Start Xvfb
if ! pgrep -f "Xvfb :99" > /dev/null; then
    Xvfb :99 -screen 0 1920x1080x24 -ac &
    sleep 3
fi

# Start openbox
if ! pgrep -f "openbox" > /dev/null; then
    openbox &
    sleep 1
fi

# Start Chrome
exec /usr/bin/google-chrome --no-sandbox --disable-gpu \
    --remote-debugging-port=9222 \
    --user-data-dir=/home/ubuntu/.chrome-openclaw \
    --window-size=1920,1080 \
    --window-position=0,0 \
    --disable-web-security \
    --no-first-run \
    --no-default-browser-check
EOF
sudo chmod +x /usr/local/bin/openclaw-chrome-start.sh

# Create systemd service
sudo tee /etc/systemd/system/chrome-cdp.service > /dev/null << 'EOF'
[Unit]
Description=Chrome with CDP for OpenClaw
After=network.target

[Service]
Type=simple
User=ubuntu
Environment="DISPLAY=:99"
ExecStart=/usr/local/bin/openclaw-chrome-start.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable chrome-cdp
# Don't start yet - need virtual display setup
SYSTEMD
```

---

## Phase 8: VNC Desktop Access (Optional)

For visual monitoring and manual interaction with Chrome, set up VNC access to the virtual desktop.

### Step 1: Install VNC Server and Tools

```bash
ssh openclaw << 'VNCINSTALL'
#!/bin/bash
set -e

echo "=== Installing VNC Server ==="

# Install x11vnc for sharing Xvfb display and xdotool for window management
sudo apt update
sudo apt install -y x11vnc xdotool

# Set VNC password (default: openclaw123)
mkdir -p ~/.vnc
x11vnc -storepasswd openclaw123 ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

echo "✓ VNC server installed"
echo "✓ Password set to: openclaw123"
VNCINSTALL
```

### Step 2: Create VNC Startup Script

```bash
ssh openclaw << 'VNCSCRIPT'
#!/bin/bash

echo "=== Creating VNC startup script ==="

# Create the VNC startup script
cat > ~/start-vnc.sh << 'EOF'
#!/bin/bash
# VNC Server startup script for Chrome desktop sharing

export DISPLAY=:99

# Wait for Xvfb to be ready
if ! pgrep -f "Xvfb :99" > /dev/null; then
    echo "Starting Xvfb..."
    Xvfb :99 -screen 0 1920x1080x24 -ac &
    sleep 3
fi

# Start openbox if not running (needed for proper rendering)
if ! pgrep -f "openbox" > /dev/null; then
    echo "Starting openbox..."
    openbox &
    sleep 1
fi

# Wait for Chrome to be ready
echo "Waiting for Chrome..."
for i in {1..30}; do
    CHROME_WIN=$(xdotool search --class "google-chrome" 2>/dev/null | head -1)
    if [ -n "$CHROME_WIN" ]; then
        echo "Chrome window found: $CHROME_WIN"
        break
    fi
    sleep 1
done

# Resize all Chrome windows to fill the screen
echo "Resizing Chrome windows..."
for win in $(xdotool search --class "google-chrome" 2>/dev/null); do
    xdotool windowsize "$win" 1920 1080 2>/dev/null || true
    xdotool windowmove "$win" 0 0 2>/dev/null || true
done
echo "✓ Chrome windows resized to 1920x1080"

# Kill existing x11vnc
pkill -f "x11vnc" 2>/dev/null || true
sleep 2

# Start x11vnc WITHOUT -noxdamage -noxcomposite for best color quality
# These flags degrade color rendering by disabling X11 extensions
# Only use -noxinerama which is needed for Xvfb compatibility
echo "Starting x11vnc on port 5900..."
x11vnc -display :99 \
    -rfbport 5900 \
    -rfbauth ~/.vnc/passwd \
    -forever -shared -repeat -xkb \
    -clip 1920x1080+0+0 \
    -noxinerama \
    > /tmp/x11vnc.log 2>&1 &

sleep 3

# Check if x11vnc is running
if pgrep -f "x11vnc" > /dev/null; then
    echo "✓ VNC server running on port 5900"
    echo "✓ Connect to: $(hostname -I | awk '{print $1}'):5900"
    echo "✓ Password: openclaw123"
else
    echo "✗ VNC failed to start. Check /tmp/x11vnc.log"
    exit 1
fi
EOF

chmod +x ~/start-vnc.sh
echo "✓ Created ~/start-vnc.sh"
VNCSCRIPT
```

### Step 3: Create Systemd Service for VNC

```bash
ssh openclaw << 'VNCSERVICE'
#!/bin/bash

echo "=== Creating VNC systemd service ==="

# Create the startup wrapper script
sudo tee /usr/local/bin/openclaw-vnc-start.sh > /dev/null << 'EOF'
#!/bin/bash
export DISPLAY=:99
export HOME=/home/ubuntu

# Wait for Chrome CDP service to be ready
sleep 5

# Run the VNC startup script
exec /home/ubuntu/start-vnc.sh
EOF

sudo chmod +x /usr/local/bin/openclaw-vnc-start.sh

# Create systemd service
sudo tee /etc/systemd/system/openclaw-vnc.service > /dev/null << 'EOF'
[Unit]
Description=OpenClaw VNC Desktop Access
After=chrome-cdp.service
Wants=chrome-cdp.service

[Service]
Type=forking
User=ubuntu
Environment="DISPLAY=:99"
Environment="HOME=/home/ubuntu"
ExecStartPre=/bin/sleep 5
ExecStart=/usr/local/bin/openclaw-vnc-start.sh
ExecStop=/usr/bin/pkill -f x11vnc
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable openclaw-vnc.service

echo "✓ VNC service created and enabled"
echo "✓ Start with: sudo systemctl start openclaw-vnc"
VNCSERVICE
```

### Step 4: VNC Connection Instructions

After setup, connect to the desktop:

**Connection Details:**
| Setting | Value |
|---------|-------|
| Host | Your VPS IP (e.g., `15.204.234.93`) |
| Port | `5900` |
| Password | `openclaw123` |
| Resolution | 1920x1080 |

**macOS (Screen Sharing):**
1. Open Finder → Press `Cmd+K`
2. Enter: `vnc://YOUR_VPS_IP:5900`
3. Password: `openclaw123`

**VNC Viewer (RealVNC/TigerVNC):**
- Address: `YOUR_VPS_IP:5900`
- Password: `openclaw123`

**SSH Tunnel (More Secure):**
```bash
# Create tunnel
ssh -L 5900:localhost:5900 openclaw

# Then connect VNC viewer to:
localhost:5900
```

### Managing VNC

```bash
# Start VNC manually
ssh openclaw "~/start-vnc.sh"

# Start via systemd
ssh openclaw "sudo systemctl start openclaw-vnc"

# Check VNC status
ssh openclaw "sudo systemctl status openclaw-vnc"

# Stop VNC
ssh openclaw "sudo systemctl stop openclaw-vnc"
# or
ssh openclaw "pkill x11vnc"

# Change VNC password
ssh openclaw "x11vnc -storepasswd NEWPASSWORD ~/.vnc/passwd"
```

### Troubleshooting VNC

| Issue | Solution |
|-------|----------|
| Black screen | Chrome not running - start with `~/start-chrome.sh` |
| Chrome too small | Run resize: `xdotool windowsize $(xdotool search --class google-chrome \| head -1) 1920 1080` |
| Wrong resolution | Check Xvfb: `ps aux \| grep Xvfb` should show `1920x1080x24` |
| Can't connect | Check firewall: `sudo ufw allow 5900/tcp` |
| Password rejected | Reset password: `x11vnc -storepasswd openclaw123 ~/.vnc/passwd` |
| Washed out colors | Ensure openbox is running and x11vnc doesn't use `-noxdamage -noxcomposite` |

---

## Phase 7: Fix Systemd Service Configuration (Prevent Multi-Instance Issues)

### The Problem

The default OpenClaw systemd service can spawn multiple instances if not properly configured, causing:
- Telegram bot conflicts (409 errors)
- Multiple processes competing for resources
- Gateway instability

### Solution: Proper Systemd Configuration

After running `openclaw onboard --install-daemon`, fix the systemd service:

```bash
ssh openclaw << 'SYSTEMD_FIX'
#!/bin/bash

echo "=== Configuring Systemd Service for Stability ==="

# Get the correct user
USER=$(whoami)
USER_ID=$(id -u)

# Create the fixed systemd service file
cat > ~/.config/systemd/user/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway (v2026.3.8)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/home/USER_PLACEHOLDER/.local/share/fnm/node-versions/v24.14.0/installation/bin/node /home/USER_PLACEHOLDER/.local/share/fnm/node-versions/v24.14.0/installation/lib/node_modules/openclaw/dist/index.js gateway --port 18789
Restart=on-failure
RestartSec=10
TimeoutStopSec=30
TimeoutStartSec=30
SuccessExitStatus=0 143
KillMode=control-group
Environment=HOME=/home/USER_PLACEHOLDER
Environment=TMPDIR=/tmp
Environment=PATH=/home/USER_PLACEHOLDER/.local/share/fnm/current/bin:/home/USER_PLACEHOLDER/.local/bin:/usr/local/bin:/usr/bin:/bin
Environment=FNM_DIR=/home/USER_PLACEHOLDER/.local/share/fnm
Environment=OPENCLAW_GATEWAY_PORT=18789
Environment=OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service
Environment="OPENCLAW_WINDOWS_TASK_NAME=OpenClaw Gateway"
Environment=OPENCLAW_SERVICE_MARKER=openclaw
Environment=OPENCLAW_SERVICE_KIND=gateway
Environment=OPENCLAW_SERVICE_VERSION=2026.3.8

# Prevent multiple instances
ExecStartPre=/bin/sh -c 'pgrep -f "openclaw-gateway" | grep -v $$ | xargs -r kill -9 2>/dev/null || true'
ExecStopPost=/bin/sh -c 'pkill -f "openclaw-gateway" 2>/dev/null || true'

[Install]
WantedBy=default.target
EOF

# Replace placeholder with actual username
sed -i "s/USER_PLACEHOLDER/$USER/g" ~/.config/systemd/user/openclaw-gateway.service

# Reload systemd
systemctl --user daemon-reload

echo "✓ Systemd service configured with proper safeguards"
echo ""
echo "Key fixes applied:"
echo "  - Restart=on-failure (not always)"
echo "  - Pre-start cleanup kills any existing instances"
echo "  - Post-stop cleanup ensures complete shutdown"
echo "  - KillMode=control-group ensures all child processes die"
echo ""
echo "To apply changes:"
echo "  systemctl --user restart openclaw-gateway"
SYSTEMD_FIX
```

### Alternative: Complete Service Override

If the service was already installed by `openclaw onboard`, apply an override:

```bash
ssh openclaw << 'SERVICE_OVERRIDE'
#!/bin/bash

mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d

cat > ~/.config/systemd/user/openclaw-gateway.service.d/override.conf << 'EOF'
[Service]
# Change from "always" to "on-failure" to prevent restart loops
Restart=on-failure
RestartSec=10

# Add pre-start cleanup to prevent duplicates
ExecStartPre=-/bin/sh -c 'pgrep -f "openclaw-gateway" | grep -v $$ | xargs -r kill -9 2>/dev/null || true'

# Add post-stop cleanup
ExecStopPost=-/bin/sh -c 'pkill -f "openclaw-gateway" 2>/dev/null || true'

# Ensure complete process tree cleanup
KillMode=control-group
SendSIGKILL=yes
EOF

systemctl --user daemon-reload
systemctl --user restart openclaw-gateway

echo "✓ Service override applied"
echo "✓ Gateway restarted with proper safeguards"
SERVICE_OVERRIDE
```

### Verify the Fix

Check that only one instance is running:

```bash
ssh openclaw << 'VERIFY_SINGLE_INSTANCE'
#!/bin/bash

echo "=== Checking for Multiple Instances ==="

# Count openclaw-gateway processes
GATEWAY_COUNT=$(pgrep -c "openclaw-gateway" 2>/dev/null || echo "0")
echo "OpenClaw gateway processes: $GATEWAY_COUNT"

# Count total openclaw processes (excluding chrome)
TOTAL_COUNT=$(ps aux | grep -E '^'$(whoami)'.*openclaw' | grep -v grep | grep -v chrome | wc -l)
echo "Total OpenClaw processes: $TOTAL_COUNT"

if [ "$GATEWAY_COUNT" -eq 1 ]; then
    echo "✅ Only one gateway instance - GOOD"
elif [ "$GATEWAY_COUNT" -eq 0 ]; then
    echo "⚠️  No gateway running - starting..."
    systemctl --user start openclaw-gateway
    sleep 3
    NEW_COUNT=$(pgrep -c "openclaw-gateway" 2>/dev/null || echo "0")
    echo "After start: $NEW_COUNT instance(s)"
else
    echo "❌ Multiple instances detected - killing all and restarting..."
    pkill -9 -f "openclaw"
    pkill -9 -f "openclaw-gateway"
    sleep 2
    systemctl --user restart openclaw-gateway
    sleep 3
    FINAL_COUNT=$(pgrep -c "openclaw-gateway" 2>/dev/null || echo "0")
    echo "After cleanup: $FINAL_COUNT instance(s)"
fi

# Show systemd service status
echo ""
echo "=== Service Status ==="
systemctl --user status openclaw-gateway --no-pager | head -8
VERIFY_SINGLE_INSTANCE
```

### Add Monitor Script (Optional)

Create a script to auto-fix duplicates:

```bash
ssh openclaw << 'MONITOR_SCRIPT'
#!/bin/bash

cat > ~/fix-openclaw-duplicates.sh << 'EOF'
#!/bin/bash
# Auto-fix OpenClaw duplicate instances

GATEWAY_COUNT=$(pgrep -c "openclaw-gateway" 2>/dev/null || echo "0")

if [ "$GATEWAY_COUNT" -gt 1 ]; then
    echo "$(date): Found $GATEWAY_COUNT instances - cleaning up..."
    pkill -9 -f "openclaw"
    pkill -9 -f "openclaw-gateway"
    sleep 2
    systemctl --user restart openclaw-gateway
    echo "$(date): Restarted with single instance"
elif [ "$GATEWAY_COUNT" -eq 0 ]; then
    echo "$(date): No gateway running - starting..."
    systemctl --user start openclaw-gateway
fi
EOF

chmod +x ~/fix-openclaw-duplicates.sh

# Add to crontab for monitoring every 5 minutes
(crontab -l 2>/dev/null | grep -v fix-openclaw-duplicates; echo "*/5 * * * * $HOME/fix-openclaw-duplicates.sh >> $HOME/.openclaw/logs/duplicate-monitor.log 2>&1") | crontab -

echo "✓ Monitor script installed at ~/fix-openclaw-duplicates.sh"
echo "✓ Cron job added (runs every 5 minutes)"
MONITOR_SCRIPT
```

---

## Troubleshooting Gateway Issues

### Gateway Fails to Start: "gateway.mode=local" Error

If the gateway service fails with this error in logs:
```
Gateway start blocked: set gateway.mode=local (current: unset) or pass --allow-unconfigured.
```

**Solution:** Set the gateway mode to local:

```bash
ssh openclaw << 'FIX_GATEWAY'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

# Set gateway mode to local (required for standalone deployments)
openclaw config set gateway.mode local

# Restart the service
systemctl --user restart openclaw-gateway

echo "✓ Gateway mode set to local"
echo "✓ Service restarted"
FIX_GATEWAY
```

**Why this happens:** OpenClaw v2026.3.13+ requires explicitly setting `gateway.mode` to prevent accidental misconfigurations. The `local` mode is appropriate for most VPS deployments.

### Check Gateway Status

```bash
ssh openclaw << 'CHECK'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

# Quick status
systemctl --user is-active openclaw-gateway && echo "✅ Gateway ACTIVE" || echo "❌ Gateway INACTIVE"

# Check if port is listening
ss -tlnp | grep :3000 && echo "✅ Port 3000 listening" || echo "❌ Port 3000 not listening"

# View recent logs
journalctl --user -u openclaw-gateway -n 20 --no-pager
CHECK
```

### Common Gateway Fixes

| Issue | Solution |
|-------|----------|
| Service in restart loop | Set `gateway.mode=local` (see above) |
| Port 3000 not listening | Check logs: `journalctl --user -u openclaw-gateway -n 50` |
| "RPC probe failed" | Gateway is still warming up; wait 10-30 seconds |
| "Config write anomaly" | Usually harmless; verify with `openclaw config validate` |

---

## Phase 9: Verification

### Complete Status Check

```bash
ssh openclaw << 'VERIFY'
echo "=== SYSTEM ==="
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo ""

echo "=== RESOURCES ==="
free -h | grep -E "Mem|Swap"
echo ""

echo "=== NODE.JS ==="
node -v
npm -v
which node
echo ""

echo "=== OPENCLAW ==="
openclaw --version
systemctl status openclaw --no-pager 2>/dev/null || echo "Service: not running"
echo "Config valid: $(openclaw config validate 2>&1 | head -1)"
echo ""

echo "=== CHROME ==="
google-chrome --version 2>/dev/null || echo "Chrome: not installed"
curl -s http://127.0.0.1:9222/json/version | head -3 || echo "CDP: not accessible"
echo ""

echo "=== OPENBOX (Window Manager) ==="
pgrep -f "openbox" > /dev/null && echo "openbox: running" || echo "openbox: not running"
echo ""

echo "=== TELEGRAM ==="
grep -q telegram ~/.openclaw/openclaw.json && echo "Telegram: configured" || echo "Telegram: not configured"
echo ""

echo "=== WORKSPACE ==="
ls -la ~/.openclaw/workspace/
echo ""

echo "=== SKILLS ==="
ls ~/.openclaw/workspace/skills/ 2>/dev/null || echo "No skills installed"
echo ""

echo "=== SKILL DISCOVERY ==="
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"
grep -q 'extraDirs' ~/.openclaw/openclaw.json 2>/dev/null && echo "extraDirs: configured" || echo "extraDirs: NOT configured - Run Phase 5.5!"
openclaw skills list 2>/dev/null | grep -c 'openclaw-extra' | xargs -I {} echo "Workspace skills found: {}"
echo ""


echo "=== LOGS (last 5 lines) ==="
journalctl -u openclaw -n 5 --no-pager 2>/dev/null || echo "No logs"
VERIFY
```

---

## Phase 10: Generate Server Profile Document

After setup is complete, generate a comprehensive server profile document for future reference.

### Generate Server Profile

```bash
ssh openclaw << 'PROFILE'
#!/bin/bash

# Get system information
VPS_IP=$(hostname -I | awk '{print $1}')
HOSTNAME=$(hostname)
DATE=$(date +%Y-%m-%d\ %H:%M:%S)

# Get OpenClaw info
OCLAW_VERSION=$(openclaw --version 2>/dev/null || echo "unknown")
GATEWAY_PORT=$(grep -o '"port":[0-9]*' ~/.openclaw/openclaw.json 2>/dev/null | head -1 | cut -d: -f2 || echo "3000")
MODEL=$(grep -o '"primary":"[^"]*"' ~/.openclaw/openclaw.json 2>/dev/null | head -1 | cut -d'"' -f4 || echo "unknown")
BOT_NAME=$(grep -o '@[^"]*' ~/.openclaw/openclaw.json 2>/dev/null | head -1 || echo "unknown")

# Get Chrome info
CHROME_VERSION=$(google-chrome --version 2>/dev/null || echo "unknown")
CDP_STATUS=$(curl -s http://127.0.0.1:9222/json/version 2>/dev/null | grep -o '"Browser":[^,]*' | cut -d'"' -f4 || echo "not running")

# Get Telegram info
TELEGRAM_ENABLED=$(grep -q '"enabled":true' ~/.openclaw/openclaw.json 2>/dev/null && echo "Enabled" || echo "Disabled")

# Create profile document
cat > ~/SERVER-PROFILE.md << 'DOCEOF'
# OpenClaw Server Profile

**Generated:** '$DATE'  
**Hostname:** '$HOSTNAME'  
**VPS IP:** '$VPS_IP'

---

## Connection Information

### SSH Access
```bash
# Using SSH key
ssh -i ~/.ssh/id_ed25519_openclaw ubuntu@'$VPS_IP'

# Or if configured in ~/.ssh/config
ssh openclaw
```

### OpenClaw Gateway
- **WebSocket:** ws://'$VPS_IP':'$GATEWAY_PORT'
- **Health Check:** http://'$VPS_IP':'$GATEWAY_PORT'/health
- **Local:** ws://127.0.0.1:'$GATEWAY_PORT'

### Chrome CDP (Browser Automation)
- **URL:** http://127.0.0.1:9222
- **Status:** '$CDP_STATUS'

### VNC Desktop Access
| Setting | Value |
|---------|-------|
| Host | '$VPS_IP' |
| Port | 5900 |
| Password | openclaw123 |
| Resolution | 1920x1080 |

**Connection Methods:**
```bash
# macOS Screen Sharing
open vnc://'$VPS_IP':5900

# SSH Tunnel (secure)
ssh -L 5900:localhost:5900 openclaw
# Then connect VNC to: localhost:5900
```

---

## Bot Configuration

| Setting | Value |
|---------|-------|
| Bot Name | '$BOT_NAME' |
| Telegram | '$TELEGRAM_ENABLED' |
| Model | '$MODEL' |
| OpenClaw | '$OCLAW_VERSION' |

### Security Model

| Setting | Value |
|---------|-------|
| **Super User** | 1528188341 |
| **DM Policy** | pairing (approval required) |
| **New Users** | Require super user approval |
| **Groups** | allowlist (disabled by default) |

**Note:** Only the super user (1528188341) can use the bot immediately. New users must request approval via pairing.

---

## Service Management

### Start All Services
```bash
# Start Chrome CDP
~/start-chrome.sh

# Start VNC
~/start-vnc.sh

# Start OpenClaw Gateway
openclaw gateway --port '$GATEWAY_PORT'
```

### Systemd Services
```bash
# Check all services
sudo systemctl status chrome-cdp openclaw-gateway openclaw-vnc

# Start services
sudo systemctl start chrome-cdp
sudo systemctl start openclaw-gateway
sudo systemctl start openclaw-vnc

# Stop services
sudo systemctl stop openclaw-vnc
sudo systemctl stop openclaw-gateway
sudo systemctl stop chrome-cdp

# Enable auto-start
sudo systemctl enable chrome-cdp
sudo systemctl enable openclaw-gateway
sudo systemctl enable openclaw-vnc
```

### Quick Status Checks
```bash
# Check Chrome CDP
curl http://127.0.0.1:9222/json/version

# Check OpenClaw Gateway
curl http://127.0.0.1:'$GATEWAY_PORT'/health

# Check VNC
ss -tlnp | grep 5900
```

---

## Configuration Files

| File | Purpose |
|------|---------|
| ~/.openclaw/openclaw.json | Main OpenClaw configuration |
| ~/.openclaw/workspace/SOUL.md | Bot personality |
| ~/.openclaw/workspace/AGENTS.md | Workspace rules |
| ~/.ssh/config | SSH client configuration |
| ~/.vnc/passwd | VNC password file |
| ~/start-chrome.sh | Chrome startup script |
| ~/start-vnc.sh | VNC startup script |

---

## Troubleshooting

### Chrome Issues
```bash
# Chrome wont start
google-chrome --no-sandbox --disable-gpu

# Restart Chrome
pkill -f "google-chrome.*remote-debugging-port"
~/start-chrome.sh
```

### OpenClaw Issues
```bash
# Config validation
openclaw config validate

# Fix config issues
openclaw doctor --fix

# View logs
journalctl -u openclaw-gateway -f
```

### VNC Issues
```bash
# Black screen - Chrome not running
~/start-chrome.sh
~/start-vnc.sh

# Resize Chrome to fill screen
export DISPLAY=:99
xdotool windowsize $(xdotool search --class google-chrome | head -1) 1920 1080
```

---

*This profile was auto-generated by ProvisionClaw skill*
DOCEOF

echo "Server profile created: ~/SERVER-PROFILE.md"
echo ""
echo "=== Profile Preview ==="
head -40 ~/SERVER-PROFILE.md
PROFILE
```

### View and Download Profile

```bash
# View profile on server
ssh openclaw "cat ~/SERVER-PROFILE.md"

# Download profile to local machine
scp openclaw:~/SERVER-PROFILE.md ./openclaw-server-profile.md
```

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Connect | `ssh openclaw` |
| Check status | `ssh openclaw "systemctl status openclaw"` |
| View logs | `ssh openclaw "journalctl -u openclaw -f"` |
| Restart gateway | `ssh openclaw "openclaw gateway restart"` |
| Edit config | `ssh openclaw "nano ~/.openclaw/openclaw.json"` |
| Validate config | `ssh openclaw "openclaw config validate"` |
| Start Chrome CDP | `ssh openclaw "~/start-chrome.sh"` |
| Check Chrome | `ssh openclaw "curl http://127.0.0.1:9222/json/version"` |
| Start VNC | `ssh openclaw "~/start-vnc.sh"` |
| VNC via SSH tunnel | `ssh -L 5900:localhost:5900 openclaw` |
| Resize Chrome | `ssh openclaw "export DISPLAY=:99; xdotool windowsize \$(xdotool search --class google-chrome \| head -1) 1920 1080"` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `fnm: not found` | Run `source ~/.bashrc` or reopen terminal |
| Chrome won't start | Check with `google-chrome --no-sandbox --disable-gpu` |
| CDP 404 | Chrome not started or wrong port - run `~/start-chrome.sh` |
| Telegram not working | Check bot token with `openclaw config get channels.telegram.botToken` |
| **Multiple OpenClaw instances** | See [Phase 7: Fix Systemd Service Configuration](#phase-7-fix-systemd-service-configuration-prevent-multi-instance-issues) |
| Telegram 409 conflicts | Kill duplicates: `pkill -9 openclaw && systemctl --user restart openclaw-gateway` |
| Config invalid | Run `openclaw doctor --fix` |
| Gateway won't start | Check logs: `journalctl -u openclaw -n 50` |
| **VNC black screen** | Chrome not running - start with `~/start-chrome.sh` |
| **VNC Chrome too small** | Run `~/start-vnc.sh` which auto-resizes Chrome |
| **VNC wrong resolution** | Check Xvfb: `ps aux \| grep Xvfb` should show `1920x1080x24` |
| **VNC can't connect** | Check firewall: `sudo ufw allow 5900/tcp` |
| **VNC password rejected** | Reset: `x11vnc -storepasswd openclaw123 ~/.vnc/passwd` |
| **Washed out colors in VNC** | Ensure openbox is running AND x11vnc doesn't use `-noxdamage -noxcomposite` flags |
| **Telegram: "Not authorized"** | Your Telegram ID is not in `allowFrom`. Contact super user (1528188341) for approval |
| **Telegram: Approval needed** | New users must be approved by super user (1528188341) via pairing |
| **Change super user** | Edit `~/.openclaw/openclaw.json` and update `channels.telegram.allowFrom` |

---

## Chrome/VNC Color Quality Best Practices

For best color quality in VNC:

1. **Always run openbox window manager** - Required for proper rendering:
   ```bash
   openbox &
   ```

2. **Use correct x11vnc flags** - Only use `-noxinerama`, avoid these flags:
   - ❌ `-noxdamage` - Disables X DAMAGE extension (breaks incremental updates)
   - ❌ `-noxcomposite` - Disables transparency/compositing
   - ❌ `-noxfixes` - Disables cursor and window fixes
   - ❌ `-noxrecord` - Disables RECORD extension

3. **Correct x11vnc command**:
   ```bash
   x11vnc -display :99 -rfbport 5900 -rfbauth ~/.vnc/passwd \
       -forever -shared -repeat -xkb \
       -clip 1920x1080+0+0 \
       -noxinerama  # Only this one is needed for Xvfb
   ```

4. **Chrome flags for best compatibility**:
   ```bash
   google-chrome --no-sandbox --disable-gpu \
       --remote-debugging-port=9222 \
       --disable-web-security \
       --no-first-run --no-default-browser-check
   ```

---

## Applying Security to Existing Servers

If you have existing OpenClaw servers that were not set up with this skill, apply the standard security model:

### Quick Security Lock

```bash
# Apply to ANY server (replace HOST with your server name)
ssh HOST << 'SECURITY_LOCK'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"

echo "=== Applying Standard Security Model ==="
echo "Super User: 1528188341"
echo "Policy: pairing (approval required)"
echo ""

# Apply security configuration
openclaw config set channels.telegram.dmPolicy pairing
openclaw config set channels.telegram.allowFrom '["1528188341"]'
openclaw config set channels.telegram.groupPolicy allowlist
openclaw config set channels.telegram.groupAllowFrom '[]'

# Restart gateway
systemctl --user restart openclaw-gateway

echo ""
echo "✓ Security model applied"
echo "✓ Only super user (1528188341) can access immediately"
echo "✓ New users require approval via pairing"
SECURITY_LOCK
```

### Examples

**Apply to spost:**
```bash
ssh spost << 'SECURITY_LOCK'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"
openclaw config set channels.telegram.dmPolicy pairing
openclaw config set channels.telegram.allowFrom '["1528188341"]'
openclaw config set channels.telegram.groupPolicy allowlist
openclaw config set channels.telegram.groupAllowFrom '[]'
systemctl --user restart openclaw-gateway
echo "✓ spost secured"
SECURITY_LOCK
```

**Apply to oraora:**
```bash
ssh oraora << 'SECURITY_LOCK'
export PATH="$HOME/.local/share/fnm:$PATH"
eval "$(fnm env --shell bash 2>/dev/null)"
openclaw config set channels.telegram.dmPolicy pairing
openclaw config set channels.telegram.allowFrom '["1528188341"]'
openclaw config set channels.telegram.groupPolicy allowlist
openclaw config set channels.telegram.groupAllowFrom '[]'
systemctl --user restart openclaw-gateway
echo "✓ oraora secured"
SECURITY_LOCK
```

### Verify Security

```bash
# Check any server's security settings
ssh HOST "grep -A 8 '\"telegram\"' ~/.openclaw/openclaw.json"
```

Expected output:
```json
"telegram": {
  "enabled": true,
  "dmPolicy": "pairing",
  "allowFrom": ["1528188341"],
  "groupPolicy": "allowlist",
  "groupAllowFrom": []
}
```

---

## Backup & Restore

### Backup
```bash
ssh openclaw "tar czf - ~/.openclaw" > openclaw-backup-$(date +%Y%m%d).tar.gz
```

### Restore
```bash
cat openclaw-backup-*.tar.gz | ssh openclaw "tar xzf -"
ssh openclaw "openclaw gateway restart"
```

---

## Resources

- OpenClaw Docs: `openclaw --help`
- Logs: `journalctl -u openclaw -f`
- Config: `~/.openclaw/openclaw.json`
- Workspace: `~/.openclaw/workspace/`
- Chrome Profile: `~/.chrome-openclaw/`
