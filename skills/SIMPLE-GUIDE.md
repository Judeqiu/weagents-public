# Financial Skills - Simple Guide

A beginner-friendly guide to using the financial analysis tools.

---

## What Are These Skills For?

Imagine you want to know:
- **"How much is this company worth?"** → Use the valuation tools
- **"Who might want to buy this company?"** → Use the buyer list tool
- **"Is this a good stock to invest in?"** → Use the research tools
- **"Can we make money buying and selling this business?"** → Use the PE tools

---

## Before You Start

### Step 1: Install the Tools (One Time Only)

Open your terminal and type:

```bash
pip3 install openpyxl pandas numpy
```

This installs the software needed to create Excel files.

---

## Skill 1: Finding Out What a Company is Worth

### What It Does

This is like asking: *"My neighbor is selling their house. How do I know if the price is fair?"*

You would:
1. Look at what similar houses sold for
2. Check how big the house is
3. See what features it has
4. Compare to other houses in the neighborhood

We do the same thing for companies!

### How To Use It

#### Method A: Compare to Similar Companies (The Easy Way)

**Command:**
```bash
python3 skills/financial-analysis-core/scripts/generate-comps.py \
  --target "Coffee Shop Chain" \
  --peers "Starbucks,Dunkin,Peets,Local Cafe A,Local Cafe B" \
  --output coffee_shop_value.xlsx
```

**What this does:**
- Creates an Excel spreadsheet
- Sets up tables to compare your company to 5 similar ones
- Calculates if the price is fair

**What you need to fill in:**
1. Open `coffee_shop_value.xlsx`
2. Look for **blue cells** - these are where you type numbers
3. For each competitor, enter:
   - Their stock price
   - How much money they make (revenue)
   - Their profit
4. The spreadsheet automatically calculates the answer!

**Example Result:**
```
Based on similar coffee shops:
- Low estimate: $2 million
- Fair price: $3 million  
- High estimate: $4 million
```

#### Method B: Calculate Future Money (The Thorough Way)

**Command:**
```bash
python3 skills/financial-analysis-core/scripts/generate-dcf.py \
  --company "Coffee Shop Chain" \
  --years 5 \
  --output coffee_shop_future.xlsx
```

**What this does:**
- Predicts how much money the company will make in the next 5 years
- Calculates what that future money is worth today
- Like saying: *"If this business makes $100k per year for 5 years, what's that worth right now?"*

**What you need to fill in:**
1. How much money the company made last year
2. How fast you think it will grow
3. How much profit it keeps after paying all bills

**Example Result:**
```
If the coffee shop grows 10% each year:
- Today's value: $2.8 million
```

---

## Skill 2: Finding People Who Want to Buy a Company

### What It Does

This is like asking: *"I want to sell my bicycle. Who might want to buy it?"*

You would think about:
- Friends who need a bike
- Bike shops that resell bikes
- People who collect bikes

For companies, we find:
- **Big companies** who want to buy competitors
- **Investment firms** who buy businesses to make money

### How To Use It

**Command:**
```bash
python3 skills/investment-banking/scripts/generate-buyer-list.py \
  --company "My Coffee Shop" \
  --industry "food" \
  --revenue 5 \
  --ebitda 1 \
  --output potential_buyers.csv
```

**What those numbers mean:**
- `--revenue 5` = The coffee shop makes $5 million per year
- `--ebitda 1` = After paying all costs, it keeps $1 million as profit

**What you get:**
A list file (`potential_buyers.csv`) with:
- Names of companies who might buy
- Why they would want to buy
- How good of a fit they are

**Example Output:**
```
Tier 1 - Best Fits:
✓ Starbucks - They buy small chains to grow
✓ Dunkin - Looking to expand in your area
✓ Private Equity Firm A - Buys food businesses

Tier 2 - Maybe:
○ Local Restaurant Group - Might want cafes
○ Investment Firm B - Sometimes buys food companies

Tier 3 - Probably Not:
× Tech Company - Doesn't buy coffee shops
```

---

## Skill 3: Deciding If a Stock is a Good Buy

