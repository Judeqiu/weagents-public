---
name: quantitative-research
description: "Quantitative research and statistical analysis for finding market edges. Uses Renaissance Technologies-inspired data-driven methods to identify patterns, anomalies, and statistical advantages in stock behavior. Use for alpha generation, factor analysis, backtesting, and quantitative strategy development."
metadata:
  category: "quantitative-research"
  domains: ["quantitative-finance", "statistical-arbitrage", "factor-investing", "algorithmic-trading"]
  outputs: ["quantitative-memos", "statistical-analyses", "backtest-results", "factor-models", "alpha-research"]
  requires:
    bins: ["python3"]
    python_packages: ["pandas", "numpy", "scipy", "scikit-learn", "statsmodels", "matplotlib", "seaborn"]
    skills: ["equity-research", "technical-analysis"]
---

# Quantitative Research

Data-driven quantitative analysis using statistical methods to find market edges and alpha opportunities.

## When to Use

✅ **Use this skill for:**

- **Statistical Pattern Recognition**: Find recurring patterns in price data
- **Factor Analysis**: Identify factors driving stock returns
- **Seasonality Analysis**: Discover calendar-based patterns
- **Event Study Analysis**: Measure impact of specific events
- **Anomaly Detection**: Find statistical deviations from normal behavior
- **Backtesting**: Test strategies on historical data
- **Correlation Analysis**: Find relationships between securities
- **Regime Detection**: Identify market regime changes

❌ **Don't use for:**

- Fundamental company analysis (use equity-research)
- Technical chart patterns (use technical-analysis)
- Macroeconomic forecasting (use macro-research)
- Subjective investment thesis development

## Quick Reference

| Task | Tool/Script | Output |
|------|-------------|--------|
| Seasonal patterns | `analyze-seasonality.py` | Seasonal pattern report |
| Event correlation | `event-study.py` | Event impact analysis |
| Factor analysis | `factor-model.py` | Factor exposures |
| Correlation matrix | `correlation-analysis.py` | Correlation heatmap |
| Anomaly detection | `detect-anomalies.py` | Anomaly list |
| Backtest strategy | `backtest.py` | Performance metrics |
| Statistical summary | `quant-summary.py` | Full quantitative memo |

## Core Workflows

### 1. Renaissance Technologies Pattern Finder (Full Analysis)

**Purpose**: Comprehensive quantitative analysis to find statistical edges.

