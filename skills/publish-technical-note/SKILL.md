---
name: publish-technical-note
description: Publish a technical note on the rmax.ai site from raw article input through reviewed markdown, HTML, navigation updates, changelog, and sitemap. Use when the user wants to publish an article, note, essay, or inbox draft into `notes/<slug>/` using the repository's binding publishing contract and prompt files.
---

# Publish Technical Note

## Overview

Publish a note by following the repository's contract-driven workflow, not by improvising page edits. Treat the contract as the authority for scope, order, invariants, gates, and stopping conditions.

## Required Inputs

- A source article in `inbox/*.md`
- Or explicit user authorization to materialize pasted content into `inbox/*.md`

If the source exists only in chat and there is no override, stop and ask the user to place it in `inbox/` or authorize you to create the file.

## Authority Files

Read these first:

- `docs/contracts/publish-technical-note.md`
- `.agent/mode/publishing-orchestrator.agent.md`
- `notes/schema.yaml`

Then use the fixed prompts referenced by the contract:

- `.agent/prompts/intake-and-slug.prompt.md`
- `.agent/prompts/write-technical-note.prompt.md`
- `.agent/prompts/review-technical-note.prompt.md`
- `.agent/prompts/failure-mode-review.prompt.md`
- `.agent/prompts/apply-frontmatter.prompt.md`
- `.agent/prompts/publish-note.prompt.md`
- `.agent/prompts/link-audit.prompt.md`
- `.agent/prompts/update-changelog.prompt.md`

## Expanded Write Scope

The contract treats these files as expanded write scope:

- `index.html`
- `index.md`
- `notes/index.html`
- `sitemap.xml`

Before editing any of them, ensure the user has explicitly authorized that scope for the run. If not, stop and ask.

## Workflow

Execute phases in strict order.

### 1. Intake and slug

- Read the source note.
- Derive the title and semantic slug using the intake prompt rules.
- Check whether `notes/<slug>/` already exists.
- If it exists, stop and ask for a different slug.
- Create `notes/<slug>/`.

### 2. Draft the note

- Use the writer prompt to convert the source into a publication-ready technical note.
- Write only the returned markdown to `notes/<slug>/index.md`.
- Ensure the draft is non-empty.

### 3. Review the draft

- Run an editorial pass against the draft.
- Preserve factual claims and any explicit source links that materially support the note.
- Overwrite `notes/<slug>/index.md` with only the revised markdown.

### 4. Run the failure-mode gate

- Run the failure-mode review on the reviewed note.
- If the verdict is blocking, stop.
- If the verdict is cautionary, continue and preserve the warnings for the changelog.

### 5. Apply frontmatter

- Generate frontmatter from `notes/schema.yaml`.
- Enforce exact slug consistency between:
  - directory name
  - frontmatter slug
  - canonical URL path
- Do not add extra fields.

### 6. Publish HTML

- Render `notes/<slug>/index.html` using the site's existing note structure.
- Preserve any `Sources` or `References` section from markdown as clickable links in HTML.
- Ensure the HTML includes:
  - canonical link
  - `/styles/footer.css`
  - standardized footer markup
  - `window.footerThoughts` with exactly 3 items
  - `/scripts/footer.js` immediately after the thoughts block

### 7. Audit links and discoverability

- Audit internal links, canonical path, metadata consistency, and discoverability.
- Check the note is reachable from:
  - `notes/index.html`
  - `index.html`
  - `index.md`
- If the note is orphaned and you have expanded write authorization, add it to the necessary discovery surfaces and rerun the audit.
- If the audit remains blocking, stop.

### 8. Update changelog

- Append one entry to `CHANGELOG.md` using the changelog prompt format.
- Include any warnings from the failure-mode review and link audit.

### 9. Regenerate sitemap

- Only after the note and discovery surfaces are in place, regenerate `sitemap.xml` with `scripts/generate-sitemap.py`.
- Validate:
  - the new note URL exists
  - URLs are unique
  - URLs are lexicographically sorted
  - root element is `urlset`

## Validation

Before declaring success, verify:

- `notes/<slug>/index.md` exists and includes schema-compliant frontmatter
- `notes/<slug>/index.html` exists and includes the required footer assets
- the note is listed in `notes/index.html`
- the note is listed in the main note discovery area of `index.html`
- the note is present in `index.md`
- `CHANGELOG.md` contains the new entry
- `sitemap.xml` contains the canonical note URL

## Stop Conditions

Stop immediately if:

- the source note is missing and not authorized to be materialized
- the slug collides
- a review gate returns a blocking verdict
- expanded write scope is required but not authorized
- schema validation fails

## Output

Return:

- the slug
- files created or updated
- any cautionary warnings
- whether publication completed or stopped at a gate