### What It Does

This helps you decide: *"Should I buy stock in this company?"*

Like when you're choosing which toy to buy:
- Is it popular?
- Is the price fair?
- Will it be worth more later?

### How To Use It

**Step 1: Read the guide**
```bash
cat skills/equity-research/SKILL.md
```

**Step 2: Create your analysis**

Copy the template:
```bash
cp skills/equity-research/examples/sample-earnings-update.md \
   my_stock_analysis.md
```

**Step 3: Fill in your answers**

Open `my_stock_analysis.md` and answer these questions:

1. **What does the company do?**
   - Example: "They sell video games"

2. **How much money did they make?**
   - Example: "They made $1 billion, which was MORE than expected"

3. **Is the price fair?**
   - Example: "Stock costs $50, but I think it's worth $60"

4. **Should I buy?**
   - Example: "YES - They're growing fast and price is good"

**Example Result:**
```
COMPANY: GameMaker Inc
PRICE: $50 per share
MY RATING: BUY ⭐

WHY:
✓ They made more money than expected
✓ New games coming out soon
✓ Price is lower than it should be

RISKS:
⚠ Competition from other game companies
⚠ People might stop buying games

MY TARGET PRICE: $65 (30% higher than today)
```

---

## Skill 4: Buying a Whole Business (Like on Shark Tank)

### What It Does

This is for when you want to buy an ENTIRE business, fix it up, and sell it later for more money.

Like buying a fixer-upper house:
1. Buy it for $200k
2. Spend $50k fixing it up
3. Sell it for $350k
4. Profit: $100k!

### How To Use It

**Step 1: Read the guide**
```bash
cat skills/private-equity/SKILL.md
```

**Step 2: Look at an example**
```bash
cat skills/private-equity/examples/sample-lbo-output.md
```

**Step 3: Answer these questions**

1. **How much does the business cost?**
   - Example: $5 million

2. **How much money will I make each year?**
   - Example: $500k per year

3. **How much can I sell it for in 5 years?**
   - Example: $8 million

4. **Is this a good deal?**
   - Calculate: Will I make more than 20% profit per year?

**Simple Formula:**
```
If you invest:     $2 million
And get back:      $4 million
After 5 years

Your profit: 2x your money (100% return)
Or: 15% per year
```

**Good Deal?**
- ✅ YES if you make 20%+ per year
- ⚠️ MAYBE if you make 15% per year
- ❌ NO if you make less than 15% per year

---

## Common Words Explained

| Word | Simple Meaning | Example |
|------|---------------|---------|
| **Revenue** | Total money coming in | A coffee shop makes $1 million in sales |
| **Profit** | Money left after paying bills | After costs, they keep $200k |
| **Valuation** | What something is worth | The coffee shop is worth $2 million |
| **Stock** | A piece of ownership in a company | Owning 1 share of Apple |
| **EBITDA** | Profit before some costs | A way to compare companies fairly |
| **Multiple** | How many times profit = value | 10x EBITDA = value is 10 × profit |
| **Comps** | Comparison to similar things | What similar coffee shops sold for |
| **DCF** | Guessing future money | Predicting what future profits are worth today |
| **LBO** | Buying with borrowed money | Buying a business using a loan |

---

## Color Coding in Excel Files

When you open the Excel files, you'll see different colors:

| Color | What It Means | What You Do |
|-------|---------------|-------------|
| **Blue** | Numbers YOU type in | Enter your data here |
| **Black** | Automatic calculations | Don't touch - it's a formula! |
| **Green** | Links to other sheets | References data from elsewhere |

**Rule: Only change BLUE cells!**

---

## Step-by-Step Example: Valuing a Lemonade Stand

Let's say your friend wants to sell their lemonade stand. Is $10,000 a fair price?

### Step 1: Find Similar Stands

```bash
python3 skills/financial-analysis-core/scripts/generate-comps.py \
  --target "Sarah's Lemonade Stand" \
  --peers "Mike's Lemonade,Corner Stand,Park Kiosk,Mall Cart,Beach Vendor" \
  --output lemonade_comps.xlsx
```

