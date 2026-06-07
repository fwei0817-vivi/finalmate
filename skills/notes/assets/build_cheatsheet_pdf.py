#!/usr/bin/env python3
"""Build a multi-column PDF cheatsheet from a Markdown source.

Pipeline:  cheatsheet.md
   └─[pandoc --mathjax]──► HTML fragment (math kept inline as $...$)
        └─[wrap in template]──► standalone HTML
              ├─ KaTeX CDN auto-render
              ├─ @page Letter + tight margins
              ├─ <section class="page"> per physical page
              └─ column-count: 2 (or 3) + column-rule
                  └─[Chrome headless --print-to-pdf]──► cheatsheet.pdf

How to use:
    1. Drop this file into your project (anywhere is fine; defaults assume
       it lives one level below the project root, e.g. <project>/code/).
    2. Put your source at <project>/notes/cheatsheet.md with the structure:

         <!-- cheatsheet:start -->
         ## 📋 Page 1 — ...
         ### 1 · Topic
         #### 1.1 Sub-topic
         ...
         <!-- cheatsheet:end -->

         <!-- cheatsheet:start -->
         ## 📋 Page 2 — ...
         ...
         <!-- cheatsheet:end -->

    3. Run:  python3 code/build_cheatsheet_pdf.py
       (or pass --md / --pdf / --pages / --columns to override defaults).

Requirements (all standard on macOS):
    - pandoc on $PATH
    - Google Chrome at the macOS default location
    - (optional) pdftoppm for visual verification

Tuning levers, in order of impact:
    1. body font-size  (default 8.3pt; raise if sparse, lower if overflows)
    2. column count    (--columns 2 default; 3 only if math is sparse)
    3. h3/h4 margins   (top/bottom; trim by 1pt each to claw back ~5%)
    4. @page margin    (already aggressive at 0.32–0.38in)

See <skill>/references/cheatsheet_pdf.md for design discipline and
hierarchy validation checklist.
"""
from __future__ import annotations
import argparse, pathlib, re, subprocess, sys


CHROME_DEFAULT = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def parse_args() -> argparse.Namespace:
    here = pathlib.Path(__file__).resolve()
    project = here.parents[1]
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--md",   default=str(project / "notes" / "cheatsheet.md"),
                   help="Markdown source path")
    p.add_argument("--html", default=str(project / "notes" / "cheatsheet_print.html"),
                   help="Intermediate HTML output path")
    p.add_argument("--pdf",  default=str(project / "notes" / "cheatsheet.pdf"),
                   help="Final PDF output path")
    p.add_argument("--pages",   type=int, default=2,
                   help="Number of physical pages expected (informational only)")
    p.add_argument("--columns", type=int, default=2, choices=(1, 2, 3),
                   help="Number of columns per page")
    p.add_argument("--font-size", type=float, default=8.3,
                   help="Body font size in pt; raise if sparse, lower if overflows")
    p.add_argument("--title",
                   default="Course · Final Cheatsheet",
                   help="Title shown at the top of page 1")
    p.add_argument("--subtitle",
                   default="Letter 8.5×11 · ⭐ key · 🅐🅑 arbitrage · 📐 procedure",
                   help="Subtitle line under the title")
    p.add_argument("--chrome", default=CHROME_DEFAULT,
                   help="Path to Google Chrome binary")
    return p.parse_args()


# ---------- 1. pandoc: MD → HTML fragment, keep $...$ for KaTeX ----------

def md_to_html_fragment(md_path: pathlib.Path) -> str:
    out = subprocess.run(
        ["pandoc", str(md_path),
         "-f", "markdown+tex_math_dollars+raw_html+pipe_tables",
         "-t", "html", "--mathjax"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout


def split_pages(fragment: str, max_pages: int = 8) -> list[str]:
    """Split fragment into per-page HTML chunks at `## 📋 Page N` h2 markers.

    The h2 itself is stripped from each chunk — physical page breaks come
    from <section class="page"> wrapping plus CSS `break-before: page`.
    """
    # Strip top-level <h1> (rendered separately as a title bar)
    fragment = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", fragment, count=1, flags=re.S)

    chunks = [fragment]
    for n in range(2, max_pages + 1):
        marker = re.compile(rf'<h2[^>]*>📋 Page {n}[^<]*</h2>')
        tail = chunks[-1]
        m = marker.search(tail)
        if not m:
            break
        chunks[-1] = tail[: m.start()]
        chunks.append(tail[m.start():])

    # Strip the page-marker h2 from every chunk
    cleaned = []
    for ch in chunks:
        ch = re.sub(r'<h2[^>]*>📋 Page \d+[^<]*</h2>\s*', "", ch, count=1)
        cleaned.append(ch)
    return cleaned


# ---------- 2. wrap into print-ready HTML ----------

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[
    {left:'$$',right:'$$',display:true},
    {left:'\\[',right:'\\]',display:true},
    {left:'$',right:'$',display:false},
    {left:'\\(',right:'\\)',display:false}
  ], throwOnError:false, strict:'ignore'});"></script>
