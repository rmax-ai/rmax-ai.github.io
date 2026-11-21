#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""Render the three editorial figures for the RMax AI year-one article.

Editable source for every published figure. Deterministic: same input, same bytes.
Data-bearing values are read from metrics.json; each figure is emitted twice, a
wide layout and a narrow (mobile) layout, so no figure is scaled into illegibility.

Outputs (tracked, served with the note):
    notes/<slug>/figures/fig-1-timeline.svg         fig-1-timeline-mobile.svg
    notes/<slug>/figures/fig-2-control-loop.svg     fig-2-control-loop-mobile.svg
    notes/<slug>/figures/fig-3-outcomes.svg         fig-3-outcomes-mobile.svg

Usage:  python3 processed/<slug>/figures/render_figures.py
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SLUG = "rmax-ai-year-one-from-agents-to-verified-work"
ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "processed" / SLUG / "figures"
OUT = ROOT / "notes" / SLUG / "figures"
METRICS = json.loads((ROOT / "processed" / SLUG / "metrics.json").read_text())

# ---------------------------------------------------------------- palette ----
BG = "#0b1220"
PANEL = "#0f1724"
BORDER = "#1e293b"
TEXT = "#e6eef8"
MUTED = "#94a3b8"
DIM = "#64748b"
ACCENT = "#8b5cf6"
BLUE = "#60a5fa"
GREEN = "#34d399"
RED = "#f87171"
AMBER = "#fbbf24"
FONT = "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"

# Rough advance width per character, in em, for the regular and bold faces.
EM_REG = 0.515
EM_BOLD = 0.545


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def wrap(text: str, width: float, size: float, bold: bool = False) -> list[str]:
    """Greedy wrap using an approximate advance width. Good enough for layout."""
    em = EM_BOLD if bold else EM_REG
    limit = width / (size * em)
    words, lines, cur = text.split(), [], ""
    for w in words:
        candidate = f"{cur} {w}".strip()
        if len(candidate) <= limit or not cur:
            cur = candidate
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(
    x: float,
    y: float,
    lines: list[str],
    size: float,
    fill: str = TEXT,
    bold: bool = False,
    lh: float = 1.45,
    anchor: str = "start",
) -> tuple[str, float]:
    weight = ' font-weight="600"' if bold else ""
    out = []
    for i, line in enumerate(lines):
        out.append(
            f'<text x="{x:.1f}" y="{y + i * size * lh:.1f}" font-size="{size:.1f}" '
            f'fill="{fill}"{weight} text-anchor="{anchor}">{esc(line)}</text>'
        )
    return "".join(out), y + (len(lines) - 1) * size * lh


def pill(x: float, y: float, label: str, colour: str, size: float = 9.5) -> tuple[str, float]:
    w = len(label) * size * 0.60 + 14
    s = (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{size + 8:.1f}" rx="4" '
        f'fill="{colour}" fill-opacity="0.14" stroke="{colour}" stroke-opacity="0.55"/>'
        f'<text x="{x + w / 2:.1f}" y="{y + size + 1.4:.1f}" font-size="{size:.1f}" '
        f'fill="{colour}" text-anchor="middle" letter-spacing="0.4">{esc(label)}</text>'
    )
    return s, w


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


# --------------------------------------------------------------- figure 1 ----
# Seven phases of the operating model. `kind` drives the evidence marker.
PHASES = [
    (
        "Nov 2025",
        "Origin, no artifact",
        "The initiative's starting point exists only in the operator's account.",
        "account",
    ),
    (
        "Dec 2025 - Jan 2026",
        "Foundations",
        "Repository and site from Dec 23; first public note Jan 3; execution contracts and earned autonomy established; earliest agent-workspace records Jan 31.",
        "mixed",
    ),
    (
        "Feb - Mar 2026",
        "Portfolio expansion",
        "Autonomous editing, a book project, workflow experiments and an application prototype. Commit volume rises; it does not prove finished products.",
        "repo",
    ),
    (
        "Apr 2026",
        "Dormancy",
        "Zero indexed commits or issues; 30 heartbeat-only sessions. The records show a pause, not its cause.",
        "dormant",
    ),
    (
        "May - Jul 2026",
        "Platform rebuild",
        "Runtime migration on May 11; scheduled work and knowledge pipelines expand; governed research and bounded loops become a cluster.",
        "repo",
    ),
    (
        "Aug - Oct 2026",
        "Control plane",
        "Media, telemetry and a tool gateway, then delegation, a second-model request channel, system review and architecture records.",
        "repo",
    ),
    (
        "Nov 1 - 18 2026",
        "Verification debt",
        "Maintenance, evaluation and self-audit surface acceptance failures and maintenance cost. The window closes Nov 18.",
        "repo",
    ),
]

