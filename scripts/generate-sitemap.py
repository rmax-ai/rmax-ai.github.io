#!/usr/bin/env python3
"""
generate-sitemap.py

Generate sitemap.xml for rmax.ai using the local filesystem only.

Rules:
- Only index.html files define routable pages
- URLs are derived from directory structure
- No crawling, no network access
- Deterministic output (stable diffs)

Usage:
  python generate-sitemap.py

Output:
  sitemap.xml (written to repo root)
"""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

# -----------------------------
# Configuration
# -----------------------------

DOMAIN = "https://rmax.ai"

EXCLUDED_DIRS = {
    ".agent",
    ".vscode",
    "docs",
}

EXCLUDED_FILES = {
    "README.md",
    "CHANGELOG.md",
    "CNAME",
}

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "sitemap.xml"


# -----------------------------
# Helpers
# -----------------------------

def is_excluded(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDED_DIRS:
            return True
    return False


def index_html_files(root: Path) -> list[Path]:
    files: list[Path] = []

    for path in root.rglob("index.html"):
        if is_excluded(path):
            continue
        if any(parent.name in EXCLUDED_DIRS for parent in path.parents):
            continue
        files.append(path)

    return sorted(files)


def url_for_index(path: Path) -> str:
    if path.parent == ROOT:
        return f"{DOMAIN}/"

    rel = path.parent.relative_to(ROOT).as_posix()
    return f"{DOMAIN}/{rel}/"


def lastmod(path: Path) -> str:
    ts = path.stat().st_mtime
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    index_files = index_html_files(ROOT)

    if not index_files:
        sys.exit("ERROR: No index.html files found. Aborting sitemap generation.")

    # Collect entries to ensure we can sort by URL
    entries = []
    for index in index_files:
        entries.append({
            "loc": url_for_index(index),
            "lastmod": lastmod(index)
        })

    # Sort entries lexicographically by URL
    entries.sort(key=lambda x: x["loc"])

    urlset = ET.Element(
        "urlset",
        attrib={
            "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"
        },
    )

    for entry in entries:
        url = ET.SubElement(urlset, "url")

        loc = ET.SubElement(url, "loc")
        loc.text = entry["loc"]

        lm = ET.SubElement(url, "lastmod")
        lm.text = entry["lastmod"]

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)

    print(f"✔ sitemap.xml generated with {len(entries)} URLs")


if __name__ == "__main__":
    main()

