# Behavioral Coach

A coaching skill for practicing quiet confidence, strategic communication, and self-respect based on 42 core principles.

## Description

This skill helps you internalize 42 behavioral principles organized into three tiers:

**Foundation (1-12):** Physical presence, immediate reactions, basic boundaries
- Lowering emotional volume, holding eye contact, saying no without explanation
- Slow movements, enforcing early boundaries, ending conversations on your terms

**Tactical (13-27):** Communication strategy, silence, interruptions, emotional control
- Strategic silence, handling interruptions, delaying decisions
- Managing access to you, ignoring gossip, not chasing attention

**Strategic (28-42):** Trust, value demonstration, long-term patterns
- Guarding vulnerabilities, not proving value, acting on patterns
- Protecting wins, quiet confidence, natural consequences

## Installation

The skill is self-contained. Just ensure Python 3 is available.

```bash
cd skills/behavioral-coach
./coach list
```

## Commands

| Command | Description |
|---------|-------------|
| `./coach list` | List all 42 principles with summaries |
| `./coach principle <num>` | Get detailed coaching (1-42) |
| `./coach daily` | Get a daily practice prompt |
| `./coach log <num> "note"` | Log your practice session |
| `./coach stats` | View your practice statistics |
| `./coach scenario "situation"` | Get coaching for a specific situation |

## The 42 Principles

### Foundation (1-12)

#### 1. Stop Reacting Instantly
When you pause before responding, people feel the shift. That small delay shows control. Controlled people are treated more carefully.

#### 2. Say No Without Long Explanations
Short refusals signal self-respect. When you stop justifying every decision, others stop questioning them.

#### 3. Don't Chase Conversations
If someone pulls back, you let them. That detachment changes the dynamic fast. People value what doesn't beg for attention.

#### 4. Lower Your Emotional Volume
Calm tone, steady face, relaxed posture. When you stop showing every feeling, others stop trying to trigger you.

#### 5. Hold Eye Contact Slightly Longer
Not aggressively, just calmly. It makes people think twice before interrupting or dismissing you.

#### 6. Enforce One Boundary Early
The first time someone crosses a line, you address it quietly. That single action reshapes how they deal with you going forward.

#### 7. Stop Oversharing Personal Details
Mystery creates space. When people know less about your struggles, they treat you with more respect.

#### 8. End Conversations on Your Terms
A simple, confident close changes perception. People respect those who decide when enough is enough.

#### 9. Protect Your Time Like It's Limited
Late replies, limited availability, focused presence. The moment your time looks valuable, you become valuable.

#### 10. Stop Correcting Everyone
Let small mistakes pass. When you only speak up for important things, your words carry more weight.

#### 11. Stop Laughing at Disrespectful Jokes About You
One calm "I don't find that funny" changes everything. People rarely repeat what doesn't get rewarded.

#### 12. Slow Your Movements Instead of Rushing
Fast movements signal anxiety. Slow, deliberate actions signal control and confidence.

### Tactical (13-27)

#### 13. Don't Reveal Your Next Move Too Early
Talking about plans feels powerful but weakens leverage. Quiet progress makes people adjust to you later.

#### 14. Keep Emotions Steady in Disagreement
When you disagree calmly, others either rise to your level or back down. Raised voices lose influence.

#### 15. Stop Seeking Instant Replies
If someone delays responding, you don't chase. This balance removes desperation from your side.

#### 16. Ask Direct Questions When Unclear
Clarity exposes manipulation fast. Calm directness forces honesty or discomfort.

#### 17. Limit How Much Access People Have to You
Not everyone deserves your full attention. Limited access increases respect automatically.

#### 18. Become Comfortable with Silence
Silence makes others uneasy, not you. The person comfortable in silence holds invisible control.

#### 19. Stop Filling Every Silence
When a pause appears, you let it sit. The other person usually speaks more and reveals more.

#### 20. Stop Explaining Your Standards
You live them instead. People adjust faster to behavior than to speeches.

#### 21. Don't Compete for Attention
When others try to dominate the room, you stay composed. The calm presence often stands out more.

#### 22. Stop Reacting to Gossip About You
Defending yourself feeds it. Ignoring it starves it. People respect the one who stays above noise.

#### 23. Finish Your Sentences When Interrupted
Calmly continue speaking without raising your voice. This resets the dynamic without creating drama.

#### 24. Delay Emotional Decisions
You don't reply to heated messages immediately. Time cools emotions and protects your leverage.

#### 25. Reward Respect and Ignore Disrespect
Positive behavior gets attention. Negative behavior gets distance. People learn what earns your engagement.

#### 26. Stop Overcommitting
You choose fewer obligations and complete them well. Reliability builds reputation faster than busyness.

#### 27. Accept That Not Everyone Needs to Like You
Approval stops being your goal. When you detach from being liked, people start taking you seriously.

### Strategic (28-42)

#### 28. Guard Your Struggles
Not everyone deserves access to your vulnerabilities. Share selectively with those who've earned trust.

#### 29. Calm Correction
Respond to disrespect with steady firmness, not emotion. "That's not acceptable" carries more weight than anger.

#### 30. Stop Proving Your Value
Proving signals doubt. Let results speak—people will assume competence instead of questioning it.

#### 31. Reduce Complaining
Handle problems quietly. Complaints lower perceived strength; resilience commands respect.

#### 32. Strategic Information
Don't reveal everything you know. Mystery creates leverage and commands respect.

#### 33. Control Facial Reactions
Your face gives away information. A neutral expression protects your position.

#### 34. Walk Away from Disrespect
Calmly leaving shows self-respect. People treat you better when you don't tolerate nonsense.

#### 35. Act on Patterns
Stop negotiating with people based on promises. One repeated behavior tells you enough.

#### 36. Delayed Responses
Don't answer every message immediately. Measured responses show you have priorities.

#### 37. Don't Argue with the Committed
Disengage from people committed to misunderstanding you. Protect your energy.

#### 38. Ignore Passive Aggression
Address directly or ignore completely. Don't play manipulation games.

#### 39. Protect Your Wins
Don't share good news with secret competitors. Not everyone celebrates your growth.

#### 40. Quiet Confidence
Stop seeking reassurance. Confidence in your choices changes how others approach you.

#### 41. Natural Consequences
Stop rescuing people. Let them learn from their choices.

#### 42. Consistent Tone
Treat everyone the same regardless of status. Consistency builds respect.

## Data Storage

- Practice logs: `skills/behavioral-coach/data/practice_log.json`
- Statistics: `skills/behavioral-coach/data/stats.json`

## Example Usage

```bash
# See all principles
./coach list

# Deep dive into principle 5
./coach principle 5

# Get today's practice
./coach daily

# Log your practice
./coach log 12 "Walked slower and felt more in control"

# Check your progress
./coach stats

# Get help with a situation
./coach scenario "Someone keeps interrupting me"
```
