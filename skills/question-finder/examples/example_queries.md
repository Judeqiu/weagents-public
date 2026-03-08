# Question Finder — Example Queries

A reference table mapping natural language student requests to parsed fields and expected behaviour.
The AI should use this to calibrate how to interpret user queries.

---

## Level 1: Simple Subject Requests

| User Says | Subject | Level | Board | Topic | Route |
|-----------|---------|-------|-------|-------|-------|
| "find me maths questions for A-Level" | math | a-level | any | — | PMT → `/maths/a-level/` |
| "gcse chemistry questions" | chemistry | gcse | any | — | PMT → `/chemistry/gcse/` |
| "A-Level biology questions" | biology | a-level | any | — | PMT → `/biology/a-level/` |
| "physics questions" | physics | a-level | any | — | PMT (default to a-level) |

---

## Level 2: Topic-Specific Requests

| User Says | Subject | Level | Topic | Route |
|-----------|---------|-------|-------|-------|
| "find algebra questions for A-Level" | math | a-level | algebra | PMT `/maths/a-level/algebra/` |
| "GCSE rates of reaction questions" | chemistry | gcse | rates of reaction | PMT `/chemistry/gcse/rates-of-reaction/` |
| "integration worksheets A-Level" | math | a-level | integration | PMT + Maths Genie |
| "organic chemistry A-Level topic questions" | chemistry | a-level | organic chemistry | PMT `/chemistry/a-level/organic/` |
| "forces and motion GCSE practice" | physics | gcse | forces | PMT `/physics/gcse/forces/` |
| "genetics questions A-Level biology" | biology | a-level | genetics | PMT `/biology/a-level/genetics/` |

---

## Level 3: Board-Specific Requests

| User Says | Subject | Level | Board | Route |
|-----------|---------|-------|-------|-------|
| "AQA A-Level maths questions" | math | a-level | aqa | PMT (AQA filter) + Google `site:aqa.org.uk` |
| "OCR GCSE biology past papers" | biology | gcse | ocr | OCR website |
| "Edexcel A-Level physics" | physics | a-level | edexcel | Edexcel/Pearson website |
| "Cambridge IGCSE chemistry" | chemistry | igcse | caie | Easy Paper + PMT |

---

## Level 4: Past Paper Requests

| User Says | Subject | Year | Board | Paper | Route |
|-----------|---------|------|-------|-------|-------|
| "CAIE Physics 2023 paper 2" | physics | 2023 | caie | 2 | Easy Paper (code 9702) |
| "Cambridge maths past papers" | math | — | caie | — | Easy Paper (code 9709) |
| "CAIE Chemistry 9701 Oct/Nov 2022 paper 1" | chemistry | 2022 | caie | 1 | Easy Paper (code 9701, session=w) |
| "A-Level maths past papers last 5 years" | math | 2019-2024 | any | — | PMT past papers section |

---

## Level 5: International / Other Systems

| User Says | Subject | Level | Route |
|-----------|---------|-------|-------|
| "SAT math practice questions" | math | sat | Khan Academy |
| "AP Chemistry practice" | chemistry | ap | Khan Academy |
| "IB Biology topic 6" | biology | ib | Google fallback → `site:ibo.org` or Khan Academy |
| "IB Math HL integration questions" | math | ib | Google fallback |
| "GRE quantitative reasoning practice" | math | gre | Khan Academy + Google fallback |

---

## Level 6: Ambiguous Requests → How to Clarify

If the request is very vague, still attempt a search but also ask for clarification.

| User Says | Assumption Made | Clarification to Ask |
|-----------|----------------|---------------------|
| "find me some questions" | — | "What subject and level? (e.g. A-Level maths, GCSE physics)" |
| "maths questions" | level=a-level | "Is this A-Level or GCSE maths?" |
| "chemistry past papers" | board=caie, level=a-level | "Which board? (CAIE, AQA, OCR, Edexcel?)" |
| "help me with algebra" | — | This is not a question-finding request — answer it directly |

---

## Output Format Examples

### Example 1: Topic Questions

**User:** "Find me A-Level maths integration questions"

**Expected response:**
```
## 📚 Found 5 resources for Maths A-Level (Integration)

| # | Title | Source | Link |
|---|-------|--------|------|
| 1 | PMT — Maths A-Level Integration Questions | physicsandmathstutor.com | https://www.physicsandmathstutor.com/maths/a-level/integration/ |
| 2 | Maths Genie — Integration Revision | mathsgenie.co.uk | https://www.mathsgenie.co.uk/alevel-integration.html |
| 3 | Save My Exams — A-Level Maths Integration | savemyexams.com | https://www.savemyexams.com/search/?q=a-level+maths+integration |

> **Tip:** PMT includes both topic questions and full past papers. Try the mark schemes alongside to self-check your work.
```

---

### Example 2: Past Paper

**User:** "CAIE Physics 9702 2023 paper 2"

**Expected response:**
```
## 📚 Found CAIE Physics Paper — 2023

| # | Title | Source | Link |
|---|-------|--------|------|
| 1 | Easy Paper — CAIE Physics 9702 2023 | easy-paper.com | https://easy-paper.com/papersearch?q=9702+2023 |
| 2 | PMT — A-Level Physics Past Papers | physicsandmathstutor.com | https://www.physicsandmathstutor.com/physics/a-level/past-papers/ |

> **Tip:** Use the `easy-paper-download` skill to automate the PDF download. Mark scheme (MS) is usually available alongside the question paper (QP).
```

---

## Common Subject/Level Synonyms

| User Phrase | Maps To |
|-------------|---------|
| "A levels", "A Levels", "AS level" | level: a-level |
| "GCSE", "GCSEs" | level: gcse |
| "Cambridge", "CIE" | board: caie |
| "Edexcel", "Pearson" | board: edexcel |
| "maths", "math", "mathematics" | subject: math |
| "bio" | subject: biology |
| "chem" | subject: chemistry |
| "phys" | subject: physics |
| "econ" | subject: economics |
| "further maths", "FM" | subject: further-maths |
| "CS", "comp sci" | subject: computer-science |
