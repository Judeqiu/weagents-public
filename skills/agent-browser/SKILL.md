---
name: agent-browser
description: Use when automating browser interactions, web scraping, testing web applications, or controlling headless browsers via CLI for AI agents
---

# Agent Browser

## Overview

Headless browser automation CLI for AI agents. Fast Rust CLI with Node.js fallback. Provides deterministic element selection via accessibility tree snapshots with refs (@e1, @e2).

## When to Use

- **Web automation workflows**: Form filling, clicking, navigation
- **Web scraping**: Extract data from web pages
- **Web application testing**: E2E testing, screenshot comparison
- **Authentication flows**: Login automation with state persistence
- **Visual regression**: Compare screenshots or snapshots between versions

**Don't use when:**
- Making simple HTTP requests (use curl/httpie instead)
- API testing (use direct API clients)

## Core Pattern

The snapshot-ref workflow is optimal for LLMs:

```
1. OPEN  → agent-browser open <url>
2. SNAP   → agent-browser snapshot -i    # Get interactive elements with refs
3. ACT    → agent-browser click @e1      # Use refs from snapshot
4. REPEAT → Re-snapshot after page changes
```

## Quick Reference

### Essential Commands

| Command | Purpose |
|---------|---------|
| `open <url>` | Navigate to URL |
| `snapshot -i` | Get interactive elements with refs (@e1, @e2) |
| `click @eN` | Click element by ref |
| `fill @eN "text"` | Clear and fill input |
| `type @eN "text"` | Type into element |
| `get text @eN` | Get element text content |
| `screenshot [path]` | Take screenshot (--full for full page) |
| `close` | Close browser |

### Element Selection

```bash
# By ref (deterministic, preferred)
agent-browser click @e2

# By CSS selector
agent-browser click "#submit"
agent-browser click ".button-class"

# By ARIA role
agent-browser find role button click --name "Submit"

# By text content
agent-browser find text "Sign In" click
```

### Session Management

```bash
# Isolated sessions
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com

# Persistent state across restarts
agent-browser --session-name myapp open myapp.com

# Persistent profile directory
agent-browser --profile ~/.myapp-profile open myapp.com
```

### Installation

```bash
# Global install (fastest - native Rust CLI)
npm install -g agent-browser
agent-browser install  # Download Chromium

# Or try without installing
npx agent-browser install
npx agent-browser open example.com

# On Linux - with system deps
agent-browser install --with-deps
```

## Implementation

### Basic Workflow Example

```bash
# 1. Navigate
agent-browser open example.com

# 2. Get snapshot with refs
agent-browser snapshot -i
# Output shows refs like: [ref=e1] button "Submit"

# 3. Interact using refs
agent-browser click @e1
agent-browser fill @e2 "test@example.com"

# 4. Take screenshot
agent-browser screenshot result.png

# 5. Cleanup
agent-browser close
```

### Chaining Commands

```bash
# Chain with && for efficiency
agent-browser open example.com && \
  agent-browser wait --load networkidle && \
  agent-browser snapshot -i

# Multi-step interaction
agent-browser fill @e1 "user@example.com" && \
  agent-browser fill @e2 "password" && \
  agent-browser click @e3
```

### State Persistence

```bash
# Save auth state after login
agent-browser state save github-auth

# Load state in future sessions
agent-browser state load github-auth
```

### Diff & Regression Testing

```bash
# Compare snapshots
agent-browser diff snapshot

# Compare screenshots
agent-browser diff screenshot --baseline before.png

# Compare two URLs
agent-browser diff url https://v1.com https://v2.com
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using CSS selectors instead of refs | Use refs from snapshot for deterministic selection |
| Not re-snapshotting after actions | Always snapshot after page changes to get fresh refs |
| Forgetting to close browser | Run `agent-browser close` or use `--session` for isolation |
| Using npx for regular use | Install globally: `npm install -g agent-browser` |
| Long timeouts without adjustment | Set `AGENT_BROWSER_DEFAULT_TIMEOUT` for slow pages |

## Security Features (Opt-in)

```bash
# Domain allowlist
agent-browser --allowed-domains "example.com,*.example.com" open example.com

# Content boundaries for LLM safety
agent-browser --content-boundaries snapshot

# Output limits
agent-browser --max-output 50000 snapshot
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `AGENT_BROWSER_SESSION` | Session name for isolation |
| `AGENT_BROWSER_SESSION_NAME` | Auto-save/load session state |
| `AGENT_BROWSER_DEFAULT_TIMEOUT` | Default timeout in ms (default: 25000) |
| `AGENT_BROWSER_HEADED` | Show browser window for debugging |
| `AGENT_BROWSER_ANNOTATE` | Annotated screenshots with labels |
