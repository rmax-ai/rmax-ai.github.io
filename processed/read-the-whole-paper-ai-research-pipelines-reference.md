# Inbox source — "Read the Whole Paper: Lessons from Benchmarking AI Research Pipelines"

Target slug: `read-the-whole-paper-ai-research-pipelines`
Target path: `notes/read-the-whole-paper-ai-research-pipelines/index.md`
Publication date: 2026-09-27

This file is the complete raw material for the writer: the editorial brief, the verified evidence (every figure below was re-verified against the public benchmark repository on 2026-09-27), the exact Mermaid diagram sources, and the hard publication-boundary rules. Follow it. Where this brief and the repository's binding contract (`docs/contracts/publish-technical-note.md`) conflict on process, the contract wins.

## 1. Editorial brief

- **Audience:** senior engineers and platform builders who run LLM/agent pipelines in production. Assume they know retrieval, structured outputs, and model routing; do not explain basics.
- **Register:** engineering field report / benchmark-driven architecture note. "We hypothesized", "we measured", "the tested strategy failed", "the evidence suggests", "we changed the architecture". No marketing tone, no provider leaderboard.
- **Thesis (hold this):** Every compression boundary in an AI pipeline must prove that it preserves the evidence the downstream system needs.
- **The interesting result is not that one model won a benchmark.** It is that two plausible efficiency optimizations both introduced information loss, while a simpler architecture performed better — for less money. The subject is pipeline architecture, information loss, evidence integrity, and empirical simplification.
- **Length:** ~8–12 minute technical read. Target ~2,100–2,400 prose words. Tables and diagrams carry detail; prose keeps the experimental narrative moving.
- **Prose rhythm per hypothesis:** intuition → experiment → observed failure → mechanism → architectural change → remaining uncertainty.
- **Separate registers explicitly where claims are made:** observed (measured in the benchmark) / interpretation (our reading) / open (not yet established). When in doubt, qualify down.

## 2. The narrative spine (fixed — do not restructure)

```
Hypothesis 1 — "We don't need to read the whole PDF."
  → selective page reading
  → missed load-bearing evidence
  → rejected

Hypothesis 2 — "Use a cheap model to extract evidence, then hand a small packet to the stronger model."
  → Gemini evidence packet → Luna synthesis
  → information lost at the handoff
  → rejected

Simpler measured path — full text → one model (Luna, reasoning off) → deterministic evidence verification
  → better measured quality, lower complexity, lower cost than the tested two-stage pipeline
```

The write-up must not turn this into a provider comparison. The two staged arms are architecture probes, not model endorsements.

## 3. Verified evidence map (all figures verified 2026-09-27 against the public repository `rmax-ai/ai-papers-routing-benchmark`)

### Experiment 1 — selective reading (the "DQ79" evaluation)

Source anchors: `report/report.md` (Layer 2, Layer 4, generator×evaluator matrix, cost table) and `artifacts/failures/selective-reading.md`.

- The selective strategy used visual page-image reads (Gemini Flash-Lite, PyMuPDF page renders). **It examined 34 of 203 paper pages (16.7%).**
- The model was asked to request more pages when needed; **it requested none on all eight papers.** Its `stop_reason` was free-form prose instead of the requested stop token, so the loop stopped because the model returned no page requests. This is a strategy/contract failure, not a successful bounded iteration.
- Measured recovery: **0.309 mean load-bearing-page recall; 0.212 mean claim recall** at the primary lexical match threshold (content-word Jaccard ≥ 0.20). D (the full-document reference) is the operational comparison target, not independent truth.
- Concrete misses (against the operational reference, lexical flags — not human adjudication): on one paper it missed all four reference claims, including the 33/505 confirmed reward-hack cases and the 40.5% cumulative evasion result; on another, three claims including the reported 98% best-of-three evasion-attempt rate and 88% success rate; on another, three of five claims including the late-commit/unknown-in-flight limit on exactly-once guarantees.
- The benchmark's post-hoc tolerance (stated as not preregistered): at most 0.5/4 loss in faithfulness and evidence support, at least 0.90 evidence-page and claim recall, at least 0.95 normalized schema/page-reference validity. **No selective pipeline met it. The full-document reference → GPT-6 Luna cell was the only measured cell that met its own reference quality and structural gates.**
- That winning reference cell cost **$0.112304 for eight papers** ($0.079122 extraction + $0.033183 generation), with canonical schema passing 8/8 and citation quote containment 0.776.
- **The entire evaluation cost approximately $0.538550 estimated** (300 saved attempts across all layers — triage, page strategies, generation arms, blind judging, post-checks; 6.7% of its $8 cap). Costs are rate-card estimates from recorded usage, not invoices.
- Frame this as a **bounded rejection of the tested selective-reading strategy**, not proof that selective reading can never work. The failure artifact's own conclusion: a future contract would need explicit page requests, preserved stop-token semantics, and recall measured against a larger, independently adjudicated evidence set.
- Sample: 24 purposively sampled papers (12 high-value proxies / 8 adjacent / 4 negative controls; balanced by construction, not random); the eight-paper deep subset was preselected as long/figure/table-heavy (six papers of 20+ pages). Labels are proxies, not a gold relevance set.

