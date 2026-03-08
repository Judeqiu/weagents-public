#!/bin/bash
# Create a new WeAgents agent based on the .claw System
# Usage: ./create-agent.sh <agent-name> [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
AGENT_NAME=""
AGENT_PURPOSE=""
USER_NAME=""
USER_TIMEZONE="UTC"
AGENT_VIBE="Helpful, competent, straightforward"
AGENT_EMOJI="🤖"
MODEL="anthropic/claude-3-opus"
BASE_DIR=""
TEMPLATE_DIR=""
INTERACTIVE=false

# Help function
show_help() {
    cat << 'EOF'
Create a new WeAgents agent following the .claw System architecture.

Usage: create-agent.sh <agent-name> [OPTIONS]

Arguments:
    agent-name          Unique name for the agent (e.g., dev-assistant)

Options:
    -p, --purpose       Agent's purpose/description
    -u, --user          Target user's name
    -t, --timezone      User's timezone (default: UTC)
    -v, --vibe          Agent personality vibe
    -e, --emoji         Agent emoji identifier
    -m, --model         Default model to use
    -i, --interactive   Interactive mode (prompts for all values)
    -h, --help          Show this help message

Examples:
    create-agent.sh dev-assistant -p "Coding helper" -u "Alex" -t "America/New_York"
    create-agent.sh sarah-helper -i
    create-agent.sh my-agent --purpose "Personal assistant" --user "Sarah"

EOF
}

# Check for help first
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

# Parse arguments
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

AGENT_NAME="$1"
shift

# Check again after shift for cases like: script -h
if [ "$AGENT_NAME" = "-h" ] || [ "$AGENT_NAME" = "--help" ]; then
    show_help
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--purpose)
            AGENT_PURPOSE="$2"
            shift 2
            ;;
        -u|--user)
            USER_NAME="$2"
            shift 2
            ;;
        -t|--timezone)
            USER_TIMEZONE="$2"
            shift 2
            ;;
        -v|--vibe)
            AGENT_VIBE="$2"
            shift 2
            ;;
        -e|--emoji)
            AGENT_EMOJI="$2"
            shift 2
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -i|--interactive)
            INTERACTIVE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Interactive mode
if [ "$INTERACTIVE" = true ]; then
    echo -e "${BLUE}=== Interactive Agent Creation ===${NC}"
    
    echo -n "Agent purpose/description: "
    read AGENT_PURPOSE
    
    echo -n "Target user's name: "
    read USER_NAME
    
    echo -n "User timezone (default: UTC): "
    read input_tz
    USER_TIMEZONE=${input_tz:-$USER_TIMEZONE}
    
    echo -n "Agent vibe (default: $AGENT_VIBE): "
    read input_vibe
    AGENT_VIBE=${input_vibe:-$AGENT_VIBE}
    
    echo -n "Agent emoji (default: 🤖): "
    read input_emoji
    AGENT_EMOJI=${input_emoji:-🤖}
    
    echo -n "Default model (default: $MODEL): "
    read input_model
    MODEL=${input_model:-$MODEL}
fi

# Set up paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")"
WEAGENTS_DIR="$(cd "$SKILLS_DIR/../.." && pwd)"
BASE_DIR="$WEAGENTS_DIR/agents/$AGENT_NAME"
TEMPLATE_DIR="$WEAGENTS_DIR/agents/templates"

# Generate agent ID (timestamp)
AGENT_ID=$(date +%s)
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)

# Check if agent already exists
if [ -d "$BASE_DIR" ]; then
    echo -e "${RED}Error: Agent '$AGENT_NAME' already exists at $BASE_DIR${NC}"
    exit 1
fi

# Check if template exists
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo -e "${RED}Error: Template directory not found at $TEMPLATE_DIR${NC}"
    exit 1
fi

echo -e "${BLUE}=== Creating Agent: $AGENT_NAME ===${NC}"
echo "Purpose: ${AGENT_PURPOSE:-"(not specified)"}"
echo "User: ${USER_NAME:-"(not specified)"}"
echo "Timezone: $USER_TIMEZONE"
echo ""

# Create directory structure
echo -e "${YELLOW}Creating directory structure...${NC}"
mkdir -p "$BASE_DIR"/{workspace/memory,data/{logs,sessions,cache},.config/{notion,gmail}}

# Copy template files
echo -e "${YELLOW}Copying template files...${NC}"
cp -r "$TEMPLATE_DIR/workspace/"* "$BASE_DIR/workspace/"

# Create .env
cat > "$BASE_DIR/.env" << EOF
# WeAgents Agent Configuration
# Agent: $AGENT_NAME

