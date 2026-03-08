# Equity Research Skill

Equity analysis and research report workflows.

## Overview

This skill provides tools and templates for:
- Earnings updates and analysis
- Initiating coverage reports
- Investment thesis development
- Stock screening and idea generation
- Catalyst tracking

## Installation

No additional dependencies required beyond financial-analysis-core.

## Usage

### Generate Earnings Update

```bash
python3 scripts/generate-earnings-update.py \
  --company "TechCorp" \
  --ticker "TECH" \
  --quarter "Q1-2026" \
  --output earnings-update.md
```

### Stock Screen

```bash
python3 scripts/stock-screener.py \
  --universe "sp500" \
  --style "growth" \
  --min-market-cap 1000 \
  --output screen-results.csv
```

### Update Catalyst Calendar

```bash
python3 scripts/update-catalysts.py \
  --ticker "TECH" \
  --add "2026-05-15:Product Launch:High" \
  --output catalyst-calendar.md
```

## File Structure

```
equity-research/
├── SKILL.md                    # Main documentation
├── README.md                   # This file
├── scripts/
│   ├── generate-earnings-update.py  # Earnings report generator
│   ├── stock-screener.py            # Stock screening tool
│   └── update-catalysts.py          # Catalyst tracker
├── templates/
│   ├── earnings-update-template.md  # Earnings update template
│   ├── initiating-coverage-template.docx  # Full research report
│   ├── thesis-tracker.md            # Investment thesis monitoring
│   └── catalyst-calendar.md         # Event tracking
└── examples/
    └── sample-earnings-update.md    # Example earnings report
```

## Key Concepts

### Rating Framework

| Rating | Upside/Downside | Action |
|--------|-----------------|--------|
| Buy | >15% | Outperform |
| Hold | ±15% | Market perform |
| Sell | <-15% | Underperform |

### Price Target Components

```
PT = Forward Metric × Appropriate Multiple

Factors:
- Growth rate
- Quality of earnings
- Balance sheet strength
- Market conditions
```

### Earnings Update Timing

| Phase | Duration | Activity |
|-------|----------|----------|
| 0-15 min | Read release | Compare to estimates |
| 15-30 min | Earnings call | Listen to management |
| 30-60 min | Update model | Write report |
| 60-90 min | Review | Publish, communicate |

## Best Practices

1. **Lead with conclusion** - Don't bury the thesis
2. **Differentiate** - What's your unique insight?
3. **Be honest** - Acknowledge uncertainty
4. **Track vs. actuals** - Learn from mistakes

## Disclaimer

Research tools for analysis only. Not investment advice.
