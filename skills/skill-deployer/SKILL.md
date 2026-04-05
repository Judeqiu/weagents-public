---
name: skill-deployer
description: Deploy any skill to OpenClaw agents on remote VMs via SSH. Deploys to ~/.openclaw/workspace/skills/ where OpenClaw discovers skills. Use when you need to install, update, or manage skills on OpenClaw instances.
version: 1.0.2
---

**Version:** 1.0.3  
**Last Updated:** 2026-03-22

### Changelog

**v1.0.3 (2026-03-22)**
- **Documented as universal skill deployer** - explicitly states it works with ANY skill
- Added "Finding Skills Automatically" section explaining search algorithm
- Added examples showing deployment of various different skills
- Clarified that only requirement is a `SKILL.md` file

**v1.0.2 (2026-03-22)**
- **Enhanced clean deploy process** with explicit 5-step workflow:
  1. Check and delete existing skill
  2. Copy fresh skill files
  3. Set executable permissions
  4. Install dependencies (if requested)
  5. Verify deployment
- Added detailed progress logging for each deployment step
- Ensures no stale files remain from previous deployments

**v1.0.1 (2026-03-22)**
- Fixed documentation to consistently reference `~/.openclaw/workspace/skills/` as the only deployment target
- Removed all references to `~/.config/agents/skills/` which was incorrect

# Skill Deployer

**Deploy ANY skill to OpenClaw agents on remote VMs via SSH.**

This is a **universal skill deployer** - it works with any skill that follows the standard structure. Simply provide the skill name or path, and it handles the deployment logistics including:
- Finding the skill locally (searches multiple locations)
- Connecting to remote hosts via SSH
- Cleaning existing deployments (removes old files)
- Copying fresh files
- Setting permissions
- Installing dependencies
- Verifying the deployment

Works with any skill: `marketing-creator`, `financial-analysis-core`, `my-custom-skill`, etc.

## Quick Deploy

