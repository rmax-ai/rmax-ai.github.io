# Editorial review: RMax AI, Year One — From Agents to Verified Work

**Reviewer:** rmax-10 (editorial leg, delegation trigger `rmax-ai/delegation-queue#345`)
**Date:** 2026-11-19
**Source:** `inbox/rmax-ai-year-one-from-agents-to-verified-work.md` (head `f39a003d1fe5f94d574966bd805658d790424017`)
**Output:** `notes/rmax-ai-year-one-from-agents-to-verified-work/` + a reader-facing evidence appendix
**Evidence cutoff:** 2026-11-18. No number in the note is drawn from a later census.

## Verdict

**Publish with caution.** The argument, chronology, chronology-gaps framing and conclusion are
supported by the retained audit and the two dated field reports. Two aggregate discrepancies from
the accepted audit remain unreconciled against their original queries; both are disclosed inside
the article and in the appendix, and neither is turned into a chart. Nothing in the note requires a
private repository, a local runtime payload, or an employer identity to be legible.

## Reconciliation of the audit's residual defects

Each item below is the disposition of a specific defect listed on DQ #345. The distinction
"fact / interpretation / proposal" is applied per paragraph, not per article.

| # | Defect as filed | Disposition in the published note |
| --- | --- | --- |
| 1 | Attempt categories sum to 1,380 against a stated 1,375; 518/1,375 = 37.7% | Both numbers are stated together in "Where the system still falls short". Figure 3 panel B uses the **stated** denominator (1,375) and prints 810 OK + 518 acceptance failures + 47 other non-success, i.e. the seven listed categories less the five unclassified records. The five are named in the caption prose as lying outside the classified total. No complete attempt-state composition is published; the 37.7% is labelled audit-reported. |
| 2 | Inbox labels total 834 against 844 requests; overlap with 291 open issues not given | Reported as 834 accounted (590 consumed + 241 answered + 3 pending) with ten unaccounted, explicitly left unclassified, and with the open-issue count stated as a separate snapshot rather than a subset. No pie chart, no completion rate. |
| 3 | 77 dated articles + 1 redirect = 78 pages; January 17 exceeds June 14 | Stated exactly that way in "Knowledge and publication". The note calls 78 *published note pages*, not 78 articles, and January is the publication peak. |
| 4 | 11,393 monthly search matches vs 11,336 after upstream-history subtraction | Neither figure is used as an authorship measure. The note separates imported upstream framework history from the lab's integration work and makes no unique-output claim. |
| 5 | `rmax-flow-engine` has an implemented bounded slice; architecture README documents an ADR numbering repair | Removed the blanket "concept-only" and duplicate-ADR framings. The note avoids per-repository maturity labels and publishes no ADR count. |
| 6 | Architecture, flow-engine, system-review, DQ and Inbox are private | No private URL or raw payload appears in the note or appendix. Aggregate figures are scoped facts stated without source links, which is what the accepted evidence permits. |
| 7 | Relative evidence links break when moving from `inbox/` to `notes/<slug>/index.md` | Resolved by building a real route: `notes/rmax-ai-year-one-from-agents-to-verified-work/evidence-notes/index.html`, linked as `evidence-notes/` from three places (body, status section, sources list). The appendix is generated from `processed/.../evidence-notes.md` and carries its own canonical URL, footer and backlink. |

## Fact / interpretation / proposal separation

