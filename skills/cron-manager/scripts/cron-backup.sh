#!/bin/bash
# Backup current crontab

BACKUP_FILE="$HOME/.crontab.backup.$(date +%Y%m%d-%H%M%S)"

if crontab -l > "$BACKUP_FILE" 2>/dev/null; then
    echo "Crontab backed up to: $BACKUP_FILE"
    echo ""
    echo "Contents:"
    cat "$BACKUP_FILE"
else
    echo "No crontab to backup (or empty)."
    touch "$BACKUP_FILE"
    echo "Created empty backup: $BACKUP_FILE"
fi
