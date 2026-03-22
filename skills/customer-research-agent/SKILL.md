---
name: customer-research-agent
description: Use when needing to research B2B customer backgrounds, analyze potential clients, generate sales briefs, or prepare first-touch emails. Automates the "understand customer" pre-sales workflow using Chrome CDP browser automation.
---

# Customer Research Agent

Automated customer background research for B2B sales. Transforms 2 hours of manual research into minutes of automated data gathering and AI-powered analysis.

## What It Does

This skill automates the complete pre-sales research workflow:

1. **Information Gathering** - Searches Google, scrapes company websites, finds LinkedIn profiles
2. **Customer Analysis** - Classifies customer type, evaluates priority, assesses business fit
3. **Sales Preparation** - Generates talking points, sales approach recommendations
4. **Email Generation** - Creates personalized first-touch email drafts

## Prerequisites

### Chrome with Remote Debugging

Chrome must be running with CDP (Chrome DevTools Protocol) enabled:

```bash
# Start Chrome with remote debugging
google-chrome \
  --no-sandbox \
  --disable-gpu \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.chrome-research \
  --window-size=1920,1080
```

**Verify CDP is working:**
```bash
curl http://127.0.0.1:9222/json/version
```

## Quick Start

### Research a Company

```bash
python3 ~/.config/agents/skills/customer-research-agent/scripts/research_customer.py \
  --company "TechVision Automation GmbH" \
  --output ./research_output
```

### Research from Email

```bash
# Save email to file first
echo "From: hans@techvision.de..." > /tmp/inquiry.txt

python3 ~/.config/agents/skills/customer-research-agent/scripts/research_customer.py \
  --email /tmp/inquiry.txt \
  --output ./research_output
```

## Workflow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Input: Company │────▶│  Search & Scrape │────▶│  AI Analysis    │
│  Name or Email  │     │  (Google/Website │     │  (Classification│
│                 │     │  /LinkedIn)      │     │  /Priority)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                           ┌──────────────────┐          │
                           │  Output: Report  │◀─────────┤
                           │  + Email Draft   │          │
                           └──────────────────┘          │
                                    ▲                    │
                                    │            ┌───────┴─────────┐
                                    └────────────│  CRM Update     │
                                                 │  (Optional)     │
                                                 └─────────────────┘
```

## Step-by-Step Usage

### Step 1: Run Research Script

```bash
cd ~/.config/agents/skills/customer-research-agent

python3 scripts/research_customer.py \
  --company "Company Name Here" \
  --output ./output
```

**Output files created:**
- `{company}_{timestamp}_data.json` - Raw research data
- `{company}_{timestamp}_report.md` - Human-readable report

### Step 2: AI Analysis (Using OpenClaw)

The script outputs an analysis prompt at the end. Use this prompt with your LLM:

```
---OPENCLAW_OUTPUT---
{
  "analysis_prompt": "You are an expert B2B sales researcher..."
}
```

**Process:**
1. Copy the analysis prompt
2. Send to LLM for customer classification and assessment
3. Save the JSON response to a file

### Step 3: Generate Email Draft

Use the analysis results to generate a personalized first-touch email:

```bash
# With analysis file
python3 scripts/research_customer.py \
  --company "Company Name" \
  --analysis-file ./output/analysis.json \
  --output ./output
```

Or manually prompt the LLM with the generated email prompt.

### Step 4: Review and Use

Final outputs include:
- **Customer Brief** - One-page summary with classification, priority, talking points
- **Email Draft** - Personalized first-touch email ready to send
- **Structured Data** - JSON format for CRM integration

## Output Format

### Customer Brief Structure

```json
{
  "company_summary": "Brief description of company business",
  "customer_type": "End User | Distributor | System Integrator | OEM | Competitor",
  "priority_score": "High | Medium | Low",
  "priority_reasoning": "Explanation of priority assessment",
  "industry_segment": "Primary industry classification",
  "potential_value": "Estimated deal size or strategic value",
  "key_contacts": ["Identified personnel"],
  "business_fit": "Assessment of fit with ideal customer profile",
  "sales_approach": "Recommended strategy",
  "talking_points": ["Conversation starters"],
  "red_flags": ["Concerns to watch"],
  "next_steps": ["Recommended actions"]
}
```

### Email Draft Structure

- **Subject Line** - Compelling and relevant
- **Opening** - Personalized hook
- **Value Proposition** - How you can help
- **Proof Point** - Credibility statement
- **Call to Action** - Specific next step
- **Sign-off** - Professional closing

## Advanced Usage

### Custom Chrome CDP URL

```bash
export CHROME_CDP_URL="http://remote-server:9222"

