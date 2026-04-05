#!/bin/bash
# Add a cron job
# Usage: ./cron-add.sh "schedule" "command"

SCHEDULE="$1"
COMMAND="$2"

if [ -z "$SCHEDULE" ] || [ -z "$COMMAND" ]; then
    echo "Usage: $0 \"schedule\" \"command\""
    echo ""
    echo "Examples:"
    echo "  $0 \"0 9 * * *\" \"/home/user/script.sh\""
    echo "  $0 \"@reboot\" \"/home/user/startup.sh\""
    echo "  $0 \"*/30 * * * *\" \"/home/user/check.sh >> /tmp/check.log 2>&1\""
    exit 1
fi

# Backup current crontab
BACKUP_FILE="$HOME/.crontab.backup.$(date +%Y%m%d-%H%M%S)"
crontab -l > "$BACKUP_FILE" 2>/dev/null || touch "$BACKUP_FILE"

echo "Backing up current crontab to: $BACKUP_FILE"

# Add new job
(crontab -l 2>/dev/null; echo "$SCHEDULE $COMMAND") | crontab -

echo "Added cron job:"
echo "  Schedule: $SCHEDULE"
echo "  Command:  $COMMAND"
echo ""
echo "Current crontab:"
crontab -l | tail -5
