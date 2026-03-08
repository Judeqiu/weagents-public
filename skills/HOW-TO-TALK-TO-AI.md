# How to Talk to the AI Using Financial Skills

What to say to the AI agent and what it will do for you.

---

## The Basic Pattern

**You say:** "I want to [do something]"

**AI does:** Runs the skill, asks questions, creates outputs

**You get:** Files, analysis, recommendations

---

## Skill 1: Valuation (Finding What a Company is Worth)

### What You Can Ask

#### For Comparing to Similar Companies:

**You say:**
> "Help me value TechFlow Inc. It's a software company with $65M revenue and $15M profit."

**AI will:**
1. Ask: "Who are their competitors?"
2. You answer: "CloudSys, DataPro, SoftCore, AppMatrix, CloudNine"
3. AI runs the comps generator
4. AI creates an Excel file
5. AI fills in what data it can find
6. AI tells you what numbers to fill in
7. AI reads the results and tells you: "Based on similar companies, TechFlow is worth $480-520M"

#### For Predicting Future Value:

**You say:**
> "What's TechFlow worth based on future cash flows?"

**AI will:**
1. Ask about growth rates, profit margins
2. You provide estimates or say "use industry average"
3. AI builds the DCF model
4. AI runs scenarios
5. AI tells you: "Based on 15% growth for 5 years, TechFlow is worth $485M"

#### For Quick Valuation:

**You say:**
> "Quick valuation of a coffee shop making $500k profit per year"

**AI will:**
1. Pick similar businesses automatically
2. Run the analysis
3. Give you a range: "Coffee shops typically sell for 3-5× profit, so $1.5-2.5M"

---

## Skill 2: Finding Buyers (M&A)

### What You Can Ask

#### Finding Who Might Buy a Company:

**You say:**
> "Who would want to buy my software company?"

**AI will:**
1. Ask: "How big is your company? Revenue and profit?"
2. You say: "$50M revenue, $10M profit"
3. AI runs buyer list generator
4. AI gives you categories:
   - **Tier 1:** Microsoft, Salesforce, Thoma Bravo (PE firm)
   - **Tier 2:** Mid-size competitors
   - **Tier 3:** Maybe not interested
5. AI explains why each might buy
6. AI suggests: "Start with Tier 1 - reach out to these 8 companies first"

#### For Industry-Specific Search:

**You say:**
> "Find hospital buyers for a $200M medical device company"

**AI will:**
1. Generate buyer list for healthcare industry
2. Include: Stryker, Medtronic, J&J, healthcare PE firms
3. Rank by fit
4. Tell you: "Stryker and Medtronic are most active acquirers in this space"

---

## Skill 3: Equity Research (Stock Analysis)

### What You Can Ask

#### For Earnings Analysis:

**You say:**
> "Apple just reported earnings. What do you think?"

**AI will:**
1. Look up Apple's earnings report
2. Compare to expectations
3. Write an analysis:
   - "Revenue beat by 5%"
   - "iPhone sales stronger than expected"
   - "Guidance raised"
4. Give recommendation: "BUY - thesis intact"

#### For Investment Decision:

**You say:**
> "Should I buy Tesla stock at $200?"

**AI will:**
1. Analyze current valuation
2. Look at growth prospects
3. Assess risks
4. Create thesis document
5. Tell you:
   - Bull case: $300 (+50%)
   - Base case: $240 (+20%)
   - Bear case: $150 (-25%)
   - "Recommendation: WAIT for dip to $180"

#### For Tracking Your Stocks:

**You say:**
> "Track my portfolio: AAPL, TSLA, NVDA. Alert me to any news."

**AI will:**
1. Create tracking list
2. Monitor earnings dates
3. Watch for news
4. Tell you: "NVDA reports earnings next week - here's what to expect"

---

## Skill 4: Private Equity (Buying Businesses)

### What You Can Ask

#### For LBO Analysis:

**You say:**
> "Can we make money buying this manufacturing company for $50M?"

**AI will:**
1. Ask about current profits and growth
2. Build an LBO model
3. Calculate returns
4. Tell you:
   - "If you buy for $50M, fix it up, sell for $80M in 5 years"
   - "You'll make 2.2× your money"
   - "That's 17% per year - good but not great"
   - "Deal is marginal, try to negotiate to $45M"

