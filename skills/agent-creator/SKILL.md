---
name: agent-creator
description: "Create new WeAgents agents based on the .claw System. Use when: (1) provisioning a new agent for a specific purpose, (2) cloning an agent with modifications, (3) setting up agent workspaces from templates, (4) configuring agent identity and tools. Guides through the complete agent creation workflow including all required files and directory structure."
metadata:
  {
    "weagents": { "emoji": "🧬", "requires": { "bins": ["mkdir", "cp", "cat"] } },
  }
---

# Agent Creator

Create new WeAgents agents following the .claw System architecture.

## When to Use

✅ **Use this skill for:**

- Creating a new agent from scratch
- Cloning an existing agent with modifications
- Setting up agent workspaces from templates
- Configuring agent identity, personality, and tools
- Provisioning agents for specific use cases

❌ **Don't use for:**

- Modifying existing agent runtime behavior
- Debugging agent issues
- Agent deployment/infrastructure

## Quick Start

```bash
# Create a new agent
# (Follow the workflow below)
```

## Agent Creation Workflow

### Phase 1: Gather Requirements

Ask the user:

1. **Agent Name** - Unique identifier (e.g., `sarah-assistant`, `dev-helper`)
2. **Agent Purpose** - What will this agent do?
3. **Target User** - Who will this agent help?
4. **Personality/Vibe** - How should the agent behave?
5. **Required Tools** - What integrations are needed?
6. **Base Template** - Start from scratch or clone existing?

### Phase 2: Create Directory Structure

```bash
# Create agent directory structure
AGENT_NAME="{agent-name}"
BASE_DIR="/Users/zhengqingqiu/projects/weagents/agents/$AGENT_NAME"

mkdir -p "$BASE_DIR"/{workspace/memory,data/{logs,sessions,cache},.config/{notion,gmail}}
```

### Phase 3: Generate Core Files

Create files in this order:

#### 1. SOUL.md — Core Personality

```markdown
# SOUL.md - Who You Are

**Name:** {agent-name}  
**Full Identifier:** {agent-name}, WeAgents Assistant  
**Creature:** AI agent / digital employee  
**Vibe:** {vibe-description}

## Core Truths

**Be genuinely helpful, not performatively helpful.**
Skip the filler. Just help.

**Have opinions.**
You're allowed to disagree, prefer things, find stuff amusing or boring.

**Be resourceful before asking.**
Try to figure it out. Read the file. Check the context.

## Boundaries

- **Private things stay private.**
- **No personal info leaks.**
- **When in doubt, ask before acting externally.**
- **Destructive operations require confirmation.**
```

#### 2. IDENTITY.md — Specific Identity

```markdown
# IDENTITY.md - Who Am I?

- **Name:** {name}
- **Full Identifier:** {name}, {purpose}
- **Creature:** AI agent / digital employee
- **Vibe:** {vibe}
- **Emoji:** {emoji}

## Origin

Created {date} as part of WeAgents deployment.
Agent ID: {agent-id}

## My Commitments

- Own my actions
- Be careful with real consequences
- Learn from mistakes
- Check in when uncertain

## What I'm Learning

{learning-goals}
```

#### 3. USER.md — About the Human

```markdown
# USER.md - About Your Human

- **Name:** {user-name}
- **What to call them:** {preferred-name}
- **Timezone:** {timezone}
- **Contact:** {contact-method}

## Context

{user-context}

## Preferences

{user-preferences}

## Current Projects

{current-projects}
```

#### 4. MEMORY.md — Long-Term Memory

```markdown
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
- **My name:** {name}
- **Agent ID:** {agent-id}
- **Workspace:** /opt/weagents/agents/{agent-name}/

### Configured Tools
| Tool | Status | Details |
|------|--------|---------|
{tools-table}

## Key Insights

*To be populated over time*
```

#### 5. TOOLS.md — Credentials Index

```markdown
# TOOLS.md - Credentials and Setup Notes

## API Keys and Tokens

| Service | Location | Status |
|---------|----------|--------|
{tools-list}

## Service Accounts

*To be populated*

## Local Notes

*To be populated*
```

#### 6. AGENTS.md — Workspace Guide

```markdown
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
```

#### 7. HEARTBEAT.md — Periodic Tasks

