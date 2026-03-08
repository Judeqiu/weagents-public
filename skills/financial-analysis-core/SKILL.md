---
name: financial-analysis-core
description: "Core financial analysis capabilities including comparable company analysis (comps), DCF valuation, and financial modeling. Use for investment banking, equity research, corporate finance, and valuation tasks. Provides Excel templates, modeling standards, and workflow guidance."
metadata:
  category: "financial-analysis"
  domains: ["investment-banking", "equity-research", "corporate-finance", "valuation"]
  outputs: ["excel_models", "valuation_analysis", "presentation_materials"]
  requires:
    bins: ["python3", "pip"]
    python_packages: ["openpyxl", "pandas", "numpy"]
---

# Financial Analysis Core

Core financial analysis capabilities for valuation and modeling tasks.

## When to Use

✅ **Use this skill for:**

- **Comparable Company Analysis (Comps)**: Valuation multiples, benchmarking
- **DCF Valuation**: Discounted cash flow models, terminal value
- **Financial Modeling**: 3-statement models, projection building
- **Precedent Transactions**: M&A deal analysis, transaction comps
- **Presentation Materials**: Output formatting for decks and reports

❌ **Don't use for:**

- Real-time trading decisions (use specialized trading tools)
- Regulatory compliance filing (consult legal/compliance)
- Tax advice (consult tax professionals)

## Quick Reference

| Analysis Type | Command/Tool | Output |
|--------------|--------------|--------|
| Comparable Companies | `generate-comps.py` | Excel workbook |
| DCF Model | `generate-dcf.py` | Excel model |
| 3-Statement Model | Use template | Excel model |
| Precedent Transactions | `generate-precedents.py` | Excel workbook |

## Core Workflows

### 1. Comparable Company Analysis (Comps)

**Purpose**: Value a company based on trading multiples of similar public companies.

#### Standard Process:

1. **Define the Universe**
   - Identify target company sector/sub-sector
   - Find publicly traded competitors
   - Include companies with similar:
     - Business model
     - Growth profile
     - Margin structure
     - Geographic exposure

2. **Select Metrics**

   **Equity Value Multiples:**
   | Multiple | Formula | Best For |
   |----------|---------|----------|
   | P/E | Price / EPS | Profitable companies |
   | P/B | Price / Book Value | Financial institutions |
   | Dividend Yield | Dividend / Price | Income stocks |

   **Enterprise Value Multiples:**
   | Multiple | Formula | Best For |
   |----------|---------|----------|
   | EV/Revenue | EV / Revenue | Growth companies, pre-profit |
   | EV/EBITDA | EV / EBITDA | Most industries (excl. banks) |
   | EV/EBIT | EV / EBIT | Capital-intensive businesses |

3. **Calculate Multiples**
   - Use LTM (Last Twelve Months) or NTM (Next Twelve Months)
   - Calendarize if fiscal years differ
   - Adjust for non-recurring items
   - Use fully diluted shares outstanding

4. **Analyze and Apply**
   - Calculate median, mean, high, low
   - Consider qualitative factors
   - Apply appropriate discount/premium
   - Derive valuation range

#### Example Output Structure:

```
COMPARABLE COMPANY ANALYSIS

Company          | EV/Rev | EV/EBITDA | P/E  | P/B
-----------------|--------|-----------|------|-----
Peer A           | 4.2x   | 12.5x     | 18.2x| 2.1x
Peer B           | 3.8x   | 11.2x     | 16.8x| 1.9x
Peer C           | 5.1x   | 14.3x     | 21.1x| 2.4x
-----------------|--------|-----------|------|-----
Median           | 4.2x   | 12.5x     | 18.2x| 2.1x
Mean             | 4.4x   | 12.7x     | 18.7x| 2.1x
High             | 5.1x   | 14.3x     | 21.1x| 2.4x
Low              | 3.8x   | 11.2x     | 16.8x| 1.9x

Implied Valuation (Target):
- Low: $X million (at 3.8x EV/EBITDA)
- Median: $Y million (at 12.5x EV/EBITDA)
- High: $Z million (at 14.3x EV/EBITDA)
```

### 2. DCF Valuation

**Purpose**: Value a company based on projected future cash flows.

#### Standard Process:

1. **Project Free Cash Flows (5-10 years)**

   **Unlevered Free Cash Flow (UFCF):**
   ```
   EBIT
   (-) Taxes on EBIT
   (+) D&A
   (-) Capex
   (-) Change in NWC
   = UFCF
   ```

   **Key Drivers:**
   - Revenue growth rate
   - EBITDA margin expansion/contraction
   - Tax rate
   - D&A as % of revenue or PP&E
   - Capex as % of revenue
   - NWC days

2. **Calculate WACC**

   ```
   WACC = (E/V) × Re + (D/V) × Rd × (1 - Tc)
   
   Where:
   - E = Market value of equity
   - D = Market value of debt
   - V = E + D (Total value)
   - Re = Cost of equity (CAPM)
   - Rd = Cost of debt
   - Tc = Corporate tax rate
   ```

   **Cost of Equity (CAPM):**
   ```
   Re = Rf + β × (Rm - Rf)
   
   Where:
   - Rf = Risk-free rate (10-year Treasury)
   - β = Equity beta
   - Rm - Rf = Market risk premium (typically 5-7%)
   ```

3. **Calculate Terminal Value**

   **Perpetuity Growth Method:**
   ```
   TV = UFCF(n+1) / (WACC - g)
      = UFCF(n) × (1 + g) / (WACC - g)
   
   Where g = perpetual growth rate (typically 2-3%, max GDP growth)
   ```

   **Exit Multiple Method:**
   ```
   TV = EBITDA(n) × Exit Multiple
   ```

4. **Discount to Present Value**

   ```
   PV = FCF / (1 + WACC)^n
   ```

5. **Calculate Enterprise and Equity Value**

   ```
   Enterprise Value = PV(Explicit Period) + PV(Terminal Value)
   
   Equity Value = Enterprise Value
                  (-) Total Debt
                  (-) Preferred Stock
                  (-) Non-controlling Interests
                  (+) Cash & Cash Equivalents
   ```

#### Example Output Structure:

```
DCF VALUATION SUMMARY

Assumptions:
- WACC: 9.5%
- Terminal Growth Rate: 2.5%
- Forecast Period: 5 years

Projected Free Cash Flows ($ millions):
Year    | 1    | 2    | 3    | 4    | 5
--------|------|------|------|------|------
Revenue | 100  | 115  | 130  | 145  | 160
EBITDA  | 20   | 24   | 28   | 32   | 36
UFCF    | 12   | 15   | 18   | 21   | 24

Valuation:
- PV of Explicit FCF: $65 million
- Terminal Value: $320 million
- PV of Terminal Value: $204 million
- Enterprise Value: $269 million
- (+) Cash: $10 million
- (-) Debt: $50 million
- Equity Value: $229 million

Implied Share Price: $XX.XX
```

### 3. Three-Statement Financial Model

**Purpose**: Integrated income statement, balance sheet, and cash flow projections.

#### Key Linkages:

```
INCOME STATEMENT
  Revenue
  (-) COGS
  = Gross Profit
  (-) OpEx
  = EBITDA
  (-) D&A
  = EBIT
  (-) Interest
  = EBT
  (-) Taxes
  = Net Income

BALANCE SHEET (Changes flow to...)
  Assets:
    Cash ← From Cash Flow Statement
    AR ← Driven by revenue, DSO
    Inventory ← Driven by COGS, Inventory days
    PP&E ← (+) Capex, (-) D&A
  
  Liabilities & Equity:
    Debt ← Debt schedule
    Equity ← (+) Net Income, (-) Dividends

CASH FLOW STATEMENT
  CFO: Net Income + D&A - ΔNWC
  CFI: (-) Capex + Asset sales
  CFF: Debt issuance/repayment + Equity
  
  Cash = Beginning Cash + ΔCash
```

#### Model Color Coding:

| Color | Meaning | Example |
|-------|---------|---------|
| **Blue** | Hardcoded inputs/constants | Historical data, assumptions |
| **Black** | Formulas/calculations | Projections, derived values |
| **Green** | Links to other sheets | References, cross-sheet links |

## Implementation

### Installation

```bash
# Install Python dependencies
pip3 install openpyxl pandas numpy

# Verify installation
python3 skills/financial-analysis-core/scripts/generate-comps.py --help
```

### Generating a Comps Model

