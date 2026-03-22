---
name: remote-ops
description: "Remote server operations via SSH. Use when: (1) creating agents on remote VMs, (2) managing remote infrastructure, (3) deploying to remote servers, (4) executing commands on remote machines, (5) syncing files to/from remote hosts. Supports SSH key-based auth, command execution, file transfer, and agent provisioning on remote systems. Works with weagents and oraora servers."
metadata:
  {
    "weagents": { "emoji": "🌐", "requires": { "bins": ["ssh", "scp", "rsync"] } },
    "oraora": { "emoji": "📚", "requires": { "bins": ["ssh", "scp", "rsync"] } }
  }
---

# Remote Operations

Execute commands and manage resources on remote servers via SSH.

## When to Use

✅ **Use this skill for:**

- Creating agents on remote VMs/servers
- Executing commands on remote machines
- Transferring files to/from remote hosts
- Setting up remote infrastructure
- Deploying configurations to remote systems
- Managing remote agent workspaces

❌ **Don't use for:**

- Local operations (use direct commands)
- Complex orchestration across many nodes (use proper orchestration tools)
- Persistent connections/interactive sessions (use tmux/screen)

## Prerequisites

### SSH Access Requirements

Before using this skill, ensure:

1. **SSH access is configured:**
   - SSH key-based authentication (preferred)
   - Or password auth (less secure)
   - Bastion/jump host if needed

2. **Required binaries on remote host:**
   - `bash` or compatible shell
   - `mkdir`, `cp`, `cat`, `chmod`
   - `tar` or `rsync` (for file transfers)

3. **Network connectivity:**
   - SSH port (22) accessible
   - No firewall blocking connections

## Configuration

### SSH Config File (~/.ssh/config)

```
Host my-vm
    HostName 192.168.1.100
    User ubuntu
    IdentityFile ~/.ssh/id_rsa
    StrictHostKeyChecking accept-new

Host weagents-prod
    HostName prod.example.com
    User weagent
    IdentityFile ~/.ssh/weagents_prod_key
    ProxyJump bastion-host

# Pre-configured servers
Host weagents
    HostName 152.42.253.91
    User root
    IdentityFile ~/.ssh/id_ed25519_weagents
    StrictHostKeyChecking accept-new

Host oraora
    HostName 15.204.234.93
    User jude
    IdentityFile ~/.ssh/id_ed25519_weagents
    StrictHostKeyChecking accept-new
```

### Environment Variables

```bash
# Default SSH options
export SSH_USER=ubuntu
export SSH_KEY=~/.ssh/id_rsa
export REMOTE_HOST=192.168.1.100
export REMOTE_BASE_PATH=/opt/weagents
```

## Quick Start

### 1. Test Connectivity

```bash
ssh -o ConnectTimeout=5 user@host "echo 'Connected successfully'"
```

### 2. Execute Remote Command

```bash
ssh user@host "ls -la /opt/weagents/agents/"
```

### 3. Transfer Files

```bash
# Local to remote
scp -r ./local-dir user@host:/remote/path/

# Remote to local
scp -r user@host:/remote/path/ ./local-dir/
```

## Workflows

### Create Agent on Remote VM

```bash
# Step 1: Ensure remote directory exists
ssh user@host "mkdir -p /opt/weagents/agents"

# Step 2: Generate agent files locally first
./skills/agent-creator/scripts/create-agent.sh remote-agent \
    --purpose "Remote operations assistant" \
    --user "RemoteUser" \
    --timezone "UTC"

# Step 3: Transfer to remote
scp -r ./agents/remote-agent user@host:/opt/weagents/agents/

# Step 4: Verify on remote
ssh user@host "ls -la /opt/weagents/agents/remote-agent/workspace/"
```

### Remote Agent Setup Script

```bash
#!/bin/bash
# setup-remote-agent.sh - Run on remote host

AGENT_NAME="$1"
AGENT_PURPOSE="$2"
USER_NAME="$3"

if [ -z "$AGENT_NAME" ]; then
    echo "Usage: $0 <agent-name> [purpose] [user-name]"
    exit 1
fi

BASE_DIR="/opt/weagents/agents/$AGENT_NAME"

# Create directory structure
mkdir -p "$BASE_DIR"/{workspace/memory,data/{logs,sessions,cache},.config}

# Create .env
cat > "$BASE_DIR/.env" << EOF
OPENCLAW_AGENT_NAME=$AGENT_NAME
OPENCLAW_AGENT_ID=$(date +%s)
OPENCLAW_WORKSPACE=/opt/weagents/agents/$AGENT_NAME/workspace
OPENCLAW_DEFAULT_MODEL=anthropic/claude-3-opus
TZ=UTC
EOF

echo "Agent $AGENT_NAME created at $BASE_DIR"
```

Run remotely:
```bash
scp setup-remote-agent.sh user@host:/tmp/
ssh user@host "bash /tmp/setup-remote-agent.sh my-agent 'Dev helper' 'Alex'"
```

### Sync Local Agent to Remote

