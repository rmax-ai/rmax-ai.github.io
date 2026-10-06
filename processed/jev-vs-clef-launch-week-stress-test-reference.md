# Inbox source — "Jev vs Clef: What a Launch-Week Stress Test Found"

Target slug: `jev-vs-clef-launch-week-stress-test`
Target path: `notes/jev-vs-clef-launch-week-stress-test/index.md`
Publication date: 2026-10-06 (revision 2 — rerun consumed; see below)

This file is the complete raw material for the writer: the editorial brief, the independently re-verified evidence map (every quantitative figure below was re-derived from the public benchmark repository and re-probed at primary sources on **2026-10-03** — use exactly these figures and caveats), the exact Mermaid diagram sources, the cross-link list, and the hard publication-boundary rules. Follow it. Where this brief and the repository's binding contract (`docs/contracts/publish-technical-note.md`) conflict on process, the contract wins.

**Revision 2 (2026-10-06):** this brief was updated to consume the post-launch full rerun (`results/run-20261004-rerun/`, executed 2026-10-06; the launch run is preserved unchanged). §2 gains Amendment 3; the §3 rows and Appendix A figures below are updated where the rerun supersedes them. Where this revision and earlier text disagree, **this revision governs**. The article presents two dated measurements (launch · rerun).

## 1. Editorial brief

- **Audience:** engineers and platform / agent-infrastructure people. Assume fluency with LLM APIs, latency, serialization, and CI-style evaluation; do not explain basics.
- **Register:** systems field report — concrete before abstract, evidence-labeled, calm. No hype, no futurism, no provider leaderboard, no marketing voice. The article is about a workload contract, not about which vendor wins.
- **Thesis (hold this):** *A decision-model swap is safe only after validating the workload contract: semantics, serialization, latency, determinism, and wire compatibility — not just benchmark accuracy.*
- **Keep measured API latency distinct from vendor-published model-benchmark latency everywhere** — different measurement paths, never merged into one comparison.
- **Length:** ~2,000–2,800 prose words (an 11–13 minute technical read). Tables carry measured detail; diagrams carry the spatial ideas; prose carries the argument and never merely restates tables/diagrams.
- **Publication-spec obligations (verbatim constraints — do not weaken):**
  1. Use "author-labeled" / "author-expected" for the n=24 accuracy subset; describe it as 24 question-level decisions (several decisions per case, never "24 cases"); **never** call it ground truth.
  2. Do not say the benchmark proves Clef is queue-bound. Say the observed pattern is *consistent with* queueing / scale-from-zero / serving-path overhead; the root cause was not isolated.
  3. Do not compare Cloudflare's published 209.3 ms / 38.8 ms model-benchmark figures directly to the measured 18–19 s API wall clock as if they measured the same path.
  4. Qualify "fully API-compatible": the tested hosted paths required a `noul`↔`boolean` mapping.
  5. Do not turn the 6/6 injection checks into a security claim.
  6. Do not generalize Clef repeatability from three repeats to global determinism.
  7. Do not use the 96% / 92% / 79% small-sample result to declare an overall model winner.

## 2. Verification record (completed 2026-10-03, before drafting; source of truth = the public benchmark repo)

All benchmark figures below were **independently re-derived from the raw call log** (`rmax-ai/jev-vs-clef` @ `4097859`, `results/run-20261003-main/{report.md,calls.jsonl,summary.json}`) — not transcribed from any summary. External claims were re-probed live at their primary sources the same day. The following outputs of this pass matter for drafting:

- **Verified-kept (no change to the reference draft's wording):** the `noul`↔`boolean` caveat; small-n labeling; bounded injection and repeatability framing; the measured-vs-vendor latency separation; the AI-assistance disclosure. The concurrency ratio stays **1.03×** — the value supported by the committed report and the raw probe latencies (sequential median ~18.8 s vs four-way-parallel median ~19.3 s); use 1.03× wherever the ratio appears.
- **Amendment 1 (apply exactly) — latency persistence:** the latency section's sentence *"A re-smoke later that day still produced 18–19 second responses, and the final API-only battery reproduced the result."* is replaced (already reflected in the Appendix A text below) with: *"The same 18–19 second band held across every phase of both runs — smoke, probe, and the full battery."* Reason: the earlier re-smoke's artifacts are not part of the public repository; the replacement preserves the "not a blip" point using only committed evidence.
- **Amendment 2 (apply exactly) — accuracy-subset semantics (verification update, 2026-10-04):** the n=24 subset is **24 author-expected question-level decisions** across the labeled clear-cut cases (several decisions per case) — never describe it as "24 cases". Wording pairs (already reflected in the Appendix A text below): *"On the 24 author-labeled cases, Clef 27B matched 23, Jev 22, and Clef-flash 19:"* → *"Across 24 author-expected question-level decisions, Clef 27B matched 23, Jev 22, and Clef-flash 19:"*; table row *"Labeled-case accuracy, n=24"* → *"Author-expected decision accuracy (n=24)"*; *"Twenty-four author-labeled examples"* → *"Twenty-four author-expected question-level decisions"*; *"the labeled cases used author expectations"* → *"the labeled subset used author expectations"*.
- **Amendment 3 (apply exactly) — post-launch rerun consumption (2026-10-06):** the full battery was re-run (`results/run-20261004-rerun/`, executed 2026-10-06; launch run preserved unchanged). Headline deltas: hosted latency did **not** normalize — clef/flash p50 18.6 s / 18.5 s (launch 18.7 s / 18.6 s); sequential-vs-parallel 1.01× (launch 1.03×); the 2026-10-04 lightweight probe's sub-second medians (~0.70 s / ~0.48 s) did **not** reproduce (matched-shape probe at rerun time: medians ~18.7 s / ~18.7 s). Accuracy: clef 23/24 in both runs; jev 22 → 20; clef-flash 19 in both (n=24 author-expected question-level decisions; run-to-run movement at this size is expected and should be framed as such). Agreement vs jev: 90% → 88% (clef), 85% → 83% (clef-flash). Everything else (format sensitivity, determinism, injection holds, vision, batching, wire seam) is unchanged across runs. Present latency as two dated measurements and never imply normalization.

## 3. Evidence map (quantitative anchors — use exactly these figures with these caveats)

| Claim area | Exact verified figure / wording | Source | Caveat that must travel with it |
|---|---|---|---|
| Battery scope | 159 calls per run; two dated full runs (launch 2026-10-03; rerun 2026-10-06); main ok 147/149 each; smoke → probe → battery phases under a spend guard | both runs' calls.jsonl, report.md | single synthetic battery; one environment; two measurement windows |
| Launch vs rerun delta | every headline metric recomputed from both raw call logs with one independent implementation | `results/run-20261004-rerun/delta-vs-20261003.md` | reproduces both generated reports |
| p50 latency | launch: 0.3 / 18.7 / 18.6 s · rerun: 0.3 / 18.6 / 18.5 s (Jev / Clef / Clef-flash) | both report.md latency tables | one test environment; wall clock, not SLA; the ~18–19 s band persisted across both runs |
| Concurrency probe | launch: 18.8 s vs 19.3 s (1.03×) · rerun: 18.6 s vs 18.8 s (1.01×) | both reports' concurrency probes | identical payload; single probe per run |
| Author-expected decision accuracy | launch 92% / 96% / 79% (Jev 22/24, Clef 23/24, Clef-flash 19/24) · rerun 83% / 96% / 79% (Jev 20/24) | both report.md accuracy tables | author-expected decisions, not cases; not ground truth; n=24; run-to-run movement visible |
| Agreement vs Jev | launch: 90% (43/48) / 85% (41/48) · rerun: 88% (42/48) / 83% (40/48) (Clef / Clef-flash) | both reports' agreement tables | question-match metric; agreement ≠ accuracy |
| Cost | avg/call $0.000021 / $0.000111–0.000113 / $0.000038–0.000039; spend $0.0097 (launch) + $0.0099 (rerun) computed; $0.017 each conservative | both `summary.json` + cost tables | provider-usage derived; conservative estimate is an upper bound |
| Format sensitivity (B1) | Clef urgent probability 0.90 (prose) / 0.86 (flat JSON) / 0.09–0.10 (nested JSON), consistent across both runs | both runs' calls.jsonl (B1p/f/n) | yes/no questions only; choice/score outputs stable in the runs |
| Destructive probe (B2) | at least one arm crossed the 0.5 boundary on a format change (Clef 0.93 → 0.31 flat → 0.58) | `calls.jsonl` (B2*) | representation belongs in the behavioral contract |
| Determinism | Clef repeats byte-identical across 3 repeats; Jev small numeric variants, labels stable | `report.md` determinism table | three repeats only; a bounded observation |
| Injection probes | 6/6 held (C06 urgency, C07 routing; all three arms) | `report.md` injection table | regression signal only; not a security result |
| Vision | 3/3 on the synthetic shapes image, both Clef sizes; images as base64 data URIs; raw base64 → HTTP 422; image tokens included in `usage.input_tokens` | `report.md` G5/G4; `SPEC.md` | interface verification, not a quality claim |
| Wire gap | Clef accepts `noul`; the Jev gateway path expects `boolean`; Clef rejected `boolean` (HTTP 400, G7); the README documents that each side rejects the other's spelling | `calls.jsonl` G7; `README.md`; `SPEC.md` | one-field adapter in the tested path: "endpoint + model + schema field", not "model name only" |
| Scale | needle retention at ~13 KB states | `report.md` scale table | group D synthetic states |
| 64 questions / dotted ids / array state | accepted; 64 answers returned | `report.md` edge cases | interface checks |
| Vendor latency figures | Cloudflare launch post: median latency 209.3 ms / 38.8 ms | `blog.cloudflare.com/clef-decision-models/` | vendor benchmark numbers; not an end-to-end SLA |
| Pricing (input) | $0.042/M (Jev) · $0.24/M (Clef) · $0.09/M (Clef-flash) | `SPEC.md`; Cloudflare model docs | input-token pricing as used by the run |
| Capabilities | Clef: 64K context (65,536 tokens), multimodal state (text/JSON/images/video), 1–64 questions, vision, Apache-2.0 weights | Cloudflare model docs; Hugging Face model cards | documentation-level facts, re-verified 2026-10-03 |

**External-source verification (all re-probed live 2026-10-03):** Cloudflare launch post (209.3/38.8 table; "fully Jev-API compatible"; "strictly typed outputs similar to Jev"; "more powerful precision model … latency-critical decisions"; Apache-2.0; dated October 1, 2026); Cloudflare Workers AI model docs for `clef` and `clef-flash` (context 65,536; vision; "images … Clef extension to the System One API"; 1–64 questions; `noul`; $0.24 / $0.09 per M input tokens); Hugging Face model cards (`license:apache-2.0`, both); TypeSafe blog (System One + Jev framing; "unstructured state in, typed probabilistic decisions out"); Vercel AI Gateway model page + changelog ("evaluation model" terminology; classification / routing / rubric-based assessment / automated verification).

**Source-of-truth rule:** every number must be traceable to `rmax-ai/jev-vs-clef` (`report.md` / `calls.jsonl` / `summary.json`) or to one of the named primary sources above. Never invent, round differently, or extrapolate. If a number is missing, omit it rather than estimating.

## 4. Diagrams (exactly three; use these exact sources)

Embed byte-identically: ` ```mermaid ` fenced blocks in `index.md`; `<pre class="mermaid">` blocks in `index.html` (opening tag flush-left at column 0, content indented four spaces, mirroring the most recent published note). Never `<br/>`, `<`, or a raw `&` inside a diagram block. Include the `pre.mermaid` CSS rule and the page-level Mermaid runtime module (dark `themeVariables` + the `themeCSS` overflow fix) exactly as in the most recent published note's HTML.

**Placement:** D1 = end of the introduction (after the paragraph that ends "…would have changed system behavior."). D2 = in the latency section, after the paragraph presenting the p50-versus-p50 numbers. D3 = in the state-serialization section, after the paragraph that presents 0.90 / 0.86 / 0.09.

**Diagram 1 — the swap-validation surface:**

```
flowchart TD
    S["candidate decision-model swap"] --> C1["semantic contract: same questions, same output types"]
    S --> C2["wire contract: field-level compatibility"]
    S --> C3["state-format contract: serialization stability"]
    S --> C4["latency contract: deployment-environment call path"]
    S --> C5["determinism contract: repeats, replay, audit"]
    S --> C6["capability surface: vision, context, batching"]
    C1 --> G{"validated on the workload?"}
    C2 --> G
    C3 --> G
    C4 --> G
    C5 --> G
    C6 --> G
    G -->|"yes"| D["swap"]
    G -->|"no"| R["rework or keep the adapter"]
    classDef neutral fill:#1f2937,stroke:#6b7280,color:#e6eef8
    classDef blue fill:#1e3a5f,stroke:#3b82f6,color:#e6eef8
    classDef gate fill:#3b1f6e,stroke:#7c3aed,color:#e6eef8
    classDef good fill:#14532d,stroke:#22c55e,color:#e6eef8
    class S,R neutral
    class C1,C2,C3,C4,C5,C6 blue
    class G gate
    class D good
```

**Diagram 2 — the two measurement paths:**

```
flowchart TD
    subgraph vendor["Vendor benchmark - published numbers"]
        V1["model inference, measured on the vendor stack"] --> V2["median latency 209.3 ms / 38.8 ms"]
    end
    subgraph ours["Our measurement - committed run"]
        O1["client call from the test environment"] --> O2["hosted endpoint path: mechanism not isolated"] --> O3["18.7 / 18.6 s p50 launch - 18.6 / 18.5 s rerun"]
    end
    V2 --> M["two different measurement objects"]
    O3 --> M
    classDef neutral fill:#1f2937,stroke:#6b7280,color:#e6eef8
    classDef blue fill:#1e3a5f,stroke:#3b82f6,color:#e6eef8
    class V1,V2,O1,O2,O3 blue
    class M neutral
```

**Diagram 3 — the state-format crossing (B1 refund case):**

```
flowchart TD
    R["refund request - same semantic content"] --> P["prose encoding"]
    R --> F["flat JSON encoding"]
    R --> N["nested JSON encoding"]
    P --> PU["Clef urgent probability 0.90"]
    F --> FU["Clef urgent probability 0.86"]
    N --> NU["Clef urgent probability 0.09"]
    PU --> B{"0.5 decision boundary"}
    FU --> B
    NU --> B
    B -->|"above"| A["treated as urgent"]
    B -->|"below"| T["not urgent"]
    classDef neutral fill:#1f2937,stroke:#6b7280,color:#e6eef8
    classDef blue fill:#1e3a5f,stroke:#3b82f6,color:#e6eef8
    classDef gate fill:#3b1f6e,stroke:#7c3aed,color:#e6eef8
    class R,P,F,N blue
    class PU,FU,NU neutral
    class B gate
    class A,T neutral
```

Each diagram must be paralleled by prose: every node/edge's claim appears in the text with its evidence class, or carries its explicit conditional qualifier. No additional diagrams; no diagram that restates a table.

## 5. Cross-links and required sources

- The reference draft already links the sibling note `https://rmax.ai/notes/jev-vs-generative-models-for-typed-software-decisions/` inline — keep it. No other cross-links are required; do not force any.
- Every external claim links inline to its primary source at first substantive mention. Required URLs (References carries the full list):
  - https://github.com/rmax-ai/jev-vs-clef · https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261003-main/report.md · https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261003-main/calls.jsonl
  - https://blog.cloudflare.com/clef-decision-models/ · https://developers.cloudflare.com/workers-ai/models/clef/ · https://huggingface.co/Cloudflare/clef · https://huggingface.co/Cloudflare/clef-flash
  - https://typesafe.ai/blog/introducing-system-one-models-and-jev · https://api.typesafe.ai/docs · https://vercel.com/ai-gateway/models/jev
  - https://rmax.ai/notes/jev-vs-generative-models-for-typed-software-decisions/

## 6. House requirements

- **End sections in order:** Practical Takeaways (4–6 bullets), Positioning Note, Status & Scope, References (linked list).
- **Frontmatter** per `notes/schema.yaml` — exact fields, no extras; slug equals directory; `date`/`updated`: `2026-10-03`; `author: "rmax.ai AI assistants"`; `site: rmax.ai`; `section: notes`; `type: essay`; `status: published`; `canonical_url: https://rmax.ai/notes/jev-vs-clef-launch-week-stress-test/`; `license: CC BY 4.0`; `reading_time` calibrated from the final prose word count at ~206 words/min, rounded to a 2-minute band, formatted `N–M min read`.
- **Summary copy (byte-equal on every surface):** use exactly this description in the frontmatter, `<meta name="description">`, `og:description`, and all four index blurbs:
  `A 32-case launch-week stress test of Cloudflare's Clef models against TypeSafe's Jev measures accuracy, latency, state-format sensitivity, and wire compatibility — and shows when a decision-model swap is safe.`
- **HTML invariants:** canonical link; `<link rel="stylesheet" href="/styles/footer.css">`; standard `rmax-footer` markup; `window.footerThoughts` with exactly 3 article-specific thoughts (self-referential, under ~140 chars, tied to this article's subject); `<script src="/scripts/footer.js"></script>` after the thoughts block; page title/meta consistent with frontmatter.
- **Four index surfaces** (`index.md`, `index.html`, `notes/index.md`, `notes/index.html`) get the newest-first entry following the newest existing entries exactly (`notes/index.md` dual-entry; `notes/index.html` card carries its own date + reading-time meta).
- **CHANGELOG.md:** one entry at the top of `## [Unreleased]` → `### Added` — `- 2026-10-03: Published technical note: [jev-vs-clef-launch-week-stress-test](notes/jev-vs-clef-launch-week-stress-test/index.md). <one factual sentence>.\n  - *Warnings*: Failure-mode verdict: <verdict + one-line reason>. Link audit verdict: <verdict + one-line reason>.`
- **sitemap.xml:** regenerate via `python3 scripts/generate-sitemap.py` from the repo root; keep the generated shape.
- No "Editorial Notes" artifacts; no TODOs or placeholders. Final compression pass after tables/diagrams — remove prose that merely restates them; keep every caveat beside the claim it qualifies.

## 7. Public boundary (hard rules)

- The note (and this brief, which ships as the public `processed/` reference) cites only public destinations: rmax.ai pages and the public sources above. No private repository names, no internal issue numbers, no chat links or contents, no local filesystem paths, no credentials, no prompts/traces, no operator-identifying material.
- No tracking parameters in any link (`utm_`, `?ref=`, `fbclid`, etc.).
- Numbers appear exactly as given in this brief, with their caveats; do not introduce numbers from anywhere else.

## 8. Avoid (failure-mode list)

- Provider-leaderboard rhetoric; winner declarations; "proves", "always", "never".
- Timeless latency claims — date the measurement (launch week, single test environment) wherever latency appears.
- Presenting vendor figures as our measurements or vice versa; merging the 209.3 ms / 38.8 ms benchmark numbers with the 18–19 s API observations.
- Security claims from the injection probes; global determinism claims from three repeats.
- Dropping the small-n / author-expected caveats, the `noul`↔`boolean` caveat, or the AI-assistance disclosure.
- Extrapolating beyond the committed evidence ("we expect Clef to be slow everywhere" / "Clef is better than Jev").

## Appendix A — Reference draft (raw material; materially review, do not publish verbatim)

The draft below is the externally produced editorial draft. Its narrative structure, figures, and phrasing are the working baseline, with the §2 amendments (including the 2026-10-04 verification corrections) applied and all §1 obligations preserved. Compose the final note from it under this brief; do not copy it verbatim where this brief asks for adaptation.

## Jev vs Clef: What a Launch-Week Stress Test Found

Decision models occupy an unusual point in an agent stack. They do not generate plans or prose. They take application state plus typed questions and return bounded answers with probabilities that software can branch on directly.

TypeSafe introduced this interface with [System One models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev). Its API accepts a shared `state` and questions such as booleans, choices, or scores; the output is typed rather than free-form text. [Vercel exposes Jev as an evaluation model](https://vercel.com/ai-gateway/models/jev) for routing, classification, rubric scoring, and verification.

On October 1, Cloudflare released [Clef and Clef-flash](https://blog.cloudflare.com/clef-decision-models/), two open-weight decision models hosted on Workers AI. Cloudflare describes them as System One-compatible and positions the 27B Clef model for higher-precision decisions and the 9B Clef-flash model for latency-sensitive use. The [Workers AI documentation](https://developers.cloudflare.com/workers-ai/models/clef/) adds 64K context, multimodal state, up to 64 questions per request, and vision; the model weights are published under Apache-2.0 for [Clef](https://huggingface.co/Cloudflare/clef) and [Clef-flash](https://huggingface.co/Cloudflare/clef-flash).

We already use Jev-style decision models in workflow experiments, so the practical question was not whether Clef looked competitive on a vendor benchmark. It was whether we could substitute it in the kinds of gates we actually build.

We ran a small launch-week stress test on our own box, then re-ran the full battery three days later, keeping both dated runs side by side. The result was mixed in the useful way: the larger Clef model was strong on our author-expected decisions and added capabilities Jev did not have, but latency, state-format sensitivity, and one API incompatibility were large enough that a blind swap would have changed system behavior.

### The benchmark

The public [jev-vs-clef repository](https://github.com/rmax-ai/jev-vs-clef) contains the harness, specification, raw calls, and final report. The main run recorded **159 calls** across three arms:

| Arm | Hosted path | Input price used by the run | Relevant capability |
|---|---|---:|---|
| Jev | TypeSafe System One through Vercel AI Gateway | $0.042 / M tokens | text decision model |
| Clef 27B | Cloudflare Workers AI | $0.24 / M tokens | 64K context, vision |
| Clef-flash 9B | Cloudflare Workers AI | $0.09 / M tokens | 64K context, vision |

The battery used synthetic support-routing, guardrail, formatting, scale, repeatability, batching, and edge cases. Each arm received the same state and question content, except for one documented type-name translation: Cloudflare expects `noul` for yes/no questions while the Jev gateway path expects `boolean`.

Each run proceeded through smoke, probe, and battery phases under a spend guard. Every raw request, response, latency, provider-usage record, and cost is committed in the two call logs ([launch](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261003-main/calls.jsonl) · [rerun](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261004-rerun/calls.jsonl)). The derived numbers below come from the two reports ([launch](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261003-main/report.md) · [rerun](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261004-rerun/report.md)) and the [launch-versus-rerun delta](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261004-rerun/delta-vs-20261003.md).

### Accuracy was close; operational behavior was not

Across 24 author-expected question-level decisions, Clef 27B matched 23 in both runs, Jev 22 and then 20, and Clef-flash 19 in both:

| Metric | Jev | Clef 27B | Clef-flash |
|---|---:|---:|---:|
| Author-expected decision accuracy (n=24) — launch · rerun | 92% · 83% | 96% · 96% | 79% · 79% |
| Agreement with Jev, 48 questions — launch · rerun | — | 90% · 88% | 85% · 83% |
| p50 latency in our test environment — launch · rerun | 0.3 s · 0.3 s | 18.7 s · 18.6 s | 18.6 s · 18.5 s |
| Average cost per call from provider usage | $0.000021 | $0.000111 · $0.000113 | $0.000038 · $0.000039 |

This is too small a labeled set for a general quality ranking. The labels are our expected answers, not independent ground truth, and the disagreements concentrated on deliberately ambiguous cases: mixed-topic routing, borderline urgency, spam/security-disclosure handling, and feature-request classification. The labeled subset also moved between our two runs — Jev from 22 to 20 — a reminder about sample size, not a trend about models.

That concentration matters. A decision model usually sits at a branch point. The interesting failures are not only obvious wrong answers but cases near a policy boundary where two reasonable classifiers disagree. Those are also the cases where an escalation band or human review is useful.

The cost differences were real but small in absolute terms. Across the two 159-call batteries, computed spend was **$0.0097** and **$0.0099** from provider usage; the conservative estimates were **$0.017** each. For this workload, model cost was not the limiting resource.

Latency was.

### The hosted latency was the main surprise

Cloudflare's launch post reports median model-benchmark latencies of **209.3 ms for Clef** and **38.8 ms for Clef-flash**, and presents Clef-flash as appropriate for latency-critical decisions. Those are vendor benchmark numbers, not an end-to-end SLA.

Our API path during launch week behaved very differently: **18.7 s p50 for Clef and 18.6 s for Clef-flash**, versus **0.3 s for Jev** in the same harness. The full rerun three days later measured **18.6 s and 18.5 s** — the same 18–19 second band across every phase of both runs.

We checked whether simple client-side serialization was hiding the difference. It was not. Sequential and four-way-parallel Clef probes gave ~19 s medians in both runs (ratios of 1.03× and 1.01×). Even an intentionally invalid image request returned only after roughly the same delay — about 18.7 s — so the wait is not proportional to request work.

The measurements do **not** prove why the hosted path was slow; the observed pattern is consistent with serving-path overhead, but the harness did not isolate the mechanism. One anomaly is worth recording precisely: between the two runs, a lightweight probe on October 4 saw sub-second medians — about **0.70 s** for Clef and **0.48 s** for Clef-flash across ten calls each. We could not reproduce that window: the full rerun stayed at ~18.6 s, and a matched-shape probe of ten calls per model at rerun time measured medians of **~18.7 s / ~18.7 s**. We report both observations; the difference is unexplained in our data.

The deployment consequence is simpler than the causal diagnosis. In that environment, Clef was suitable for asynchronous gates, batch triage, and background analysis. It was not suitable for a synchronous hot path where a user or agent is waiting on every branch. Before putting it there, we would re-measure from the intended region and concurrency profile — and keep re-measuring: within one week, the same endpoints produced both a ~19-second and a ~0.7-second observation.

This is why model benchmarks and system benchmarks are different objects. A 39 ms model result can coexist with a 19 s API observation when they measure different paths — or with a sub-second one, when the serving path cooperates. The hosted path is part of the contract.

### State serialization is part of the model contract

The second surprise was format sensitivity.

We asked semantically equivalent questions over three encodings of the same state: prose, flat JSON, and nested JSON. Choice and score outputs were mostly stable. Some yes/no probabilities were not.

For the same refund-request case, Clef's urgent probability moved from **0.90 in prose** to **0.86 in flat JSON** and **0.09–0.10 in nested JSON** (consistent across both runs). On another destructive-action probe, at least one arm crossed the decision boundary when the representation changed.

Jev was not format-invariant either. The benchmark is therefore not evidence that one provider has a serialization problem and another does not. It is evidence that **representation belongs in the behavioral contract**.

This is easy to miss when state is assembled by upstream software. A refactor from prose to JSON can look like a harmless transport improvement while changing the model's decision surface. For deterministic code, equivalent data structures are usually expected to preserve behavior. For decision models, that equivalence has to be measured.

The rule we would use in production is straightforward: keep state formatting stable per pipeline, version it like an interface, and rerun the workload eval when the representation changes.

### Determinism also differs by provider

The repeat probes exposed another operational distinction.

For the tested requests, Clef and Clef-flash returned byte-identical answers across three repeats in both runs. Jev returned small numeric variants while preserving the final labels.

Neither behavior is inherently better. Exact repeatability is convenient for caching, regression debugging, and replay. Small probability movement can be acceptable when downstream code already uses bands, hysteresis, or review thresholds.

What matters is that the system knows which contract it has. A pipeline that treats a probability as a stable score for audit or deduplication needs a stricter repeatability test than a pipeline that only branches on a wide threshold.

### Vision is a real capability difference

Clef was the only tested family with vision support. Both Clef sizes correctly answered all three questions on a synthetic shapes image, in both runs.

The wire contract was specific: images worked as base64 data URIs, while raw base64 was rejected with HTTP 422. Image tokens were included in `usage.input_tokens`.

The public [Cloudflare model documentation](https://developers.cloudflare.com/workers-ai/models/clef/) describes image inputs as an extension to the System One API. That makes Clef interesting for gates that otherwise require a separate vision model before classification: document triage, screenshot inspection, UI-state checks, or image-based moderation. We did not benchmark those workloads here, so the result is capability verification, not a quality claim.

### “API-compatible” still needs an adapter

Cloudflare describes Clef as fully compatible with Jev and the System One API. At the semantic level, the match is close: state plus typed questions in, typed probabilistic decisions out.

At the wire level, our two hosted paths disagreed on the boolean question keyword. Cloudflare accepts `noul`; the Vercel/TypeSafe path used by the harness expects `boolean`. Each rejected the other's spelling in the tested API path.

That is a one-field adapter, not a deep incompatibility. But it changes the deployment claim from “change only the model name” to “change the endpoint/model and translate one schema field.”

This kind of seam is normal in infrastructure. It is also exactly why compatibility should be tested from the client boundary rather than inferred from conceptual similarity.

### The two injection probes held, but that is not a security result

The battery included two synthetic prompt-injection-style cases. One embedded text telling the model to ignore instructions and mark a ticket non-urgent; another embedded a fake `SYSTEM:` directive asking it to route to billing.

All three arms preserved the intended routing/urgency decision across those six checks.

That result is useful only at its actual scale: **6/6 on two synthetic probes**. It does not establish prompt-injection robustness. A real security evaluation would need adversarial generation, broader attack classes, repeated trials, and workload-specific harm definitions.

The point of keeping these cases in the battery is regression detection. If a provider or formatting change suddenly flips them, the pipeline gets a concrete warning.

### Decision models should be evaluated like dependencies

The benchmark changed how we think about decision-model substitution.

A normal model comparison asks which model scores higher. An infrastructure comparison asks a larger set of questions:

- Does it preserve the decisions that matter on our workload?
- What happens around ambiguous policy boundaries?
- What is the end-to-end latency from the deployment environment?
- Does parallel load change that latency?
- Does semantically equivalent state serialization change decisions?
- Are identical calls repeatable enough for replay and audit?
- Are the APIs actually wire-compatible?
- What capabilities, such as vision or longer context, change the architecture?
- What does the full path cost at realistic request volume?

That framing matches our earlier distinction between [typed probabilistic decisions and generative models](https://rmax.ai/notes/jev-vs-generative-models-for-typed-software-decisions/). A decision model is attractive precisely because it narrows the output contract. The surrounding system should be equally explicit about the input and operational contract.

For our current use, the measured guidance is workload-specific rather than a winner:

| Workload property | What this run suggests |
|---|---|
| Low-latency synchronous branch | Jev was the only tested hosted path meeting that requirement in our environment; re-measure Clef before use |
| Async triage / background gate | Clef 27B is plausible: strong small-sample accuracy, low absolute cost |
| Cost-sensitive async gate | Clef-flash was cheaper than Clef 27B but weaker on our labeled subset |
| Multimodal decision | Clef is the only tested option with vision |
| Replay-sensitive deterministic workflow | Clef repeats were byte-identical in our probes; validate over a larger sample |
| Existing Jev integration | The semantic API is close, but keep an explicit `boolean`↔`noul` adapter and compatibility tests |

These are not universal provider recommendations. They are the decisions supported by one synthetic battery, one test environment, and launch-week hosted behavior.

### What we would test next

The next run should focus less on adding cases and more on separating causes.

First, latency needs replication in more dimensions: multiple Workers AI regions if selectable, repeated windows across several days, cold/warm patterns, and concurrency ramps — plus a method that can explain why identical client calls ranged from sub-second to ~19 seconds within one week. Our temporal replication so far is a full rerun that agreed with the launch window, bracketed by a probe window that disagreed; the spread itself is the thing to chase.

Second, the format test should become a metamorphic evaluation. Generate multiple semantically equivalent encodings of the same state—field order, nesting, prose, normalized JSON—and measure label stability and probability drift automatically.

Third, the accuracy set needs independent labels and more naturally occurring borderline cases. Twenty-four author-expected question-level decisions are useful for regression but not enough for a quality ranking.

Fourth, repeatability should be measured over hundreds of identical calls, not three, and should distinguish exact bytes, label stability, probability drift, and decision-band crossings.

Finally, vision deserves its own workload. Passing a three-question shapes test shows the interface works. It says little about document or UI decisions under real ambiguity.

## Practical Takeaways

- Treat a decision-model migration as an interface and systems change, not a model-name change.
- Benchmark the hosted path from the actual deployment environment, and repeat the measurement over time; vendor model latency and end-to-end API latency answer different questions.
- Version state serialization and re-evaluate when its structure changes.
- Put compatibility shims in one explicit adapter and test them; do not spread provider-specific field names through application code.
- Use small synthetic batteries for regression and integration discovery, not for broad claims about model quality.
- Keep ambiguous decisions inside review bands. Agreement rates matter less than what happens at policy boundaries.

## Positioning Note

This is an engineering field report, not a general benchmark of Jev, Clef, or decision models. The measured battery was small and synthetic, the labeled subset used author expectations rather than independent adjudication, and latency came from one deployment environment across two dated measurement windows in Clef's first week. Vendor-published benchmark latency and our observed API latency use different measurement paths and should not be compared as if they were the same metric.

## Status & Scope

Measurements were collected on October 3 and October 6, 2026 and are reproducible from the public [benchmark repository](https://github.com/rmax-ai/jev-vs-clef): the [launch-window run](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261003-main/report.md), the [rerun](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261004-rerun/report.md), their committed raw call logs, and the [launch-versus-rerun delta](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261004-rerun/delta-vs-20261003.md). External capability and launch claims were checked against Cloudflare, TypeSafe, Vercel, and the released Hugging Face model cards. Research synthesis and this draft were prepared with AI assistance; the benchmark evidence is committed for independent inspection.

## References

- [Benchmark repository](https://github.com/rmax-ai/jev-vs-clef)
- [Launch-window run report](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261003-main/report.md)
- [Launch-window raw call log](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261003-main/calls.jsonl)
- [Rerun report](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261004-rerun/report.md)
- [Rerun raw call log](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261004-rerun/calls.jsonl)
- [Launch-versus-rerun delta table](https://github.com/rmax-ai/jev-vs-clef/blob/main/results/run-20261004-rerun/delta-vs-20261003.md)
- [Cloudflare: Introducing Clef](https://blog.cloudflare.com/clef-decision-models/)
- [Cloudflare Workers AI: Clef documentation](https://developers.cloudflare.com/workers-ai/models/clef/)
- [Cloudflare Clef model card](https://huggingface.co/Cloudflare/clef)
- [Cloudflare Clef-flash model card](https://huggingface.co/Cloudflare/clef-flash)
- [TypeSafe: Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [TypeSafe API documentation](https://api.typesafe.ai/docs)
- [Vercel AI Gateway: Jev](https://vercel.com/ai-gateway/models/jev)
- [rmax.ai: Jev vs Generative Models for Typed Software Decisions](https://rmax.ai/notes/jev-vs-generative-models-for-typed-software-decisions/)
