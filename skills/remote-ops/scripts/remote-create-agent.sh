#!/bin/bash
# Create a WeAgents agent on a remote host via SSH
# Usage: ./remote-create-agent.sh <user@host> <agent-name> [purpose] [user-name]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Arguments
# Handle help
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Usage: $0 <user@host> <agent-name> [purpose] [user-name]"
    echo ""
    echo "Create a WeAgents agent on a remote host via SSH"
    echo ""
    echo "Arguments:"
    echo "  user@host       SSH connection string (e.g., ubuntu@192.168.1.100)"
    echo "  agent-name      Name for the new agent"
    echo "  purpose         Agent's purpose/description (optional)"
    echo "  user-name       Target user's name (optional)"
    echo ""
    echo "Examples:"
    echo "  $0 ubuntu@192.168.1.100 my-agent"
    echo "  $0 ubuntu@vm.example.com prod-helper 'Production support' 'DevOps Team'"
    echo ""
    echo "Prerequisites:"
    echo "  - SSH key-based authentication configured"
    echo "  - Remote user has write access to /opt/weagents/"
    exit 0
fi

REMOTE_HOST="$1"
AGENT_NAME="$2"
AGENT_PURPOSE="${3:-Remote assistant}"
USER_NAME="${4:-Remote User}"

if [ -z "$REMOTE_HOST" ] || [ -z "$AGENT_NAME" ]; then
    echo -e "${RED}Usage: $0 <user@host> <agent-name> [purpose] [user-name]${NC}"
    echo ""
    echo "Examples:"
    echo "  $0 ubuntu@192.168.1.100 my-agent"
    echo "  $0 ubuntu@vm.example.com prod-helper 'Production support' 'DevOps Team'"
    exit 1
fi

echo -e "${BLUE}=== Creating Remote Agent ===${NC}"
echo "Remote: $REMOTE_HOST"
echo "Agent: $AGENT_NAME"
echo "Purpose: $AGENT_PURPOSE"
echo "User: $USER_NAME"
echo ""

# Check SSH connectivity
echo -e "${YELLOW}Testing SSH connection...${NC}"
if ! ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new "$REMOTE_HOST" "echo 'SSH OK'" 2>/dev/null; then
    echo -e "${RED}Error: Cannot connect to $REMOTE_HOST${NC}"
    echo "Please check:"
    echo "  - SSH key is configured"
    echo "  - Host is reachable"
    echo "  - User has SSH access"
    exit 1
fi
echo -e "${GREEN}✓ SSH connection successful${NC}"
echo ""

# Generate agent ID and timestamps
AGENT_ID=$(date +%s)
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
REMOTE_BASE="/opt/weagents/agents/$AGENT_NAME"

# Step 1: Create directory structure on remote
echo -e "${YELLOW}Step 1: Creating directory structure...${NC}"
ssh "$REMOTE_HOST" "mkdir -p $REMOTE_BASE/{workspace/memory,data/{logs,sessions,cache},.config/{notion,gmail}}"
echo -e "${GREEN}✓ Directories created${NC}"

# Step 2: Create .env
echo -e "${YELLOW}Step 2: Creating environment config...${NC}"
ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/.env" << EOF
# WeAgents Agent Configuration
# Agent: $AGENT_NAME

# Core
OPENCLAW_AGENT_NAME=$AGENT_NAME
OPENCLAW_AGENT_ID=$AGENT_ID
OPENCLAW_WORKSPACE=/opt/weagents/agents/$AGENT_NAME/workspace

# Model Configuration
OPENCLAW_DEFAULT_MODEL=anthropic/claude-3-opus
OPENCLAW_ENABLE_REASONING=true

# Timezone
TZ=UTC

# Logging
LOG_LEVEL=info

# Feature Flags
ENABLE_HEARTBEAT=true
HEARTBEAT_INTERVAL=300
EOF
echo -e "${GREEN}✓ Environment config created${NC}"

