# OpenClaw Financial Skills Ecosystem

A comprehensive suite of financial analysis skills for the OpenClaw agent framework, adapted from the Anthropic Financial Services Plugins.

## Overview

This ecosystem provides specialized capabilities for:
- **Investment Banking** - M&A advisory, pitch materials, CIMs
- **Equity Research** - Stock analysis, earnings updates, investment theses
- **Private Equity** - LBO modeling, deal sourcing, portfolio monitoring
- **Financial Analysis** - Valuation, modeling, and analysis tools

## Quick Start

```bash
# Install dependencies
pip3 install openpyxl pandas numpy

# Generate a comps model
python3 financial-analysis-core/scripts/generate-comps.py \
  --target "Acme Corp" \
  --peers "PeerA,PeerB,PeerC" \
  --output acme_comps.xlsx

# Generate buyer list
python3 investment-banking/scripts/generate-buyer-list.py \
  --company "Target Inc" \
  --industry software \
  --output buyers.csv

# Generate DCF model
python3 financial-analysis-core/scripts/generate-dcf.py \
  --company "Acme Corp" \
  --years 5 \
  --output acme_dcf.xlsx
```

## Skill Hierarchy

```
skills/
├── financial-analysis-core/    # Foundation (REQUIRED FIRST)
│   ├── SKILL.md               # Core valuation & modeling
│   ├── scripts/
│   │   ├── generate-comps.py  # Comparable company analysis
│   │   └── generate-dcf.py    # DCF valuation models
│   └── templates/             # Excel templates
│
├── investment-banking/         # M&A Advisory
│   ├── SKILL.md               # Deal execution workflows
│   ├── scripts/
│   │   └── generate-buyer-list.py  # Strategic/PE buyers
│   └── examples/              # CIM, teaser examples
│
├── equity-research/           # Equity Analysis
│   ├── SKILL.md               # Research workflows
│   └── examples/              # Earnings update examples
│
└── private-equity/            # PE Investing
    ├── SKILL.md               # LBO & investment workflows
    └── examples/              # LBO output examples
```

## Skill Capabilities

### 1. Financial Analysis Core (Foundation)

| Capability | Tool | Output |
|------------|------|--------|
| Comparable Companies | `generate-comps.py` | Excel workbook with multiples |
| DCF Valuation | `generate-dcf.py` | 5-10 year projection model |
| Three-Statement Model | Templates | Integrated financial model |
| Precedent Transactions | Templates | Transaction comps |

**Key Features:**
- Investment banking formatting (blue/black/green color scheme)
- Sensitivity analysis tables
- Standard valuation methodologies
- Excel templates for manual modeling

### 2. Investment Banking

| Capability | Tool | Output |
|------------|------|--------|
| Buyer Universe | `generate-buyer-list.py` | Strategic + Financial buyers |
| CIM Structure | Templates | Confidential memorandum |
| Teaser Format | Templates | One-page marketing |
| Merger Model | Templates | Accretion/dilution |

**Key Features:**
- Industry-specific buyer databases
- Deal process management
- Bid summary formats
- Pitch book structures

### 3. Equity Research

| Capability | Description |
|------------|-------------|
| Earnings Updates | Post-earnings quick-take reports |
| Coverage Initiation | Full research reports |
| Investment Thesis | Bull/bear case frameworks |
| Stock Screening | Universe filtering |
| Catalyst Tracking | Event calendar |

**Key Features:**
- Rating framework (Buy/Hold/Sell)
- Price target methodologies
- Model maintenance workflows
- Morning note formats

### 4. Private Equity

| Capability | Tool | Output |
|------------|------|--------|
| LBO Modeling | Scripts/Templates | Returns analysis |
| Deal Sourcing | Templates | Pipeline tracking |
| IC Memos | Templates | Investment memos |
| Portfolio Monitoring | Templates | KPI dashboards |

**Key Features:**
- Debt schedule modeling
- Value creation planning
- Returns sensitivity
- DD checklists

## Usage Examples

### Complete M&A Sell-Side Workflow

```bash
# Step 1: Value the company
python3 financial-analysis-core/scripts/generate-comps.py \
  --target "TechFlow Inc" \
  --peers "PeerA,PeerB,PeerC,PeerD,PeerE" \
  --output techflow_comps.xlsx

python3 financial-analysis-core/scripts/generate-dcf.py \
  --company "TechFlow Inc" \
  --years 5 \
  --wacc 10 \
  --growth 2.5 \
  --output techflow_dcf.xlsx

# Step 2: Generate buyer list
python3 investment-banking/scripts/generate-buyer-list.py \
  --company "TechFlow Inc" \
  --industry software \
  --revenue 65 \
  --ebitda 15 \
  --output techflow_buyers.csv

# Step 3: Create CIM from template
cp investment-banking/templates/cim-template.docx techflow_cim.docx

# Step 4: Create teaser
cp investment-banking/templates/teaser-template.docx techflow_teaser.docx
```

