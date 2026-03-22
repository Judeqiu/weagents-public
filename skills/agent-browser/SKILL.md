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

**Use mychrome instead when:**
- You need **real Google Chrome** (not bundled Chromium)
- You need **persistent login sessions** across restarts
- You're working with sites that detect headless browsers
- You need Chrome extensions or specific Chrome features
- See [Alternative: mychrome](#alternative-mychrome-chrome-cdp) section below

**Don't use when:**
- Making simple HTTP requests (use curl/httpie instead)
- API testing (use direct API clients)
- You need persistent browser sessions (use **mychrome** instead)

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

### Linux/VPS Configuration

On Ubuntu 23.10+ and some Linux distributions, Chrome requires additional configuration:

```bash
# Option 1: Use --no-sandbox flag (recommended for VPS/containers)
agent-browser --args "--no-sandbox" open example.com

# Option 2: Set environment variable (permanent solution)
export AGENT_BROWSER_ARGS="--no-sandbox"
# Add to ~/.bashrc to make permanent
```

**Why:** Modern Linux distributions restrict unprivileged user namespaces with AppArmor. The `--no-sandbox` flag is required for Chrome to run in these environments.

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

## Alternative Methods

When agent-browser (bundled Chromium) doesn't work, you have two fallback options:

### Option 1: mychrome (Chrome CDP) - RECOMMENDED

For use cases requiring **real Google Chrome** with persistent sessions, use the **mychrome** skill instead.

### When to Use mychrome vs agent-browser

| Use Case | Recommended Tool | Why |
|----------|------------------|-----|
| Quick scraping, no login needed | **agent-browser** | Fast, ephemeral, snapshot-based |
| Sites requiring real Chrome | **mychrome** | Uses actual Google Chrome binary |
| Persistent login sessions | **mychrome** | Chrome profile persists across sessions |
| Chrome extensions needed | **mychrome** | Real Chrome supports extensions |
| Complex Playwright workflows | **mychrome** | Full Playwright API access |
| Quick snapshot interactions | **agent-browser** | @e1, @e2 refs are deterministic |

### Using mychrome

```bash
# Check if Chrome CDP is running
curl http://localhost:9222/json/version

# Use mychrome skill for Chrome CDP automation
~/.openclaw/workspace/skills/mychrome/scripts/chrome_manager.sh status

# Take screenshot with mychrome
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --url https://example.com \
  --screenshot /tmp/screenshot.png
```

### Key Differences

| Feature | agent-browser | mychrome |
|---------|---------------|----------|
| **Browser** | Bundled Chromium | Real Google Chrome |
| **Installation** | `npm install -g agent-browser` | Chrome must be pre-installed |
| **Session** | Ephemeral (default) | Persistent profiles |
| **Element IDs** | @e1, @e2 snapshot refs | CSS selectors, Playwright API |
| **Speed** | Very fast (Rust) | Standard (Playwright) |
| **CDP Required** | No | Yes (Chrome must run with --remote-debugging-port=9222) |
| **Best For** | Quick tasks, testing | Automation with login state |

**Tip:** Start with `agent-browser` for quick tasks. Switch to `mychrome` when you need persistent sessions or real Chrome behavior.

---

## 🚀 Smart Fetch Scripts (RECOMMENDED)

The easiest way to retrieve content or screenshots is using the **smart fetch scripts**, which automatically try all available methods until one succeeds.

### fetch_content.sh - Smart Content Retrieval

Automatically tries all browser methods in order:
1. **agent-browser** (local, fastest)
2. **mychrome** (Chrome CDP)
3. **Browserless API** (cloud fallback)
4. **curl** (simple HTTP)

```bash
# Fetch content (auto-selects best method)
~/.openclaw/workspace/skills/agent-browser/scripts/fetch_content.sh \
  --url https://example.com

# Save to file
~/.openclaw/workspace/skills/agent-browser/scripts/fetch_content.sh \
  --url https://example.com \
  --output /tmp/content.html

# Verbose mode to see which method was used
~/.openclaw/workspace/skills/agent-browser/scripts/fetch_content.sh \
  --url https://example.com \
  --verbose

# Force specific method
~/.openclaw/workspace/skills/agent-browser/scripts/fetch_content.sh \
  --url https://example.com \
  --method browserless
```

### fetch_screenshot.sh - Smart Screenshot Capture

Same smart fallback logic for screenshots:

```bash
# Capture screenshot
~/.openclaw/workspace/skills/agent-browser/scripts/fetch_screenshot.sh \
  --url https://example.com \
  --output /tmp/screenshot.png

# Full page screenshot
~/.openclaw/workspace/skills/agent-browser/scripts/fetch_screenshot.sh \
  --url https://example.com \
  --output /tmp/full.png \
  --full-page

# Mobile viewport
~/.openclaw/workspace/skills/agent-browser/scripts/fetch_screenshot.sh \
  --url https://example.com \
  --output /tmp/mobile.png \
  --width 375 --height 812
```

### Why Use Smart Fetch?

| Benefit | Description |
|---------|-------------|
| **Zero config** | Works out of the box, tries all methods automatically |
| **Resilient** | If one method fails, automatically tries the next |
| **Fast** | Uses fastest available method first |
| **Reliable** | Always falls back to Browserless API (cloud) if needed |

### Example Output

```
$ ./fetch_content.sh --url https://example.com --verbose
Fetching: https://example.com

[INFO] Trying agent-browser...
[INFO] agent-browser failed
[INFO] Trying mychrome...
[INFO] mychrome failed
[INFO] Trying Browserless API...
[INFO] Browserless succeeded

✓ Success using: browserless
```

---

---

### Option 2: Browserless API - LAST RESORT

When neither agent-browser nor mychrome works (no Chrome available, incompatible system, or remote environment without browser access), use **Browserless** cloud-hosted browser automation.

#### What is Browserless?

Browserless provides cloud-hosted browser automation via API:
- **No local browser installation required**
- **REST API** for simple operations (screenshots, PDFs, content)
- **WebSocket API** for full Puppeteer/Playwright control
- **Multiple regions** (US West, Europe UK, Amsterdam)

#### Browserless REST API (Simple Operations)

```bash
# Set your token (provided by admin)
export BROWSERLESS_TOKEN="your-token-here"

# Take screenshot
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh screenshot \
  --url https://example.com \
  --output /tmp/screenshot.png

# Extract page content
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh content \
  --url https://example.com

# Generate PDF
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh pdf \
  --url https://example.com \
  --output /tmp/page.pdf

# Check API status
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh status
```

#### Browserless WebSocket (Full Control)

```bash
# Connect via WebSocket for full Puppeteer/Playwright control
export BROWSERLESS_TOKEN="your-token-here"
export BROWSERLESS_WS_URL="wss://production-sfo.browserless.io/chrome"

# Run script with browserless
node scripts/browserless_ws_example.js
```

#### Browserless Regions

| Region | URL | Best For |
|--------|-----|----------|
| US West | `production-sfo.browserless.io` | Americas, Asia-Pacific |
| Europe UK | `production-lon.browserless.io` | UK, Western Europe |
| Amsterdam | `production-ams.browserless.io` | Europe, Africa |

#### When to Use Each Method

| Scenario | Recommended Tool | Why |
|----------|------------------|-----|
| Local quick tasks | **agent-browser** | Fast, no external dependencies |
| Persistent login sessions | **mychrome** | Chrome profile persists across sessions |
| Sites requiring real Chrome | **mychrome** | Uses actual Google Chrome binary |
| No Chrome/CDP available locally | **Browserless** | Cloud-hosted, no local browser needed |
| Remote server without browser | **Browserless** | Works anywhere with HTTP access |
| ARM/unsupported architecture | **Browserless** | Cloud handles browser execution |
| Blocked by corporate firewall | **Browserless** | Uses standard HTTPS (port 443) |

#### Browserless Token Setup

The agent-browser skill comes with a pre-configured Browserless API token. No setup required!

```bash
# Token is already embedded in the skill
# Just use it directly:
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh status

# Optional: Choose region (default: sfo)
export BROWSERLESS_REGION="lon"  # Options: sfo, lon, ams
```

**Default Configuration:**
- **Token**: Pre-configured (embedded in skill)
- **Region**: US West (San Francisco)
- **Base URL**: `https://production-sfo.browserless.io`

**To customize (optional):**
```bash
# Run setup script to save to shell profile
~/.openclaw/workspace/skills/agent-browser/scripts/setup_browserless.sh

# Or manually set your own token
export BROWSERLESS_TOKEN="your-own-token"
export BROWSERLESS_REGION="lon"  # Change region
```

#### Browserless Pricing

- **Free tier**: Limited daily requests
- **Paid plans**: Scale with usage
- **Enterprise**: Custom plans available
- Contact admin for organization token

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using CSS selectors instead of refs | Use refs from snapshot for deterministic selection |
| Not re-snapshotting after actions | Always snapshot after page changes to get fresh refs |
| Forgetting to close browser | Run `agent-browser close` or use `--session` for isolation |
| Using npx for regular use | Install globally: `npm install -g agent-browser` |
| Long timeouts without adjustment | Set `AGENT_BROWSER_DEFAULT_TIMEOUT` for slow pages |
| Using agent-browser when you need persistent login | Switch to **mychrome** for session persistence |

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

---

## Files

| File | Purpose |
|------|---------|
| `scripts/fetch_content.sh` | **Smart content retrieval** - tries all methods automatically (RECOMMENDED) |
| `scripts/fetch_screenshot.sh` | **Smart screenshot capture** - tries all methods automatically (RECOMMENDED) |
| `scripts/browserless_helper.sh` | Browserless API helper for cloud browser automation |
| `scripts/setup_browserless.sh` | Setup script for Browserless configuration |
| `install.sh` | Installation script for agent-browser npm package |
| `SKILL.md` | This documentation |