### Step 2: Fill In The Information

Open `lemonade_comps.xlsx` and enter:

| Stand | Yearly Sales | Yearly Profit |
|-------|-------------|---------------|
| Mike's | $20,000 | $5,000 |
| Corner | $15,000 | $3,000 |
| Park | $25,000 | $6,000 |
| Mall | $30,000 | $8,000 |
| Beach | $22,000 | $4,000 |

Sarah's Stand: $18,000 sales, $4,000 profit

### Step 3: Read The Answer

The spreadsheet calculates:
```
Similar stands sell for 4× their yearly profit

Sarah's profit: $4,000
Fair price: $4,000 × 4 = $16,000

Friend is asking: $10,000
VERDICT: GOOD DEAL! 🎉
```

---

## Checklist: Did I Do It Right?

### For Valuation:
- [ ] I picked 3-5 similar companies
- [ ] I entered their sales and profit
- [ ] I calculated the average price
- [ ] I applied it to my company

### For Buyer List:
- [ ] I know how much money my company makes
- [ ] I picked the right industry
- [ ] I got a list of 20-30 potential buyers
- [ ] I focused on the "Tier 1" buyers first

### For Stock Analysis:
- [ ] I looked at recent earnings
- [ ] I compared price to value
- [ ] I listed good and bad points
- [ ] I made a clear buy/hold/sell decision

### For Buying a Business:
- [ ] I know the purchase price
- [ ] I estimated yearly profit
- [ ] I guessed a future selling price
- [ ] I calculated if profit is more than 20% per year

---

## Quick Command Reference

### See How Much a Company is Worth
```bash
python3 skills/financial-analysis-core/scripts/generate-comps.py \
  --target "Company Name" \
  --peers "Competitor1,Competitor2,Competitor3" \
  --output myfile.xlsx
```

### Predict Future Money
```bash
python3 skills/financial-analysis-core/scripts/generate-dcf.py \
  --company "Company Name" \
  --years 5 \
  --output myfile.xlsx
```

### Find Potential Buyers
```bash
python3 skills/investment-banking/scripts/generate-buyer-list.py \
  --company "Company Name" \
  --industry software \
  --revenue 50 \
  --ebitda 10 \
  --output buyers.csv
```

### Read the Guides
```bash
cat skills/financial-analysis-core/SKILL.md
cat skills/investment-banking/SKILL.md
cat skills/equity-research/SKILL.md
cat skills/private-equity/SKILL.md
```

---

## Getting Help

### If You Get Stuck:

1. **Read the error message** - It often tells you what's wrong
2. **Check you typed everything correctly** - One wrong letter breaks it!
3. **Make sure you installed the tools** - Run `pip3 install openpyxl`
4. **Look at the examples** - They show you what the output should look like

### Example Outputs to Study:

```bash
# Good comps report
cat skills/financial-analysis-core/examples/sample-comps-report.md

# Good DCF report
cat skills/financial-analysis-core/examples/sample-dcf-output.md

# Good stock analysis
cat skills/equity-research/examples/sample-earnings-update.md

# Good business purchase analysis
cat skills/private-equity/examples/sample-lbo-output.md
```

---

## Remember

1. **These are just tools** - They help you organize information, but YOU make the decisions
2. **Garbage in, garbage out** - If you put in bad numbers, you get bad answers
3. **Real life is messy** - These are simplified models. Real business is more complex!
4. **Always double-check** - Run the numbers twice before making big decisions

---

## Summary

| I Want To... | I Use... | The Command Is... |
|-------------|----------|-------------------|
| Know what a company is worth | Valuation skills | `generate-comps.py` or `generate-dcf.py` |
| Find people to buy a company | Investment banking | `generate-buyer-list.py` |
| Decide if a stock is good | Equity research | Read `SKILL.md` and use templates |
| Buy and sell whole businesses | Private equity | Read `SKILL.md` and use examples |

---

**Happy Learning!** 🚀

Start with the lemonade stand example and work your way up to real companies!
