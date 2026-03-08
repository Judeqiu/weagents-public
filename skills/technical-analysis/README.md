# Technical Analysis Skill

Professional-grade technical analysis for trading decisions.

## Overview

This skill provides institutional-quality technical analysis using quantitative methods to time entries and exits. Based on Citadel-grade analysis frameworks.

## Installation

```bash
# Install dependencies
pip install pandas numpy matplotlib ta-lib
```

## Quick Start

```bash
# Full technical analysis
ono-cli technical analyze AAPL

# Specific analysis types
ono-cli technical trend AAPL --timeframes daily,weekly
ono-cli technical levels AAPL
ono-cli technical indicators AAPL
ono-cli technical trade-plan AAPL --risk 2% --reward 6%
```

## Workflows

1. **Technical Deep Dive** - Complete analysis with trade plan
2. **Trend Analysis** - Multi-timeframe trend assessment
3. **Support/Resistance** - Key level identification
4. **Pattern Recognition** - Chart pattern detection

## Output Formats

- Technical report cards
- Trade plans with entry/exit/stop levels
- Risk/reward calculations
- Confidence ratings

## Examples

See `examples/` directory for sample outputs.
