# Detailed Templates

Load this file only when a specific output artifact needs more structure than `SKILL.md` provides.

## Section Template

````markdown
### 2.X Section Title

⭐ ==One-sentence core claim with key terms highlighted==.

**Orientation** (use when the concept is new):
- **Where it sits:** relationship to prior concepts
- **Why it exists:** the problem prior approaches could not solve
- **How it works:** one-sentence mechanism, argument, or method summary
- **Common confusion:** neighboring concept or trap

> Source wording:
> [Preserve the exact source phrase that matters for recognition.]

**Breakdown**

| Term / Move | Concrete meaning |
|---|---|
| ... | ... |

<span style="color:gray">Nuance, boundary condition, or background.</span>

**Worked example** (choose the discipline-appropriate form):
- Quantitative: variables, formula, substitution, result, units
- Technical/code: minimal runnable snippet or API trace
- Humanities/social science: claim, evidence, warrant, limitation
- Law/policy/business: facts, rule/framework, application, decision
- Science/medicine: mechanism, intervention, expected observation, caveat

```quiz
Q: Question stem in the configured quiz language.
A: ...
B: ...
C: ...
D: ...
correct: B
explain: Explanation with distractor analysis.
```
````

## Orientation Examples

Use one short orientation block before dense material. Do not let it replace the actual mechanism.

### Quantitative model

```markdown
- Where it sits: Extends simple average cost into time-phased project control.
- Why it exists: Raw spending cannot tell whether the team bought real progress.
- How it works: Compare earned work against actual cost and planned value.
- Common confusion: CPI is cost efficiency; SPI is schedule efficiency.
```

### Concept pair

```markdown
- Where it sits: Belongs to measurement quality.
- Why it exists: A measurement can be repeatable while still targeting the wrong construct.
- How it works: Separate consistency from correctness.
- Common confusion: Reliable does not automatically mean valid.
```

### Argument/case analysis

```markdown
- Where it sits: Turns evidence into an exam answer.
- Why it exists: Facts alone do not answer "so what?"
- How it works: Claim -> evidence -> warrant -> limitation.
- Common confusion: A quote is not analysis until the warrant explains relevance.
```

## Solutions Mode

Trigger: user asks for "solutions", "answers", "answer key", "worked solution", "exam reference", or equivalent.

Differences from notes mode:

- Suppress quiz generation.
- Each `##` is a problem or prompt.
- Each `###` is a solving phase.
- Cheatsheet content becomes solving patterns and common traps.
- Solving phases do not need quiz/⭐ unless a takeaway is useful.

Template:

````markdown
## Problem N

### Question
> [Problem statement preserved in source wording.]

### Approach
⭐ ==One-sentence solving strategy==.
- **Why this method:** what in the prompt makes this approach appropriate
- **Common trap:** what a student is likely to do wrong

### Step-by-step
1. Define variables/terms.
2. Apply the formula, framework, rule, or argument structure.
3. Substitute evidence/numbers/facts.
4. Interpret the result in the prompt's context.

### Final answer
⭐ ==Final answer with units, decision, or claim==.

> Sanity check: one-line verification of sign, units, logic, or scope.
````

## Mock Exam Mode

Trigger: explicit mock/practice exam request, or `mockExam.enabled = true` plus a practice signal.

Default structure:

```markdown
# Course — Mock Exam

> Time limit, allowed materials, and scoring assumptions.

## Q1: Multiple Choice [N × pts]

> [!question] 1. <topic>
> Question stem.
> A. ...
> B. ...
> C. ...
> D. ...
>
> > [!success]- Answer
> > **X**. Explanation.

## Q2: Quantitative / procedural scenario [pts]

### (a) Setup [pts]
...

> [!success]- Answer
> Worked steps.

## Q3: Concept comparison / mechanism [pts]

## Q4: Case / essay / application [pts]

## Self-grading rubric

| Q | Easy points | Killer trap |
|---|---|---|
| ... | ... | ... |
```

Mock exam quality rules:

- Solve quantitative questions yourself before delivery.
- Pick numbers that produce clean arithmetic unless the exam intentionally tests approximation.
- For at least 5 MC questions, keep A/B/C/D each in the 15-35% band.
- Every distractor must represent a real misconception.

## Cheatsheet Templates

Prefer filled-in templates over concept dumps.

### Quantitative template

```markdown
**Metric diagnosis — worked template**

| Given | Compute | Interpretation | Action |
|---|---|---|---|
| `EV = 80`, `AC = 100`, `PV = 90` | `CPI = 0.80`; `SPI = 0.89` | Over budget and behind schedule | Cost owner audits overruns; schedule owner checks blocked work. |

Procedure: compute -> compare threshold -> diagnose -> name owner/action.
```

### Concept comparison template

```markdown
**Neighboring concepts**

| Pair | Difference test | Example |
|---|---|---|
| Reliability vs validity | Consistent, or correct? | A scale can repeat the same wrong value: reliable but invalid. |
```

### Case / essay template

```markdown
**Claim-evidence-warrant-limitation**

| Move | Fill it |
|---|---|
| Claim | One-sentence answer to the prompt. |
| Evidence | One concrete fact, number, quote, or observation. |
| Warrant | Why that evidence supports the claim. |
| Limitation | Boundary condition, uncertainty, or counterargument. |
```

### Model / optimization template

For LP, optimization, or formal model problems, make the setup self-contained:

- Indices and sets
- Parameters with units
- Decision variables and domains
- Objective
- Constraints with quantifiers
- One feasibility or sanity check

## LaTeX Cheatsheet Mode

Only use when the user asks for a printable PDF/LaTeX cheatsheet.

- Use `\documentclass[9pt,a4paper]{extarticle}` with `multicols*{2}`.
- Use compact boxes for formulas and templates.
- After compile, run `pdftotext` and compare rendered section count with source section count.
- Check page count with `pdfinfo`.
- If over budget, trim low-priority concept lists first, not worked templates.

Common pitfalls:

- `\end{kb>` typo can silently eat later sections.
- Tall unbreakable boxes inside columns can drop content.
- Math-heavy extraction can be misleading; visually verify the rendered PDF.

