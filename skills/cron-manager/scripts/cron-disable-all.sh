#!/bin/bash
# Disable all cron jobs by backing up and clearing crontab

BACKUP_FILE="$HOME/.crontab.backup.$(date +%Y%m%d-%H%M%S)"

# Check if there's anything to disable
if ! crontab -l 2>/dev/null | grep -q .; then
    echo "No cron jobs currently configured."
    exit 0
fi

echo "Current cron jobs:"
echo "=================="
crontab -l
echo ""
echo "=================="
echo ""

# Backup
crontab -l > "$BACKUP_FILE"
echo "Backup saved to: $BACKUP_FILE"

# Clear all
crontab -r

echo ""
echo "All cron jobs have been disabled."
echo ""
echo "To restore: ./cron-restore.sh $BACKUP_FILE"