```
QUANTITATIVE RESEARCH MEMO: [SYMBOL]
Date: [Date] | Analyst: Quantitative Research
Classification: CONFIDENTIAL

═══════════════════════════════════════════════════════════════
EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════════

Stock: [SYMBOL]
Analysis Period: [Start Date] to [End Date]
Key Finding: [One-sentence summary of primary edge]
Statistical Edge: [Yes/No - with confidence level]
Actionable Signal: [Current signal strength and direction]

═══════════════════════════════════════════════════════════════
1. SEASONAL PATTERN ANALYSIS
═══════════════════════════════════════════════════════════════

Monthly Performance Patterns:
┌─────────┬──────────┬──────────┬──────────┐
│ Month   │ Avg Ret% │ Win Rate │ T-Stat   │
├─────────┼──────────┼──────────┼──────────┤
│ January │   +X.X%  │   XX%    │  X.XX    │
│ February│   +X.X%  │   XX%    │  X.XX    │
│ ...     │   ...    │   ...    │  ...     │
│ December│   +X.X%  │   XX%    │  X.XX    │
└─────────┴──────────┴──────────┴──────────┘

Best Performing Months: [List with statistical significance]
Worst Performing Months: [List with statistical significance]

Statistical Significance (p < 0.05): [Yes/No]
Effect Size (Cohen's d): [Small/Medium/Large]

Intra-Month Patterns:
- First trading day of month: [Performance summary]
- Last trading day of month: [Performance summary]
- Mid-month (options expiration): [Performance summary]

═══════════════════════════════════════════════════════════════
2. DAY-OF-WEEK ANALYSIS
═══════════════════════════════════════════════════════════════

Daily Returns by Day:
┌───────────┬──────────┬──────────┬──────────┐
│ Day       │ Avg Ret% │ Win Rate │ T-Stat   │
├───────────┼──────────┼──────────┼──────────┤
│ Monday    │   +X.X%  │   XX%    │  X.XX    │
│ Tuesday   │   +X.X%  │   XX%    │  X.XX    │
│ Wednesday │   +X.X%  │   XX%    │  X.XX    │
│ Thursday  │   +X.X%  │   XX%    │  X.XX    │
│ Friday    │   +X.X%  │   XX%    │  X.XX    │
└───────────┴──────────┴──────────┴──────────┘

Statistically Significant Day Effects: [Yes/No - details]

═══════════════════════════════════════════════════════════════
3. MARKET EVENT CORRELATION
═══════════════════════════════════════════════════════════════

Federal Reserve Events:
┌─────────────────────┬──────────┬──────────┬──────────┐
│ Event               │ Avg Ret% │ Win Rate │ Sample N │
├─────────────────────┼──────────┼──────────┼──────────┤
│ FOMC Meeting Day    │   +X.X%  │   XX%    │    XX    │
│ Day After FOMC      │   +X.X%  │   XX%    │    XX    │
│ Fed Chair Speech    │   +X.X%  │   XX%    │    XX    │
└─────────────────────┴──────────┴──────────┴──────────┘

Economic Data Releases:
- CPI Release Day: [Performance]
- Non-Farm Payrolls: [Performance]
- GDP Announcement: [Performance]
- Earnings Season: [Performance]

Correlation with Market Events: [Strong/Moderate/Weak]
Predictive Power: [High/Medium/Low]

═══════════════════════════════════════════════════════════════
4. INSTITUTIONAL FLOW ANALYSIS
═══════════════════════════════════════════════════════════════

Insider Activity (Last 6 Months):
┌─────────────┬────────┬────────┬───────────┐
│ Activity    │ Buys   │ Sells  │ Net Ratio │
├─────────────┼────────┼────────┼───────────┤
│ Insider     │   XX   │   XX   │  X.X:1    │
└─────────────┴────────┴────────┴───────────┘

Institutional Ownership Trend:
- Last Quarter: XX.X%
- Previous Quarter: XX.X%
- Trend: [Increasing/Decreasing/Stable]
- Net Change: +X.X%

Significant Institutional Moves:
- [Institution Name]: [Buy/Sell] [X,XXX,XXX] shares
- [Institution Name]: [Buy/Sell] [X,XXX,XXX] shares

Institutional Sentiment: [Bullish/Bearish/Neutral]

═══════════════════════════════════════════════════════════════
5. SHORT INTEREST & SQUEEZE POTENTIAL
═══════════════════════════════════════════════════════════════

Short Interest Metrics:
- Short Interest: XX.XM shares
- Short % of Float: X.X%
- Days to Cover: X.X days
- Short Interest Trend: [Rising/Falling/Stable]

Squeeze Potential Score: [1-10]
  - High short interest: [Yes/No]
  - Price momentum: [Positive/Negative]
  - Volume surge potential: [High/Medium/Low]

Risk/Reward for Shorts: [Favorable/Unfavorable]

═══════════════════════════════════════════════════════════════
6. OPTIONS MARKET SIGNALS
═══════════════════════════════════════════════════════════════

Options Activity (Last 30 Days):
- Call/Put Volume Ratio: X.XX
- Unusual Volume Days: XX days
- Net Premium Flow: [Positive/Negative] $X.XM

Implied Volatility Analysis:
- Current IV: XX.X%
- IV Percentile: XXth
- IV vs HV Spread: +X.X%

Skew Analysis:
- Put Skew: [Steep/Flat/Inverted]
- Call Skew: [Steep/Flat]
- Sentiment Indicator: [Bullish/Bearish/Neutral]

Unusual Options Activity Signals:
- Large block trades: [X trades identified]
- Sweep activity: [High/Medium/Low]
- Institutional flow: [Direction]

═══════════════════════════════════════════════════════════════
7. EARNINGS BEHAVIOR PATTERNS
═══════════════════════════════════════════════════════════════

Historical Earnings Reactions:
┌────────────┬──────────┬──────────┬──────────┐
│ Quarter    │ Expected │ Surprise │ Price Chg│
├────────────┼──────────┼──────────┼──────────┤
│ Q4 2024    │   $X.XX  │   +X%    │   +X.X%  │
│ Q3 2024    │   $X.XX  │   -X%    │   -X.X%  │
│ Q2 2024    │   $X.XX  │   +X%    │   +X.X%  │
│ Q1 2024    │   $X.XX  │   -X%    │   -X.X%  │
└────────────┴──────────┴──────────┴──────────┘

Earnings Pattern Recognition:
- Pre-earnings drift: [Positive/Negative/None] - [Statistical significance]
- Post-earnings gap pattern: [Fill/Reverses/Continues]
- Earnings day volatility: XX.X% avg move
- Beat/Miss cycle: [Identifiable pattern?]

Implied Earnings Move: ±X.X%
Historical Average Move: ±X.X%
Edge Opportunity: [Yes/No - explanation]

═══════════════════════════════════════════════════════════════
8. SECTOR ROTATION SIGNALS
═══════════════════════════════════════════════════════════════

Sector Momentum:
- Current Sector Ranking: [X] of [11]
- Momentum Score: XX.X/100
- Relative Strength vs Sector: [Outperforming/Underperforming]
- Relative Strength vs Market: [Outperforming/Underperforming]

Sector Rotation Position:
- Early cycle: [Yes/No]
- Late cycle: [Yes/No]
- Defensive rotation: [Yes/No]
- Growth/Value rotation: [Yes/No]

Correlation with Sector Rotation Factors:
- Interest rate sensitivity: [High/Medium/Low]
- Inflation sensitivity: [High/Medium/Low]
- Economic cycle position: [Expansion/Peak/Contraction/Trough]

═══════════════════════════════════════════════════════════════
9. STATISTICAL EDGE SUMMARY
═══════════════════════════════════════════════════════════════

Quantifiable Edges Identified:

Edge #1: [Seasonal/Day-of-week/Event pattern]
  - Confidence: [High/Medium/Low]
  - Statistical Significance: p = 0.0XX
  - Historical Win Rate: XX%
  - Expected Return: +X.X%
  - Sharpe Ratio: X.XX
  - Max Drawdown: -X.X%

Edge #2: [Another pattern]
  [Same metrics]

[Continue for all significant edges]

═══════════════════════════════════════════════════════════════
10. BACKTEST RESULTS
═══════════════════════════════════════════════════════════════

Strategy: [Description of signal-based strategy]
Period: [X years of historical data]

Performance Metrics:
┌─────────────────────┬──────────┬──────────┐
│ Metric              │ Strategy │ Benchmark│
├─────────────────────┼──────────┼──────────┤
│ Annual Return       │  +XX.X%  │  +XX.X%  │
│ Volatility          │   XX.X%  │   XX.X%  │
│ Sharpe Ratio        │   X.XX   │   X.XX   │
│ Max Drawdown        │  -XX.X%  │  -XX.X%  │
│ Win Rate            │   XX%    │   N/A    │
│ Profit Factor       │   X.XX   │   N/A    │
│ Calmar Ratio        │   X.XX   │   N/A    │
└─────────────────────┴──────────┴──────────┘

Alpha Generated: +X.X% annually
Beta to Market: X.XX
Information Ratio: X.XX

Out-of-Sample Testing: [Results if available]
Walk-Forward Analysis: [Results if available]

═══════════════════════════════════════════════════════════════
11. RISK FACTORS & CAVEATS
═══════════════════════════════════════════════════════════════

Statistical Limitations:
- Sample size: [Large/Adequate/Small - X observations]
- Look-ahead bias: [Controlled/Potential issue]
- Survivorship bias: [Addressed/Not applicable]
- Multiple testing: [Bonferroni correction applied?]

Economic Regime Considerations:
- Current regime: [Bull/Bear/High volatility/Low volatility]
- Pattern robustness across regimes: [Strong/Moderate/Weak]

Data Quality Issues:
- [Any data concerns]

═══════════════════════════════════════════════════════════════
12. CONCLUSION & RECOMMENDATION
═══════════════════════════════════════════════════════════════

Primary Edge: [Summary of strongest finding]

Current Signal Strength: [Strong/Moderate/Weak/None]
Signal Direction: [Long/Short/Neutral]

Position Sizing Recommendation:
- Base on edge strength and conviction
- Suggested allocation: X% of portfolio

Entry Timing: [Immediate/Wait for trigger/Not recommended]
Exit Strategy: [Based on signal reversal or stop-loss]

Next Review: [When to re-evaluate]

───────────────────────────────────────────────────────────────
This analysis is for research purposes only. Past performance 
does not guarantee future results. Statistical edges can decay 
over time as markets become more efficient.
───────────────────────────────────────────────────────────────
```

