---
name: private-equity
description: "Private equity workflows including deal sourcing, due diligence, LBO modeling, IC memos, and portfolio monitoring. Use for PE investing, growth equity, buyouts, and portfolio company management."
metadata:
  category: "private-equity"
  domains: ["leveraged-buyouts", "growth-equity", "venture-capital", "portfolio-management"]
  outputs: ["lbo-models", "ic-memos", "dd-checklists", "portfolio-reports", "deal-sourcing"]
  requires:
    bins: ["python3"]
    skills: ["financial-analysis-core", "investment-banking"]
---

# Private Equity

Private equity investing and portfolio management workflows.

## When to Use

✅ **Use this skill for:**

- **Deal Sourcing**: Finding investment opportunities
- **LBO Modeling**: Leveraged buyout analysis
- **Due Diligence**: Pre-investment analysis
- **IC Memos**: Investment committee presentations
- **Portfolio Monitoring**: Tracking portfolio companies
- **Exit Planning**: Sale preparation and execution

❌ **Don't use for:**

- Public equity analysis (use equity-research skill)
- Sell-side M&A (use investment-banking skill)
- Short-term trading decisions

## Quick Reference

| Task | Tool/Template | Output |
|------|---------------|--------|
| LBO analysis | LBO model script | Excel model with returns |
| Screen deals | Deal sourcing template | Target list |
| Investment decision | IC memo template | Investment memo |
| Due diligence | DD checklist | Work stream tracker |
| Track portfolio | Portfolio dashboard | KPI monitoring |

## Core Workflows

### 1. LBO (Leveraged Buyout) Model

**Purpose**: Analyze returns from acquiring a company with debt.

#### Key Assumptions:

```
TRANSACTION ASSUMPTIONS
- Entry EV: $500M
- Equity Contribution: $200M (40%)
- Debt: $300M (60%)
  - Senior Debt: $200M
  - Subordinated: $100M
- Transaction Fees: $15M (3%)
- Management Equity: 5% rollover

DEBT ASSUMPTIONS
- Senior Interest: SOFR + 400bps (8.5%)
- Subordinated Interest: 12%
- Senior Term: 7 years
- Subordinated Term: 10 years
- Mandatory Amortization: 5% of senior/year

OPERATING ASSUMPTIONS
- Revenue CAGR: 8%
- EBITDA Margin: 25% → 28%
- Capex: 3% of revenue
- NWC: 15% of revenue

EXIT ASSUMPTIONS
- Exit Year: Year 5
- Exit Multiple: 10x EBITDA
- Exit Debt/EBITDA: 3.0x
```

#### Returns Calculation:

```
LBO RETURNS ANALYSIS

Entry (Year 0):
- Purchase EV: $500M
- (+) Fees: $15M
- (=) Total Sources: $515M
- Equity: $200M
- Debt: $300M
- Rollover: $15M

Exit (Year 5):
- Revenue: $220M
- EBITDA: $62M (28% margin)
- Exit Multiple: 10.0x
- Exit EV: $620M
- (-) Net Debt: $150M
- (=) Equity Value: $470M

RETURNS:
- Multiple of Money (MoM): 2.35x
- IRR: 18.6%
- Gross Multiple: 2.35x
- Net Multiple (fees): 2.25x
```

#### Sensitivity Analysis:

```
ENTRY/EXIT MULTIPLE SENSITIVITY

Exit Multiple
Entry  | 8.0x   | 9.0x   | 10.0x  | 11.0x  | 12.0x
-------|--------|--------|--------|--------|-------
8.0x   | 1.8x   | 2.0x   | 2.2x   | 2.4x   | 2.6x
9.0x   | 1.6x   | 1.8x   | 2.0x   | 2.2x   | 2.4x
10.0x  | 1.4x   | 1.6x   | 1.8x   | 2.0x   | 2.2x
11.0x  | 1.2x   | 1.4x   | 1.6x   | 1.8x   | 2.0x

IRR SENSITIVITY (Exit Multiple = 10x)

                   | Base  | +1yr  | -1yr
-------------------|-------|-------|------
IRR                | 18.6% | 15.2% | 23.1%
```

### 2. Deal Sourcing & Screening

**Purpose**: Identify and evaluate investment opportunities.

