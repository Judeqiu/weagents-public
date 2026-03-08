---
name: investment-banking
description: "Investment banking workflows including M&A analysis, pitch materials, CIMs, teasers, buyer lists, and deal execution. Use for sell-side and buy-side advisory, fairness opinions, and transaction analysis."
metadata:
  category: "investment-banking"
  domains: ["mergers-acquisitions", "sell-side-advisory", "buy-side-advisory", "capital-markets"]
  outputs: ["pitch-books", "cim", "teasers", "buyer-lists", "merger-models", "fairness-opinions"]
  requires:
    bins: ["python3"]
    skills: ["financial-analysis-core"]
---

# Investment Banking

Investment banking advisory workflows and deliverables.

## When to Use

✅ **Use this skill for:**

- **Sell-Side Advisory**: Selling a company or asset
- **Buy-Side Advisory**: Acquiring a company or asset
- **M&A Analysis**: Merger modeling, accretion/dilution
- **Pitch Materials**: Pitch books, teasers, executive summaries
- **Deal Execution**: CIMs, buyer lists, process letters
- **Fairness Opinions**: Valuation opinions for boards

❌ **Don't use for:**

- Day-to-day corporate finance (use financial-analysis-core)
- Public equity research (use equity-research skill)
- Fund investment decisions (use private-equity skill)

## Quick Reference

| Task | Tool/Template | Output |
|------|---------------|--------|
| Sell-side process | CIM template | Confidential Information Memorandum |
| Market a deal | Teaser template | One-page teaser |
| Find buyers | Buyer list script | Strategic and financial buyers |
| M&A modeling | Merger model template | Accretion/dilution analysis |
| Pitch a client | Pitch book template | Presentation deck |

## Core Workflows

### 1. Sell-Side M&A Process

**Overview**: Guide a client through selling their business.

#### Phase 1: Preparation (Weeks 1-4)

1. **Engagement & Diligence**
   - Sign engagement letter
   - Gather company information
   - Build financial model
   - Identify value drivers and risks

2. **Valuation**
   - Trading comps
   - Precedent transactions
   - DCF analysis
   - LBO analysis (if relevant)

3. **Marketing Materials**
   - Draft teaser
   - Prepare CIM
   - Build data room
   - Create management presentation

#### Phase 2: Marketing (Weeks 5-10)

1. **Buyer Universe**
   ```
   Strategic Buyers:
   - Direct competitors
   - Adjacent industry players
   - Suppliers/customers
   - Platform acquirers
   
   Financial Buyers:
   - Large-cap PE (>$10B AUM)
   - Mid-market PE ($1-10B AUM)
   - Family offices
   - Search funds
   ```

2. **Outreach Process**
   | Week | Activity |
   |------|----------|
   | 1 | Send teasers to buyer list |
   | 2-3 | NDA execution |
   | 3-4 | CIM distribution |
   | 5-6 | Indication of Interest (IOI) due |
   | 7-8 | Management meetings |
   | 9-10 | Final bids / LOI |

3. **Bid Comparison**
   | Bidder | Value | Structure | Certainty | Timing |
   |--------|-------|-----------|-----------|--------|
   | A | $500M | Cash | High | 60 days |
   | B | $520M | 50/50 | Medium | 90 days |
   | C | $480M | Stock | Lower | 45 days |

#### Phase 3: Execution (Weeks 11-20)

1. **Letter of Intent (LOI)**
   - Exclusive period (30-60 days)
   - Purchase price and adjustments
   - Key terms and conditions

2. **Due Diligence**
   - Financial (accounting policies, working capital)
   - Legal (contracts, litigation, IP)
   - Commercial (customers, markets, competition)
   - Operational (facilities, employees, systems)

3. **Definitive Agreement**
   - Purchase agreement negotiation
   - Representations and warranties
   - Indemnification provisions
   - Closing conditions

### 2. Buy-Side M&A Process

**Overview**: Advise a client on acquiring a target company.

#### Phase 1: Strategy & Targeting

1. **Investment Thesis**
   - Strategic rationale
   - Synergy opportunities
   - Integration challenges
   - Financial returns

2. **Target Screening**
   | Criteria | Weight | Target A | Target B | Target C |
   |----------|--------|----------|----------|----------|
   | Strategic fit | 30% | 8/10 | 6/10 | 9/10 |
   | Financial profile | 25% | 7/10 | 8/10 | 6/10 |
   | Cultural fit | 20% | 6/10 | 7/10 | 8/10 |
   | Valuation | 25% | 7/10 | 6/10 | 7/10 |
   | **Weighted Score** | | **7.1** | **6.8** | **7.5** |