#### For Investment Memo:

**You say:**
> "Write an investment memo for buying a dental practice chain"

**AI will:**
1. Create memo structure
2. Fill in sections:
   - Market analysis
   - Financial projections
   - Risks
   - Returns
3. Format for investment committee
4. Give you a complete document to present

---

## Conversation Examples

### Example 1: Valuation Conversation

**You:** Help me value my friend's software startup.

**AI:** I'd be happy to help! To value the company, I need some information:
1. What does the company do exactly? (e.g., CRM software, AI tools, etc.)
2. What's their annual revenue?
3. What's their annual profit (or are they pre-profit)?
4. Do you know any public competitors I can compare to?

**You:** It's a CRM for dentists. $2M revenue, $400k profit. Competitors are Salesforce, HubSpot, and some smaller ones like DentalCRM.

**AI:** Great! Let me run a comparable company analysis. I'll compare your friend's company to similar CRM businesses.

*[AI runs generate-comps.py]*

**AI:** Based on my analysis:
- Similar CRM companies sell for 4-6× revenue or 10-15× profit
- Your friend's company: $2M revenue, $400k profit
- Valuation range: $8-12M (revenue method) or $4-6M (profit method)
- **Fair value estimate: $6-8M**

I've created an Excel file (dentist_crm_value.xlsx) where you can adjust assumptions. The blue cells are where you enter data.

### Example 2: M&A Buyer Search

**You:** I need to find buyers for a healthcare IT company.

**AI:** I'll help you identify potential buyers. A few questions:
1. What's the company's annual revenue?
2. Annual profit (EBITDA)?
3. What type of healthcare IT? (e.g., billing software, patient records, telehealth)

**You:** $30M revenue, $6M profit. They do electronic health records.

**AI:** Perfect! Let me generate a list of strategic and financial buyers who are active in healthcare IT.

*[AI runs generate-buyer-list.py]*

**AI:** Here's your buyer list (saved as healthcare_buyers.csv):

**TIER 1 - Contact These First (High Fit):**
- Epic Systems (if they acquire)
- Cerner/Oracle Health
- Veritas Capital (PE firm specializing in healthcare)
- Francisco Partners (healthcare tech investors)

**TIER 2 - Good Backups:**
- Athenahealth
- eClinicalWorks
- Other mid-market PE firms

**Why these?** They all actively buy healthcare IT companies in the $20-50M revenue range. I can help you draft a teaser email to send to Tier 1 buyers.

### Example 3: Stock Analysis

**You:** What do you think about buying NVIDIA at current prices?

**AI:** Let me analyze NVIDIA's valuation and prospects.

*[AI uses equity-research skill]*

**AI:** Here's my analysis:

**THE GOOD:**
- Leading AI chip provider
- Revenue growing 100%+ year-over-year
- Strong competitive position

**THE CONCERNS:**
- Trading at 60× earnings (expensive!)
- Competition from AMD, custom chips
- AI demand might slow down

**VALUATION:**
- Current price: $900
- My fair value: $800-1000
- **It's fairly priced right now**

**RECOMMENDATION:** HOLD
- If you own it: Keep holding
- If you don't: Wait for a dip to $750-800 before buying

I've created a full analysis document (nvidia_analysis.md) with my model.

### Example 4: LBO Analysis

**You:** Can we make money buying a chain of car washes for $5M?

**AI:** Let me analyze this as a leveraged buyout opportunity.

**AI:** First, some questions:
1. What's the annual profit (EBITDA)?
2. How fast is it growing?
3. How much can you put in vs. borrow?

**You:** $800k profit per year. Growing 5% annually. We can put in $2M cash, borrow the rest.

**AI:** Got it! Let me build an LBO model.

*[AI creates LBO model]*

**AI:** Here's the deal analysis:

**THE DEAL:**
- Buy price: $5M
- Your money: $2M (40%)
- Bank loan: $3M (60%)
- Profit: $800k/year growing 5%

**5 YEARS LATER:**
- Profit grown to: $1M/year
- You paid off: $2.5M of the loan
- You sell for: $8M (10× profit)
- After paying remaining loan: You get $6.5M

