---
name: equity-research
description: "Equity research workflows including earnings updates, initiating coverage reports, investment thesis development, and stock screening. Use for buy-side and sell-side equity analysis, portfolio management, and investment recommendations."
metadata:
  category: "equity-research"
  domains: ["sell-side-research", "buy-side-research", "portfolio-management", "stock-analysis"]
  outputs: ["research-reports", "earnings-updates", "investment-theses", "stock-screens", "price-targets"]
  requires:
    bins: ["python3"]
    skills: ["financial-analysis-core"]
---

# Equity Research

Equity analysis and research workflows for buy-side and sell-side.

## When to Use

✅ **Use this skill for:**

- **Earnings Analysis**: Post-earnings updates, guidance changes
- **Coverage Initiation**: New stock coverage launch
- **Investment Thesis**: Bull/bear case development
- **Stock Screening**: Finding investment opportunities
- **Valuation Updates**: Price target changes
- **Catalyst Tracking**: Events that could move the stock

❌ **Don't use for:**

- M&A transactions (use investment-banking skill)
- Private company analysis (use private-equity skill)
- Macro research (not covered)

## Quick Reference

| Task | Tool/Template | Output |
|------|---------------|--------|
| Earnings reaction | Earnings update template | Quick-take report |
| New coverage | Initiating coverage template | Full research report |
| Investment view | Thesis template | Bull/bear case |
| Find ideas | Stock screener script | Universe of candidates |
| Track events | Catalyst calendar | Event timeline |

## Core Workflows

### 1. Earnings Update Report

**Purpose**: Quick analysis of quarterly earnings results.

#### Standard Structure:

```
EARNINGS UPDATE: [Company] - [Ticker]
Date: [Date] | Rating: [Rating] | Price Target: $XX

QUICK TAKE
[1-2 sentence summary of key takeaway]

KEY METRICS vs. ESTIMATES
| Metric | Actual | Estimate | Beat/Miss |
|--------|--------|----------|-----------|
| Revenue | $XXM | $XXM | +X% |
| EPS | $X.XX | $X.XX | +$0.XX |
| EBITDA | $XXM | $XXM | +X% |

HIGHLIGHTS
✓ Positive: [Key positive]
✓ Positive: [Key positive]
⚠ Concern: [Key concern]

GUIDANCE
- Revenue: $XXXM - $XXXM (prior: $XXXM)
- EPS: $X.XX - $X.XX (prior: $X.XX)

VALUATION UPDATE
- Prior PT: $XX → New PT: $XX
- Rationale: [Why changed]

KEY QUOTES FROM CALL
"[Management quote]" - [Executive], [Title]

MODEL UPDATES
| Year | Old EPS | New EPS | Change |
|------|---------|---------|--------|
| 2026 | $X.XX | $X.XX | +X% |
| 2027 | $X.XX | $X.XX | +X% |

RATING/RISK
Rating: [Buy/Hold/Sell]
Key Risks: [Risk 1], [Risk 2]
```

#### Time Allocation:

| Phase | Time | Activity |
|-------|------|----------|
| 1 | 0-15 min | Read release, compare to estimates |
| 2 | 15-30 min | Listen to earnings call |
| 3 | 30-60 min | Update model, write report |
| 4 | 60-90 min | Review, publish, communicate |

### 2. Initiating Coverage Report

**Purpose**: Comprehensive analysis launching coverage of a new stock.

#### Standard Sections:

1. **Investment Summary**
   ```
   COMPANY: [Name] ([Ticker])
   RATING: [Buy/Hold/Sell]
   PRICE TARGET: $XX.XX
   CURRENT PRICE: $XX.XX
   UPSIDE/DOWNSIDE: +XX%
   
   INVESTMENT THESIS
   [2-3 paragraph investment case]
   
   KEY METRICS
   | Metric | Value |
   |--------|-------|
   | Market Cap | $XXB |
   | Enterprise Value | $XXB |
   | Revenue (LTM) | $XXM |
   | Revenue Growth | XX% |
   | EBITDA Margin | XX% |
   | P/E (NTM) | XX.x |
   | EV/EBITDA (NTM) | XX.x |
   ```

2. **Business Overview**
   - What the company does
   - Revenue breakdown by product/segment
   - Geographic exposure
   - Key customers/partners

3. **Industry Analysis**
   - Market size and growth
   - Competitive landscape
   - Industry trends
   - Porter's Five Forces

4. **Competitive Positioning**
   ```
   Competitive Matrix:
   | Company | Market Share | Growth | Margins | Moat |
   |---------|--------------|--------|---------|------|
   | [Target]| XX% | XX% | XX% | Strong |
   | Peer A  | XX% | XX% | XX% | Medium |
   | Peer B  | XX% | XX% | XX% | Weak |
   ```

5. **Financial Analysis**
   - Historical trends (3-5 years)
   - Key performance indicators
   - Margin analysis
   - Capital allocation
   - Balance sheet strength