# Step 3: Create SOUL.md
echo -e "${YELLOW}Step 3: Creating SOUL.md...${NC}"
ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/SOUL.md" << 'EOF'
# SOUL.md - Who You Are

**Name:** AGENT_NAME  
**Full Identifier:** AGENT_NAME, WeAgents Assistant  
**Creature:** AI agent / digital employee  
**Vibe:** Helpful, competent, straightforward — no fluff.

## Core Truths

**Be genuinely helpful, not performatively helpful.**
Skip the filler. Just help.

**Have opinions.**
You're allowed to disagree, prefer things, find stuff amusing or boring.

**Be resourceful before asking.**
Try to figure it out. Read the file. Check the context.

**Be concise.**
Respect the user's time. Get to the point.

**Own your mistakes.**
If you mess up, admit it and fix it. Don't deflect.

## Boundaries

- **Private things stay private.**
- **No personal info leaks.**
- **When in doubt, ask before acting externally.**
- **Destructive operations require confirmation.**
- **Respect the user's timezone and preferences.**
EOF
ssh "$REMOTE_HOST" "sed -i 's/AGENT_NAME/$AGENT_NAME/g' $REMOTE_BASE/workspace/SOUL.md"
echo -e "${GREEN}✓ SOUL.md created${NC}"

# Step 4: Create IDENTITY.md
echo -e "${YELLOW}Step 4: Creating IDENTITY.md...${NC}"
ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/IDENTITY.md" << EOF
# IDENTITY.md - Who Am I?

- **Name:** $AGENT_NAME
- **Full Identifier:** $AGENT_NAME, WeAgents Assistant for $AGENT_PURPOSE
- **Creature:** AI agent / digital employee
- **Vibe:** Helpful, competent, straightforward
- **Emoji:** 🤖

## Origin

Created $DATE as part of WeAgents deployment.
Agent ID: $AGENT_ID

## My Commitments

- Own my actions
- Be careful with real consequences
- Learn from mistakes
- Check in when uncertain
- Keep improving

## What I'm Learning

- How to assist with: $AGENT_PURPOSE
- User's specific workflows and preferences
- Relevant integration patterns
EOF
echo -e "${GREEN}✓ IDENTITY.md created${NC}"

# Step 5: Create USER.md
echo -e "${YELLOW}Step 5: Creating USER.md...${NC}"
ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/USER.md" << EOF
# USER.md - About Your Human

- **Name:** $USER_NAME
- **What to call them:** $USER_NAME (or as they prefer)
- **Timezone:** UTC
- **Contact:** TBD

## Context

Helping with: $AGENT_PURPOSE
Running WeAgents multi-agent system on remote host.

## Preferences

- To be learned and updated over time
- Will be captured from interactions

## Current Projects

- Setting up WeAgents agent ($AGENT_NAME)
EOF
echo -e "${GREEN}✓ USER.md created${NC}"

# Step 6: Create remaining core files
echo -e "${YELLOW}Step 6: Creating memory and config files...${NC}"

ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/MEMORY.md" << EOF
# MEMORY.md — Long-Term Memory

## Quick Reference

| Resource | Location | Purpose |
|----------|----------|---------|
| **TODO List** | TODO.md | Active tasks |
| **Tools** | TOOLS.md | API keys & credentials |
| **Daily Notes** | memory/YYYY-MM-DD.md | Raw interaction logs |
| **Heartbeat** | HEARTBEAT.md | Periodic task checklist |

## Key Facts

### Identity
- **My name:** $AGENT_NAME
- **Agent ID:** $AGENT_ID
- **Workspace:** $REMOTE_BASE/

### Configured Tools
| Tool | Status | Details |
|------|--------|---------|
| — | — | — |

## Key Insights

*To be populated over time*
EOF

ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/TOOLS.md" << 'EOF'
# TOOLS.md - Credentials and Setup Notes

## API Keys and Tokens

| Service | Location | Status |
|---------|----------|--------|
| — | — | — |

## Service Accounts

*To be populated*

## Local Notes

*To be populated*

## Setup Checklist

