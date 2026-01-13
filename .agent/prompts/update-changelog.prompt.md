# Prompt: Update CHANGELOG.md for Published Note

## Objective
Append a single changelog entry for a newly published technical note.

## Inputs
- `changelog_path`: `CHANGELOG.md`
- `slug`: `<slug>`
- `note_path`: `notes/<slug>/index.md`
- `warnings`: warnings collected from failure-mode review and link audit

## Output (STRICT)
Return a single JSON object (no surrounding prose):

```json
{
  "appended": true,
  "entry": "<the exact text appended>"
}
```

## Rules
- Append (do not rewrite) `CHANGELOG.md`.
- Entry must include:
  - ISO date (YYYY-MM-DD)
  - Action: `Published technical note`
  - Slug and path
  - One factual sentence describing what was published
  - Warnings (if any), factually stated
- Keep formatting consistent with the existing changelog style.