6. **Valuation**
   ```
   VALUATION SUMMARY
   
   Methodology        | Multiple | Implied Value | Weight |
   -------------------|----------|---------------|--------|
   Trading Comps      | XX.x     | $XX           | 30%    |
   Precedent M&A      | XX.x     | $XX           | 20%    |
   DCF                | XX% WACC | $XX           | 35%    |
   LBO                | XX% IRR  | $XX           | 15%    |
   -------------------|----------|---------------|--------|
   BLENDED PT         |          | $XX           | 100%   |
   ```

7. **Bull/Bear Case**
   ```
   BULL CASE ($XX - XX% upside)
   Assumptions:
   - [Key assumption 1]
   - [Key assumption 2]
   Implied Multiple: XX.x EV/EBITDA
   
   BEAR CASE ($XX - XX% downside)
   Assumptions:
   - [Key assumption 1]
   - [Key assumption 2]
   Implied Multiple: XX.x EV/EBITDA
   ```

8. **Risk Factors**
   - Company-specific risks
   - Industry risks
   - Macro risks
   - ESG considerations

9. **Catalyst Calendar**
   | Date | Event | Impact |
   |------|-------|--------|
   | Q1 | Earnings | High |
   | May | Investor Day | Medium |
   | Q2 | Product Launch | High |

### 3. Investment Thesis Development

**Purpose**: Structured framework for investment decisions.

#### Thesis Framework:

```
INVESTMENT THESIS: [Company]

THESIS STATEMENT (1 sentence)
[Company] is a [bull/bear] case because [core argument].

THEME ALIGNMENT
□ Secular growth trend
□ Cyclical recovery
□ Market share gains
□ Margin expansion
□ Capital return
□ Special situation

KEY ASSUMPTIONS
1. [Assumption 1] - Confidence: High/Med/Low
2. [Assumption 2] - Confidence: High/Med/Low
3. [Assumption 3] - Confidence: High/Med/Low

WHAT NEEDS TO GO RIGHT
1. [Positive factor 1]
2. [Positive factor 2]

WHAT COULD GO WRONG
1. [Risk 1]
2. [Risk 2]

MARGIN OF SAFETY
Current valuation vs. intrinsic value: XX%
Downside case: -XX%
Upside case: +XX%
Risk/Reward: X:1

CONVICTION LEVEL
[High/Medium/Low] - [Explanation]
```

#### Thesis Monitoring:

```
THESIS TRACKER: [Company]

Original Thesis Date: [Date]
Last Review: [Date]
Status: [On Track/At Risk/Broken]

THESIS CHECKPOINTS
| Checkpoint | Original | Current | Status |
|------------|----------|---------|--------|
| Revenue growth | XX% | XX% | ✓ On track |
| Margin expansion | XXbps | XXbps | ⚠ Behind |
| Market share | XX% | XX% | ✓ On track |

REVIEWS
[Date]: [What happened, thesis update]
[Date]: [What happened, thesis update]

EXIT CRITERIA
- Sell if: [Trigger 1]
- Sell if: [Trigger 2]
```

### 4. Stock Screening

**Purpose**: Identify investment opportunities from a universe.

#### Screening Criteria by Style:

**Growth Screen:**
```
CRITERIA:
- Revenue growth > 20%
- EBITDA margins > 15%
- Market cap $500M - $10B
- PEG ratio < 2.0
- ROIC > 15%
```

**Value Screen:**
```
CRITERIA:
- P/E < 15x
- P/B < 2.0x
- EV/EBITDA < 10x
- Dividend yield > 2%
- Debt/EBITDA < 3.0x
```

**Quality Screen:**
```
CRITERIA:
- ROE > 15% (5-year avg)
- Gross margins > 40%
- FCF conversion > 80%
- Debt/EBITDA < 2.0x
- Revenue CAGR > 10%
```

#### Output Format:

```
STOCK SCREEN RESULTS
Screen: [Screen Name] | Date: [Date] | Universe: [Index/Sector]

RESULTS: XX companies

TOP 10:
| Rank | Ticker | Company | Sector | Metric 1 | Metric 2 | Metric 3 |
|------|--------|---------|--------|----------|----------|----------|
| 1 | XXX | [Name] | [Sector] | XX.x | XX.x | XX.x |
| 2 | XXX | [Name] | [Sector] | XX.x | XX.x | XX.x |

NEW ADDITIONS (vs. last screen):
- [Ticker]: [Reason added]

DROPPED (vs. last screen):
- [Ticker]: [Reason dropped]

WATCHLIST WORTHY:
- [Ticker]: [Brief rationale]
```

### 5. Catalyst Tracking

**Purpose**: Monitor events that could impact stock price.

#### Catalyst Calendar:

```
CATALYST CALENDAR: [Company] ([Ticker])

UPCOMING CATALYSTS (Next 90 Days)
| Date | Catalyst | Impact | Direction | Bull/Bear |
|------|----------|--------|-----------|-----------|
| 4/25 | Q1 Earnings | High | ? | Beat: +10% Miss: -15% |
| 5/15 | Analyst Day | Med | ? | New targets: +5% |
| 6/10 | FDA Decision | High | ? | Approve: +30% Deny: -40% |

RECENT CATALYSTS (Last 90 Days)
| Date | Catalyst | Actual | Impact | Stock Reaction |
|------|----------|--------|--------|----------------|
| 2/15 | Q4 Earnings | Beat | +8% | +12% |
| 3/1 | Guidance | Raised | +5% | +3% |

CATALYST SCORECARD
- Positive catalysts realized: X
- Negative catalysts realized: X
- Thesis on track: Yes/No
```

#### Catalyst Types:

| Type | Examples | Typical Impact |
|------|----------|----------------|
| **Earnings** | Quarterly results, guidance | High |
| **Product** | Launches, approvals, recalls | High |
| **Corporate** | M&A, spin-offs, buybacks | High |
| **Regulatory** | FDA, antitrust, policy | High |
| **Industry** | Competitor actions, pricing | Medium |
| **Management** | Changes, guidance, strategy | Medium |
| **Macro** | Rates, FX, commodities | Variable |

## Implementation

### Generate Earnings Update

```bash
python3 skills/equity-research/scripts/generate-earnings-update.py \
  --company "TechCorp" \
  --ticker "TECH" \
  --quarter "Q1-2026" \
  --output earnings-update.md
```

### Stock Screen

```bash
python3 skills/equity-research/scripts/stock-screener.py \
  --universe "sp500" \
  --style "growth" \
  --output screen-results.csv
```

### Create Coverage Initiation

```bash
cp skills/equity-research/templates/initiating-coverage-template.docx \
   my-coverage-report.docx
```

### Update Catalyst Calendar

```bash
python3 skills/equity-research/scripts/update-catalysts.py \
  --ticker "TECH" \
  --add "2026-05-15:Product Launch:High" \
  --output catalyst-calendar.md
```

## Best Practices

### Research Process

1. **Pre-Earnings Prep**
   - Review model vs. consensus
   - Identify key metrics to watch
   - Prepare questions for call

2. **Model Maintenance**
   - Update quarterly
   - Revisit assumptions annually
   - Track vs. actuals

3. **Idea Generation**
   - Screen regularly
   - Read voraciously
   - Talk to industry contacts

### Writing Guidelines

1. **Be Concise**
   - 1-page for earnings updates
   - 20-30 pages for initiations
   - Lead with conclusion

2. **Differentiate**
   - What's your unique insight?
   - Why will the stock move?
   - What's priced in?

3. **Be Honest**
   - Acknowledge uncertainty
   - Admit when wrong
   - Update views with new info

### Rating Framework

| Rating | Definition | Expected Return |
|--------|------------|-----------------|
| **Buy** | Expect >15% upside | Outperform |
| **Hold** | Expect ±15% | Market perform |
| **Sell** | Expect >15% downside | Underperform |

### Price Target Methodology

```
Price Target = Forward Metric × Appropriate Multiple

Factors affecting multiple:
- Growth rate (higher = higher multiple)
- Quality of earnings (higher = higher multiple)
- Balance sheet (stronger = higher multiple)
- Market conditions (bull = higher multiples)
- Competitive position (stronger = higher multiple)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Anchoring to price paid | Value based on fundamentals |
| Confirmation bias | Seek disconfirming evidence |
| Overconfidence | Use probability-weighted scenarios |
| Ignoring macro | Consider cycle position |
| Short-term focus | Invest with 2-3 year horizon |

## Output Formatting

### Morning Note Format

```
MORNING NOTE - [Date]

MARKET CONTEXT
- S&P 500: X,XXX (+/-X%)
- 10Y Treasury: X.XX%
- VIX: XX
- Key events: [List]

PORTFOLIO MOVERS
| Stock | Move | Driver |
|-------|------|--------|
| XXX | +X% | [Reason] |
| XXX | -X% | [Reason] |

TODAY'S CALENDAR
| Time | Event | Watch |
|------|-------|-------|
| 8:30 | Jobs Report | Wages, participation |
| 10:00 | ISM Services | Employment sub-index |

STOCK SPECIFIC
[Stock]: [News] - [Implication]
[Stock]: [News] - [Implication]

LOOKING AHEAD
- Tomorrow: [Event]
- This week: [Events]
```

## Resources

### Templates

- `templates/earnings-update-template.md` - Earnings update
- `templates/initiating-coverage-template.docx` - Full research report
- `templates/thesis-tracker.md` - Investment thesis monitoring
- `templates/catalyst-calendar.md` - Event tracking
- `templates/morning-note.md` - Daily market summary

### Examples

- `examples/sample-earnings-update.md` - Earnings report example
- `examples/sample-initiation.md` - Initiation example
- `examples/sample-thesis.md` - Thesis framework example

### External Resources

- Estimates: Bloomberg, FactSet, Visible Alpha
- Research: Sell-side reports, industry publications
- Data: Capital IQ, Refinitiv, SEC EDGAR

---

**Disclaimer**: Research tools for analysis workflows only. Not investment advice. Always do your own due diligence.