**Deploy Path:** `~/.openclaw/workspace/skills/` (OpenClaw's skill discovery directory)

### Finding Skills Automatically

The deployer searches for skills in this order:

1. **Direct path** - If you provide a full path: `./deploy.py /path/to/my-skill`
2. **Current directory** - `./my-skill/`
3. **Parent directory** - `../my-skill/` (useful if deployer is in `skill-deployer/` and skills are in `skills/`)
4. **Config source path** - From `config.json` `skills_source_path`
5. **Name variants** - Tries both `my-skill` and `my_skill`

As long as the directory contains a `SKILL.md` file, the deployer will find it.

**⚠️ IMPORTANT: The deployer ALWAYS does a clean redeploy by default.**
This means it will:
1. Remove the entire existing skill directory on the remote host
2. Copy ALL files fresh from local
3. This ensures no stale files remain

```bash
# Deploy a skill to default host (kai) - CLEAN REDEPLOY to ~/.openclaw/workspace/skills/
./deploy.py my-skill

# Deploy to specific host
./deploy.py my-skill --host weagents

# Deploy from specific source directory
./deploy.py my-skill --source /path/to/my-skill

# Deploy and verify
./deploy.py my-skill --verify
```

## Deploy Multiple Skills

```bash
# Deploy multiple skills at once
./deploy.py skill1 skill2 skill3

# Deploy all skills from a directory
./deploy.py --all --source /path/to/skills/
```

## List Remote Skills

```bash
# List skills on default host
./deploy.py --list

# List skills on specific host
./deploy.py --list --host kai
```

## Remove Skills

```bash
# Remove a skill from remote host
./deploy.py --remove my-skill

# Remove from specific host
./deploy.py --remove my-skill --host weagents
```

## Configuration

### Target Hosts

Target hosts are read from `~/.ssh/config`. The deployer uses SSH aliases defined there.

```
Host kai
    HostName 15.204.118.66
    User ubuntu

Host weagents
    HostName 152.42.253.91
    User ubuntu
```

### Default Settings

Create `config.json` to customize defaults:

```json
{
  "default_host": "kai",
  "skills_source_path": "/path/to/skills",
  "remote_skills_path": "~/.openclaw/workspace/skills",
  "verify_after_deploy": true,
  "restart_agent_after_deploy": false
}
```

**Note:** The default `remote_skills_path` is `~/.openclaw/workspace/skills` which is where OpenClaw discovers skills.

## How It Works

The deployer follows a strict **5-step clean deployment process**:

### Deployment Steps

1. **Source Discovery** - Finds skill directory locally (by name or path)
2. **SSH Connection** - Connects to target host using SSH config
3. **Base Directory Creation** - Creates `~/.openclaw/workspace/skills/` if needed

### The Clean Deploy Process (Always Executed)

**STEP 1: Delete Existing Skill**
- Checks if skill already exists on remote host
- If yes: Completely removes the old skill directory (`rm -rf`)
- If no: Continues with fresh deploy
- **Purpose:** Ensures no stale files remain

**STEP 2: Copy Fresh Files**
- Copies ALL skill files from local to remote via SCP
- Preserves directory structure
- **Purpose:** Deploys the complete, up-to-date skill

**STEP 3: Set Permissions**
- Makes Python scripts executable (`chmod +x *.py`)
- Makes shell scripts executable (`chmod +x *.sh`)
- **Purpose:** Ensures scripts can be run

**STEP 4: Install Dependencies** (if `--install-deps` flag used)
- Installs packages from `requirements.txt` if present
- Uses `--break-system-packages` if needed
- **Purpose:** Ensures Python dependencies are available

**STEP 5: Verify Deployment**
- Confirms skill directory exists
- Confirms `SKILL.md` is present
- Reports success/failure
- **Purpose:** Validates the deployment worked

### Result
- Skill is automatically discoverable by OpenClaw in `~/.openclaw/workspace/skills/`
- No stale files from previous versions
- Clean, reproducible deployments every time

## Required Skill Structure

For a skill to be deployable, it needs:

```
my-skill/
├── SKILL.md           # Required - skill definition with name/description
├── *.py               # Optional - Python scripts
├── *.sh               # Optional - Shell scripts
├── requirements.txt   # Optional - Python dependencies
└── ...                # Other supporting files
```

The `SKILL.md` must have YAML front matter:

```yaml
---
name: my-skill-name
description: Clear description of what this skill does
---
```

## Deployment Examples

### Deploy ANY Skill

The deployer works with any skill that has a `SKILL.md` file:

```bash
# Deploy marketing-creator skill
./deploy.py marketing-creator

# Deploy financial-analysis-core
./deploy.py financial-analysis-core

# Deploy your custom skill
./deploy.py my-custom-skill

# Deploy by full path
./deploy.py /path/to/any/skill-directory
```

### Deploy to Multiple Hosts

```bash
# Deploy to kai and weagents
./deploy.py marketing-creator --host kai --host weagents

# Deploy to all configured hosts
./deploy.py marketing-creator --all-hosts
```

### Deploy Multiple Skills at Once

```bash
# Deploy multiple skills to the same host
./deploy.py marketing-creator financial-analysis-core investment-banking

# Deploy multiple skills to multiple hosts
./deploy.py skill1 skill2 skill3 --host kai --host weagents
```

### Update Existing Skill (Clean Redeploy)

```bash
# Same as deploy - removes old files and copies fresh
./deploy.py marketing-creator

# The deployer ALWAYS does a clean redeploy by default
```

### Deploy with Dependencies

```bash
# Install Python requirements on remote host
./deploy.py marketing-creator --install-deps
```

## Verification

The deployer can verify that a skill was deployed correctly:

```bash
# Verify specific skill
./deploy.py --verify my-skill

# Verify all skills on host
./deploy.py --verify-all --host kai
```

Verification checks:
- SKILL.md exists and is readable
- Required files are present
- Scripts are executable
- Python dependencies are installed (if applicable)

## Troubleshooting

### SSH Connection Issues

```bash
# Test SSH connection to host
ssh -G kai

# Verify host is reachable
./deploy.py --test-connection kai
```

### Permission Denied

Make sure the remote user has write access to `~/.openclaw/workspace/skills/`:

```bash
ssh kai "mkdir -p ~/.openclaw/workspace/skills && chmod 755 ~/.openclaw/workspace/skills"
```

### Skill Not Discoverable

OpenClaw scans `~/.openclaw/workspace/skills/` for SKILL.md files. Verify:

```bash
ssh kai "ls -la ~/.openclaw/workspace/skills/my-skill/SKILL.md"
```

## Command Reference

| Command | Description |
|---------|-------------|
| `./deploy.py SKILL` | Deploy skill to default host |
| `./deploy.py SKILL --host HOST` | Deploy to specific host |
| `./deploy.py --list` | List deployed skills |
| `./deploy.py --remove SKILL` | Remove a skill |
| `./deploy.py --verify SKILL` | Verify skill deployment |
| `./deploy.py --all` | Deploy all skills from source path |
| `./deploy.py --test-connection HOST` | Test SSH connectivity |

## Requirements

- SSH access to target hosts (configured in `~/.ssh/config`)
- Python 3.8+ on both local and remote hosts
- `scp` command for file transfers
