---
name: ssh-config-add
description: SAFELY add new SSH host entries to ~/.ssh/config. APPEND-ONLY - never modifies or deletes existing entries. Use when you need to create SSH shortcuts for new VMs. If host already exists, it will refuse to make any changes.
version: 1.0.0
---

# SSH Config Add - Append Only

**⚠️ SAFETY FIRST: This tool is APPEND-ONLY**

- ✅ Can ADD new hosts
- ❌ Will NOT modify existing hosts
- ❌ Will NOT delete hosts
- ❌ Will NOT replace hosts

If a host already exists, the tool will refuse to make any changes and tell you to edit manually.

## When to Use

- You have a new VM and want to create an SSH shortcut
- You want to avoid typing `ssh user@ip` every time
- You need consistent SSH config for automation tools

## Requirements

- SSH key already copied to the VM (`ssh-copy-id` done)
- Write access to `~/.ssh/config`

## Quick Usage

### Interactive Mode (Recommended)

```bash
./add-host.sh
```

You'll be prompted for:
- Host name (e.g., `kai`, `enraie`)
- Hostname/IP (e.g., `15.204.118.66`)
- User (default: `ubuntu`)
- SSH key path (optional, default: none)

### Command Line Mode

```bash
./add-host.sh --name myserver --ip 192.168.1.100 --user ubuntu
```

## What It Does

1. **Checks if host exists** - Reads `~/.ssh/config`
2. **If host exists** - Exits immediately with warning
3. **If host is new** - Appends entry to end of file
4. **Sets permissions** - Ensures `~/.ssh/config` is 600

## Safety Guarantees

### Before Adding

```
Checking if 'kai' already exists in ~/.ssh/config...
❌ Host 'kai' already exists!

EXISTING ENTRY:
Host kai
    HostName 15.204.118.66
    User ubuntu

NO CHANGES MADE.
To modify this entry, please edit ~/.ssh/config manually.
```

### After Adding

```
Checking if 'newserver' already exists in ~/.ssh/config...
✅ Host 'newserver' not found - safe to add.

Appending to ~/.ssh/config...
✅ Successfully added 'newserver'

NEW ENTRY:
Host newserver
    HostName 192.168.1.100
    User ubuntu
    StrictHostKeyChecking accept-new

BACKUP: ~/.ssh/config.backup.20260328_121500
```

## Examples

### Add a Simple Host

```bash
./add-host.sh --name kai --ip 15.204.118.66
```

Creates:
```
Host kai
    HostName 15.204.118.66
    User ubuntu
    StrictHostKeyChecking accept-new
```

### Add with Custom User

```bash
./add-host.sh --name enraie --ip 148.113.174.79 --user admin
```

### Add with Specific SSH Key

```bash
./add-host.sh --name myserver --ip 192.168.1.100 --key ~/.ssh/my_key
```

Creates:
```
Host myserver
    HostName 192.168.1.100
    User ubuntu
    IdentityFile ~/.ssh/my_key
    StrictHostKeyChecking accept-new
```

## Manual Verification

Always verify the new entry works:

```bash
# Test the connection
ssh <hostname> "hostname && whoami"

# Example:
ssh kai "hostname && whoami"
```

## Troubleshooting

### "Host already exists"

This is expected behavior! The tool refuses to modify existing entries.

**Options:**
1. Use a different host name: `./add-host.sh --name kai2 --ip ...`
2. Edit manually: `vim ~/.ssh/config`

### "Permission denied"

Make sure you own the SSH config:
```bash
ls -la ~/.ssh/config
# Should show: -rw------- 1 <you> <you>
```

Fix permissions:
```bash
chmod 600 ~/.ssh/config
```

### "SSH config not found"

The tool will create `~/.ssh/config` if it doesn't exist.

## Important Notes

- **Backup created** before each add (timestamped)
- **StrictHostKeyChecking accept-new** added automatically for new hosts
- **No duplicates** - tool refuses to create duplicate entries
- **No editing** - use `vim ~/.ssh/config` for modifications
- **No deletion** - use `vim ~/.ssh/config` to remove entries

## Backup Files

Every operation creates a backup:
```
~/.ssh/config.backup.20260328_121500
~/.ssh/config.backup.20260328_134522
```

To restore:
```bash
cp ~/.ssh/config.backup.20260328_121500 ~/.ssh/config
```