**YOUR RETURN:**
- Invested: $2M
- Got back: $6.5M
- **Profit: 3.25× your money**
- **Annual return: 26%**

**VERDICT:** ✅ GREAT DEAL!

This beats the 20% minimum we look for. I recommend proceeding. Would you like me to draft an investment memo for your partners?

---

## What the AI Can and Cannot Do

### ✅ The AI Can:

- Run the financial models
- Fill in data it can find
- Ask you for missing information
- Create Excel files and documents
- Give you recommendations
- Explain the results in plain English

### ❌ The AI Cannot:

- Access real-time stock prices (without data connection)
- Make actual investment decisions for you
- Guarantee returns
- Replace a human financial advisor

---

## Tips for Better Conversations

### Be Specific

**Instead of:** "Value this company"

**Say:** "Value TechFlow, a $65M revenue software company. Public comps are Salesforce, Adobe, and Intuit."

### Provide Context

**Instead of:** "Find buyers"

**Say:** "Find buyers for a B2B SaaS company with $50M revenue, 25% profit margins, growing 30% annually."

### Ask for Explanations

**You can ask:**
- "Explain how you got that number"
- "What assumptions did you make?"
- "What could go wrong?"
- "Show me the best and worst case"

### Request Different Formats

**You can say:**
- "Give me the short version"
- "Write this as a formal report"
- "Create a presentation summary"
- "Show me the Excel file"

---

## Quick Reference: What to Say

| I Want To... | Say This... |
|-------------|-------------|
| Value a company | "Help me value [COMPANY]. It's a [TYPE] with $[X]M revenue and $[Y]M profit. Competitors are [A, B, C]." |
| Find buyers | "Who would buy [COMPANY]? It's a [INDUSTRY] company with $[X]M revenue and $[Y]M profit." |
| Analyze a stock | "Should I buy [STOCK] at $[PRICE]?" or "What do you think of [COMPANY]'s earnings?" |
| Buy a business | "Can we make money buying [BUSINESS] for $[PRICE]?" |
| Get a summary | "Give me the quick version" or "Summarize in 3 bullet points" |
| See the details | "Show me the full analysis" or "Walk me through your thinking" |
| Change assumptions | "What if growth is only 10% instead of 15%?" |
| Compare scenarios | "Show me best case, worst case, and base case" |

---

## Example Flows

### Flow 1: Complete Valuation

**You:** Value my software company  
**AI:** What's your revenue and profit? Who are your competitors?  
**You:** $10M revenue, $2M profit. We compete with Asana, Monday.com, and ClickUp  
**AI:** [Runs model] Your company is worth $40-60M based on comparables  
**You:** What if we grow faster?  
**AI:** [Updates model] At 30% growth, worth $70-90M  
**You:** Create a summary for investors  
**AI:** [Creates document] Here's your valuation summary...

### Flow 2: Stock Decision

**You:** Should I buy Apple?  
**AI:** At what price?  
**You:** $180  
**AI:** [Analyzes] It's fairly priced. I see $200 upside, $160 downside  
**You:** What are the risks?  
**AI:** iPhone sales slowing, China competition...  
**You:** Compare to Microsoft  
**AI:** Microsoft has better growth, similar valuation. I'd pick MSFT over AAPL right now

### Flow 3: M&A Process

**You:** Help me sell my business  
**AI:** Tell me about it  
**You:** $25M revenue, healthcare IT, $5M profit  
**AI:** [Finds buyers] Here are 25 potential buyers  
**You:** Who should I contact first?  
**AI:** Start with these 5 strategic acquirers...  
**You:** Draft an email to send them  
**AI:** [Writes email] Here's a teaser email...  
**You:** What's a fair price?  
**AI:** [Values company] $75-100M is the fair range

---

## Remember

1. **The AI does the work** - You just ask questions
2. **Provide numbers when you have them** - Revenue, profit, growth
3. **Ask for explanations** - "How did you calculate that?"
4. **Request files** - "Send me the Excel file"
5. **Iterate** - "What if we change this assumption?"

**Just start talking!** The AI will guide you through it.
