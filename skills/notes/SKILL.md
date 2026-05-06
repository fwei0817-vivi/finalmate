---
name: notes
description: Use when writing or rewriting lecture notes, study guides, exam-prep materials, cheatsheets, mock exams, worked solutions, or interactive HTML study notes from course/source material. Supports Markdown/Obsidian output and interactive HTML with quizzes, self-assessment, highlights, progress, and AI-ready question prompts. Designed for multi-discipline learning and source-language exam recognition.
---

# FinalMate · Notes

Create dense, pyramid-structured study notes for university, professional, or self-study material. Preserve the source terminology that a learner must recognize, while explaining in the learner's preferred output language.

## Step 1 — Resolve Config

Be quiet about config. Do not print config JSON or "using cached config" messages unless the user asks.

Read `<project>/.notes-config.json` first.

- If the cache covers this request, reuse it silently.
- If the user says "reconfigure" / "change config" / "重新配置", ask only affected fields and overwrite them.
- If one field is missing for this request, ask only that field.
- Inline overrides like "make this HTML", "quiz in Spanish", or "exam mode only" satisfy the relevant fields.

Before writing, scan the output directory, default `<project>/notes/`, for existing files. If a naming pattern already exists, match it. Defaults below are only for empty folders.

### Required Fields

Ask only what's missing. Most fields can be inferred from the user's message or source filenames.

| Field | Default | Ask user when... |
|---|---|---|
| `depth` | `"feynman"` | Always ask once per project; this is the only mandatory first-run question |
| `format` | `"A"` Markdown/Obsidian | User requests HTML, web, interactive, or both |
| `course` | inferred from filename/title | Source name is ambiguous |
| `outputLang` | user's language, else `"en"` | User writes in multiple languages and preference is unclear |
| `sourceLang` | inferred from source | Source material has multiple languages and exact quote language matters |
| `quizLang` | `sourceLang` for exam prep, else `outputLang` | Recognition language is unclear |
| `examFormat` | `"mixed"` | User says summary-only, essay-only, MC-only, quantitative-only, etc. |
| `cheatsheet.enabled` | `false` | User asks for cheatsheet, crib sheet, formula sheet, quick review |
| `mockExam.enabled` | `false` | User asks for mock exam, practice exam, 出题, 模考 |

Legacy compatibility: if cache contains `nativeLang`, treat it as `outputLang` and rewrite the cache with `outputLang`. `classes` is historical only; never treat a new class/topic as a conflict.

### Cache Schema

Save answers to `<project>/.notes-config.json`:

```json
{
  "depth": "feynman",
  "format": "A",
  "course": "Course or source title",
  "outputLang": "en",
  "sourceLang": "en",
  "quizLang": "en",
  "examFormat": "mixed",
  "cheatsheet": { "enabled": false, "pages": 0 },
  "mockExam": { "enabled": false }
}
```

### Depth Modes

Ask once, in the user's language:

> Is this new material or mostly review?
> (a) New material: start from intuition and prereqs  ← default
> (b) Review: focus on exam traps and edge cases

- `"feynman"`: under each `##`, prepend `### 0. Intuition` with 3-5 concise lines: everyday analogy, simplest worked case, why it matters, prereq links to existing notes when available, and likely misconceptions. Keep the rigor; add an on-ramp.
- `"exam"`: skip intuition and start with the takeaway. Use more aggressive distractors and trap analysis.

## Step 2 — Writing Principles

These override default writing habits:

1. Pyramid: each section starts with a conclusion. Mark exam-level takeaways with `⭐`.
2. Positive phrasing: state what something is or does, not only what it is not.
3. Decompose abstractions in-place: vague terms such as "heavy", "limited", "robust", or "invisible" need concrete meaning in the same paragraph.
4. Problem -> intervention -> resolution: for any mechanism, argument, method, law, model, or workflow, explain the normal case, where the problem appears, and how the method resolves it at the same step.
5. Discipline-appropriate worked examples: use runnable code only when code is the natural artifact. Otherwise use calculations, case applications, textual close reading, proof sketches, diagrams, or scenario walkthroughs.
6. Actionable templates over concept lists: cheatsheets and exam prep must provide filled-in templates, worked examples, procedures, formulas, or owner/action specifics, not bare lists of named concepts.

