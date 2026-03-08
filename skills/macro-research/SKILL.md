---
name: macro-research
description: "Macroeconomic research and impact assessment for portfolio strategy. Uses McKinsey-level analysis to evaluate how economic trends, policy decisions, and global factors affect equity markets and portfolio positioning. Use for asset allocation, sector rotation, and macro-driven investment strategy."
metadata:
  category: "macro-research"
  domains: ["macroeconomics", "asset-allocation", "sector-strategy", "policy-analysis"]
  outputs: ["macro-strategy-briefings", "sector-rotation-recommendations", "policy-impact-assessments", "economic-outlooks"]
  requires:
    bins: ["python3"]
    python_packages: ["pandas", "numpy", "matplotlib"]
    skills: ["equity-research", "quantitative-research"]
---

# Macro Research

Comprehensive macroeconomic analysis for portfolio strategy and asset allocation decisions.

## When to Use

✅ **Use this skill for:**

- **Interest Rate Analysis**: Impact on growth vs value, duration exposure
- **Inflation Assessment**: Sector winners/losers, real vs nominal returns
- **GDP Forecasting**: Corporate earnings implications
- **Currency Analysis**: International vs domestic exposure
- **Fed Policy Outlook**: Rate path implications
- **Employment Analysis**: Consumer spending and labor market
- **Global Risk Assessment**: Geopolitics, trade, supply chains
- **Sector Rotation Strategy**: Cyclical positioning based on cycle
- **Portfolio Adjustments**: Macro-driven rebalancing

❌ **Don't use for:**

- Individual stock picking (use equity-research)
- Technical trading signals (use technical-analysis)
- Quantitative alpha strategies (use quantitative-research)
- Company-specific valuation (use financial-analysis-core)

## Quick Reference

| Task | Tool/Workflow | Output |
|------|---------------|--------|
| Interest rate impact | `analyze-rates.py` | Rate sensitivity report |
| Inflation analysis | `inflation-outlook.py` | Inflation impact assessment |
| Fed policy outlook | `fed-analysis.py` | Policy path forecast |
| Sector rotation | `sector-cycle-model.py` | Rotation recommendations |
| Global risk scan | `global-risk-monitor.py` | Risk dashboard |
| Full macro assessment | `macro-deep-dive` workflow | Executive briefing |

## Core Workflows

### 1. McKinsey-Level Macro Impact Assessment (Full Analysis)

**Purpose**: Comprehensive macro strategy briefing with clear action plan.

