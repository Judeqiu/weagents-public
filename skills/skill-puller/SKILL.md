---
name: skill-puller
description: Download specific skills from GitHub repository to remote VMs. Fast, lightweight skill downloader using git sparse-checkout - only downloads the requested skill folder without cloning the entire repository. Requires public GitHub repository.
version: 1.0.0
---

# Skill Puller

Download specific skills from the GitHub repository directly to remote VMs. This is faster than skill-deployer because it downloads directly on the target VM using `git sparse-checkout`, avoiding the need to upload from local machine.

## Prerequisites

⚠️ **The GitHub repository must be PUBLIC for this tool to work.**

If the repository is private, use `skill-deployer` instead (which uploads from your local machine).

## How It Works

1. Uses `git sparse-checkout` to download only the specific skill folder from GitHub
2. Downloads directly on the remote VM (no local upload needed)
3. Places skill in `~/.openclaw/workspace/skills/`
4. Sets proper permissions automatically

## Quick Usage

```bash
# Pull a skill to default host (kai)
./pull.py lextok-search

# Pull multiple skills
./pull.py lextok-search producthunter caddy-manager

# Pull to specific host
./pull.py marketing-creator --host spost

# Force re-download (remove existing first)
./pull.py lextok-search --force

# List available skills
./pull.py --list
```

## Requirements

- GitHub repository must be **public**
- `git` command on remote VM (auto-installed if missing)
- SSH access to target hosts configured in `~/.ssh/config`

## Features

- ✅ **Fast** - Downloads only the skill folder, not entire repo
- ✅ **Lightweight** - No local dependencies, runs entirely on remote VM
- ✅ **Smart** - Skips download if skill already exists (use `--force` to override)
- ✅ **Multiple skills** - Can pull multiple skills in one command
- ✅ **Auto permissions** - Sets executable permissions on scripts

## Command Reference

| Command | Description |
|---------|-------------|
| `./pull.py SKILL` | Pull skill to default host |
| `./pull.py SKILL1 SKILL2` | Pull multiple skills |
| `./pull.py SKILL --host HOST` | Pull to specific host |
| `./pull.py SKILL --force` | Force re-download |
| `./pull.py --list` | List available skills on GitHub |

## GitHub Repository

- **Repo**: `https://github.com/Judeqiu/weagents`
- **Skills Path**: `trunk/skills/{skill-name}/`

## Comparison with Skill Deployer

| Feature | Skill Deployer | Skill Puller |
|---------|---------------|--------------|
| Source | Local files | GitHub repo |
| Upload method | SCP from local | Direct download on VM |
| Speed | Depends on local upload | Fast (direct download) |
| Use case | Deploy local changes | Get latest from GitHub |
| Network efficiency | Uploads from local | Downloads on VM |
