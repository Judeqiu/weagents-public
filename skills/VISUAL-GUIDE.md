# 📊 Visual Guide to Financial Skills

Understanding the skills with pictures and diagrams.

---

## The Big Picture

```
┌─────────────────────────────────────────────────────────────┐
│                     FINANCIAL SKILLS                        │
│                      (What You Can Do)                      │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  1. VALUATION   │  │  2. M&A DEALS   │  │  3. INVESTING   │
│                 │  │                 │  │                 │
│  "What's it     │  │  "Who wants to  │  │  "Should I      │
│   worth?"       │  │   buy it?"      │  │   buy this?"    │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Skill 1: Valuation (Finding the Price)

### Real Life Example: Buying a House 🏠

```
Your friend says:
"I'm selling my house for $500,000"

You think:
"Is that fair? Let me check..."

┌────────────────────────────────────────────┐
│         HOW TO CHECK THE PRICE             │
├────────────────────────────────────────────┤
│                                            │
│  Step 1: Look at similar houses            │
│          that sold recently                │
│                                            │
│  Similar House A: $480,000  ──┐            │
│  Similar House B: $520,000  ──┼── Average  │
│  Similar House C: $500,000  ──┘   $500,000 │
│                                            │
│  Step 2: Compare features                  │
│                                            │
│  Your friend's house:                      │
│  ✓ Same size as House B ($520k)            │
│  ✓ Better location than House A            │
│  ✓ Needs some repairs (like House C)       │
│                                            │
│  Step 3: Decide                            │
│                                            │
│  Fair price = $500,000                     │
│  Friend is asking = $500,000               │
│                                            │
│  ✅ FAIR PRICE!                            │
│                                            │
└────────────────────────────────────────────┘
```

### For Companies (Same Idea!)

```
Your friend says:
"I'm selling my coffee shop for $2 million"

You use the TOOL:

┌────────────────────────────────────────────┐
│    RUN: generate-comps.py                  │
│                                            │
│    Input:                                  │
│    • Your coffee shop                      │
│    • 5 similar coffee shops                │
│                                            │
│    Output: Excel file with tables          │
└────────────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────┐
│         THE SPREADSHEET SHOWS:             │
├────────────────────────────────────────────┤
│                                            │
│  Similar Coffee Shop A: $1.8M  ──┐         │
│  Similar Coffee Shop B: $2.2M  ──┼──       │
│  Similar Coffee Shop C: $2.0M  ──┘   Avg   │
│  Similar Coffee Shop D: $1.9M        $2.0M │
│  Similar Coffee Shop E: $2.1M              │
│                                            │
│  Your friend's shop: $2.0M (FAIR!)         │
│                                            │
│  Friend is asking: $2.0M                   │
│                                            │
│  ✅ FAIR PRICE!                            │
│                                            │
└────────────────────────────────────────────┘
```

---

## Skill 2: Finding Buyers (M&A)

### Real Life Example: Selling Your Bicycle 🚲

```
You want to sell your bike.
Who might buy it?