```
MACRO STRATEGY BRIEFING
Date: [Date] | Classification: CONFIDENTIAL
Prepared for: [Portfolio/Client Name]

═══════════════════════════════════════════════════════════════
EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════════

Current Economic Regime: [Expansion/Peak/Contraction/Trough]
Market Cycle Position: [Early/Mid/Late]
Recommended Portfolio Stance: [Offensive/Neutral/Defensive]

Key Action Items:
1. [Primary recommendation with rationale]
2. [Secondary recommendation]
3. [Tertiary recommendation]

Immediate Risks: [List top 3 risks with mitigation]
Opportunities: [List top 3 opportunities]

═══════════════════════════════════════════════════════════════
1. INTEREST RATE ENVIRONMENT
═══════════════════════════════════════════════════════════════

Current Fed Funds Rate: X.XX%
Market Implied Path (Fed Funds Futures):
┌─────────────┬──────────────┬──────────────┐
│ Meeting     │ Implied Rate │ Probability  │
├─────────────┼──────────────┼──────────────┤
│ [Month]     │    X.XX%     │   XX% hike   │
│ [Month]     │    X.XX%     │   XX% pause  │
│ [Month]     │    X.XX%     │   XX% cut    │
└─────────────┴──────────────┴──────────────┘

Yield Curve Analysis:
- 2Y Treasury: X.XX%
- 10Y Treasury: X.XX%
- Spread: -XXbps [Inverted/Flat/Steep]
- Historical Context: [Xth percentile]

Real Rates (10Y TIPS): X.XX%

Impact on Asset Classes:

┌─────────────────┬─────────────┬─────────────┬─────────────┐
│ Asset Class     │ Sensitivity │ Impact      │ Position    │
├─────────────────┼─────────────┼─────────────┼─────────────┤
│ Growth Stocks   │    High     │  Negative   │  Underweight│
│ Value Stocks    │    Low      │  Positive   │  Overweight │
│ Long Duration   │    High     │  Negative   │  Reduce     │
│ Short Duration  │    Low      │  Positive   │  Increase   │
│ REITs           │    High     │  Negative   │  Underweight│
│ Financials      │    Medium   │  Mixed      │  Neutral    │
│ Utilities       │    High     │  Negative   │  Underweight│
└─────────────────┴─────────────┴─────────────┴─────────────┘

Interest Rate Outlook (6-12 months):
- Base Case: [Scenario description]
- Upside (Rates Higher): [Probability and impact]
- Downside (Rates Lower): [Probability and impact]

═══════════════════════════════════════════════════════════════
2. INFLATION ANALYSIS
═══════════════════════════════════════════════════════════════

Current Inflation Metrics:
- CPI (YoY): X.X% [Rising/Falling/Stable]
- Core CPI (YoY): X.X% [Ex food/energy]
- PCE (YoY): X.X% [Fed's preferred measure]
- Core PCE (YoY): X.X%

Inflation Components:
- Goods inflation: X.X% [Transitory/Sticky]
- Services inflation: X.X% [Wage-driven/Supply-driven]
- Housing (OER): X.X% [Lagging indicator]
- Energy: X.X% [Volatile component]

5-Year Breakeven Inflation: X.X%
10-Year Breakeven Inflation: X.X%

Inflation Trajectory Forecast:
┌────────────┬─────────┬─────────┬─────────┐
│ Period     │ CPI YoY │ Core CPI│ Trend   │
├────────────┼─────────┼─────────┼─────────┤
│ Current    │   X.X%  │   X.X%  │  [↗↘→]  │
│ 6 Months   │   X.X%  │   X.X%  │  [↗↘→]  │
│ 12 Months  │   X.X%  │   X.X%  │  [↗↘→]  │
└────────────┴─────────┴─────────┴─────────┘

Sector Impact Matrix:

Beneficiaries of Inflation:
- Energy: [Rationale]
- Materials: [Rationale]
- Financials (steepener): [Rationale]
- Real Assets: [Rationale]

Hurt by Inflation:
- Technology (high duration): [Rationale]
- Consumer Discretionary: [Rationale]
- Utilities: [Rationale]

═══════════════════════════════════════════════════════════════
3. GDP GROWTH OUTLOOK
═══════════════════════════════════════════════════════════════

Current GDP Data:
- Last Quarter (QoQ annualized): +X.X%
- Last Quarter (YoY): +X.X%
- vs. Potential Growth (~2%): [Above/Below] trend

GDP Components Health:
- Consumption: [Strong/Moderate/Weak] - [Details]
- Investment: [Strong/Moderate/Weak] - [Details]
- Government: [Strong/Moderate/Weak] - [Details]
- Net Exports: [Strong/Moderate/Weak] - [Details]

Leading Indicators:
- ISM Manufacturing: XX.X [Expansion/Contraction]
- ISM Services: XX.X [Expansion/Contraction]
- Yield Curve: [Leading/Recession signal]
- Consumer Confidence: [Trend]

GDP Forecast:
┌────────────┬──────────────┬──────────────┐
│ Period     │ Consensus    │ Your View    │
├────────────┼──────────────┼──────────────┤
│ Q[X] 20XX  │    +X.X%     │    +X.X%     │
│ Q[X] 20XX  │    +X.X%     │    +X.X%     │
│ Full Year  │    +X.X%     │    +X.X%     │
└────────────┴──────────────┴──────────────┘

Recession Probability (Next 12 Months): XX%
- Source: [Fed model, yield curve, consensus]

Earnings Impact:
- Current S&P 500 EPS Growth: +X.X%
- Historical relationship to GDP: [Correlation]
- Forward EPS risk: [Upside/Downside bias]

═══════════════════════════════════════════════════════════════
4. US DOLLAR ANALYSIS
═══════════════════════════════════════════════════════════════

Dollar Index (DXY): XXX.XX [Strong/Moderate/Weak]
Trend: [Appreciating/Depreciating/Stable]

Major Currency Pairs:
- EUR/USD: X.XXXX
- USD/JPY: XXX.XX
- GBP/USD: X.XXXX
- USD/CNY: X.XXXX

Dollar Drivers:
- Interest rate differentials: [Favoring USD/Against USD]
- Safe haven flows: [Supporting/Pressuring]
- Growth differential: [US stronger/Weaker]
- Fed vs CB policy: [Divergent/Convergent]

Portfolio Impact:

Domestic vs International Exposure:
┌─────────────────┬──────────────┬──────────────┐
│ Exposure Type   │ Dollar Impact│ Recommended  │
├─────────────────┼──────────────┼──────────────┤
│ US Domestic     │  Neutral     │  Overweight  │
│ International   │  Negative    │  Hedge FX    │
│ EM (USD debt)   │  Negative    │  Underweight │
│ Commodities     │  Negative    │  Underweight │
└─────────────────┴──────────────┴──────────────┘

Hedging Recommendations:
- [Specific currency hedging strategies if needed]

═══════════════════════════════════════════════════════════════
5. EMPLOYMENT & CONSUMER ANALYSIS
═══════════════════════════════════════════════════════════════

Labor Market Health:
- Unemployment Rate: X.X%
- Non-Farm Payrolls (last): +XXX,XXX
- Job Openings (JOLTS): X.X million
- Labor Force Participation: XX.X%
- Wage Growth (YoY): +X.X%

Employment Trends:
- Job creation: [Strong/Moderate/Weak]
- Wage pressure: [Rising/Stable/Falling]
- Labor slack: [Minimal/Moderate/Significant]

Consumer Health Indicators:
- Real Personal Income Growth: +X.X%
- Personal Savings Rate: X.X%
- Consumer Credit Growth: +X.X%
- Retail Sales Trend: [Strong/Moderate/Weak]

Consumer Spending Outlook:
- Near term (3 months): [Positive/Neutral/Negative]
- Medium term (12 months): [Positive/Neutral/Negative]

Sector Implications:
- Consumer Discretionary: [Impact and recommendation]
- Consumer Staples: [Impact and recommendation]
- Housing/REITs: [Impact and recommendation]

═══════════════════════════════════════════════════════════════
6. FEDERAL RESERVE POLICY OUTLOOK
═══════════════════════════════════════════════════════════════

Fed's Dual Mandate Status:
- Maximum Employment: [Achieved/Near achieved/Not achieved]
- Price Stability: [Achieved/Near achieved/Not achieved]

Fed Communication Analysis:
- Latest FOMC Statement: [Key changes]
- Chair Powell's Tone: [Hawkish/Dovish/Neutral]
- Dot Plot Implications: [Rate path]

Market Pricing vs Fed Guidance:
- Market pricing [More hawkish/More dovish/Aligned] with Fed
- Discrepancy in [X] meetings

Policy Scenarios (Next 12 Months):

Scenario 1: Soft Landing (XX% probability)
- Description: Inflation falls to 2% without recession
- Rate path: Hold at X.XX%, then cut to X.XX%
- Market impact: [Positive for risk assets]
- Portfolio action: [Overweight equities, favor quality]

Scenario 2: Hard Landing (XX% probability)
- Description: Inflation requires recession to tame
- Rate path: Hold, then aggressive cuts to X.XX%
- Market impact: [Negative initially, then recovery]
- Portfolio action: [Defensive positioning, then buy dip]

Scenario 3: Stagflation (XX% probability)
- Description: Inflation persistent with weak growth
- Rate path: Higher for longer
- Market impact: [Negative for most assets]
- Portfolio action: [Real assets, commodities, cash]

Most Likely Scenario: [Scenario name]
Confidence Level: [High/Medium/Low]

═══════════════════════════════════════════════════════════════
7. GLOBAL RISK FACTORS
═══════════════════════════════════════════════════════════════

Geopolitical Risks:
┌─────────────────────┬──────────┬──────────┬──────────┐
│ Risk Factor         │ Severity │ Probability│ Impact  │
├─────────────────────┼──────────┼──────────┼──────────┤
│ [Risk 1]            │  High    │   XX%    │ [Type]   │
│ [Risk 2]            │  Medium  │   XX%    │ [Type]   │
│ [Risk 3]            │  Low     │   XX%    │ [Type]   │
└─────────────────────┴──────────┴──────────┴──────────┘

Trade War / Supply Chain:
- Current tariffs/trade tensions: [Status]
- Supply chain normalization: [Progress]
- Near-shoring trends: [Impact]
- Commodity price impact: [Details]

China Economic Slowdown:
- Property sector crisis: [Status]
- Consumer confidence: [Trend]
- Export impact to US: [Details]
- EM contagion risk: [Assessment]

Energy Market:
- Oil price trend: $XX.XX [Direction]
- Supply constraints: [OPEC+, shale]
- Demand outlook: [China, EV adoption]
- Energy transition: [Timeline and impact]

Climate Policy:
- Regulatory changes: [Upcoming]
- Transition costs: [Sector impact]
- Green investment opportunities: [Areas]

═══════════════════════════════════════════════════════════════
8. SECTOR ROTATION STRATEGY
═══════════════════════════════════════════════════════════════

Current Economic Cycle Position: [Early/Mid/Late/Turning]

Historical Sector Performance by Cycle Phase:
┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Sector          │ Early Cycle │ Mid Cycle   │ Late Cycle  │ Recession   │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Technology      │    ★★★      │    ★★       │    ★        │    ★        │
│ Financials      │    ★★       │    ★★★      │    ★★       │    ★        │
│ Industrials     │    ★★★      │    ★★★      │    ★★       │    ★        │
│ Consumer Disc   │    ★★★      │    ★★       │    ★        │    ★        │
│ Materials       │    ★★       │    ★★★      │    ★★       │    ★        │
│ Energy          │    ★        │    ★        │    ★★★      │    ★★       │
│ Health Care     │    ★★       │    ★★       │    ★★       │    ★★★      │
│ Consumer Staples│    ★        │    ★        │    ★★       │    ★★★      │
│ Utilities       │    ★        │    ★        │    ★★       │    ★★★      │
└─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
★ = Relative performance

Recommended Sector Allocation:

┌─────────────────┬──────────┬────────────┬────────────┬────────────┐
│ Sector          │ Current  │ Target     │ Change     │ Conviction │
├─────────────────┼──────────┼────────────┼────────────┼────────────┤
│ Technology      │   XX%    │   XX%      │   ±X%      │   High     │
│ Financials      │   XX%    │   XX%      │   ±X%      │   High     │
│ Health Care     │   XX%    │   XX%      │   ±X%      │   Medium   │
│ Industrials     │   XX%    │   XX%      │   ±X%      │   Medium   │
│ Consumer Disc   │   XX%    │   XX%      │   ±X%      │   Low      │
│ Energy          │   XX%    │   XX%      │   ±X%      │   Medium   │
│ Materials       │   XX%    │   XX%      │   ±X%      │   Low      │
│ Consumer Staples│   XX%    │   XX%      │   ±X%      │   Medium   │
│ Utilities       │   XX%    │   XX%      │   ±X%      │   Low      │
│ Real Estate     │   XX%    │   XX%      │   ±X%      │   Low      │
│ Communication   │   XX%    │   XX%      │   ±X%      │   Neutral  │
└─────────────────┴──────────┴────────────┴────────────┴────────────┘

Sector Rotation Rationale:
1. [Primary sector pick with detailed reasoning]
2. [Secondary sector pick with reasoning]
3. [Sector to underweight with reasoning]

Factor Rotation:
- Growth vs Value: [Recommendation and macro driver]
- Large vs Small: [Recommendation and macro driver]
- Quality vs Cyclical: [Recommendation and macro driver]

═══════════════════════════════════════════════════════════════
9. PORTFOLIO ADJUSTMENT RECOMMENDATIONS
═══════════════════════════════════════════════════════════════

Current Portfolio Summary:
- Total Value: $XXX,XXX
- Equity Allocation: XX%
- Fixed Income: XX%
- Alternatives: XX%
- Cash: XX%

Recommended Adjustments:

IMMEDIATE ACTIONS (This Week):
1. [Action 1: Reduce/increase specific position]
   - Current: XX%
   - Target: XX%
   - Rationale: [Macro driver]
   
2. [Action 2: Add new position/sector]
   - Add: [Ticker/Sector]
   - Size: X%
   - Rationale: [Macro driver]

3. [Action 3: Hedge/reduce risk]
   - Action: [Specific hedge]
   - Cost: $X,XXX
   - Protection: [What risk it addresses]

NEAR-TERM ACTIONS (This Month):
1. [Rebalancing trigger]
2. [Sector rotation execution]
3. [Duration adjustment in fixed income]

CONDITIONAL ACTIONS (If/Then):
- IF [condition], THEN [action]
- IF [condition], THEN [action]

═══════════════════════════════════════════════════════════════
10. TIMELINE & CATALYSTS
═══════════════════════════════════════════════════════════════

Key Economic Releases (Next 30 Days):
┌────────────┬─────────────────────┬──────────────┐
│ Date       │ Event               │ Market Impact│
├────────────┼─────────────────────┼──────────────┤
│ [Date]     │ CPI Release         │  High        │
│ [Date]     │ FOMC Meeting        │  High        │
│ [Date]     │ Jobs Report         │  High        │
│ [Date]     │ GDP Revision        │  Medium      │
│ [Date]     │ Retail Sales        │  Medium      │
└────────────┴─────────────────────┴──────────────┘

Expected Market Impact Timeline:
- Immediate (0-3 months): [Key macro factors driving markets]
- Medium term (3-6 months): [Expected developments]
- Longer term (6-12 months): [Structural shifts]

When to Re-evaluate:
- [Trigger 1: Data release or event]
- [Trigger 2: Change in Fed communication]
- [Trigger 3: Recession signal or recovery confirmation]

Next Review Date: [Date]

═══════════════════════════════════════════════════════════════
11. RISK SCENARIOS & MITIGATION
═══════════════════════════════════════════════════════════════

Top 3 Downside Risks:

Risk 1: [Specific risk name]
- Probability: XX%
- Impact: [Portfolio loss estimate]
- Early Warning Signs: [What to watch]
- Mitigation: [Specific hedge or position change]

Risk 2: [Specific risk name]
- [Same structure]

Risk 3: [Specific risk name]
- [Same structure]

Stress Test Results:
- Portfolio return if recession in 6 months: -X.X%
- Portfolio return if inflation re-accelerates: -X.X%
- Portfolio return if soft landing: +X.X%

═══════════════════════════════════════════════════════════════
12. CONCLUSION & ACTION PLAN
═══════════════════════════════════════════════════════════════

Strategic View: [Summary of macro outlook]

Portfolio Stance: [Offensive/Neutral/Defensive]

Top 3 Actions:
1. [Most important action with target completion date]
2. [Second action with timeline]
3. [Third action with timeline]

Expected Portfolio Impact:
- Risk-adjusted return improvement: +X.X%
- Volatility impact: [Increase/Decrease/Stable]
- Downside protection: [Improved/Stable]

───────────────────────────────────────────────────────────────
DISCLAIMER: This macro analysis is based on current economic 
data and market conditions. Views expressed are subject to 
change based on new information. Past performance does not 
guarantee future results.
───────────────────────────────────────────────────────────────
```

