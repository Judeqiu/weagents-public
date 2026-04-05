# Daily Check-in Workflow

**Duration:** 5-10 minutes  
**Frequency:** Every day  
**Trigger:** Student says "Morning Agent"

## Purpose

The daily check-in maintains momentum, provides structure, and ensures no gaps develop. It's the heartbeat of the Mastery Agent system.

## Agent Response Flow

```
Student: "Morning Agent"
   ↓
Agent checks (in order):
   1. Any 🔴 Critical topics needing drills?
   2. Any spaced reviews due today?
   3. Any unfixed errors from yesterday?
   4. New papers to attempt?
   ↓
Agent generates personalized plan
```

## Decision Tree

```
IF Critical topics with score < 50% exist:
    → Assign 20-min weakness drill
    
ELIF Spaced review is due today:
    → Assign re-attempt paper/question set
    → Specify review type (1W/3W/6W)
    
ELIF Errors from last session not yet fixed:
    → Assign Error Elimination micro-drill
    → Specify drill questions
    
ELIF No urgent items:
    → "Upload any stuck question for Instant Resolver"
    → OR suggest light topic review
```

## Example Responses

### Scenario 1: Critical Topic Drill

```
📅 MONDAY, MARCH 8 - YOUR DAILY PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 TODAY'S FOCUS: Weakness Drill

Topic: Circular Motion (Current: 45% - 🔴 Critical)
Papers: 9702_s19_qp_11, 9702_w18_qp_12

📋 TASKS:
   1. Complete Q2, Q6 from 9702_s19_qp_11 (15 min)
   2. Check answers with mark scheme (5 min)
   3. Log any errors in Error Log

💡 TIP: Focus on drawing force diagrams first.
   Common error: Forgetting weight acts downward too.

📊 THIS WEEK:
   • Tuesday: Spaced review - Thermodynamics
   • Wednesday: Error elimination session
   • Thursday: New paper - 9702_w21_qp_12
   • Sunday: Weekly deep session (90 min)

Progress: 67% topics at mastery (▲ 5% from last month)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Scenario 2: Spaced Review Due

```
📅 TUESDAY, MARCH 9 - YOUR DAILY PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔁 TODAY'S FOCUS: 3-Week Spaced Review

Paper: 9702_w20_qp_12
Type: Full re-attempt, closed book
Initial score: 84%
Target: 85%+

⏱️  TIME: 75 minutes (full exam conditions)

📋 REQUIREMENTS:
   • No notes, no mark scheme
   • Timed strictly
   • Fresh copy (or cover your previous working)

📊 AFTER COMPLETION:
   1. Self-mark with mark scheme
   2. Log any errors
   3. Report score to Agent

💡 REMINDER: This tests TRUE mastery (not memory).
   If score drops below 80%, topic goes back to drills.

📅 UPCOMING:
   • Tomorrow: Weakness drill - Gravitational Fields
   • Thursday: 1-week review of 9702_s21_qp_11
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Scenario 3: Error Elimination

```
📅 WEDNESDAY, MARCH 10 - YOUR DAILY PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 TODAY'S FOCUS: Error Elimination

You have 3 unaddressed errors from Monday's paper:

1. Q3(b) - Substitution error (Calculation)
   → Drill: 10 substitution practice questions
   → Folder: /drills/substitution/
   
2. Q5(a) - Direction confusion (Conceptual)
   → Drill: 5 vertical circular motion Qs
   → Folder: /drills/circular_motion/
   
3. Q7(c) - Sign convention (Conceptual)
   → Drill: Review thermodynamics notes
   → Re-test: 9702_s19_qp_11 Q4

⏱️  TIME: 30 minutes

✅ SUCCESS CRITERIA:
   All drills completed → Schedule re-test for Friday

📅 UPCOMING:
   • Thursday: Spaced review
   • Friday: Re-test errors
   • Sunday: Weekly deep session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Scenario 4: No Urgent Items

```
📅 THURSDAY, MARCH 11 - YOUR DAILY PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ ALL CAUGHT UP!

No critical drills, reviews, or errors pending.

💡 OPTIONS FOR TODAY:

Option 1: Upload a stuck question
   → Working on homework? Past paper? Textbook?
   → Photo upload → Instant solution

Option 2: Light topic review
   → Quick 15-min recap of 🟢 mastered topic
   → Keep it fresh for exam day

Option 3: Preview upcoming paper
   → Sunday's paper: 9702_w21_qp_13
   → Skim questions (don't solve yet)

📊 YOUR STATUS:
   • Topics at mastery: 12/18 (67%)
   • Papers this month: 6
   • Error elimination rate: 84%

Great work maintaining consistency! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Student Actions

After receiving daily plan:

1. **Read completely** - Don't skim
2. **Gather materials** - Papers, mark schemes, drill questions
3. **Set timer** - Stick to allocated time
4. **Complete tasks** - Follow the plan
5. **Report back** - Tell Agent what you completed
6. **Log errors** - If any occurred

## Agent Follow-up

End of day check (optional):

```
Student: "Daily check-in complete"

Agent: Great! Summary:
   ✅ Drill completed: Circular Motion (2 questions)
   ✅ Errors: 0 new errors
   ✅ Score: 100% on drill

Tomorrow: Spaced review - Thermodynamics
Keep it up! 🎉
```

## Consistency Tracking

| Day | Check-in | Tasks Completed | Notes |
|-----|----------|-----------------|-------|
| Mon | ⬜ | / | |
| Tue | ⬜ | / | |
| Wed | ⬜ | / | |
| Thu | ⬜ | / | |
| Fri | ⬜ | / | |
| Sat | ⬜ | / | |
| Sun | ⬜ | / | |

**Weekly target:** 7/7 days

## Missed Day Protocol

If student misses a day:

```
Agent: You missed yesterday's check-in.

Priority catch-up:
   1. Complete yesterday's drill (if any) - 20 min
   2. Today's scheduled item - 20 min
   3. If overwhelmed, focus on Critical topics only

Don't double up on everything—prioritize!
```

## Motivation Boosters

Include occasionally:

```
📈 PROGRESS SPOTLIGHT:
   Circular Motion: 45% → 62% this month!
   One more week and you'll hit mastery. 💪

🏆 MILESTONE:
   You've completed 50 papers—top 5% of students!

💡 QUOTE:
   "Consistency is more important than intensity."
```
