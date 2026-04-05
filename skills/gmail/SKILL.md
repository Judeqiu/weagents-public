---
name: gmail
description: Read, search, and manage Gmail emails using the gws CLI and Gmail API. Use when user asks to check email, read emails, search inbox, find messages, or perform any Gmail-related tasks. Provides commands for listing emails, getting message details, searching with Gmail query syntax, and managing email status.
---

# Gmail Skill

Manage Gmail emails through the Google Workspace CLI (gws).

## Prerequisites

- gws CLI installed: `npm install -g @googleworkspace/cli`
- OAuth authentication completed: `gws auth login`
- Gmail API enabled in Google Cloud Console

## Quick Reference

### List Recent Emails
```bash
# Using gws directly
gws gmail users messages list --params '{"userId": "me", "maxResults": 10}'

# Using helper script
~/.openclaw/workspace/skills/gmail/scripts/gmail-helper.sh list 10
```

### Get Email Content
```bash
# Get full message details
gws gmail users messages get --params '{"userId": "me", "id": "MESSAGE_ID", "format": "full"}'

# Using helper script
~/.openclaw/workspace/skills/gmail/scripts/gmail-helper.sh get MESSAGE_ID
```

### Search Emails
```bash
# Using Gmail query syntax
gws gmail users messages list --params '{"userId": "me", "q": "from:example@gmail.com", "maxResults": 5}'

# Using helper script
~/.openclaw/workspace/skills/gmail/scripts/gmail-helper.sh search 'from:example@gmail.com'
```

### List Unread Emails
```bash
gws gmail users messages list --params '{"userId": "me", "q": "is:unread", "maxResults": 10}'

# Using helper script
~/.openclaw/workspace/skills/gmail/scripts/gmail-helper.sh unread
```

## Gmail Query Syntax

Common search operators:
- `from:email@domain.com` - From specific sender
- `to:email@domain.com` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `has:attachment` - Has attachments
- `is:unread` - Unread messages
- `is:starred` - Starred messages
- `in:inbox` - In inbox
- `in:spam` - In spam
- `in:trash` - In trash
- `after:2024/01/01` - After date
- `before:2024/12/31` - Before date
- `older_than:7d` - Older than 7 days
- `newer_than:1d` - Newer than 1 day

## Helper Script Commands

The `gmail-helper.sh` script provides simplified access:

```bash
~/.openclaw/workspace/skills/gmail/scripts/gmail-helper.sh <command> [args]

Commands:
  list [count]              List recent emails
  get <message_id>          Get email content
  search '<query>' [max]    Search emails
  unread [count]            List unread emails
  trash <message_id>        Move to trash
  status                    Check connection
```

## Response Format

Email list response contains:
- `messages[].id` - Message ID
- `messages[].threadId` - Thread ID
- `resultSizeEstimate` - Total matching messages

Email detail response contains:
- `id` - Message ID
- `threadId` - Thread ID
- `labelIds` - Labels (UNREAD, INBOX, etc.)
- `snippet` - Preview text
- `payload.headers` - Email headers (From, To, Subject, Date)
- `payload.parts[]` - Message body parts (text/plain, text/html)

## Common Patterns

### Extract Email Headers
```bash
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID", "format": "metadata", "metadataHeaders": ["Subject", "From", "Date"]}'
```

### Get Plain Text Body
The message body is base64 encoded in `payload.parts[].body.data`. Decode with:
```bash
echo "BASE64_DATA" | base64 -d
```

## Troubleshooting

**401/403 Error:**
- Run `gws auth login` to refresh credentials
- Check Gmail API is enabled in Google Cloud Console

**No messages returned:**
- Verify email address in `gws auth status`
- Check query syntax is correct

**Rate limiting:**
- Add delays between requests
- Use batch operations when possible

## Resources

- Helper script: `scripts/gmail-helper.sh`
- gws CLI docs: Run `gws --help`
- Gmail API docs: https://developers.google.com/gmail/api
