# Agent Browser Skill

Natural language web browsing skill for Claude.

## Quick Start

```
You: "Get the content from https://example.com"

Claude: "I'll fetch that for you. Based on the URL pattern, I'll try the most 
appropriate method."
[Claude interprets SKILL.md, chooses method, executes, returns content]
```

## What's New in v2.0

- **Natural Language Skill**: No rigid scripts - Claude interprets instructions
- **CDP First Priority**: Chrome CDP (mychrome) is now the first choice for complex sites
- **Single Source of Truth**: Priority defined in SKILL.md, not code
- **Better Site Support**: Enhanced site patterns for anti-bot platforms

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | **Main skill definition** - Natural language instructions for Claude |
| `QUICKREF.md` | Quick reference card for common patterns |
| `ARCHITECTURE-v2.md` | Architecture documentation |
| `examples/workflow-examples.md` | Example scenarios showing how Claude handles requests |
| `references/site-patterns/` | Platform-specific browsing guidance |

## Usage

### Basic Browsing
```
"Get the article from https://blog.example.com/post-123"
```

### Anti-Bot Sites
```
"Get this 小红书 note: https://xiaohongshu.com/explore/..."
→ Claude knows to use browser automation directly
```

### With Screenshots
```
"Screenshot https://example.com and extract the text"
```

### Multi-URL Research
```
"Compare prices on these 3 sites: [urls]"
```

## Method Priority

Claude follows this priority (defined in SKILL.md):

1. **Chrome CDP (mychrome)** - For login sites, persistent sessions
2. **Bundled Chromium (agent-browser)** - Quick tasks, no external deps
3. **Browserless API** - Cloud fallback
4. **curl / FetchURL** - Simple static pages
5. **Jina AI** - Articles (token efficient)

## Site Patterns

Known platforms with special handling:

| Platform | File | Priority |
|----------|------|----------|
| 小红书 (Red) | `xiaohongshu.com.md` | Browser only |
| 微信 (WeChat) | `mp.weixin.qq.com.md` | Browser only |
| 知乎 (Zhihu) | `zhihu.com.md` | Browser only |
| 微博 (Weibo) | `weibo.com.md` | Browser only |

## For Developers

### Old vs New Approach

**Before (v1.x)**:
```python
# Script decides
python3 scripts/smart_fetch.py --url https://example.com
```

**Now (v2.0)**:
```
# Claude decides based on natural language skill
"Get the content from https://example.com"
```

### Legacy Scripts

Scripts in `scripts/` directory are maintained for backwards compatibility:
- `smart_fetch.py` - Legacy priority-based fetcher (deprecated)
- `browserless_helper.sh` - Cloud browser utility
- `site_experience.py` - Site pattern query tool
- `parallel_research.py` - Multi-URL research

New interactions should use the natural language skill instead.

## Architecture

```
User Request
    ↓
Claude reads SKILL.md
    ↓
Natural language decision tree
    ↓
Choose appropriate tool
    ↓
Execute and return result
```

See `ARCHITECTURE-v2.md` for details.

## Version History

- **v2.0.0** - Natural language skill refactor
- **v1.5.0** - Smart fetch with priority order
- **v1.0.0** - Basic agent-browser CLI wrapper

## License

Part of the OpenClaw skill ecosystem.
