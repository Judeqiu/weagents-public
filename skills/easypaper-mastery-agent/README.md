# EasyPaper Mastery Agent

A unified proactive study agent for A-Level, IGCSE, IB, and AP exam preparation. This 5-skill cluster creates a complete 360° system that acquires resources, diagnoses gaps, solves problems instantly, fixes mistakes permanently, and builds long-term retention.

## The 5-Skill Architecture

```
                    ┌─────────────────┐
                    │  1. Downloader  │ ← easypaper-pdf-finder
                    │     Skill       │   (existing skill)
                    └────────┬────────┘
                             │ (feeds papers)
                             ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   5. Spaced  │◄────►│  2. Weakness │─────►│  3. Error    │
│   Mastery    │      │   Hunter     │      │ Elimination  │
│   Cycle      │      │   Skill      │      │    Loop      │
└──────┬───────┘      └──────────────┘      └──────┬───────┘
       ▲                                            │
       │                                            │
       └────────────────────────────────────────────┘
                        (feeds corrected topics)
                             ▲
                             │
                    ┌────────┴────────┐
                    │  4. Instant     │
                    │   Resolver      │
                    │    (24/7)       │
                    └─────────────────┘
```

## Skills Overview

### 1. Downloader Skill (Existing)
- **File:** Use `easypaper-pdf-finder` skill
- **Purpose:** Automatically acquires fresh PDFs and mark schemes
- **Trigger:** Monthly or when new papers released

### 2. Weakness Hunter Skill
- **File:** `SKILL-weakness-hunter.md`
- **Purpose:** Diagnoses knowledge gaps through data-driven analysis
- **Trigger:** Every 4 weeks (Monthly Audit)
- **Output:** Ranked list of weak topics with mastery scores

### 3. Instant Resolver Skill
- **File:** `SKILL-instant-resolver.md`
- **Purpose:** 24/7 emergency help for stuck questions
- **Trigger:** Student uploads stuck question + photo
- **Output:** Step-by-step solution + similar practice questions

### 4. Error Elimination Loop Skill
- **File:** `SKILL-error-elimination-loop.md`
- **Purpose:** Transforms mistakes into permanent learning
- **Trigger:** After every practice session
- **Output:** Micro-drills + verification of error elimination

### 5. Spaced Mastery Cycle Skill
- **File:** `SKILL-spaced-mastery-cycle.md`
- **Purpose:** Builds long-term retention through spaced repetition
- **Trigger:** Continuous automated scheduling
- **Output:** 1-week / 3-week / 6-week review schedule

## Quick Start

### For Students

```
1. Initialize your agent:
   "Initialize Mastery Agent for A-Level Physics (9702) 
    and Math (9709), exam date: June 2025"

2. Daily check-in:
   "Morning Agent" → Get personalized daily plan

3. When stuck:
   "I'm stuck on this" + upload photo → Instant solution

4. Weekly review:
   "Weekly review" → Error elimination + scheduling

5. Monthly audit:
   "Monthly audit" → Full weakness analysis + progress report
```

### For AI Agents

When a student needs comprehensive exam preparation:

```
1. Load SKILL.md (main agent instructions)
2. Load relevant sub-skills based on context:
   - Weakness Hunter for gap analysis
   - Instant Resolver for stuck questions
   - Error Elimination for mistake fixing
   - Spaced Mastery for scheduling
3. Reference easypaper-pdf-finder for downloads
4. Reference easypaper-exam-prep for fundamentals
```

## Workflows

### Daily Workflow (5-10 minutes)

```
Student: "Morning Agent"
   ↓
Agent checks:
   - Any 🔴 Critical topics? → Assign 20-min drill
   - Spaced review due today? → Assign re-attempt
   - Unfixed errors? → Assign Error Elimination
   - None above → "Upload stuck question"
   ↓
Agent provides personalized plan
```

### Weekly Workflow (Sunday, 60-90 minutes)

```
Student: "Weekly review"
   ↓
Phase 1 (20 min): Error Elimination
   - Review all week's mistakes
   - Assign micro-drills
   
Phase 2 (30 min): Mini Weakness Hunter
   - Re-score 1-2 subjects
   - Update mastery matrix
   
Phase 3 (10 min): Schedule next week
   - Set spaced reviews
   - Confirm daily check-ins
```

### Monthly Workflow (1st weekend, 2-3 hours)

