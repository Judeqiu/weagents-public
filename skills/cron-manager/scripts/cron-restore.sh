#!/bin/bash
# Restore crontab from backup
# Usage: ./cron-restore.sh <backup-file>

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup-file>"
    echo ""
    echo "Available backups:"
    ls -la ~/.crontab.backup.* 2>/dev/null || echo "  No backups found"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring crontab from: $BACKUP_FILE"
echo ""
echo "Contents to restore:"
cat "$BACKUP_FILE"
echo ""

crontab "$BACKUP_FILE"

echo ""
echo "Crontab restored successfully!"
echo ""
echo "Current crontab:"
crontab -l
