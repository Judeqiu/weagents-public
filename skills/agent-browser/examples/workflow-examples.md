# Agent Browser - Workflow Examples

This file shows how Claude should handle different browsing scenarios using natural language decision making.

---

## Example 1: Simple Blog Article

**User Request**: "Get the content from https://techblog.example.com/posts/2024/03/ai-trends"

### Claude's Thought Process

1. **Analyze URL**: Contains `/posts/2024/03/` - date path pattern suggests article
2. **Check category**: Likely `article_friendly`
3. **Decision**: Try Jina AI first (token efficient for articles)

### Execution

```bash
# Step 1: Try Jina AI (preferred for articles)
curl -sL "https://r.jina.ai/https://techblog.example.com/posts/2024/03/ai-trends"
```

**If Success**: Return markdown content to user

**If Fail**:
```bash
# Step 2: Try curl as fallback
curl -sL "https://techblog.example.com/posts/2024/03/ai-trends"
```

**If Still Fail**:
```bash
# Step 3: Use browser automation
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --url "https://techblog.example.com/posts/2024/03/ai-trends" \
  --extract-content
```

### Response Format

```markdown
# AI Trends in 2024
[Article content in clean markdown...]

---
*Retrieved using Jina AI at 2024-03-15*
```

---

## Example 2: Anti-Bot Platform (小红书)

**User Request**: "Get this 小红书 post: https://www.xiaohongshu.com/explore/6568abc123def45678901234"

### Claude's Thought Process

1. **Analyze URL**: `xiaohongshu.com` - known anti-bot platform
2. **Read site pattern**: Check `references/site-patterns/xiaohongshu.com.md`
3. **Key findings**:
   - Category: `anti_bot_social`
   - Priority: `use_browser_only`
   - Login required for full content
   - SPA architecture
4. **Decision**: Skip curl/Jina, go straight to Chrome CDP

### Execution

```bash
# Step 1: Check if Chrome CDP is available
curl -s http://localhost:9222/json/version

# If available, proceed with CDP
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --url "https://www.xiaohongshu.com/explore/6568abc123def45678901234" \
  --extract-content
```

**If CDP Not Available**:
```bash
# Fall back to agent-browser
agent-browser open "https://www.xiaohongshu.com/explore/6568abc123def45678901234" && \
  agent-browser snapshot -i && \
  agent-browser close
```

**If Still Fail**:
```bash
# Use Browserless API
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh \
  content --url "https://www.xiaohongshu.com/explore/6568abc123def45678901234"
```

### Response Format

```markdown
# 小红书 Note

**Title**: [提取的标题]
**Author**: [用户名]
**Content**: 
[正文内容...]

**Images**: 3 images visible (login required for full album)

**Note**: This content was retrieved using browser automation due to platform restrictions.
```

---

## Example 3: Product Page (E-commerce)

**User Request**: "Check the price and availability of https://shop.example.com/products/laptop-123"

### Claude's Thought Process

1. **Analyze URL**: `/products/` path - e-commerce site
2. **Considerations**:
   - Likely dynamic content (price may load via JS)
   - May have anti-scraping measures
   - Need accurate, up-to-date information
3. **Decision**: Try browser method directly (skip curl)

### Execution

```bash
# Try Chrome CDP first for best results
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --url "https://shop.example.com/products/laptop-123" \
  --screenshot /tmp/product-page.png \
  --extract-content
```

### Response Format

```markdown
# Product Information

**Product**: [Name]
**Price**: $XXX (as of [timestamp])
**Availability**: [In Stock / Out of Stock]
**Key Specs**:
- [Spec 1]
- [Spec 2]

**Screenshot**: [Attached or referenced]

*Note: Prices may change. Screenshot captured for verification.*
```

---

## Example 4: Documentation Page

**User Request**: "Get the API docs from https://docs.api.example.com/v2/authentication"

### Claude's Thought Process

1. **Analyze URL**: `/docs/` path - documentation site
2. **Characteristics**:
   - Usually static or minimally dynamic
   - Technical content - accuracy important
   - Often markdown-friendly structure
3. **Decision**: Try curl first, fall back to Jina if structured extraction needed

### Execution

```bash
# Step 1: Try curl
curl -sL "https://docs.api.example.com/v2/authentication"
```

**If content is messy HTML**:
```bash
# Step 2: Use Jina for cleaner extraction
curl -sL "https://r.jina.ai/https://docs.api.example.com/v2/authentication"
```