#### Sourcing Channels:

```
DEAL SOURCING MATRIX

Channel           | Volume | Quality | Effort | Focus
------------------|--------|---------|--------|------
Proprietary       | Low    | High    | High   | Primary
Intermediaries    | High   | Med     | Med    | Active
Auctions          | High   | Low     | Low    | Selective
Inbound           | Med    | Var     | Low    | Evaluate
Co-invest         | Med    | High    | Low    | Opportunistic
```

#### Initial Screening Criteria:

```
SCREENING SCORECARD

Criteria                    | Weight | Score (1-5) | Weighted
----------------------------|--------|-------------|----------
Market attractiveness       | 20%    |             |
Competitive position        | 20%    |             |
Financial profile           | 15%    |             |
Growth prospects            | 15%    |             |
Management quality          | 15%    |             |
Deal structure/fit          | 10%    |             |
Valuation                   | 5%     |             |
----------------------------|--------|-------------|----------
TOTAL                       | 100%   |             |

Minimum to proceed: 3.5/5.0
```

#### Deal Tracking:

```
DEAL PIPELINE

| Company | Sector | Revenue | EBITDA | Source | Status | Probability | Target Close |
|---------|--------|---------|--------|--------|--------|-------------|--------------|
| Co A    | HC     | $50M    | $12M   | Bank   | DD     | 60%         | Q2-26        |
| Co B    | Tech   | $30M    | $8M    | Prop   | IOI    | 40%         | Q3-26        |
| Co C    | Ind    | $80M    | $16M   | Int    | Screen | 20%         | TBD          |

PIPELINE SUMMARY
- Active: 3 deals
- Weighted value: $XXM
- Q2 close probability: 60%
```

### 3. Due Diligence

**Purpose**: Comprehensive pre-investment analysis.

#### DD Workstreams:

```
DUE DILIGENCE CHECKLIST

COMMERCIAL DD
□ Market size and growth
□ Competitive positioning
□ Customer concentration
□ Pricing power
□ Barriers to entry
□ Technology/IP assessment

FINANCIAL DD
□ Quality of earnings
□ Working capital analysis
□ Debt-like items
□ Accounting policies
□ Financial projections
□ Capex requirements

OPERATIONAL DD
□ Facility tours
□ Manufacturing assessment
□ Supply chain review
□ IT systems
□ Organizational structure
□ KPI deep-dive

LEGAL DD
□ Corporate structure
□ Material contracts
□ Litigation review
□ IP ownership
□ Regulatory compliance
□ Environmental issues

MANAGEMENT DD
□ Background checks
□ Reference calls
□ Compensation review
□ Succession planning
□ Alignment/rollover

ESG DD
□ Environmental practices
□ Social impact
□ Governance structure
□ Compliance history
```

#### DD Report Structure:

```
DUE DILIGENCE SUMMARY

EXECUTIVE SUMMARY
- Overall assessment: [Green/Yellow/Red]
- Key findings: [List]
- Deal-breakers: [List or None]
- Value creation opportunities: [List]

FINDINGS BY WORKSTREAM

Commercial
✓ Strengths: [List]
⚠ Concerns: [List]
□ Action items: [List]

Financial
✓ Strengths: [List]
⚠ Concerns: [List]
□ Action items: [List]

[Repeat for each workstream]

RISK ASSESSMENT
| Risk | Probability | Impact | Mitigation | Status |
|------|-------------|--------|------------|--------|
| [Risk 1] | Med | High | [Action] | Open |
| [Risk 2] | Low | Med | [Action] | Closed |

RECOMMENDATION
[Proceed/Proceed with conditions/Do not proceed]

CONDITIONS TO CLOSE
1. [Condition 1]
2. [Condition 2]
```

### 4. Investment Committee Memo

**Purpose**: Present investment opportunity to investment committee.

#### Standard Sections:

```
INVESTMENT COMMITTEE MEMO

1. EXECUTIVE SUMMARY
   - Company: [Name]
   - Investment: $XXM equity
   - Transaction Value: $XXXM
   - Expected IRR: XX%
   - MoM: X.Xx
   - Recommendation: [Approve/Reject]

2. COMPANY OVERVIEW
   - Business description
   - History and milestones
   - Market position
   - Competitive advantages

3. MARKET ANALYSIS
   - Market size (TAM/SAM/SOM)
   - Growth drivers
   - Competitive landscape
   - Industry trends

4. INVESTMENT THESIS
   Primary drivers:
   1. [Thesis point 1]
   2. [Thesis point 2]
   3. [Thesis point 3]
   
   Value creation plan:
   - Revenue growth: [Initiatives]
   - Margin expansion: [Initiatives]
   - Multiple expansion: [Drivers]

5. FINANCIAL ANALYSIS
   Historical Performance:
   | Year | Revenue | EBITDA | Margin |
   |------|---------|--------|--------|
   | 2023 | $XXM    | $XM    | XX%    |
   | 2024 | $XXM    | $XM    | XX%    |
   | LTM  | $XXM    | $XM    | XX%    |
   
   Projections:
   | Year | Revenue | EBITDA | FCF   |
   |------|---------|--------|-------|
   | 1    | $XXM    | $XM    | $XM   |
   | 3    | $XXM    | $XM    | $XM   |
   | 5    | $XXM    | $XM    | $XM   |

6. TRANSACTION SUMMARY
   Sources & Uses:
   Sources:
   - Equity: $XXM
   - Debt: $XXM
   - Total: $XXM
   
   Uses:
   - Purchase price: $XXM
   - Fees: $XM
   - Refi existing: $XM
   - Cash to BS: $XM

7. RETURNS ANALYSIS
   Base Case:
   - Entry: $XXM EBITDA @ X.Xx
   - Exit: $XXM EBITDA @ X.Xx
   - MoM: X.Xx
   - IRR: XX%
   
   Sensitivity:
   | Case    | EBITDA | Multiple | MoM  | IRR  |
   |---------|--------|----------|------|------|
   | Upside  | $XXM   | XX.x     | X.Xx | XX%  |
   | Base    | $XXM   | XX.x     | X.Xx | XX%  |
   | Downside| $XXM   | XX.x     | X.Xx | XX%  |

8. RISK FACTORS
   Key risks:
   1. [Risk 1] - Mitigation: [Action]
   2. [Risk 2] - Mitigation: [Action]
   3. [Risk 3] - Mitigation: [Action]

9. ESG CONSIDERATIONS
   - Environmental: [Assessment]
   - Social: [Assessment]
   - Governance: [Assessment]

10. APPENDIX
    - Detailed model
    - Due diligence reports
    - Management bios
    - Key contracts
```

### 5. Portfolio Monitoring

**Purpose**: Track performance of portfolio companies.

#### KPI Dashboard:

```
PORTFOLIO DASHBOARD
As of: [Date]

SUMMARY METRICS
| Metric           | Fund    | Target | Status |
|------------------|---------|--------|--------|
| TVPI             | 1.4x    | 2.0x   | ⚠      |
| DPI              | 0.3x    | 0.5x   | ✓      |
| RVPI             | 1.1x    | 1.5x   | ⚠      |
| IRR              | 18%     | 25%    | ⚠      |

PORTFOLIO COMPANY KPIs

| Company | Sector | Revenue | EBITDA | vs Plan | Value | MoM |
|---------|--------|---------|--------|---------|-------|-----|
| Co 1    | HC     | $XXM    | $XM    | +5%     | $XXM  | 1.8x|
| Co 2    | Tech   | $XXM    | $XM    | -3%     | $XXM  | 2.2x|
| Co 3    | Ind    | $XXM    | $XM    | +12%    | $XXM  | 2.5x|

ATTENTION REQUIRED
| Company | Issue | Action | Owner | Due |
|---------|-------|--------|-------|-----|
| Co 2    | Miss  | Plan   | MD    | 3/15|

UPCOMING BOARD MEETINGS
| Company | Date | Key Topics |
|---------|------|------------|
| Co 1    | 3/20 | M&A, 2026 budget |
| Co 3    | 4/5  | Exit planning |
```

#### Monthly Reporting Template:

