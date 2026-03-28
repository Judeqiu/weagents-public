---
name: skill-downloader
description: Download specific skills from a remote OpenClaw VM to your local ./skills/ folder. Use when you need to copy a skill from a remote server to your local machine for backup, editing, or redistribution.
version: 1.0.0
---

# Skill Downloader

Download skills FROM a remote OpenClaw VM TO your local `./skills/` folder. This is useful when:

- You want to backup skills from a remote VM
- You need to edit a skill that's only on a remote server
- You want to redistribute a skill that's installed on a VM

## How It Works

1. Connects to the remote VM via SSH
2. Uses `tar` to archive the skill folder on the remote machine
3. Streams the archive back via SSH
4. Extracts it to your local `./skills/` folder

## Quick Usage

```bash
# Download a skill from default host (kai)
./download.py lextok-search

# Download multiple skills
./download.py lextok-search producthunter caddy-manager

# Download from specific host
./download.py marketing-creator --host enraie

# Download to a specific local directory
./download.py lextok-search --output ./my-skills/
```

## Requirements

- SSH access to the remote host (configured in `~/.ssh/config`)
- `tar` command available on the remote VM

## How to Download a Skill

### Step 1: Check Available Skills on Remote

First, see what skills are available on the remote VM:

```bash
ssh kai "ls ~/.openclaw/workspace/skills/"
```

### Step 2: Download the Skill

Run the download script:

```bash
cd ~/.config/agents/skills/skill-downloader
./download.py lextok-search
```

### Step 3: Verify Local Copy

Check that the skill was downloaded:

```bash
ls -la ./skills/lextok-search/
cat ./skills/lextok-search/SKILL.md | head -20
```

## Command Reference

| Command | Description |
|---------|-------------|
| `./download.py SKILL` | Download skill from default host |
| `./download.py SKILL1 SKILL2` | Download multiple skills |
| `./download.py SKILL --host HOST` | Download from specific host |
| `./download.py SKILL --output DIR` | Download to specific directory |
| `./download.py SKILL --force` | Overwrite if exists locally |

## Workflow Example

### Download a Skill for Editing

```bash
# Download skill from kai to local
./download.py lextok-search

# Edit the skill locally
vim ./skills/lextok-search/SKILL.md

# Deploy updated skill back to kai
./deploy.py lextok-search --host kai
```

### Backup All Skills from Remote

```bash
# Get list of skills from remote
SKILLS=$(ssh kai "ls ~/.openclaw/workspace/skills/" | tr '\n' ' ')

# Download all
./download.py $SKILLS
```

## Configuration

### Default Host

Set default host in the script or use `--host` flag:

```bash
# Set default to enraie
DEFAULT_HOST = "enraie"
```

### Output Directory

Default output is `./skills/` (relative to where you run the script).

Change with `--output`:
```bash
./download.py lextok-search --output /path/to/skills/
```

## Troubleshooting

### "SSH connection failed"

Make sure the host is configured in `~/.ssh/config`:
```
Host kai
    HostName 15.204.118.66
    User ubuntu
```

### "Skill not found on remote"

Check available skills:
```bash
ssh kai "ls ~/.openclaw/workspace/skills/"
```

### "Permission denied"

Ensure you have read access to the skills directory on the remote VM.

## Comparison with Other Tools

| Tool | Direction | Use Case |
|------|-----------|----------|
| **skill-downloader** | VM → Local | Copy skills from VM to local machine |
| **skill-puller** | GitHub → VM | Download skills from GitHub to VM |
| **skill-deployer** | Local → VM | Upload local skills to VM |

## Directory Structure

```
./skills/
├── skill-downloader/
│   ├── SKILL.md
│   └── download.py
├── lextok-search/        # Downloaded skills go here
│   ├── SKILL.md
│   └── ...
└── producthunter/
    ├── SKILL.md
    └── ...
```

## Notes

- Skills are downloaded via `tar` archive to preserve file permissions
- Large skills may take longer to download
- Existing local skills are preserved unless `--force` is used