### Response Format

```markdown
# API Documentation: Authentication

## Overview
[Clean markdown content...]

## Endpoints
[Structured endpoint documentation...]

---
*Retrieved from docs.api.example.com*
```

---

## Example 5: Multi-Site Research

**User Request**: "Compare pricing for product X across these sites: [5 URLs]"

### Claude's Thought Process

1. **Task**: Multiple independent fetches
2. **Strategy**: Parallel execution with appropriate method per site
3. **Create plan for each URL based on domain analysis

### Execution

```bash
# Use parallel_research.py for efficiency
python3 ~/.openclaw/workspace/skills/agent-browser/scripts/parallel_research.py \
  --targets '[
    {"name": "Amazon", "url": "https://amazon.com/dp/XXX", "method": "browser"},
    {"name": "Best Buy", "url": "https://bestbuy.com/product/XXX", "method": "browser"},
    {"name": "Official Store", "url": "https://brand.com/products/XXX", "method": "auto"}
  ]' \
  --output pricing_comparison.md
```

Or handle sequentially with method selection:

```bash
# For each URL:
# 1. Detect domain type
# 2. Choose appropriate method
# 3. Extract pricing info
# 4. Aggregate results
```

### Response Format

```markdown
# Pricing Comparison: Product X

| Retailer | Price | Availability | Notes |
|----------|-------|--------------|-------|
| Amazon | $XXX | In Stock | Prime eligible |
| Best Buy | $XXX | In Stock | Store pickup available |
| Official | $XXX | In Stock | Warranty included |

**Best Deal**: [Analysis...]

*Data retrieved: [timestamp]*
```

---

## Example 6: Site Requiring Login

**User Request**: "Check my notifications on https://github.com/notifications"

### Claude's Thought Process

1. **Analyze URL**: GitHub notifications - requires authenticated session
2. **Key requirement**: Persistent login state
3. **Decision**: Must use Chrome CDP with existing session

### Execution

```bash
# Check Chrome CDP availability
curl -s http://localhost:9222/json/version

# Use CDP - assuming user is already logged in Chrome
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --cdp-url http://localhost:9222 \
  --url "https://github.com/notifications" \
  --extract-content
```

**If not logged in**:
Inform user: "You need to be logged into GitHub in Chrome. Please log in first, then I can check your notifications."

### Response Format

```markdown
# GitHub Notifications

**Unread**: X notifications

1. [Repo] [Notification title] - [time ago]
2. [Repo] [Notification title] - [time ago]
...

**Note**: Retrieved from your authenticated GitHub session.
```

---

## Example 7: JavaScript-Heavy SPA

**User Request**: "Get the trending videos from https://video-platform.com/trending"

### Claude's Thought Process

1. **Analyze URL**: Video platform trending page
2. **Characteristics**:
   - Likely SPA (Single Page Application)
   - Content loaded dynamically via JS
   - Scroll to load more
3. **Decision**: Browser automation required

### Execution

```bash
# Use Chrome CDP for JavaScript execution
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --url "https://video-platform.com/trending" \
  --wait-for-networkidle \
  --extract-content
```

Or with agent-browser:

```bash
agent-browser open "https://video-platform.com/trending"
agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser close
```

### Response Format

```markdown
# Trending Videos

1. **[Title 1]** - [Creator] - [Views]
2. **[Title 2]** - [Creator] - [Views]
3. ...

*Retrieved via browser automation (JavaScript rendering required)*
```

---

## Summary: Claude's Decision Checklist

For every browsing request, ask:

1. [ ] **What type of site is this?**
   - Anti-bot platform? → Use browser only
   - Article/blog? → Try Jina first
   - Static content? → Try curl first
   - Login required? → Use Chrome CDP

2. [ ] **What is the user's goal?**
   - Quick content? → Fastest working method
   - Accurate data? → Browser for dynamic sites
   - Token efficiency? → Jina for articles
   - Screenshot/visual? → Browser required

3. [ ] **What tools are available?**
   - Chrome CDP running? → Preferred for complex sites
   - agent-browser installed? → Good fallback
   - Browserless configured? → Cloud fallback

4. [ ] **Should I check site patterns?**
   - Known platform (小红书, 微信, etc.)? → Read pattern file first
   - Unfamiliar site? → Start simple, adapt based on results

Remember: **Adapt based on results**, not rigid rules. If a method fails, escalate intelligently.