```
PORTFOLIO COMPANY UPDATE
Company: [Name] | Month: [Month] | Report Date: [Date]

FINANCIAL PERFORMANCE
| Metric       | Actual | Budget | Variance | YTD    | vs YTD Budget |
|--------------|--------|--------|----------|--------|---------------|
| Revenue      | $XM    | $XM    | +X%      | $XXM   | +X%           |
| EBITDA       | $XM    | $XM    | -X%      | $XM    | -X%           |
| EBITDA Margin| XX%    | XX%    | -Xpbs    | XX%    | -Xpbs         |
| Cash         | $XM    | $XM    | +$XM     | -      | -             |

OPERATIONAL HIGHLIGHTS
✓ [Positive development]
✓ [Positive development]
⚠ [Challenge or concern]

VALUE CREATION PROGRESS
| Initiative | Status | Impact | Notes |
|------------|--------|--------|-------|
| [Init 1]   | Green  | +$XM   | Ahead of plan |
| [Init 2]   | Yellow | +$XM   | Delayed 1 month |
| [Init 3]   | Red    | -      | Stalled |

RISKS & ISSUES
| Risk | Status | Mitigation | Owner |
|------|--------|------------|-------|
| [Risk 1] | Open | [Action] | [Name] |

LOOKING AHEAD
Next 30 days:
- [Action item]
- [Action item]

NEXT BOARD MEETING: [Date]
Key topics: [List]
```

## Implementation

### Generate LBO Model

```bash
python3 skills/private-equity/scripts/generate-lbo-model.py \
  --company "TargetCo" \
  --entry-ev 500 \
  --equity 200 \
  --exit-year 5 \
  --output lbo-model.xlsx
```

### Create IC Memo

```bash
python3 skills/private-equity/scripts/generate-ic-memo.py \
  --company "TargetCo" \
  --investment 50 \
  --irr 25 \
  --output ic-memo.md
```

### Track Deal Pipeline

```bash
python3 skills/private-equity/scripts/update-pipeline.py \
  --add "Company XYZ,Software,$30M revenue,Active DD" \
  --output pipeline.csv
```

### Portfolio Dashboard

```bash
python3 skills/private-equity/scripts/generate-portfolio-dashboard.py \
  --fund "Fund IV" \
  --quarter "Q1-2026" \
  --output portfolio-update.md
```

## Best Practices

### LBO Modeling

1. **Conservative Assumptions**
   - Use base case, not best case
   - Stress test key drivers
   - Model downside scenarios

2. **Capital Structure**
   - Don't maximize leverage
   - Leave cushion for operations
   - Consider refinancing risk

3. **Returns Hurdles**
   - Minimum 2.0x MoM
   - Minimum 20% IRR
   - Consider hold period flexibility

### Due Diligence

1. **Red Flags**
   - Customer concentration >30%
   - Declining market share
   - Key person dependency
   - Accounting irregularities
   - Litigation exposure

2. **Value Creation Focus**
   - Identify low-hanging fruit
   - Quantify revenue synergies
   - Assess margin levers
   - Plan for add-ons

### Portfolio Management

1. **Active Ownership**
   - Monthly KPI tracking
   - Quarterly board meetings
   - Annual strategic planning
   - Value creation playbook

2. **Early Warning Signs**
   - Misses to plan
   - Management turnover
   - Customer losses
   - Margin compression

## Output Formatting

### Investment Summary Format

```
INVESTMENT SUMMARY

Company: [Name] | Sector: [Sector]
Investment: $XXM | Date: [Date]

THESIS
[2-3 sentence investment case]

RETURNS
- MoM: X.Xx
- IRR: XX%
- Hold: X years

STATUS
[Active/Realized/Written off]
Current value: $XXM
```

## Resources

### Templates

- `templates/lbo-template.xlsx` - LBO model
- `templates/ic-memo-template.md` - Investment memo
- `templates/dd-checklist.md` - Due diligence checklist
- `templates/portfolio-update.md` - Monthly reporting

### Examples

- `examples/sample-lbo-output.md` - LBO summary example
- `examples/sample-ic-memo.md` - IC memo example
- `examples/sample-dd-report.md` - DD report example

### External Resources

- LBO data: Preqin, PitchBook, Burgiss
- Debt markets: LCD, S&P Leveraged Commentary
- Industry data: Same as investment banking

---

**Disclaimer**: PE tools for analysis workflows only. Not investment advice. Models are illustrative - actual returns will vary.