```bash
AGENT_NAME="my-agent"
REMOTE_HOST="user@vm.example.com"
REMOTE_PATH="/opt/weagents/agents"

# Sync workspace (exclude data and .config)
rsync -avz --exclude='data/' --exclude='.config/' \
    "./agents/$AGENT_NAME/" \
    "$REMOTE_HOST:$REMOTE_PATH/$AGENT_NAME/"

# Verify
ssh "$REMOTE_HOST" "ls -la $REMOTE_PATH/$AGENT_NAME/workspace/"
```

### Remote Command Execution Patterns

**Single command:**
```bash
ssh user@host "cd /opt/weagents && ls -la"
```

**Multiple commands:**
```bash
ssh user@host '
    cd /opt/weagents/agents
    for dir in */; do
        echo "Agent: $dir"
        ls "$dir"workspace/TODO.md 2>/dev/null && echo "  ✓ Has TODO"
    done
'
```

**With environment variables:**
```bash
ssh user@host "export VAR=value && echo \$VAR"
```

## Common Operations

### Check Remote Agent Status

```bash
ssh user@host '
    for agent in /opt/weagents/agents/*/; do
        name=$(basename "$agent")
        if [ -f "$agent/workspace/TODO.md" ]; then
            echo "✓ $name: active"
        else
            echo "✗ $name: incomplete setup"
        fi
    done
'
```

### Backup Remote Agents

```bash
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
ssh user@host "tar czf /tmp/weagents-backup-$BACKUP_DATE.tar.gz -C /opt weagents/agents"
scp user@host:/tmp/weagents-backup-$BACKUP_DATE.tar.gz ./backups/
```

### Deploy Agent Update

```bash
AGENT="target-agent"
REMOTE="user@host"

# Update specific file
scp "./agents/$AGENT/workspace/SOUL.md" "$REMOTE:/opt/weagents/agents/$AGENT/workspace/"

# Restart agent (if using systemd/docker)
ssh "$REMOTE" "sudo systemctl restart weagent-$AGENT"
```

## Safety Guidelines

### Before Executing Remote Commands

- [ ] Verify correct host (check hostname/IP)
- [ ] Verify user has appropriate permissions
- [ ] Test with non-destructive command first
- [ ] Have rollback plan

### File Transfer Safety

- Never transfer `.config/` with credentials to untrusted locations
- Use `rsync --dry-run` first to preview changes
- Verify checksums for critical files

### SSH Security

- Use key-based authentication only
- Keep private keys secure (chmod 600)
- Use jump hosts/bastions for production
- Verify host keys on first connect

## Troubleshooting

### Connection Issues

```bash
# Test basic connectivity
ssh -v user@host "echo test"

# Check SSH config
ssh -G user@host

# Test with explicit key
ssh -i ~/.ssh/specific_key user@host
```

### Permission Denied

```bash
# Fix key permissions
chmod 600 ~/.ssh/id_rsa

# Check remote user exists
ssh user@host "whoami"

# Check sudo access
ssh user@host "sudo -l"
```

### Path Issues

```bash
# Use absolute paths
ssh user@host "cd /opt/weagents && pwd"

# Check path exists
ssh user@host "test -d /opt/weagents && echo exists || echo missing"
```

## Scripts

Located in `scripts/`:

| Script | Purpose | Example |
|--------|---------|---------|
| `remote-create-agent.sh` | Create agent on remote host | `./remote-create-agent.sh user@host my-agent` |
| `remote-sync-agent.sh` | Sync local agent to remote | `./remote-sync-agent.sh user@host my-agent` |
| `remote-list-agents.sh` | List agents on remote | `./remote-list-agents.sh user@host` |

## Examples

### Full Remote Agent Creation

```bash
# 1. Define variables
REMOTE="ubuntu@192.168.1.100"
AGENT_NAME="prod-helper"
AGENT_PURPOSE="Production support assistant"
USER_NAME="DevOps Team"

# 2. Ensure remote directory exists
ssh "$REMOTE" "sudo mkdir -p /opt/weagents/agents && sudo chown \$USER:\$USER /opt/weagents/agents"

# 3. Create agent structure locally
./skills/agent-creator/scripts/create-agent.sh "$AGENT_NAME" \
    --purpose "$AGENT_PURPOSE" \
    --user "$USER_NAME"

# 4. Transfer to remote
scp -r "./agents/$AGENT_NAME" "$REMOTE:/opt/weagents/agents/"

# 5. Verify
ssh "$REMOTE" "ls -la /opt/weagents/agents/$AGENT_NAME/workspace/"

# 6. Set permissions
ssh "$REMOTE" "chmod 700 /opt/weagents/agents/$AGENT_NAME/.config"
```

## File Relationships

This skill works with:
- `agent-creator` skill - generates agent files to transfer
- Local `agents/` directory - source of agent files
- Remote `/opt/weagents/agents/` - destination on VMs

---

## 🔧 Pre-Configured Server Configurations

### Server Overview

| Server | Alias | IP Address | User | Purpose |
|--------|-------|------------|------|---------|
| **WeAgents** | `weagents` | 152.42.253.91 | root | Production agent server |
| **Educational Agent** | `oraora` | 15.204.234.93 | jude | Educational/development VM |

