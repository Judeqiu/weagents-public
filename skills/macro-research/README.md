# Macro Research Skill

McKinsey-level macroeconomic analysis for portfolio strategy.

## Overview

This skill provides comprehensive macroeconomic research to evaluate how economic trends, policy decisions, and global factors affect equity markets and portfolio positioning.

## Installation

```bash
# Install dependencies
pip install pandas numpy matplotlib
```

## Quick Start

```bash
# Full macro assessment
ono-cli macro analyze --portfolio myportfolio

# Specific analyses
ono-cli macro rates --current 5.25 --scenario +100bps
ono-cli macro inflation --current-cpi 3.2 --target 2.0
ono-cli macro sectors --cycle-phase mid
ono-cli macro fed --meetings 4
ono-cli macro risks
```

## Workflows

1. **Macro Impact Assessment** - Full strategy briefing
2. **Interest Rate Analysis** - Rate sensitivity and impact
3. **Inflation Assessment** - Sector winners/losers
4. **Sector Rotation** - Cycle-based positioning
5. **Global Risk Scan** - Geopolitical and systemic risks

## Output Formats

- Macro strategy briefings
- Sector rotation recommendations
- Policy impact assessments
- Economic outlooks

## Examples

See `examples/` directory for sample outputs.