#### Phase 2: Analysis & Approach

1. **Initial Valuation**
   - Public comps (if applicable)
   - Precedent transactions
   - DCF analysis
   - Synergy-adjusted valuation

2. **Approach Strategy**
   - Friendly vs. hostile
   - Timing considerations
   - Regulatory approvals needed
   - Financing structure

#### Phase 3: Execution

1. **Due Diligence Checklist**
   ```
   Financial:
   □ 3 years audited financials
   □ Latest 12 months actuals
   □ Financial projections
   □ Working capital analysis
   □ Debt schedule
   □ Cap table
   
   Commercial:
   □ Customer list and contracts
   □ Market analysis
   □ Competitive landscape
   □ Pricing and margins
   
   Legal:
   □ Material contracts
   □ Litigation summary
   □ IP portfolio
   □ Regulatory compliance
   
   Operational:
   □ Employee census
   □ Facility leases
   □ IT systems
   □ Insurance policies
   ```

2. **Offer Structuring**
   | Component | Option A | Option B |
   |-----------|----------|----------|
   | Cash | 100% | 60% |
   | Stock | 0% | 40% |
   | Earnout | None | $50M |
   | Total Value | $500M | $550M |

### 3. Merger Model (Accretion/Dilution)

**Purpose**: Analyze the financial impact of an acquisition.

#### Model Structure:

```
ACQUISITION ASSUMPTIONS
- Purchase Price: $500M
- Financing: 50% Debt ($250M @ 6%), 50% Equity
- Synergies: $20M (Year 1), $35M (Year 2)
- Transaction Costs: $15M

PRO FORMA INCOME STATEMENT
                        Buyer    Target    Pro Forma
Revenue                 $400M    $150M     $550M
EBITDA                  $80M     $30M      $130M (incl. synergies)
D&A                     $20M     $8M       $30M
EBIT                    $60M     $22M      $100M

Interest Expense        $5M      $0M       $20M ($5M + $15M new)
EBT                     $55M     $22M      $80M
Taxes (25%)             $13.8M   $5.5M     $20M
Net Income              $41.3M   $16.5M    $60M

Shares Outstanding      50M      -         60M (50M + 10M issued)
EPS                     $0.83    -         $1.00
```

#### Accretion/Dilution Analysis:

```
Standalone Buyer EPS: $0.83
Pro Forma EPS: $1.00
Accretion: $0.17 (+20%)
```

#### Key Metrics:

| Metric | Calculation |
|--------|-------------|
| EPS Accretion/(Dilution) | Pro Forma EPS - Standalone EPS |
| % Accretion | Accretion / Standalone EPS |
| Break-even Synergies | Synergies needed for neutral EPS |
| IRR | Internal rate of return on investment |

### 4. Confidential Information Memorandum (CIM)

**Purpose**: Detailed selling document for potential buyers.

#### Standard Sections:

1. **Executive Summary**
   - Company overview
   - Investment highlights
   - Financial summary
   - Transaction overview

2. **Business Overview**
   - History and milestones
   - Products/services
   - Market opportunity
   - Competitive advantages
   - Growth strategy

3. **Management Team**
   - Biographies
   - Organization chart
   - Key personnel risks

4. **Financial Information**
   - Historical financials (3-5 years)
   - Management projections
   - Key performance indicators
   - Working capital trends
   - Capital structure

5. **Market Analysis**
   - Industry overview
   - Competitive landscape
   - Customer analysis
   - Growth drivers

6. **Risk Factors**
   - Business risks
   - Financial risks
   - Industry risks
   - Regulatory risks

7. **Appendix**
   - Detailed financial statements
   - Customer contracts
   - Facility information
   - Additional due diligence materials

### 5. Teaser (Executive Summary)

**Purpose**: One-page document to generate interest without revealing identity.

#### Format:

```
INVESTMENT OPPORTUNITY
[Industry] Company - $XXXM Revenue

OVERVIEW
- Leading provider of [products/services]
- [X] years of operating history
- [XX]% market share in [segment]
- Strong, stable customer relationships

FINANCIAL HIGHLIGHTS
Revenue:     $XXXM (XX% 3-year CAGR)
EBITDA:      $XXM (XX% margin)
EBITDA CAGR: XX%
Free Cash Flow: $XXM

INVESTMENT HIGHLIGHTS
✓ [Key strength 1]
✓ [Key strength 2]
✓ [Key strength 3]
✓ [Key strength 4]

MARKET OPPORTUNITY
$XXB addressable market growing at X% annually

TRANSACTION
Seeking strategic alternatives including:
- Sale to strategic buyer
- Sale to financial sponsor
- Recapitalization

CONTACT
[Investment Bank Name]
[Contact information]
```

## Implementation

### Generate Buyer List

```bash
python3 skills/investment-banking/scripts/generate-buyer-list.py \
  --company "Target Inc" \
  --industry "software" \
  --revenue-range "50-200" \
  --output buyers.csv
```

### Create Teaser Template

```bash
cp skills/investment-banking/templates/teaser-template.docx \
   my-teaser.docx
```

### Create CIM Template

```bash
cp skills/investment-banking/templates/cim-template.docx \
   my-cim.docx
```

### Merger Model

```bash
python3 skills/investment-banking/scripts/generate-merger-model.py \
  --buyer "Acquirer Corp" \
  --target "Target Inc" \
  --price 500 \
  --mix "50/50" \
  --synergies 35 \
  --output merger-model.xlsx
```

## Best Practices

### Deal Process Management

1. **Maintain Momentum**
   - Set clear deadlines
   - Keep buyers engaged
   - Manage client expectations

2. **Information Control**
   - Phase information disclosure
   - Protect sensitive data
   - Use clean rooms for competitive buyers

3. **Competitive Tension**
   - Multiple bidders preferred
   - Create urgency
   - Manage auction dynamics

### CIM Writing Tips

1. **Tell a Story**
   - Clear narrative arc
   - Compelling investment thesis
   - Address potential concerns upfront

2. **Be Specific**
   - Quantify claims
   - Provide customer examples
   - Include market data

3. **Highlight Value**
   - Growth opportunities
   - Margin expansion potential
   - Strategic value to buyers

### Buyer List Criteria

| Buyer Type | Strategic | Financial |
|------------|-----------|-----------|
| **Focus** | Synergies, strategic fit | Returns, growth potential |
| **Valuation** | Often pay more (synergies) | Disciplined returns hurdle |
| **Speed** | May move slower (integration planning) | Often faster (platform deals) |
| **Certainty** | Cash on balance sheet | Financing condition |
| **Fit** | Similar businesses | Various industries |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Over-sharing in teaser | Keep it high-level, anonymous |
| Weak competitive tension | Minimum 3-4 serious bidders |
| Poor data room organization | Index everything, be thorough |
| Ignoring cultural issues | Address integration early |
| Unrealistic valuation expectations | Market data beats wishful thinking |

## Output Formatting

### Bid Summary Format

```
BID SUMMARY - [Company Name]
Date: [Date]

| Bidder | Price | Structure | Certainty | Closing |
|--------|-------|-----------|-----------|---------|
| A | $520M | All cash | High (cash on hand) | 45 days |
| B | $535M | 75/25 C/S | Medium (financing) | 75 days |
| C | $510M | All cash | High | 30 days |

RECOMMENDATION: [Recommendation with rationale]
```

### Fairness Opinion Summary

```
FAIRNESS OPINION - [Company Name]

We have reviewed the proposed transaction...

VALUATION ANALYSIS:
- Trading Comps: $400M - $500M
- Precedent Transactions: $450M - $550M
- DCF: $420M - $520M
- LBO: $400M - $480M

CONCLUSION: The consideration to be received is fair...
```

## Resources

### Templates

- `templates/cim-template.docx` - Confidential Information Memorandum
- `templates/teaser-template.docx` - One-page teaser
- `templates/pitch-book.pptx` - Pitch presentation
- `templates/merger-model.xlsx` - Accretion/dilution model
- `templates/process-letter.docx` - Process letter to buyers

### Examples

- `examples/sample-cim-outline.md` - CIM structure example
- `examples/sample-teaser.md` - Teaser content example
- `examples/sample-bid-summary.md` - Bid summary format

### External Resources

- M&A databases: Capital IQ, PitchBook, MergerMarket
- Public filings: SEC EDGAR for precedent transactions
- Industry reports: IBISWorld, Gartner, Forrester

---

**Disclaimer**: These tools assist with investment banking workflows. This is not investment advice. All materials should be reviewed by qualified professionals before use.