KIND = {
    "repo": (ACCENT, "Repository evidence"),
    "mixed": (BLUE, "Repository + operator account"),
    "account": (AMBER, "Operator account only"),
    "dormant": (RED, "Observed gap in records"),
}


def figure1_wide() -> str:
    w, x_rail, x_period, x_body, body_w = 760, 30, 58, 214, 512
    head_h, row_pad = 78, 20
    rows = []
    for period, name, desc, kind in PHASES:
        lines = wrap(desc, body_w, 11.4)
        rows.append((period, name, lines, kind))
    h = head_h + sum(max(len(r[2]) * 11.4 * 1.5 + 22, 46) + row_pad for r in rows) + 62

    s = [svg_open(
        w, h,
        "Seven phases of the RMax AI operating model, November 2025 to November 18, 2026",
        "A vertical timeline. November 2025 is marked as operator account only, with no surviving "
        "artifact. April 2026 is marked as a dormancy observed in the records: zero indexed commits "
        "and 30 heartbeat-only sessions. The remaining phases are supported by repository evidence.",
        "f1w",
    )]
    s.append(
        f'<text x="30" y="40" font-size="15" font-weight="600" fill="{TEXT}">'
        f'Seven phases of the operating model</text>'
        f'<text x="30" y="60" font-size="11" fill="{MUTED}">'
        f'November 2025 to November 18, 2026</text>'
    )
    y = head_h
    s.append(f'<line x1="{x_rail}" y1="{y - 8}" x2="{x_rail}" y2="{h - 74}" stroke="{BORDER}"/>')
    for period, name, lines, kind in rows:
        colour = KIND[kind][0]
        block_h = max(len(lines) * 11.4 * 1.5 + 22, 46)
        s.append(f'<circle cx="{x_rail}" cy="{y + 20}" r="5" fill="{colour}"/>')
        s.append(f'<rect x="{x_rail + 14}" y="{y + 8}" width="2.5" height="{block_h - 8}" fill="{colour}" opacity="0.5"/>')
        s.append(
            f'<text x="{x_period}" y="{y + 16}" font-size="12" font-weight="600" fill="{TEXT}">{esc(name)}</text>'
            f'<text x="{x_period}" y="{y + 33}" font-size="9.5" fill="{MUTED}" letter-spacing="0.3">{esc(period.upper())}</text>'
        )
        body, _ = text_lines(x_body, y + 15, lines, 11.4, MUTED)
        s.append(body)
        y += block_h + row_pad

    ly = h - 52
    x = x_rail
    for key in ("repo", "mixed", "account", "dormant"):
        colour, label = KIND[key]
        s.append(f'<circle cx="{x + 4}" cy="{ly}" r="4" fill="{colour}"/>')
        s.append(f'<text x="{x + 15}" y="{ly + 3.6}" font-size="10" fill="{MUTED}">{esc(label)}</text>')
        x += 15 + len(label) * 10 * EM_REG + 22
    s.append(
        f'<text x="{x_rail}" y="{ly + 22}" font-size="10" fill="{DIM}">'
        f'Phases are categorical; widths carry no proportional meaning.</text>'
    )
    s.append("</svg>")
    return "".join(s)