### 2. Interest Rate Sensitivity Analysis

**Purpose**: Measure portfolio impact from rate changes.

**Analysis Framework**:
1. **Duration Analysis**: Weighted average duration of holdings
2. **Sector Sensitivity**: Rate sensitivity by sector
3. **Factor Analysis**: Growth (long duration) vs Value (short duration)
4. **Scenario Testing**: +100bps, -100bps impact

### 3. Inflation Regime Analysis

**Purpose**: Determine inflation trajectory and sector impact.

**Inflation Types**:
- **Demand-Pull**: Strong economy, consumer spending
- **Cost-Push**: Supply constraints, input costs
- **Built-In**: Wage-price spirals

**Sector Winners/Losers by Inflation Type**:
| Type | Winners | Losers |
|------|---------|--------|
| Demand-Pull | Cyclicals, Financials | Defensives |
| Cost-Push | Commodities, Energy | Marginal businesses |
| Built-In | Real assets, TIPS | Fixed income, Cash |

### 4. Economic Cycle Positioning

**Purpose**: Align portfolio with economic cycle phase.

**Cycle Phases**:
1. **Early Cycle**: Recovery from recession
   - Favor: Financials, Consumer Discretionary, Technology
2. **Mid Cycle**: Expansion peak
   - Favor: Industrials, Materials, Energy
