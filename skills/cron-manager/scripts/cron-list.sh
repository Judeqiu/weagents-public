#!/bin/bash
# List all cron jobs

echo "Current Cron Jobs:"
echo "=================="
echo ""

if crontab -l 2>/dev/null | grep -q .; then
    crontab -l | cat -n
else
    echo "No cron jobs configured."
fi

echo ""
echo "=================="
