---
domain: xiaohongshu.com
aliases: ["小红书", "小红书笔记", "xhs"]
updated: 2026-03-22
category: anti_bot_social
claude_priority: use_browser_only
---

## Site Summary for Claude

**小红书 (Xiaohongshu/Red)** is a Chinese lifestyle sharing platform with strict anti-bot protection. 

**Key Rule**: Skip simple HTTP methods (curl, Jina) - they won't work. Go directly to browser automation.

## Platform Characteristics

| Aspect | Details | Implication for Browsing |
|--------|---------|------------------------|
| **Architecture** | Single Page Application (SPA) | JavaScript rendering required |
| **Anti-Bot Level** | Strict | Blocks curl, needs real browser |
| **Login Requirement** | Required for full content | Without login: only 3 images visible |
| **Content Loading** | Scroll-triggered lazy loading | Need to scroll to load all content |
| **Image Protection** | Anti-hotlinking with referer check | Browser must handle headers correctly |

## Browsing Strategy

### For Claude: Follow This Priority

```
1. Chrome CDP (mychrome) - BEST
   → Real Chrome with proper fingerprint
   → Can maintain login session
   → Handles lazy loading well

2. agent-browser - GOOD
   → Bundled Chromium with stealth
   → May need to handle visibility checks

3. Browserless API - FALLBACK
   → Cloud browser if local unavailable
   → May have different IP geolocation
```

### DO NOT Use
- ❌ curl / wget - Returns empty or blocked
- ❌ Jina AI - Not applicable for social content
- ❌ Simple HTTP fetch - Will fail

## URL Patterns

| Content Type | URL Pattern | Example |
|-------------|-------------|---------|
| Note/Post | `/explore/{note_id}` | `/explore/6568abc123def45678901234` |
| User Profile | `/user/profile/{user_id}` | `/user/profile/5f4e3d2c1b0a9f8e7d6c5b4a` |
| Search Results | `/search_result?keyword=` | `/search_result?keyword=护肤` |

**Note**: Note IDs are 24-character hexadecimal strings.

## Extraction Selectors

### Note Content
```javascript
// Title
.note-container .title
.note-content .title

// Description/Content  
.note-content .desc
.note-text

// Images
.swiper-slide img[src]
.note-content img

// Author info
.author-info .username
```

### Important for Claude
When extracting content:
1. Wait for page to fully load (SPA navigation)
2. Scroll down to trigger lazy loading of images
3. Check for login wall - if present, note that login is required
4. Images may be Canvas-rendered - screenshot may be more reliable than DOM extraction

## Known Traps & Limitations

| Issue | Details | Workaround |
|-------|---------|------------|
| Image limit without login | Only 3 images visible | Inform user login needed |
| Rate limiting | Frequent visits trigger captcha/IP ban | Add delays, rotate methods |
| Canvas rendering | Text may be rendered as Canvas | Use screenshot + OCR if needed |
| Dynamic fonts | Custom font rendering | Text extraction may be garbled |
| Mobile-first | Desktop site is mobile-responsive | Use mobile viewport for consistency |

## Example Workflow for Claude

**User**: "Get this 小红书 note: https://www.xiaohongshu.com/explore/6568abc123def45678901234"

**Claude should do**:
1. Recognize domain as anti-bot platform
2. Skip curl/Jina - won't work
3. Check Chrome CDP availability
4. If available → use CDP with proper wait and scroll
5. If not available → try agent-browser
6. Extract title, description, image URLs
7. Note if content is truncated (login required)

**Expected output format**:
```markdown
# 小红书 Note
**Title**: [title]
**Author**: [username]  
**Content**: [description text]
**Images**: [count] images (3 visible without login)
**Note**: Full content requires login
```
