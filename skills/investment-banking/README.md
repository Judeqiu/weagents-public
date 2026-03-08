# Investment Banking Skill

M&A advisory and transaction execution workflows.

## Overview

This skill provides tools and templates for:
- Sell-side and buy-side M&A advisory
- Merger modeling and accretion/dilution analysis
- Confidential Information Memorandums (CIMs)
- Buyer universe development
- Pitch materials and process management

## Installation

No additional dependencies required beyond financial-analysis-core.

## Usage

### Generate Buyer List

```bash
python3 scripts/generate-buyer-list.py \
  --company "Target Inc" \
  --industry software \
  --revenue 100 \
  --ebitda 25 \
  --output buyers.csv
```

### Create Merger Model

```bash
python3 scripts/generate-merger-model.py \
  --buyer "Acquirer Corp" \
  --target "Target Inc" \
  --price 500 \
  --mix "50/50" \
  --synergies 35 \
  --output merger-model.xlsx
```

## File Structure

```
investment-banking/
├── SKILL.md                    # Main documentation
├── README.md                   # This file
├── scripts/
│   ├── generate-buyer-list.py     # Strategic/PE buyer generator
│   ├── generate-merger-model.py   # Accretion/dilution model
│   └── generate-cim-outline.py    # CIM structure generator
├── templates/
│   ├── cim-template.docx          # CIM template
│   ├── teaser-template.docx       # Teaser template
│   ├── pitch-book.pptx            # Pitch deck template
│   └── merger-model.xlsx          # Merger model template
└── examples/
    ├── sample-cim-outline.md      # CIM outline example
    ├── sample-teaser.md           # Teaser example
    └── sample-bid-summary.md      # Bid summary example
```

## Key Concepts

### Sell-Side Process Timeline

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| Preparation | 4-6 weeks | Valuation, CIM, data room |
| Marketing | 6-8 weeks | Teasers, NDAs, management meetings |
| Execution | 8-12 weeks | Due diligence, definitive agreement |

### Buyer Types

| Type | Focus | Typical Premium |
|------|-------|-----------------|
| Strategic | Synergies | 20-40% |
| Financial | Returns | 10-25% |

### Merger Model Key Outputs

- EPS accretion/(dilution)
- Break-even synergies
- IRR on investment
- Pro forma financials

## Best Practices

1. **Maintain competitive tension** - Minimum 3 serious bidders
2. **Phase information disclosure** - Protect sensitive data
3. **Document everything** - Audit trail for fairness opinion
4. **Manage timeline** - Keep momentum, avoid process fatigue

## Disclaimer

For advisory workflow support only. Not investment advice.
