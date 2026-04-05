---
name: easypaper-error-elimination-loop
description: Use when fixing mistakes from practice sessions permanently. Use for systematic error analysis, categorizing mistake types, creating micro-drills to eliminate recurring errors, or transforming wrong answers into learning opportunities. Essential for breaking patterns of repeated mistakes.
---

# Error Elimination Loop Skill

## Overview

**Transform every mistake into permanent learning through systematic error analysis.**

The Error Elimination Loop ensures you never make the same mistake twice. It analyzes every error from your practice sessions, identifies the root cause, assigns targeted micro-drills, and verifies elimination through re-testing.

**Core principle:** A mistake not analyzed is a mistake repeated.

**Runs:** After every practice session (Daily/Weekly trigger)

## When to Use

**Use this skill when:**
- You've completed a past paper and marked it
- You notice recurring mistakes on the same topic
- You're reviewing errors before an exam
- Weekly deep sessions (Error Elimination phase)
- You want to understand WHY you got something wrong

**Trigger:** Automatic after marking any paper, or command: *"Run error elimination"*

## The Error Elimination Process

```
Error Occurs
     ↓
Categorize Error Type
     ↓
Identify Root Cause
     ↓
Assign Micro-Drill
     ↓
Practice Correct Approach
     ↓
Re-Test (Verification)
     ↓
Error Eliminated ✓
```

## Error Categories

### Category 1: Conceptual Errors
**Definition:** Wrong understanding of the underlying physics/math

**Examples:**
- Thinking centripetal force points outward
- Confusing heat and temperature
- Misunderstanding derivative interpretation

**Elimination Strategy:**
1. Re-read textbook notes on concept
2. Watch explanation video
3. Complete 5 questions focusing ONLY on that concept
4. Explain concept aloud to verify understanding

### Category 2: Calculation Errors
**Definition:** Arithmetic, algebra, or unit mistakes

**Examples:**
- Sign errors (- becomes +)
- Calculator mistakes
- Unit conversion errors (cm → m)
- Power of 10 errors

**Elimination Strategy:**
1. Re-do calculation slowly with full working
2. Estimate answer first (order of magnitude check)
3. Practice 10 similar calculations
4. Use calculator's memory functions correctly

### Category 3: Careless Errors
**Definition:** Rushing, misreading, or skipping steps

**Examples:**
- Using wrong value from question
- Missing a part of a multi-part question
- Not converting units when required
- Wrong formula substitution

**Elimination Strategy:**
1. Create a "checklist" for that question type
2. Practice under timed conditions (build speed + accuracy)
3. Develop personal error-checking routine
4. Slow down on that question type

### Category 4: Exam Technique Errors
**Definition:** Understanding correct but marks lost on presentation

**Examples:**
- Not showing enough working
- Missing "hence" or "therefore" statements
- Wrong significant figures
- Not answering the exact question asked

**Elimination Strategy:**
1. Study mark scheme for exact phrasing required
2. Compare your answer to model answer
3. Practice writing "exam-style" responses
4. Memorize command word definitions

## The Error Elimination Workflow

### Step 1: Log the Error

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 ERROR LOG ENTRY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Date: 2024-03-08
Paper: 9702_w20_qp_12
Question: 3(b)
Topic: Gravitational Fields
Marks Lost: 2/3

Your Answer: g = GM/r² = 10 m/s² ❌
Correct Answer: g = 8 × 9.8 = 78 m/s² ✓
```

### Step 2: Categorize and Analyze

```
🔍 ERROR ANALYSIS:

Category: Calculation Error (specifically: incomplete substitution)

Root Cause Analysis:
   ❌ You stopped at the formula
   ❌ Didn't substitute the new mass and radius values
   ❌ Forgot that R' = R/2 means denominator becomes (R/2)² = R²/4

Why it happened:
   - Rushed through the question
   - Didn't write out substitution step explicitly
   - Mental math instead of written working

Pattern Check:
   → This is your 3rd error involving substitution
   → Pattern identified: Insufficient working shown
```

### Step 3: Assign Micro-Drill

```
🎯 MICRO-DRILL ASSIGNED:

Focus: Explicit substitution practice
Quantity: 10 questions requiring formula substitution
Source: 9702 past papers (similar gravitational field Qs)
Time: 15 minutes

Drill Structure:
   1. Write formula clearly
   2. Write substitution line (EVERY variable)
   3. Calculate step by step
   4. Box final answer with units

Questions downloaded to:
   → /drills/substitution_practice/
```

### Step 4: Complete the Drill

```
⏱️ DRILL SESSION: 15 minutes

Question 1/10: Gravitational field on Mars
   Formula: g = GM/R²
   Substitution: g = (6.67×10⁻¹¹)(6.42×10²³)/(3.39×10⁶)²
   Working: g = ...
   Answer: 3.71 m/s² ✓

Question 2/10: Gravitational field on Jupiter
   ...
```

### Step 5: Re-Test (Verification)

```
📋 RE-TEST: Original Question (9702_w20_qp_12 Q3)

Complete without looking at previous working:

Given: g_Earth = GM/R²
       M' = 2M, R' = R/2
Find: g_planet

Your working:
   g' = G(2M)/(R/2)²
      = 2GM / (R²/4)
      = 8GM/R²
      = 8 × 9.8
      = 78.4 ≈ 78 m/s² ✓✓✓

✅ ERROR ELIMINATED
   Time to elimination: 2 days
   Drill questions completed: 10/10
   Re-test: Correct
```

## Error Tracking Matrix

| Date | Paper | Q# | Error Type | Root Cause | Drill Assigned | Re-test Date | Status |
|------|-------|-----|------------|------------|----------------|--------------|--------|
| 03/08 | 9702_w20 | 3 | Calculation | No substitution | 10 substitution Qs | 03/10 | ✅ Fixed |
| 03/08 | 9702_w20 | 5 | Conceptual | Wrong force direction | Concept review + 5 Qs | 03/11 | 🔄 In Progress |
| 03/06 | 9702_s19 | 2 | Careless | Rushed reading | Checklist method | 03/09 | ✅ Fixed |

## Weekly Error Elimination Session (Sunday)

### Phase 1: Review Week's Errors (10 min)

```
📊 THIS WEEK'S ERROR SUMMARY:

Total errors: 12
By category:
   - Conceptual: 3 (25%)
   - Calculation: 5 (42%)
   - Careless: 4 (33%)

Recurring patterns:
   ⚠️ 3 substitution errors (trending up)
   ⚠️ 2 direction errors in circular motion (new pattern)
```

### Phase 2: Bulk Drill Assignment (30 min)

```
🎯 PRIORITY DRILLS FOR THIS WEEK:

Priority 1: Substitution errors (5 occurrences)
   → 20 substitution practice questions
   → Daily 10-min sessions

Priority 2: Circular motion direction confusion (3 occurrences)
   → 15 direction-focused questions
   → Force diagram practice

Priority 3: Careless reading (4 occurrences)
   → "Checklist method" for all future questions
```

### Phase 3: Re-Test Previous Errors (20 min)

```
📝 RE-TEST SESSION:

Testing 5 errors from last week:
   ✅ Q1 (Gravitational fields): Correct
   ✅ Q2 (Circular motion): Correct
   ❌ Q3 (Thermodynamics): Still wrong → Assign new drill
   ✅ Q4 (SHM): Correct
   ✅ Q5 (Electric fields): Correct

Elimination rate: 80% (4/5)
```

## Error Elimination Rate Tracking

Track your error elimination progress:

```
MONTHLY ERROR ELIMINATION REPORT:

Errors identified: 45
Errors re-tested: 45
Errors eliminated: 38 (84%)
Still recurring: 7 (16%)

Trend: ↗️ Improving
   Last month: 78% elimination
   This month: 84% elimination
   Target: 90% elimination

Top recurring issues (need attention):
   1. Unit conversions (still happening)
   2. Sign conventions in thermodynamics
