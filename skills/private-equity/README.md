# Private Equity Skill

Private equity investing and portfolio management workflows.

## Overview

This skill provides tools and templates for:
- LBO (Leveraged Buyout) modeling
- Deal sourcing and screening
- Investment Committee memos
- Due diligence checklists
- Portfolio monitoring

## Installation

No additional dependencies required beyond financial-analysis-core.

## Usage

### Generate LBO Model

```bash
python3 scripts/generate-lbo-model.py \
  --company "TargetCo" \
  --entry-ev 500 \
  --equity 200 \
  --exit-year 5 \
  --output lbo-model.xlsx
```

### Create IC Memo

```bash
python3 scripts/generate-ic-memo.py \
  --company "TargetCo" \
  --investment 50 \
  --irr 25 \
  --output ic-memo.md
```

### Track Deal Pipeline

```bash
python3 scripts/update-pipeline.py \
  --add "Company XYZ,Software,$30M revenue,Active DD" \
  --output pipeline.csv
```

## File Structure

```
private-equity/
├── SKILL.md                    # Main documentation
├── README.md                   # This file
├── scripts/
│   ├── generate-lbo-model.py      # LBO model generator
│   ├── generate-ic-memo.py        # IC memo generator
│   ├── update-pipeline.py         # Deal pipeline tracker
│   └── generate-portfolio-dashboard.py  # Portfolio monitoring
├── templates/
│   ├── lbo-template.xlsx          # LBO model template
│   ├── ic-memo-template.md        # Investment memo template
│   ├── dd-checklist.md            # Due diligence checklist
│   └── portfolio-update.md        # Monthly reporting template
└── examples/
    └── sample-lbo-output.md       # LBO summary example
```

## Key Concepts

### LBO Returns Hurdles

| Metric | Minimum Target |
|--------|----------------|
| MoM | 2.0x |
| IRR | 20% |
| Hold Period | 4-6 years |

### Capital Structure

| Component | Typical Range |
|-----------|---------------|
| Equity | 30-50% |
| Senior Debt | 40-60% |
| Subordinated | 10-20% |

### Value Creation Levers

1. **Revenue growth** - Organic expansion, M&A
2. **Margin expansion** - Cost reduction, pricing
3. **Multiple expansion** - De-risking, growth acceleration
4. **Deleveraging** - Debt paydown from FCF

## Best Practices

1. **Conservative assumptions** - Base case, not best case
2. **Multiple exit options** - Strategic, IPO, secondary
3. **Active ownership** - Monthly KPIs, quarterly boards
4. **Early warning signs** - Misses to plan, management turnover

## Disclaimer

PE tools for analysis workflows. Not investment advice. Actual returns will vary.
