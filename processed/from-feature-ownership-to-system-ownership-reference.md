# Inbox source — "From Feature Ownership to System Ownership"

Target slug: `from-feature-ownership-to-system-ownership`
Target path: `notes/from-feature-ownership-to-system-ownership/index.md`
Publication date: 2026-09-28

This file is the complete raw material for the writer: the editorial brief, the independently re-verified evidence map (every quantitative figure below was re-derived from its primary source on **2026-09-28** — use exactly these figures and caveats), the three exact Mermaid diagram sources, the cross-link list, and the hard publication-boundary rules. Follow it. Where this brief and the repository's binding contract (`docs/contracts/publish-technical-note.md`) conflict on process, the contract wins.

## 1. Editorial brief

- **Audience:** senior engineers, staff-plus ICs, and engineering leaders who already use coding agents intensively (or evaluate them seriously). Assume fluency with agent workflows, CI, and platform engineering; do not explain basics.
- **Register:** practitioner analysis — concrete before abstract, mildly skeptical, evidence-labeled. No AI-hype rhetoric, no futurism, no provider marketing. Where evidence is thin, say so in the sentence itself.
- **Thesis (hold this):** *Coding agents are beginning to change senior software engineering less by eliminating implementation than by making implementation capacity programmable. In agent-intensive teams, the engineer's leverage increasingly comes from defining intent, architecture, constraints, verification and operational feedback systems that allow many implementation tasks to execute safely in parallel. This extends the DevOps tradition of end-to-end ownership into a new form: ownership of the software-production system itself. The transition is already visible in frontier teams and production case studies, but evidence that it has broadly produced smaller teams or flatter organizations remains preliminary.*
- **The distinction that matters:** AI increasing implementation productivity is the weaker, better-evidenced claim. AI changing **what an engineer owns** is the claim this article is about. Keep the two separate everywhere.
- **Ownership-outcome discipline (the claim's weakest joint — treat it as such):** throughput, PR counts, and agent counts cannot establish a role change. The ownership claim may only lean on (a) direct role evidence — the Vella & Blincoe longitudinal survey (self-report; label it) and (b) documented workflow duties in production accounts (who specifies tasks, maintains harnesses, gates changes, handles incidents, closes telemetry loops — label as observed-in-account or inferred). If in drafting the direct role evidence cannot carry a clause, drop that clause rather than deriving ownership from throughput. The pre-registered fallback thesis if the direct evidence fails: *"In several documented frontier workflows, coding agents make some implementation tasks delegable and create substantial verification and integration work. Some teams have built reusable systems to coordinate that work. Current evidence does not establish a general change in senior engineers' responsibilities or AI-caused changes in team size or hierarchy."*
- **Conclusion boundary:** the thesis is supported **partially** — comparatively strong evidence for workflow/bottleneck change; weak, mostly correlational evidence for organizational restructuring. Do not upgrade it in the telling; organizational data is *context only* — do not write "acceleration" as a finding (at most, one clearly-labeled interpretation sentence, or omit).
- **Length:** 2,000–3,000 prose words (a 10–14 minute technical read). Tables and diagrams carry detail; prose carries the argument.
- **Evidence discipline (label in the prose, not only in footnotes):**
  - measured results (randomized: METR, Microsoft RCT) vs observational/simulation (AgenticFlict, concurrent-agents, agent-PR study) vs survey (DORA, Vella & Blincoe) vs vendor case accounts (OpenAI, Anthropic, Cursor cases — existence proofs, not generality) vs author estimates/counterfactuals (Bun year-estimate, OpenAI 1/10th-time, Faire 18-month migration) vs interpretation (this note's readings).
  - On first mention of each study/case, name its type inline ("a randomized field experiment", "a survey of", "a simulation study", "a company account") — the References section alone does not preserve evidence type.
  - Keep **workflow/bottleneck evidence** separate from **organizational claims**. Never infer that AI caused smaller teams, flatter orgs, fewer managers, or senior-heavy staffing where the evidence is correlational.
  - Secondary sources (practitioner newsletters) are hypothesis generators only — at most one attributed sentence, never causal evidence.
  - **Causal-language gate:** no "AI caused / flattened / reduced headcount" unless an identification strategy addresses secular trends and selection — none of the sources has one; write associative language only ("concurrent with", "in the same period").

## 2. Verified evidence map (all figures re-verified 2026-09-28 against primary sources)

### A0. Claim ledger & denominator discipline (binding on every number in the note)

1. **Denominator discipline.** Every quantitative sentence preserves its unit, numerator/outcome, denominator, population, window, and comparator: Microsoft = *additional completed tasks per developer in the study window* (not "faster", not "better code"); METR = *task time for 16 recruited developers / 246 sampled issues in 2025* (not universal productivity); AgenticFlict = *simulated processed PRs* (27.67% of 107K+ processed of 142K+ collected — never "of production PRs"); concurrent-agent figures = *the analyzed replay subset* (with the 0.5% base rate); DORA = *survey responses* (association, not experiment); SignalFire = *vendor talent-report data over its own periods*; Carta = *Series-A cohorts by year*. If a missing field would change the reader's interpretation, omit the number.
2. **Construct gating.** A number may only support the construct it measured: task-completion counts are throughput proxies; simulated/replay conflicts are coordination cost in simulation; review-platform telemetry is review events, not accepted-and-useful reviews; survey responses are perceptions. Conflict *incidence* is never presented as merge delay, production loss, or net productivity.
3. **Counterfactual quarantine.** "1/10th the time" (OpenAI), "a full year" (Bun), and Faire's migration compression are author/company estimates — attribute them ("reported", "estimated"); never convert to speedup ratios, never merge with measured figures in one arithmetic claim.
4. **What each class cannot establish (state it where the case does heavy lifting).** Vendor accounts are existence proofs: they can omit failed runs, human rescue, task mix, quality outcomes. A source snapshot proves provenance, not truth. Measured numbers say nothing about unattempted work.
5. **Review-cost adjacency.** Wherever a throughput or generation-volume figure appears (OpenAI PRs, Copilot review volume, agent runs/week), the same section must carry the review/verification/repair cost — never a throughput paragraph that defers all friction to a later section.
6. **Falsifier repetition.** METR's bound is not a single paragraph: repeat a short, specific bound beside the vendor cases, the concurrency section, and the career section (one sentence each, not a caveat pile).

### A. Quantitative anchors — use exactly these figures, with these caveats

| Claim | Exact verified figure / wording to use | Class | Caveat that must travel with it |
|---|---|---|---|
| Microsoft field experiments | "26.08% increase (SE: 10.3%) in completed tasks" across three field experiments and **4,867** developers; "less experienced developers had higher adoption rates and greater productivity gains" | Randomized field experiments (Microsoft, Accenture, one anonymous Fortune 100) | Wide SE; task-completion count — not speed, not quality |
| METR early-2025 | "when developers use AI tools, they take **19% longer** than without"; 16 experienced open-source developers; 246 real issues; CI +2% to +39% | Randomized controlled trial | Early-2025 tools on mature, familiar repos; n=16 |
| METR 2026 update | "our data is only **very weak evidence** for the size of this increase"; selection effects (task choice; pay cut $150→$50/hr); design being changed | Follow-up methodological note | The bound on ALL later-speedup claims |
| DORA 2025 | "survey responses from nearly 5,000 technology professionals"; 100+ hours qualitative; "AI's primary role is as an **amplifier** — it magnifies the strengths of high-performing organizations and the dysfunctions of struggling ones" | Industry survey | Self-report; correlational; amplifier framing is the report's interpretation |
| OpenAI harness | 5-month experiment; "0 lines of manually-written code"; 3 engineers → 7; "~1,500 pull requests"; "~1 million lines of code"; "3.5 PRs per engineer per day"; runs "upwards of 6 hours" | Vendor first-party case (existence proof) | "built in approximately **1/10th the time** it would have taken by hand" = author estimate — attribute; failed runs not disclosed |
| OpenAI Symphony | "**500% increase** in landed pull requests **on some teams** within the first three weeks"; interactive ceiling 3–5 agent sessions | Vendor first-party case | Keep "some teams" + "first three weeks" |
| Anthropic compiler | "**16 agents**"; "nearly **2,000** Claude Code sessions"; "**$20,000**"; "a **100,000-line** compiler that can build Linux 6.9 on x86, ARM, and RISC-V"; two weeks; 2B input / 140M output tokens | Vendor first-party technical account | The concurrency failure story is as important as the result |
| Bun Rust rewrite | "**535,496 lines** of Zig"; "**~50 dynamic workflows** … **11 days**"; "**64 Claudes** running for 11 days"; "**6,778 commits**" (May 3 → merged May 14); net diff +1,009,272; "0 tests skipped or deleted" | Vendor first-party account (git-log measured) | "would take a small team … a **full year**" = author counterfactual — attribute; human monitoring continued throughout |
| AgenticFlict | "**142K+** Agentic PRs collected from 59K+ repositories, of which **107K+** are … processed through deterministic merge simulation"; "**29K+** PRs exhibiting merge conflicts, yielding a conflict rate of **27.67%**"; "336K+ fine-grained conflict regions" | Observational simulation study | Simulated, not live; preprocessing scope; keep the full fraction |
| Concurrent agents | cross-agent vs intra-agent textual conflict: "**41.7% vs. 19.8%**" (non-overlapping 95% CIs), in the analyzed replay subset | Observational replay study | Base rate: "only **0.5%** of co-active pairs were cross-agent" — both numbers, same sentence pair |
| Agent PR failures | "**33k** agent-authored PRs" from five agents; highest merge success: documentation/CI/build; worst: performance, bug-fix; not-merged = larger diffs, more files, CI failures; 600-PR taxonomy (reviewer disengagement, duplicates, unwanted features, misalignment) | Large-scale observational study (MSR 2026) | Correlation; five agents, one era |
| Vella & Blincoe | two-wave survey: 158 → 101 participants, matched n=95; "**82%** reporting less [time] on writing code"; shift "from creation to **verification**"; "**supervisory engineering work**"; paradox: **84%** perceived improvement, worsened experience "from **14% to 27%**" | Longitudinal survey (self-report) — the DIRECT role evidence | Perceptions, not measurements; 6-month window; single cohort |
| SignalFire State of Talent | EM spans "**~12** (up from 10)" at tech majors (+14% vs 2019); startups "**~15**" (+34%); PMs +22%; engineers "**55% of all hiring**" (46% in 2019) | Recruiting-firm report (proprietary data) | Correlational; vendor dataset; context only |
| Carta | "Series A in **2024** had a median of **15** full-time employees, down from **22** in **2022**"; author: "would be inaccurate to pin the entirety of this" on AI; "No final conclusions yet" | Marketplace data note | Mirror the author's own no-causation stance |

### B. The five "strong" claims and their sources

1. **Implementation leverage rises in bounded regimes.** Lead with the Microsoft RCT; vendor cases are existence proofs only.
2. **Frontier teams already run multiple agents and reusable harnesses.** OpenAI harness; Symphony; GitHub "Mission Control"; Cursor Automations (internal: security review on push, agentic codeowners, incident response); Faire (25+ automations, 2,000+ runs/month); Amplitude (1,000+ runs/week).
3. **Throughput shifts scarce attention toward review, verification, integration.** Harness post: "the bottleneck became **human QA capacity**". Symphony: bottleneck "became **human attention**"; 3–5 session ceiling. Copilot code review: "**60 million**" reviews, 10× growth, "more than **one in five** code reviews on GitHub", "**12,000** organizations" auto-run. Bugbot: resolution "**52% to over 70%**". Vella & Blincoe: creation→verification shift. (Pair every throughput figure with the review-cost sentence — see A0.5.)
4. **Level 3/4 workflows exist in real production.** Harness (prompt → agent → PR → agent reviews → iterate); Symphony (board control plane; agents file follow-ups; DAGs); Bun (concurrency in the low tens); Anthropic compiler (multi-week, oracle-verified).
5. **Engineers in such teams increasingly work on specification, environment design, constraints, orchestration, verification, feedback.** Hold this to Vella & Blincoe (direct) + documented duties in accounts; do not inflate into a general occupational claim.

### C. Falsifiers — main narrative, adjacent to the claim they bound

1. **METR 19% slowdown** — immediately after the first leverage claim (section 2/3). Not a caveat paragraph.
2. **METR's own limits** — directly after falsifier 1: "only very weak evidence" of improvement later; selection effects; design under revision.
3. **Agent-PR failure concentration** — in the verification section: harder/larger/integration-heavy work fails most; CI failures; rejection taxonomy.
4. **Concurrency/merge costs** — concurrency section, with base rate: 27.67% conflict rate (simulated); 41.7% vs 19.8% (replay subset); Anthropic's overwrite story until a deterministic oracle. Never aggregate the two studies; never convert conflict incidence to delay.
5. **Pre-AI org trends = mandatory controls, placed FIRST in the organizational section (before any AI reading).** Meta 2023 "Year of Efficiency" (≈10,000 roles cut + 5,000 open reqs closed; "make our organization flatter by removing multiple layers of management") — before coding agents existed; the post-2022 efficiency cycle; Carta 2022→2024; SignalFire spans. AI = concurrent, not established cause.
6. **Leverage transfers to senior reviewers** — Vella & Blincoe paradox (84% perceived improvement vs 14%→27% worsened experience; flow and cognitive load eroding while feedback loops improved) — the work moved and changed character; total effort reduction is not demonstrated.

### D. Production cases (use; keep bounded)

- **OpenAI harness** (Feb 2026): 0 hand-written lines; "a map, not a 1,000-page instruction manual"; per-worktree bootable apps + CDP + logs/metrics; "Ralph Wiggum Loop"; humans optional reviewers; "**Humans steer. Agents execute.**" — Then: what the account does not establish (failed runs, human rescue, task mix).
- **OpenAI Symphony** (Apr 2026): board as control plane; every open task gets an agent; tickets "can represent much larger units of work"; spec open-sourced.
- **Anthropic compiler**: multi-agent overwrites required a deterministic oracle (GCC cross-checks); measured cost/tokens stated plainly.
- **Anthropic harnesses** (Nov 2025): "Effective harnesses for long-running agents" — human-engineer-inspired structure; four named failure modes.
- **GitHub Mission Control** (Dec 2025): "from babysitting single agent runs to orchestrating a small fleet".
- **Cursor cases**: Bugbot (52%→70%+, 40 experiments, 2M+ PRs/month); Amplitude (3× weekly production commits; 60–70% of low-risk PRs merged directly; cloud-vs-local ceiling); Faire (2× PR throughput; 18-month migration compressed — attribute).

### E. Historical controls (mandatory lineage, section 7)

specialist roles → full-stack → DevOps ("you build it, you run it" — Vogels, ACM Queue, **2006**) → platform engineering (Backstage: first internal version **2018**, "over 2,600 companies") → Staff+ system ownership → AI-assisted engineering → agent orchestration → production-system ownership. **Present this as overlapping, dated antecedents — not a clean succession**: each practice coexisted with the others; reserve novelty strictly for *documented, dateable* instances of programmable implementation capacity (agents + reusable harnesses + verification gates). "First"/"new" claims must be scope-limited.

## 3. Suggested structure (9 sections; adapt titles, keep the arc)

1. **The feature is losing its monopoly as the unit of engineering work** — what an engineer "owns" when implementation is delegable; state the question precisely (ownership, not speed).
2. **Implementation leverage, immediately bounded** — Microsoft RCT numbers, then METR 19% + the 2026 selection-effects bound, same section.
3. **Where the bottleneck goes** — review, verification, integration, specification — with cost figures adjacent to throughput figures; the harness post's "human QA capacity"; Symphony's "human attention"; Copilot review volume; Bugbot; agent-PR failure concentration (falsifier 3). Introduce the "software-producing system".
4. **The machines that actually exist** — OpenAI harness + Symphony, Anthropic compiler + harness engineering, Bun, carefully caveated Cursor cases; each followed (same section) by its non-established remainder + a one-line METR-bound reminder.
5. **Concurrency and coordination economics** — conflicts and overwrites as the bill (falsifier 4); verification/integration as the scarce resource; Anthropic's oracle story.
6. **Smaller teams, flatter orgs: context, not cause** — controls first (Meta 2023, post-2022 cycle, Carta), then SignalFire/Carta as concurrent trends, labeled context-only; no untested "acceleration" claim.
7. **The lineage: ownership is old; programmable implementation capacity is the new element to test** — Vogels 2006 → platform engineering → Staff+; overlapping antecedents (section E).
8. **What it means role by role** — junior/mid: raised floor, different ladder; senior/staff: system ownership, verification, architecture; managers: the calibration framing, attributed; no "learn AI or die"; repeat one concrete bound.
9. **The operational question** — close on: "What system would let this class of feature be implemented, verified, shipped, observed and improved repeatedly without depending on me to write every line?" — and make the close conditional: this asks for design work that must itself be verified and operated; state the boundary honestly.

## 4. Diagrams (exactly three; use these exact sources)

Embed byte-identically: ` ```mermaid ` fenced blocks in `index.md`; `<pre class="mermaid">` blocks in `index.html` (flush-left at column 0, content indented four spaces in HTML). Never `<br/>`, `<`, or a raw `&` inside a diagram block. Include the `pre.mermaid` CSS rule and the page-level Mermaid runtime module with the dark themeVariables exactly as in the most recent published note's HTML.

**Diagram 1 — feature ownership and system ownership (overlapping, not replaced)** (section 1 or 2):

```
flowchart TD
    subgraph before["Feature ownership"]
        F1["Feature request"] --> F2["Design the change"] --> F3["Write the code"] --> F4["Review and merge"] --> F5["Ship the feature"]
    end
    subgraph after["System ownership - additional layer in agent-intensive teams"]
        S1["Intent and constraints"] --> S2["Task decomposition"] --> S3["Agent implementation"] --> S4["Verification and integration"] --> S5["Deploy, observe, feed back"]
        S5 --> S1
    end
    F5 ~~~ S1
    classDef neutral fill:#1f2937,stroke:#6b7280,color:#e6eef8
    classDef blue fill:#1e3a5f,stroke:#3b82f6,color:#e6eef8
    class F1,F2,F3,F4,F5 neutral
    class S1,S2,S3,S4,S5 blue
```

**Diagram 2 — where the bottleneck can migrate (conditional on measured allocation shifts)** (section 3):

```
flowchart TD
    B1["Implementation leverage rises in some regimes"] --> B2["Review and verification load grows"]
    B2 --> B3["Integration and human attention become the constraint"]
    B3 --> B4["Leverage moves to specification, architecture, and feedback design"]
    classDef good fill:#14532d,stroke:#22c55e,color:#e6eef8
    classDef blue fill:#1e3a5f,stroke:#3b82f6,color:#e6eef8
    classDef gate fill:#3b1f6e,stroke:#7c3aed,color:#e6eef8
    class B1 good
    class B2,B3 blue
    class B4 gate
```

**Diagram 3 — the software-producing loop, with human gates** (section 3 or 9):

```
flowchart TD
    H["Engineer defines intent, architecture, constraints"] --> A["Implementation agents run tasks in parallel"]
    A --> V["Tests, evals, review, security gates"]
    V --> D["Integration and deployment"]
    D --> P["Production telemetry"]
    P --> F["Diagnosis and improvement"]
    F --> H
    H --> G["Human approval gates - where documented"]
    G --> D
    classDef neutral fill:#1f2937,stroke:#6b7280,color:#e6eef8
    classDef gate fill:#3b1f6e,stroke:#7c3aed,color:#e6eef8
    classDef good fill:#14532d,stroke:#22c55e,color:#e6eef8
    class H,A,D neutral
    class V,G gate
    class P,F good
```

Each diagram must be paralleled by prose: every node/edge's claim appears in the text with its evidence class, or the diagram element carries its explicit conditional/conceptual qualifier. No additional diagrams; no diagram that restates a table.

## 5. Cross-links (natural placement only — do not force) and required sources

- `https://rmax.ai/notes/the-harness-is-becoming-the-runtime/` — section 4 or 9: harnesses as the programmable runtime layer.
- `https://rmax.ai/notes/verification-first-software-engineering/` — section 3: verification systems as the durable asset when implementation cost falls.
- `https://rmax.ai/notes/the-change-is-the-unit-of-assurance/` — section 3 or 5: assurance attaching to changes and evidence, not prose.
- `https://rmax.ai/notes/beyond-evals-assurance-model/` — section 3 or 8: beyond evals — evidence, controls, verification in production agent systems.
- `https://rmax.ai/notes/from-human-orchestrated-agent-to-autonomous-control-plane/` — sections 4/8: continuity with the field report on operating agent systems.

Every non-common factual claim links inline to its primary source at first substantive mention. These URLs must appear in the note (References carries the full list):

- https://openai.com/index/harness-engineering/ · https://openai.com/index/open-source-codex-orchestration-symphony/
- https://www.anthropic.com/engineering/building-c-compiler · https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://bun.com/blog/bun-in-rust
- https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/
- https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ · https://metr.org/blog/2026-02-24-uplift-update/
- https://dora.dev/research/2025/dora-report/ · https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- https://arxiv.org/abs/2605.23135 · https://arxiv.org/abs/2601.15195 · https://arxiv.org/abs/2604.03551 · https://arxiv.org/abs/2607.04697
- https://github.blog/ai-and-ml/github-copilot/how-to-orchestrate-agents-using-mission-control/ · https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/
- https://cursor.com/blog/automations · https://cursor.com/blog/building-bugbot · https://cursor.com/blog/amplitude · https://cursor.com/blog/faire
- https://www.signalfire.com/blog/signalfire-state-of-talent-report-2026 · https://carta.com/data/newsletter-ai-takes-startup-jobs/
- https://about.fb.com/news/2023/03/mark-zuckerberg-meta-year-of-efficiency/
- https://aws.amazon.com/blogs/aws/acm_queue_inter/ · https://backstage.spotify.com/discover/backstage-101
- https://newsletter.pragmaticengineer.com/p/the-great-engineering-leader-career-break (secondary — attributed only)

## 6. Public boundary (hard rules)

- The note cites only public destinations (rmax.ai pages, the sources above). No private repository names, no internal issue numbers, no chat links or contents, no local filesystem paths, no credentials, no prompts or traces, no operator-identifying material.
- No tracking parameters in any link (`utm_`, `?ref=`, `fbclid`).
- Numbers appear exactly as given in this brief with their caveats; do not introduce numbers from anywhere else.

## 7. House requirements

- End sections in order: **Practical Takeaways** (3–6 bullets), **Positioning Note**, **Status & Scope**, **References** (linked list).
- Frontmatter per `notes/schema.yaml` — exact fields, slug equals directory; `date`/`updated`: `2026-09-28`; `author: Max`; `section: notes`; canonical URL `https://rmax.ai/notes/from-feature-ownership-to-system-ownership/`; `reading_time` calibrated to the final prose count at ~206 words/min, formatted `N–M min read`.
- No "Editorial Notes" artifacts; no TODOs; no placeholders. Final compression pass after tables/diagrams — remove prose that merely restates them.
- After the last substantive edit, re-verify (grep-level) that every quantitative sentence still carries its qualifier (reported / measured / simulated / estimate / survey), and that no causal language ("caused", "drove", "led to", "flattened") appears in organizational passages. Fix before finishing.
- The four index surfaces (`index.md`, `index.html`, `notes/index.md`, `notes/index.html`) get the newest-first entry following the newest existing entries exactly (`notes/index.md` dual-entry: short line + heading block).

## 8. Avoid (failure-mode list)

- Universal claims from single cases; "proves", "always", "never"; timeless "agents are faster/slower" (date every capability claim: "early-2025 tools on mature repositories" vs "late-2025→2026 agentic workflows").
- Provider comparisons, leaderboards; vendor numbers presented as measurements (attribute 1/10th-time, full-year, migration figures).
- Any implication that AI caused smaller teams/flatter orgs/fewer managers; flattening is older than coding agents (controls first, context-only framing).
- "Learn AI or die" rhetoric; claims that code comprehension or direct programming is becoming irrelevant.
- Benchmark/simulation-vs-production extrapolation: conflict rates, merge studies, review telemetry describe regimes.
- Dropping caveats: METR n=16 + selection effects; SE 10.3%; survey self-report; vendor selection; 0.5% cross-agent base rate; simulated denominators.
- Leaking review/repair cost out of throughput paragraphs; converting conflict incidence into delay or production loss; aggregating AgenticFlict with the replay study.