### Experiment 2 — cheap extractor → stronger synthesizer (the "DQ84" evaluation)

Source anchors: `dq84-luna-vs-gemini/report.md`, `dq84-luna-vs-gemini/findings.md`, `dq84-luna-vs-gemini/comparison-table.md`, `dq84-luna-vs-gemini/metrics/aggregate.json`.

Arms (identical Luna system prompt and output schema; only the source differs):

```
Arm A: full extracted paper text → GPT-6 Luna (one call per paper)
Arm B: full extracted paper text → Gemini Flash-Lite evidence packet → GPT-6 Luna
```

The packet contained exactly four fields (`candidate_claims`, `key_claims`, `limitations`, `load_bearing_pages`), serialized with sorted keys, compact separators, UTF-8; `requested_pages` and `stop_reason` were omitted. Both stages ran serially per paper.

| Metric | Full text → Luna (A) | Gemini packet → Luna (B) |
|---|---:|---:|
| mean load-bearing-page recall | 0.509 | 0.273 |
| cited-quote containment | 0.804 | 0.654 |
| unsupported/weak claims | 13.3% (6/45) | 43.2% (19/44) |
| estimated cost per paper | $0.003639 | $0.010907 |
| median latency per paper | 15.4 s | 39.8 s |
| blind-judge means (n=7) | faithfulness 4.00 / evidence support 4.00 / depth 4.00 | 3.286 / 2.714 / 2.714 |
| schema (native, normalized) | 8/8, 8/8 | 8/8, 7/8 |

**The most interesting mechanism — the packet found material; the handoff lost it.** Pooled across 25 paper-specific reference-claim instances at the primary lexical threshold: the Gemini packet matched **24**; the final B artifact matched **17**; **7 packet-matched claims were lost at the Luna synthesis stage**, and the packet's misses were recovered by final Luna **0** times. A page-level version: the packet's own evidence-reference recall was 0.231 while the final artifact reached 0.273 — the loss shows up sharply in claims, not uniformly in pages. One worked example: a claim the packet matched at 0.414 Jaccard came back at 0.035 in the final artifact ("B synthesis/handoff loss: Gemini packet matched it; Luna final did not"). The handoff — a serialization of four fields through one more model — is where information died.

**Do not overclaim.** The report's own verdict is mixed, and the note must say so:

- The two-stage arm's lexical claim-overlap advantage (0.652 vs 0.440) is **confounded**: the operational reference was itself produced by the same model family as the B extraction stage. It is not independent truth.
- All claim/page/quote metrics are lexical (content-word Jaccard, quote containment), not semantic entailment.
- The blind judge was a single small judge (n=7 usable cells), ceiling-heavy for Arm A (all normalized A ratings were 4/4, limiting discrimination), with imperfect response-format compliance; no second judge produced usable scores.
- n=8, purposive subset; costs are estimates; latency is serial wall per paper.
- `reasoning_effort=none` bounds the result to that setting; a small medium-effort sensitivity arm (4 papers) showed **no measured quality gain**.
- **The winning arm is not perfect:** one-pass Luna still missed substantial reference evidence (page recall 0.509). The conclusion is "best among those tested", not "optimal".
- The report's post-hoc improvement rule (B must show ≥ +0.5/4 judge gain or ≥ +10pp recall, positive direction in ≥6/8 pairs) was applied after observing the run and is a pragmatic threshold for a small sample, not a validated universal rule.

### Where the probabilistic evaluator actually fit (JEV)

Source anchors: `report/report.md` (Layer 1, Layer 4, "Recommended role-based routing and thresholds").

- For **triage/routing**, JEV at a provisional P(relevant) ≥ 0.70 threshold measured **proxy precision 0.857 and recall 1.000 on the purposive sample** (12/12 high-value proxies detected), at roughly **$0.000047 per call** — the cheapest measured escalation threshold. The benchmark's own guidance: use 0.50–0.69 as a review band; do not auto-discard below it on n=24.
- For **truth adjudication after generation**, it did not hold up: at P(supported) ≥ 0.75, **19 of 43 predicted-supported candidates failed exact quote containment**; raising the threshold to 0.95 lifted proxy precision to 0.80 but dropped recall to 0.154. There was no balanced automatic acceptance threshold in this sample.
- The principle to derive: **probabilistic evaluators can prioritize attention; deterministic systems should enforce invariants. Evidence acceptance needs stronger verification than a typed probability.**
- This section connects naturally to the earlier rmax.ai note on typed probabilistic decisions (see cross-links): the benchmark is what operationalizing that architecture looks like when the object being judged is evidence.