### LBO Analysis Workflow

```bash
# Step 1: Generate LBO model
python3 private-equity/scripts/generate-lbo-model.py \
  --company "Industrial Solutions" \
  --entry-ev 500 \
  --equity 200 \
  --exit-year 5 \
  --output industrial_lbo.xlsx

# Step 2: Create IC memo
cp private-equity/templates/ic-memo-template.md industrial_ic_memo.md

# Step 3: Review due diligence checklist
cat private-equity/templates/dd-checklist.md
```

### Equity Research Workflow

```bash
# Step 1: Generate earnings update framework
cp equity-research/templates/earnings-update-template.md tech_q1_update.md

# Step 2: Stock screen
cp equity-research/scripts/stock-screener.py .
python3 stock-screener.py --universe sp500 --style growth

# Step 3: Track catalysts
cp equity-research/templates/catalyst-calendar.md tech_catalysts.md
```

## Integration with OpenClaw

These skills are designed for OpenClaw agents:

1. **Skill Activation** - SKILL.md provides trigger conditions
2. **Script Execution** - Python scripts generate standardized outputs
3. **Template Usage** - Consistent formatting across deliverables
4. **Example Reference** - Shows expected output formats

### Agent Workflow Integration

```
User: "Help me value TechCorp for a potential sale"

Agent (reads financial-analysis-core/SKILL.md):
1. "I'll help you value TechCorp using trading comps and DCF analysis"
2. Runs generate-comps.py with appropriate peers
3. Runs generate-dcf.py with assumptions
4. Generates valuation summary
5. Recommends next steps (buyer outreach, CIM preparation)
```

## Color Coding Standards

Following investment banking conventions:

| Color | Meaning | Usage |
|-------|---------|-------|
| **Blue** | Inputs | Hardcoded assumptions, constants |
| **Black** | Calculations | Formulas, derived values |
| **Green** | Links | References to other sheets |

## Data Sources (Future MCP Integration)

Potential MCP integrations for live data:

| Data Type | Potential Sources |
|-----------|-------------------|
| Market Data | Bloomberg, Refinitiv, FactSet |
| Financials | SEC EDGAR, CapIQ, S&P Global |
| Estimates | Visible Alpha, Bloomberg |
| M&A Data | PitchBook, Preqin, MergerMarket |
| Research | Sell-side reports, industry pubs |

## Best Practices

### Modeling Standards
1. Use consistent time periods (all LTM or all NTM)
2. Calendarize fiscal years if needed
3. Use fully diluted share counts
4. Include sensitivity analysis
5. Document all assumptions

### Process Management
1. Maintain version control on models
2. Create backup scenarios
3. Review with fresh eyes before presenting
4. Get second opinion on key assumptions

## Roadmap

### Phase 3 (Future)
- [ ] Live data integration via MCP
- [ ] Automated financial data fetching
- [ ] Precedent transaction database
- [ ] Industry-specific templates
- [ ] Automated report generation
- [ ] Visualization (charts, graphs)

### Phase 4 (Future)
- [ ] Real-time market data
- [ ] AI-powered company screening
- [ ] Automated comparable selection
- [ ] PDF report generation
- [ ] Email distribution integration

## Contributing

To add new capabilities:

1. Add script to `skills/{skill}/scripts/`
2. Add template to `skills/{skill}/templates/`
3. Document in `skills/{skill}/SKILL.md`
4. Add example to `skills/{skill}/examples/`
5. Update this README

## Resources

### Internal
- [financial-analysis-core/SKILL.md](financial-analysis-core/SKILL.md) - Core valuation
- [investment-banking/SKILL.md](investment-banking/SKILL.md) - M&A advisory
- [equity-research/SKILL.md](equity-research/SKILL.md) - Stock research
- [private-equity/SKILL.md](private-equity/SKILL.md) - PE investing

### External References
- Aswath Damodaran: pages.stern.nyu.edu/~adamodar/
- SEC EDGAR: sec.gov/edgar
- Original Inspiration: github.com/anthropics/financial-services-plugins

## Disclaimer

These tools assist with financial analysis workflows but do not provide investment advice. Always verify conclusions with qualified financial professionals. AI-generated analysis should be reviewed by financial professionals before being relied upon for financial or investment decisions.

## License

Part of the OpenClaw/WeAgents ecosystem.
