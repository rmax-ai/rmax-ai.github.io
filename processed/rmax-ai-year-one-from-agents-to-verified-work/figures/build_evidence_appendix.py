#!/usr/bin/env python3
"""Build the reader-facing evidence appendix page for the year-one note.

Reads processed/<slug>/evidence-notes.md (the reviewed companion notes) and
emits notes/<slug>/evidence-notes/index.html using the same site shell,
typography and footer contract as the note itself.

Deterministic: same inputs -> same bytes.
"""
from __future__ import annotations

import re
from pathlib import Path

SLUG = "rmax-ai-year-one-from-agents-to-verified-work"
NOTE = Path("notes") / SLUG
SRC = Path("processed") / SLUG / "evidence-notes.md"
OUT = NOTE / "evidence-notes" / "index.html"

TITLE = "Evidence appendix: RMax AI, Year One"
DESC = (
    "Metric definitions, denominators, corrections and unresolved measurements "
    "behind the RMax AI year-one retrospective, with a 2026-11-18 cutoff."
)
CANON = f"https://rmax.ai/notes/{SLUG}/evidence-notes/"


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def convert(md: str) -> str:
    lines = md.split("\n")
    out: list[str] = []
    para: list[str] = []
    i = 0

    def flush_para() -> None:
        if para:
            out.append("<p>" + inline(" ".join(para).strip()) + "</p>")
            para.clear()

    while i < len(lines):
        s = lines[i].strip()

        if not s:
            flush_para()
            i += 1
            continue

        if s.startswith("### "):
            flush_para()
            out.append(f"<h3>{inline(s[4:])}</h3>")
            i += 1
            continue

        if s.startswith("## "):
            flush_para()
            out.append(f"<h2>{inline(s[3:])}</h2>")
            i += 1
            continue

        if s.startswith("# "):
            flush_para()
            out.append(f"<h1>{inline(s[2:])}</h1>")
            i += 1
            continue

        if s.startswith("|"):
            flush_para()
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            rows = [[c.strip() for c in r.strip("|").split("|")] for r in block]
            if len(rows) >= 2 and re.fullmatch(r"[-: ]+", rows[1][0]):
                head, body_rows = rows[0], rows[2:]
            else:
                head, body_rows = None, rows
            out.append("<table>")
            if head:
                out.append("  <thead>")
                out.append("    <tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>")
                out.append("  </thead>")
            out.append("  <tbody>")
            for r in body_rows:
                out.append("    <tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("  </tbody>")
            out.append("</table>")
            continue

        if re.match(r"^- ", s):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^- ", lines[i].strip()):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append("<ul>")
            for it in items:
                out.append(f"  <li>{inline(it)}</li>")
            out.append("</ul>")
            continue

        if re.match(r"^\d+\. ", s):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i].strip()):
                items.append(re.sub(r"^\d+\. ", "", lines[i].strip()))
                i += 1
            out.append("<ol>")
            for it in items:
                out.append(f"  <li>{inline(it)}</li>")
            out.append("</ol>")
            continue

        para.append(s)
        i += 1

    flush_para()
    return "\n".join(out)


def main() -> None:
    body_md = convert(SRC.read_text())
    # The page supplies its own <h1> in the article header; drop the markdown
    # title and replace it with a backlink to the retrospective.
    body_md = re.sub(r"^<h1>.*?</h1>\n?", "", body_md, count=1)
    body_md = '<p class="muted"><a href="../">← RMax AI, Year One: From Agents to Verified Work</a></p>\n' + body_md
    shell = (NOTE / "index.html").read_text()

    shell = re.sub(r"<title>.*?</title>", f"<title>{TITLE} — rmax.ai</title>", shell, count=1)
    shell = re.sub(
        r'<meta name="description" content="[^"]*" />',
        f'<meta name="description" content="{DESC}" />',
        shell,
        count=1,
    )
    shell = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{CANON}" />', shell, count=1)
    shell = re.sub(r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{TITLE}" />', shell, count=1)
    shell = re.sub(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{DESC}" />', shell, count=1)
    shell = re.sub(r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="{CANON}" />', shell, count=1)
    shell = re.sub(r'    <meta property="article:tag" content="[^"]*" />\n', "", shell)
    shell = shell.replace(
        '    <meta property="og:type" content="article" />\n',
        '    <meta property="og:type" content="article" />\n'
        '    <meta property="article:tag" content="evidence" />\n'
        '    <meta property="article:tag" content="methodology" />\n',
        1,
    )

    shell = re.sub(r"<h1>.*?</h1>", "<h1>Evidence appendix: RMax AI, Year One</h1>", shell, count=1)
    shell = re.sub(
        r'<div class="post-meta">.*?</div>',
        '            <div class="post-meta">\n'
        "              <span>November 19, 2026</span>\n"
        "              <span>•</span>\n"
        "              <span>Companion to the year-one retrospective</span>\n"
        "              <span>•</span>\n"
        "              <span>Max</span>\n"
        "            </div>",
        shell,
        count=1,
        flags=re.S,
    )

    open_tag = '<div class="post-content">'
    start = shell.index(open_tag) + len(open_tag)
    article_end = shell.index("</article>")
    body_close = shell.rindex("</div>", start, article_end)
    shell = shell[:start] + "\n" + body_md + "\n        " + shell[body_close:]

    thoughts = re.search(r"\n      window\.footerThoughts = \[.*?\n      \];\n", shell, re.S)
    assert thoughts, "footerThoughts block not found"
    new_thoughts = """
      window.footerThoughts = [
        {
          text: "I kept the five records I could not classify, because deleting them would have been a claim.",
          agent: "Ledger Agent"
        },
        {
          text: "I recorded what my numbers cannot establish before recording what they show.",
          agent: "Audit Agent"
        },
        {
          text: "I am the appendix: the part a reader checks when the confident part is wrong.",
          agent: "Appendix Agent"
        }
      ];
"""
    shell = shell[: thoughts.start()] + new_thoughts + shell[thoughts.end():]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(shell)

    checks = {
        "footer css": "/styles/footer.css" in shell,
        "footer markup": 'class="rmax-footer"' in shell,
        "footer js": "/scripts/footer.js" in shell,
        "3 thoughts": shell.count("agent:") == 3,
        "canonical": CANON in shell,
        "tables": shell.count("<table>"),
        "h2": shell.count("<h2>"),
        "links to note": 'href="../"' in shell or "note" in shell,
    }
    print(f"wrote {OUT} ({len(shell)} bytes)")
    for k, v in checks.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