## 4. Suggested structure (9 sections; adapt titles, keep the arc)

1. **The PDF wall** — the starting problem: paper discovery signals existed, but durable, evidence-grounded research memory required reading, extracting evidence, synthesizing, keeping provenance. The efficiency questions: can we avoid reading the whole document? Can a cheap model compress it first? Can a probabilistic evaluator cheaply decide what deserves deeper processing?
2. **The architecture that looked sensible** — the staged intuition (signal → cheap routing → selective/cheap reading → evidence packet → stronger synthesis → verification → durable insight) and why progressive compression looks economically attractive. Then the question: what information does each compression boundary destroy?
3. **Hypothesis 1 — "we don't need to read the whole PDF"** — the selective-page experiment; lead with evidence-retrieval metrics, not token savings; the contract failure (no page requests, prose stop reasons); one or two concrete missed-evidence cases; bounded conclusion.
4. **Hypothesis 2 — "let a cheap model extract the evidence"** — the A/B experiment; the table; the handoff mechanism and its numbers; derive: **intermediate representations are lossy interfaces** — a model-to-model handoff is not free abstraction; it adds serialization assumptions, omissions, reinterpretation, latency, cost, and another failure surface.
5. **The simpler architecture** — the measured default that replaced the staged maze: relevance triage (advisory) → exact-version full-document acquisition → deterministic extraction with stable evidence IDs → GPT-6 Luna at reasoning off with strict structured output → deterministic evidence-reference validation → immutable record. "Best architecture among those tested", not universal optimality.
6. **Where JEV actually fit** — routing vs truth adjudication, with the numbers; the principle above.
7. **Don't let the LLM write the citation** — the evidence-ID design: the extractor creates version-pinned evidence blocks; the model selects their IDs; deterministic code resolves page, section, quote, offsets, hashes; dangling IDs and model-authored coordinates are hard failures. This is the concrete mechanism behind "deterministic evidence verification".
8. **What this says about agent architecture** — generalize: context compression has a measurable quality cost; model/agent handoffs are information bottlenecks; every extra stage must earn its place empirically; optimize for evidence preservation, not token minimization; simpler pipelines can be cheaper precisely because they eliminate serial stages and failure surfaces.
9. **What remains unsolved** — one-pass Luna still misses evidence; current evidence metrics are largely lexical; routing labels are purposive proxies, not naturally-prevalent human gold; the judge sample is small; the next benchmark should use an independent human-adjudicated evidence set; reasoning-effort sensitivity and larger routing calibration remain open. End with the stronger systems lesson: **the lesson is not that full context always wins — it is that every optimization that removes context must demonstrate that it preserves the evidence the downstream decision needs.**

## 5. Diagrams (exactly three; use these exact sources)

Embed byte-identically: ` ```mermaid ` fenced blocks in `index.md`; `<pre class="mermaid">` blocks in `index.html` (flush-left at column 0, content indented four spaces in HTML). Never `<br/>`, `<`, or a raw `&` inside a diagram block. Include the `pre.mermaid` CSS rule and the page-level Mermaid runtime module with the dark themeVariables exactly as in the most recent published note's HTML.

**Diagram 1 — hypotheses and falsification** (place in section 2 or 3):

```
flowchart TD
    subgraph rejected["Rejected hypotheses"]
        H1["Hypothesis 1 - skip the full PDF"] --> S1["Selective page reading - 34 of 203 pages"]
        S1 --> M1["Missed load-bearing evidence - page recall 0.309"]
        M1 --> X1["Rejected"]
        H2["Hypothesis 2 - cheap extractor before the strong model"] --> S2["Gemini packet to Luna synthesis"]
        S2 --> M2["Handoff loss - 7 of 24 matched claims lost"]
        M2 --> X2["Rejected"]
    end
    subgraph kept["Measured path"]
        K1["Full text to one model - Luna, reasoning off"] --> K2["Deterministic evidence verification"]
        K2 --> K3["Only tested cell inside the post-hoc gates"]
    end
    X2 ~~~ K1
    classDef neutral fill:#1f2937,stroke:#6b7280,color:#e6eef8
    classDef bad fill:#7f1d1d,stroke:#ef4444,color:#e6eef8
    classDef good fill:#14532d,stroke:#22c55e,color:#e6eef8
    class H1,S1,H2,S2 neutral
    class M1,X1,M2,X2 bad
    class K1,K2,K3 good
