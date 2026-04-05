#!/bin/bash
# Remove cron jobs matching a pattern
# Usage: ./cron-remove.sh "pattern"

PATTERN="$1"

if [ -z "$PATTERN" ]; then
    echo "Usage: $0 \"pattern\""
    echo ""
    echo "Removes all cron jobs matching the pattern."
    echo ""
    echo "Examples:"
    echo "  $0 \"daily-report\"     # Remove jobs containing 'daily-report'"
    echo "  $0 \"order_check\"      # Remove jobs containing 'order_check'"
    exit 1
fi

# Check if any jobs match
MATCHES=$(crontab -l 2>/dev/null | grep "$PATTERN" || true)

if [ -z "$MATCHES" ]; then
    echo "No cron jobs found matching: $PATTERN"
    exit 0
fi

echo "Found matching cron jobs:"
echo "$MATCHES"
echo ""

# Backup
BACKUP_FILE="$HOME/.crontab.backup.$(date +%Y%m%d-%H%M%S)"
crontab -l > "$BACKUP_FILE" 2>/dev/null
echo "Backup saved to: $BACKUP_FILE"

# Remove matching jobs
crontab -l 2>/dev/null | grep -v "$PATTERN" | crontab -

echo ""
echo "Removed jobs matching: $PATTERN"
echo ""
echo "Remaining cron jobs:"
crontab -l | cat -n 2>/dev/null || echo "  (none)"