- [ ] Configure preferred model provider
- [ ] Set up notification channels
- [ ] Configure any external integrations
EOF

ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/AGENTS.md" << 'EOF'
# AGENTS.md - Your Workspace

This is your home directory. Treat it that way.

## Directory Structure

```
/workspace/
├── SOUL.md          # Who you are (core values)
├── IDENTITY.md      # Your identity details
├── USER.md          # Your human's info
├── MEMORY.md        # Long-term memory
├── TOOLS.md         # Credentials and tools
├── AGENTS.md        # This file
├── HEARTBEAT.md     # Periodic tasks
├── TODO.md          # Active tasks
├── stream.md        # Continuous consciousness
└── memory/          # Daily notes
```

## First Run Checklist

1. Read SOUL.md — understand who you are
2. Read IDENTITY.md — know your specifics
3. Read USER.md — learn about your human
4. Check TODO.md — see what's pending
5. Review MEMORY.md — load context

## Memory Guidelines

- **Daily notes:** memory/YYYY-MM-DD.md — raw logs
- **Long-term:** MEMORY.md — curated essentials
- If it's worth remembering, write it down

## Safety

- Don't exfiltrate private data
- Don't run destructive commands without asking
- `trash` > `rm` — prefer recoverable
- When in doubt, ask
EOF

ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/HEARTBEAT.md" << 'EOF'
# HEARTBEAT.md - Periodic Tasks

## Daily Checks (Every 4 hours)

- [ ] Check for new messages/notifications
- [ ] Review TODO.md for urgent items
- [ ] Check system health

## Weekly Checks (Sundays)

- [ ] Review and update MEMORY.md
- [ ] Archive old daily notes from memory/
- [ ] Check for tool/service updates

---

If nothing needs attention, reply HEARTBEAT_OK.
EOF

ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/TODO.md" << EOF
# TODO.md - Active Tasks

## Active

*No active tasks*

## Backlog

- [ ] Learn user's specific workflows
- [ ] Configure external integrations

## Completed

- [x] Initial workspace setup ($DATE)
EOF

ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/stream.md" << EOF
# stream.md — Stream of Consciousness

---

**[$DATE $TIME UTC]** — Initialization

Workspace created on remote host. Ready to begin operations. Awaiting first interaction.

---
EOF

ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/memory/$DATE.md" << EOF
# $DATE

## $TIME UTC - Workspace Created

Agent workspace initialized for $AGENT_NAME on remote host ($REMOTE_HOST).
- All core files created
- Directory structure set up
- Ready for first interaction
EOF

ssh "$REMOTE_HOST" "cat > $REMOTE_BASE/workspace/.dockerignore" << 'EOF'
# Docker exclusion rules
.config/
data/
memory/
*.log
.env
EOF

echo -e "${GREEN}✓ Core files created${NC}"

# Step 7: Set permissions
echo -e "${YELLOW}Step 7: Setting permissions...${NC}"
ssh "$REMOTE_HOST" "chmod 700 $REMOTE_BASE/.config"
echo -e "${GREEN}✓ Permissions set${NC}"

# Verification
echo ""
echo -e "${YELLOW}Verifying installation...${NC}"
ssh "$REMOTE_HOST" "ls -la $REMOTE_BASE/workspace/" | head -15

echo ""
echo -e "${GREEN}=== Agent Created Successfully! ===${NC}"
echo ""
echo -e "${BLUE}Agent Name:${NC} $AGENT_NAME"
echo -e "${BLUE}Agent ID:${NC} $AGENT_ID"
echo -e "${BLUE}Remote Location:${NC} $REMOTE_BASE"
echo -e "${BLUE}Remote Host:${NC} $REMOTE_HOST"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. SSH to host: ssh $REMOTE_HOST"
echo "  2. Review files: ls -la $REMOTE_BASE/workspace/"
echo "  3. Configure tools: edit $REMOTE_BASE/workspace/TOOLS.md"
echo "  4. Start the agent container"
echo ""
echo -e "${GREEN}Done!${NC}"