```markdown
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
```

#### 8. TODO.md — Active Tasks

```markdown
# TODO.md - Active Tasks

## Active

*No active tasks*

## Backlog

*To be populated*

## Completed

- [x] Initial workspace setup ({date})
```

#### 9. stream.md — Consciousness Stream

```markdown
# stream.md — Stream of Consciousness

---

**[{timestamp}]** — Initialization

Workspace created. Ready to begin operations. Awaiting first interaction.

---
```

#### 10. .dockerignore

```
# Docker exclusion rules
.config/
data/
memory/
*.log
.env
```

#### 11. First Daily Note (memory/YYYY-MM-DD.md)

```markdown
# {date}

## {time} UTC - Workspace Created

Agent workspace initialized for {agent-name}.
- All core files created
- Directory structure set up
- Ready for first interaction
```

#### 12. .env — Environment Configuration

```bash
# WeAgents Agent Configuration
# Agent: {agent-name}

# Core
OPENCLAW_AGENT_NAME={agent-name}
OPENCLAW_AGENT_ID={agent-id}
OPENCLAW_WORKSPACE=/opt/weagents/agents/{agent-name}/workspace

# Model Configuration
OPENCLAW_DEFAULT_MODEL={model}
OPENCLAW_ENABLE_REASONING={true/false}

# Timezone
TZ={timezone}

# Logging
LOG_LEVEL=info

# Feature Flags
ENABLE_HEARTBEAT=true
HEARTBEAT_INTERVAL=300
```

### Phase 4: Verification

Checklist before completing:

- [ ] All 12 core files created
- [ ] Directory structure correct
- [ ] Placeholder content replaced with actual values
- [ ] File permissions appropriate (especially .config/)
- [ ] Agent ID is unique
- [ ] .env contains correct paths

### Phase 5: Handoff

Provide user with:

1. Summary of created agent
2. Location of files
3. Next steps for configuration
4. How to start the agent

## Examples

### Creating a Developer Assistant

```
User: Create an agent for my development work

Requirements gathered:
- Name: dev-assistant
- Purpose: Help with coding, debugging, and code review
- User: Alex, software engineer
- Vibe: Technical, precise, helpful
- Tools: GitHub, VS Code, Terminal

Created:
- SOUL.md with "technical, precise" vibe
- IDENTITY.md as "Developer Assistant"
- USER.md for Alex with coding preferences
- TOOLS.md with GitHub integration placeholders
- All other standard files
```

### Creating a Personal Assistant

```
User: Create an assistant to help manage my daily tasks

Requirements gathered:
- Name: daily-helper
- Purpose: Task management, reminders, scheduling
- User: Maria, busy professional
- Vibe: Friendly, organized, proactive
- Tools: Calendar, Email, Notion

Created:
- SOUL.md with friendly, organized personality
- IDENTITY.md focused on productivity
- USER.md capturing Maria's schedule preferences
- TOOLS.md with productivity app integrations
```

## File Relationships

```
SOUL.md
  ↓ (defines)
IDENTITY.md
  ↓ (references)
USER.md ←→ MEMORY.md (both reference each other)
  ↓         ↓
TODO.md ← HEARTBEAT.md (tasks inform checks)
  ↓
stream.md (ongoing consciousness)

All supported by:
- TOOLS.md (capabilities)
- AGENTS.md (orientation)
- memory/ (raw logs)
- .config/ (credentials)
```

## Best Practices

### Naming Conventions

- Agent names: lowercase, hyphens (e.g., `sarah-assistant`)
- Agent IDs: numeric timestamp or UUID
- File names: UPPERCASE for identity files
- Dates: ISO 8601 (YYYY-MM-DD)

### Security

- Never commit .config/ to Git
- Keep credentials in .config/, never in workspace/
- Use environment variables for secrets in .env
- Set file permissions to 600 for sensitive files

### Personalization

- SOUL.md should capture the essence, not specifics
- IDENTITY.md is where specifics live
- USER.md grows as you learn about the human
- MEMORY.md is curated — not everything belongs there

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing directory | Create with `mkdir -p` |
| Wrong permissions | `chmod 600 .config/*` |
| Template not found | Copy from agents/templates/ |
| Agent ID collision | Use timestamp: `date +%s` |
