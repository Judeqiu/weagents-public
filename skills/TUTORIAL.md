# Financial Skills Tutorial

A hands-on guide to using the OpenClaw Financial Skills Ecosystem.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Tutorial 1: Valuation Analysis](#tutorial-1-valuation-analysis)
3. [Tutorial 2: M&A Sell-Side Process](#tutorial-2-ma-sell-side-process)
4. [Tutorial 3: Equity Research Report](#tutorial-3-equity-research-report)
5. [Tutorial 4: LBO Analysis](#tutorial-4-lbo-analysis)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Step 1: Install Dependencies

```bash
# Navigate to your OpenClaw directory
cd /Users/zhengqingqiu/projects/weagents

# Install Python dependencies
pip3 install openpyxl pandas numpy

# Verify installation
python3 --version
pip3 show openpyxl
```

### Step 2: Test the Skills

```bash
# Test comps generator
python3 skills/financial-analysis-core/scripts/generate-comps.py --help

# Test DCF generator
python3 skills/financial-analysis-core/scripts/generate-dcf.py --help

# Test buyer list generator
python3 skills/investment-banking/scripts/generate-buyer-list.py --help
```

### Step 3: Understand the Skill Structure

Each skill follows this pattern:

```
skills/{skill-name}/
├── SKILL.md              # When to use, how to use
├── README.md             # Quick reference
├── scripts/              # Executable tools
│   └── *.py
├── templates/            # Starting points
│   └── *.xlsx, *.md
└── examples/             # Completed examples
    └── *.md
```

---

## Tutorial 1: Valuation Analysis

**Scenario:** You're advising TechFlow Inc., a $65M revenue software company, on valuation for a potential sale.

### Part 1A: Comparable Company Analysis

```bash
# Generate the comps model
python3 skills/financial-analysis-core/scripts/generate-comps.py \
  --target "TechFlow Inc" \
  --peers "CloudSys Inc,DataPro Ltd,SoftCore Corp,AppMatrix,CloudNine Tech" \
  --output techflow_comps.xlsx
```

**Expected Output:**
```
Generating Comps Analysis for: TechFlow Inc
Peers (5): CloudSys Inc, DataPro Ltd, SoftCore Corp, AppMatrix, CloudNine Tech
Output: techflow_comps.xlsx
✓ Generated: techflow_comps.xlsx

Next steps:
1. Open the Excel file
2. Fill in company data (blue cells)
3. Add formulas in calculation cells
4. Review implied valuation ranges
```

**What to do with the Excel file:**

1. **Open the file** - You'll see sections for:
   - Company data inputs (share price, shares outstanding, etc.)
   - Valuation multiples (EV/Revenue, EV/EBITDA, P/E)
   - Implied valuation for your target
   - Notes & methodology

2. **Fill in blue cells** (hardcoded inputs):
   ```
   For each peer company:
   - Share Price: Current stock price
   - Shares Outstanding: Fully diluted shares
   - Market Cap: Share price × Shares
   - Total Debt: From balance sheet
   - Cash: From balance sheet
   - Enterprise Value: Market Cap + Debt - Cash
   - LTM EBITDA: Last 12 months EBITDA
   ```

3. **Calculate multiples** (black cells with formulas):
   ```excel
   EV/Revenue = Enterprise Value / LTM Revenue
   EV/EBITDA = Enterprise Value / LTM EBITDA
   P/E = Market Cap / Net Income
   ```

4. **Calculate statistics**:
   ```excel
   MEDIAN: =MEDIAN(range)
   MEAN: =AVERAGE(range)
   HIGH: =MAX(range)
   LOW: =MIN(range)
   ```

5. **Derive implied valuation** for TechFlow:
   ```excel
   Implied EV = TechFlow EBITDA × Peer Median Multiple
   ```

### Part 1B: DCF Valuation

```bash
# Generate the DCF model
python3 skills/financial-analysis-core/scripts/generate-dcf.py \
  --company "TechFlow Inc" \
  --years 5 \
  --wacc 10.0 \
  --growth 2.5 \
  --output techflow_dcf.xlsx
```

**What to do with the DCF model:**

1. **Fill in assumptions** (blue cells):
   ```
   WACC Components:
   - Risk-free Rate: 4.0% (10-year Treasury)
   - Market Risk Premium: 5.5%
   - Beta: 1.15 (from comparable companies)
   - Cost of Debt: 6.0%
   - Tax Rate: 21%
   ```

2. **Input historical data** (LTM column):
   ```
   - Revenue: $65M
   - EBITDA: $15M
   - EBIT: $12M
   - Net Income: $10M
   ```

3. **Build projections** (Years 1-5):
   ```excel
   Revenue Year 1 = LTM Revenue × (1 + Growth Rate)
   Example: =65 * 1.15 = $74.75M (15% growth)
   ```

4. **Calculate Free Cash Flow**:
   ```excel
   UFCF = EBIT(1 - Tax Rate) + D&A - Capex - ΔNWC
   ```

5. **Calculate Terminal Value**:
   ```excel
   Perpetuity Growth Method:
   TV = UFCF_Year5 × (1 + g) / (WACC - g)
   ```

6. **Discount to present value**:
   ```excel
   PV = FCF / (1 + WACC)^Year
   ```

### Part 1C: Synthesis

Create a valuation summary:

```markdown
# TechFlow Inc. Valuation Summary

## Valuation Methods

| Method | Implied Enterprise Value | Weight |
|--------|-------------------------|--------|
| Trading Comps (EV/Revenue) | $520M | 25% |
| Trading Comps (EV/EBITDA) | $495M | 25% |
| DCF | $485M | 35% |
| Precedent Transactions | $510M | 15% |
| **Blended** | **$500M** | 100% |

## Implied Share Price

| Component | Value |
|-----------|-------|
| Enterprise Value | $500M |
| (+) Cash | $25M |
| (-) Debt | $45M |
| **= Equity Value** | **$480M** |
| Shares Outstanding | 12M |
| **Implied Share Price** | **$40.00** |
```

---

## Tutorial 2: M&A Sell-Side Process

**Scenario:** You're the investment banker representing TechFlow Inc. in a sale process.

### Step 1: Generate Buyer List

```bash
python3 skills/investment-banking/scripts/generate-buyer-list.py \
  --company "TechFlow Inc" \
  --industry software \
  --revenue 65 \
  --ebitda 15 \
  --output techflow_buyers.csv
```

**Review the output:**
```
BUYER LIST FOR: TechFlow Inc
Industry: Software | Revenue: $65M | EBITDA: $15M
============================================================

Tier 1 - High Priority (8 buyers)
------------------------------------------------------------

Microsoft (MSFT)
  Type: Strategic
  Market Cap: $3000B
  Fit: High
  Rationale: Cloud platform expansion

Salesforce (CRM)
  Type: Strategic
  Market Cap: $250B
  Fit: High
  Rationale: SaaS consolidation

Thoma Bravo
  Type: Mid-market PE
  AUM: $130B
  Fit: High
  Sweet Spot: $200-1000M
  Rationale: Software specialist

[... additional buyers ...]

Total Buyers Identified: 32
✓ Buyer list saved to: techflow_buyers.csv
```

### Step 2: Review Buyer CSV

```bash
cat techflow_buyers.csv | head -20
```

Output format:
```csv
tier,name,ticker,type,market_cap_aum,fit,rationale,priority
Tier 1 - High Priority,Microsoft,MSFT,Strategic,3000,High,Cloud platform expansion,High
Tier 1 - High Priority,Salesforce,CRM,Strategic,250,High,SaaS consolidation,High
```

### Step 3: Prepare Marketing Materials

```bash
# Copy templates
cp skills/investment-banking/templates/teaser-template.docx techflow_teaser.docx
cp skills/investment-banking/templates/cim-template.docx techflow_cim.docx

# Review the SKILL.md for structure
cat skills/investment-banking/SKILL.md | grep -A 50 "Teaser Format"
```

### Step 4: Create Teaser Content

Based on the SKILL.md structure, draft a teaser:

```markdown
# INVESTMENT OPPORTUNITY
Enterprise Software Company - $65M Revenue

## OVERVIEW
- Leading provider of AI-powered workflow automation
- 8 years of operating history, profitable since Year 3
- 35% market share in mid-market segment
- Strong, diversified customer base (200+ customers)

## FINANCIAL HIGHLIGHTS
Revenue:     $65M (28% 3-year CAGR)
EBITDA:      $15M (23% margin)
EBITDA CAGR: 35%
Free Cash Flow: $12M
Net Retention: 125%

## INVESTMENT HIGHLIGHTS
✓ Rapidly growing AI/ML platform with differentiated technology
✓ Strong unit economics: 80% gross margins, 120% net retention
✓ Diversified customer base across Fortune 1000 and mid-market
✓ Proven management team with successful exit history
✓ Significant whitespace in adjacent markets

## MARKET OPPORTUNITY
$50B addressable market growing at 20% annually

## TRANSACTION
Seeking strategic alternatives including:
- Sale to strategic buyer
- Sale to financial sponsor
- Minority growth investment

## CONTACT
[Investment Bank Name]
[Contact information]
```

### Step 5: Process Management

Follow the timeline from SKILL.md:

| Week | Activity | Your Action |
|------|----------|-------------|
| 1 | Send teasers | Email Tier 1 buyers |
| 2-3 | NDA execution | Track signatures |
| 3-4 | CIM distribution | Send full CIM |
| 5-6 | IOI due | Collect indications |
| 7-8 | Management meetings | Schedule presentations |
| 9-10 | Final bids | Negotiate LOI |

---

## Tutorial 3: Equity Research Report

**Scenario:** You're initiating coverage on TechFlow Inc. (TFL) as a BUY.

### Step 1: Use the Earnings Update Framework

```bash
# Read the sample for reference
cat skills/equity-research/examples/sample-earnings-update.md

# Create your own
cp skills/equity-research/examples/sample-earnings-update.md \
   my_tfl_update.md
```

### Step 2: Fill in the Structure

From SKILL.md, the key sections are:

```markdown
# Earnings Update: TechFlow Inc. (TFL)

**Date:** [Date]
**Rating:** BUY (Maintained)
**Price Target:** $45.00
**Current Price:** $37.50

## Quick Take
[1-2 sentence summary]

## Key Metrics vs. Estimates
| Metric | Actual | Estimate | Beat/Miss |
|--------|--------|----------|-----------|
| Revenue | $XXM | $XXM | +X% |
| EPS | $X.XX | $X.XX | +$X.XX |

## Highlights
### ✓ Positives
1. [Positive point]
2. [Positive point]

### ⚠ Concerns
1. [Concern]
2. [Concern]

## Guidance
[Updated guidance]

## Valuation Update
- Prior PT: $XX → New PT: $XX
- Rationale: [Why changed]

## Model Updates
| Year | Old EPS | New EPS | Change |
|------|---------|---------|--------|
| 2026 | $X.XX | $X.XX | +X% |

## Rating & Risk
Rating: BUY
Key Risks: [List risks]
```

### Step 3: Create Investment Thesis

```bash
# Reference the thesis framework
cat skills/equity-research/SKILL.md | grep -A 30 "INVESTMENT THESIS"
```

Draft your thesis:

```markdown
# INVESTMENT THESIS: TechFlow Inc. (TFL)

## THESIS STATEMENT
TechFlow is a BUY because its AI-powered automation platform is 
capturing significant share in a $50B market growing at 20% annually, 
with 125% net revenue retention indicating strong product-market fit 
and expansion potential.

## THEME ALIGNMENT
✓ Secular growth trend (AI/automation adoption)
✓ Market share gains (35% and growing)
✓ Margin expansion (20% → 25% EBITDA margins)

## KEY ASSUMPTIONS
1. AI revenue grows 70%+ annually (Confidence: High)
2. Net retention stays >120% (Confidence: High)
3. Operating leverage drives margin expansion (Confidence: Medium)

## WHAT NEEDS TO GO RIGHT
1. Enterprise adoption of AI automation accelerates
2. Competition from Microsoft/Google doesn't erode pricing
3. International expansion succeeds

## WHAT COULD GO WRONG
1. AI hype cycle ends, growth decelerates sharply
2. Large customers build in-house solutions
3. Macroeconomic downturn freezes enterprise IT spending

## MARGIN OF SAFETY
Current valuation: $37.50
Downside case: $28 (-25%)
Base case: $45 (+20%)
Upside case: $58 (+55%)
Risk/Reward: 3:1 (favorable)

## CONVICTION LEVEL
HIGH - Multiple data points support thesis
```

### Step 4: Track Catalysts

```markdown
# CATALYST CALENDAR: TechFlow Inc. (TFL)

## UPCOMING CATALYSTS (Next 90 Days)
| Date | Catalyst | Impact | Direction |
|------|----------|--------|-----------|
| 4/25 | Q1 Earnings | High | ? |
| 5/15 | AI Product Launch | High | Positive |
| 6/10 | Analyst Day | Medium | Neutral |

## RECENT CATALYSTS
| Date | Catalyst | Impact |
|------|----------|--------|
| 2/15 | Q4 Earnings | +12% |
| 3/1 | Partnership Announcement | +5% |

## CATALYST SCORECARD
- Positive catalysts realized: 3
- Negative catalysts realized: 0
- Thesis on track: YES
```

---

## Tutorial 4: LBO Analysis

**Scenario:** You're analyzing TechFlow Inc. as a potential PE buyout target.

### Step 1: Review LBO Framework

```bash
# Read the LBO example
cat skills/private-equity/examples/sample-lbo-output.md

# Review the SKILL.md section
cat skills/private-equity/SKILL.md | grep -A 100 "LBO (Leveraged Buyout)"
```

### Step 2: Set Up Assumptions

From the example, key inputs:

```markdown
# LBO ASSUMPTIONS: TechFlow Inc.

## Transaction
- Entry EV: $500M (10x LTM EBITDA)
- Equity: $200M (40%)
- Debt: $300M (60%)
  - Senior: $200M @ 8.5%
  - Subordinated: $100M @ 12%

## Operations (5-Year Projection)
| Year | Revenue | Growth | EBITDA | Margin |
|------|---------|--------|--------|--------|
| 0 | $65M | - | $15M | 23% |
| 1 | $74M | 15% | $18M | 24% |
| 2 | $86M | 15% | $22M | 26% |
| 3 | $100M | 17% | $28M | 28% |
| 4 | $117M | 17% | $35M | 30% |
| 5 | $137M | 17% | $42M | 31% |

## Exit
- Year 5 EBITDA: $42M
- Exit Multiple: 10x (unchanged)
- Exit EV: $420M
```

### Step 3: Calculate Returns

```markdown
# RETURNS CALCULATION

## Entry
- Sponsor Equity: $200M
- Net Debt: $285M ($300M - $15M cash)

## Exit (Year 5)
- Exit EV: $420M
- Net Debt: $23M (debt paydown from FCF)
- Equity Value: $397M
- Less: Management Equity (5%): $20M
- Sponsor Proceeds: $377M

## Returns
- MoM: 1.9x ($377M / $200M)
- IRR: ~13.5%

## Value Creation
| Source | Amount | % |
|--------|--------|---|
| EBITDA Growth | $27M × 10x = $270M | 71% |
| Debt Paydown | $262M | 69% |
| Multiple Expansion | $0 | 0% |
```

### Step 4: Sensitivity Analysis

```markdown
# SENSITIVITY ANALYSIS

## Exit Multiple vs. Revenue Growth (MoM)
| Growth \ Multiple | 8x | 9x | 10x | 11x |
|-------------------|----|----|----|----|
| 12% CAGR | 1.3x | 1.5x | 1.7x | 1.9x |
| 15% CAGR | 1.5x | 1.7x | 1.9x | 2.1x |
| 17% CAGR | 1.7x | 1.9x | 2.1x | 2.4x |

Base case (15% growth, 10x): 1.9x MoM, 13.5% IRR
```

### Step 5: IC Memo Structure

```bash
# Use the template from SKILL.md
cat skills/private-equity/SKILL.md | grep -A 80 "Investment Committee Memo"
```

Key sections to include:
1. Executive Summary (investment, returns, recommendation)
2. Company Overview (business description)
3. Market Analysis (TAM, growth, competition)
4. Investment Thesis (3-4 key points)
5. Financial Analysis (historical + projections)
6. Transaction Summary (sources & uses)
7. Returns Analysis (base/upside/downside)
8. Risk Factors (key risks + mitigation)
9. ESG Considerations
10. Appendix (detailed model)

---

## Best Practices

### Excel Modeling

1. **Color Coding** (strict adherence):
   - Blue: Hardcoded inputs
   - Black: Formulas
   - Green: Links to other sheets

2. **Formula Best Practices**:
   ```excel
   # Good: Reference assumption cells
   =Revenue * Gross_Margin
   
   # Bad: Hardcode in formulas
   =1000 * 0.40
   ```

3. **Sheet Organization**:
   - Assumptions (first sheet)
   - Income Statement
   - Balance Sheet
   - Cash Flow Statement
   - Valuation/Returns
   - Sensitivity

### Process Management

1. **Version Control**:
   ```
   techflow_comps_v1.xlsx
   techflow_comps_v2.xlsx
   techflow_comps_final.xlsx
   techflow_comps_final_FINAL.xlsx
   ```

2. **Documentation**:
   - Keep a changelog
   - Note assumption changes
   - Document data sources

3. **Review Checklist**:
   ```
   □ All formulas work
   □ Blue/black/green color coding correct
   □ Sensitivity analysis included
   □ Sources cited
   □ Math checks out
   □ Second pair of eyes reviewed
   ```

### Quality Standards

| Deliverable | Standard |
|-------------|----------|
| Comps | 5-10 comparable companies, multiple methodologies |
| DCF | 5-10 year projections, sensitivity analysis, terminal value |
| CIM | 30-50 pages, comprehensive, tells a story |
| Teaser | 1 page, anonymous, compelling highlights |
| LBO | 2.0x+ MoM, 20%+ IRR base case |
| Research Report | Clear thesis, differentiated view, price target |

---

## Troubleshooting

### Common Issues

#### Issue: "openpyxl not installed"
```bash
# Fix
pip3 install openpyxl pandas numpy

# Verify
python3 -c "import openpyxl; print('openpyxl:', openpyxl.__version__)"
```

#### Issue: "Permission denied" when running scripts
```bash
# Fix
chmod +x skills/*/scripts/*.py

# Or run with python explicitly
python3 skills/financial-analysis-core/scripts/generate-comps.py --help
```

#### Issue: Excel file won't open
- Check that you have Excel or LibreOffice installed
- Try opening with Google Sheets
- Check file isn't corrupted: `file techflow_comps.xlsx`

#### Issue: CSV output format is wrong
```bash
# View with proper formatting
column -s, -t techflow_buyers.csv | head -20

# Or use less
less -S techflow_buyers.csv
```

### Getting Help

1. **Read the SKILL.md** - Most questions answered there
   ```bash
   cat skills/financial-analysis-core/SKILL.md | less
   ```

2. **Check examples** - See how outputs should look
   ```bash
   ls skills/financial-analysis-core/examples/
   ```

3. **Review README** - Quick reference
   ```bash
   cat skills/financial-analysis-core/README.md
   ```

4. **Use --help flag** - Script documentation
   ```bash
   python3 skills/financial-analysis-core/scripts/generate-comps.py --help
   ```

---

## Next Steps

### Practice Exercises

1. **Valuation Exercise**:
   - Pick a public company
   - Build comps using the script
   - Build DCF with 3 scenarios
   - Compare to current market price

2. **M&A Exercise**:
   - Choose a recent M&A deal
   - Generate buyer list for target
   - Create teaser outline
   - Build merger model

3. **Research Exercise**:
   - Write an earnings update for a company that just reported
   - Develop investment thesis
   - Create catalyst calendar

4. **PE Exercise**:
   - Analyze a company as LBO candidate
   - Build debt schedule
   - Calculate returns
   - Write IC memo outline

### Advanced Topics

1. **Integration with live data** (Phase 3):
   - Fetch financials from SEC EDGAR
   - Pull market data from APIs
   - Automate comparable selection

2. **Report generation**:
   - Convert markdown to PDF
   - Generate presentation decks
   - Create data visualizations

3. **Collaboration**:
   - Share models with team
   - Version control with Git
   - Review workflows

---

**Happy Modeling!** 🚀

For questions or issues, refer to the SKILL.md files or the examples directory.
