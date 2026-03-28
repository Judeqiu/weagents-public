---
skill_name: agent-browser
skill_version: 2.0.0
skill_type: natural_language
claude_version: requires_claude_4_or_later
description: |
  Web browsing and content extraction skill using natural language decision flow.
  Prioritizes Chrome CDP for dynamic sites, with automatic fallback through multiple methods.
---

# Agent Browser - Natural Language Skill

## Overview

This skill enables web browsing and content extraction using a **natural language decision flow**. Instead of rigid scripts, Claude interprets the task and selects the appropriate method dynamically.

### Core Philosophy

> **Be like a human researcher**: Start simple, escalate complexity only when needed, adapt based on what you find.

### Method Priority (Natural Language Decision Tree)

When asked to fetch or browse a web page, follow this priority order:

```
1. Chrome CDP (mychrome)     ← FIRST if CDP is available and site needs real browser
2. Bundled Chromium          ← SECOND if agent-browser is installed  
3. Browserless API           ← THIRD as cloud fallback
4. curl / FetchURL           ← FOURTH for simple static pages
5. Jina AI Summarizer        ← FIFTH for articles (saves tokens)
```

---

## Tool Usage Reference

### Quick Decision Matrix

| Site Characteristics | Recommended Approach | Claude Tool |
|---------------------|---------------------|-------------|
| Needs login / persistent session | Chrome CDP | Shell → mychrome scripts |
| Anti-bot protection (小红书, 微信, 知乎) | Real browser required | Chrome CDP or Browserless |
| Simple static HTML | Fastest approach | FetchURL or curl |
| Article, blog, documentation | Token-efficient | Jina AI service |
| JavaScript-heavy SPA | Browser rendering required | Chrome CDP or agent-browser |
| Unknown / first visit | Auto-detect | Start with curl, escalate if needed |

### Tool Selection Patterns

#### Pattern 1: Chrome CDP (mychrome)
**When to use:**
- Site requires login/authentication
- Persistent session needed across requests
- Real Chrome fingerprint required
- Previous attempts with simpler methods failed

**How to check availability:**
```bash
curl -s http://localhost:9222/json/version
```

**How to use:**
```bash
# Basic fetch with CDP
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --cdp-url http://localhost:9222 \
  --url "https://example.com" \
  --extract-content

# With screenshot
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --cdp-url http://localhost:9222 \
  --url "https://example.com" \
  --screenshot /tmp/screenshot.png
```

#### Pattern 2: Bundled Chromium (agent-browser)
**When to use:**
- Quick browsing tasks
- No persistent session needed
- Fast snapshot-based interactions
- CDP not available

**How to check availability:**
```bash
which agent-browser
```

**How to use:**
```bash
# Open and get snapshot
agent-browser open "https://example.com"
agent-browser snapshot -i
agent-browser close

# Or chained
agent-browser open "https://example.com" && \
  agent-browser content && \
  agent-browser close
```

#### Pattern 3: Browserless API (Cloud)
**When to use:**
- No local browser available
- Previous methods blocked
- Remote/cloud environment
- Need guaranteed availability

**How to use:**
```bash
# Content extraction
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh \
  content --url "https://example.com"

# Screenshot
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh \
  screenshot --url "https://example.com" --output /tmp/screenshot.png
```

#### Pattern 4: Simple HTTP (curl / FetchURL)
**When to use:**
- Static HTML pages
- API endpoints
- Fastest possible retrieval
- No JavaScript execution needed

**How to use:**
```bash
# Using curl
curl -sL -A "Mozilla/5.0" "https://example.com"

# For FetchURL tool, just provide the URL directly
```

#### Pattern 5: Jina AI (Article Summarizer)
**When to use:**
- Article, blog post, documentation
- Need Markdown format
- Want to save tokens
- URL pattern suggests article (/blog/, /article/, /docs/, date paths)

