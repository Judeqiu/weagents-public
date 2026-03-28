---
name: skill-puller
description: Download and install skills from the GitHub repository to this OpenClaw instance. Use when you need to get a skill from GitHub, install a new skill, or update an existing skill. Fast download using git sparse-checkout.
version: 1.0.0
---

# Skill Puller - For OpenClaw Agents

This skill allows YOU (the OpenClaw agent) to download and install skills directly from the GitHub repository to this VM.

## When to Use This Skill

- You need a skill that is not currently installed
- You want to update an existing skill to the latest version
- The user asks you to install a specific skill from GitHub

## Prerequisites (IMPORTANT)

⚠️ **The GitHub repository MUST be public** for this to work.

If the repository is private, ask the user to use `skill-deployer` instead.

## How to Install a Skill - Step by Step

### Step 1: Check if the Skill Already Exists

First, check if the skill is already installed:

```bash
ls -la ~/.openclaw/workspace/skills/
```

If the skill exists and you want the latest version, use `--force` flag later.

### Step 2: Run the Pull Script

Navigate to the skill-puller directory and run the pull script:

```bash
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py SKILL_NAME
```

Replace `SKILL_NAME` with the actual skill name (e.g., `lextok-search`, `producthunter`, etc.)

### Step 3: Verify Installation

Check that the skill was downloaded successfully:

```bash
ls -la ~/.openclaw/workspace/skills/SKILL_NAME/
cat ~/.openclaw/workspace/skills/SKILL_NAME/SKILL.md | head -20
```

## Available Commands

### Install a Single Skill
```bash
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py lextok-search
```

### Install Multiple Skills at Once
```bash
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py lextok-search producthunter marketing-creator
```

### Force Re-install (Update Existing Skill)
```bash
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py lextok-search --force
```

### List All Available Skills
```bash
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py --list
```

## Workflow for Installing a New Skill

When the user asks you to install a skill, follow this workflow:

### 1. Ask for the Skill Name (if not provided)

> "Which skill would you like me to install? You can check available skills with `./pull.py --list`"

### 2. Check Current Skills

```bash
ls ~/.openclaw/workspace/skills/
```

### 3. Install the Skill

```bash
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py SKILL_NAME
```

### 4. Confirm Success

```bash
ls ~/.openclaw/workspace/skills/SKILL_NAME/
```

### 5. Report to User

> "✅ Successfully installed `SKILL_NAME` skill. It's now available at `~/.openclaw/workspace/skills/SKILL_NAME/`"

## Example Scenarios

### Scenario 1: User asks "Install the lextok-search skill"

```bash
# Check if already exists
ls ~/.openclaw/workspace/skills/ | grep lextok-search

# If not found, install it
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py lextok-search

# Verify
ls ~/.openclaw/workspace/skills/lextok-search/
```

### Scenario 2: User asks "What skills are available?"

```bash
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py --list
```

Then show the list to the user and ask which one they want.

### Scenario 3: User asks "Update the producthunter skill"

```bash
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py producthunter --force
```

## Troubleshooting

### "Repository appears to be PRIVATE"

This means the GitHub repository is not public. Tell the user:

> "The repository appears to be private. Please either:
> 1. Make the repository public on GitHub, OR
> 2. Use `skill-deployer` from their local machine"

### "Skill not found in repository"

The skill name might be incorrect. List available skills:

```bash
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py --list
```

### "git not found"

Git will be auto-installed. Just wait for the installation to complete.

## Configuration

- **Default Host**: Runs on the current VM (no `--host` needed for OpenClaw)
- **Repository**: `https://github.com/Judeqiu/weagents.git`
- **Skills Path**: `~/.openclaw/workspace/skills/`

## How It Works (Technical Details)

1. Uses `git sparse-checkout` to download only the specific skill folder
2. Downloads directly from GitHub to `~/.openclaw/workspace/skills/`
3. Sets executable permissions on scripts automatically
4. Cleans up temporary files after download

## Comparison with Skill Deployer

| | Skill Puller | Skill Deployer |
|---|---|---|
| **Source** | GitHub repository | Local machine |
| **Who runs it** | OpenClaw agent on VM | User on their computer |
| **Speed** | Fast (direct download) | Depends on upload speed |
| **Repo requirement** | Must be public | Works with private repos |
| **Use case** | Get latest from GitHub | Deploy local changes |

## Quick Reference Card

```bash
# INSTALL SKILL
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py SKILL_NAME

# INSTALL MULTIPLE
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py skill1 skill2 skill3

# UPDATE (force re-download)
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py SKILL_NAME --force

# LIST AVAILABLE
cd ~/.openclaw/workspace/skills/skill-puller
./pull.py --list

# CHECK INSTALLED SKILLS
ls ~/.openclaw/workspace/skills/
```

## Important Notes for Agents

1. **Always check if skill exists first** - Avoid unnecessary re-downloads
2. **Use `--force` for updates** - To get the latest version of an existing skill
3. **Report errors clearly** - If the repo is private, explain the situation to the user
4. **Verify after installation** - Always check the skill directory was created
5. **This VM only** - The skill is installed on THIS VM, not user's local machine
