---
name: skill-discovery-helper
description: Use when needing to find, discover, or use OpenClaw skills. Helps the agent understand where skills are located, how to discover all available skills, and how to use skills from different sources. Essential for agents to find skills in ~/.openclaw/workspace/skills/.
---

# Skill Discovery Helper

Helps OpenClaw agents accurately find and use skills from all sources.

## The Problem

`<available_skills>` context is **INCOMPLETE**. It only shows bundled skills and misses:
- Skills in `~/.openclaw/workspace/skills/` (most custom skills)
- Skills from extraDirs configuration
- Agent-specific workspace skills

## The Solution

**ALWAYS use `openclaw skills list` to find ALL skills.**

## Quick Start

### Find All Available Skills

```bash
# List ALL skills with their sources
openclaw skills list
```

Example output:
```
✓ marketing-creator        (source: openclaw-extra)
✓ customer-research-agent  (source: openclaw-extra)
✓ mychrome                 (source: openclaw-extra)
✓ lazada-browser           (source: openclaw-workspace)
✓ fetch                    (source: openclaw-bundled)
✓ github                   (source: openclaw-bundled)
```

### Check What's Installed in Workspace

```bash
# List skills in workspace directory
ls ~/.openclaw/workspace/skills/
```

### Find a Specific Skill

```bash
# Search for skill by name
openclaw skills list | grep "skill-name"

# Or check workspace directly
ls ~/.openclaw/workspace/skills/ | grep "skill-name"
```

## Skill Locations

| Location | Path | Description |
|----------|------|-------------|
| **Bundled** | Built-in | Skills shipped with OpenClaw |
| **Extra** | `~/.openclaw/workspace/skills/` | **Main workspace skills directory** |
| **Workspace** | `~/.openclaw/agents/{agent}/workspace/skills/` | Agent-specific skills |

## Important: Workspace Skills Directory

**Most custom skills are installed here:**
```
~/.openclaw/workspace/skills/
```

Common skills in this directory:
- `customer-research-agent` - B2B customer research
- `mychrome` - Chrome CDP automation
- `marketing-creator` - Marketing content creation
- `lazada-browser` - Lazada Seller Center
- `shopee-seller` - Shopee Seller Centre
- `financial-analysis-core` - Financial analysis
- `skill-deployer` - Deploy skills to remote hosts

## How to Use This Skill

### Before Using Any Skill

1. **Run discovery command:**
   ```bash
   openclaw skills list
   ```

2. **Check workspace directory:**
   ```bash
   ls ~/.openclaw/workspace/skills/
   ```

3. **Verify skill exists** before claiming it doesn't

### When User Asks for a Skill

**DON'T say:** "That skill doesn't exist"

**DO:**
1. Run `openclaw skills list`
2. Check `ls ~/.openclaw/workspace/skills/`
3. Then respond with actual available skills

### Chrome/CDP Based Skills

These skills require Chrome to be running:
```bash
# Check Chrome CDP is accessible
curl http://localhost:9222/json/version

# Common CDP skills:
# - customer-research-agent
# - mychrome
# - lazada-browser
# - shopee-seller
```

## Skill Discovery Protocol

### For Every Session

1. **Read MEMORY.md** - Contains skill discovery protocol
2. **Check AGENTS.md** - May have skill-related instructions
3. **Run `openclaw skills list`** - Get current skill inventory

### When Skill Not Found

```bash
# Step 1: List all skills
openclaw skills list

# Step 2: Check workspace directory
ls -la ~/.openclaw/workspace/skills/

# Step 3: Check if extraDirs is configured
grep extraDirs ~/.openclaw/openclaw.json

# Step 4: Search for skill files
find ~/.openclaw -name "SKILL.md" 2>/dev/null | head -20
```

### If Skill is Missing

```bash
# Deploy from local skills repository
skill-deployer deploy skill-name --host kai

# Or clone from git
cd ~/.openclaw/workspace/skills/
git clone <skill-repo>

# Then restart gateway
systemctl --user restart openclaw-gateway
```

## Available Scripts

### list_skills.sh - List All Skills

```bash
./scripts/list_skills.sh
```

Shows:
- All skills from `openclaw skills list`
- Skills in workspace directory
- Skills by source (bundled, extra, workspace)

