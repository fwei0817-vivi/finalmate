# Cheatsheet → PDF (2-column print layout)

Reusable pipeline + design discipline for turning `cheatsheet.md` into a printable
multi-column PDF cheatsheet. Load when the user asks for a PDF cheatsheet, crib
sheet, formula sheet, or "make this printable / multi-column".

## When to load this

- User says "PDF", "print", "two/three columns", "crib sheet", "8.5×11", "Letter".
- User wants the aggregated `cheatsheet.<ext>` produced in Step 6 to be a *printable*
  artifact, not just an editable Markdown file.

## Pipeline at a glance

```
cheatsheet.md
  └─[pandoc --mathjax]──► HTML fragment (raw $...$ math kept inline)
       └─[wrap in template]──► standalone HTML
             ├─ KaTeX CDN auto-render
             ├─ @page Letter + margins
             ├─ <section class="page"> per physical page
             └─ column-count: 2 (or 3) + column-rule
                 └─[Chrome headless --print-to-pdf]──► cheatsheet.pdf
```

Three external tools, all standard on macOS:

- `pandoc` (Markdown → HTML fragment, keeps math as `$...$`)
- `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` (headless print-to-pdf)
- `pdftoppm` (poppler, optional — for verifying page count and visual layout)

KaTeX is pulled from a CDN at print time; no local install.

## Hard rules (learned from iteration)

These override the generic Step 6 cheatsheet discipline when producing a printable
PDF. They came from real user feedback in a finance final-exam build.

1. **Abstract procedures, not numerical examples.** Each problem type gets a
   numbered ①②③④⑤ step list (the "procedure"). Do not include worked numerical
   examples — they bloat the page and aren't reusable. Concrete examples belong
   in the per-lecture notes; the cheatsheet is a *procedure reference*.

   - ✅ "📐 ① compute $F^*$ ② compare with market $F$ ③ if $F>F^*$ run 🅐 ④ verify
     0 today, $>0$ at $T$"
   - ❌ "Worked: $S=40, r=5\%$ quarterly → $F^*=40.50$ < 43 → profit \$2.50"

2. **Three-tier visual hierarchy.** A dense cheatsheet without clear levels looks
   like a wall of text. Enforce three distinct visual treatments:

   | Level | Markdown | Rendered as |
   |---|---|---|
   | Section (numbered topic) | `### 3 · Forward Contracts` | white text on colored bar, bold |
   | Subsection (`N.M` numbered) | `#### 3.2 Arbitrage detection` | colored text + left border |
   | Atomic concept | `**Bull call spread**` | inline bold, accent color |

   The page-title `##` is hidden via CSS (`display: none`) — physical page breaks
   come from `<section class="page">` + `break-before: page`, not from `<h2>`.

3. **Exam-source language preserved.** The cheatsheet is a recognition tool at
   exam time. Even if the user's `outputLang` is Chinese, if the exam is given in
   English, write the cheatsheet in **English** (or at least keep all formulas,
   procedures, and arbitrage labels in the exam language). Ask if unsure.

4. **HW-coverage pass before finalizing.** Before writing the final cheatsheet,
   scan the user's homework directory (typically `HW/` or `homework/`). Real
   exams test what HWs test. Dispatch an Explore subagent if there are >5 HW
   PDFs — read assignments + solutions to extract problem types, then update the
   cheatsheet to cover any gap. Topics commonly missed from lecture-only review:
   bounds/inequalities, immunization, NPV/IRR, combination strategies (spreads,
   butterflies), basis risk, power contracts $S^k$, full Greek tables.

5. **Page-fill heuristic: 90–98%.** A 60% full cheatsheet feels lazy; a 100% full
   one risks losing the last line. After rebuilding, check page count with
   `mdls -name kMDItemNumberOfPages` or `pdftoppm`. Iterate font / margins until
   the user's page budget is exactly hit. The font on `body` is the single biggest
   lever — typical range 8.3pt–9.0pt for Letter 2-column.

## File layout (suggested, not required)

```
<project>/
  notes/
    cheatsheet.md            # source
    cheatsheet.pdf           # final, 2 pages
    cheatsheet_print.html    # intermediate HTML (useful for debugging)
  code/
    build_cheatsheet_pdf.py  # reusable build script (see below)
```

## Markdown source structure

```markdown
# <Course> Cheatsheet (Lec ...)

> ⭐ must-memorize · 🅐🅑 arbitrage routes · 📐 step-by-step procedure · 🔥 importance.

<!-- cheatsheet:start -->
## 📋 Page 1 — <bucket A> · <bucket B> · ...
### 1 · <Topic group> (Lec X–Y, HW N)
#### 1.1 <Sub-topic>
- key fact / formula with $\boxed{...}$ marker.
- 📐 ① ... ② ... ③ ...

#### 1.2 <Next sub-topic>
...
<!-- cheatsheet:end -->

<!-- cheatsheet:start -->
## 📋 Page 2 — <bucket C> · <bucket D> · ...
### 5 · <Topic group>
#### 5.1 ...
...
<!-- cheatsheet:end -->
```