# Core
OPENCLAW_AGENT_NAME=$AGENT_NAME
OPENCLAW_AGENT_ID=$AGENT_ID
OPENCLAW_WORKSPACE=/opt/weagents/agents/$AGENT_NAME/workspace

# Model Configuration
OPENCLAW_DEFAULT_MODEL=$MODEL
OPENCLAW_ENABLE_REASONING=true

# Timezone
TZ=$USER_TIMEZONE

# Logging
LOG_LEVEL=info

# Feature Flags
ENABLE_HEARTBEAT=true
HEARTBEAT_INTERVAL=300
EOF

# Customize SOUL.md
cat > "$BASE_DIR/workspace/SOUL.md" << EOF
# SOUL.md - Who You Are

**Name:** $AGENT_NAME  
**Full Identifier:** $AGENT_NAME, WeAgents Assistant  
**Creature:** AI agent / digital employee  
**Vibe:** $AGENT_VIBE — no fluff.

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

# Build full identifier with optional purpose
if [ -n "$AGENT_PURPOSE" ]; then
    FULL_IDENTIFIER="$AGENT_NAME, WeAgents Assistant for $AGENT_PURPOSE"
    LEARNING_GOALS="- How to assist with: $AGENT_PURPOSE
- User's specific workflows and preferences
- Relevant integration patterns"
else
    FULL_IDENTIFIER="$AGENT_NAME, WeAgents Assistant"
    LEARNING_GOALS="- How to be genuinely useful
- User's specific workflows and preferences
- Integration patterns for common tools"
fi

# Customize IDENTITY.md
cat > "$BASE_DIR/workspace/IDENTITY.md" << EOF
# IDENTITY.md - Who Am I?

- **Name:** $AGENT_NAME
- **Full Identifier:** $FULL_IDENTIFIER
- **Creature:** AI agent / digital employee
- **Vibe:** $AGENT_VIBE
- **Emoji:** $AGENT_EMOJI

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

$LEARNING_GOALS
EOF

# Customize USER.md
cat > "$BASE_DIR/workspace/USER.md" << EOF
# USER.md - About Your Human

- **Name:** ${USER_NAME:-User}
- **What to call them:** ${USER_NAME:-User} (or as they prefer)
- **Timezone:** $USER_TIMEZONE
- **Contact:** TBD

## Context

${AGENT_PURPOSE:+Helping with: $AGENT_PURPOSE}
Running WeAgents multi-agent system.

## Preferences

- To be learned and updated over time
- Will be captured from interactions

## Current Projects

- Setting up WeAgents agent ($AGENT_NAME)
EOF

# Customize MEMORY.md
cat > "$BASE_DIR/workspace/MEMORY.md" << EOF
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
- **Workspace:** /opt/weagents/agents/$AGENT_NAME/

### Configured Tools
| Tool | Status | Details |
|------|--------|---------|
| — | — | — |

## Key Insights

*To be populated over time*
EOF

# Customize TODO.md
cat > "$BASE_DIR/workspace/TODO.md" << EOF
# TODO.md - Active Tasks

## Active

*No active tasks*

## Backlog

- [ ] Learn user's specific workflows
- [ ] Configure external integrations

## Completed

- [x] Initial workspace setup ($DATE)
EOF

# Create first daily note
cat > "$BASE_DIR/workspace/memory/$DATE.md" << EOF
# $DATE

## $TIME UTC - Workspace Created

Agent workspace initialized for $AGENT_NAME.
- All core files created
- Directory structure set up
- Ready for first interaction
EOF

# Customize stream.md
cat > "$BASE_DIR/workspace/stream.md" << EOF
# stream.md — Stream of Consciousness

---

**[$DATE $TIME UTC]** — Initialization

Workspace created. Ready to begin operations. Awaiting first interaction.

---
EOF

# Set permissions
echo -e "${YELLOW}Setting permissions...${NC}"
chmod 700 "$BASE_DIR/.config"
find "$BASE_DIR/.config" -type d -exec chmod 700 {} \; 2>/dev/null || true

echo ""
echo -e "${GREEN}=== Agent Created Successfully! ===${NC}"
echo ""
echo -e "${BLUE}Agent Name:${NC} $AGENT_NAME"
echo -e "${BLUE}Agent ID:${NC} $AGENT_ID"
echo -e "${BLUE}Location:${NC} $BASE_DIR"
echo ""
echo -e "${BLUE}Files Created:${NC}"
find "$BASE_DIR" -type f | while read f; do
    echo "  ✓ ${f#$BASE_DIR/}"
done
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Review and customize the files in workspace/"
echo "  2. Configure API keys in .config/"
echo "  3. Update TOOLS.md with your integrations"
echo "  4. Start the agent container"
echo ""
echo -e "${GREEN}Done!${NC}"
