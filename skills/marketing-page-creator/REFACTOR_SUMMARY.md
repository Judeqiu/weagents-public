# Marketing Page Creator - Refactor Summary

## Before (Script-Driven) ❌

### User Experience
```bash
# User had to type exact commands
./scripts/create_marketing_page.sh \
  --name "mens-shoes" \
  --topic "Men's Running Shoes" \
  --sites "amazon,asos" \
  --items 5 \
  --template deals \
  --deploy
```

### Problems
1. **Rigid workflow** - One script controlled everything
2. **No flexibility** - Can't adapt to partial failures
3. **Hard to modify** - Want to change one product? Restart entire pipeline
4. **Brittle** - One step fails = everything fails
5. **No reasoning** - No explanation of decisions

### Architecture
```
User → create_marketing_page.sh (orchestrator)
           ├── research_products.sh (heavy, complex)
           ├── generate_page.sh (heavy, complex)
           └── deploy_to_netlify.sh
```

---

## After (Natural Language Driven) ✅

### User Experience
> "Create a deals page for men's running shoes"

That's it. The LLM handles the rest.

### Benefits
1. **Natural language** - Just describe what you want
2. **Adaptive** - LLM can retry, suggest alternatives, adjust on the fly
3. **Transparent** - LLM explains each step and asks for approval
4. **Composable** - Tools are simple, focused, reusable
5. **Resilient** - One tool fails, LLM can work around it

### Architecture
```
User → Natural language request
           ↓
    LLM interprets intent
           ↓
    ┌──────┼──────┬──────┐
    ▼      ▼      ▼      ▼
 research filter generate deploy
   _site   _products _page   
    │      │      │      │
    └──────┴──────┴──────┘
           ↓
    Results presented
    for user approval
```

---

## File Changes

### Deleted (Old Script-Heavy Approach)
| File | Size | Purpose |
|------|------|---------|
| `create_marketing_page.sh` | 19KB | Heavy orchestrator (GONE) |
| `research_products.sh` | 14KB | Complex multi-site script (GONE) |
| `research_amazon_real.sh` | 11KB | Amazon-specific scraper (GONE) |
| `generate_page.sh` (old) | 10KB | Overly complex generator (GONE) |
| `deploy_to_netlify.sh` | 1.5KB | Simple but replaced |

### Created (New Tool-Based Approach)
| File | Size | Purpose |
|------|------|---------|
| `tools/research_site.sh` | 11KB | Research ONE site with anti-bot protection |
| `tools/research_parallel.sh` | 2.2KB | Research multiple sites in parallel |
| `tools/fetch_product_page.sh` | 2.5KB | Fetch specific product URL |
| `tools/filter_products.sh` | 1.7KB | Filter/sort products |
| `tools/generate_page.sh` | 9KB | Generate HTML page |
| `tools/deploy.sh` | 1.2KB | Deploy to Netlify |
| `SKILL.md` (new) | 11KB | Natural language orchestration guide |
| `LLM_GUIDE.md` | 6KB | Quick reference for LLMs |

### Size Comparison
- **Old scripts total:** ~56KB of bash orchestration
- **New tools total:** ~32KB of focused tools
- **Note:** Size increased due to anti-bot handling, but complexity is much lower

---

## Usage Comparison

### Scenario: Create deals page for summer dresses

#### OLD WAY (Script-Driven)
```bash
# User must construct exact command
./scripts/create_marketing_page.sh \
  --name "summer-dresses" \
  --topic "Summer Dress Deals" \
  --sites "asos,johnlewis,next" \
  --items 6 \
  --template deals \
  --color "#ff6b6b" \
  --deploy

# Problems:
# - If Next fails, whole script fails
# - Can't see products before deploying
# - Can't say "skip the floral one"
# - Must remember all flag names
```

#### NEW WAY (Natural Language Driven)
```
User: "Create a deals page for summer dresses"

Agent: I'll research ASOS, John Lewis, and Next for summer dress deals.
       
       Found 18 dresses. Here are the top 6 by discount:
       
       [shows table]
       
       Should I proceed with these, or would you like adjustments?

User: "Remove the red one and add something cheaper"

Agent: Removed the red dress. Found 2 cheaper options - adding the £18 one.
       
       Proceed with these 6?

User: "Yes, deploy it"

Agent: ✓ Page created and deployed: https://summer-dresses-xyz.netlify.app
```

---

## Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **User Input** | CLI flags | Natural language |
| **Orchestration** | Rigid bash script | Flexible LLM reasoning |
| **Error Handling** | Script exits | LLM adapts and informs |
| **User Control** | All or nothing | Step-by-step approval |
| **Modifiability** | Restart from scratch | Edit at any point |
| **Debugging** | Read bash code | LLM explains decisions |
| **Extensibility** | Edit complex scripts | Add simple tools |

---

## Migration Guide

If you were using the old scripts:

| Old Command | New Approach |
|-------------|--------------|
| `create_marketing_page.sh --name X --topic Y --sites A,B` | Just say: "Create a page about Y from sites A and B" |
| `research_products.sh --query X --sites A,B` | LLM calls `research_site.sh` for each site |
| `generate_page.sh --input X --template deals` | LLM calls `generate_page.sh` after approval |
| `deploy_to_netlify.sh --dir X` | LLM calls `deploy.sh` when you're ready |

---

## Anti-Bot Protection (New in 2.1)

### The Problem
Sites like Amazon aggressively block automated access:
- CAPTCHA challenges
- JavaScript requirements
- IP-based blocking
- Rate limiting

### The Solution
New `research_site.sh` automatically handles this:

```
Attempt 1: curl (0.5s)
    ↓ Blocked (CAPTCHA detected)
Attempt 2: agent-browser (Chromium)
    ↓ Success!
    ↓ Extract real product data
```

### Fallback Chain
If one method fails, automatically tries:
1. **curl** - Fast HTTP request
2. **agent-browser** - Local Chromium
3. **mychrome** - Chrome CDP (if available)
4. **Browserless API** - Cloud browser (always works)
5. **mock data** - Simulated data as last resort

### Agent-Browser Integration
```bash
# research_site.sh automatically uses:
~/.openclaw/workspace/skills/agent-browser/scripts/fetch_content.sh
# Which tries: agent-browser → mychrome → Browserless → curl
```

**Result:** Real product data even from heavily protected sites.

---

## Philosophy

> **Scripts are tools, not orchestrators.**

The LLM should handle the "thinking" part:
- Deciding which sites to research
- Handling partial failures gracefully
- Presenting options for approval
- Explaining trade-offs

Scripts should do one thing well:
- Research ONE site
- Filter a list
- Generate HTML
- Deploy

This separation makes the skill more powerful, flexible, and maintainable.
