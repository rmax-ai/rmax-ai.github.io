#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""Generate the annual edition's architecture and task-state SVG pairs."""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SLUG = "rmax-ai-year-one-from-agents-to-verified-work"
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "notes" / SLUG / "figures"
METRICS = json.loads((ROOT / "processed" / SLUG / "metrics.json").read_text())

# ---------------------------------------------------------------- palette ----
BG = "#0b1220"
BORDER = "#1e293b"
TEXT = "#e6eef8"
MUTED = "#94a3b8"
DIM = "#64748b"
BLUE = "#60a5fa"
GREEN = "#34d399"
RED = "#f87171"
FONT = "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"

# Approximate regular character width for the task legend and label-fit check.
EM_REG = 0.515


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg_open(w: int, h: float, title: str, desc: str, tid: str) -> str:
    h = int(round(h))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-labelledby="{tid}-t {tid}-d" '
        f'style="font-family:{FONT}">'
        f'<title id="{tid}-t">{esc(title)}</title>'
        f'<desc id="{tid}-d">{esc(desc)}</desc>'
        f'<rect width="{w}" height="{h}" rx="10" fill="{BG}"/>'
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="none" '
        f'stroke="{BORDER}"/>'
    )


def architecture(mobile: bool) -> str:
    """Lay out the two paths (dispatch and return) across three boundaries."""
    w, h = (380, 640) if mobile else (1080, 420)
    parts = [svg_open(w, h, "From scope to merge approval",
                      "The operator authorizes scope. GitHub and rmax-10 coordinate an attempt. "
                      "Execution, local checks and review return evidence for the merge decision. "
                      "A dashed arrow proposes a new task after disposition.", "architecture")]
    parts.append('<defs><marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" '
                 'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
                 '<path d="M0 0 L8 4 L0 8Z" fill="#d8c7fb"/></marker></defs>')

    def label(x, y, text, size, colour=TEXT, anchor="middle"):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{colour}" '
                     f'text-anchor="{anchor}">{esc(text)}</text>')

    def panel(x, y, width, height, title):
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
                     f'rx="10" fill="#211e38" stroke="#59536f"/>')
        label(x+14, y+28, title, 15 if mobile else 18, "#dcc8ff", "start")

    def node(cx, cy, lines, width):
        parts.append(f'<rect x="{cx-width/2}" y="{cy-26}" width="{width}" height="52" '
                     f'rx="6" fill="#34314e" stroke="#9484ae"/>')
        for i, line in enumerate(lines):
            label(cx, cy+5+(i-(len(lines)-1)/2)*18, line, 14 if mobile else 17)

    def edge(path, dashed=False):
        dash = ' stroke-dasharray="5 5"' if dashed else ""
        parts.append(f'<path d="{path}" fill="none" stroke="#d8c7fb" stroke-width="2"'
                     f'{dash} marker-end="url(#arrow)"/>')

    if mobile:
        panel(8, 10, 364, 132, "1  Human authority")
        panel(8, 168, 364, 151, "2  Durable coordination and state")
        panel(8, 345, 364, 278, "3  Execution and verification")
        node(94, 91, ["Authorize scope"], 140)
        node(284, 91, ["Approve merge", "or adoption"], 140)
        node(94, 246, ["GitHub issue", "rmax-10 dispatch"], 140)
        node(284, 246, ["GitHub PR", "review record"], 140)
        node(94, 429, ["Codex / Droid"], 140)
        node(94, 559, ["Local check"], 140)
        node(284, 559, ["Independent review", "ChatGPT"], 148)
        edge("M94 117 V162 M94 205 V218")
        edge("M94 272 V340 M94 382 V401")
        edge("M65 455 V531")
        edge("M130 533 V457")
        label(153, 498, "retry", 13)
        edge("M164 559 H208")
        edge("M284 533 V274")
        edge("M284 220 V119")
        edge("M240 117 V155 H144 V162 M144 205 V220", True)
        label(190, 151, "proposed follow-up", 12)
    else:
        panel(18, 18, 282, 380, "1  Human authority")
        panel(322, 18, 366, 380, "2  Durable coordination and state")
        panel(710, 18, 352, 380, "3  Execution and verification")
        node(160, 108, ["Authorize scope"], 210)
        node(160, 316, ["Approve merge", "or adoption"], 210)
        node(505, 108, ["GitHub issue", "rmax-10 dispatch"], 248)
        node(505, 316, ["GitHub PR", "review record"], 248)
        node(887, 108, ["Codex / Droid"], 218)
        node(887, 213, ["Local check"], 218)
        node(887, 316, ["Independent review", "ChatGPT"], 218)
        edge("M265 108 H379")
        edge("M629 108 H776")
        edge("M846 134 V185")
        edge("M934 187 V136")
        label(948, 166, "retry", 14, anchor="start")
        edge("M887 239 V288")
        edge("M778 316 H631")
        edge("M381 316 H267")
        edge("M160 290 V214 H505 V136", True)
        label(422, 204, "proposed follow-up", 15)
    parts.append("</svg>")
    return "\n".join(parts)


