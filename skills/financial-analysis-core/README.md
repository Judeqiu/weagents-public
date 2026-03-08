# Financial Analysis Core Skill

Core financial analysis capabilities for valuation and modeling tasks in the OpenClaw ecosystem.

## Overview

This skill provides standardized tools and templates for:
- **Comparable Company Analysis (Comps)** - Trading multiples valuation
- **DCF Valuation** - Discounted cash flow modeling
- **Three-Statement Modeling** - Integrated financial projections
- **Precedent Transaction Analysis** - M&A deal comps

## Installation

### Prerequisites

- Python 3.8+
- pip

### Install Dependencies

```bash
pip3 install -r requirements.txt
```

Or install directly:

```bash
pip3 install openpyxl pandas numpy
```

## Usage

### Generate a Comps Model

```bash
python3 scripts/generate-comps.py \
  --target "Acme Corp" \
  --peers "PeerA,PeerB,PeerC,PeerD,PeerE" \
  --output acme_comps.xlsx
```

Or with a peers file:

```bash
python3 scripts/generate-comps.py \
  --target "Acme Corp" \
  --peers-file peers.csv \
  --output acme_comps.xlsx
```

### Generate a DCF Model

```bash
python3 scripts/generate-dcf.py \
  --company "Acme Corp" \
  --years 5 \
  --wacc 9.5 \
  --growth 2.5 \
  --output acme_dcf.xlsx
```

### Use Excel Templates

Copy templates for manual completion:

```bash
cp templates/comps-template.xlsx my-analysis.xlsx
cp templates/dcf-template.xlsx my-dcf.xlsx
cp templates/3-statement-template.xlsx my-model.xlsx
```

## File Structure

```
financial-analysis-core/
├── SKILL.md              # Main skill documentation
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── scripts/
│   ├── generate-comps.py    # Comps model generator
│   └── generate-dcf.py      # DCF model generator
├── templates/
│   ├── comps-template.xlsx       # Comps Excel template
│   ├── dcf-template.xlsx         # DCF Excel template
│   └── 3-statement-template.xlsx # 3-statement model template
└── examples/
    ├── sample-comps-report.md    # Sample comps output
    └── sample-dcf-output.md      # Sample DCF output
```

## Excel Standards

### Color Coding

Following investment banking conventions:

| Color | Meaning | Usage |
|-------|---------|-------|
| **Blue** | Inputs | Hardcoded constants, assumptions |
| **Black** | Calculations | Formulas, derived values |
| **Green** | Links | References to other sheets |

### Formatting

- **Currency:** $#,##0.0,,"M" (millions)
- **Multiples:** 0.0"x"
- **Percentages:** 0.0%
- **Decimals:** One decimal place standard

## Key Concepts

### Enterprise Value vs Equity Value

```
Enterprise Value = Market Cap + Debt - Cash + Minority Interest
Equity Value = Enterprise Value - Debt + Cash - Minority Interest
```

### Common Multiples

**Enterprise Value Multiples:**
- EV/Revenue - Best for growth companies, pre-profit
- EV/EBITDA - Most common for mature companies
- EV/EBIT - Better for capital-intensive businesses

**Equity Value Multiples:**
- P/E - Most common for profitable companies
- P/B - Best for financial institutions
- Dividend Yield - For income-focused valuation

### WACC Components

```
WACC = (E/V) × Re + (D/V) × Rd × (1 - Tc)

Cost of Equity (CAPM):
Re = Rf + β × (Market Risk Premium)
```

### Free Cash Flow

```
UFCF = EBIT(1 - Tax Rate) + D&A - Capex - ΔNWC
```

## Best Practices

1. **Always calendarize** if fiscal years differ from calendar year
2. **Use fully diluted shares** for market cap calculations
3. **Adjust for non-recurring items** in EBITDA
4. **Include sensitivity analysis** on key assumptions
5. **Document all assumptions** in the model

## Examples

See the `examples/` directory for:
- Sample comps report format
- Sample DCF output structure
- Valuation summary templates

## Integration with OpenClaw

This skill is designed to work with the OpenClaw agent framework:

1. **Skill activation:** The SKILL.md provides context for when to use these tools
2. **Script execution:** Python scripts generate standardized Excel models
3. **Template usage:** Templates ensure consistent formatting
4. **Example reference:** Examples show expected output format

## Extending the Skill

To add new capabilities:

1. Add new scripts to `scripts/`
2. Add templates to `templates/`
3. Document in SKILL.md
4. Add examples to `examples/`

## Disclaimer

These tools assist with financial analysis workflows but do not provide investment advice. Always verify conclusions with qualified financial professionals. AI-generated analysis should be reviewed by financial professionals before being relied upon for financial or investment decisions.

## License

Part of the OpenClaw/WeAgents ecosystem.