```bash
# Basic usage
python3 skills/financial-analysis-core/scripts/generate-comps.py \
  --target "Acme Corp" \
  --peers "PeerA,PeerB,PeerC" \
  --output "acme_comps.xlsx"

# With metrics specification
python3 skills/financial-analysis-core/scripts/generate-comps.py \
  --target "Acme Corp" \
  --peers-file peers.csv \
  --metrics "EV/EBITDA,P/E,EV/Revenue" \
  --output "acme_comps.xlsx"
```

### Generating a DCF Model

```bash
# Basic usage
python3 skills/financial-analysis-core/scripts/generate-dcf.py \
  --company "Acme Corp" \
  --years 5 \
  --wacc 9.5 \
  --growth 2.5 \
  --output "acme_dcf.xlsx"
```

### Using Templates

```bash
# Copy 3-statement model template
cp skills/financial-analysis-core/templates/3-statement-template.xlsx \
   my-company-model.xlsx

# Copy comps template
cp skills/financial-analysis-core/templates/comps-template.xlsx \
   my-comps-analysis.xlsx
```

## Best Practices

### Modeling Standards

1. **Consistency**
   - Use consistent time periods (all LTM or all NTM)
   - Calendarize fiscal years that don't align
   - Same currency for all companies

2. **Accuracy**
   - Double-check share counts (fully diluted)
   - Verify net debt calculations
   - Include all balance sheet items in EV

3. **Transparency**
   - Document all assumptions
   - Show your work in intermediate calculations
   - Use clear labels and units

4. **Sensitivity Analysis**
   - Always include sensitivity tables
   - Test key assumptions (WACC, growth, margins)
   - Show range of outcomes

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mixing equity and enterprise multiples | Be clear about which is which |
| Using different time periods | Standardize to LTM or NTM |
| Forgetting to add back cash | Equity Value = EV - Net Debt |
| Ignoring dilution | Use fully diluted shares |
| Wrong sign on NWC | Increase in NWC = cash outflow |
| Not calendarizing | Adjust for fiscal year mismatches |

## Excel Tips

### Keyboard Shortcuts

| Action | Windows | Mac |
|--------|---------|-----|
| Fill down | Ctrl+D | Cmd+D |
| Fill right | Ctrl+R | Cmd+R |
| Absolute reference | F4 | Cmd+T |
| Sum formula | Alt+= | Cmd+Shift+T |
| Go to cell | Ctrl+G | Cmd+G |
| Find precedent | Ctrl+[ | Cmd+[ |

### Formula Best Practices

```excel
# Never hardcode in formulas - use assumption cells
=Revenue * GrossMargin  ✅
=1000 * 0.40            ❌

# Use named ranges for important inputs
=WACC * (1 - TaxRate)   ✅
=9.5% * (1 - 21%)       ❌

# Always anchor references appropriately
=A$1 * B2              ✅ (row anchor for header)
=A1 * B2               ❌ (will break when copied)
```

## Output Formatting

### Standard Sections for Valuation Output

1. **Executive Summary**
   - Key metrics and conclusions
   - Valuation range
   - Key assumptions

2. **Company Overview**
   - Business description
   - Financial highlights
   - Key metrics

3. **Valuation Analysis**
   - Comps table
   - Precedent transactions (if applicable)
   - DCF summary
   - Football field chart (valuation ranges)

4. **Appendix**
   - Detailed assumptions
   - Sensitivity analysis
   - Company financials

### Football Field Chart Format

```
Valuation Summary ($ millions)

                    Low     Median   High
Comps (EV/EBITDA)   200     250      300
Comps (P/E)         220     280      340
Precedents          240     290      350
DCF                 230     270      310
-----------------------------------------
Overall Range       220     270      325
```

## Resources

### Templates

- `templates/comps-template.xlsx` - Comparable company analysis
- `templates/dcf-template.xlsx` - DCF valuation model
- `templates/3-statement-template.xlsx` - Integrated financial model
- `templates/precedents-template.xlsx` - Transaction comps

### Examples

- `examples/sample-comps-report.md` - Sample comps output
- `examples/sample-dcf-output.md` - Sample DCF output

### External Resources

- Aswath Damodaran's data: pages.stern.nyu.edu/~adamodar/
- SEC EDGAR for filings: sec.gov/edgar
- Bloomberg/Reuters for market data

---

**Disclaimer**: These tools and templates assist with financial analysis workflows but do not provide investment advice. Always verify conclusions with qualified financial professionals.
