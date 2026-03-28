#!/usr/bin/env python3
"""
Behavioral Coach - Practice quiet confidence and strategic behavior
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

# Data directory (use workspace path to avoid permission issues)
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PRACTICE_LOG = DATA_DIR / "practice_log.json"
STATS_FILE = DATA_DIR / "stats.json"

# The 42 Principles (#1-42)
PRINCIPLES = {
    1: {
        "title": "Stop reacting instantly",
        "core": "When you pause before responding, people feel the shift.",
        "why": "That small delay shows control. Controlled people are treated more carefully.",
        "practice": [
            "Count to 3 before responding to any question today",
            "When surprised, breathe before reacting",
            "Notice when others rush to respond—observe the difference"
        ],
        "triggers": ["You're caught off guard", "You feel pressured to answer", "Emotional moments"],
        "mantra": "Pause is power. Speed signals anxiety."
    },
    2: {
        "title": "Say no without long explanations",
        "core": "Short refusals signal self-respect.",
        "why": "When you stop justifying every decision, others stop questioning them.",
        "practice": [
            "Practice saying 'No, that doesn't work for me' without adding reasons",
            "When declining, stop after one sentence—don't elaborate",
            "Notice the urge to explain—resist it"
        ],
        "triggers": ["You're asked to do something you don't want to", "You feel guilty saying no", "Pressure to justify"],
        "mantra": "No is a complete sentence. Explanations invite negotiation."
    },
    3: {
        "title": "Don't chase conversations",
        "core": "If someone pulls back, you let them.",
        "why": "That detachment changes the dynamic fast. People value what doesn't beg for attention.",
        "practice": [
            "When someone stops engaging, don't double-message",
            "Let conversations end naturally—don't force continuation",
            "Practice walking away first sometimes"
        ],
        "triggers": ["They stop replying", "Conversation feels forced", "You feel needy"],
        "mantra": "What chases, repels. What withdraws, attracts."
    },
    4: {
        "title": "Lower your emotional volume",
        "core": "Calm tone, steady face, relaxed posture.",
        "why": "When you stop showing every feeling, others stop trying to trigger you.",
        "practice": [
            "Practice speaking 20% softer than your natural volume today",
            "Check your posture—relax your shoulders when you notice tension",
            "Observe your facial expressions in interactions—keep them neutral"
        ],
        "triggers": ["You feel excited", "You feel angry", "You feel nervous"],
        "mantra": "Emotional restraint commands respect."
    },
    5: {
        "title": "Hold eye contact slightly longer than before",
        "core": "Not aggressively, just calmly.",
        "why": "It makes people think twice before interrupting or dismissing you.",
        "practice": [
            "In your next conversation, hold eye contact one second longer than comfortable",
            "When speaking to a group, hold gaze with individuals",
            "Don't be the first to look away during important moments"
        ],
        "triggers": ["You're being dismissed", "Someone interrupts you", "You want to show confidence"],
        "mantra": "Eyes show certainty. Hold your ground."
    },
    6: {
        "title": "Enforce one boundary early",
        "core": "The first time someone crosses a line, you address it quietly.",
        "why": "That single action reshapes how they deal with you going forward.",
        "practice": [
            "Identify one boundary that's been crossed recently—address it today",
            "Practice the phrase: 'That's not okay with me' in a calm tone",
            "Don't wait for the third violation—act on the first"
        ],
        "triggers": ["Someone crosses a line", "You feel disrespected", "A new relationship dynamic forms"],
        "mantra": "Early boundaries prevent bigger problems."
    },
    7: {
        "title": "Stop oversharing personal details",
        "core": "Mystery creates space.",
        "why": "When people know less about your struggles, they treat you with more respect.",
        "practice": [
            "Share 50% less about your personal life this week",
            "When asked personal questions, answer briefly and redirect",
            "Notice when you overshare to bond—stop yourself"
        ],
        "triggers": ["You want to connect", "You feel nervous", "Someone asks personal questions"],
        "mantra": "Less is more. Mystery commands respect."
    },
    8: {
        "title": "End conversations on your terms",
        "core": "A simple, confident close changes perception.",
        "why": "People respect those who decide when enough is enough.",
        "practice": [
            "Practice exit lines: 'I need to go' or 'This was good, let's continue another time'",
            "Leave while the conversation is still good—don't wait for it to die",
            "Be the first to end interactions sometimes"
        ],
        "triggers": ["Conversation is dragging", "You have other priorities", "You want to leave"],
        "mantra": "You control your time. End with confidence."
    },
    9: {
        "title": "Protect your time like it's limited",
        "core": "Late replies, limited availability, focused presence.",
        "why": "The moment your time looks valuable, you become valuable.",
        "practice": [
            "Block 'focus time' on your calendar—treat it as sacred",
            "Take 2+ hours to respond to non-urgent messages",
            "When with someone, give them your full attention—then withdraw it fully"
        ],
        "triggers": ["Someone demands immediate time", "You feel your schedule slipping", "Requests for your attention"],
        "mantra": "Your time is currency. Spend it deliberately."
    },
    10: {
        "title": "Stop correcting everyone",
        "core": "Let small mistakes pass.",
        "why": "When you only speak up for important things, your words carry more weight.",
        "practice": [
            "Let one small error go uncorrected today",
            "Before correcting, ask: 'Does this actually matter?'",
            "Reserve your corrections for things that truly affect outcomes"
        ],
        "triggers": ["Someone is wrong", "You know the right answer", "You feel the urge to correct"],
        "mantra": "Silence on small things amplifies your voice on big things."
    },
    11: {
        "title": "Stop laughing at disrespectful jokes about you",
        "core": "One calm 'I don't find that funny' changes everything.",
        "why": "People rarely repeat what doesn't get rewarded.",
        "practice": [
            "When someone makes a joke at your expense, don't laugh—stay neutral",
            "Practice saying: 'I don't find that funny' without smiling",
            "Withdraw attention from those who make disrespectful jokes"
        ],
        "triggers": ["Someone roasts you", "You feel the need to laugh along", "Disrespect disguised as humor"],
        "mantra": "Your dignity is not negotiable. Don't laugh it away."
    },
    12: {
        "title": "Slow your movements instead of rushing",
        "core": "Fast movements signal anxiety.",
        "why": "Slow, deliberate actions signal control and confidence.",
        "practice": [
            "Walk 20% slower today—feel the difference",
            "When reaching for things, move deliberately",
            "Pause before standing up or sitting down"
        ],
        "triggers": ["You feel rushed", "You're nervous", "You want to appear confident"],
        "mantra": "Slow is smooth. Smooth is confident."
    },
    13: {
        "title": "Don't reveal your next move too early",
        "core": "Talking about plans feels powerful but weakens leverage.",
        "why": "Quiet progress makes people adjust to you later.",
        "practice": [
            "Keep your next project to yourself until it's 80% complete",
            "When asked about plans, say: 'I'm exploring a few things'",
            "Celebrate wins after they happen, not before"
        ],
        "triggers": ["You're excited about a new idea", "Someone asks what you're working on", "You want validation for your plans"],
        "mantra": "Surprise is power. Silence builds leverage."
    },
    14: {
        "title": "Keep your emotions steady in disagreement",
        "core": "When you disagree calmly, others either rise to your level or back down.",
        "why": "Raised voices lose influence.",
        "practice": [
            "In your next disagreement, speak 20% slower than usual",
            "Pause and breathe before responding to a heated comment",
            "Practice saying 'I see it differently' in a neutral tone"
        ],
        "triggers": ["Someone raises their voice at you", "You feel your adrenaline rising", "The conversation becomes heated"],
        "mantra": "Calm is contagious. Steady wins the influence game."
    },
    15: {
        "title": "Stop seeking instant replies",
        "core": "If someone delays responding, you don't chase.",
        "why": "This balance removes desperation from your side.",
        "practice": [
            "Send one message, then wait. No follow-ups for 48 hours minimum.",
            "Notice the urge to double-text—sit with it without acting",
            "Match their response time or take longer"
        ],
        "triggers": ["They haven't replied in hours", "You feel anxious about being ignored", "You want to send 'just checking in'"],
        "mantra": "Chasing repels. Patience commands respect."
    },
    16: {
        "title": "Ask direct questions when something feels unclear",
        "core": "Clarity exposes manipulation fast.",
        "why": "Calm directness forces honesty or discomfort.",
        "practice": [
            "When you sense evasion, ask: 'What exactly do you mean by that?'",
            "Practice asking one direct question in your next vague conversation",
            "Notice when people deflect—ask again, more specifically"
        ],
        "triggers": ["Something feels off", "You get a vague answer", "You sense manipulation"],
        "mantra": "Clarity is power. Vague is a red flag."
    },
    17: {
        "title": "Limit how much access people have to you",
        "core": "Not everyone deserves your full attention.",
        "why": "Limited access increases respect automatically.",
        "practice": [
            "Set specific 'office hours' for messages—don't respond outside them",
            "Before answering, ask: 'Is this worth my attention right now?'",
            "Practice the delayed response: wait 2+ hours even when you're free"
        ],
        "triggers": ["Someone demands immediate attention", "You feel drained by constant availability", "Boundary-pushers"],
        "mantra": "Scarcity creates value. Your attention is currency."
    },
    18: {
        "title": "Become comfortable with silence",
        "core": "Silence makes others uneasy, not you.",
        "why": "The person comfortable in silence holds invisible control.",
        "practice": [
            "In your next conversation, count to 5 before responding",
            "Let awkward silences sit—don't rush to fill them",
            "Practice the 'thoughtful pause' even when you know what to say"
        ],
        "triggers": ["The conversation lulls", "You feel pressure to speak", "Tense moments"],
        "mantra": "Silence is not empty. It's full of power."
    },
    19: {
        "title": "Stop filling every silence",
        "core": "When a pause appears, you let it sit.",
        "why": "The other person usually speaks more and reveals more. Control shifts quietly in your favor.",
        "practice": [
            "After someone speaks, wait 3 seconds before responding",
            "In negotiations, let the other party break the silence first",
            "Notice when you talk just to avoid silence—stop yourself"
        ],
        "triggers": ["After you ask a question", "During negotiations", "When you feel nervous"],
        "mantra": "He who speaks first, loses. Let silence work for you."
    },
    20: {
        "title": "Stop explaining your standards",
        "core": "You live them instead.",
        "why": "People adjust faster to behavior than to speeches.",
        "practice": [
            "Next time you want to explain your boundaries, just enforce them",
            "Show your standards through actions, not declarations",
            "When challenged, respond with silence or minimal words"
        ],
        "triggers": ["Someone crosses a boundary", "You feel the need to justify", "They ask why you do things differently"],
        "mantra": "Demonstrate, don't explain. Actions are the only argument."
    },
    21: {
        "title": "Don't compete for attention",
        "core": "When others try to dominate the room, you stay composed.",
        "why": "The calm presence often stands out more than the loud one.",
        "practice": [
            "In group settings, speak 30% less than your instinct tells you",
            "When someone interrupts to grab attention, maintain eye contact with the speaker",
            "Notice the attention-seekers—observe, don't compete"
        ],
        "triggers": ["Someone dominates the conversation", "You feel invisible", "Group dynamics feel competitive"],
        "mantra": "Still water runs deep. Loud is often insecure."
    },
    22: {
        "title": "Stop reacting to gossip about you",
        "core": "Defending yourself feeds it. Ignoring it starves it.",
        "why": "Over time, people respect the one who stays above noise.",
        "practice": [
            "When you hear gossip about yourself, don't address it directly",
            "If someone asks about rumors, say: 'I don't engage with that'",
            "Let your continued excellence be your only response"
        ],
        "triggers": ["You hear someone talked about you", "Rumors reach your ears", "You feel the urge to clear your name"],
        "mantra": "The high road has less traffic. Results silence gossip."
    },
    23: {
        "title": "Finish your sentences when interrupted",
        "core": "Calmly continue speaking without raising your voice.",
        "why": "This resets the dynamic without creating drama.",
        "practice": [
            "When interrupted, pause, then continue exactly where you left off",
            "Don't acknowledge the interruption—just proceed",
            "If they interrupt again, say: 'Let me finish'—then finish"
        ],
        "triggers": ["Someone talks over you", "You're cut off mid-sentence", "Dominant personalities"],
        "mantra": "Your voice deserves completion. Don't yield the floor."
    },
    24: {
        "title": "Delay emotional decisions",
        "core": "You don't reply to heated messages immediately.",
        "why": "Time cools emotions and protects your leverage.",
        "practice": [
            "When angry, write the response—then delete it and wait 24 hours",
            "Set a rule: no replies to charged messages until next day",
            "Notice when emotions rise—step away before responding"
        ],
        "triggers": ["You receive an angry message", "You feel reactive", "Emotions are running high"],
        "mantra": "Time is the best editor. Cool heads keep leverage."
    },
    25: {
        "title": "Reward respect and ignore disrespect",
        "core": "Positive behavior gets attention. Negative behavior gets distance.",
        "why": "People quickly learn what earns your engagement.",
        "practice": [
            "When someone is respectful, give them your full attention",
            "When someone is disrespectful, withdraw attention without announcement",
            "Notice who gets your energy—audit it weekly"
        ],
        "triggers": ["Someone is rude", "Someone is kind", "You feel pulled to react to negativity"],
        "mantra": "Feed what you want to grow. Starve what you want to die."
    },
    26: {
        "title": "Stop overcommitting",
        "core": "You choose fewer obligations and complete them well.",
        "why": "Reliability builds reputation faster than busyness.",
        "practice": [
            "Before saying yes, ask: 'Can I complete this excellently?'",
            "Say no to one thing this week that you'd usually accept",
            "Under-promise, then over-deliver"
        ],
        "triggers": ["You're asked to take on more", "You feel pressured to say yes", "Fear of missing out"],
        "mantra": "Fewer commitments, greater excellence. Busy is not impressive."
    },
    27: {
        "title": "Accept that not everyone needs to like you",
        "core": "Approval stops being your goal.",
        "why": "When you detach from being liked, people start taking you seriously.",
        "practice": [
            "Do one thing today that might be unpopular but is right",
            "Notice when you soften your stance to be liked—stop yourself",
            "Practice the phrase: 'We can agree to disagree'"
        ],
        "triggers": ["You feel disliked", "You want to people-please", "Someone disagrees with you strongly"],
        "mantra": "Liked by many, respected by few—or the reverse. Choose respect."
    },
    28: {
        "title": "Stop revealing your weaknesses to people who have not earned trust",
        "core": "Not everyone deserves access to your struggles.",
        "why": "When you share selectively, people handle you more carefully.",
        "practice": [
            "Before sharing a struggle, ask: 'Has this person proven they can hold my vulnerability?'",
            "Identify your 'inner circle'—only 2-3 people get your unfiltered struggles",
            "Practice the phrase: 'I'm working through some things' without elaborating"
        ],
        "triggers": ["You want to vent to someone new", "You feel emotionally overwhelmed", "Someone asks 'how are you really?'"],
        "mantra": "Trust is earned, not given. Your struggles are sacred."
    },
    29: {
        "title": "Respond to disrespect with calm correction, not emotion",
        "core": "A steady tone carries more weight than anger.",
        "why": "Calm firmness makes people rethink their behavior instantly.",
        "practice": [
            "Memorize the phrase: 'That's not acceptable' in a steady, low tone",
            "When disrespected, take a breath before responding—count to 3",
            "Practice saying boundaries without raising your voice or apologizing"
        ],
        "triggers": ["Someone crosses a line", "You feel your temper rising", "Public disrespect"],
        "mantra": "Calm authority > loud anger."
    },
    30: {
        "title": "Stop trying to prove your value",
        "core": "Proving signals doubt.",
        "why": "When you let results speak, people assume competence instead of questioning it.",
        "practice": [
            "In your next meeting, say 20% less. Let silence do the work.",
            "When you feel the urge to explain your credentials, stop yourself",
            "Document your wins privately—let others discover them organically"
        ],
        "triggers": ["New environment", "You feel underestimated", "Someone questions your expertise"],
        "mantra": "Your work speaks louder than your words."
    },
    31: {
        "title": "Reduce how often you complain",
        "core": "Complaints lower perceived strength. Handle problems quietly.",
        "why": "When you handle problems quietly, people see resilience instead of weakness.",
        "practice": [
            "Before speaking a complaint, ask: 'What am I hoping to gain from saying this?'",
            "Replace one complaint today with a solution or silence",
            "Notice when others complain excessively—observe how it affects your perception of them"
        ],
        "triggers": ["When you want to vent", "When things go wrong", "When you feel frustrated"],
        "mantra": "Silence is strength. Actions speak louder than complaints."
    },
    32: {
        "title": "Don't reveal everything you know",
        "core": "Keeping information creates quiet leverage.",
        "why": "People respect those who are not fully predictable.",
        "practice": [
            "In your next conversation, listen 70% and speak 30%",
            "Before sharing something, ask: 'Does this person need to know this?'",
            "Practice the pause—count to 3 before responding"
        ],
        "triggers": ["When you want to impress", "When you know the answer", "When asked for your opinion"],
        "mantra": "Mystery commands respect. Not everything needs to be shared."
    },
    33: {
        "title": "Control your facial reactions",
        "core": "Surprise, anger, or insecurity on your face gives others clues.",
        "why": "A neutral expression protects your position.",
        "practice": [
            "Practice a calm, neutral 'listening face' in the mirror",
            "When you hear surprising news, breathe before reacting",
            "Observe how poker players maintain composure—adopt that energy"
        ],
        "triggers": ["Receiving criticism", "Hearing unexpected news", "During negotiations"],
        "mantra": "Your face is information. Guard it."
    },
    34: {
        "title": "Become comfortable walking away mid-disrespect",
        "core": "Leaving calmly shows self-respect.",
        "why": "People treat you differently when they know you won't tolerate nonsense.",
        "practice": [
            "Identify your boundary: What behavior is your walk-away line?",
            "Rehearse exit lines: 'I need to step away' or 'This conversation is over'",
            "Practice leaving without explanation or apology"
        ],
        "triggers": ["Someone raises their voice at you", "Dismissive comments", "Repeated interruptions"],
        "mantra": "You don't owe anyone your presence in disrespect."
    },
    35: {
        "title": "Stop negotiating with people who show patterns",
        "core": "One repeated behavior tells you enough.",
        "why": "When you act on patterns instead of promises, your standards rise—and so does how people treat you.",
        "practice": [
            "List 3 people and their predictable patterns—accept them as facts",
            "Stop giving second chances for the same behavior",
            "Make decisions based on history, not hope"
        ],
        "triggers": ["They apologize again", "They promise to change", "You want to believe them"],
        "mantra": "Believe actions, not words. Patterns are truth."
    },
    36: {
        "title": "Stop answering every message immediately",
        "core": "Instant replies make you look available at all times.",
        "why": "Measured responses show you have priorities and structure.",
        "practice": [
            "Set specific times to check messages (e.g., 10am, 2pm, 6pm)",
            "Wait at least 30 minutes before responding to non-urgent messages",
            "Turn off notifications for a full day"
        ],
        "triggers": ["Phone buzzes", "You feel the urge to reply instantly", "FOMO"],
        "mantra": "Your attention is valuable. Don't give it away for free."
    },
    37: {
        "title": "Stop arguing with people committed to misunderstanding you",
        "core": "Not every disagreement deserves your energy.",
        "why": "When you disengage calmly, you protect your time and authority.",
        "practice": [
            "Recognize the signs: they twist your words, move goalposts, or refuse to acknowledge your points",
            "Use the phrase: 'I don't think we're going to agree on this'",
            "Exit the conversation without needing to 'win'"
        ],
        "triggers": ["Circular arguments", "They put words in your mouth", "You feel exhausted explaining"],
        "mantra": "You don't need to convince everyone. Some minds are closed."
    },
    38: {
        "title": "Refuse to react to passive-aggressive comments",
        "core": "Address directly or ignore completely.",
        "why": "That clarity makes manipulation ineffective.",
        "practice": [
            "When you hear a passive-aggressive remark, pause and ask: 'What do you mean by that?'",
            "If they backtrack, let them—it's their embarrassment, not yours",
            "Practice the blank stare—no reaction is a powerful reaction"
        ],
        "triggers": ["Backhanded compliments", "Sarcastic comments", "Subtle digs"],
        "mantra": "Call it out or let it die. Don't play the game."
    },
    39: {
        "title": "Stop sharing good news with people who secretly compete with you",
        "core": "Not everyone celebrates your growth.",
        "why": "Protecting your wins keeps jealousy away from your progress.",
        "practice": [
            "Identify who genuinely celebrates you vs. who competes with you",
            "Share your wins selectively—quality over quantity",
            "Celebrate privately sometimes; the win is yours regardless"
        ],
        "triggers": ["You want to share exciting news", "They ask what you're working on", "You feel the urge to update"],
        "mantra": "Not everyone deserves front-row seats to your life."
    },
    40: {
        "title": "Don't seek reassurance for every decision",
        "core": "Constant validation lowers perceived strength.",
        "why": "Quiet confidence in your choices changes how others approach you.",
        "practice": [
            "Make one small decision today without asking anyone's opinion",
            "When you want to ask 'Is this okay?', ask yourself instead",
            "Notice when you seek validation—what fear is behind it?"
        ],
        "triggers": ["Before making a choice", "After making a choice", "When you feel uncertain"],
        "mantra": "Trust yourself. You've made it this far."
    },
    41: {
        "title": "Let people feel the consequences of their actions",
        "core": "Stop rescuing, reminding, or covering for them.",
        "why": "Natural consequences teach faster than warnings.",
        "practice": [
            "When someone forgets something, let them deal with it",
            "Resist the urge to send reminder texts",
            "Let them experience the discomfort of their own choices"
        ],
        "triggers": ["You want to help", "You see them about to fail", "You feel responsible for their outcomes"],
        "mantra": "You're not their safety net. They're capable of learning."
    },
    42: {
        "title": "Maintain the same tone with everyone",
        "core": "No sudden shifts for status or authority.",
        "why": "Consistency builds respect across all levels.",
        "practice": [
            "Treat the CEO and the intern with the same baseline respect",
            "Notice if your voice or posture changes around certain people",
            "Practice being genuinely courteous to service staff"
        ],
        "triggers": ["Talking to someone powerful", "Talking to someone 'below' you", "Networking events"],
        "mantra": "Status is temporary. Character is permanent."
    }
}


def load_log():
    """Load practice log"""
    if PRACTICE_LOG.exists():
        with open(PRACTICE_LOG) as f:
            return json.load(f)
    return []


def save_log(log):
    """Save practice log"""
    with open(PRACTICE_LOG, 'w') as f:
        json.dump(log, f, indent=2)


def load_stats():
    """Load stats"""
    if STATS_FILE.exists():
        with open(STATS_FILE) as f:
            return json.load(f)
    return {"total_practices": 0, "last_practice": None, "streak": 0}


def save_stats(stats):
    """Save stats"""
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)


def list_principles():
    """List all principles"""
    print("\n🎯 The 42 Principles of Quiet Confidence\n")
    for num, p in PRINCIPLES.items():
        print(f"  {num}. {p['title']}")
        print(f"     {p['core']}")
    print()


def show_principle(num):
    """Show detailed coaching for a principle"""
    if num not in PRINCIPLES:
        print(f"❌ Principle {num} not found. Choose from 31-42.")
        return
    
    p = PRINCIPLES[num]
    print(f"\n{'='*60}")
    print(f"  #{num}: {p['title']}")
    print(f"{'='*60}\n")
    print(f"  💡 Core Principle:")
    print(f"     {p['core']}\n")
    print(f"  🎯 Why It Matters:")
    print(f"     {p['why']}\n")
    print(f"  📋 Practice This Week:")
    for i, practice in enumerate(p['practice'], 1):
        print(f"     {i}. {practice}")
    print(f"\n  ⚡ Common Triggers:")
    print(f"     {', '.join(p['triggers'])}")
    print(f"\n  🧘 Your Mantra:")
    print(f"     \"{p['mantra']}\"")
    print(f"\n{'='*60}\n")


def daily_prompt():
    """Generate a daily practice prompt"""
    log = load_log()
    
    # Find least practiced principles
    counts = {num: 0 for num in PRINCIPLES}
    for entry in log:
        if entry['principle'] in counts:
            counts[entry['principle']] += 1
    
    # Prioritize under-practiced, but add some randomness
    sorted_principles = sorted(counts.items(), key=lambda x: x[1])
    
    if random.random() < 0.3:  # 30% chance of pure random
        num = random.choice(list(PRINCIPLES.keys()))
    else:  # 70% chance of focusing on weak areas
        num = sorted_principles[0][0]
    
    p = PRINCIPLES[num]
    practice = random.choice(p['practice'])
    
    print("\n🌅 Daily Practice Prompt\n")
    print(f"  Today's Focus: Principle #{num} - {p['title']}")
    print(f"\n  🎯 Practice:")
    print(f"     {practice}")
    print(f"\n  🧘 Mantra:")
    print(f"     \"{p['mantra']}\"")
    print(f"\n  💡 Remember:")
    print(f"     {p['why']}")
    print(f"\n  📊 Log your practice with:")
    print(f"     ./coach log {num} \"what you did\"")
    print()


def log_practice(num, note):
    """Log a practice session"""
    if num not in PRINCIPLES:
        print(f"❌ Principle {num} not found. Choose from 1-42.")
        return
    
    log = load_log()
    stats = load_stats()
    
    entry = {
        "date": datetime.now().isoformat(),
        "principle": num,
        "note": note
    }
    log.append(entry)
    save_log(log)
    
    # Update stats
    stats["total_practices"] += 1
    
    # Calculate streak
    today = datetime.now().date()
    last = stats.get("last_practice")
    if last:
        last_date = datetime.fromisoformat(last).date()
        if today - last_date == timedelta(days=1):
            stats["streak"] += 1
        elif today == last_date:
            pass  # Already practiced today
        else:
            stats["streak"] = 1
    else:
        stats["streak"] = 1
    
    stats["last_practice"] = datetime.now().isoformat()
    save_stats(stats)
    
    p = PRINCIPLES[num]
    print(f"\n✅ Logged practice for Principle #{num}: {p['title']}")
    print(f"   Note: {note}")
    print(f"   Current streak: {stats['streak']} days")
    print()


def show_stats():
    """Show practice statistics"""
    log = load_log()
    stats = load_stats()
    
    print("\n📊 Your Practice Statistics\n")
    print(f"  Total practices: {stats.get('total_practices', 0)}")
    print(f"  Current streak: {stats.get('streak', 0)} days")
    
    if stats.get('last_practice'):
        last = datetime.fromisoformat(stats['last_practice'])
        print(f"  Last practice: {last.strftime('%Y-%m-%d %H:%M')}")
    
    # Count by principle
    print("\n  Practices by Principle:")
    counts = {num: 0 for num in PRINCIPLES}
    for entry in log:
        if entry['principle'] in counts:
            counts[entry['principle']] += 1
    
    for num in sorted(PRINCIPLES.keys()):
        p = PRINCIPLES[num]
        count = counts[num]
        bar = "█" * count + "░" * (10 - min(count, 10))
        print(f"    #{num}: {bar} ({count}) {p['title'][:30]}...")
    
    print()


def scenario_coach(situation):
    """Get coaching for a specific situation"""
    situation_lower = situation.lower()
    
    # Simple keyword matching
    matches = []
    
    keywords = {
        1: ["react", "instant", "pause", "respond", "quick", "delay"],
        2: ["no", "explain", "refuse", "decline", "justification", "short"],
        3: ["chase", "conversation", "pull back", "withdraw", "message", "engage"],
        4: ["emotional", "volume", "calm", "tone", "face", "posture"],
        5: ["eye contact", "look", "gaze", "stare", "confidence", "dismiss"],
        6: ["boundary", "cross", "line", "enforce", "early", "limit"],
        7: ["overshare", "personal", "detail", "mystery", "private", "reveal"],
        8: ["end", "conversation", "leave", "exit", "terms", "close"],
        9: ["time", "protect", "limited", "valuable", "availability", "focus"],
        10: ["correct", "mistake", "wrong", "error", "speak", "important"],
        11: ["joke", "laugh", "funny", "disrespect", "humor", "mock"],
        12: ["slow", "movement", "rush", "fast", "deliberate", "anxiety"],
        13: ["plan", "next move", "reveal", "early", "project", "announce"],
        14: ["disagree", "disagreement", "calm", "heated", "argument", "steady"],
        15: ["chase", "reply", "respond", "waiting", "ignored", "desperate"],
        16: ["unclear", "vague", "question", "direct", "manipulation", "honest"],
        17: ["access", "attention", "available", "reach", "demand", "time"],
        18: ["silence", "quiet", "awkward", "pause", "uneasy", "comfortable"],
        19: ["fill", "silence", "pause", "speak", "quiet", "space"],
        20: ["explain", "standard", "boundary", "justify", "speech", "tell"],
        21: ["attention", "dominate", "loud", "compete", "speak", "quiet"],
        22: ["gossip", "rumor", "talk", "defend", "noise", "ignore"],
        23: ["interrupt", "cut off", "finish", "sentence", "speak", "talk over"],
        24: ["emotional", "decision", "heated", "angry", "reply", "cool"],
        25: ["respect", "disrespect", "ignore", "reward", "attention", "engage"],
        26: ["commit", "overcommit", "busy", "obligation", "yes", "no"],
        27: ["like", "approval", "people please", "popular", "accept", "attach"],
        28: ["weakness", "struggle", "vulnerable", "trust", "secret", "private"],
        29: ["disrespect", "correction", "anger", "firm", "steady", "acceptable"],
        30: ["prove", "value", "worth", "credentials", "impress", "demonstrate"],
        31: ["complain", "complaining", "vent", "frustrated", "annoying"],
        32: ["talk", "share", "overshare", "tell", "reveal", "information"],
        33: ["face", "expression", "react", "surprise", "poker face"],
        34: ["disrespect", "rude", "walk away", "leave", "boundary"],
        35: ["pattern", "repeat", "always", "never", "promise", "change"],
        36: ["message", "text", "reply", "respond", "phone", "notification"],
        37: ["argue", "argument", "misunderstand", "circular", "debate"],
        38: ["passive", "aggressive", "sarcasm", "sarcastic", "backhanded"],
        39: ["compete", "competition", "jealous", "win", "success", "news"],
        40: ["reassurance", "validate", "sure", "okay", "decision", "choice"],
        41: ["rescue", "save", "remind", "consequence", "help", "bail"],
        42: ["tone", "status", "authority", "power", "boss", "employee"]
    }
    
    for num, words in keywords.items():
        score = sum(1 for w in words if w in situation_lower)
        if score > 0:
            matches.append((num, score))
    
    matches.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n🎯 Coaching for: \"{situation}\"\n")
    
    if matches:
        top_match = matches[0][0]
        p = PRINCIPLES[top_match]
        print(f"  Relevant Principle: #{top_match} - {p['title']}")
        print(f"\n  💡 Apply this:")
        print(f"     {p['core']}")
        print(f"\n  🎯 Action:")
        print(f"     {random.choice(p['practice'])}")
        print(f"\n  🧘 Remember:")
        print(f"     \"{p['mantra']}\"")
    else:
        print("  Hmm, I'm not sure which principle applies here.")
        print("  Try describing the situation with different words,")
        print("  or browse all principles with: ./coach list")
    
    print()


def main():
    if len(sys.argv) < 2:
        print("""