**How to use:**
```bash
# Jina AI service
curl -sL "https://r.jina.ai/https://example.com/article"
```

---

## Site Experience Database

### Known Anti-Bot Platforms

These sites typically require a real browser (Chrome CDP or Browserless):

| Platform | Domain Pattern | Special Handling |
|----------|---------------|------------------|
| 小红书 (Red) | xiaohongshu.com, xhslink.com | Strict anti-bot, login required for full content |
| 微信公众号 | mp.weixin.qq.com | SSR with protection, lazy images |
| 知乎 (Zhihu) | zhihu.com | Hybrid rendering, scroll to load |
| 微博 (Weibo) | weibo.com | Strict login requirement |
| 抖音 (TikTok) | douyin.com | SPA, heavy anti-bot |
| Bilibili | bilibili.com | Dynamic content |
| Taobao/Tmall | taobao.com, tmall.com | Login required for most content |
| JD.com | jd.com | Anti-scraping protection |
| LinkedIn | linkedin.com | Strict bot detection |
| Instagram | instagram.com | Login wall |
| Twitter/X | twitter.com, x.com | Rate limiting, dynamic |

### Site Pattern Files

Detailed patterns are stored in:
```
references/site-patterns/
├── xiaohongshu.com.md
├── mp.weixin.qq.com.md
├── zhihu.com.md
└── weibo.com.md
```

**When browsing these sites:**
1. Read the pattern file first
2. Note the "Platform Features" and "Known Traps" sections
3. Use the suggested selectors and approaches

---

## Natural Language Workflows

### Workflow 1: Simple Page Fetch

**User says:** "Get me the content from https://example.com"

**Claude should think:**
1. Is this a known anti-bot site? → Check site patterns
2. Is it an article/blog URL? → Consider Jina AI
3. Start simple: try curl/FetchURL first
4. If that fails → escalate to browser

**Execution:**
```
Step 1: Try curl
  ↓ Success? → Return content
  ↓ Fail?
Step 2: Try Chrome CDP (if available)
  ↓ Success? → Return content
  ↓ Fail?
Step 3: Try agent-browser
  ↓ Success? → Return content
  ↓ Fail?
Step 4: Try Browserless API
  ↓ Success? → Return content
  ↓ Fail? → Report failure with suggestions
```

### Workflow 2: Article Extraction

**User says:** "Summarize this article: https://blog.example.com/post-123"

**Claude should think:**
1. URL pattern suggests article (/blog/, /post-/) → Jina AI is ideal
2. Try Jina first for token efficiency
3. If Jina fails → fall back to browser

**Execution:**
```
Step 1: Try Jina AI
  ↓ Success? → Return markdown content
  ↓ Fail?
Step 2: Try curl (in case Jina service is down)
  ↓ Success? → Return content
  ↓ Fail?
Step 3: Try Chrome CDP / agent-browser
  ↓ Success? → Return content
```

### Workflow 3: Dynamic Site with Login

**User says:** "Check my notifications on https://site.com/dashboard"

**Claude should think:**
1. Dashboard = dynamic site, likely requires login
2. Need persistent session → Chrome CDP required
3. Check if CDP is available
4. May need user to log in first

**Execution:**
```
Step 1: Check Chrome CDP availability
  ↓ Available?
    → Use mychrome scripts
    → User may need to log in manually first
  ↓ Not available?
    → Report: "Chrome CDP required for login sites"
    → Suggest: Start Chrome with --remote-debugging-port=9222
```

### Workflow 4: Anti-Bot Site

**User says:** "Get content from https://xiaohongshu.com/note/123"

**Claude should think:**
1. xiaohongshu.com = known anti-bot platform
2. Read site pattern file for specific guidance
3. Skip simple methods (curl/Jina), go straight to browser
4. Chrome CDP preferred over bundled Chromium