```

**Diagram 2 — the lossy handoff** (place in section 4):

```
flowchart TD
    P["Full paper text"] --> G["Gemini packet stage - matched 24 of 25 reference claims"]
    G --> B["Packet boundary - loss point - 7 matched claims lost"]
    B --> L["Luna synthesis - final artifact matched 17 of 25"]
    L --> O["Downstream insight"]
    classDef neutral fill:#1f2937,stroke:#6b7280,color:#e6eef8
    classDef loss fill:#7f1d1d,stroke:#ef4444,color:#e6eef8
    class P,G,L,O neutral
    class B loss
```

**Diagram 3 — final evidence architecture** (place in section 5 or 7):

```
flowchart TD
    S["Paper signals"] --> T["Cheap relevance triage - advisory"]
    T --> A["Exact-version full-document acquisition"]
    A --> E["Deterministic extraction + stable evidence IDs"]
    E --> M["Luna - reasoning off - strict structured output"]
    M --> V["Deterministic evidence-reference validation"]
    V --> I["Immutable PaperInsight"]
    classDef neutral fill:#1f2937,stroke:#6b7280,color:#e6eef8
    classDef gate fill:#3b1f6e,stroke:#7c3aed,color:#e6eef8
    class S,T,A,E,M,I neutral
    class V gate
```

No additional diagrams. If a diagram only restates the comparison table, remove it and say why in the change summary — but the three above all add information (falsification flow, loss point, final architecture) and are structurally distinct from the tables.

## 6. Cross-links (natural placement only — do not force)

- `https://rmax.ai/notes/jev-vs-generative-models-for-typed-software-decisions/` — in section 6: the earlier argument about typed probabilistic decisions vs generative judgment; this benchmark is what happens when you operationalize it.
- `https://rmax.ai/notes/deep-research-evidence-workflow/` — in sections 5/7: deep research as an evidence workflow; deterministic citation resolution.
- `https://rmax.ai/notes/the-change-is-the-unit-of-assurance/` — in section 7: assurance should attach to verifyable evidence, not prose.
- `https://rmax.ai/notes/the-harness-is-becoming-the-runtime/` — in section 8: pipeline architecture as runtime design.
- `https://rmax.ai/notes/from-human-orchestrated-agent-to-autonomous-control-plane/` — in sections 8/9: continuity with the field report on running agent pipelines.

Public source links that MUST appear: the benchmark repository `https://github.com/rmax-ai/ai-papers-routing-benchmark`, the DQ79 report `https://github.com/rmax-ai/ai-papers-routing-benchmark/blob/main/report/report.md`, the failure walkthrough `https://github.com/rmax-ai/ai-papers-routing-benchmark/blob/main/artifacts/failures/selective-reading.md`, and the DQ84 subtree `https://github.com/rmax-ai/ai-papers-routing-benchmark/tree/main/dq84-luna-vs-gemini`. Link them at first substantive mention.

## 7. Public boundary (hard rules)

- The note cites only public destinations (rmax.ai pages, the public benchmark repo and its files, arXiv links already represented in the benchmark).
- No private repository names, no internal issue/record numbers, no chat links or contents, no local filesystem paths, no credentials, no prompts or traces, no operator-identifying material.
- Model/provider names appear only in their measured roles (GPT-6 Luna, Gemini Flash-Lite, JEV), never as recommendations or rankings.
- No tracking parameters in any link.

## 8. House requirements

- End sections in order: **Practical Takeaways** (3–6 bullets), **Positioning Note**, **Status & Scope** (state: engineering field report; bounded experiments; lexical-proxy caveats), **References** (linked list with URLs).
- Frontmatter per `notes/schema.yaml` — exact fields, slug equals directory; `date`/`updated`: `2026-09-27`; `author: Max`; `section: notes`; canonical URL `https://rmax.ai/notes/read-the-whole-paper-ai-research-pipelines/`; `reading_time` calibrated to the final prose count at ~206 words/min, formatted `N–M min read`.
- Tables: keep the two comparison tables (Experiment 2 headline; optionally the cost/latency one) concise; the prose around them carries interpretation, not duplication.
- No "Editorial Notes" artifacts; no TODOs; no placeholder text.
- Do a final compression pass after tables/diagrams are in place: remove prose that merely restates them.

## 9. Avoid (failure-mode list)

- Universal claims from n=8 or n=24; "proves", "never", "always".
- Claiming semantic correctness from lexical containment.
- Treating post-hoc thresholds as production guarantees.
- "X is smarter/better" outside the measured role; provider marketing language.
- Implying the two-stage arm found nothing (the packet often found material — that is the point).
- Implying one-pass Luna is perfect (it still missed substantial reference evidence).
- Losing the caveats: purposive samples, lexical metrics, single small judge, estimated costs, serial latency, reasoning-effort scope, and the Gemini-family reference confound.