## Step 3 — Structure and Visual Format

Use one file title and two content heading levels only:

```markdown
# Class N: <Topic>
## 1. Knowledge Module 🔥🔥🔥
### 1.1 Sub-concept
```

`##` headings must include a rating:

- `🔥🔥🔥` = must-know, repeated, likely assessed, or central to later topics
- `🔥🔥` = high-frequency or important prerequisite
- `🔥` = useful context/background

Each ordinary `###` must include:

- 1 `⭐` takeaway, max 2
- At least one source quote when source wording matters
- At least one quiz when `examFormat` includes MC/mixed
- A worked example when the concept is procedural, quantitative, argumentative, or application-based

Meta-section exemptions: `## 📋 Cheatsheet` and solutions-mode phases do not need rating, quiz, or self-assessment.

### Visual Syntax

| Markdown source | Mode A | Mode B | Use |
|---|---|---|---|
| `⭐` | text marker | text marker | Core takeaway |
| `==term==` | Obsidian highlight | `<mark>` | Must-remember term |
| `**bold**` | bold | bold | Emphasis |
| `<span style="color:gray">…</span>` | gray | gray | Supplementary nuance |
| `> blockquote` | quote | styled quote | Source wording |
| `> [!question]` | quiz callout | converted to quiz card | Mode A source quiz |
| ` ```quiz ` | inert unless converted | clickable quiz card | Mode B quiz |
| ` ```mermaid ` | rendered if supported | rendered | Diagram |
| `<!-- cheatsheet:start/end -->` | harmless comments | cheatsheet toggle anchors | Cheatsheet |

### Renderer Pitfalls

1. No literal `=` inside `==term==`. Use `==EV==: $EV = \% \times BAC$`, not `==EV = % × BAC==`.
2. Use display math only when the user's existing notes already support it; otherwise prefer inline `$...$`.
3. Use `×` for multiplication, not bare `*`, unless inside code.
4. Put HTML comments on their own lines, never inside Markdown tables.
5. Mode B content is JSON-embedded. Replace `{{MD_CONTENT_JSON}}` with `JSON.stringify(markdown).replace(/<\//g, '<\\/')`.
6. Mode B labels are JSON-embedded. Replace `{{UI_LABELS_JSON}}` with a JSON object; use `{}` for default English labels.
7. Never paste raw Markdown into `template.html`; raw `</script>` inside examples will truncate the page.

Render and visually verify HTML before delivery whenever possible.

## Step 4 — Output Modes

### Mode A: Markdown / Obsidian

- Default file: `class<N>.md`
- Quiz syntax: Obsidian callout
- Self-assessment slot required at the end of every leaf `###`

```markdown

- [ ] ✅ I understand this section

> [!question]- ❓ Remaining question
> My question:
```

Translate the self-assessment labels to `outputLang`.

### Mode B: Interactive HTML

- Default file: `class<N>.html`
- Use `template.html` from this skill directory.
- Replace `{{TITLE}}`, `{{MD_CONTENT_JSON}}`, and `{{UI_LABELS_JSON}}`.
- Use ` ```quiz ` fences for best results; Obsidian quiz callouts are also converted.
- Cheatsheet markers are required when a cheatsheet is present.

Built-in features: clickable quiz cards, per-`###` self-assessment with 🟢/🟡/🔴, green rating soft-dims completed sections, red rating adds a red left border, autosaved question textareas, per-section "Copy Section" AI prompts with full section context, global "Copy Questions" prompt with only saved questions and section titles, sticky highlighter mode (pick a color first, then select text), selection popover shortcuts `1`/`2`/`3`/`4` and `0`, code copy buttons, Mermaid diagrams, KaTeX math, cheatsheet-only toggle, localStorage progress, and dashboard stats.

For non-English HTML UI, set `{{UI_LABELS_JSON}}` with translated labels. Leave missing keys out; the template falls back to English.

### Mode C: Both

