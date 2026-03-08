# 🚀 START HERE - Financial Skills

The absolute simplest guide to get started.

---

## Step 1: Install (Do This Once)

```bash
pip3 install openpyxl pandas numpy
```

---

## Step 2: Choose What You Want To Do

### Option A: "How much is this company worth?"

**Use this:**
```bash
python3 skills/financial-analysis-core/scripts/generate-comps.py \
  --target "Company Name" \
  --peers "Competitor1,Competitor2,Competitor3" \
  --output value.xlsx
```

**Then:** Open `value.xlsx` and fill in the BLUE cells

**You get:** A number like "This company is worth $5 million"

---

### Option B: "Who wants to buy this company?"

**Use this:**
```bash
python3 skills/investment-banking/scripts/generate-buyer-list.py \
  --company "Company Name" \
  --industry software \
  --revenue 50 \
  --ebitda 10 \
  --output buyers.csv
```

**You get:** A list of 20-30 companies who might want to buy

---

### Option C: "Should I buy this stock?"

**Read this:**
```bash
cat skills/equity-research/examples/sample-earnings-update.md
```

**Copy and edit:**
```bash
cp skills/equity-research/examples/sample-earnings-update.md my_analysis.md
```

---

### Option D: "Can I make money buying this business?"

**Read this:**
```bash
cat skills/private-equity/examples/sample-lbo-output.md
```

---

## The Only 4 Commands You Need

| # | What You Want | Command |
|---|---------------|---------|
| 1 | Value a company | `python3 skills/financial-analysis-core/scripts/generate-comps.py --target "NAME" --peers "A,B,C" --output file.xlsx` |
| 2 | Predict future money | `python3 skills/financial-analysis-core/scripts/generate-dcf.py --company "NAME" --years 5 --output file.xlsx` |
| 3 | Find buyers | `python3 skills/investment-banking/scripts/generate-buyer-list.py --company "NAME" --industry software --revenue 50 --ebitda 10 --output buyers.csv` |
| 4 | Read guides | `cat skills/financial-analysis-core/SKILL.md` |

---

## Example: Value a Lemonade Stand

**The Story:** Your friend Sarah wants to sell her lemonade stand for $10,000. Is that fair?

**Step 1 - Run the tool:**
```bash
python3 skills/financial-analysis-core/scripts/generate-comps.py \
  --target "Sarah's Lemonade" \
  --peers "Mikes Stand,Corner Cart,Park Vendor" \
  --output lemonade.xlsx
```

**Step 2 - Fill in the spreadsheet:**

Open `lemonade.xlsx` and enter:

| Stand | Sales/Year | Profit/Year |
|-------|-----------|-------------|
| Mike's | $20,000 | $5,000 |
| Corner | $15,000 | $3,000 |
| Park | $25,000 | $6,000 |

**Step 3 - Sarah's numbers:**
- Sales: $18,000
- Profit: $4,000

**Step 4 - Read the answer:**
```
Fair price = 4 times yearly profit
Sarah's profit = $4,000
Fair price = $16,000

Sarah is asking = $10,000
✅ GOOD DEAL!
```

---

## Color Guide for Excel Files

When you open the Excel files:

🔵 **BLUE** = Type your numbers here  
⚫ **BLACK** = Automatic calculation (don't touch!)  
🟢 **GREEN** = Link to another sheet

**Rule: Only change BLUE cells!**

---

## What The Numbers Mean

| Word | Simple Meaning |
|------|----------------|
| Revenue | Total money the company makes |
| Profit | Money left after paying bills |
| EBITDA | Profit before certain costs |
| Multiple | How many times profit = value |
| Valuation | What the company is worth |
| Comps | Similar companies to compare |

---

## If You Get Errors

| Error | Fix |
|-------|-----|
| "openpyxl not found" | Run `pip3 install openpyxl` |
| "Permission denied" | Run `chmod +x skills/*/scripts/*.py` |
| "No such file" | Make sure you're in the right folder |

---

## Read More

- **Full tutorial:** `cat skills/SIMPLE-GUIDE.md`
- **Quick reference:** `cat skills/QUICK-REFERENCE.md`
- **Detailed guide:** `cat skills/TUTORIAL.md`

---

## Remember

1. 🎯 Pick what you want to do (value, find buyers, analyze stock, buy business)
2. 🔧 Run the right command
3. 📝 Fill in your information
4. ✅ Read the answer

**Start small, learn as you go!**