```
Student: "Monthly audit"
   ↓
Step 1: Downloader refresh
   - Check for new papers
   - Update resource library
   
Step 2: Full Weakness Hunter
   - Analyze all subjects
   - Calculate mastery scores
   
Step 3: Progress report
   - Generate progress metrics
   - Set next month's targets
```

## Agent Commands

| Command | Function |
|---------|----------|
| `"Initialize Mastery Agent"` | Set up subjects and exam date |
| `"Morning Agent"` | Get today's personalized plan |
| `"I'm stuck on this"` + photo | Instant Resolver activation |
| `"Weekly review"` | Run weekly Error Elimination |
| `"Monthly audit"` | Full Weakness Hunter + report |
| `"Show my progress"` | Generate progress report |
| `"Add subject: [code]"` | Add new subject to tracking |
| `"What's my schedule?"` | Show upcoming reviews |
| `"Run weakness hunter on [subject]"` | Analyze specific subject |

## Templates

Located in `/templates/`:

- `topic-mastery-matrix.md` - Track topic scores
- `error-log.md` - Log and track errors
- `spaced-review-schedule.md` - Review calendar
- `progress-report.md` - Monthly progress summary

## File Structure

```
easypaper-mastery-agent/
├── SKILL.md                          # Main agent skill (central brain)
├── SKILL-weakness-hunter.md          # Skill 2: Gap diagnosis
├── SKILL-instant-resolver.md         # Skill 3: Emergency help
├── SKILL-error-elimination-loop.md   # Skill 4: Fix mistakes
├── SKILL-spaced-mastery-cycle.md     # Skill 5: Long-term retention
├── README.md                         # This file
├── templates/                        # Tracking templates
│   ├── topic-mastery-matrix.md
│   ├── error-log.md
│   ├── spaced-review-schedule.md
│   └── progress-report.md
└── workflows/                        # Detailed workflows
    ├── daily-checkin.md
    ├── weekly-session.md
    └── monthly-audit.md
```

## Integration with Other Skills

### Required Sub-Skills

- **easypaper-pdf-finder** - For downloading papers
- **easypaper-exam-prep** - For exam preparation fundamentals

### Skill Interconnections

```
Weakness Hunter → Spaced Mastery Cycle
   (feeds weak topics) → (schedules drills)

Weakness Hunter → Error Elimination Loop
   (identifies gaps) → (creates micro-drills)

Error Elimination Loop → Weakness Hunter
   (fixed topics) → (re-scores mastery)

Instant Resolver → Weakness Hunter
   (recurring stuck) → (adds to critical list)

Instant Resolver → Spaced Mastery Cycle
   (solution provided) → (schedules re-attempt)

Instant Resolver → Error Elimination Loop
   (errors identified) → (creates drills)
```

## Agent Personality

The EasyPaper Mastery Agent is:
- **Proactive:** Never waits for you to ask—pushes daily plan
- **Data-driven:** Decisions based on performance metrics
- **Strict but encouraging:** Holds you accountable, celebrates progress
- **Never lets you procrastinate:** Miss a session → immediate reschedule

## Success Metrics

The system is working when:
- ✅ Student completes daily 5-10 min check-ins
- ✅ Topic mastery improves month-over-month
- ✅ Same errors don't recur (elimination rate > 80%)
- ✅ 6-week review scores > 90%
- ✅ Student feels confident, not overwhelmed

## Best Practices

### DO:
- ✅ Check in daily (even if just to confirm nothing due)
- ✅ Upload stuck questions immediately (don't stay stuck)
- ✅ Complete error drills before re-tests
- ✅ Treat spaced reviews as seriously as new papers
- ✅ Trust the data over your feelings

### DON'T:
- ❌ Skip daily check-ins (momentum dies)
- ❌ Ignore 🔴 Critical topics (they don't fix themselves)
- ❌ Rush through error elimination (fix it once, fix it forever)
- ❌ Skip spaced reviews (forgetting curve is real)
- ❌ Study without a plan (random = ineffective)

## Getting Help

If you're a student using this system:
- Say "Morning Agent" to start each day
- Upload stuck questions anytime
- Ask "What's my progress?" for motivation

If you're an AI agent implementing this:
- Start with SKILL.md for overall flow
- Reference sub-skills for specific functionality
- Use templates for student tracking

## License

Part of the EasyPaper skill cluster for exam preparation.
