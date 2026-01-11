# Analytics Events Spec (v1)

> Owner: Max Espinoza (rmax.ai)    Last updated: 2026-01-10  
> Version: 2026.01.01

## Goals
1. Measure which surfaces drive contact intent so signal from readers → collaborators/partners.
2. Capture outbound interest (GitHub, X, LinkedIn) and downloads without exploding the taxonomy.
3. Guard taxonomy drift with a single source of truth and a lightweight deprecation workflow.

## Event reference

### `click_contact_email`
- **Trigger:** User activates any `mailto:` link for `hello@rmax.ai` (header, contact section, or elsewhere). Automated click handler watches `mailto:` URIs and flags them once per interaction.
- **Metadata**
  - `email` (string, optional) – populated with the address in the clicked URI (currently `hello@rmax.ai`).
- **Notes:** This event is the primary proxy for contact intent; it fires via both annotated links and automated mailto tracking.

### `click_nav`
- **Trigger:** Header nav clicks that intentionally guide readers through `Notes`, `Research`, `About`, or `Contact`.
- **Metadata**
  - `item` (enum): `notes`, `research`, `about`, `contact`.
- **Notes:** Data attributes (`data-simple-nav-item`) ensure nav clicks surface in the taxonomy without naming explosions.

### `click_cta`
- **Trigger:** High-signal CTAs beyond the baseline nav set (currently the “View all” links for Research and Notes).
- **Metadata**
  - `cta_id` (enum): `research_view_all`, `notes_view_all`.
- **Notes:** Only add a new `cta_id` when the CTA has measurable downstream outcomes; document the new value in this spec before deployment.

### `click_outbound`
- **Trigger:** Clicks that resolve to a hostname external to `rmax.ai` (LinkedIn, X, GitHub, etc). Annotated social links provide host candidates while the automated handler covers arbitrary outbound targets.
- **Metadata**
  - `host` (string, lowercased, without leading `www.`). Current high-signal values: `linkedin.com`, `x.com`, `github.com`, `substack.com`. Additional hosts may be observed via automated tracking; update this spec if those hosts become recurring signals or need grouping.

### `download_asset`
- **Trigger:** Clicks on links whose resolved path ends in a stable download extension (`.pdf`, `.zip`, `.png`, `.svg`, etc.).
- **Metadata**
  - `file` (string) – the pathname plus search string of the target asset.
  - `type` (enum): `pdf`, `zip`, `gz`, `tar`, `csv`, `tsv`, `xlsx`, `xls`, `pptx`, `ppt`, `docx`, `doc`, `png`, `jpg`, `jpeg`, `svg`.
- **Notes:** The automated handler enforces this rule so downloads stay trackable even without manual instrumentation.

## Versioning & deprecation
1. **Schema changes:** Any new event name or metadata key requires this document to be updated before merging. Revision history lives here and should be referenced in pull requests that touch analytics.
2. **Deprecation policy:** Keep the prior event name in the DOM and event queue for at least two weeks after announcing the change; add a migration note to this spec (e.g., “`click_contact_email_v2` introduced on YYYY-MM-DD, old event retired on YYYY-MM-DD”).
3. **Validation guardrails:** Use the simple analytics helper script (`click` listener + `data-simple-event` attributes) so event names are consistent. Before deploying, confirm the new event surfaces in the Simple Analytics Events Explorer with the expected metadata keys.

## Operational notes
- **Event ownership:** rmax.ai keeps a single steward (Max) for analytics instrumentation and review; escalate via the repository issue tracker if you stumble on regressions.
- **Drift protection:** `analytics-events.md` is the canonical taxonomy file; insist on updates during code review before introducing new `data-simple-event` values or automated handlers.