# --------------------------------------------------------------- figure 3 ----
TASKS = METRICS["tasks"]

TASK_SEGS = [
    ("Succeeded", TASKS["states"]["SUCCEEDED"], GREEN),
    ("Failed", TASKS["states"]["FAILED"], RED),
    ("Cancelled", TASKS["states"]["CANCELLED"], DIM),
    ("Running", TASKS["states"]["RUNNING"], BLUE),
]
def pct(n: int, d: int) -> str:
    return f"{100 * n / d:.1f}%"


def bar(
    x: float, y: float, w: float, h: float, segs: list[tuple[str, int, str]], total: int, mobile: bool,
    *, unit: str, metrics: dict,
) -> tuple[str, list[tuple[str, int, str, float, float]]]:
    """Draw a bar normalised to its own total; return per-segment geometry."""
    if unit == "attempt" and not metrics["attempts"]["complete_composition_chart_allowed"]:
        raise ValueError("attempt partition refused: complete_composition_chart_allowed is false")
    if unit not in {"task", "attempt"} or total <= 0 or sum(value for _, value, _ in segs) != total:
        raise ValueError(f"{unit} states must sum to their positive denominator")
    out, geom, cx = [], [], x
    for label, value, colour in segs:
        sw = w * value / total
        geom.append((label, value, colour, cx, sw))
        out.append(
            f'<rect x="{cx:.1f}" y="{y:.1f}" width="{max(sw, 0.8):.1f}" height="{h:.1f}" fill="{colour}" '
            f'fill-opacity="0.82"/>'
        )
        cx += sw
    if not mobile:
        for label, value, colour, sx, sw in geom:
            if sw < 96:
                continue
            out.append(
                f'<text x="{sx + sw / 2:.1f}" y="{y + h / 2 + 4:.1f}" font-size="11.5" font-weight="600" '
                f'fill="#08101c" text-anchor="middle">{value} {esc(label)}</text>'
            )
    return "".join(out), geom


def legend(x: float, y: float, segs: list[tuple[str, int, str]], total: int, size: float) -> str:
    out, cx = [], x
    for label, value, colour in segs:
        w = 10
        out.append(f'<rect x="{cx:.1f}" y="{y - 8:.1f}" width="{w}" height="{w}" rx="2" fill="{colour}" fill-opacity="0.82"/>')
        out.append(
            f'<text x="{cx + w + 5:.1f}" y="{y:.1f}" font-size="{size}" fill="{MUTED}">'
            f'{esc(label)} <tspan fill="{TEXT}" font-weight="600">{value}</tspan> ({pct(value, total)})</text>'
        )
        cx += w + 5 + (len(label) + len(str(value)) + 9) * size * EM_REG + 14
    return "".join(out)