def figure1_mobile() -> str:
    w, pad, x_body, body_w = 380, 24, 44, 312
    rows = []
    for period, name, desc, kind in PHASES:
        rows.append((period, name, wrap(desc, body_w, 12), kind))
    h = 76 + sum(len(r[2]) * 12 * 1.5 + 40 for r in rows) + 96

    s = [svg_open(
        w, h,
        "Seven phases of the RMax AI operating model, November 2025 to November 18, 2026",
        "A stacked timeline. November 2025 is marked as operator account only, with no surviving "
        "artifact. April 2026 is marked as a dormancy observed in the records: zero indexed commits "
        "and 30 heartbeat-only sessions.",
        "f1m",
    )]
    s.append(
        f'<text x="{pad}" y="38" font-size="14" font-weight="600" fill="{TEXT}">Seven phases</text>'
        f'<text x="{pad}" y="56" font-size="11" fill="{MUTED}">Nov 2025 - Nov 18, 2026</text>'
    )
    y = 80
    s.append(f'<line x1="{pad + 5}" y1="{y - 6}" x2="{pad + 5}" y2="{h - 84}" stroke="{BORDER}"/>')
    for period, name, lines, kind in rows:
        colour = KIND[kind][0]
        s.append(f'<circle cx="{pad + 5}" cy="{y + 12}" r="4.5" fill="{colour}"/>')
        s.append(f'<text x="{x_body}" y="{y + 8}" font-size="9" fill="{colour}" letter-spacing="0.5">{esc(period.upper())}</text>')
        s.append(f'<text x="{x_body}" y="{y + 25}" font-size="12.5" font-weight="600" fill="{TEXT}">{esc(name)}</text>')
        body, _ = text_lines(x_body, y + 42, lines, 12, MUTED)
        s.append(body)
        y += len(lines) * 12 * 1.5 + 40

    ly = h - 62
    for i, key in enumerate(("repo", "mixed", "account", "dormant")):
        colour, label = KIND[key]
        yy = ly + i * 15
        s.append(f'<circle cx="{pad + 4}" cy="{yy}" r="3.5" fill="{colour}"/>')
        s.append(f'<text x="{pad + 14}" y="{yy + 3.4}" font-size="9.5" fill="{MUTED}">{esc(label)}</text>')
    s.append("</svg>")
    return "".join(s)


# --------------------------------------------------------------- figure 2 ----
# Stage ladder. `gutter` tells the wide layout where a return edge terminates.
STAGES = [
    ("Operator", "Scope, authority, and final approval of consequential actions.", "human decision", "operator"),
    ("GitHub task state", "Issue carries the task, owner, claims, implementation artifacts, and review history.", "durable state", "state"),
    ("Orchestrator", "Selects eligible work, dispatches one bounded attempt, records findings and next owner.", "automation", "auto"),
    ("Execution lane", "Coding agent works inside a bounded attempt and returns a branch, change, and evidence.", "automation", "auto"),
    ("Acceptance gate", "A command with an expected result runs against the change; the evidence attaches to the pull request.", "automation", "gate"),
    ("Independent review", "A second model and, where risk warrants, the operator return a verdict bound to an exact revision.", "review", "review"),
    ("Disposition", "The outcome is recorded with a next owner: verified, delegated, deferred, or closed with a reason.", "durable state", "state"),
]

STAGE_TONE = {
    "operator": AMBER,
    "state": ACCENT,
    "auto": BLUE,
    "gate": GREEN,
    "review": BLUE,
}


