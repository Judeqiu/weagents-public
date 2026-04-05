# Agent Browser - Quick Reference

## Decision Tree (Read This First)

```
User asks to browse/fetch a URL
│
├─ Is it a known anti-bot site? (小红书, 微信, 知乎, etc.)
│  └─ YES → Skip to browser methods (CDP > agent-browser > Browserless)
│
├─ Is it an article/blog URL? (/blog/, /article/, /docs/, date path)
│  └─ YES → Try Jina AI first → then browser if fails
│
├─ Does it need login/persistent session?
│  └─ YES → Use Chrome CDP (mychrome)
│
└─ Default path:
   1. Try curl/FetchURL (fastest)
   2. If fails → Chrome CDP
   3. If fails → agent-browser
   4. If fails → Browserless API
```

## One-Liners

### Check What's Available
```bash
# Check Chrome CDP
curl -s http://localhost:9222/json/version && echo "CDP OK" || echo "CDP not running"

# Check agent-browser
which agent-browser && echo "agent-browser OK" || echo "agent-browser not installed"
```

### Quick Fetch by Method
```bash
# Method 1: Chrome CDP (preferred for complex sites)
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --url "https://example.com" --extract-content

# Method 2: agent-browser (quick, no session)
agent-browser open "https://example.com" && agent-browser content && agent-browser close

# Method 3: Browserless (cloud fallback)
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh \
  content --url "https://example.com"

# Method 4: curl (static pages)
curl -sL "https://example.com"

# Method 5: Jina AI (articles)
curl -sL "https://r.jina.ai/https://example.com/article"
```

## Site Categories

| If URL contains... | Likely Type | Start With |
|-------------------|-------------|------------|
| xiaohongshu.com, xhslink.com | Anti-bot social | CDP / Browserless |
| mp.weixin.qq.com | Protected content | CDP |
| zhihu.com | Q&A platform | CDP |
| weibo.com | Social media | CDP |
| /blog/, /article/, /post/ | Article | Jina AI |
| /docs/, /guide/, /tutorial/ | Documentation | Jina AI |
| /2024/, /2023/ (date) | Blog post | Jina AI |
| /product/, /item/, /shop/ | E-commerce | CDP |
| /dashboard/, /admin/, /panel/ | Dynamic app | CDP |

## Common Patterns

### Read Article
```bash
# Token-efficient approach
curl -sL "https://r.jina.ai/https://blog.example.com/my-post"
```

### Screenshot Page
```bash
# Using Chrome CDP
python3 ~/.openclaw/workspace/skills/mychrome/scripts/chrome_cdp_helper.py \
  --url "https://example.com" --screenshot /tmp/page.png

# Using Browserless
~/.openclaw/workspace/skills/agent-browser/scripts/browserless_helper.sh \
  screenshot --url "https://example.com" --output /tmp/page.png
```

### Multi-URL Research
```bash
# Parallel research
python3 ~/.openclaw/workspace/skills/agent-browser/scripts/parallel_research.py \
  --targets '[
    {"name": "Site A", "url": "https://a.com", "task": "extract pricing"},
    {"name": "Site B", "url": "https://b.com", "task": "extract pricing"}
  ]' --output results.md
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| curl returns empty/403 | Site blocks bots → Use browser method |
| Jina returns error | Not an article or service down → Try curl or browser |
| CDP connection refused | Chrome not running with --remote-debugging-port=9222 |
| agent-browser not found | Run: `npm install -g agent-browser` |
| Browserless fails | Check token / network / try different region |

## Environment Variables

```bash
# Chrome CDP endpoint
export CHROME_CDP_URL=http://localhost:9222

# Browserless region (sfo, lon, ams)
export BROWSERLESS_REGION=sfo

# agent-browser args
export AGENT_BROWSER_ARGS="--no-sandbox"
```