<style>
@page { size: letter; margin: 0.38in 0.32in; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; }
body {
  font-family: "Helvetica Neue", "PingFang SC", "Hiragino Sans GB",
               "Songti SC", Arial, sans-serif;
  font-size: __FONT_SIZE__pt; line-height: 1.26; color:#111;
}
.title-bar {
  text-align:center; margin:0 0 5pt 0;
  border-bottom: 1.4pt solid #0033aa; padding-bottom:2pt;
}
.title-bar h1 { font-size:12pt; margin:0; color:#0033aa; font-weight:700; letter-spacing:0.2pt; }
.title-bar .sub { font-size:8pt; color:#555; margin-top:1pt; }

.page {
  column-count: __COLUMNS__;
  column-gap: 14pt;
  column-rule: 0.5pt solid #cfd5e0;
}
.page + .page { break-before: page; padding-top:4pt; }

/* convention blockquote at the very top, spans all columns of page 1 */
.page:first-of-type > blockquote:first-child {
  column-span: all; font-size:7.8pt; padding:2.5pt 8pt; margin:0 0 5pt 0;
  background:#f6f8fc; border-left:2.5pt solid #0033aa;
}

h2 { display:none; }                  /* page-title placeholders */

/* h3 = section: "3 · Forwards" — colored bar */
h3 {
  font-size:9.4pt; margin:5pt 0 2pt 0;
  color:#fff; background:#0033aa;
  padding:1.6pt 5pt 1.4pt 5pt; border-radius:2pt;
  font-weight:700; letter-spacing:0.15pt;
  break-after: avoid; break-inside: avoid;
}
h3:first-child { margin-top:0; }

/* h4 = subsection: "3.2 Arbitrage detection" — left bar */
h4 {
  font-size:8.6pt; margin:2.5pt 0 1pt 0;
  color:#0033aa; font-weight:700;
  border-left:2pt solid #0033aa; padding-left:4pt;
  break-after: avoid; break-inside: avoid;
}

p { margin:1.5pt 0; }
ul, ol { margin:1pt 0; padding-left:14pt; }
li { margin:0.5pt 0; }

table { border-collapse:collapse; width:100%; font-size:7.9pt;
        margin:2pt 0; break-inside: avoid; }
th, td { border:0.4pt solid #888; padding:1.5pt 3pt; vertical-align:top;
         word-wrap: break-word; }
th { background:#eef1f8; font-weight:700; }

code { background:#f4f4f4; padding:0 2pt; border-radius:2pt; font-size:8pt;
       font-family:"SF Mono", Menlo, Consolas, monospace; }

blockquote { margin:2pt 0; padding:1.5pt 6pt; border-left:2pt solid #999;
             color:#444; font-size:8.2pt; }
hr { border:none; border-top:0.4pt dashed #aaa; margin:3pt 0; }
strong { color:#c0392b; }

.katex { font-size:0.98em; }
.katex-display { margin:1.5pt 0 !important; }
.katex-display > .katex { white-space: normal; }

table, blockquote, h3, h4 { break-inside: avoid; }
</style>
</head>
<body>
<div class="title-bar">
  <h1>__TITLE__</h1>
  <div class="sub">__SUB__</div>
</div>
__PAGES__
</body>
</html>
"""


def render_html(pages: list[str], *, title: str, subtitle: str,
                columns: int, font_size: float) -> str:
    sections = "\n".join(f'<section class="page">\n{p}\n</section>' for p in pages)
    return (TEMPLATE
        .replace("__TITLE__", title)
        .replace("__SUB__", subtitle)
        .replace("__COLUMNS__", str(columns))
        .replace("__FONT_SIZE__", f"{font_size:g}")
        .replace("__PAGES__", sections)
    )


# ---------- 3. Chrome headless print to PDF ----------

def html_to_pdf(html_path: pathlib.Path, pdf_path: pathlib.Path, chrome: str) -> None:
    subprocess.run([
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        # KaTeX is defer-loaded from a CDN; give it ample time to render.
        "--virtual-time-budget=10000",
        "--run-all-compositor-stages-before-draw",
        f"file://{html_path}",
    ], check=True)


def page_count(pdf_path: pathlib.Path) -> int | None:
    """Return PDF page count via macOS `mdls`, or None if unavailable."""
    try:
        out = subprocess.run(
            ["mdls", "-name", "kMDItemNumberOfPages", str(pdf_path)],
            capture_output=True, text=True, check=True,
        ).stdout
        m = re.search(r"=\s*(\d+)", out)
        return int(m.group(1)) if m else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def main() -> int:
    args = parse_args()
    md_path = pathlib.Path(args.md).resolve()
    html_path = pathlib.Path(args.html).resolve()
    pdf_path = pathlib.Path(args.pdf).resolve()

    if not md_path.exists():
        sys.stderr.write(f"error: source not found: {md_path}\n")
        return 2

    fragment = md_to_html_fragment(md_path)
    pages = split_pages(fragment)
    if not pages or all(not p.strip() for p in pages):
        sys.stderr.write("error: no page content found after split\n")
        return 2

    html = render_html(pages,
                       title=args.title, subtitle=args.subtitle,
                       columns=args.columns, font_size=args.font_size)
    html_path.write_text(html, encoding="utf-8")
    print(f"[1/2] HTML written: {html_path}")

    html_to_pdf(html_path, pdf_path, args.chrome)
    print(f"[2/2] PDF written:  {pdf_path}")

    n = page_count(pdf_path)
    if n is not None:
        flag = "✓" if n == args.pages else "⚠"
        print(f"     {flag} pages: {n} (expected {args.pages})"
              + (" — adjust --font-size if mismatched" if n != args.pages else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
