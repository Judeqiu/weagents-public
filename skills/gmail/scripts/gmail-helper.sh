#!/bin/bash
# Gmail Helper Script - Wrapper for gws Gmail API commands
# Usage: ./gmail-helper.sh <command> [args]

set -e

# Check if gws is installed
if ! command -v gws &> /dev/null; then
    echo "Error: gws CLI not found. Install with: npm install -g @googleworkspace/cli"
    exit 1
fi

# Check authentication
if ! gws auth status &> /dev/null; then
    echo "Error: Not authenticated. Run: gws auth login"
    exit 1
fi

COMMAND="$1"
shift || true

case "$COMMAND" in
    list)
        # List recent emails
        MAX_RESULTS="${1:-10}"
        gws gmail users messages list --params "{\"userId\": \"me\", \"maxResults\": $MAX_RESULTS}"
        ;;
    
    get)
        # Get email by ID
        MESSAGE_ID="$1"
        if [ -z "$MESSAGE_ID" ]; then
            echo "Usage: $0 get <message_id>"
            exit 1
        fi
        gws gmail users messages get --params "{\"userId\": \"me\", \"id\": \"$MESSAGE_ID\", \"format\": \"full\"}"
        ;;
    
    search)
        # Search emails with query
        QUERY="$1"
        MAX_RESULTS="${2:-10}"
        if [ -z "$QUERY" ]; then
            echo "Usage: $0 search '<query>' [max_results]"
            echo "Example: $0 search 'from:example@gmail.com'"
            exit 1
        fi
        gws gmail users messages list --params "{\"userId\": \"me\", \"q\": \"$QUERY\", \"maxResults\": $MAX_RESULTS}"
        ;;
    
    unread)
        # List unread emails
        MAX_RESULTS="${1:-10}"
        gws gmail users messages list --params "{\"userId\": \"me\", \"q\": \"is:unread\", \"maxResults\": $MAX_RESULTS}"
        ;;
    
    trash)
        # Move email to trash
        MESSAGE_ID="$1"
        if [ -z "$MESSAGE_ID" ]; then
            echo "Usage: $0 trash <message_id>"
            exit 1
        fi
        gws gmail users.messages trash --params "{\"userId\": \"me\", \"id\": \"$MESSAGE_ID\"}"
        ;;
    
    status)
        # Check Gmail connection status
        echo "=== Gmail Connection Status ==="
        gws auth status 2>&1 | grep -E "(user|token_valid|scope_count)"
        echo ""
        echo "Testing Gmail API..."
        if gws gmail users messages list --params '{"userId": "me", "maxResults": 1}' &> /dev/null; then
            echo "✓ Gmail API is working"
        else
            echo "✗ Gmail API error"
        fi
        ;;
    
    *)
        echo "Gmail Helper Script"
        echo ""
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  list [count]           - List recent emails (default: 10)"
        echo "  get <message_id>       - Get full email content by ID"
        echo "  search '<query>' [max] - Search emails (Gmail query syntax)"
        echo "  unread [count]         - List unread emails"
        echo "  trash <message_id>     - Move email to trash"
        echo "  status                 - Check connection status"
        echo ""
        echo "Examples:"
        echo "  $0 list 5"
        echo "  $0 get 19d4c3fcf193c277"
        echo "  $0 search 'from:google.com'"
        echo "  $0 unread"
        exit 1
        ;;
esac
