# Agent workflow

Allowed task classes: design, plan, implementation, review, verification, research.
Protected branches: main.
Branch names: spec/issue-N-slug for design/plan/docs-only work; agent/issue-N-slug for execution; claims/issue-N is the atomic claim ref and never a work branch.

Required publication checks:
- python3 scripts/audit_technical_note_structure.py notes/<slug>/index.md
- python3 scripts/generate-sitemap.py
- verify notes/<slug>/index.md frontmatter against notes/schema.yaml
- verify notes/<slug>/index.html contains the canonical URL and required footer assets
- verify the note is discoverable from notes/index.html, index.html, and index.md

Test-count mode: not applicable to prose-only publication tasks.

Allowed paths for publication tasks are issue-specific and may include inbox/**, processed/**, notes/<slug>/**, CHANGELOG.md, sitemap.xml, index.md, index.html, and notes/index.html.
Forbidden paths unless an issue explicitly changes the governing contract: .agent/mode/**, .agent/prompts/**, notes/schema.yaml, docs/contracts/**, .env*, **/secrets/**.

The binding authority for note publication is docs/contracts/publish-technical-note.md plus skills/publish-technical-note/SKILL.md and AGENTS.md. Do not weaken or bypass their phase order, subagent requirements, gates, or stop conditions.

Approval gates: the operator's ready transition is execution approval; merge is operator-only.
Public disclosure: repository is public; disclose AI assistance in PR evidence.
Proof of work: Objective / Changes / Verification / Evidence / Risks / Human Review Needed / Follow-up Issues.
Rollback: revert PR; never force-push or rewrite accepted history.
