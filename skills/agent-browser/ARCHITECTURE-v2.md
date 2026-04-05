# Agent Browser v2.0 - Architecture

## Overview

Agent Browser has been refactored from a **script-based skill** to a **natural language skill** optimized for Claude.

### Key Changes

| Aspect | v1.x (Script-Based) | v2.0 (Natural Language) |
|--------|---------------------|------------------------|
| **Control Flow** | Hardcoded in Python/Bash scripts | Interpreted by Claude from SKILL.md |
| **Priority Logic** | `PRIORITY_ORDER` constant in code | Natural language decision tree |
| **Site Knowledge** | Parsed by Python scripts | Read and interpreted by Claude |
| **Tool Selection** | Script decides which tool to call | Claude decides based on context |
| **Extensibility** | Edit Python files | Update markdown documentation |
| **Maintenance** | Code changes require testing | Documentation updates |

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Claude's Decision Engine                           │
│ (Natural language interpretation of SKILL.md)               │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Helper Scripts (optional)                          │
│ (browserless_helper.sh, site_experience.py, etc.)           │
│ → These provide utilities but don't control flow            │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Site Patterns                                      │
│ (Markdown files with platform knowledge)                    │
│ → Claude reads these to understand specific sites           │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Core Tools                                         │
│ (Chrome CDP, agent-browser, curl, Jina AI)                  │
│ → Standard tools Claude can invoke                          │
└─────────────────────────────────────────────────────────────┘
```

---

## File Organization

```
agent-browser/
├── SKILL.md                    # Main skill definition (natural language)
├── QUICKREF.md                 # Quick reference for common patterns
├── ARCHITECTURE-v2.md          # This file
├── examples/
│   └── workflow-examples.md    # Example scenarios and responses
├── references/
│   ├── browsing-philosophy.md  # Design philosophy
│   └── site-patterns/
│       ├── README.md           # How to use site patterns
│       ├── xiaohongshu.com.md  # Platform-specific guidance
│       ├── zhihu.com.md
│       └── ...
└── scripts/                    # Helper utilities (not primary interface)
    ├── browserless_helper.sh   # Cloud browser API wrapper
    ├── site_experience.py      # Site pattern query tool
    ├── parallel_research.py    # Multi-URL research
    └── jina_fetch.py           # Jina AI wrapper
```

---

## How It Works

### Scenario: User asks to browse a URL

**v1.x Approach**:
1. User requests URL
2. Claude calls `smart_fetch.py`
3. Script internally decides priority
4. Script executes commands
5. Script returns result

**v2.0 Approach**:
1. User requests URL
2. Claude reads SKILL.md for guidance
3. Claude interprets context (URL pattern, site category, etc.)
4. Claude decides which tool to use based on natural language rules
5. Claude invokes appropriate tool(s)
6. Claude returns formatted result

### Example Decision Flow

```
User: "Get content from https://xiaohongshu.com/note/123"

Claude:
1. Analyze URL → xiaohongshu.com (known anti-bot platform)
2. Read SKILL.md → "Known Anti-Bot Platforms" section
3. Check site-patterns/xiaohongshu.com.md → "use_browser_only"
4. Decision: Skip curl/Jina, use Chrome CDP directly
5. Check if CDP available (curl localhost:9222)
6. Execute: chrome_cdp_helper.py --url ...
7. Return extracted content
```

---

## Advantages of Natural Language Skill

### 1. **Flexibility**
- No rigid code paths
- Claude can adapt based on full context
- Easy to handle edge cases

### 2. **Maintainability**
- Update markdown files instead of code
- No syntax errors in Python/Bash
- Version control friendly

### 3. **Clarity**
- Intent is documented in natural language
- Site patterns are readable
- Examples show expected behavior

### 4. **Composability**
- Mix and match tools as needed
- Combine with other skills naturally
- No script dependencies to manage

---

## Migration Guide

### For Users

**Before (v1.x)**:
```bash
# Rely on script's internal priority
python3 scripts/smart_fetch.py --url https://example.com
```

**After (v2.0)**:
```
# Ask Claude naturally
"Get the content from https://example.com"

# Claude decides the best approach based on:
# - Site type
# - Content category  
# - Available tools
# - Your goal
```

### For Developers

**Before (v1.x)**:
- Edit `smart_fetch.py` to change priority
- Modify `PRIORITY_ORDER` constant
- Test script execution
- Update version

**After (v2.0)**:
- Edit `SKILL.md` to change guidance
- Update natural language instructions
- Add examples if needed
- Site patterns are self-documenting

---

## When to Use Helper Scripts

The scripts in `scripts/` directory are still useful but are now **utilities** rather than **controllers**:

| Script | When to Use |
|--------|-------------|
| `browserless_helper.sh` | When you specifically need cloud browser |
| `site_experience.py` | When you want to query site patterns programmatically |
| `parallel_research.py` | When processing many URLs in parallel |
| `jina_fetch.py` | When you specifically want Jina AI with validation |

**Default**: Let Claude decide based on natural language skill.

---

## Best Practices

### Writing Site Patterns

1. Use clear YAML frontmatter
2. Include `claude_priority` hint
3. Document platform characteristics in tables
4. Provide specific CSS selectors
5. Include example workflows

### Writing Examples

1. Show the thought process
2. Provide alternative paths (if X fails, try Y)
3. Include realistic response formats
4. Document common pitfalls

### Using the Skill

1. Ask Claude naturally - no special syntax needed
2. Provide context about what you need
3. Mention if you know the site requires special handling
4. Let Claude check site patterns when unsure

---

## Future Enhancements

Possible improvements for v2.x:

1. **More Site Patterns**: Expand coverage of popular platforms
2. **Interactive Mode**: Claude asks clarifying questions when uncertain
3. **Result Caching**: Remember what worked for specific sites
4. **Feedback Loop**: Learn from successes/failures
5. **Multi-Modal**: Handle images, PDFs, videos more intelligently

---

## Backwards Compatibility

The old scripts (`smart_fetch.py`, `fetch_content.sh`) are preserved for:
- Existing automation that depends on them
- Headless/non-Claude usage
- Specific use cases requiring deterministic behavior

**Recommendation**: For new Claude interactions, use the natural language skill approach rather than calling scripts directly.