### 2. Seasonal Pattern Analysis

**Purpose**: Identify calendar-based patterns in stock performance.

**Methodology**:
1. Calculate average returns by month (last 10+ years)
2. Test statistical significance (t-test, p < 0.05)
3. Check consistency across years
4. Analyze sub-periods (first half, second half of month)
5. Identify intraday patterns if data available

### 3. Event Study Analysis

**Purpose**: Measure stock reaction to specific events.

**Event Types**:
- Earnings announcements
- Fed meetings
- Economic data releases
- Product launches
- Regulatory decisions
- CEO changes
- M&A announcements

**Analysis Window**:
- Pre-event: [-5, -1] days
- Event day: [0]
- Post-event: [+1, +5] days
- Cumulative abnormal returns (CAR)

### 4. Factor Analysis

**Purpose**: Identify factor exposures driving returns.

**Common Factors**:
- **Market**: Beta to overall market
- **Size**: Small-cap vs large-cap
- **Value**: Book-to-price, earnings yield
- **Momentum**: 12-month minus 1-month returns
- **Quality**: Profitability, stability
- **Volatility**: Low volatility premium
- **Liquidity**: Amihud illiquidity measure

**Regression Model**:
```
Stock Return = α + β1(Market) + β2(Size) + β3(Value) + β4(Momentum) + ε
```

