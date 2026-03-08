# Quantitative Research Skill

Renaissance Technologies-style quantitative analysis for finding market edges.

## Overview

This skill uses data-driven statistical methods to identify patterns, anomalies, and quantifiable advantages in stock behavior.

## Installation

```bash
# Install dependencies
pip install pandas numpy scipy scikit-learn statsmodels matplotlib seaborn
```

## Quick Start

```bash
# Full quantitative analysis
ono-cli quant analyze AAPL --period 5y

# Specific analyses
ono-cli quant seasonality AAPL
ono-cli quant event-study AAPL --event earnings
ono-cli quant factors AAPL --model fama-french-5
ono-cli quant correlation AAPL,MSFT,GOOGL
ono-cli quant backtest AAPL --strategy seasonal
```

## Workflows

1. **Pattern Finder** - Comprehensive statistical analysis
2. **Seasonality Analysis** - Calendar-based patterns
3. **Event Study** - Reaction to specific events
4. **Factor Analysis** - Multi-factor exposure
5. **Anomaly Detection** - Statistical deviations

## Output Formats

- Quantitative research memos
- Statistical edge summaries
- Backtest results
- Factor exposure reports

## Examples

See `examples/` directory for sample outputs.