Page splits are physical: each `## 📋 Page N` lives inside its own
`<!-- cheatsheet:start --> ... <!-- cheatsheet:end -->` block. The build script
also splits on the `## 📋 Page 2` heading to wrap each page in a separate
`<section class="page">` so the column flow restarts and a forced page break
applies.

For arbitrage routines, use a compact procedure *table* (not prose) showing
$t=0$ and $t=T$ cash flows. Tables count as procedure templates, not as
examples — keep them.

## Build script (drop-in)

The full, tuned build script lives at `<skill>/assets/build_cheatsheet_pdf.py`
and supports up to 8 page sections out of the box. Copy it into the user's
project (e.g. as `code/build_cheatsheet_pdf.py`) — defaults assume the script
sits one level below the project root and reads `notes/cheatsheet.md`.

```bash
cp <skill>/assets/build_cheatsheet_pdf.py <project>/code/
python3 code/build_cheatsheet_pdf.py            # uses all defaults
python3 code/build_cheatsheet_pdf.py \
    --md notes/cheatsheet.md \
    --pdf notes/cheatsheet.pdf \
    --pages 2 --columns 2 --font-size 8.3 \
    --title "<Course> Final Cheatsheet" \
    --subtitle "2 pages · ⭐ key · 📐 procedure"
```

Key behaviour the script encodes (do not re-implement from scratch — copy):

- `pandoc -f markdown+tex_math_dollars+raw_html+pipe_tables -t html --mathjax`
  keeps `$...$` intact for KaTeX to render in the browser.
- Strips the top-level `<h1>` (the project title is rendered separately in the
  title bar) and the per-page `<h2>📋 Page N</h2>` markers.
- Wraps each page chunk in `<section class="page">` so `column-count` restarts
  per page and `.page + .page { break-before: page }` forces the physical break.
- KaTeX is `defer`-loaded from CDN, so Chrome must be invoked with
  `--virtual-time-budget=10000` (~10s) to let math render before printing.
- After printing, calls `mdls` to report actual page count vs `--pages`, with
  a ⚠ flag if they disagree — a clear signal to bump `--font-size`.

## CSS tuning levers (in order of impact)

1. **`body { font-size }`** — biggest lever. 8.3pt fits dense 2-column Letter;
   9.0pt is comfortable but harder to fit 2 pages. Step in 0.2pt increments.
2. **`.page { column-count }`** — 2 columns is the safe default. 3 columns
   often breaks long display equations across columns; only use 3 if math is
   sparse.
3. **`h3 { margin }` / `h4 { margin }`** — top/bottom margins; trim by 1pt
   each to claw back ~5% of vertical space.
4. **`@page { margin }`** — already aggressive at 0.32–0.38in. Below this,
   printers may clip.
5. **`line-height`** — 1.26–1.30 sweet spot.
6. **Table `font-size`** — drop tables to 7.9pt independently of body text
   when they contain long Greek formulas.

## Verification loop

After every rebuild, sanity-check:

```bash
mdls -name kMDItemNumberOfPages notes/cheatsheet.pdf
pdftoppm -r 110 -png notes/cheatsheet.pdf /tmp/pgs   # renders each page
```

Read `/tmp/pgs-*.png` to visually confirm:

- Page count matches `cheatsheet.pages` from config.
- No content is clipped at the bottom of the last page.
- No empty bottom-half of any page (page-fill < 80% means content didn't reach).
- KaTeX rendered (math is typeset, not raw `$...$`).
- No column-break inside a table or formula box.

If page count is wrong by exactly 1, the body font-size lever resolves 95% of
cases. If a single formula breaks awkwardly across columns, add
`break-inside: avoid` to its containing element.

## KaTeX gotchas

- KaTeX scripts are `defer`-loaded; Chrome's print is timed by
  `--virtual-time-budget`. **Always pass `--virtual-time-budget=10000`** to give
  CDN load + math render ~10s. Lower values intermittently print before render.
- KaTeX is strict about LaTeX commands. Use `\tfrac` (allowed) over custom
  macros; replace `\dfrac` only where display fractions are needed.
- `&` inside math (`{align*}` etc.) is unsupported — keep math single-line or use
  `\begin{aligned}`.

## Hierarchy validation checklist

After generating, scan the rendered PDF and confirm you can answer "yes" to all:

- [ ] Can a reader spot the 4–8 top-level sections at a glance? (h3 bars)
- [ ] Do the `N.M` subsections form a clear secondary scan order? (h4 left bars)
- [ ] Are the most-tested formulas boxed (`\boxed{}` in math)?
- [ ] Do procedures use ①②③④⑤ enumeration, not prose?
- [ ] Are arbitrage strategies in *tables* with $t=0$ and $t=T$ columns?
- [ ] Does each major topic note the source lecture and HW (e.g., "Lec 13, HW 7")?
- [ ] Have you done the HW-coverage pass? (a one-line answer per HW is enough)