### find_skill.sh - Find a Specific Skill

```bash
./scripts/find_skill.sh skill-name
```

Searches:
- Bundled skills
- Workspace skills
- All SKILL.md files

### verify_discovery.sh - Verify Skill Discovery is Working

```bash
./scripts/verify_discovery.sh
```

Checks:
- extraDirs configuration
- Workspace directory exists
- Skills are discoverable

## Common Skill Sources

### Bundled Skills (Always Available)

```
fetch       - Web fetching
github      - GitHub integration
linear      - Linear issue tracking
netlify     - Netlify deployment
postgres    - PostgreSQL database
slack       - Slack messaging
```

### Common Workspace Skills

```
customer-research-agent  - B2B customer research with Chrome CDP
mychrome                 - Chrome CDP helper/bridge
marketing-creator        - Marketing content creation
skill-deployer          - Deploy skills to remote hosts
lazada-browser          - Lazada Seller Center automation
shopee-seller           - Shopee Seller Centre automation
financial-analysis-core - Financial data analysis
equity-research         - Equity research tools
provisionclaw           - OpenClaw server provisioning
```

## Troubleshooting

### "Skill doesn't exist"

**Problem:** Skill exists in workspace but agent can't find it

**Solution:**
```bash
# 1. Verify skill exists
ls ~/.openclaw/workspace/skills/skill-name/SKILL.md

# 2. Check extraDirs configuration
openclaw config get skills.load.extraDirs

# 3. If not set, configure it
openclaw config set skills.load.extraDirs '["/home/USERNAME/.openclaw/workspace/skills"]'

# 4. Restart gateway
systemctl --user restart openclaw-gateway

# 5. Verify discovery
openclaw skills list | grep skill-name
```

### Skills Not Showing in List

**Problem:** `openclaw skills list` doesn't show workspace skills

**Solution:**
```bash
# Check extraDirs is properly configured
cat ~/.openclaw/openclaw.json | grep -A 5 extraDirs

# Should show:
# "extraDirs": ["/home/ubuntu/.openclaw/workspace/skills"]

# If missing, add it:
openclaw config set skills.load.extraDirs '["/home/ubuntu/.openclaw/workspace/skills"]'
systemctl --user restart openclaw-gateway
```

### Agent Still Can't Find Skill

**Problem:** Agent claims skill doesn't exist even after discovery

**Solution:**
1. Make sure agent read MEMORY.md at session start
2. Ensure AGENTS.md references skill discovery protocol
3. Remind agent to run `openclaw skills list` before skill tasks

## Memory Integration

### Update MEMORY.md

Add this to `~/.openclaw/workspace/MEMORY.md`:

```markdown
## Skill Discovery Protocol

### Workspace Skills Location
**Skills are installed in:** `~/.openclaw/workspace/skills/`

### Discovery Command
**ALWAYS run:** `openclaw skills list`

### Common Workspace Skills
- customer-research-agent - B2B research
- mychrome - Chrome CDP helper
- marketing-creator - Marketing content
- skill-deployer - Deploy skills

### Chrome/CDP Skills
These need Chrome running:
```bash
curl http://localhost:9222/json/version
```
```

### Update AGENTS.md

Add to `~/.openclaw/workspace/AGENTS.md`:

```markdown
## Skill Discovery (CRITICAL)

Before using any skill:
1. Run `openclaw skills list` to see ALL skills
2. Check `~/.openclaw/workspace/skills/` for custom skills
3. Remember `<available_skills>` is INCOMPLETE

Common workspace skills: customer-research-agent, mychrome, marketing-creator
```

## Best Practices

1. **Always discover first** - Run `openclaw skills list` before claiming a skill doesn't exist
2. **Check workspace** - Most skills are in `~/.openclaw/workspace/skills/`
3. **Verify Chrome** - CDP skills need Chrome running on port 9222
4. **Read memory** - MEMORY.md contains skill inventory
5. **Keep inventory updated** - Add new skills to MEMORY.md

## Files

| File | Purpose |
|------|---------|
| `scripts/list_skills.sh` | List all skills by source |
| `scripts/find_skill.sh` | Find specific skill |
| `scripts/verify_discovery.sh` | Verify discovery is working |
| `SKILL.md` | This documentation |
