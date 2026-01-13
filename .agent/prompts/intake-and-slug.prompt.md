# Prompt: Intake & Slug Derivation (Publishing)

## Objective
Given a raw inbox note, derive a semantic slug and perform safe setup checks.

## Inputs
- `inbox_path`: path under `inbox/`
- `source_note`: full markdown contents

## Output (STRICT)
Return a single JSON object (no surrounding prose):

```json
{
  "title": "<string>",
  "slug": "<string>",
  "notes_dir": "notes/<slug>",
  "collision": false
}
```

## Rules
- Derive title from the note (prefer first H1; fallback to first non-empty line).
- Slug rules:
  - lowercase
  - hyphenated
  - semantic (avoid stopwords where possible)
  - only `[a-z0-9-]`
  - no leading/trailing hyphen
  - max length 64
- Collision check:
  - if `notes/<slug>/` already exists, set `collision=true` and still return a best-effort slug.
- Do not write files.
