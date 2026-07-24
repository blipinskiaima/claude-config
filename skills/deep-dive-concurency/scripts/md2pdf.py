#!/usr/bin/env python3
"""Convertit un ou plusieurs markdown en un PDF unique, charte AIMA.

Usage: md2pdf.py sortie.pdf source1.md [source2.md ...]
Chaque source supplémentaire démarre sur une nouvelle page.
"""
import sys
from pathlib import Path

import markdown
from weasyprint import HTML, CSS

DST = Path(sys.argv[1])
SRCS = [Path(p) for p in sys.argv[2:]]

CSS_TXT = """
@page {
    size: A4;
    margin: 18mm 16mm 20mm 16mm;
    @bottom-center {
        content: counter(page) " / " counter(pages);
        font-family: 'DejaVu Sans', sans-serif; font-size: 8pt; color: #888;
    }
    @bottom-right {
        content: "AIMA Diagnostics — veille concurrentielle";
        font-family: 'DejaVu Sans', sans-serif; font-size: 7.5pt; color: #bbb;
    }
}
body { font-family: 'DejaVu Sans', sans-serif; font-size: 9.5pt; line-height: 1.45; color: #222; }
h1 {
    color: #1a4480; font-size: 18pt; border-bottom: 2.5pt solid #1a4480;
    padding-bottom: 6pt; margin-bottom: 12pt;
}
h2 {
    color: #1a4480; font-size: 13pt; border-bottom: 0.8pt solid #ddd;
    padding-bottom: 3pt; margin-top: 18pt; page-break-after: avoid;
}
h3 { color: #333; font-size: 10.5pt; margin-top: 12pt; page-break-after: avoid; }
h4 { color: #555; font-size: 9.8pt; page-break-after: avoid; }
a { color: #1a73e8; text-decoration: none; }
code {
    font-family: 'DejaVu Sans Mono', monospace; font-size: 8.3pt; background: #f4f6f8;
    padding: 1pt 3pt; border-radius: 2pt; color: #1a4480;
}
pre {
    font-family: 'DejaVu Sans Mono', monospace; font-size: 7.4pt; line-height: 1.3;
    background: #f7f9fb; border-left: 3pt solid #1a4480; padding: 7pt 9pt;
    white-space: pre-wrap; page-break-inside: avoid;
}
pre code { background: none; padding: 0; color: #222; }
table {
    border-collapse: collapse; width: 100%; margin: 8pt 0;
    font-size: 8.2pt; page-break-inside: avoid;
}
th { background: #1a4480; color: #fff; text-align: left; padding: 4.5pt 6pt; font-weight: bold; }
td { border-bottom: 0.6pt solid #dde3e9; padding: 4pt 6pt; vertical-align: top; }
tr:nth-child(even) td { background: #f7f9fb; }
blockquote {
    border-left: 3pt solid #f9ab00; background: #fffdf5; margin: 8pt 0;
    padding: 6pt 10pt; color: #555; font-size: 8.6pt;
}
hr { border: none; border-top: 0.8pt solid #ddd; margin: 12pt 0; }
strong { color: #111; }
ul, ol { margin: 5pt 0; padding-left: 16pt; }
li { margin: 2.5pt 0; }
.partbreak { page-break-before: always; }
"""

parts = []
for i, src in enumerate(SRCS):
    body = markdown.markdown(
        src.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
    )
    cls = "partbreak" if i else ""
    parts.append(f"<div class='{cls}'>{body}</div>")

html_doc = "<html><head><meta charset='utf-8'></head><body>" + "".join(parts) + "</body></html>"
HTML(string=html_doc, base_url=str(SRCS[0].parent)).write_pdf(str(DST), stylesheets=[CSS(string=CSS_TXT)])
print(f"OK -> {DST}  ({len(SRCS)} partie(s))")
