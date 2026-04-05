---
name: ssh-vm-lister
description: Use when listing available SSH hosts, discovering SSH VM names from config, or needing to see what SSH connections are configured
---

# SSH VM Lister

List all SSH VM names from the SSH config file automatically.

## Quick List

List all SSH hosts:

```bash
# Extract Host entries from SSH config
grep -E "^Host " ~/.ssh/config | sed 's/Host //' | column -t
```

## With Details

List hosts with HostName:

```bash
awk '/^Host /{host=$2} /^    HostName /{print host " -> " $2}' ~/.ssh/config | column -t
```

## As Table

```bash
echo "VM Name | Host/IP | User"
echo "--------|---------|------"
awk '/^Host /{host=$2} /^    HostName /{hn=$2} /^    User /{user=$2} host&&hn&&user{print host " | " hn " | " user; host=hn=user=""}' ~/.ssh/config
```

## Check Specific Host

```bash
# Show full config for a host
ssh -G <hostname> 2>/dev/null || awk '/^Host <hostname>$/,/^$/' ~/.ssh/config
```

## Programmatic Access

Get hosts as array (for scripts):

```bash
HOSTS=($(grep -E "^Host " ~/.ssh/config | awk '{print $2}'))
echo "Available hosts: ${HOSTS[@]}"
```

## Common Patterns

| Task | Command |
|------|---------|
| List all names only | `grep "^Host " ~/.ssh/config \| awk '{print $2}'` |
| Count hosts | `grep -c "^Host " ~/.ssh/config` |
| Search by IP | `grep -B1 "Hostname.*192" ~/.ssh/config` |
| Check if host exists | `ssh -G <host> > /dev/null 2>&1 && echo "Exists"` |

## Example Output

```
enraie      ->  148.113.174.79
oraora      ->  15.204.234.93
weagents    ->  152.42.253.91
spost       ->  15.204.93.25
aideal      ->  135.148.121.241
aidealns    ->  vps-fc8b59d9.vps.ovh.us
spostmarketing -> 15.204.249.142
```