┌────────────────────────────────────────────┐
│        THINKING OF BUYERS                  │
├────────────────────────────────────────────┤
│                                            │
│  TIER 1 - Best Chance:                     │
│  ⭐ Your friend who needs a bike           │
│  ⭐ Local bike shop (resells bikes)        │
│  ⭐ Someone whose bike just got stolen     │
│                                            │
│  TIER 2 - Maybe:                           │
│  ○ Parent looking for kid's bike           │
│  ○ College student                         │
│                                            │
│  TIER 3 - Probably Not:                    │
│  ✗ Your grandma (doesn't ride)             │
│  ✗ Car dealership                          │
│                                            │
└────────────────────────────────────────────┘
```

### For Companies (Same Idea!)

```
You want to sell a coffee shop chain.
Who might buy it?

┌────────────────────────────────────────────┐
│    RUN: generate-buyer-list.py             │
│                                            │
│    Input:                                  │
│    • Coffee shop business                  │
│    • Makes $5M per year                    │
│                                            │
│    Output: CSV file with buyers            │
└────────────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────┐
│         THE LIST SHOWS:                    │
├────────────────────────────────────────────┤
│                                            │
│  TIER 1 - Best Fits (Call These First):    │
│  ⭐ Starbucks (buys small chains)          │
│  ⭐ Dunkin' (expanding in your area)       │
│  ⭐ Private Equity Firm A (loves cafes)    │
│                                            │
│  TIER 2 - Maybe (Call If Tier 1 Says No):  │
│  ○ Restaurant Group (diversifying)         │
│  ○ Smaller Competitor (wants to grow)      │
│                                            │
│  TIER 3 - Probably Not:                    │
│  ✗ Tech Company (doesn't buy cafes)        │
│  ✗ Industrial Manufacturer                 │
│                                            │
└────────────────────────────────────────────┘
```

---

## Skill 3: Stock Analysis (Should I Buy?)

### Real Life Example: Buying a Toy 🎮

```
You have $50 to spend on a toy.
Which one should you buy?

┌────────────────────────────────────────────┐
│        TOY A: ROBOT DOG                    │
│        Price: $50                          │
├────────────────────────────────────────────┤
│  ✓ Everyone wants one                      │
│  ✓ Price might go up to $70                │
│  ✓ Fun to play with                        │
│                                            │
│  ⚠ Might break easily                      │
│  ⚠ Newer model coming soon                 │
│                                            │
│  VERDICT: BUY! ⭐⭐⭐⭐⭐                  │
│  Expected value: $70 (+40%)                │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│        TOY B: BOARD GAME                   │
│        Price: $50                          │
├────────────────────────────────────────────┤
│  ✓ Well made                               │
│  ✓ Lasts long time                         │
│                                            │
│  ⚠ Not very popular                        │
│  ⚠ Price might drop to $40                 │
│                                            │
│  VERDICT: DON'T BUY ⭐⭐                   │
│  Expected value: $40 (-20%)                │
└────────────────────────────────────────────┘
```

### For Stocks (Same Idea!)

```
You have $1,000 to invest.
Should you buy GameCompany stock?

┌────────────────────────────────────────────┐
│    READ: examples/sample-earnings-update   │
│                                            │
│    Then write your own analysis            │
└────────────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────┐
│     YOUR STOCK ANALYSIS:                   │
├────────────────────────────────────────────┤
│                                            │
│  STOCK: GameCompany                        │
│  PRICE: $50 per share                      │
│                                            │
│  THE GOOD:                                 │
│  ✓ Sold more games than expected           │
│  ✓ New hit game coming out                 │
│  ✓ Price is lower than it should be        │
│                                            │
│  THE BAD:                                  │
│  ⚠ Competitors are strong                  │
│  ⚠ People might stop buying games          │
│                                            │
│  VERDICT: BUY! ⭐⭐⭐⭐                    │
│  Fair price: $65 (+30%)                    │
│                                            │
└────────────────────────────────────────────┘
```

---

## Skill 4: Buying a Business (LBO)

### Real Life Example: Fixer-Upper House 🏚️➡️🏠

```
You want to buy a house, fix it, sell it for profit.

┌────────────────────────────────────────────┐
│        THE DEAL:                           │
├────────────────────────────────────────────┤
│                                            │
│  BUY:                                      │
│  House price:        $200,000              │
│  Your money:         $50,000               │
│  Bank loan:          $150,000              │
│                                            │
│  FIX UP (1 year):                          │
│  Repairs:            $30,000               │
│  New kitchen:        $20,000               │
│  Total spent:        $250,000              │
│                                            │
│  SELL (1 year later):                      │
│  Selling price:      $350,000              │
│  Pay back loan:      ($150,000)            │
│  Pay bank interest:  ($15,000)             │
│  You get:            $185,000              │
│                                            │
│  RESULT:                                   │
│  You invested:       $50,000               │
│  You got back:       $185,000              │
│  Profit:             $135,000              │
│  Return:             270% in 2 years!      │
│                                            │
│  ✅ GREAT DEAL!                            │
│                                            │
└────────────────────────────────────────────┘
```

### For Businesses (Same Idea!)

```
You want to buy a coffee shop chain, improve it,
sell it in 5 years for profit.

┌────────────────────────────────────────────┐
│    READ: examples/sample-lbo-output        │
│                                            │
│    Then calculate your deal                │
└────────────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────┐
│        THE BUSINESS DEAL:                  │
├────────────────────────────────────────────┤
│                                            │
│  BUY:                                      │
│  Business price:     $5,000,000            │
│  Your money:         $2,000,000            │
│  Bank loan:          $3,000,000            │
│                                            │
│  RUN BUSINESS (5 years):                   │
│  Year 1 profit:      $500,000              │
│  Year 5 profit:      $1,000,000            │
│  (You made it better!)                     │
│                                            │
│  Pay back loan from profits:               │
│  Loan paid off:      $3,000,000            │
│  Interest paid:      $800,000              │
│                                            │
│  SELL (year 5):                            │
│  Selling price:      $10,000,000           │
│  Loan remaining:     ($0 - all paid!)      │
│  You get:            $10,000,000           │
│                                            │
│  RESULT:                                   │
│  You invested:       $2,000,000            │
│  You got back:       $10,000,000           │
│  Profit:             $8,000,000            │
│  Return:             5× your money!        │
│  Or: 38% per year                          │
│                                            │
│  ✅ GREAT DEAL!                            │
│                                            │
└────────────────────────────────────────────┘
```

---

## How The Skills Connect

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR DECISION JOURNEY                    │
└─────────────────────────────────────────────────────────────┘

SCENARIO 1: You own a business and want to sell it

    ┌─────────────┐
    │  "What's my │
    │   business  │
    │   worth?"   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐     ┌─────────────┐
    │  Use Skill 1 │────▶│ Get value:  │
    │  (Valuation) │     │ $5 million  │
    └─────────────┘     └─────────────┘
           │
           ▼
    ┌─────────────┐
    │  "Who wants │
    │   to buy?"  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐     ┌──────────────────┐
    │  Use Skill 2 │────▶│ Get buyer list:  │
    │  (M&A)       │     │ 30 potential     │
    └─────────────┘     │ buyers           │
                        └──────────────────┘


SCENARIO 2: You want to invest in stocks

    ┌─────────────┐
    │  "Should I  │
    │   buy this  │
    │   stock?"   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐     ┌─────────────┐
    │  Use Skill 3 │────▶│ Decision:   │
    │  (Research)  │     │ BUY!        │
    └─────────────┘     │ Target: $65 │
                        └─────────────┘


SCENARIO 3: You want to buy a whole business

    ┌─────────────┐
    │  "Can I    │
    │   make     │
    │   money?"  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐     ┌─────────────┐
    │  Use Skill 4 │────▶│ Result:     │
    │  (LBO)       │     │ 5× return!  │
    └─────────────┘     └─────────────┘
```

---

## Quick Comparison Table

| If you want to... | Think of it like... | Use this skill | Get this file |
|-------------------|---------------------|----------------|---------------|
| Know what something is worth | Getting your house appraised | Valuation | `.xlsx` |
| Find people to buy something | Listing your bike for sale | M&A | `.csv` |
| Decide if a purchase is smart | Reading toy reviews | Research | `.md` |
| Buy, fix, and sell for profit | House flipping | LBO | `.md` |

---

## Remember These 4 Things

1. 🔵 **BLUE cells** in Excel = You type numbers here
2. ⚫ **BLACK cells** = Automatic answers (don't touch!)
3. 📊 **Comps** = Compare to similar things
4. 🔮 **DCF** = Predict the future

---

## Next Steps

1. 📖 Read the simple guide: `cat skills/SIMPLE-GUIDE.md`
2. 🚀 Start here: `cat skills/START-HERE.md`
3. 📋 Quick commands: `cat skills/QUICK-REFERENCE.md`

**You've got this!** 💪
