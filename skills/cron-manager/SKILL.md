---
name: cron-manager
description: Manage cron jobs for automated tasks. Use to schedule, list, enable, disable, or remove cron jobs for periodic scripts and tasks.
---

# Cron Manager

Manage cron jobs for automated periodic tasks.

## When to Use

- Schedule periodic scripts (daily, hourly, etc.)
- List current cron jobs
- Enable/disable cron jobs
- Remove existing cron jobs
- Backup and restore cron configurations

## Quick Start

### List Current Cron Jobs

```bash
# List user crontab
crontab -l

# List with line numbers (for editing)
crontab -l | cat -n
```

### Add a Cron Job

```bash
# Edit crontab
crontab -e

# Or add directly (be careful!)
(crontab -l 2>/dev/null; echo "0 9 * * * /path/to/script.sh") | crontab -
```

### Remove a Cron Job

```bash
# Remove by pattern
crontab -l | grep -v "script-to-remove" | crontab -

# Clear all cron jobs
crontab -r
```

## Common Schedules

| Schedule | Description |
|----------|-------------|
| `@reboot` | Run at system startup |
| `@daily` or `0 0 * * *` | Run once a day at midnight |
| `@hourly` or `0 * * * *` | Run every hour |
| `*/30 * * * *` | Run every 30 minutes |
| `0 9 * * 1-5` | Run at 9 AM on weekdays |
| `0 0 * * 0` | Run weekly on Sunday |

## Scripts

Located in `scripts/`:

| Script | Purpose | Example |
|--------|---------|---------|
| `cron-list.sh` | List all cron jobs | `./cron-list.sh` |
| `cron-add.sh` | Add a new cron job | `./cron-add.sh "0 9 * * *" "/path/to/script.sh"` |
| `cron-remove.sh` | Remove cron jobs by pattern | `./cron-remove.sh "script-name"` |
| `cron-backup.sh` | Backup current crontab | `./cron-backup.sh` |
| `cron-restore.sh` | Restore from backup | `./cron-restore.sh ~/.crontab.backup.2025...` |
| `cron-disable-all.sh` | Disable all cron jobs | `./cron-disable-all.sh` |

## Examples

### Schedule Daily Task

```bash
./scripts/cron-add.sh "0 8 * * *" "/home/user/scripts/daily-report.sh"
```

### Schedule Every 30 Minutes

```bash
./scripts/cron-add.sh "*/30 * * * *" "/home/user/scripts/check-status.sh"
```

### Remove Specific Job

```bash
./scripts/cron-remove.sh "daily-report.sh"
```

### Backup and Clear

```bash
# Backup first
./scripts/cron-backup.sh

# Clear all
crontab -r
```

## Safety Notes

- Always backup before making changes
- Test scripts manually before scheduling
- Use absolute paths in cron jobs
- Redirect output to logs to avoid email spam
- Check `PATH` environment in cron (limited by default)