**Execution:**
```
Step 1: Read references/site-patterns/xiaohongshu.com.md
Step 2: Try Chrome CDP (with noted selectors from pattern)
  ↓ Success? → Return content
  ↓ Fail?
Step 3: Try agent-browser with stealth mode
  ↓ Success? → Return content
  ↓ Fail?
Step 4: Try Browserless API
```

### Workflow 5: Multi-Page Research

**User says:** "Research these 5 companies: [urls...]"

**Claude should think:**
1. Multiple independent targets → Parallel execution possible
2. Each URL may need different approach
3. Use parallel_research.py or handle sequentially

**Execution:**
```
Option A: Use parallel_research.py script
  → Concurrent execution
  → Each URL gets appropriate method

Option B: Sequential with method selection per URL
  → For each URL:
    → Detect best method
    → Fetch content
    → Aggregate results
```

---

## Helper Scripts Reference

These scripts are available but Claude decides when to use them based on context:

| Script | Purpose | When to Invoke |
|--------|---------|----------------|
| `scripts/browserless_helper.sh` | Cloud browser API | When local browsers unavailable |
| `scripts/site_experience.py` | Query site patterns | Before browsing known platforms |
| `scripts/parallel_research.py` | Multi-URL parallel | Research tasks with 3+ URLs |
| `scripts/jina_fetch.py` | Jina AI wrapper | Article extraction with validation |

---

## Error Handling Patterns

### Pattern: "Connection refused" on CDP
```
Error: curl: (7) Failed to connect to localhost:9222

Interpretation: Chrome CDP not running
Response: 
  1. Check if Chrome is running with remote debugging
  2. If not available, fall back to agent-browser
  3. If agent-browser not available, use Browserless API
```

### Pattern: "403 Forbidden" or blocking
```
Error: HTTP 403, or empty content from curl

Interpretation: Site blocks simple HTTP requests
Response:
  1. Escalate to browser automation
  2. Check site patterns for known anti-bot measures
  3. Use stealth techniques if available
```

### Pattern: JavaScript-required content
```
Observation: curl returns skeleton HTML, content loaded via JS

Interpretation: SPA or dynamic site
Response:
  1. Must use browser automation (CDP, agent-browser, or Browserless)
  2. Wait for networkidle before extracting
```

---

## Best Practices (Natural Language Guidelines)

### Do:
- **Start simple**, escalate complexity only when needed
- **Check site patterns** before attempting known anti-bot platforms
- **Prefer Jina AI** for articles to save tokens
- **Use Chrome CDP** when persistent sessions matter
- **Cache results** when appropriate
- **Report which method succeeded** for transparency

### Don't:
- Don't use curl for known anti-bot sites (wastes time)
- Don't use Jina for product pages or dashboards (wrong tool)
- Don't skip reading site patterns for complex platforms
- Don't forget to handle timeouts gracefully

---

## Version History

- **v2.0.0** - Refactored to natural language skill
- **v1.5.0** - Added smart_fetch.py with priority order
- **v1.0.0** - Basic agent-browser CLI wrapper

---

## Metadata for Claude

<skill_metadata>
<priority_order>
1. Chrome CDP (mychrome) - for persistent sessions and real Chrome
2. Bundled Chromium (agent-browser) - for quick tasks
3. Browserless API - for cloud fallback
4. curl/FetchURL - for static pages
5. Jina AI - for articles
</priority_order>

<anti_bot_sites>
xiaohongshu.com, mp.weixin.qq.com, zhihu.com, weibo.com, 
douyin.com, bilibili.com, taobao.com, linkedin.com, instagram.com
</anti_bot_sites>

<article_patterns>
/blog/, /article/, /post/, /news/, /docs/, /guide/, /tutorial/,
date paths (/2024/01/01/), long content slugs
</article_patterns>

<cdp_endpoint>http://localhost:9222</cdp_endpoint>

<site_patterns_dir>references/site-patterns/</site_patterns_dir>
</skill_metadata>
