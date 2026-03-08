# Remote Operations - Quick Start

Execute commands and create agents on remote servers via SSH.

## Prerequisites

```bash
# Ensure SSH access is configured
ssh -o ConnectTimeout=5 user@host "echo 'OK'"
```

## Quick Commands

### Test Connection
```bash
ssh user@host "hostname && uptime"
```

### Create Remote Directory
```bash
ssh user@host "mkdir -p /opt/weagents/agents"
```

### Transfer Agent to Remote
```bash
# Create agent locally first
./skills/agent-creator/scripts/create-agent.sh remote-agent \
    --purpose "Remote assistant" \
    --user "RemoteUser"

# Transfer to remote
scp -r ./agents/remote-agent user@host:/opt/weagents/agents/

# Verify
ssh user@host "ls /opt/weagents/agents/remote-agent/workspace/"
```

## Scripts

### remote-create-agent.sh

Create an agent directly on a remote host:

```bash
./skills/remote-ops/scripts/remote-create-agent.sh \
    ubuntu@192.168.1.100 \
    my-remote-agent \
    "Production support" \
    "DevOps Team"
```

### remote-list-agents.sh

List all agents on a remote host:

```bash
./skills/remote-ops/scripts/remote-list-agents.sh ubuntu@192.168.1.100
```

### remote-sync-agent.sh

Sync local agent changes to remote:

```bash
./skills/remote-ops/scripts/remote-sync-agent.sh \
    ubuntu@192.168.1.100 \
    my-agent
```

## SSH Config Tips

Add to `~/.ssh/config`:

```
Host weagents-vm
    HostName 192.168.1.100
    User ubuntu
    IdentityFile ~/.ssh/weagents_key
    StrictHostKeyChecking accept-new
```

Then use:
```bash
ssh weagents-vm "command"
```

## Common Patterns

**Execute multiple commands:**
```bash
ssh user@host '
    cd /opt/weagents
    ls -la agents/
    df -h
'
```

**Copy with rsync:**
```bash
rsync -avz --exclude='data/' \
    ./agents/my-agent/ \
    user@host:/opt/weagents/agents/my-agent/
```

**Remote backup:**
```bash
ssh user@host "tar czf - /opt/weagents/agents" > backup-$(date +%Y%m%d).tar.gz
```