def figure3_wide() -> str:
    w, pad, head_h = 760, 34, 92
    bar_w, bar_h = w - 2 * pad, 44
    h = 230
    s = [svg_open(
        w, h,
        "Recorded queue task states, without independent delivery verification",
        "Of 1,078 tasks, 809 succeeded, 210 failed, 58 were cancelled and one was running. "
        "Queue states do not establish deployment or use.",
        "f3w",
    )]
    s.append(
        f'<text x="{pad}" y="38" font-size="15" font-weight="600" fill="{TEXT}">What the queue recorded, and what it cannot prove</text>'
        f'<text x="{pad}" y="58" font-size="11" fill="{MUTED}">Task states at the November 18 cutoff. Deployment and use were not verified.</text>'
    )

    y1 = head_h + 26
    s.append(
        f'<text x="{pad}" y="{y1}" font-size="12" font-weight="600" fill="{TEXT}">Recorded task states</text>'
        f'<text x="{w - pad}" y="{y1}" font-size="11" fill="{MUTED}" text-anchor="end">n = {TASKS["total"]:,} tasks</text>'
    )
    yb1 = y1 + 14
    body, geo = bar(pad, yb1, bar_w, bar_h, TASK_SEGS, TASKS["total"], False, unit="task", metrics=METRICS)
    s.append(body)
    # The single running task is too narrow to label in place.
    run = geo[-1]
    s.append(
        f'<path d="M{run[3] + run[4] / 2:.1f} {yb1 + bar_h} L{run[3] + run[4] / 2:.1f} {yb1 + bar_h + 16}" '
        f'stroke="{BLUE}" stroke-width="1"/>'
        f'<text x="{run[3] + run[4] / 2:.1f}" y="{yb1 + bar_h + 28}" font-size="10" fill="{BLUE}" '
        f'text-anchor="end">1 running (0.1%)</text>'
    )
    s.append(legend(pad, yb1 + bar_h + 20, TASK_SEGS[:3], TASKS["total"], 10))

    s.append("</svg>")
    return "".join(s)


def figure3_mobile() -> str:
    w, pad = 380, 22
    bar_w, bar_h = w - 2 * pad, 34
    head_h = 84
    h = 244
    s = [svg_open(
        w, h,
        "Recorded queue task states, without independent delivery verification",
        "Of 1,078 tasks, 809 succeeded, 210 failed, 58 were cancelled and one was running. "
        "Queue states do not establish deployment or use.",
        "f3m",
    )]
    s.append(
        f'<text x="{pad}" y="34" font-size="13.5" font-weight="600" fill="{TEXT}">What the queue recorded</text>'
        f'<text x="{pad}" y="52" font-size="10.5" fill="{MUTED}">Queue states do not establish deployment or use.</text>'
    )

    y1 = head_h
    s.append(
        f'<text x="{pad}" y="{y1}" font-size="11.5" font-weight="600" fill="{TEXT}">Recorded task states</text>'
        f'<text x="{w - pad}" y="{y1}" font-size="10.5" fill="{MUTED}" text-anchor="end">{TASKS["total"]:,} tasks</text>'
        f'<text x="{pad}" y="{y1 + 24}" font-size="9" fill="{BLUE}">1 running (0.1%) is too small to see.</text>'
    )
    yb1 = y1 + 34
    body, _ = bar(pad, yb1, bar_w, bar_h, TASK_SEGS, TASKS["total"], True, unit="task", metrics=METRICS)
    s.append(body)
    yy = yb1 + bar_h + 20
    for label, value, colour in TASK_SEGS:
        s.append(f'<rect x="{pad}" y="{yy - 8}" width="9" height="9" rx="2" fill="{colour}" fill-opacity="0.82"/>')
        s.append(
            f'<text x="{pad + 15}" y="{yy}" font-size="10.5" fill="{MUTED}">{esc(label)} '
            f'<tspan fill="{TEXT}" font-weight="600">{value}</tspan> ({pct(value, TASKS["total"])})</text>'
        )
        yy += 15

    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ main ----
