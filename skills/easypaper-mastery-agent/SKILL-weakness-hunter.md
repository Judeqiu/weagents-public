---
name: easypaper-weakness-hunter
description: Use when diagnosing knowledge gaps in exam preparation. Use for systematic topic analysis, calculating mastery percentages, identifying critical weak areas, or generating prioritized study lists based on past paper performance. Essential for monthly audits and tracking improvement over time.
---

# Weakness Hunter Skill

## Overview

**Systematic diagnosis of knowledge gaps through data-driven topic analysis.**

The Weakness Hunter analyzes your past paper performance to identify exactly where you're losing marks. It transforms vague feelings of "I'm bad at physics" into actionable data: "Circular Motion mastery: 45%—prioritize this topic."

**Core principle:** You can't fix what you haven't measured. This skill provides the measurement.

**Runs:** Every 4 weeks (Monthly Audit) or on demand

## When to Use

**Use this skill when:**
- Starting exam prep and need a baseline assessment
- Monthly progress reviews (1st weekend of each month)
- After completing 3+ papers on a subject
- Planning topic prioritization for intensive study
- Feeling unsure which topics need attention

**Output:** Ranked list of weak topics with specific mastery scores

## The Weakness Hunter Process

```
Step 1: Collect Data → Step 2: Score Topics → Step 3: Rank & Prioritize
        ↓                    ↓                       ↓
   Past paper results    Calculate % per topic    Color-coded matrix
```

### Step 1: Data Collection

For each paper completed, record:
- Paper code (e.g., 9702_w20_qp_12)
- Topic for each question
- Marks obtained / Total marks

**Minimum data needed:** 3 papers per subject for reliable scoring

### Step 2: Topic Scoring Formula

```
Topic Mastery % = (Total marks earned in topic) / (Total marks available in topic) × 100

Categories:
- 🟢 Mastery: 80-100%
- 🟡 Developing: 50-79%
- 🔴 Critical: <50%
```

### Step 3: Priority Ranking

Topics are ranked by:
1. **Mastery %** (lowest first—biggest gaps)
2. **Exam weight** (high-weight topics prioritized)
3. **Time until exam** (closer = higher priority)

## Quick Reference: Weakness Hunter Commands

| Command | Action |
|---------|--------|
| `"Run weakness hunter on [subject]"` | Full analysis for one subject |
| `"Run full weakness audit"` | Analyze all subjects |
| `"Show my critical topics"` | List only 🔴 Critical topics |
| `"What's my weakest topic?"` | Single lowest-scoring topic |

## Implementation: Monthly Audit

### Phase 1: Paper Collection

```python
# Gather all papers completed this month
papers_this_month = [
    "9702_w20_qp_12",
    "9702_s19_qp_11", 
    "9702_w18_qp_12",
    # ... all papers completed
]

# Extract marks per topic
topic_scores = {
    "Circular Motion": {"earned": 9, "total": 20},
    "Thermodynamics": {"earned": 18, "total": 25},
    "Waves": {"earned": 27, "total": 30},
    # ... etc
}
```

### Phase 2: Calculate Mastery Matrix

```
┌─────────────────────┬──────────┬────────┬───────┬────────┐
│ Topic               │ Attempted│ Correct│   %   │ Status │
├─────────────────────┼──────────┼────────┼───────┼────────┤
│ Circular Motion     │    20    │    9   │  45%  │  🔴    │
│ Gravitational Fields│    16    │    6   │  38%  │  🔴    │
│ Thermodynamics      │    25    │   18   │  72%  │  🟡    │
│ Electric Fields     │    25    │   18   │  72%  │  🟡    │
│ Waves               │    30    │   27   │  90%  │  🟢    │
│ Superposition       │    20    │   17   │  85%  │  🟢    │
└─────────────────────┴──────────┴────────┴───────┴────────┘
```

### Phase 3: Generate Action Plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 WEAKNESS HUNTER RESULTS: Physics (9702)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRITICAL TOPICS (Immediate Action Required):
   1. Gravitational Fields: 38%
      → Target: 70% by end of month
      → Action: 40 questions + mark scheme study
      
   2. Circular Motion: 45%
      → Target: 70% by end of month
      → Action: 30 questions + concept review

🟡 DEVELOPING TOPICS (Maintain Progress):
   3. Thermodynamics: 72%
      → Target: 80% by end of month
      → Action: 20 questions to solidify
      
   4. Electric Fields: 72%
      → Target: 80% by end of month
      → Action: Continue current practice

🟢 MASTERED TOPICS (Spaced Review Only):
   ✓ Waves: 90%
   ✓ Superposition: 85%
   → Review every 3 weeks to maintain

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Topic-Specific Drill Assignment

For each Critical topic, the Weakness Hunter assigns:

| Topic Score | Daily Drill | Duration |
|-------------|-------------|----------|
| <50% (🔴) | 20 questions/day | 3-4 weeks |
| 50-70% (🟡→🔴) | 15 questions/day | 2-3 weeks |
| 70-80% (🟡) | 10 questions/day | 1-2 weeks |
| 80%+ (🟢) | Review only | Every 3 weeks |

## Tracking Template

### Weakness Hunter Matrix (Update Monthly)

| Subject | Topic | Attempted | Correct | % | Status | Target % | Deadline |
|---------|-------|-----------|---------|---|--------|----------|----------|
| 9702 | Circular Motion | 20 | 9 | 45% | 🔴 | 70% | 04/01 |
| 9702 | Thermodynamics | 25 | 18 | 72% | 🟡 | 80% | 04/01 |
| 9702 | Waves | 30 | 27 | 90% | 🟢 | 85% | 04/01 |
| 9709 | Integration | 15 | 12 | 80% | 🟢 | 85% | 04/01 |

## CAIE A-Level Topic Weight Reference

### Physics (9702) - Major Topics
| Topic | Approx. Weight | Priority if Critical |
|-------|---------------|---------------------|
| Mechanics (Circular, Gravitation) | 20% | 🔥 Highest |
| Thermal Physics | 12% | 🔥 Highest |
| Waves & Superposition | 15% | High |
| Electricity | 18% | 🔥 Highest |
| Modern Physics | 20% | 🔥 Highest |
| Practical Skills | 15% | Medium |

### Mathematics (9709) - Major Topics
| Topic | Approx. Weight | Priority if Critical |
|-------|---------------|---------------------|
| Pure Math (P1-3) | 60% | 🔥 Highest |
| Mechanics (M1-2) | 20% | High |
| Statistics (S1-2) | 20% | High |

## Common Mistakes

| Mistake | Why It Hurts | Fix |
|---------|--------------|-----|
| Estimating scores | Inaccurate data → wrong priorities | Use exact mark schemes |
| Too few papers | Unreliable scoring | Minimum 3 papers per subject |
| Ignoring 🔴 topics | Gaps persist into exam | Drill Critical topics daily |
| Focusing only on weak areas | Mastered topics fade | Schedule spaced review |
| Not updating monthly | Data gets stale | Set 1st weekend audit reminder |

## Integration with Other Skills

### Outputs to Spaced Mastery Cycle
```
🟢 Mastery topics → Schedule 3-week review
🟡 Developing topics → Schedule 1-week review
🔴 Critical topics → Daily drill until 70%
```

### Outputs to Error Elimination Loop
```
🔴 Critical topics → Flag for error analysis
    ("Why are you getting 45%? Let's examine the errors.")
```

### Outputs to Instant Resolver
```
When stuck question uploaded:
Agent checks: "Is this topic Critical?"
If yes → Add to priority drill list
```

## Example: Complete Weakness Hunter Session

```
Student: "Run weakness hunter on Physics"

Agent: Gathering your Physics paper data...

Found:
- 9702_w20_qp_12 (completed 03/01)
- 9702_s19_qp_11 (completed 03/03)
- 9702_w18_qp_12 (completed 03/06)

Analyzing 85 questions across 12 topics...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 WEAKNESS HUNTER RESULTS: Physics (9702)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERVIEW:
Topics at Mastery:        7/12 (58%)
Topics Developing:        3/12 (25%)
Critical Topics:          2/12 (17%)

🔴 CRITICAL (Require immediate attention):
   1. Gravitational Fields (38%)
      Papers: 9702_w20_qp_12 Q3, 9702_s19_qp_11 Q5, Q7
      Common errors: Confused g = GM/r² with orbital velocity
      
   2. Circular Motion (45%)
      Papers: 9702_w18_qp_12 Q2, Q6
      Common errors: Forgot centripetal force direction

🟡 DEVELOPING (Maintain progress):
   3. Thermodynamics (72%)
   4. Electric Fields (72%)
   5. Capacitance (68%)

🟢 MASTERED (Spaced review only):
   ✓ Waves (90%)
   ✓ Superposition (85%)
   ✓ SHM (82%)
   ✓ etc.

RECOMMENDED ACTIONS:
1. This week: 20 Gravitational Fields questions daily
2. Next week: 20 Circular Motion questions daily
3. Schedule: Thermodynamics review in 1 week

I'll update your daily plans with these priorities. Say "Morning Agent" tomorrow to begin!
```

## Success Metrics

A successful Weakness Hunter implementation:
- ✅ Identifies ALL topics below 50% (no hidden gaps)
- ✅ Tracks progress month-to-month
- ✅ Prioritizes high-weight exam topics
- ✅ Drives daily drill assignments
- ✅ Celebrates topics reaching Mastery (80%+)
