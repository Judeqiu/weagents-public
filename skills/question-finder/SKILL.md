---
name: question-finder
description: "Use when a user wants to find exam questions, practice problems, or past papers for a subject and level (e.g. A-Level algebra, GCSE chemistry, CAIE past papers, SAT math). Understands natural language requests and routes to the best educational website."
metadata:
  category: "education"
  domains: ["a-level", "gcse", "igcse", "ib", "sat", "ap", "caie", "aqa", "ocr", "edexcel"]
  outputs: ["question-links", "past-paper-links", "topic-worksheets"]
  requires:
    bins: ["python3"]
    skills: ["agent-browser"]
---

# Question Finder

Find exam questions, practice problems, and past papers from curated educational websites.

## When to Use

✅ **Use this skill for:**

- "Find me algebra questions for A-Level"
- "Give me CAIE Physics past papers from 2023"
- "I need GCSE chemistry questions on rates of reaction"
- "Find IB Math HL practice questions on integration"
- "Get me SAT math questions about quadratics"
- Any request to find, search, or retrieve exam/practice questions

❌ **Don't use for:**

- Explaining how to solve a problem (just answer directly)
- Writing original questions (do it without a skill)
- Downloading PDFs (use the `easy-paper-download` skill for CAIE PDFs)

---

## Step-by-Step Workflow

Follow these **5 steps** every time. Do not skip steps.

### Step 1 — UNDERSTAND the User's Intent

Read the user's request and use your own comprehension to identify:

- **Subject** — what are they studying? (maths, physics, chemistry, biology, economics, computer science, etc.)
- **Level** — what qualification? (A-Level, GCSE, IGCSE, IB, SAT, AP, university, etc.). Default to A-Level if unclear.
- **Exam board** — did they specify one? (CAIE/Cambridge, AQA, OCR, Edexcel, IB, College Board, etc.). Leave open if not mentioned.
- **Topic** — a specific chapter or concept? (integration, organic chemistry, genetics, forces, etc.). Leave broad if not stated.
- **Year** — a specific exam year? Default to most recent if not mentioned.
- **Type** — past paper, topic question bank, worksheet, or revision notes? Default to question bank.

> **You are the LLM.** Use natural language understanding — do not pattern-match. A student saying *"I need help with C1 differentiation"* clearly wants A-Level Maths differentiation questions. *"Cambridge chem 2022"* clearly means CAIE Chemistry past papers from 2022. Trust your comprehension; only ask for clarification when genuinely ambiguous.

---

### Step 2 — CHOOSE the Best Site

Based on your understanding of the request, pick the most appropriate site(s) from the registry below. You may use more than one site when they complement each other (e.g. PMT for topic questions alongside Easy Paper for the official past paper).

**Guiding principles:**
- UK A-Level/GCSE across most subjects → prefer **Physics & Maths Tutor** and **Save My Exams**
- Official CAIE past papers → use **Easy Paper** (or delegate to the `easy-paper-download` skill)
- GCSE/A-Level Maths topic worksheets → **Maths Genie** is excellent
- A-Level Maths/Further Maths worked solutions → **Exam Solutions**
- SAT, AP, or US curriculum → **Khan Academy**
- Official board past papers (AQA/OCR/Edexcel) → go directly to the board's own website
- Unusual subject or unsure → **Google** with a `site:` filter on the most relevant site

#### Site Registry

| Site | URL | Best For |
|------|-----|----------|
| **Physics & Maths Tutor (PMT)** | `physicsandmathstutor.com` | A-Level & GCSE — all subjects, UK boards |
| **Save My Exams** | `savemyexams.com` | A-Level & GCSE — revision + topic questions |
| **Easy Paper** | `easy-paper.com/papersearch` | CAIE past papers — search by subject code |
| **Maths Genie** | `mathsgenie.co.uk` | GCSE & A-Level Maths — topic worksheets & past papers |
| **Exam Solutions** | `examsolutions.net` | A-Level Maths & Further Maths — worked solutions |
| **Khan Academy** | `khanacademy.org` | SAT, AP, general K-12 |
| **AQA** | `aqa.org.uk/find-past-papers` | AQA official past papers & mark schemes |
| **OCR** | `ocr.org.uk` | OCR official past papers & mark schemes |
| **Edexcel/Pearson** | `qualifications.pearson.com` | Edexcel official past papers & mark schemes |
| **Google (fallback)** | `google.com` | Any subject not covered above |

---

### Step 3 — SEARCH the Site

Use the approach that best fits the chosen site.

#### Physics & Maths Tutor — Direct URL

PMT organises content by subject and level. Construct a direct URL using lowercase hyphenated slugs:
```
https://www.physicsandmathstutor.com/{subject}/{level}/{topic}/
```
Use `read_url_content` or `browser_subagent` to fetch the page and extract question/worksheet links.

If the direct URL doesn't work, fall back to a Google site-search:
```
site:physicsandmathstutor.com {level} {subject} {topic} questions
```

#### Save My Exams or Khan Academy — Browser Search

These sites are JavaScript-heavy. Use `browser_subagent`:
1. Open the site
2. Find the search bar
3. Type a natural search query
4. Extract result titles and URLs

#### Easy Paper — CAIE Past Papers

Search via:
```
https://easy-paper.com/papersearch?q={subject-code} {year}
```

CAIE subject codes — reference data for lookup:

| Subject | Code |
|---------|------|
| Physics | 9702 |
| Mathematics | 9709 |
| Further Mathematics | 9231 |
| Chemistry | 9701 |
| Biology | 9700 |
| Computer Science | 9618 |
| Economics | 9708 |
| Psychology | 9990 |
| English Language | 9093 |

For automated PDF download, delegate to the `easy-paper-download` skill.

#### Google Fallback

Use `search_web` with a natural query and optional `site:` filter:
```
site:physicsandmathstutor.com A-Level biology genetics questions
```

---

### Step 4 — EXTRACT Results

From the fetched content, extract:
- **Title** of the question set, paper, or worksheet
- **Direct URL** (the actual content page, not a search results page)
- **Brief description** — topic, year, paper number, or any useful context
- **Source site** name

Aim for **5–10 results**. Fewer is fine if that's all that's available.

---

### Step 5 — PRESENT to User

```
## 📚 Found [N] resources for [subject] [level] [topic]

| # | Title | Source | Link |
|---|-------|--------|------|
| 1 | [Title] | [Site] | [URL] |
| 2 | [Title] | [Site] | [URL] |
...

> **Tip:** [Relevant advice — e.g. "The mark scheme is available alongside each paper"]
```

For past papers, also mention: year, session (May/June, Oct/Nov, March), paper number, and whether a mark scheme is available.

---

## Using the Helper Script

A Python CLI script is available for automated searches:

```bash
python3 skills/question-finder/scripts/search_questions.py \
  --subject math \
  --level alevel \
  --topic algebra \
  --board aqa \
  --limit 8
```

The script handles its own programmatic routing. Use `--format json` for structured output.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Returning a search results page URL instead of the actual content URL | Always follow through to the real question page |
| Giving up after one site fails | Try an alternative site or the Google fallback |
| Forgetting to mention mark schemes for past papers | Always note if a mark scheme is available |
| Asking the user to clarify something you can already infer | Trust your comprehension; only ask when truly ambiguous |