def check_label_fit(root: ET.Element, name: str) -> None:
    """Allow two SVG units of clearance on either side, in local coordinates."""
    def visit(parent):
        containers = []
        for el in parent:
            tag = el.tag.split("}")[-1]
            x, y = float(el.get("x", 0)), float(el.get("y", 0))
            if tag == "rect":
                containers.append((x, y, float(el.get("width")), float(el.get("height"))))
            elif tag == "circle":
                r = float(el.get("r"))
                containers.append((float(el.get("cx")) - r, float(el.get("cy")) - r, 2*r, 2*r))
            elif tag == "text":
                boxes = [(w, left) for left, top, w, h in containers
                         if left <= x <= left+w and top < y <= top+h]
                if boxes:
                    w, left = min(boxes)
                    label = "".join(el.itertext())
                    em = sum(0.30 if c in " il.,:;!'|" else 0.85 if c in "MWmw@%"
                             else 0.64 if c.isupper() else EM_REG for c in label)
                    width = em * float(el.get("font-size")) + len(label)*float(el.get("letter-spacing", 0))
                    anchor = el.get("text-anchor")
                    start = x - width * {"middle": 0.5, "end": 1}.get(anchor, 0)
                    assert left+2 <= start and start+width <= left+w-2, f"{name}: label exceeds box: {label}"
            elif tag == "g":
                visit(el)
    visit(root)


def check(svg: str, name: str) -> None:
    root = ET.fromstring(svg)  # well-formed XML
    ns = "{http://www.w3.org/2000/svg}"
    assert root.get("role") == "img", name
    assert root.find(f"{ns}title") is not None and root.find(f"{ns}desc") is not None, name
    _, _, width, height = map(float, root.attrib["viewBox"].split())
    assert 0 < width < 8192 and 0 < height < 8192, name
    check_label_fit(root, name)
    for banned in ("chatgpt-inbox", "delegation-queue", "/home/", ".hermes"):
        assert banned not in svg, f"{name}: leaked private reference {banned}"
    assert 'href="http' not in svg, f"{name}: external reference"


def main() -> int:
    # --- consistency assertions on the published numbers --------------------
    states = TASKS["states"]
    assert sum(states.values()) == TASKS["total"] == 1078
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--probe-metrics", type=Path, help="Exercise the bar emitter with a scratch fixture")
    args.add_argument("--unit", choices=("task", "attempt"), default="task")
    args.add_argument("--check", action="store_true", help="Compare generated SVG bytes with tracked assets")
    options = args.parse_args()
    if options.probe_metrics:
        fixture = json.loads(options.probe_metrics.read_text())
        values = fixture[options.unit + "s"]
        segments = [(key, count, BLUE) for key, count in values["states"].items()]
        bar(0, 0, 300, 32, segments, values["total"], True, unit=options.unit, metrics=fixture)
        print(f"Rendered {options.unit} partition in memory")
        return 0

    if not options.check:
        OUT.mkdir(parents=True, exist_ok=True)
    figures = {
        "fig-2-control-loop.svg": architecture(False),
        "fig-2-control-loop-mobile.svg": architecture(True),
        "fig-3-outcomes.svg": figure3_wide(),
        "fig-3-outcomes-mobile.svg": figure3_mobile(),
    }
    for name, svg in figures.items():
        check(svg, name)
        path = OUT / name
        data = (svg + "\n").encode()
        if options.check:
            if path.read_bytes() != data:
                sys.exit(f"stale generated asset: {path}")
            print(f"matched {name}")
        else:
            path.write_bytes(data)
            print(f"wrote {name}")

    print(f"OK  tasks={TASKS['total']} (states sum to denominator)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
