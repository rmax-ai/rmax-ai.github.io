# Publishing Run: ai-fde-operating-model

Date: 2026-06-16
Slug: `ai-fde-operating-model`
Source inbox path: `inbox/ai-fde-operating-model.md`

## Step Status

- Step 0 Intake & Setup: completed
- Step 1 Write Technical Note: completed
- Step 2 Editorial Review: completed
- Step 2b Effective Writing Refinement: completed
- Step 3 Failure-Mode Review: completed
- Step 4 Apply YAML Frontmatter: completed
- Step 5 Publish HTML: completed
- Step 6 Link Audit + Navigation: completed
- Step 7 Update CHANGELOG: completed
- Step 8 Generate Sitemap: completed

## Workflow Warnings

- `git mv` could not be used for the inbox note because `inbox/ai-fde-operating-model.md` was untracked. The file was moved with `mv` instead so the pipeline could continue.

## Failure-Mode Review

### Failure-Mode Report

1. Risk title: Stage-gated model applied to low-consequence workflows too broadly
   Category: Over-generalization risk
   Trigger condition: A team treats the model as the default delivery pattern for lightweight drafting or summarization work that does not justify explicit stage gates.
   Likely consequence: Process overhead grows faster than risk reduction, and teams stop learning quickly.
   Severity: medium

2. Risk title: Operational maturity assumed rather than guaranteed
   Category: Hidden assumptions
   Trigger condition: Readers adopt the framework without already having clear ownership, usable telemetry, rollback paths, and reviewers who can verify outputs independently.
   Likely consequence: The control language is adopted, but the controls fail when the workflow faces real load or a real incident.
   Severity: high

3. Risk title: Governance structure adopted before a stable workflow exists
   Category: Premature optimization risk
   Trigger condition: An organization builds stage gates, review rituals, and broad governance forums before it has proved one valuable repeated workflow.
   Likely consequence: Exploration slows down, and teams spend energy managing a system that has not earned its complexity.
   Severity: medium

4. Risk title: Synthesis mistaken for standard
   Category: Authority misreading
   Trigger condition: The references to NIST, ISO, SRE, and the EU AI Act lead readers to treat the note as normative guidance rather than as an operator model.
   Likely consequence: Readers may cite the note as a best-practice standard in contexts where local constraints or legal requirements differ.
   Severity: medium

5. Risk title: Human approval used as paper control
   Category: Operational misuse
   Trigger condition: Teams copy the oversight framing but do not provide reviewers enough evidence, time, or intervention power.
   Likely consequence: The workflow looks governed while still allowing automation bias, weak review, and unsafe promotion into production.
   Severity: high

6. Risk title: Example workflows age faster than the core control logic
   Category: Longevity risk
   Trigger condition: Tooling patterns, pilot practices, or regulatory interpretations shift while the note remains online.
   Likely consequence: Readers may over-focus on dated examples and miss the more durable sequencing argument.
   Severity: medium

### Boundary Adequacy Assessment

The note states its scope reasonably well: it is aimed at governed AI workflows rather than at every AI feature. A careful reader may still hesitate about the threshold for adopting this model, especially in smaller teams where the control overhead could outweigh the operational risk.

### Publishability Verdict

Publish with caution note.

## Link Audit Report

### Broken Links

None found in:

- `notes/ai-fde-operating-model/index.md`
- `notes/ai-fde-operating-model/index.html`
- `notes/index.html`
- `index.html`
- `sitemap.xml`

### Orphaned Content Warnings

None. The note is linked from both `notes/index.html` and the home-page Notes section in `index.html`.

### Navigation Gaps

None for the new note after navigation updates.

### Inconsistent Paths or Slugs

None. The markdown frontmatter slug, directory name, canonical URL, published HTML path, and sitemap entry all resolve to `/notes/ai-fde-operating-model/`.

### External Link Anomalies

None detected locally. The markdown note preserves the source URLs from the inbox reference block, and the published HTML contains standard site navigation plus those reference links.

### Discoverability Verdict

Fully discoverable.

### Publish Gate Recommendation

Safe to release.
