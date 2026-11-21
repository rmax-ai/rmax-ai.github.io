# Editorial brief: RMax AI, Year One

## Desired result

Turn the accompanying source article into a clear, illustrated field report for engineers and operators building agent systems. Retain a recognizable year-one retrospective: origins, substantial work, concrete accomplishments, failures, and three proposed priorities for 2027.

Working title: **RMax AI, Year One: From Agents to Verified Work**  
Proposed slug: `rmax-ai-year-one-from-agents-to-verified-work`  
Evidence cutoff: **2026-11-18**  
Draft prepared: **2026-11-19**  
State: source draft for editorial review; not a live publication.

The full operational handoff and primary audit references live in the existing private coordination record. This file contains only the public editorial brief. Keep confidential personal/employer material and raw runtime data out of the publication.

## Writing pass

- State the central claim early: useful autonomy requires durable ownership, evidence and verified outcomes.
- Preserve specific accomplishments without treating repo counts, tokens, sessions or task statuses as impact.
- Tighten repetitive governance language. Define the harness and control plane once, then use concrete verbs and examples.
- Make the chronology easy to follow. Distinguish operator-reported inception in November 2025, first surviving project artifacts on December 23, and the first surviving OpenClaw session on January 31.
- Keep the April observation bounded to the inspected records. Do not infer complete personal inactivity or prove a causal autonomy failure from a missing activity series.
- Attribute Hermes to its upstream project; distinguish RMax integration, operation, extensions and experiments.
- Separate implemented slices, tested prototypes, operational paths, current health and demonstrated outcomes.
- Keep roadmap targets explicitly proposed. Explain the baseline, owner and outcome metric, and guard against improving numbers by weakening acceptance or closing unresolved work.
- Preserve the practical takeaways, positioning note, status/scope and factual references required by the site.

## Evidence reconciliation before figures

Use `evidence-notes.md` and `metrics.json`. The original operational audit has unresolved aggregate inconsistencies:

1. Its attempt-result categories sum to **1,380**, but its stated attempt total is **1,375**. The 518 acceptance failures and 37.7% rate are audit-reported; do not draw a full attempt composition chart until the source query is reconciled.
2. Its three listed Inbox label counts total **834**, while total requests are **844**. Do not silently assign the remaining ten to a category or infer how labels overlap the 291 open issues.
3. **77 dated technical notes plus one redirect** produces 78 note pages, not 78 articles. January's 17 notes exceed June's 14.
4. **11,393** monthly commit-search matches and approximately **11,336** default-branch commits after subtracting the imported Hermes history are different measures. Neither is a validated census of independently authored original work.
5. An `ACCEPTANCE_FAILED` result alone does not identify its cause. Preserve the distinction between specification defects, wrong execution roots, bad evaluators, missing artifacts and genuine implementation defects.
6. A canonical ADR numbering repair and implemented RMax Flow slice are documented in source READMEs inspected during preparation. Those repositories are private; do not cite them as publicly reproducible evidence or carry the earlier blanket duplicate-ADR or concept-only classifications into the article.

If a discrepancy cannot be resolved, retain the limitation and select a figure that does not depend on it. Do not update the November 18 baseline with a fresh live count without a separately labelled cohort.

## Illustration plan

### Figure 1 — Evolution timeline

Show five or six meaningful phases from the November 2025 origin framing through the November 18, 2026 audit. Include a visibly distinct evidence-gap marker for November and the observed April dormancy.

The figure should explain changes in operating model: experiments → persistent assistant → governed demos → durable control plane → verification and maintenance debt. It must not imply equal activity or uninterrupted progress in every month.

### Figure 2 — How work continues

Improve the source article's feedback-loop diagram. Distinguish:

- operator authority;
- ChatGPT analysis and rmax-10 coordination;
- GitHub issues, decisions and review as durable state;
- bounded Codex/Droid execution;
- verification, adoption and feedback.

Show where approval remains human and where failed verification returns work. Avoid a dense network of every repository, every channel and every scheduled job. Explicitly label any desired 2027 transition that is not consistently enforced today.

### Figure 3 — Outcomes with denominators

A task-state chart may use the internally consistent **1,078-task snapshot**: 809 SUCCEEDED, 210 FAILED, 58 CANCELLED and 1 RUNNING. Its caption must say these are queue-recorded states, not independently verified shipped products.

Place **518 / 1,375 = 37.7% reported attempt acceptance failures** in a separate annotated callout only if its provenance and unresolved category-total discrepancy remain visible. Do not combine task and attempt percentages in one composition. Prefer omitting the callout if it creates more confusion than insight.

## Rendering and accessibility

Use versioned, editable figure sources and deterministic SVG or another site-supported format. Data-bearing figures require exact values and zero-based axes where applicable. Do not use generated raster art to represent exact architecture or measurements.

Each figure needs a short claim-bearing caption, meaningful alternative text, adequate contrast and a mobile-readable layout. Inspect actual rendered output at desktop and narrow/mobile widths. Keep labels legible, avoid clipped arrows, and provide a prose/table equivalent for essential information.

## Repository workflow and handback

Work in the linked draft PR and preserve its source/evidence provenance. Follow the repository's existing `WORKFLOW.md`, publishing contract, fixed prompts and technical writing/revision skill when preparing the reviewed `notes/rmax-ai-year-one-from-agents-to-verified-work/` Markdown/HTML package.

When moving the source from `inbox/` to `notes/<slug>/index.md`, update all relative evidence links or provide a reader-accessible published appendix. Check both GitHub Markdown and rendered HTML destinations.

Record review findings in `processed/rmax-ai-year-one-from-agents-to-verified-work/editorial-review.md`. Include factual corrections, major edits, figure files and checks, remaining uncertainties and a clear review verdict. Run the structure audit, frontmatter checks, canonical/footer checks, navigation audit and sitemap validation as applicable.

The requested handback is a reviewed PR and a durable completion report. A Slack ACK or a written plan is not the editorial deliverable. Merge and live publication remain a separate operator action.