def figure2_wide() -> str:
    w, pad, band_h, head_h = 760, 30, 64, 96
    band_w = 636
    gutter_red, gutter_amber = 690, 724
    x_badge = pad + 18
    x_title = pad + 44
    x_owner = pad + band_w - 10
    body_w = x_owner - x_title - 116
    h = head_h + len(STAGES) * band_h + 96

    s = [svg_open(
        w, h,
        "Control loop: human authority, durable GitHub state, bounded agent execution, acceptance gate, independent review, and disposition",
        "Seven documented responsibilities. The dashed red return runs from the acceptance gate to "
        "execution for a retry. The dotted amber return from disposition to GitHub task state "
        "represents a proposed follow-up.",
        "f2w",
    )]
    s.append(
        f'<text x="{pad}" y="40" font-size="15" font-weight="600" fill="{TEXT}">Where authority, execution and evidence live</text>'
        f'<text x="{pad}" y="60" font-size="11" fill="{MUTED}">One pass through the loop. Both return edges are drawn in the right gutter.</text>'
    )
    s.append(f'<line x1="{pad + 6}" y1="{head_h - 4}" x2="{pad + 6}" y2="{h - 92}" stroke="{BORDER}"/>')

    y = head_h
    for i, (name, desc, owner, tone) in enumerate(STAGES, start=1):
        colour = STAGE_TONE[tone]
        s.append(
            f'<rect x="{pad}" y="{y}" width="{band_w}" height="{band_h - 10}" rx="7" '
            f'fill="{PANEL}" stroke="{BORDER}"/>'
            f'<rect x="{pad}" y="{y}" width="3" height="{band_h - 10}" rx="1.5" fill="{colour}"/>'
            f'<circle cx="{x_badge}" cy="{y + 26}" r="11" fill="{colour}" fill-opacity="0.16" stroke="{colour}" stroke-opacity="0.6"/>'
            f'<text x="{x_badge}" y="{y + 30}" font-size="11" font-weight="600" fill="{colour}" text-anchor="middle">{i}</text>'
            f'<text x="{x_title}" y="{y + 20}" font-size="12.5" font-weight="600" fill="{TEXT}">{esc(name)}</text>'
        )
        lines = wrap(desc, body_w, 10.6)
        assert len(lines) <= 2, f"stage {i} needs {len(lines)} lines: {desc}"
        body, _ = text_lines(x_title, y + 36, lines, 10.6, MUTED, lh=1.35)
        s.append(body)
        s.append(
            f'<text x="{x_owner}" y="{y + 20}" font-size="9.5" fill="{colour}" text-anchor="end" '
            f'letter-spacing="0.3">{esc(owner.upper())}</text>'
        )
        if i < len(STAGES):
            s.append(
                f'<path d="M{pad + 6} {y + band_h - 10} L{pad + 6} {y + band_h - 2}" stroke="{BORDER}" stroke-width="1.5"/>'
                f'<path d="M{pad + 2.5} {y + band_h - 6} L{pad + 6} {y + band_h - 1.5} L{pad + 9.5} {y + band_h - 6}" '
                f'fill="none" stroke="{BORDER}" stroke-width="1.5"/>'
            )
        y += band_h

    y_exec = head_h + 3 * band_h       # execution lane
    y_gate = head_h + 4 * band_h       # acceptance gate
    y_state = head_h + 1 * band_h      # github task state
    y_disp = head_h + 6 * band_h       # disposition
    mid = (band_h - 10) / 2
    edge = pad + band_w

    # Retry route from gate to execution.
    s.append(
        f'<path d="M{edge} {y_gate + mid} H{gutter_red} V{y_exec + mid} H{edge + 4}" '
        f'fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5 4"/>'
        f'<path d="M{edge + 9} {y_exec + mid - 3.5} L{edge + 4} {y_exec + mid} L{edge + 9} {y_exec + mid + 3.5}" '
        f'fill="none" stroke="{RED}" stroke-width="1.6"/>'
    )
    # Proposed return from disposition to task state.
    s.append(
        f'<path d="M{edge} {y_disp + mid} H{gutter_amber} V{y_state + mid} H{edge + 4}" '
        f'fill="none" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="2 5"/>'
        f'<path d="M{edge + 9} {y_state + mid - 3.5} L{edge + 4} {y_state + mid} L{edge + 9} {y_state + mid + 3.5}" '
        f'fill="none" stroke="{AMBER}" stroke-width="1.6"/>'
    )
    # Rotated labels sit in the gutter on an opaque chip so the dashed line never shows through.
    def rotated_label(x: float, y: float, text: str, colour: str) -> str:
        chip = len(text) * 9 * 0.54 + 14
        return (
            f'<g transform="rotate(-90 {x} {y})">'
            f'<rect x="{x - chip / 2:.1f}" y="{y - 7:.1f}" width="{chip:.1f}" height="12" rx="3" fill="{BG}"/>'
            f'<text x="{x}" y="{y + 2.5:.1f}" font-size="9" fill="{colour}" text-anchor="middle">{text}</text>'
            f'</g>'
        )

    s.append(rotated_label(gutter_red - 8, y_exec + mid + 30, "failed check &#8594; retry", RED))
    s.append(rotated_label(gutter_amber - 8, y_state + mid + 58, "adoption gap", AMBER))

    ly = h - 70
    s.append(f'<circle cx="{pad + 6}" cy="{ly}" r="4.5" fill="{AMBER}"/>')
    s.append(
        f'<text x="{pad + 18}" y="{ly + 4}" font-size="10.5" fill="{TEXT}">'
        f'Amber marks a proposed follow-up in the next task.</text>'
    )
    s.append(
        f'<text x="{pad + 6}" y="{ly + 22}" font-size="10" fill="{MUTED}">'
        f'The audit recorded verdicts. It did not track their adoption in later tasks.</text>'
    )
    s.append(
        f'<text x="{pad + 6}" y="{ly + 38}" font-size="10" fill="{DIM}">'
        f'The stages describe responsibilities. The audit did not trace every historical task through them.</text>'
    )
    s.append("</svg>")
    return "".join(s)