---

## 🌐 WeAgents Server

**Production server for agent deployments**

### Connection Details

| Property | Value |
|----------|-------|
| **Host Alias** | `weagents` |
| **IP Address** | `152.42.253.91` |
| **User** | `root` |
| **SSH Key** | `~/.ssh/id_ed25519_weagents` |
| **Base Path** | `/opt/agents/ono-assistant/` |

### Quick Connect
```bash
ssh weagents
```

### Critical File Locations

#### Agent Workspace (SKILLS GO HERE!)
```
/opt/agents/ono-assistant/workspace/
├── skills/                    ← Install skills here
│   ├── easy-paper-download/   ← Example skill
│   ├── email-ionos/
│   ├── lazada-browser/
│   ├── package-tracker/
│   └── shopee-seller/
├── memory/                    ← Agent memory
├── SOUL.md                    ← Agent identity
├── AGENTS.md                  ← Agent config
└── ...
```

#### Other Important Paths
| Purpose | Path |
|---------|------|
| **Agent Skills** | `/opt/agents/ono-assistant/workspace/skills/` |
| **Agent Workspace** | `/opt/agents/ono-assistant/workspace/` |
| **Legacy Skills** | `/opt/weagents/skills/` (deprecated, don't use) |
| **Channel Router** | `/opt/openclaw-channel-router/` |
| **Systemd Services** | `/etc/systemd/system/` |

### Skill Installation Template (WeAgents)

```bash
# 1. Create skill directory in CORRECT location
ssh weagents "mkdir -p /opt/agents/ono-assistant/workspace/skills/YOUR-SKILL-NAME"

# 2. Copy all skill files
scp /path/to/local/skill/* weagents:/opt/agents/ono-assistant/workspace/skills/YOUR-SKILL-NAME/

# 3. Make scripts executable (if any)
ssh weagents "chmod +x /opt/agents/ono-assistant/workspace/skills/YOUR-SKILL-NAME/*.py"

# 4. Verify installation
ssh weagents "ls -la /opt/agents/ono-assistant/workspace/skills/YOUR-SKILL-NAME/"
```

### Verification Commands (WeAgents)

```bash
# Test SSH connection
ssh weagents "echo 'Connected to weagents' && hostname"

# List all installed skills
ssh weagents "ls -la /opt/agents/ono-assistant/workspace/skills/"

# Check agent workspace
ssh weagents "ls -la /opt/agents/ono-assistant/workspace/"

# Verify specific skill
ssh weagents "head -5 /opt/agents/ono-assistant/workspace/skills/SKILL-NAME/SKILL.md"
```

---

## 📚 Oraora Server (Educational Agent)

**Educational/development VM for experiments and learning**

### Connection Details

| Property | Value |
|----------|-------|
| **Host Alias** | `oraora` |
| **IP Address** | `15.204.234.93` |
| **User** | `jude` |
| **SSH Key** | `~/.ssh/id_ed25519_weagents` |
| **OS** | Ubuntu 25.04 |

### Quick Connect
```bash
ssh oraora
```

### Server Info
```
System: Ubuntu 25.04 (GNU/Linux 6.14.0-34-generic)
IPv4: 15.204.234.93
IPv6: 2604:2dc0:101:200::16da
Disk: 10.7% of 95.85GB used
Memory: ~3% used
```

### Common Operations (Oraora)

```bash
# Check system status
ssh oraora "uptime && free -h && df -h"

# Update packages
ssh oraora "sudo apt update && sudo apt upgrade -y"

# Check running processes
ssh oraora "ps aux | head -20"

# View system logs
ssh oraora "journalctl -n 50 --no-pager"
```

### File Transfer Examples (Oraora)

```bash
# Copy file to oraora
scp ./local-file.txt oraora:/home/jude/

# Copy directory to oraora
scp -r ./my-project/ oraora:/home/jude/

# Copy from oraora to local
scp -r oraora:/home/jude/logs/ ./local-logs/

# Sync with rsync
rsync -avz --progress ./project/ oraora:/home/jude/project/
```

---

### Common Mistakes to Avoid (WeAgents)

❌ **WRONG** - Old/incorrect paths:
```bash
/opt/weagents/skills/                    # Don't use - deprecated
/opt/agents/skills/                      # Don't use - wrong location
/opt/ono-assistant/skills/              # Don't use - wrong path
```

✅ **CORRECT** - Use this path:
```bash
/opt/agents/ono-assistant/workspace/skills/   # Correct location
```

### SSH Config (Local Machine)

Add to `~/.ssh/config`:
```
Host weagents
    HostName 152.42.253.91
    User root
    IdentityFile ~/.ssh/id_ed25519_weagents
    StrictHostKeyChecking accept-new

Host oraora
    HostName 15.204.234.93
    User jude
    IdentityFile ~/.ssh/id_ed25519_weagents
    StrictHostKeyChecking accept-new
```

This configuration allows simple `ssh weagents` or `ssh oraora` commands.