Behavioral Coach - Practice quiet confidence

Usage:
  ./coach list                    List all 42 principles
  ./coach principle <number>      Get coaching on principle (1-42)
  ./coach daily                   Get daily practice prompt
  ./coach log <number> <note>     Log practice for a principle
  ./coach stats                   View your statistics
  ./coach scenario <situation>    Get coaching for a situation

Examples:
  ./coach principle 35
  ./coach log 36 "Waited 1 hour before replying to non-urgent text"
  ./coach scenario "Someone keeps making sarcastic comments at me"
        """)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "list":
        list_principles()
    elif command == "principle":
        if len(sys.argv) < 3:
            print("❌ Please specify a principle number (1-42)")
            sys.exit(1)
        show_principle(int(sys.argv[2]))
    elif command == "daily":
        daily_prompt()
    elif command == "log":
        if len(sys.argv) < 4:
            print("❌ Usage: ./coach log <number> \"<note>\"")
            sys.exit(1)
        log_practice(int(sys.argv[2]), sys.argv[3])
    elif command == "stats":
        show_stats()
    elif command == "scenario":
        if len(sys.argv) < 3:
            print("❌ Please describe the situation")
            sys.exit(1)
        scenario_coach(" ".join(sys.argv[2:]))
    else:
        print(f"❌ Unknown command: {command}")
        print("Run ./coach for usage help.")


if __name__ == "__main__":
    main()