**Interpretation**:
- **Alpha (α)**: True excess return not explained by factors
- **Beta (β)**: Sensitivity to each factor
- **R²**: Percentage of returns explained by factors

### 5. Correlation Analysis

**Purpose**: Find relationships between securities.

**Types**:
- **Pairwise Correlation**: Between two securities
- **Rolling Correlation**: How correlation changes over time
- **Partial Correlation**: Controlling for market factor
- **Cross-Correlation**: Lead-lag relationships

**Applications**:
- Portfolio diversification
- Statistical arbitrage
- Risk management
- Sector rotation signals

### 6. Anomaly Detection

**Purpose**: Identify statistical deviations.

**Methods**:
- **Z-Score**: Returns > 2σ from mean
- **Bollinger Bands**: Price outside bands
- **RSI Extremes**: Overbought/oversold
- **Volume Spikes**: Unusual trading activity
- **News Sentiment**: Divergence from price

## CLI Commands

```bash
# Full quantitative analysis
ono-cli quant analyze <symbol> --period 5y

# Seasonal patterns only
ono-cli quant seasonality <symbol> --timeframe monthly

# Day-of-week analysis
ono-cli quant day-of-week <symbol>

# Event study
ono-cli quant event-study <symbol> --event earnings --window 5

# Factor analysis
ono-cli quant factors <symbol> --model fama-french-5

# Correlation matrix
ono-cli quant correlation <symbol1,symbol2,symbol3,...>

# Anomaly detection
ono-cli quant anomalies <symbol> --threshold 2sigma

# Backtest a pattern
ono-cli quant backtest <symbol> --strategy seasonal --entry-jan --exit-feb

# Institutional flow analysis
ono-cli quant institutional <symbol> --period 6m

# Options signal analysis
ono-cli quant options <symbol> --unusual-volume --sweeps
```

## Statistical Methods

### Significance Testing
- **T-Test**: For comparing means
- **Chi-Square**: For categorical patterns
- **Mann-Whitney U**: Non-parametric alternative
- **Bootstrap**: For confidence intervals

### Multiple Testing Correction
- **Bonferroni**: Conservative correction
- **False Discovery Rate (FDR)**: More lenient
- **Holm-Bonferroni**: Step-down procedure

### Time Series Analysis
- **Stationarity Tests**: ADF, KPSS
- **Autocorrelation**: ACF/PACF analysis
- **Regime Switching**: Hidden Markov Models

## Best Practices

### Do's ✅
- Use out-of-sample testing
- Apply multiple testing corrections
- Check for look-ahead bias
- Validate across different regimes
- Monitor for alpha decay
- Document all assumptions

### Don'ts ❌
- Don't data mine without validation
- Don't ignore transaction costs
- Don't overfit to historical data
- Don't ignore liquidity constraints
- Don't trade on spurious correlations
- Don't forget market impact

## Risk Management for Quant Strategies

### Model Risk
- **Decay Monitoring**: Track alpha over time
- **Regime Changes**: Detect when model stops working
- **Outlier Handling**: Robust statistics for anomalies

### Implementation Risk
- **Slippage Estimation**: Realistic fill prices
- **Liquidity Checks**: Ensure tradable size
- **Capacity Limits**: Maximum strategy size

### Operational Risk
- **Data Quality**: Clean, accurate data
- **System Reliability**: Redundant systems
- **Monitoring**: Real-time alerts

## Output Formats

### Quantitative Signal Card
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  QUANT SIGNAL: [SYMBOL]                   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  Primary Edge: [Pattern name]             ┃
┃  Confidence:   [High/Medium/Low]          ┃
┃  Significance: p < 0.05 ✅                ┃
┃  Win Rate:     XX% (X/X trades)           ┃
┃  Avg Return:   +X.X%                      ┃
┃  Sharpe:       X.XX                       ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  Current Signal: [Bullish/Bearish]        ┃
┃  Signal Age:   X days                     ┃
┃  Expected Hold: X days                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Related Skills

- **equity-research**: For fundamental context
- **technical-analysis**: For chart patterns
- **macro-research**: For regime context
- **financial-analysis-core**: For valuation context

## Data Requirements

### Essential Data
- OHLCV price data (daily minimum, intraday preferred)
- Corporate actions (splits, dividends)
- Earnings dates and estimates
- Insider trading data
- Institutional holdings
- Short interest

### Optional Data
- Options data
- News sentiment
- Social media sentiment
- Alternative data (credit cards, satellite, etc.)

## External Resources

- **Data Providers**: Polygon.io, Quandl, Bloomberg API
- **Research Papers**: SSRN, arXiv (q-fin)
- **Factor Libraries**: q-factor model, Fama-French
