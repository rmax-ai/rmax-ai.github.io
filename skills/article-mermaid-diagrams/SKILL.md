---
name: article-mermaid-diagrams
description: Add or update Mermaid diagrams in a published article or note that has both Markdown and static HTML artifacts. Use when the user wants diagrams added, improved, or synchronized across `index.md` and `index.html` in this repo's note structure.
---

# Article Mermaid Diagrams

## Overview

Use this skill when a note needs Mermaid diagrams added or updated in both the Markdown source and the published static HTML page.

Keep the change tightly scoped to the target article. Do not broaden the edit into a general rewrite.

## Relevant repo patterns

Inspect the target note first, then inspect at least one existing Mermaid-enabled note before editing. Prefer these local examples:

- `notes/enterprise-ai-agents-knowledge-layer-beyond-rag/index.md`
- `notes/enterprise-ai-agents-knowledge-layer-beyond-rag/index.html`
- `notes/stateful-enterprise-cognition/index.md`

Use those examples to match:

- Mermaid block placement in Markdown
- Mermaid container styling in HTML
- Mermaid runtime import and initialization in HTML
- Existing note layout, metadata, footer, and navigation structure

## Workflow

### 1. Inspect before editing

- Read the target `index.md` and `index.html`.
- Identify which claims or sections would genuinely benefit from diagrams.
- Prefer 1 to 3 diagrams. More than that usually harms clarity.

### 2. Choose diagram scope

Each diagram should clarify a distinct idea, such as:

- system architecture
- execution flow
- dependency or control flow
- failure modes and tradeoffs
- state transitions

Avoid diagrams that merely restate the section heading.

### 3. Write reliable Mermaid

Prefer simple, robust Mermaid syntax:

- use `flowchart TD` or `flowchart LR` by default
- keep labels short
- avoid decorative complexity
- avoid fragile syntax or overloaded diagrams
- use one clear idea per diagram

When labels contain punctuation or longer phrases, prefer quoted node labels.

### 4. Update Markdown

- Add fenced ````mermaid` blocks in the relevant sections of `index.md`.
- Add only minimal surrounding prose if the diagram needs a one-sentence setup.
- Do not rewrite unrelated sections.

### 5. Update static HTML

- Add matching Mermaid containers to `index.html`.
- Follow the repo's existing Mermaid-enabled HTML pattern instead of inventing a new one.
- Add only the minimum local CSS needed for Mermaid blocks if the page does not already have it.
- If Mermaid runtime support is missing on that page, add the same style of import/init already used elsewhere in the repo.

### 6. Preserve page invariants

Do not break or remove:

- frontmatter-derived metadata
- canonical link
- navigation
- analytics scripts
- standardized footer markup
- `window.footerThoughts`
- `/scripts/footer.js`

## Quality bar

Good diagrams:

- clarify the article's reasoning
- compress multi-paragraph explanations into a readable structure
- make architectural relationships legible
- stay readable on desktop and mobile

Weak diagrams:

- are decorative
- repeat prose without abstraction
- cram too many concepts into one graphic
- introduce new claims not supported by the article

## Verification

Before finishing, verify:

- `index.md` contains the Mermaid blocks
- `index.html` contains corresponding Mermaid containers
- Mermaid runtime/init exists in `index.html` if required
- the standardized footer markup still exists
- `/scripts/footer.js` still exists on the page

If possible, also verify rendering through the local browser workflow. If full render verification is not possible, state exactly what was checked.

## Output

Return:

- which sections received diagrams
- how many diagrams were added or updated
- whether Markdown and HTML were kept in sync
- what verification was completed
