# Financial Skills Index

A comprehensive guide to all financial analysis skills available to the OpenClaw agent (ono).

---

## Quick Reference

| Skill | Domain | Best For | Complexity |
|-------|--------|----------|------------|
| [financial-analysis-core](#1-financial-analysis-core) | Valuation | Excel models, DCF, Comps | Intermediate |
| [equity-research](#2-equity-research) | Stock Analysis | Earnings, screening, thesis | Beginner |
| [investment-banking](#3-investment-banking) | M&A Advisory | Buyer lists, CIMs, deals | Advanced |
| [private-equity](#4-private-equity) | Private Markets | LBO, deal sourcing, IC memos | Advanced |
| [technical-analysis](#5-technical-analysis) | Trading | Entry/exit timing, patterns | Intermediate |
| [quantitative-research](#6-quantitative-research) | Quant Analysis | Statistical edges, backtests | Advanced |
| [macro-research](#7-macro-research) | Strategy | Sector rotation, Fed policy | Intermediate |

---

## 1. financial-analysis-core

**Purpose**: Core valuation and financial modeling capabilities for investment banking, equity research, and corporate finance.

### When to Use

✅ **Use this skill for:**
- Building comparable company analysis (trading comps)
- Creating DCF valuation models
- Three-statement financial modeling
- Precedent transaction analysis
- Investment banking pitch materials

❌ **Don't use for:**
- Day-to-day trading decisions
- Real-time market timing
- Tax or legal advice

### Key Capabilities

| Function | Output | Description |
|----------|--------|-------------|
| Comparable Company Analysis | Excel workbook | Trading multiples, benchmarking vs peers |
| DCF Valuation | Excel model | Discounted cash flow with sensitivity tables |
| Financial Modeling | Excel models | Three-statement integrated models |
| Precedent Transactions | Excel workbook | Historical M&A deal multiples |

### Sample Agent Interactions

**Basic Comps Analysis**
```
Generate a comparable company analysis for Apple using Microsoft, 
Google, Amazon, and Meta as peers. Save the Excel file to /tmp/apple_comps.xlsx
```

**DCF Valuation**
```
Build a DCF model for NVIDIA with the following assumptions:
- 5-year forecast period
- WACC of 10%
- Terminal growth rate of 2.5%
- Output file: /tmp/nvda_dcf.xlsx
```

**Custom Comps with Specific Peers**
```
Run a comps analysis for Tesla (TSLA) comparing it to Ford, GM, 
Rivian, and Lucid Motors. Include EV/Revenue and P/E multiples.
```

**Full Valuation Package**
```
I need a complete valuation package for Microsoft:
1. Trading comps vs AMZN, GOOGL, AAPL, META
2. DCF model with base, bull, and bear cases
3. Save both files to /tmp/msft_valuation/
```

---

## 2. equity-research

**Purpose**: Equity research workflows for buy-side and sell-side analysis, including earnings updates, stock screening, and investment thesis development.

### When to Use

✅ **Use this skill for:**
- Analyzing earnings reports and guidance
- Initiating coverage on new stocks
- Developing bull/bear investment theses
- Screening for investment opportunities
- Tracking catalysts and events

❌ **Don't use for:**
- M&A transactions (use investment-banking)
- Private company analysis (use private-equity)
- Macro forecasting (use macro-research)

### Key Capabilities

| Function | Output | Description |
|----------|--------|-------------|
| Earnings Analysis | Research report | Post-earnings updates, guidance changes |
| Stock Screening | Candidate list | Filter stocks by criteria |
| Investment Thesis | Bull/bear case | Comprehensive investment view |
| Coverage Initiation | Full report | New stock coverage launch |
| Catalyst Tracking | Timeline | Events that could move the stock |
| Market Data | Price, profile | Real-time stock data via Polygon API |

### Sample Agent Interactions

**Get Stock Price**
```
What's the current stock price for NVIDIA (NVDA)? Show me the 
trading volume and daily change percentage too.
```

**Compare Multiple Stocks**
```
Compare the stock prices and performance of AAPL, MSFT, GOOGL, 
and AMZN. Which one is performing best today?
```

**Company Profile**
```
Get me the company profile for Tesla (TSLA). I want to know their 
market cap, number of employees, and what sector they operate in.
```

**Earnings Preview**
```
I'm analyzing Apple ahead of their earnings. Get me:
1. Current stock price and recent performance
2. Company profile and key metrics
3. Historical price action around past 4 earnings
```

**Stock Screening Request**
```
Screen for large-cap tech stocks with:
- Market cap > $500B
- P/E ratio < 30
- Positive revenue growth
- Dividend yield > 1%
```

**Investment Thesis Development**
```
Help me develop an investment thesis for Microsoft. I need:
1. Bull case with 3 key points
2. Bear case with 3 key risks
3. Current valuation context
4. 12-month price target range
```

---

## 3. investment-banking

**Purpose**: Investment banking advisory workflows including M&A analysis, pitch materials, confidential information memorandums (CIMs), and buyer list generation.

### When to Use

✅ **Use this skill for:**
- Sell-side M&A processes (selling a company)
- Buy-side M&A advisory (acquiring a company)
- Generating buyer lists (strategic and financial buyers)
- Creating pitch books and teasers
- Fairness opinions and valuation advisory

❌ **Don't use for:**
- Public equity research (use equity-research)
- Day-to-day corporate finance (use financial-analysis-core)
- Fund investment decisions (use private-equity)

### Key Capabilities

| Function | Output | Description |
|----------|--------|-------------|
| Buyer List Generation | CSV file | Strategic and financial buyer targets |
| CIM Creation | Document | Confidential Information Memorandum |
| Teaser Creation | One-pager | Anonymous deal marketing |
| M&A Modeling | Excel | Accretion/dilution analysis |
| Pitch Books | Presentation | Client pitch materials |

### Sample Agent Interactions

**Generate Buyer List - Software Company**
```
I'm advising a software company called "CloudTech" with $75M in 
revenue and $15M EBITDA. Generate a list of potential strategic 
and financial buyers.
```

**Healthcare M&A Targeting**
```
Create a buyer list for a healthcare services company named 
"MediCare Plus" with $200M revenue in the healthcare sector.
```

**Industrial Buyers**
```
Generate potential buyers for an industrial manufacturing company 
with $150M revenue and $30M EBITDA. Focus on both strategic 
acquirers and private equity firms.
```

**Sell-Side Process Setup**
```
We're preparing to sell a fintech company. Help me with:
1. Generate buyer list (software/ fintech focus)
2. Create a teaser one-pager outline
3. Draft CIM table of contents
```

**Buy-Side Target Screening**
```
We're a private equity firm looking at the software space. 
Generate buyer list analysis for a hypothetical $100M revenue 
SaaS company, then identify which strategic buyers would be 
most likely to pay a premium.
```

---

## 4. private-equity

**Purpose**: Private equity investing workflows including deal sourcing, leveraged buyout (LBO) modeling, due diligence, and investment committee (IC) memo preparation.

### When to Use

✅ **Use this skill for:**
- Deal sourcing and target screening
- LBO model building and return analysis
- Due diligence workstream management
- IC memo preparation
- Portfolio monitoring and value creation
- Exit planning and sale preparation

❌ **Don't use for:**
- Public equity analysis (use equity-research)
- Short-term trading (use technical-analysis)
- M&A sell-side advisory (use investment-banking)

### Key Capabilities

| Function | Output | Description |
|----------|--------|-------------|
| LBO Modeling | Excel model | Leveraged buyout returns analysis |
| Deal Sourcing | Target list | Investment opportunity screening |
| Due Diligence | Checklist | Pre-investment analysis tracker |
| IC Memos | Document | Investment committee presentations |
| Portfolio Monitoring | Dashboard | KPI tracking for portfolio companies |

### Sample Agent Interactions

**LBO Analysis Request**
```
Build an LBO model for a company with:
- Entry EV: $500M
- Revenue: $100M (growing 10% annually)
- EBITDA: $20M (20% margin)
- Debt: $300M (4x EBITDA)
- Equity: $200M
- Exit in 5 years at 8x EBITDA

What's the IRR and money-on-money multiple?
```

**Deal Screening**
```
I'm looking at industrial services companies. Help me screen for:
- $50M-$200M revenue range
- 15%+ EBITDA margins
- Strong recurring revenue
- Create a target list with rationale
```

**IC Memo Preparation**
```
Help me draft an investment committee memo for a potential 
platform acquisition in the healthcare sector. Include:
1. Executive summary
2. Investment thesis
3. Business overview
4. Financial analysis
5. Risks and mitigants
6. Returns analysis
7. Recommended terms
```

**Portfolio Company Review**
```
Create a portfolio monitoring template for tracking KPIs across 
my 3 portfolio companies (software, healthcare, industrial).
Include financial and operational metrics.
```

---

## 5. technical-analysis

**Purpose**: Professional-grade technical analysis for trading decisions using quantitative methods to time entries and exits. Based on Citadel-grade frameworks.

### When to Use

✅ **Use this skill for:**
- Identifying trend direction on multiple timeframes
- Finding key support and resistance levels
- Reading technical indicators (RSI, MACD, Bollinger Bands)
- Detecting chart patterns (head & shoulders, triangles, etc.)
- Creating trade plans with entry, stop-loss, and targets
- Calculating risk-to-reward ratios

❌ **Don't use for:**
- Long-term fundamental valuation (use financial-analysis-core)
- M&A analysis (use investment-banking)
- Macroeconomic forecasting (use macro-research)

### Key Capabilities

| Function | Output | Description |
|----------|--------|-------------|
| Trend Analysis | Report | Multi-timeframe trend assessment |
| Support/Resistance | Levels | Key price levels for trading |
| Technical Indicators | Values | RSI, MACD, moving averages, Bollinger Bands |
| Pattern Recognition | Patterns | Chart patterns and formations |
| Trade Planning | Plan | Entry, stop-loss, profit targets |
| Risk/Reward | Ratio | Position sizing calculations |

### Sample Agent Interactions

**Full Technical Analysis**
```
Perform a complete technical analysis for Apple (AAPL). I need:
1. Trend analysis (daily, weekly, monthly)
2. Key support and resistance levels
3. RSI, MACD, and Bollinger Bands
4. Any chart patterns detected
5. Fibonacci retracement levels
6. Complete trade plan with entry, stop, and targets
```

**Trade Setup Analysis**
```
Analyze the technical setup for NVIDIA (NVDA). I'm considering 
a long position. Show me:
1. Current trend direction
2. Key support levels for stop placement
3. Resistance levels for profit targets
4. Risk-to-reward ratio if I enter at current price
5. Your confidence rating (Strong Buy/Buy/Neutral)
```

**Support and Resistance Only**
```
Find the key support and resistance levels for Tesla (TSLA) 
using historical price action, moving averages, and volume profile.
```

**Technical Indicator Check**
```
Calculate the technical indicators for Microsoft (MSFT):
- RSI (14-period)
- MACD with signal line
- 50-day and 200-day moving averages
- Bollinger Bands (20-period, 2 std dev)

Interpret what these indicators are saying about the stock.
```

**Chart Pattern Detection**
```
Scan Amazon (AMZN) for chart patterns. Look for:
- Head and shoulders
- Cup and handle
- Triangles (ascending, descending, symmetrical)
- Double tops/bottoms

If any patterns are detected, provide the price target based 
on the pattern's measured move.
```

**Multi-Timeframe Trend Check**
```
Analyze the trend for AMD across daily, weekly, and monthly 
timeframes. Are they aligned or showing divergence? What's 
your overall trend assessment?
```

---

## 6. quantitative-research

**Purpose**: Renaissance Technologies-style quantitative analysis using statistical methods to find market edges, patterns, and alpha opportunities.

### When to Use

✅ **Use this skill for:**
- Finding seasonal patterns in stock returns
- Analyzing day-of-week effects
- Studying reactions to specific events (earnings, Fed meetings)
- Factor exposure analysis (value, momentum, quality)
- Correlation analysis between securities
- Detecting statistical anomalies
- Backtesting trading strategies

❌ **Don't use for:**
- Fundamental company analysis (use equity-research)
- Technical chart patterns (use technical-analysis)
- Subjective investment thesis development

### Key Capabilities

| Function | Output | Description |
|----------|--------|-------------|
| Seasonality Analysis | Report | Monthly/seasonal return patterns |
| Event Study | Analysis | Stock reaction to specific events |
| Factor Analysis | Exposures | Multi-factor model (Fama-French) |
| Correlation Matrix | Heatmap | Security relationships |
| Anomaly Detection | Alerts | Statistical deviations |
| Backtesting | Results | Strategy performance metrics |

### Sample Agent Interactions

**Comprehensive Quant Analysis**
```
Run a full quantitative analysis for Apple (AAPL) over the past 
5 years. I want to know:
1. Seasonal patterns - which months perform best/worst?
2. Day-of-week effects
3. Earnings reaction patterns
4. Factor exposures (beta, size, value, momentum)
5. Any statistical anomalies detected
6. Correlation with major market events
```

**Seasonality Study**
```
Analyze the seasonal patterns for NVDA over the past 10 years. 
Which months historically have the best returns? Is there 
statistical significance (p < 0.05)?
```

**Event Study - Earnings**
```
Perform an event study on Microsoft (MSFT) for earnings 
announcements. Analyze:
1. Pre-earnings drift (5 days before)
2. Earnings day reaction
3. Post-earnings drift (5 days after)
4. Win rate and average return
```

**Factor Exposure Analysis**
```
Calculate the factor exposures for Tesla (TSLA):
- Market beta
- Size factor
- Value factor
- Momentum factor
- Quality factor

What percentage of TSLA's returns are explained by these factors?
```

**Correlation Analysis**
```
Analyze the correlations between FAANG stocks (META, AAPL, AMZN, 
NFLX, GOOGL) over the past 2 years. Which pairs are most 
correlated? Which offer the best diversification?
```

**Anomaly Detection**
```
Scan for statistical anomalies in Bitcoin (BTC) price action 
over the past year using a 2-sigma threshold. Identify any 
volume spikes or price moves that were statistically unusual.
```

**Strategy Backtest**
```
Backtest a simple momentum strategy on the S&P 500:
- Buy when price crosses above 50-day MA
- Sell when price crosses below 50-day MA
- Period: Last 5 years
- Show me the Sharpe ratio, max drawdown, and win rate
```

---

## 7. macro-research

**Purpose**: McKinsey-level macroeconomic analysis for portfolio strategy, asset allocation, and sector rotation based on economic conditions.

### When to Use

✅ **Use this skill for:**
- Interest rate environment analysis and impact assessment
- Inflation trend analysis and sector implications
- Federal Reserve policy outlook
- Economic cycle positioning
- Sector rotation strategies
- Global risk assessment
- GDP growth forecasting
- Portfolio adjustments based on macro conditions

❌ **Don't use for:**
- Individual stock picking (use equity-research)
- Technical trading signals (use technical-analysis)
- Quantitative alpha strategies (use quantitative-research)

### Key Capabilities

| Function | Output | Description |
|----------|--------|-------------|
| Interest Rate Analysis | Report | Rate sensitivity, yield curve impact |
| Inflation Assessment | Analysis | Sector winners/losers, trajectory |
| Fed Policy Outlook | Forecast | Rate path, dot plot analysis |
| Sector Rotation | Recommendations | Cycle-based positioning |
| Global Risk Scan | Dashboard | Geopolitical and systemic risks |
| GDP Forecast | Outlook | Economic growth implications |

### Sample Agent Interactions

**Full Macro Assessment**
```
Provide a complete macro strategy briefing for my portfolio. 
I need to understand:
1. Current interest rate environment and impact on my holdings
2. Inflation trajectory and which sectors benefit/suffer
3. Fed policy outlook for next 6-12 months
4. Where we are in the economic cycle
5. Recommended sector allocation changes
6. Top 3 global risks to monitor
```

**Interest Rate Impact Analysis**
```
Analyze the impact of the current rate environment (Fed Funds 
at 5.25%, 10Y at 4.25%) on:
1. Growth stocks vs value stocks
2. Long duration assets
3. REITs and utilities
4. Financials

How should I adjust my portfolio if rates stay higher for longer?
```

**Inflation Sector Analysis**
```
With CPI at 3.2% and trending down, analyze which sectors are 
likely to benefit from disinflation and which might struggle. 
Provide specific ETF or stock recommendations for each category.
```

**Fed Policy Outlook**
```
What's the Fed likely to do over the next 4 meetings? Analyze:
1. Current Fed communications and tone
2. Market-implied probabilities
3. Economic data driving decisions
4. Scenario analysis (soft landing vs hard landing)
5. Portfolio implications of each scenario
```

**Sector Rotation Strategy**
```
Based on where we are in the economic cycle (late cycle heading 
toward potential recession), recommend:
1. Which sectors to overweight
2. Which sectors to underweight
3. Specific ETFs or stocks for each sector
4. Timeline for the rotation strategy
```

**Global Risk Assessment**
```
Scan for global macro risks that could impact my portfolio. 
Assess:
1. Geopolitical tensions
2. China economic slowdown
3. Supply chain risks
4. Energy market disruptions

For each risk, provide severity, probability, and portfolio 
hedging recommendations.
```

**Recession Probability Analysis**
```
What's the probability of a recession in the next 12 months? 
Analyze:
1. Yield curve signals
2. Leading economic indicators
3. Historical patterns
4. How my portfolio would perform in a recession
5. Defensive positioning recommendations
```

**Earnings Impact from Macro**
```
Given the current macro environment (rates, inflation, growth), 
assess the likely impact on S&P 500 earnings over the next 
4 quarters. Which sectors are most at risk? Which are resilient?
```

---

## Skill Selection Guide

### By Task Type

| If you need to... | Use this skill |
|-------------------|----------------|
| Value a company | financial-analysis-core |
| Get stock price/data | equity-research |
| Research a stock | equity-research |
| Screen for stocks | equity-research |
| Analyze earnings | equity-research |
| Generate buyer list | investment-banking |
| Create M&A materials | investment-banking |
| Build LBO model | private-equity |
| Write IC memo | private-equity |
| Time entry/exit | technical-analysis |
| Find support/resistance | technical-analysis |
| Check chart patterns | technical-analysis |
| Find seasonal patterns | quantitative-research |
| Run factor analysis | quantitative-research |
| Backtest strategy | quantitative-research |
| Assess macro impact | macro-research |
| Rotate sectors | macro-research |
| Analyze Fed policy | macro-research |

### By User Experience

**Beginner (Start Here)**
- equity-research - Stock prices, company profiles, earnings

**Intermediate**
- financial-analysis-core - Valuation models
- technical-analysis - Trading and timing
- macro-research - Economic analysis

**Advanced**
- investment-banking - M&A advisory
- private-equity - LBO and deal analysis
- quantitative-research - Statistical analysis

---

## Cross-Skill Workflows

Some analyses benefit from combining multiple skills:

### Complete Stock Research
```
1. equity-research: Get current price and profile
2. financial-analysis-core: Run comps and DCF
3. technical-analysis: Check entry timing
4. macro-research: Assess sector headwinds/tailwinds
```

### M&A Sell-Side Process
```
1. investment-banking: Generate buyer list
2. financial-analysis-core: Valuation analysis
3. private-equity: LBO analysis for PE buyers
4. macro-research: Market timing for process launch
```

### Quantitative Trading Strategy
```
1. quantitative-research: Find statistical edge
2. technical-analysis: Fine-tune entry/exit
3. macro-research: Avoid macro headwinds
4. equity-research: Check fundamentals
```

---

## Tips for Effective Agent Interactions

### Be Specific
✅ "Generate a DCF for Apple with 5-year forecast, 9% WACC, 2.5% terminal growth"
❌ "Value Apple"

### Provide Context
✅ "I'm considering a long position in NVDA for 3-6 months"
❌ "Analyze NVDA"

### Request Specific Outputs
✅ "Save the Excel file to /tmp/analysis.xlsx and show me a summary"
❌ "Create a model"

### Multi-Step Requests
✅ "First get the stock price, then run comps, then give me your investment view"
❌ "Analyze this stock completely"

### Clarify Timeframes
✅ "Show me monthly seasonality patterns over 10 years"
❌ "Check seasonality"

---

*Last Updated: March 2026*
