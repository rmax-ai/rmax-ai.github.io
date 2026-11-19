#!/usr/bin/env python3
"""Deterministic two-width render check for the year-one note.

Renders every figure at its authored width and both pages at a desktop and a
mobile viewport through headless Chromium, then records the real pixel size of
each output. Enforces the transport bound that killed the previous run: no
image passed to a vision model may exceed 8192 px on either axis.

Usage: python3 processed/<slug>/figures/check_renders.py
Exit 0 only when every check passes.
"""
from __future__ import annotations

import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

SLUG = "rmax-ai-year-one-from-agents-to-verified-work"
ROOT = Path(__file__).resolve().parents[3]
NOTE = ROOT / "notes" / SLUG
FIGS = NOTE / "figures"
MAX_PX = 8192

CHROME_CANDIDATES = [
    Path.home() / ".cache/ms-playwright/chromium-1228/chrome-linux/chrome",
    Path.home() / ".cache/ms-playwright/chromium-1200/chrome-linux/chrome",
]


def chrome() -> str:
    for c in CHROME_CANDIDATES:
        if c.is_file():
            return str(c)
    found = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if not found:
        sys.exit("no chromium binary found")
    return found


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        head = fh.read(24)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", f"not a png: {path}"
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def viewbox(svg: Path) -> tuple[int, int]:
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg.read_text())
    if not m:
        sys.exit(f"no viewBox in {svg}")
    return int(m.group(1)), int(m.group(2))


def shoot(binary: str, url: str, w: int, h: int, out: Path) -> tuple[int, int]:
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        binary,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--window-size={w},{h}",
        f"--screenshot={out}",
        url,
    ]
    subprocess.run(cmd, capture_output=True, timeout=120, check=True)
    return png_size(out)


def main() -> None:
    binary = chrome()
    tmp = Path(tempfile.mkdtemp(prefix="year-render-"))
    report: dict[str, object] = {"max_allowed_px": MAX_PX, "checks": [], "failures": []}

    def record(name: str, w: int, h: int, expected: tuple[int, int] | None = None) -> None:
        ok = max(w, h) <= MAX_PX and (expected is None or (w, h) == expected)
        entry = {"name": name, "px": f"{w}x{h}", "ok": ok}
        if expected:
            entry["expected"] = f"{expected[0]}x{expected[1]}"
        report["checks"].append(entry)
        if not ok:
            report["failures"].append(name)

    # --- figures, each at its authored width ---
    for svg in sorted(FIGS.glob("*.svg")):
        vb_w, vb_h = viewbox(svg)
        out = tmp / f"{svg.stem}.png"
        w, h = shoot(binary, f"file://{svg}", vb_w, vb_h + 24, out)
        record(f"figure:{svg.name}", w, h, (vb_w, vb_h + 24))

    # --- pages at two widths, capped height so no capture can exceed the bound ---
    for page, label in [(NOTE / "index.html", "note"), (NOTE / "evidence-notes/index.html", "appendix")]:
        for width, tag in [(1440, "desktop"), (390, "mobile")]:
            out = tmp / f"page-{label}-{tag}.png"
            w, h = shoot(binary, f"file://{page}", width, 2000, out)
            record(f"page:{label}:{tag}", w, h, (width, 2000))

    print(json.dumps(report, indent=2))
    out_json = Path(__file__).with_name("render-check.json")
    out_json.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nreport: {out_json}")
    print(f"screenshots: {tmp}")
    if report["failures"]:
        print(f"RESULT FAIL {len(report['failures'])}: {report['failures']}")
        sys.exit(1)
    print(f"RESULT PASS {len(report['checks'])}/{len(report['checks'])}")


if __name__ == "__main__":
    main()