| Class | Where it appears | Handling |
| --- | --- | --- |
| **Fact** (audit-reported, dated) | 145 repositories, 1,078 tasks (809/210/58/1), 77 dated notes, 291 open requests, 155 findings in 53 reports, USD 298.27 for Sep–Nov, 159-call Jev/Clef battery with a 24-decision label subset | Every figure carries its denominator and its 2026-11-18 cutoff. "Audit-reported" is stated wherever the article cannot re-derive the number. |
| **Interpretation** (the article's reading) | "Detection has outpaced demonstrated learning"; the 37.7% as a statement about how acceptance criteria were written; April as dormancy in the inspected records only | Marked as reading, with the counter-reading (cause unknown, records incomplete) kept in the same paragraph rather than dropped. |
| **Proposal** (2027 priorities) | Reduce acceptance failures toward 10%; disposition 95% of answered requests within 48 h; ceiling of 110 active repositories | Introduced as "proposed objectives for an initial 90-day programme, not commitments, and not completed work", and repeated in the appendix as proposals whose baselines must be re-established. |

## Editorial changes made to the draft

1. **Structure.** Opened on the narrow question the lab actually started with, then moved to the
   three distinctions (delivered message / recorded success / capable model) so the rest of the
   article has a spine instead of a project catalogue.
2. **Chronology.** Added the evidence-gap framing to the timeline (November 2025 is operator
   accounting; earliest durable artifact is 23 December) and kept the July–November table as the
   article's one long table, with an "evidence boundary" column instead of prose hedging.
3. **Density.** Cut per-project narrative in favour of what each project demonstrates; the projects
   now appear as four capability clusters rather than eleven summaries.
4. **The unenforced edge.** The control loop is drawn with the adoption step explicitly amber and
   described in the caption as "the transition the system does not yet enforce consistently". This
   is the article's main interpretive claim and it is drawn, not asserted in passing.
5. **Conclusion.** Replaced an optimistic close with the narrow honest result and the replacement
   headline metric (share of delegated work still usable a year later).
6. **Compliance sections.** Added the positioning note, the status/scope disclaimer and a numbered
   sources list required by the publishing contract.

## Figures

Three figures, each authored at two widths so no figure is scaled into illegibility. Editable
source: `processed/rmax-ai-year-one-from-agents-to-verified-work/figures/render_figures.py`
(deterministic — re-running reproduces identical bytes, verified by `sha256sum -c`).

| Figure | Wide | Mobile | What it cannot establish |
| --- | --- | --- | --- |
| 1 — operating-model timeline | `fig-1-timeline.svg` (760×663) | `fig-1-timeline-mobile.svg` (380×812) | Segment widths are categorical, not proportional to elapsed time; the April dormancy is observed in the inspected records only. |
| 2 — control loop and ownership | `fig-2-control-loop.svg` (760×640) | `fig-2-control-loop-mobile.svg` (380×824) | Arrows are responsibilities, not a guarantee that every historical task traversed the path; the dashed edge is the adoption step the system does not enforce. |
| 3 — task vs attempt outcomes | `fig-3-outcomes.svg` (760×386) | `fig-3-outcomes-mobile.svg` (380×432) | Two denominators share no axis: 1,078 recorded tasks, 1,375 classified attempts. The 5 unclassified records sit outside panel B and outside the total. |

Same-denominator check: panel A sums 809 + 210 + 58 + 1 = 1,078 (100.0%); panel B sums
810 + 518 + 47 = 1,375 with the 5 unclassified records excluded and named. The two panels are
captioned as non-composable, and the note never adds them.

Render evidence: `processed/rmax-ai-year-one-from-agents-to-verified-work/figures/render-check.json`
— 6 figures at authored width plus both pages at 1440 px and 390 px, `RESULT PASS 10/10`. Every
capture is ≤ 8192 px on both axes, the transport bound the interrupted 2026-11-19 session exceeded:
its final request was rejected with HTTP 400 on a full-page capture whose height passed 8 192 px.
Page screenshots here are capped at 2000 px tall by construction, so the check cannot reproduce that
failure mode.

## Publishing-contract receipts

| Phase | Gate | Result |
| --- | --- | --- |
| 0 Intake | slug ↔ directory ↔ frontmatter slug | `rmax-ai-year-one-from-agents-to-verified-work` in all three |
| 1 Draft | non-empty draft | 3,347 words |
| 2 Editorial review | `scripts/audit_technical_note_structure.py` | exit 0 — "All audited notes include practical takeaways, positioning, and status language." |
| 3 Failure-mode review | no content edits | Publish with caution (two disclosed aggregate discrepancies); no blocking finding |
| 4 Schema | required fields only, no extras | all 14 `notes/schema.yaml` fields present, none added, frontmatter precedes content |
| 5 HTML | footer contract | `/styles/footer.css`, `rmax-footer` markup, `window.footerThoughts` with exactly 3 page-specific items, `/scripts/footer.js` |
| 6 Link & navigation audit | block / follow-ups / safe | Release with follow-ups: canonical and appendix route are `not_yet_deployed` pre-merge; all internal links resolve locally |
| 7 Changelog | entry appended | `CHANGELOG.md` 2026-11-19 entry with warnings |
| 8 Sitemap | well-formed, rmax.ai only | 88 URLs (86 + note + appendix), parses, all `https://rmax.ai/` |

Discovery surfaces updated for this note: home `index.html`, home `index.md`, `notes/index.html`,
`sitemap.xml`.

One defect found and fixed during review: the generated `index.html` left
`<div class="post-content">` unclosed before `</article>` (browsers recover, the DOM nesting does
not). It is now closed, and the appendix builder copies the corrected shell.

## Remaining human decisions

1. **Merge and deploy.** Operator-owned. The note is drafted and validated on
   `spec/issue-345-year-one-retrospective` and stays unpublished until an operator merges PR #107.
2. **Attempt-census reconciliation.** Recovering the original collection query for the 5
   unclassified attempt records is the only path to a complete attempt-state figure. Until then the
   article publishes a stated denominator with a disclosure, which is a deliberate choice.
3. **Request-channel cross-tabulation.** A joint census of the 834 labelled requests against the 291
   open issues would license an open/closed analysis. Not attempted here.
4. **Reading-order position.** The note is listed first on all discovery surfaces as the newest
   publication. If it should be pinned rather than date-ordered, that is an editorial choice.
5. **2027 priorities.** Governance, not publication: the three proposals require an owner and a
   baseline before any measurement window starts.
