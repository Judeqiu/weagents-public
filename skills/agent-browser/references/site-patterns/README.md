# Site Patterns Reference

This directory contains operational knowledge about specific websites to help Claude browse them effectively.

## How to Use These Files

**When Claude encounters a URL from one of these domains:**

1. Read the corresponding `.md` file
2. Note the `claude_priority` and `category` metadata
3. Follow the "Browsing Strategy" section
4. Use the provided selectors for content extraction
5. Be aware of "Known Traps" to avoid issues

## Site Categories

| Category | Sites | Characteristics |
|----------|-------|-----------------|
| `anti_bot_social` | xiaohongshu.com, weibo.com, instagram.com | Blocks simple HTTP, needs browser |
| `protected_content` | mp.weixin.qq.com | Login/permission required |
| `hybrid_rendering` | zhihu.com, bilibili.com | Mix of SSR and CSR |
| `spa_platform` | douyin.com, twitter.com | Full JavaScript apps |
| `e_commerce` | taobao.com, jd.com | Anti-scraping, dynamic pricing |

## File Format

Each site pattern file follows this structure:

```yaml
---
domain: example.com
aliases: ["别名1", "别名2"]
updated: YYYY-MM-DD
category: [category_name]
claude_priority: [use_browser_only | try_curl_first | article_friendly]
---

## Site Summary for Claude
Brief description of what this site is and how to approach it.

## Platform Characteristics
Table of technical details and implications.

## Browsing Strategy
Decision tree for which methods to use.

## URL Patterns
Common URL structures for different content types.

## Extraction Selectors
CSS selectors or JavaScript patterns for content extraction.

## Known Traps & Limitations
Issues to be aware of when browsing.

## Example Workflow
Step-by-step example of how Claude should handle a request for this site.
```

## Priority Values

| `claude_priority` | Meaning | Example Sites |
|-------------------|---------|---------------|
| `use_browser_only` | Skip curl/Jina, go straight to browser | xiaohongshu.com, instagram.com |
| `try_curl_first` | Simple HTTP might work | Static blogs, documentation |
| `article_friendly` | Jina AI works well | Medium, Substack, dev blogs |
| `login_required` | Needs Chrome CDP for session | LinkedIn, Facebook |

## Adding New Sites

To add a new site pattern:

1. Create `{domain}.md` file in this directory
2. Fill in YAML frontmatter with metadata
3. Document platform characteristics
4. Provide specific guidance for Claude
5. Include example URLs and selectors
6. Note any anti-bot measures or limitations
