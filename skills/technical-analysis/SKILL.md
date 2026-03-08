---
name: technical-analysis
description: "Technical analysis and chart pattern recognition for trading decisions. Uses Citadel-grade quantitative methods combining technical indicators, statistical models, and price action analysis. Use for entry/exit timing, trend identification, support/resistance levels, and trade plan development."
metadata:
  category: "technical-analysis"
  domains: ["trading", "chart-patterns", "technical-indicators", "price-action"]
  outputs: ["technical-reports", "trade-plans", "chart-analysis", "pattern-recognition"]
  requires:
    bins: ["python3"]
    python_packages: ["pandas", "numpy", "matplotlib", "ta-lib"]
    skills: ["equity-research"]
---

# Technical Analysis

Professional-grade technical analysis using quantitative methods to time entries and exits.

## When to Use

✅ **Use this skill for:**

- **Trend Analysis**: Identify trend direction on multiple timeframes
- **Support/Resistance**: Find key price levels for entries and exits
- **Technical Indicators**: RSI, MACD, Bollinger Bands interpretation
- **Chart Patterns**: Head and shoulders, cup and handle, triangles
- **Trade Planning**: Entry prices, stop-losses, profit targets
- **Risk/Reward Analysis**: Calculate position sizing and risk metrics

❌ **Don't use for:**

- Long-term fundamental valuation (use financial-analysis-core)
- M&A analysis (use investment-banking)
- Macroeconomic forecasting (use macro-research)

## Quick Reference

| Task | Tool/Workflow | Output |
|------|---------------|--------|
| Trend analysis | `analyze-trend.py` | Trend direction report |
| Support/resistance | `find-levels.py` | Key price levels |
| Technical indicators | `calculate-indicators.py` | Indicator values |
| Pattern recognition | `detect-patterns.py` | Pattern matches |
| Trade plan | `generate-trade-plan.py` | Complete trade setup |
| Full analysis | `technical-deep-dive` workflow | Comprehensive report |

## Core Workflows

### 1. Technical Analysis Deep Dive (Citadel-Style)

**Purpose**: Complete technical breakdown of a stock for trading decisions.

#### Analysis Components:

```
TECHNICAL ANALYSIS REPORT: [SYMBOL]
Date: [Date] | Analyst: [Name]

═══════════════════════════════════════════════════════════════
1. TREND ANALYSIS
═══════════════════════════════════════════════════════════════

Daily Trend:   [Bullish/Bearish/Neutral] - [Evidence]
Weekly Trend:  [Bullish/Bearish/Neutral] - [Evidence]
Monthly Trend: [Bullish/Bearish/Neutral] - [Evidence]

Trend Strength: [Strong/Moderate/Weak]
Trend Alignment: [All timeframes aligned/Mixed signals]

═══════════════════════════════════════════════════════════════
2. KEY LEVELS
═══════════════════════════════════════════════════════════════

Support Levels:
  - S1: $XX.XX (50-day MA)
  - S2: $XX.XX (Previous low)
  - S3: $XX.XX (200-day MA)

Resistance Levels:
  - R1: $XX.XX (Recent high)
  - R2: $XX.XX (52-week high)
  - R3: $XX.XX (Psychological level)

Current Price: $XX.XX
Distance to Support: X%
Distance to Resistance: X%

═══════════════════════════════════════════════════════════════
3. TECHNICAL INDICATORS
═══════════════════════════════════════════════════════════════

Moving Averages:
  - 50-day MA:  $XX.XX [Above/Below] price
  - 100-day MA: $XX.XX [Above/Below] price
  - 200-day MA: $XX.XX [Above/Below] price
  
  Golden Cross / Death Cross: [Yes/No - details]

RSI (14): XX [Overbought(>70)/Neutral/Oversold(<30)]
  Interpretation: [Plain English explanation]

MACD:
  - MACD Line: XX
  - Signal Line: XX
  - Histogram: XX [Bullish/Bearish] crossover
  
Bollinger Bands:
  - Upper: $XX.XX
  - Middle: $XX.XX (20-day MA)
  - Lower: $XX.XX
  - Position: [Near upper/Near middle/Near lower/Breaking out]

Volume Analysis:
  - Current Volume: XX vs Avg: XX
  - Trend: [Increasing/Decreasing/Normal]
  - Interpretation: [Confirms/Contradicts] price action

═══════════════════════════════════════════════════════════════
4. CHART PATTERNS
═══════════════════════════════════════════════════════════════

Detected Patterns:
  [ ] Head and Shoulders - [Target: $XX.XX]
  [ ] Cup and Handle - [Target: $XX.XX]
  [ ] Double Top/Bottom - [Target: $XX.XX]
  [ ] Triangle (Ascending/Descending/Symmetrical)
  [ ] Flag/Pennant
  [ ] Wedges
  
Pattern Reliability: [High/Medium/Low]
Pattern Completion: [XX%]

═══════════════════════════════════════════════════════════════
5. FIBONACCI ANALYSIS
═══════════════════════════════════════════════════════════════

Retracement Levels from [High: $XX.XX] to [Low: $XX.XX]:
  - 23.6%: $XX.XX [Current position/Support/Resistance]
  - 38.2%: $XX.XX
  - 50.0%: $XX.XX
  - 61.8%: $XX.XX [Golden ratio - key level]
  - 78.6%: $XX.XX

Extension Targets (if breakout):
  - 127.2%: $XX.XX
  - 161.8%: $XX.XX

═══════════════════════════════════════════════════════════════
6. TRADE PLAN
═══════════════════════════════════════════════════════════════

Recommended Setup: [Long/Short/Wait]

Entry Strategy:
  - Ideal Entry: $XX.XX - $XX.XX
  - Entry Trigger: [Specific condition]
  - Alternative Entry: $XX.XX

Stop Loss:
  - Stop Level: $XX.XX
  - Stop Type: [Hard stop/Trailing/Technical level]
  - Risk per Share: $X.XX (X%)

Profit Targets:
  - Target 1 (Conservative): $XX.XX (R:R = 1:X)
  - Target 2 (Moderate): $XX.XX (R:R = 1:X)
  - Target 3 (Aggressive): $XX.XX (R:R = 1:X)

Position Sizing:
  - Risk Amount: $X,XXX (X% of portfolio)
  - Position Size: XXX shares
  - Position Type: [Full/Half/Quarter]

Risk-to-Reward Ratio: 1:X

═══════════════════════════════════════════════════════════════
7. CONFIDENCE RATING
═══════════════════════════════════════════════════════════════

Overall Rating: [Strong Buy / Buy / Neutral / Sell / Strong Sell]

Confidence Factors:
  ✅ [Positive factor 1]
  ✅ [Positive factor 2]
  ⚠️ [Risk factor 1]
  ⚠️ [Risk factor 2]

Conviction Level: [High/Medium/Low] - [Explanation]

═══════════════════════════════════════════════════════════════
8. SUMMARY & ACTION PLAN
═══════════════════════════════════════════════════════════════

Key Takeaways:
  1. [Most important insight]
  2. [Second key point]
  3. [Third key point]

Recommended Action:
  [Clear action with price levels and conditions]

Risk Management:
  - Maximum position size: X%
  - Time stop: [Exit if not moving by date]
  - Re-evaluation trigger: [Price level or event]

Next Review: [Date/Trigger]
```

### 2. Multi-Timeframe Trend Analysis

**Purpose**: Determine trend alignment across timeframes.

**Timeframes to Analyze**:
1. **Daily**: Primary trading timeframe
2. **Weekly**: Intermediate trend
3. **Monthly**: Long-term trend

**Trend Classification**:
- **Strong Bullish**: All timeframes bullish, aligned
- **Bullish**: Daily bullish, weekly/monthly neutral or bullish
- **Neutral**: Mixed signals or sideways
- **Bearish**: Daily bearish, weekly/monthly neutral or bearish
- **Strong Bearish**: All timeframes bearish, aligned

### 3. Support and Resistance Identification

**Purpose**: Find key price levels for trading decisions.