def figure2_mobile() -> str:
    w, pad, band_h, head_h = 380, 22, 88, 88
    body_w = w - 2 * pad - 20
    note_max = 4
    box_h = 34 + note_max * 13
    h = head_h + len(STAGES) * band_h + box_h + 34

    s = [svg_open(
        w, h,
        "Control loop: human authority, durable GitHub state, bounded agent execution, acceptance gate, independent review, and disposition",
        "Seven responsibilities stacked vertically. Red text describes a possible return to execution. "
        "An amber box describes a proposed follow-up in GitHub task state.",
        "f2m",
    )]
    s.append(
        f'<text x="{pad}" y="38" font-size="14" font-weight="600" fill="{TEXT}">Where authority, execution and evidence live</text>'
        f'<text x="{pad}" y="58" font-size="11" fill="{MUTED}">One pass through the loop.</text>'
    )
    y = head_h
    for i, (name, desc, owner, tone) in enumerate(STAGES, start=1):
        colour = STAGE_TONE[tone]
        s.append(
            f'<rect x="{pad}" y="{y}" width="{w - 2 * pad}" height="{band_h - 12}" rx="7" fill="{PANEL}" stroke="{BORDER}"/>'
            f'<rect x="{pad}" y="{y}" width="3" height="{band_h - 12}" rx="1.5" fill="{colour}"/>'
        )
        s.append(
            f'<text x="{pad + 14}" y="{y + 18}" font-size="10" font-weight="600" fill="{colour}">{i}</text>'
            f'<text x="{pad + 26}" y="{y + 18}" font-size="12" font-weight="600" fill="{TEXT}">{esc(name)}</text>'
        )
        lines = wrap(desc, body_w, 10.4)[:3]
        body, _ = text_lines(pad + 14, y + 34, lines, 10.4, MUTED, lh=1.35)
        s.append(body)
        s.append(f'<text x="{w - pad - 10}" y="{y + 18}" font-size="8.5" fill="{colour}" text-anchor="end">{esc(owner.upper())}</text>')
        if i == 5:
            s.append(
                f'<text x="{pad + 14}" y="{y + band_h - 18}" font-size="9" fill="{RED}">'
                f'A failed check can return work to stage 4.</text>'
            )
        y += band_h

    note = wrap(
        "A review finding can inform the next task. "
        "The operator or orchestrator would link the disposition at stage 7 to the task record at stage 2.",
        body_w, 10,
    )
    assert len(note) <= note_max, f"mobile note needs {len(note)} lines"
    by = h - box_h - 16
    s.append(
        f'<rect x="{pad}" y="{by}" width="{w - 2 * pad}" height="{box_h}" rx="7" fill="{AMBER}" '
        f'fill-opacity="0.08" stroke="{AMBER}" stroke-opacity="0.45"/>'
        f'<text x="{pad + 12}" y="{by + 18}" font-size="10.5" font-weight="600" fill="{AMBER}">Proposed follow-up</text>'
    )
    body, _ = text_lines(pad + 12, by + 33, note, 10, MUTED, lh=1.3)
    s.append(body)
    s.append("</svg>")
    return "".join(s)


# --------------------------------------------------------------- figure 3 ----
TASKS = METRICS["tasks"]
ATT = METRICS["attempts"]

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
    options = args.parse_args()
    if options.probe_metrics:
        fixture = json.loads(options.probe_metrics.read_text())
        values = fixture[options.unit + "s"]
        segments = [(key, count, BLUE) for key, count in values["states"].items()]
        bar(0, 0, 300, 32, segments, values["total"], True, unit=options.unit, metrics=fixture)
        print(f"Rendered {options.unit} partition in memory")
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    figures = {
        "fig-1-timeline.svg": figure1_wide(),
        "fig-1-timeline-mobile.svg": figure1_mobile(),
        "fig-2-control-loop.svg": figure2_wide(),
        "fig-2-control-loop-mobile.svg": figure2_mobile(),
        "fig-3-outcomes.svg": figure3_wide(),
        "fig-3-outcomes-mobile.svg": figure3_mobile(),
    }
    for name, svg in figures.items():
        check(svg, name)
        path = OUT / name
        path.write_text(svg + "\n")
        print(f"wrote {path.relative_to(ROOT)}  {len(svg):,} bytes")

    print(f"OK  tasks={TASKS['total']} (states sum to denominator)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