3. **Late Cycle**: Growth deceleration
   - Favor: Energy, Healthcare, Consumer Staples
4. **Recession**: Economic contraction
   - Favor: Healthcare, Utilities, Consumer Staples

## CLI Commands

```bash
# Full macro assessment
ono-cli macro analyze --portfolio <portfolio_id> --timeframe 12m

# Interest rate impact
ono-cli macro rates --current X.XX --scenario +100bps

# Inflation analysis
ono-cli macro inflation --target-cpi 2.0 --current-cpi X.X

# Fed policy outlook
ono-cli macro fed --meetings 4 --dot-plot

# Sector rotation recommendation
ono-cli macro sectors --cycle-phase mid --risk-profile moderate

# Global risk scan
ono-cli macro risks --severity high --probability 30

# Employment/consumer analysis
ono-cli macro labor --unemployment X.X --wage-growth X.X

# Currency impact
ono-cli macro fx --base USD --exposure international

# GDP forecast impact
ono-cli macro gdp --forecast +X.X --earnings-correlation
```

## Data Sources

### Essential Data
- **Fed Data**: Fed Funds rate, FOMC statements, dot plots
- **Treasury Data**: Yield curve, TIPS (real rates)
- **Economic Releases**: CPI, PPI, GDP, Employment
- **Market Data**: Sector ETFs, factor returns

