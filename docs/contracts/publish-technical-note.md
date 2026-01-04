## Execution Contract: Technical Note Publishing

**Contract ID:** `exec-contract.publish-technical-note.v1`
**Scope:** rmax lab website
**Applies to:** agent orchestrators only

---

### 1. Purpose

This contract governs the transformation of a raw technical note from `inbox/` into a published, reviewed, schema-compliant note under `notes/<slug>/`, including HTML publication, link auditing, and changelog update.

The goal is **safe, repeatable publication**, not speed or creativity.

---

### 2. Roles & Responsibilities

**Orchestrator agent**

* Coordinates execution
* Enforces order, gates, and invariants
* Never authors prose

**Subagents (delegated only via `runSubagent`)**

* Writer
* Editorial reviewer
* Failure-mode reviewer
* Publisher (HTML)
* Link & navigation auditor

---

### 3. Authority Model

**Read access**

* `inbox/**`
* `notes/schema.yaml`
* `notes/**`
* `index.html`, `index.md`
* `research/index.html`
* `README.md`

**Write access**

* `notes/<slug>/**`
* `CHANGELOG.md`

**Forbidden**

* Modifying prompts
* Modifying schema
* Writing outside declared paths

Violation ⇒ immediate halt.

---

### 4. Inputs

* One Markdown file in `inbox/`
* Fixed prompts:

  * `write-technical-note.prompt.md`
  * `review-technical-note.prompt.md`
  * `failure-mode-review.prompt.md`
  * `publish-note.prompt.md`
  * `link-audit.prompt.md`
* Schema:

  * `notes/schema.yaml`

---

### 5. Outputs (Required Artifacts)

* `notes/<slug>/index.md`

  * reviewed content
  * valid YAML frontmatter
* `notes/<slug>/index.html`
* `CHANGELOG.md` entry

No partial outputs are considered valid.

---

### 6. Execution Phases (Strict Order)

#### Phase 0 — Intake

* Read inbox note
* Derive slug
* Create `notes/<slug>/`

**Invariant:** slug ↔ directory name ↔ frontmatter slug must match.

---

#### Phase 1 — Draft Generation

* Subagent: writer
* Output: Markdown draft (no frontmatter)

**Gate:** file exists and is non-empty.

---

#### Phase 2 — Editorial Review

* Subagent: editorial reviewer
* Output: revised Markdown

**Gate:** structure present, thesis identifiable.

---

#### Phase 3 — Failure-Mode Review

* Subagent: failure-mode reviewer

**Gate logic**

* `Block publish` ⇒ STOP
* `Publish with caution` ⇒ CONTINUE + log warning
* `Safe to publish` ⇒ CONTINUE

No content edits allowed here.

---

#### Phase 4 — Schema Enforcement

* Apply YAML frontmatter from `notes/schema.yaml`

**Hard invariants**

* No missing required fields
* No extra fields
* Frontmatter precedes content
* Slug consistency enforced

Violation ⇒ STOP.

---

#### Phase 5 — HTML Publication

* Subagent: publisher
* Output: `index.html`

**Gate:** HTML exists and references reviewed Markdown content.

---

#### Phase 6 — Link & Navigation Audit

* Subagent: link auditor

**Gate logic**

* `Block release` ⇒ STOP
* `Release with follow-ups` ⇒ CONTINUE + log warning
* `Safe to release` ⇒ CONTINUE

---

#### Phase 7 — Changelog Update

Append to `CHANGELOG.md`:

* ISO date
* Action
* Slug + path
* Warnings (if any)

---

### 7. Global Invariants

* Orchestrator never writes prose
* All generative actions use `runSubagent`
* No step skipping
* No silent failure
* All blocking verdicts halt execution

---

### 8. Stopping Conditions

Execution MUST stop if:

* A blocking verdict is returned
* Schema validation fails
* Unauthorized file access occurs
* Required artifact is missing

On stop, return:

* Phase failed
* Reason
* Artifacts produced so far

---

### 9. Observability & Logging

At minimum, log:

* Slug
* Phase transitions
* Verdicts
* Warnings
* Files written

Logs may be ephemeral unless otherwise configured.

---

### 10. Non-Goals

* SEO optimization
* Marketing copy
* Academic validation
* Automatic cross-link insertion

These require separate contracts.

---

### 11. Contract Status

* **Maturity:** stable v1
* **Intended half-life:** 12–18 months
* **Change policy:** versioned, explicit migration notes required

---

### 12. Contract Principle

> Agents execute.
> Contracts decide.
> Humans refine the contract.

