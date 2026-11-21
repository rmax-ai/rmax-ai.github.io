# Year-one article: evidence notes

**Observation cutoff:** 2026-11-18. **Editorial reconciliation:** 2026-11-19.

These notes accompany *RMax AI, Year One: From Agents to Verified Work*. They distinguish the operational audit collected by rmax-10 from the checks performed while preparing the article. Aggregate audit values are historical observations, not live counters. The source audit inspected repository history, runtime records, queue state, publication files and the site sitemap. This companion is a sanitized summary; it does not reproduce private runtime records. Collection-query reproducibility remains an editorial follow-up where noted.

## Baselines and their limits

| Measure | Audit-reported value at cutoff | Interpretation |
| --- | ---: | --- |
| Organization repositories | 145 | Includes experiments, scaffolds and imported history; not a product or original-contribution count. |
| Dated technical notes | 77 | Dated frontmatter spans 2026-01-03–2026-10-25. |
| Note directories / published note routes | 78 | The additional route is an article-moved redirect, not an additional article. |
| Sitemap URLs | 86 total; 79 under `/notes/` | The notes total includes the index and redirect. |
| Queue tasks | 1,078 | Cumulative recorded task states; repeated attempts are separate records. |
| Structured channel requests | 844 | Recorded request volume; does not measure useful answers or completed downstream work. |
| Open channel issues | 291 | Separate lifecycle snapshot; the supplied data does not establish a complete state cross-tabulation. |
| Scheduled jobs | 157, including 144 enabled | Configuration counts, not proof that every job is healthy or useful. |
| Skills | 317 | Installed/source entries, not a count of effective or regularly used capabilities. |
| System-review findings | 155 across 53 reports | Includes 41 classified as silent degradation; classification frequency does not establish incident cost or severity. |
| Tracked agent cost | USD 298.27, September–November cutoff | Partial accounting: 71.06 + 191.65 + 35.56. Not an annual or all-in operating cost. |

The corrected article count supersedes the preliminary draft's 81. Monthly dated-note counts sum to 77 across nine active months. January had 17 and June 14; June must not be described as the publication peak.

## Task outcomes: usable figure data

This partition is arithmetically consistent. Its denominator is **1,078 tasks**, not attempts, PRs or deployments.

| Recorded task state | Count | Share |
| --- | ---: | ---: |
| `SUCCEEDED` | 809 | 75.0% |
| `FAILED` | 210 | 19.5% |
| `CANCELLED` | 58 | 5.4% |
| `RUNNING` | 1 | 0.1% |
| **Total** | **1,078** | **100.0%** |

**Figure caption:** Recorded queue task states at 2026-11-18. Success is the queue's recorded state; this census does not independently establish that every task produced a reviewed, deployed, useful result. The single running task was nonterminal at collection. Percentages are rounded to one decimal place.

## Discrepancies requiring editorial resolution

1. **Attempt totals conflict.** The audit reports 1,375 attempts and 518 `ACCEPTANCE_FAILED` records, giving 37.7% using the stated denominator. The category counts sum to **1,380**. No independent recount or rerun of the collection query established membership in either total. The discrepancy of five remains unresolved. Figure 3 therefore shows only task states.
2. **Channel labels are incomplete.** The listed 590 consumed, 241 answered and 3 pending sum to **834**, ten below the 844-request total. Do not turn those labels into a complete pie chart or assume that all 241 answered requests are within the 291-open subset without a joint census.
3. **Commit measures differ.** The audit's 50,113 default-branch commits minus 38,777 imported Hermes-history commits leaves 11,336. Its separate monthly search series totals 11,393. They are different counting methods; neither proves unique authorship across all repositories. Credit the upstream Hermes framework separately from RMax's integration and operational work.
4. **Closure counts lack a cohort definition.** Monthly “opened” and “closed” values count issues and PRs together. Without the original query semantics, closed items cannot be treated as members of that month's opened cohort. Do not calculate a completion rate from their ratio.

## Historical and causal limits

November 2025 is the operator's inception framing. The audit found no durable artifact before December 23; that is an evidence gap, not proof that nothing happened. January 31 identifies the earliest inspected OpenClaw workspace; May 11 is the reported Hermes migration. These dates do not establish when every agent name or identity first existed.

For April, the audit found zero indexed organization commits/issues and 30 inspected heartbeat-only sessions. This supports dormancy in the inspected records. It does not prove why activity stopped, what happened outside those records, or that a platform change caused recovery.

The audit recorded failed checks but did not classify their causes. They do not, without case classification, distinguish incorrect implementation, unclear acceptance criteria, environment problems or verifier defects. Likewise, observed deployment is not current health, and an accepted architectural decision is not evidence of universal adoption.

## Source reconciliation and public references

The source review found that some inventory labels were broader than their evidence: a bounded execution-engine slice was implemented despite a concept-only category, and the architecture corpus documents an ADR collision repair. Omit blanket maturity labels and an exact unreconciled ADR count. Do not expose private source URLs as reader-facing evidence.

Public references checked during preparation:

- [Deep Research Assistant](https://github.com/rmax-ai/deep-research-assistant/blob/main/README.md): the README describes 27 workflow nodes, 14 bounded agents and partial continuous-research functionality. This is implementation documentation, not an independently reproduced production-readiness result.
- [Jev/Clef study](https://github.com/rmax-ai/jev-vs-clef/blob/main/README.md): two 159-call batteries ran October 3 and October 6. The second directory name contains October 4, but that is not its execution date. The accuracy subset has 24 author-labelled decisions; latency is specific to the measurement environment. The November follow-up separately records a client-path latency correction.
- [Publication source](https://github.com/rmax-ai/rmax-ai.github.io) and [notes index](https://rmax.ai/notes/): historical publication counts should remain bound to the audit cutoff as later articles are added.

The 2027 objectives are proposals. Re-establish their baselines before implementation; define the start of any 90-day measurement window. Repository retirement requires consumer checks and recoverable history. Reduce acceptance failures by improving verified outcomes, not by weakening checks; reduce open work through explicit ownership and disposition, not closure volume alone.