### External Sources
- Federal Reserve Economic Data (FRED)
- Bloomberg/Reuters economic calendars
- CME FedWatch (rate probabilities)
- Consensus Economics (forecasts)

## Best Practices

### Do's ✅
- Use multiple indicators to confirm cycle position
- Consider interactions between macro factors
- Update analysis after major data releases
- Test portfolio sensitivity to macro shocks
- Monitor leading indicators, not just coincident

### Don'ts ❌
- Don't rely on single macro indicator
- Don't ignore cross-asset correlations
- Don't make binary recession/no-recession calls
- Don't forget policy lags (6-18 months)
- Don't trade on stale macro views

## Output Formats

### Macro Dashboard
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  MACRO DASHBOARD: [Date]                  ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  Economic Regime: [Expansion/Contraction] ┃
┃  Cycle Position:  [Early/Mid/Late]        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  RATES     │ Fed: X.XX% │ 10Y: X.XX%     ┃
┃  INFLATION │ CPI: X.X%  │ Trend: ↓        ┃
┃  GROWTH    │ GDP: +X.X% │ NFP: +XXXK      ┃
┃  DOLLAR    │ DXY: XXX.X │ Trend: →        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  RECOMMENDATION: [Offensive/Defensive]    ┃
┃  Conviction: [High/Medium/Low]            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Related Skills

- **equity-research**: For sector and company-specific context
- **quantitative-research**: For factor analysis and backtesting
- **technical-analysis**: For entry/exit timing
- **financial-analysis-core**: For valuation context

## Risk Management

### Macro Risk Factors
1. **Policy Mistake**: Fed overtightening or undertightening
2. **Geopolitical Shock**: War, trade conflict, sanctions
3. **Financial Instability**: Credit events, liquidity crisis
4. **Structural Shift**: Demographics, productivity changes

### Hedging Strategies
- **Duration Hedging**: Treasury futures, options
- **Currency Hedging**: FX forwards, options
- **Sector Hedging**: Sector ETFs, options
- **Tail Risk**: VIX calls, put spreads

## Resources

- **Fed Resources**: FRED, FOMC minutes, speeches
- **Economic Data**: BEA, BLS, Census Bureau
- **Research**: Fed research papers, NBER
- **Market Data**: Bloomberg, FactSet, Refinitiv
