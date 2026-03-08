# Financial Skills Quick Reference Card

## Installation
```bash
pip3 install openpyxl pandas numpy
```

## Core Commands

### Valuation
```bash
# Comparable Company Analysis
python3 skills/financial-analysis-core/scripts/generate-comps.py \
  --target "Company Name" \
  --peers "Peer1,Peer2,Peer3" \
  --output comps.xlsx

# DCF Valuation
python3 skills/financial-analysis-core/scripts/generate-dcf.py \
  --company "Company Name" \
  --years 5 \
  --wacc 9.5 \
  --growth 2.5 \
  --output dcf.xlsx
```

### Investment Banking
```bash
# Generate Buyer List
python3 skills/investment-banking/scripts/generate-buyer-list.py \
  --company "Target Inc" \
  --industry software \
  --revenue 100 \
  --ebitda 25 \
  --output buyers.csv
```

### Templates
```bash
# Copy templates for manual editing
cp skills/financial-analysis-core/templates/*.xlsx .
cp skills/investment-banking/templates/*.docx .
cp skills/private-equity/templates/*.md .
```

## File Locations

| Skill | Path |
|-------|------|
| Core | `skills/financial-analysis-core/` |
| IB | `skills/investment-banking/` |
| Research | `skills/equity-research/` |
| PE | `skills/private-equity/` |

## Key Documentation

| Document | Location |
|----------|----------|
| Tutorial | `skills/TUTORIAL.md` |
| Ecosystem Guide | `skills/README.md` |
| Valuation Guide | `skills/financial-analysis-core/SKILL.md` |
| M&A Guide | `skills/investment-banking/SKILL.md` |
| Research Guide | `skills/equity-research/SKILL.md` |
| PE Guide | `skills/private-equity/SKILL.md` |

## Excel Color Coding

| Color | Meaning | Usage |
|-------|---------|-------|
| Blue | Inputs | Hardcoded values, assumptions |
| Black | Calculations | Formulas, derived values |
| Green | Links | References to other sheets |

## Common Multiples

### Enterprise Value
- EV/Revenue - Growth companies
- EV/EBITDA - Most industries
- EV/EBIT - Capital intensive

### Equity Value
- P/E - Profitable companies
- P/B - Financials
- Dividend Yield - Income stocks

## LBO Returns Hurdles

| Metric | Target |
|--------|--------|
| MoM | 2.0x+ |
| IRR | 20%+ |
| Hold Period | 4-6 years |

## Research Ratings

| Rating | Upside | Action |
|--------|--------|--------|
| Buy | >15% | Outperform |
| Hold | ±15% | Market perform |
| Sell | <-15% | Underperform |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| openpyxl not found | `pip3 install openpyxl` |
| Permission denied | `chmod +x skills/*/scripts/*.py` |
| Need help | `python3 script.py --help` |

## Workflow Checklist

### Valuation
- [ ] Run comps generator
- [ ] Fill in peer data
- [ ] Run DCF generator
- [ ] Build projections
- [ ] Sensitivity analysis
- [ ] Synthesize results

### M&A Sell-Side
- [ ] Generate buyer list
- [ ] Create teaser
- [ ] Prepare CIM
- [ ] Manage process timeline
- [ ] Collect bids
- [ ] Negotiate LOI

### Equity Research
- [ ] Monitor earnings calendar
- [ ] Write earnings update
- [ ] Maintain model
- [ ] Track catalysts
- [ ] Update price target

### PE Investment
- [ ] Screen opportunities
- [ ] Build LBO model
- [ ] Conduct due diligence
- [ ] Write IC memo
- [ ] Monitor portfolio