**Methodology**:
1. **Historical highs/lows**: Previous significant turning points
2. **Moving averages**: 50-day, 100-day, 200-day as dynamic S/R
3. **Psychological levels**: Round numbers ($100, $150, etc.)
4. **Volume profile**: High volume nodes
5. **Fibonacci levels**: 38.2%, 50%, 61.8% retracements

### 4. Technical Indicator Toolkit

**Momentum Indicators**:
- RSI (14): Overbought (>70), Oversold (<30)
- MACD: Trend direction and momentum shifts
- Stochastic: Short-term momentum

**Volatility Indicators**:
- Bollinger Bands: Volatility and mean reversion
- ATR: Average True Range for stop placement
- Keltner Channels: Trend following with volatility

**Trend Indicators**:
- Moving Averages: 50/100/200-day
- ADX: Trend strength measurement
- Parabolic SAR: Trend following stops

**Volume Indicators**:
- OBV: On-Balance Volume
- Volume Profile: Support/resistance levels
- VWAP: Volume Weighted Average Price

## CLI Commands

```bash
# Analyze trend for a stock
ono-cli technical trend <symbol> --timeframes daily,weekly,monthly

# Find support/resistance levels
ono-cli technical levels <symbol>

# Calculate technical indicators
ono-cli technical indicators <symbol>

# Detect chart patterns
ono-cli technical patterns <symbol>

# Generate complete trade plan
ono-cli technical trade-plan <symbol> --risk 2% --reward 6%

# Full technical deep dive
ono-cli technical analyze <symbol> --full
```

## Best Practices

### Do's ✅
- Always use multiple timeframes for confirmation
- Wait for price confirmation before entering
- Use stops based on technical levels, not arbitrary percentages
- Consider volume as confirmation of price action
- Update analysis as new price data arrives

### Don'ts ❌
- Don't trade against the major trend without confirmation
- Don't ignore volume signals
- Don't use technical analysis in isolation (consider fundamentals)
- Don't chase breakouts without volume confirmation
- Don't move stops further away from entry

## Risk Management

### Position Sizing Formula
```
Position Size = Risk Amount / (Entry Price - Stop Price)

Where:
- Risk Amount = Portfolio Value × Risk % (typically 1-2%)
- Entry Price = Planned entry
- Stop Price = Technical stop level
```

### Risk-to-Reward Guidelines
- **Minimum acceptable**: 1:2 (risk $1 to make $2)
- **Good setup**: 1:3
- **Excellent setup**: 1:4 or higher

### Stop Loss Placement
- Below support for longs (with buffer)
- Above resistance for shorts (with buffer)
- Use ATR for volatility-based stops
- Never risk more than 1-2% of portfolio per trade

## Output Formats

### Technical Report Card
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECHNICAL REPORT CARD: [SYMBOL]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Trend        : [📈 Bullish / 📉 Bearish / ➡️ Neutral]
Strength     : [Strong/Moderate/Weak]
RSI          : XX [🟢/🟡/🔴]
MACD         : [Bullish/Bearish] crossover
Volume       : [Above/Below] average
Pattern      : [Pattern name or None]

Key Levels:
  Resistance : $XX.XX | $XX.XX | $XX.XX
  Support    : $XX.XX | $XX.XX | $XX.XX

Trade Setup:
  Entry      : $XX.XX
  Stop Loss  : $XX.XX (X%)
  Target 1   : $XX.XX (R:R 1:X)
  Target 2   : $XX.XX (R:R 1:X)

Rating       : [Strong Buy/Buy/Neutral/Sell/Strong Sell]
Confidence   : [High/Medium/Low]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Related Skills

- **equity-research**: For fundamental context alongside technicals
- **financial-analysis-core**: For valuation context
- **quantitative-research**: For statistical edges and pattern recognition
- **macro-research**: For broader market context

## External Resources

- **Market Data**: Polygon.io API (via equity-research skill)
- **Charting**: Consider integration with TradingView or similar
- **Data Provider**: Ensure access to OHLCV data for calculations