Produce both `.md` and `.html`. Keep one Markdown source with ` ```quiz ` fences, then convert quizzes to Obsidian callouts for the `.md` copy.

### File Naming

Match the existing folder convention. If none exists:

| Artifact | Default |
|---|---|
| Notes | `class<N>.<ext>` |
| Solutions | `class<N>_solutions.<ext>` |
| Aggregated cheatsheet | `cheatsheet.<ext>` |
| Mock exam | `mock_exam.<ext>` |

### Convention Block

At the top of every notes file, add a one-paragraph convention block in `outputLang`. Include what ⭐, highlights, quotes, quizzes, and self-assessment mean. For HTML, mention that the widget is rendered automatically by the template.

## Step 5 — Quiz and Anti-Bias Rules

Every ordinary `###` gets at least one quiz when `examFormat` includes MC/mixed.

Mode A format:

```markdown
> [!question] Quiz
> Question stem in the configured quiz language.
> A. ...
> B. ...
> C. ...
> D. ...
>
> > [!success]- Answer
> > **B**. Explanation with distractor analysis.
```

Mode B format:

````
```quiz
Q: Question stem.
A: option
B: option
C: option
D: option
correct: B
explain: One paragraph covering why the answer is right and what misconception at least one distractor targets.
```
````

Quiz language rule: use `quizLang`. For exam prep, this usually means preserving source-language stems/options so recognition practice matches the exam. Explanations may use `outputLang` unless the user wants all quiz material in `quizLang`.

Anti-bias rules:

- For quiz sets with at least 5 questions, keep A/B/C/D roughly balanced.
- Decide the correct letter before drafting options.
- Keep option lengths within about 30% of each other.
- Make distractors plausible misconceptions, not silly wrong answers.
- Put mechanism details in the explanation, not in the correct option.
- Never narrate the balancing process to the user.

## Step 6 — Cheatsheet

Skip unless `cheatsheet.enabled = true`.

Per-class section:

```markdown
<!-- cheatsheet:start -->
## 📋 Cheatsheet (Class N)
<actionable templates with worked examples>
<!-- cheatsheet:end -->
```

Cheatsheet discipline:

- Include 🔥🔥🔥 content; include 🔥🔥 when exam-relevant; omit 🔥 unless it is a crucial connector.
- Allowed: filled-in templates, formula boxes, worked calculations, procedure tables, diagrams, proof skeletons, owner/action plans, close-reading templates.
- Forbidden: bare concept lists, source quotes, quizzes, long prose, full code listings unless the course is specifically code-based.
- For quantitative models, include variables, assumptions, objective/formula, constraints/steps, and a checked numeric example.
- For case/application topics, include scenario, diagnosis, action, owner, and adaptation rule.

After all class notes, produce `cheatsheet.<ext>` by concatenating per-class cheatsheets in order. In Mode B, use the same `template.html` shell.

If `cheatsheet.pages > 0`, estimate page length. If over budget, surface trim suggestions ordered from low-priority to high-priority. Never auto-trim without the user's approval.

## Step 7 — Solutions and Mock Exams

Use solutions mode when the user asks for answers, worked solutions, answer keys, or solved problem sets. Suppress quizzes; the document itself is the answer artifact.

Use mock exam mode when `mockExam.enabled = true` or the user explicitly asks for a mock/practice exam. Include a self-grading rubric. Apply anti-bias rules more strictly because mock exams are graded directly.

See `references/templates.md` for detailed structures and cross-discipline templates.

## Step 8 — Silent Self-Check

Before delivery, silently check:

1. Quiz distribution and option length bias.
2. Renderer sanity: highlight syntax, math syntax, JSON placeholders, quiz cards, Mermaid, and ask/copy buttons.
3. Coverage: each ordinary `###` has takeaway, source quote when needed, quiz when needed, and self-assessment in Mode A.
4. Cheatsheet quality: no concept-list dumps without worked examples/templates.
5. Page budget for cheatsheets.

Completion message: 2-3 concise sentences naming created files and the useful learner-facing features. Do not dump QA logs unless something failed.

## References

Load only when needed:

- `references/templates.md` — detailed section, solutions, mock exam, and cheatsheet templates
- `template.html` — Mode B HTML shell
- `examples/class_demo.md` — Markdown demo source
- `examples/class_demo.html` — rendered HTML demo
