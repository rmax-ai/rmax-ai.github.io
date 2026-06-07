#!/usr/bin/env python3
"""Audit technical notes for required structural sections.

This audit is intentionally tolerant of a few existing house-style variants:
- heading-based sections (`## Practical Takeaways`)
- emphasized standalone labels (`**Practical Takeaways**`)
- combined scope/positioning sections that also embed status language
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PRACTICAL_RE = re.compile(
    r"(?im)^(?:#{1,6}\s*|\*\*\s*)practical\s+takeaways(?:\s*\([^)]*\))?(?::)?(?:\s*\*\*)?\s*$"
)
POSITIONING_RE = re.compile(
    r"(?im)^(?:#{1,6}\s*|\*\*\s*)(?:positioning(?:\s+note)?(?:\s*\([^)]*\))?|scope\s+and\s+positioning)(?::)?(?:\s*\*\*)?\s*$"
)
STATUS_HEADING_RE = re.compile(
    r"(?im)^(?:#{1,6}\s*|\*\*\s*)status(?:\s*&\s*|\s+and\s+)?(?:scope(?:\s+disclaimer)?|disclaimer)(?::)?(?:\s*\*\*)?\s*$"
)
STATUS_SIGNAL_RE = re.compile(
    r"(?is)\b(?:exploratory|personal\s+lab|lab\s+work|not\s+authoritative|unvalidated\s+opinion)\b"
)
SECTION_HEADING_RE = re.compile(r"(?m)^(#{1,6})\s+(.+?)\s*$")
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n+", re.S)


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def extract_heading_sections(text: str) -> dict[str, str]:
    matches = list(SECTION_HEADING_RE.finditer(text))
    sections: dict[str, str] = {}
    for i, match in enumerate(matches):
        title = match.group(2).strip().lower()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[title] = text[start:end]
    return sections


def has_status_disclaimer(text: str) -> bool:
    if STATUS_HEADING_RE.search(text):
        return True

    sections = extract_heading_sections(text)
    for title, body in sections.items():
        if title in {"scope and positioning", "positioning note"} and STATUS_SIGNAL_RE.search(body):
            return True

    # Some older notes use a standalone status paragraph instead of a heading.
    return bool(STATUS_SIGNAL_RE.search(text))


def audit_note(path: Path) -> list[str]:
    text = strip_frontmatter(path.read_text())
    missing: list[str] = []

    if not PRACTICAL_RE.search(text):
        missing.append("practical takeaways")
    if not POSITIONING_RE.search(text):
        missing.append("positioning note")
    if not has_status_disclaimer(text):
        missing.append("status disclaimer")

    return missing


def resolve_targets(paths: list[str]) -> list[Path]:
    if paths:
        return [Path(path) for path in paths]
    return sorted(Path("notes").glob("*/index.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Specific note markdown files to audit.")
    args = parser.parse_args()

    failures = []
    for path in resolve_targets(args.paths):
        missing = audit_note(path)
        if missing:
            failures.append((path, missing))

    if not failures:
        print("All audited notes include practical takeaways, positioning, and status language.")
        return 0

    for path, missing in failures:
        print(f"{path}: missing {', '.join(missing)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