```

## Common Error Patterns & Solutions

### Pattern 1: Sign Errors

**Frequency:** Very common in physics
**Solution:**
- Always draw vector arrows
- Define positive direction at start
- Check sign makes physical sense

**Drill:** 20 questions requiring sign attention

### Pattern 2: Unit Confusion

**Frequency:** Common in calculations
**Solution:**
- Convert ALL to SI at start
- Write units in every step
- Final answer units check

**Drill:** 15 questions with mixed units

### Pattern 3: Formula Selection

**Frequency:** Common in multi-topic questions
**Solution:**
- List all possible formulas
- Check what variables you have
- Eliminate formulas with missing variables

**Drill:** 10 "which formula?" identification exercises

### Pattern 4: Missing Working

**Frequency:** Loses method marks
**Solution:**
- Show every substitution
- Write formula before numbers
- Explain reasoning in words

**Drill:** Rewrite 10 answers with full working

## Integration with Other Skills

### Connection to Weakness Hunter

```
IF error rate on topic > 30%:
    → Mark topic as 🔴 Critical in Weakness Hunter
    → Increase drill frequency
```

### Connection to Spaced Mastery Cycle

```
Error identified today:
    → Micro-drill: Tomorrow
    → Re-test: +3 days
    → Verification: +1 week
    → Long-term check: +3 weeks
```

### Connection to Instant Resolver

```
IF stuck question leads to error:
    → Log error immediately
    → Assign drill before moving on
    → Don't just get answer—fix the gap
```

## Error Elimination Checklist

For every error logged, complete:

- [ ] Error categorized (Conceptual/Calculation/Careless/Technique)
- [ ] Root cause identified (be specific)
- [ ] Why it happened (honest assessment)
- [ ] Pattern checked (is this recurring?)
- [ ] Micro-drill assigned (specific quantity)
- [ ] Drill completed (with evidence)
- [ ] Re-test scheduled (within 3 days)
- [ ] Re-test passed (verified elimination)

## Success Metrics

The Error Elimination Loop is working when:
- ✅ Same error doesn't recur within 1 month
- ✅ Error elimination rate > 80%
- ✅ Students can articulate WHY they made errors
- ✅ Pattern recognition improves (catches errors before they happen)

## Example: Complete Error Elimination Session

```
Student: "I marked 9702_w20_qp_12 and got 62%"

Agent: Running Error Elimination Loop...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 ERROR ELIMINATION: Paper Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PAPER: 9702_w20_qp_12
SCORE: 31/50 (62%)
MARKS LOST: 19

ERROR BREAKDOWN:

❌ Q3(b) - Gravitational Fields (-2 marks)
   Your answer: g = 10 m/s²
   Correct: g = 78 m/s²
   
   Category: Calculation Error
   Root cause: Incomplete substitution
   Pattern: Yes—3rd substitution error this month
   
   🔧 ACTION: 10 substitution drills assigned
   📅 Re-test: 2 days

❌ Q5(a) - Circular Motion (-2 marks)
   Your answer: Tension = mv²/r
   Correct: Tension + mg = mv²/r
   
   Category: Conceptual Error
   Root cause: Forgot weight also acts toward center
   Pattern: Yes—2nd direction error
   
   🔧 ACTION: Concept review + 5 vertical circle Qs
   📅 Re-test: 3 days

❌ Q7(c) - Thermodynamics (-1 mark)
   Your answer: ΔU = Q + W
   Correct: ΔU = Q - W
   
   Category: Conceptual Error
   Root cause: Sign convention confusion
   Pattern: No—first occurrence
   
   🔧 ACTION: Review 1st Law notes
   📅 Re-test: 2 days

[Additional 4 errors...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY & ACTIONS:

Total errors: 7
By category:
   Conceptual: 3
   Calculation: 2
   Careless: 2

Drills assigned:
   • 20 substitution practice (Priority 1—recurring)
   • 15 circular motion direction (Priority 2—recurring)
   • 10 thermodynamics sign convention

All drills downloaded to /drills/this_week/
Re-tests scheduled for Thursday and Sunday.

NEXT: Complete drills before re-tests!
```

## The Elimination Mindset

```
❌ OLD MINDSET: "I got it wrong, I'll try to remember next time"
✅ NEW MINDSET: "I got it wrong, I'm going to ELIMINATE this error forever"

The difference:
   - Old: Hope-based, passive, vague
   - New: Systematic, active, measured

Every error is an opportunity to improve.
Every drill is a step toward exam perfection.
```
