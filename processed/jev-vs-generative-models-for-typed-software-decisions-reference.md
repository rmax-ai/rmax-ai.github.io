# Jev vs. Generative Models for Typed Software Decisions

A small provider-direct experiment comparing TypeSafe AI’s Jev, GPT-5.6 Luna, and DeepSeek Flash measures a specific architectural tradeoff: when software needs a bounded decision, should it invoke a general-purpose language model or a model designed specifically for typed probabilistic evaluation?

The updated experiment changes the answer from the first prototype.

Jev is not the cheapest option in the latest run. **DeepSeek Flash is.**

Jev is, however, substantially faster than both generative models while exposing a different interface: typed choices, scores, booleans, and probabilities instead of generated JSON.

The interesting result is therefore not that one model “wins.”

It is that **latency, cost, uncertainty representation, and decision quality occupy different trade-off surfaces depending on the inference primitive.**

## Why compare these systems?

Most AI applications currently use language models for almost everything.

Need to classify a request? Generate JSON.

Need to decide whether an agent should retry? Generate JSON.

Need to score risk? Generate JSON.

Need to choose a queue? Generate JSON.

This works, especially now that general-purpose models support reliable structured outputs. GPT-5.6 Luna, for example, supports structured outputs and can run with reasoning explicitly disabled. ([OpenAI](https://developers.openai.com/api/docs/models/gpt-5.6-luna))

But these operations are not inherently generation tasks.

TypeSafe AI’s Jev exposes a different abstraction. State goes in; typed `Choice`, `Score`, and `Boolean` answers come out, including probabilities. Vercel describes Jev as a probabilistic decision model for software whose declared questions are evaluated in parallel rather than produced through ordinary autoregressive text generation. ([Vercel](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway))

That distinction suggests a systems question:

**When is generation the right inference primitive, and when is a typed evaluator better?**

The [`rmax-ai/ai-provider-triage-comparison`](https://github.com/rmax-ai/ai-provider-triage-comparison) experiment is an initial probe of that question.

## A cleaner comparison

The new experiment improves substantially on the earlier `ai-gateway-example`.

It compares three reasoning-off configurations:

| Arm | Provider path | Model | Reasoning |
|---|---|---|---|
| OpenAI Luna | OpenAI API directly | `gpt-5.6-luna` | explicitly `none` |
| DeepSeek Flash | DeepSeek API directly | `deepseek-flash` | explicitly disabled |
| Jev | Vercel AI Gateway evaluation API | `typesafe-ai/jev` | not applicable |

The earlier prototype used `deepseek-v4-flash`. DeepSeek's [September 10, 2026 release notes](https://api-docs.deepseek.com/updates/) state that V4.1 Flash is now served under `deepseek-flash`; the previous V4 Flash generation is retired and its old identifier is temporarily routed to V4.1 only for compatibility.

The new experiment therefore tests the current first-party DeepSeek Flash path directly rather than relying on the obsolete identifier through an intermediary.

## The task

The benchmark contains five multi-message support threads.

Each system returns five bounded decisions:

- department: billing, tech, or sales
- urgent: boolean
- severity: integer from 0 to 4
- requires escalation: boolean
- estimated effort: categorical duration

That produces 15 calls: five tickets × three inference paths.

The two generative models receive the same canonical thread text and objective rubric. Both have reasoning disabled.

Luna uses strict JSON-schema structured output.

DeepSeek Flash uses JSON-object structured output.

Jev receives equivalent questions through its typed evaluation protocol.

The repository also runs capability probes before measurement to verify model IDs, reasoning-off behavior, structured-output support, usage accounting, and Jev reachability.

There are no retries.

This is still a very small experiment, but it removes several confounders from the first version.

## The measured result

The [committed run](https://github.com/rmax-ai/ai-provider-triage-comparison/blob/main/reports/comparison.md) from September 20, 2026 produced:

| Configuration | Five-call latency | Computed cost |
|---|---:|---:|
| Jev | **1,738 ms** | $0.000438 |
| DeepSeek Flash | 4,565 ms | **$0.000377** |
| GPT-5.6 Luna | 5,859 ms | $0.000737 |

Two different winners appear.

### Latency: Jev

Jev completed the five calls in 1.74 seconds: approximately **3.4× faster than Luna** and **2.6× faster than DeepSeek Flash** in this run.

It also consumed far more reported input tokens—10,425 versus roughly 2,100–2,500 for the chat models—yet still completed substantially faster.

That observation is directionally consistent with TypeSafe's description of Jev as a model optimized for typed probabilistic decisions rather than general-purpose language generation. ([TypeSafe AI](https://typesafe.ai/blog/introducing-system-one-models-and-jev))

TypeSafe reports much larger gains on its own workflow evaluations—up to 193.6× faster and 444.6× cheaper—but explicitly says these figures are toward the high end of what it expects in real workloads and acknowledges possible workflow-construction bias. Those figures are vendor evidence, not independent benchmark results.

### Cost: DeepSeek Flash

DeepSeek Flash was cheapest in the committed run:

- DeepSeek Flash: **$0.000377**
- Jev: **$0.000438**
- Luna: **$0.000737**

Jev was roughly 41% cheaper than Luna but about 16% more expensive than DeepSeek Flash.

That corrects the earlier prototype. A specialized evaluator does not automatically dominate cheap generative models on price.

The more defensible conclusion is narrower:

**Jev occupied a distinct latency regime in this run, while cost depended strongly on the competing model and provider pricing.**

## Decision agreement is only partial

The more important limitation is quality.

There is no labeled ground-truth dataset. The experiment measures agreement among systems, not correctness.

Across five tickets and five fields, all three systems produced identical complete decisions on only **2 of 5 tickets**.

Pairwise field agreement was:

| Field | Agreements |
|---|---:|
| urgency | 15 / 15 |
| department | 13 / 15 |
| escalation | 13 / 15 |
| estimated effort | 13 / 15 |
| severity | 11 / 15 |

This identifies where apparently simple classifications become ambiguous.

### Case 1: one ticket, two legitimate departments

The first thread combines an incorrect renewal charge with users being locked out of their workspace.

Luna and DeepSeek route it to `billing`.

Jev routes it to `tech`.

All three agree that the ticket is urgent, severity 4, requires escalation, and likely takes one to four hours.

Without an explicit routing policy for multi-issue tickets, neither department choice is obviously incorrect.

The disagreement exposes something deeper than model quality:

**the task specification itself contains unresolved policy.**

A production benchmark must define whether routing means root cause, most urgent issue, first-response owner, primary customer request, or eventual resolution owner.

Otherwise policy ambiguity is misread as model error.

### Case 2: severity boundaries

On the production-webhook outage, DeepSeek and Jev assign severity `4`; Luna assigns `3`.

Everything else agrees.

Again, the important question is not which output feels more reasonable. A labeled benchmark needs an explicit rubric defining the boundary between high and critical severity.

### Case 3: escalation is policy, not just semantics

The fifth case is an enterprise pre-sales request involving pricing, SAML, SCIM, a DPA, subprocessors, data residency, audit-log retention, and possible custom deployment.

All three systems agree that it belongs to sales and is not urgent.

They disagree on the rest:

- Luna: severity 0, no escalation, 1–4 hours
- DeepSeek: severity 1, escalate, 1–2 days
- Jev: severity 0, escalate, 1–4 hours

Jev returns 0.61 probability for escalation.

At a threshold of `0.5`, Jev says escalate. At `0.7`, it would not.

That is one of the strongest architectural properties of a probabilistic decision API: **threshold policy remains under application control.**

Vercel explicitly describes Jev as returning typed answers plus probabilities, making it possible to automate clear cases and route uncertain ones to review. ([Vercel](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway))

A production application might implement:

`p(escalate) ≥ 0.9` → escalate automatically

`0.4 ≤ p(escalate) < 0.9` → second evaluator or human review

`p(escalate) < 0.4` → continue automatically

The model provides uncertainty. The workflow defines acceptable risk.

## Calibration matters more than confidence-looking numbers

Probabilities are only useful when they are calibrated.

A model that repeatedly emits `0.8` should ideally be correct around 80% of the time on comparable examples. Calibration therefore needs to be measured separately from classification accuracy. Guo et al.'s [study of neural-network calibration](https://proceedings.mlr.press/v70/guo17a.html) is a useful foundation for this distinction.

A serious Jev evaluation should therefore measure:

- Brier score
- log loss
- expected calibration error
- reliability curves
- precision and recall at policy thresholds
- autonomous-action rate
- human-review rate
- failure cost at each threshold

That would turn probability outputs into operational evidence rather than attractive metadata.

## Why Jev can still matter if DeepSeek is cheaper

The updated experiment makes one point especially clear: **cost alone is not enough to select the inference primitive**.

DeepSeek Flash currently wins raw computed cost.

Jev wins observed latency.

But Jev also exposes a different programming contract.

A generative path conceptually looks like:

`state → prompt → generated structured output → parse → validate → decision`

A typed evaluator looks more like:

`state × typed questions → probabilities / choices / scores`

Both produce structured data, but they expose different semantics.

For an application designer, that difference affects uncertainty handling, threshold control, schema failure modes, batching of related judgments, observability, calibration, retries, and escalation policy.

The point is not that Jev replaces inexpensive LLMs.

It is that an agent runtime may benefit from supporting both.

## From model routing to inference routing

Most work on inference economics asks:

**Which model should handle this request?**

[FrugalGPT](https://arxiv.org/abs/2305.05176) showed that model cascades can reduce inference cost while preserving useful performance. [RouteLLM](https://arxiv.org/abs/2406.18665) formalized routing as a learned choice between stronger and weaker models under quality-cost trade-offs.

The next abstraction may be broader:

**What kind of computation should handle this step?**

Possible primitives include:

- deterministic code
- database queries
- search and retrieval
- typed probabilistic evaluation
- lightweight structured generation
- deep reasoning
- open-ended generation
- human review

That produces an inference graph rather than a single-model agent.

For example:

1. DeepSeek Flash extracts structured information cheaply.
2. Jev evaluates a high-frequency policy decision with low latency.
3. Deterministic code validates hard constraints.
4. Luna handles an ambiguous case requiring broader reasoning.
5. A human reviews decisions above a defined risk threshold.

The routing decision is no longer merely `Luna or DeepSeek?`

It becomes:

`code, retrieval, evaluator, cheap model, reasoning model, or human?`

## The provider path matters

The new experiment also corrects a methodological weakness in the original comparison.

OpenAI and DeepSeek now run directly against their first-party APIs. Only Jev uses Vercel AI Gateway because the experiment accesses Jev through its evaluation-model path.

Latency should therefore still not be interpreted as a perfectly controlled provider benchmark.

Network paths differ. Provider infrastructure differs. Jev passes through Vercel. Calls are sequential. A single run captures transient load.

The repository correctly describes wall-clock latency as an observed measurement, not a controlled benchmark.

A stronger experiment should repeat each condition with randomized execution order and report p50, p95, and p99 latency, variance, and timeout rate.

## Model aliases are experimental variables

The DeepSeek correction also demonstrates an easily overlooked benchmarking problem: **rolling model aliases move**.

DeepSeek now documents `deepseek-flash` as the current Flash alias for V4.1 Flash, while the previous V4 Flash identifiers are only temporarily redirected for compatibility. ([DeepSeek](https://api-docs.deepseek.com/updates/))

An experiment that records only “DeepSeek Flash” without preserving model ID, provider path, timestamp, capability probe, and pricing provenance can become difficult to interpret weeks later.

The new repository commits those artifacts.

For applied AI research, they are not implementation details. They are part of experimental reproducibility.

## What this experiment establishes

For five support-ticket threads with reasoning disabled on both general-purpose models:

1. **Jev had the lowest observed wall-clock latency.**
2. **DeepSeek Flash had the lowest computed cost.**
3. **Luna was more expensive and slower than the other two in this particular run.**
4. **The systems disagreed enough that no quality ranking is justified without labeled ground truth.**
5. **Urgency was stable across all pairwise comparisons; severity was the least stable field.**
6. **Jev's probability outputs make threshold policy explicit, which is architecturally useful even when its thresholded decision disagrees with another model.**

The experiment does not establish that Jev is more accurate.

It does not establish that DeepSeek is more accurate.

It does not establish a universal latency ordering.

It does not establish that these cost ratios generalize to other tasks.

It does show that typed evaluation deserves to be evaluated as a separate inference primitive rather than merely as another model behind a prompt.

## The next experiment

The natural next step is not another model. It is **ground truth and repeated measurement**.

A credible benchmark should contain 100–500 independently labeled support threads with explicit routing policies, adjudicated severity labels, escalation rules, effort labels, intentionally ambiguous cases, multi-issue threads, repeated calls per model, and randomized execution order.

The analysis should report:

- accuracy and macro-F1
- confusion matrices
- Brier score and log loss for probabilistic outputs
- calibration curves
- p50/p95/p99 latency
- cost per correct decision
- cost per autonomous decision
- human escalation rate
- failure rate at each confidence threshold

Then introduce a hybrid policy:

`Jev confidence high` → act immediately

`Jev confidence intermediate` → ask DeepSeek Flash

`models disagree` → ask Luna or a human

That experiment would answer a much more useful question:

**Which inference architecture achieves the required assurance level at the lowest total cost and latency?**

## The architectural conclusion

General-purpose models have become cheap enough that using them everywhere is often reasonable. DeepSeek Flash makes that especially clear.

But cheap generation and specialized evaluation are still different primitives.

The updated experiment suggests a more nuanced design principle:

**Use deterministic software when the rule is known. Use typed evaluators when the output is bounded and calibrated uncertainty is operationally useful. Use cheap generative models when flexible structured interpretation is needed. Use deeper reasoning only when the task actually requires it.**

The future agent runtime is unlikely to be built around one universal model.

It is more likely to look like an operating system for heterogeneous inference: dispatching each cognitive operation to the cheapest and fastest primitive that satisfies its quality and assurance requirements.

That is the research direction this small experiment makes worth pursuing.

## References

1. rMax.ai, [`ai-provider-triage-comparison`](https://github.com/rmax-ai/ai-provider-triage-comparison), provider-direct reasoning-off support-ticket experiment, September 20, 2026.
2. Vercel, [“TypeSafe AI's Jev now available on AI Gateway”](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway), September 16, 2026.
3. TypeSafe AI, [“Introducing System One Models & Jev”](https://typesafe.ai/blog/introducing-system-one-models-and-jev), September 15, 2026.
4. Vercel AI Gateway, [“Jev — API, Pricing & Playground”](https://vercel.com/ai-gateway/models/jev).
5. OpenAI, [“GPT-5.6 Luna Model”](https://developers.openai.com/api/docs/models/gpt-5.6-luna).
6. DeepSeek, [Change Log: DeepSeek-V4.1-Flash Release](https://api-docs.deepseek.com/updates/), September 10, 2026.
7. DeepSeek, [“DeepSeek-V4.1-Flash: Smarter, Faster, More Efficient”](https://api-docs.deepseek.com/news/news260910/).
8. Guo et al., [“On Calibration of Modern Neural Networks”](https://proceedings.mlr.press/v70/guo17a.html), ICML 2017.
9. Chen, Zaharia & Zou, [“FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance”](https://arxiv.org/abs/2305.05176).
10. Ong et al., [“RouteLLM: Learning to Route LLMs with Preference Data”](https://arxiv.org/abs/2406.18665).
