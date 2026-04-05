#!/bin/bash
# Send email with optional attachment using Google Workspace Gmail API
# Usage: ./send-email.sh "to@example.com" "Subject" "Body text" [attachment_path] [--html]

TO="$1"
SUBJECT="$2"
BODY="$3"
ATTACHMENT="$4"
HTML_FLAG="$5"

if [ -z "$TO" ] || [ -z "$SUBJECT" ] || [ -z "$BODY" ]; then
    echo "Usage: $0 \"recipient@email.com\" \"Subject\" \"Body text\" [attachment_path] [--html]"
    echo ""
    echo "Examples:"
    echo "  $0 \"to@example.com\" \"Hello\" \"Body text\""
    echo "  $0 \"to@example.com\" \"Hello\" \"Body text\" \"/path/to/file.pdf\""
    echo "  $0 \"to@example.com\" \"Hello\" \"$(cat body.html)\" --html"
    exit 1
fi

# Build gws command
CMD="gws gmail +send --to \"$TO\" --subject \"$SUBJECT\""

# Add HTML flag if specified
if [ "$HTML_FLAG" == "--html" ]; then
    CMD="$CMD --html"
fi

# Add attachment if provided and exists
if [ -n "$ATTACHMENT" ] && [ "$ATTACHMENT" != "--html" ] && [ -f "$ATTACHMENT" ]; then
    CMD="$CMD --attach \"$ATTACHMENT\""
fi

# Add body (use file content if body is a file path)
if [ -f "$BODY" ]; then
    BODY_CONTENT=$(cat "$BODY")
else
    BODY_CONTENT="$BODY"
fi

# Execute the command with body
eval "$CMD --body \"$BODY_CONTENT\""

if [ $? -eq 0 ]; then
    echo "✅ Email sent successfully to $TO"
else
    echo "❌ Failed to send email"
    exit 1
fi