python3 scripts/research_customer.py \
  --company "Company Name" \
  --cdp-url "$CHROME_CDP_URL"
```

### Batch Processing

For multiple companies, create a script:

```bash
#!/bin/bash
COMPANIES=("Company A" "Company B" "Company C")

for company in "${COMPANIES[@]}"; do
  python3 scripts/research_customer.py \
    --company "$company" \
    --output ./batch_output
done
```

### Integration with CRM

The JSON output can be directly imported into CRM systems:

```python
import json

# Load research data
with open('research_data.json') as f:
    data = json.load(f)

# Extract for CRM
crm_record = {
    'company_name': data['company_name'],
    'customer_type': analysis['customer_type'],
    'priority': analysis['priority_score'],
    'industry': analysis['industry_segment'],
    'research_date': data['timestamp']
}
```

## Common Issues

### "Cannot connect to Chrome"

**Problem:** Chrome not running or CDP not enabled.

**Solution:**
```bash
# Check if Chrome is running
ps aux | grep chrome

# Start Chrome with CDP
google-chrome --remote-debugging-port=9222 --user-data-dir=~/.chrome-research &

# Verify
 curl http://127.0.0.1:9222/json/version
```

### "No search results found"

**Problem:** Google may block automated searches.

**Solution:**
- Ensure stealth scripts are working (check `navigator.webdriver`)
- Use a different IP or add delays between requests
- Consider using a Google API key alternative

### "Website scraping returned empty"

**Problem:** Site uses heavy JavaScript or blocks scraping.

**Solution:**
- The script already waits for networkidle and applies stealth
- Increase sleep time in `scrape_website()` method if needed
- Some sites may require authentication

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `research_customer.py` | Main research script |

### research_customer.py Options

| Option | Description |
|--------|-------------|
| `--company, -c` | Company name to research |
| `--email, -e` | Path to email content file |
| `--output, -o` | Output directory (default: ./research_output) |
| `--cdp-url` | Chrome CDP URL (default: http://127.0.0.1:9222) |
| `--analysis-file, -a` | Path to AI analysis JSON |
| `--email-draft` | Path to generated email draft |

## Performance

| Task | Traditional | With This Skill |
|------|-------------|-----------------|
| Web research | 60-90 min | 2-3 min |
| LinkedIn search | 20-30 min | 1-2 min |
| Analysis & brief | 30-45 min | Instant (with AI) |
| Email writing | 20-30 min | Instant (with AI) |
| **Total** | **2+ hours** | **5-10 minutes** |

## Best Practices

1. **Keep Chrome running** - Use systemd or screen to maintain the browser session
2. **Review AI analysis** - Always verify AI-generated classifications and recommendations
3. **Personalize emails** - Use generated emails as starting points, add human touch
4. **Update regularly** - Re-research customers quarterly or before major outreach
5. **Save outputs** - Maintain a research database for ongoing sales intelligence

## Security Notes

- Chrome CDP provides full browser control - secure your VPS
- Research data may contain sensitive business information
- Store outputs securely and follow your organization's data policies
- Google searches may be rate-limited; use responsibly

## Future Enhancements

Planned additions to this skill:
- Automatic CRM integration (HubSpot, Salesforce)
- Scheduled re-research and change detection
- Competitor analysis module
- Multi-language support for international customers
- Integration with email sequencing tools
