---
title: "Where Should Query Planning Live in Agentic Search?"
author: "Max"
date: 2026-10-25
status: "draft"
tags:
  - ai
  - agents
  - search
  - mcp
  - retrieval
  - tool-design
  - evaluation
---

# Where Should Query Planning Live in Agentic Search?

Modern agents increasingly search systems that were designed for humans or conventional software: issue trackers, email, documents, code, messages, observability data, financial systems, and internal knowledge bases. The obvious engineering question is how to expose those systems as tools. A less obvious one is where the interpretation of the user's intent should happen.

Should the agent translate a request into structured fields? Should it generate a provider-specific query language? Should the connector accept natural language and perform query planning itself? Or should the two cooperate, with natural language carrying fuzzy intent while typed fields enforce hard constraints?

These interfaces can look superficially equivalent:

```text
search(status="open", project="runtime", created_after="2026-09-01")

search("status:open project:runtime after:2026-09-01 worker leases")

search("Find unresolved worker failures caused by expired leases since September")

search(
  query="worker failures caused by leases expiring unexpectedly",
  filters={status: ["open"], project: ["runtime"], created_after: "2026-09-01"}
)
```

They are not equivalent. Each one assigns a different amount of reasoning to the agent, the connector, and the retrieval backend.

This article investigates that boundary. It combines a survey of real connector and search-interface designs with a controlled benchmark that holds the search backend constant while varying the interface exposed to the agent.

> **Research status:** This is a working draft. Sections marked **[RESEARCH PLACEHOLDER]** will be grounded in commissioned research on intent/query-planning systems. Sections marked **[BENCHMARK PLACEHOLDER]** will be replaced with results from `rmax-ai/search-interface-bench` after the protocol is frozen and the holdout experiment is complete.

## The hidden architecture inside `search(query: string)`

A field named `query` tells us almost nothing about the semantics of a search interface.

It may mean:

- a provider-specific query language;
- a lexical keyword string;
- a semantic retrieval query;
- a full natural-language description of user intent;
- a reranking signal applied after lexical candidate generation;
- or one component of a hybrid search request that also carries structured constraints.

This distinction matters because the agent must know what kind of language the connector expects. A natural-language sentence passed into a provider DSL is usually a poor query. A tightly compiled keyword query passed into a semantic search system may throw away context the retriever could have used.

The tool schema alone cannot express this difference. Two tools may both expose:

```json
{"query": "string"}
```

while implementing entirely different contracts.

**[RESEARCH PLACEHOLDER — connector taxonomy]**

Insert evidence from the commissioned research here. Ground the taxonomy in concrete systems and primary documentation. At minimum, compare:

- provider-native query languages;
- free-text lexical search;
- semantic natural-language search;
- natural-language query planners that compile to structured retrieval;
- hybrid natural-language + hard-filter interfaces;
- lexical + filters + semantic-reranking decomposition;
- `search` + `fetch` two-stage contracts.

For each example, identify where query planning actually happens and what guarantees the connector provides.

The important point is that `query: string` is not an architecture. It is only a surface.

## Query planning is a systems boundary

Consider a user asking:

> Find unresolved worker failures related to leases expiring since September in the runtime project.

That request contains several different kinds of information:

- `worker failures` is topical;
- `leases expiring` is semantic and causal;
- `unresolved` maps to a status predicate;
- `since September` is a temporal predicate that must be normalized;
- `runtime project` is a scope/filter constraint.

Someone has to transform this request into an executable retrieval plan.

The conventional agent-centric architecture puts most of that work in the model:

```text
User intent
   ↓
Agent interprets request
   ↓
Agent learns tool schema / provider syntax
   ↓
Agent compiles query
   ↓
Connector executes query
   ↓
Search backend
```

This architecture is attractive because the connector can remain thin and deterministic. It also pushes a surprising amount of provider-specific knowledge into the agent.

For every system it searches, the model may need to understand:

- the available fields;
- field value vocabularies;
- date syntax;
- boolean semantics;
- query operators;
- pagination;
- ranking behavior;
- unsupported combinations;
- and when broadening a query is appropriate.

At small scale that is manageable. Across dozens or hundreds of tools, it becomes part of the model's context and planning burden.

The alternative is to move some of the compilation step behind the connector boundary:

```text
User intent
   ↓
Agent forwards semantic request
   ↓
Connector interprets intent
   ↓
Connector builds executable search plan
   ↓
Search backend
```

The agent-facing tool becomes simpler, but the connector becomes more intelligent—and potentially less transparent.

This is not a simplification in the absolute sense. It is a relocation of complexity.

## Three places query planning can live

There are three broad architectures worth separating.

### 1. Agent-side planning

The agent receives a structured schema or documented query language and compiles the user's request itself.

```text
natural language
    ↓
agent
    ↓
structured query / DSL
    ↓
connector
```

This maximizes transparency and minimizes hidden connector behavior. Hard constraints can be explicit and auditable.

The cost is cognitive and token overhead. The agent must repeatedly translate user language into provider-specific representations, and mistakes in query compilation become agent failures.

### 2. Connector-side planning

The tool accepts natural-language intent and converts it into an internal query plan.

```text
natural language
    ↓
connector planner
    ↓
structured / lexical / semantic retrieval plan
```

This reduces the agent-facing schema and lets a connector encapsulate domain-specific retrieval knowledge.

But it introduces a second reasoning system. If the planner silently drops `unresolved`, misinterprets `since September`, or adds an unjustified project constraint, the agent may receive plausible but wrong results without knowing why.

### 3. Cooperative planning

The agent supplies fuzzy semantic intent and machine-verifiable constraints separately.

```json
{
  "query": "worker failures caused by leases expiring unexpectedly",
  "filters": {
    "status": ["open"],
    "project": ["runtime"],
    "created_after": "2026-09-01"
  }
}
```

The connector owns semantic retrieval while the agent retains responsibility for constraints that should be explicit.

This creates a useful division:

```text
soft relevance      → natural language
hard correctness    → typed predicates
```

It is intuitively attractive. It is also an empirical claim. A more complex hybrid schema could impose enough additional planning cost that a simpler natural-language interface performs better in practice.

## Natural language is not a substitute for determinism

Natural-language interfaces are most useful where relevance itself is fuzzy.

Examples include:

- "incidents that look like cascading retries";
- "design discussions where people were worried about ownership";
- "runbooks relevant to a partial regional outage";
- "issues describing symptoms similar to this customer report".

These requests are difficult to reduce to enumerated filters without losing meaning.

But other constraints are not fuzzy:

- status must be open;
- document must belong to a particular tenant;
- timestamp must be after a cutoff;
- amount must exceed a threshold;
- result type must be an incident, not a document;
- access scope must match the caller's authorization.

Treating these as semantic hints is dangerous.

A useful working hypothesis is therefore:

> Use natural language where relevance is graded; use structured predicates where correctness is binary.

Whether this heuristic survives controlled measurement is one of the questions in the benchmark below.

## The search plan as an intermediate representation

A useful way to reason about agentic search is to borrow from compilers.

```text
User intent               ≈ source language
Canonical SearchPlan      ≈ intermediate representation
Provider/backend query    ≈ target code
```

The analogy is not perfect, but it exposes an important design opportunity: make query planning observable by introducing a canonical intermediate representation.

For example:

```python
class SearchPlan(BaseModel):
    lexical_query: str | None
    semantic_query: str | None
    filters: SearchFilters
    sort: list[SortSpec]
    limit: int
```

Every interface can eventually compile into this representation:

```text
Structured tool ───────┐
Provider DSL ──────────┤
Natural language ──────┼──→ SearchPlan ──→ SearchService
Hybrid query+filters ──┤
Decomposed interface ──┘
```

This boundary is valuable for two reasons.

First, different external tool contracts can share one backend implementation.

Second, failures can be localized. If the generated `SearchPlan` is wrong, the error belongs to intent interpretation or query planning. If the plan is correct but retrieval misses the gold evidence, the error belongs to retrieval. If retrieval is correct but the final answer is wrong, the error belongs downstream.

Most end-to-end agent evaluations collapse these failure modes into one score.

## What existing systems appear to be doing

**[RESEARCH PLACEHOLDER — prior art and mechanisms]**

Use the commissioned research to map real implementations onto the three planning architectures above.

Questions to answer with sources:

1. Which systems explicitly accept natural-language intent rather than keywords?
2. Which systems use an LLM or semantic parser internally to construct a search plan?
3. Which systems separate filters from semantic intent?
4. Which use lexical candidate generation followed by semantic reranking?
5. Which expose provider DSLs directly to the agent?
6. What observability exists for the generated plan?
7. How are authorization and hard filters enforced?
8. Are there published evaluations of query-planning accuracy, not just retrieval quality?

**[RESEARCH PLACEHOLDER — theoretical/academic grounding]**

Add relevant work from semantic parsing, text-to-SQL, information retrieval, query reformulation, learned sparse/dense retrieval, reranking, agent tool design, and intent-based interfaces. Keep the focus on mechanisms that inform where query planning should live.

## Why comparing products is not enough

Suppose we compare two systems:

```text
System A:
structured filters → Elasticsearch

System B:
natural language → embeddings + reranker
```

If System B retrieves better results, we cannot conclude that natural-language interfaces are better.

We changed several variables at once:

- the agent-facing schema;
- the query planner;
- the lexical representation;
- the retriever;
- the ranking policy;
- possibly the underlying index.

The experiment we actually want is narrower:

> If the user intent, agent, dataset, and search backend are held constant, how does the tool contract—and therefore the location of query planning—change outcomes?

That is the purpose of `rmax-ai/search-interface-bench`.

## A controlled benchmark of search tool contracts

The benchmark uses the following architecture:

```text
Synthetic user intent
        ↓
Fixed agent harness + fixed model
        ↓
Condition-specific MCP search tool
        ↓
Connector adapter / optional query planner
        ↓
Canonical SearchPlan
        ↓
ONE shared SearchService
        ↓
ONE frozen synthetic corpus/index
```

The invariant is important: every primary condition ultimately queries the same `SearchService` over the same frozen index snapshot.

The variable under test is the interface and the location of query planning—not the retriever.

### A0 — Fully structured search

The agent must compile the request into typed fields.

```json
{
  "text": "worker lease failures",
  "status": ["open"],
  "project": ["runtime"],
  "created_after": "2026-09-01",
  "limit": 10
}
```

This maximizes explicitness. It also makes query compilation entirely the agent's responsibility.

### A1 — Provider-style query DSL

The connector exposes one string, but the string is a deterministic search language:

```text
worker lease failures status:open after:2026-09-01 project:runtime
```

This models interfaces similar to email, issue-tracker, and search-provider query syntaxes.

### A2 — Pure natural-language intent

The agent receives only:

```text
search(query: string)
```

For example:

```text
Find unresolved worker failures caused by lease expiry since September in the runtime project.
```

A connector-side planner compiles this into the canonical `SearchPlan`.

### A3 — Natural language plus typed filters

Semantic intent and hard constraints are separated:

```json
{
  "query": "worker failures caused by leases expiring unexpectedly",
  "filters": {
    "status": ["open"],
    "project": ["runtime"],
    "created_after": "2026-09-01"
  }
}
```

This is the strongest candidate for a general-purpose interface, but the benchmark treats that as a hypothesis rather than a conclusion.

### A4 — Explicit lexical, filter, and semantic decomposition

A more detailed interface asks the agent to separate three concerns:

```json
{
  "keywords": ["worker", "lease"],
  "filters": {
    "status": ["open"],
    "created_after": "2026-09-01"
  },
  "natural_language_query": "failures caused by leases expiring unexpectedly"
}
```

This gives the retrieval layer more explicit signals, but also increases schema and planning complexity.

## A synthetic corpus with known ground truth

Real enterprise data is attractive because it is realistic. It is also difficult to evaluate cleanly because relevance is often subjective and hidden constraints are poorly labeled.

The benchmark therefore starts with a deterministic synthetic enterprise-like corpus containing thousands of records across several entity types:

- issues and tickets;
- runbooks and documents;
- messages and threads;
- change records.

Each record has realistic structured metadata—project, status, team, owner, labels, severity, timestamps, numeric fields—as well as generated text with known latent topics and relations.

More importantly, the corpus contains deliberate distractors:

- the right keywords in the wrong project;
- the right topic with the wrong status;
- semantically equivalent text with little lexical overlap;
- stale versions of otherwise relevant documents;
- near duplicates;
- negated or conflicting concepts;
- temporal distractors;
- cases requiring two or more related records.

This makes failure measurable.

Consider the query:

> Find unresolved checkout failures after the August rollout.

A synthetic task can contain:

```text
INC-142  checkout timeout after rollout     OPEN     September   ← relevant
INC-102  checkout timeout after rollout     CLOSED   September   ← status distractor
DOC-33   checkout rollout guide             —        August      ← type distractor
INC-189  checkout timeout                   OPEN     July        ← temporal distractor
INC-201  inventory timeout after rollout    OPEN     September   ← semantic distractor
```

The benchmark knows exactly why each record should or should not match.

## Task classes matter more than a single leaderboard

There is unlikely to be one universally best search interface.

The benchmark therefore evaluates separate task strata:

1. lexical exact matches;
2. structured-filter-dominant requests;
3. semantic paraphrases with low lexical overlap;
4. semantic intent combined with hard constraints;
5. negation and exclusion;
6. relative and temporal language;
7. ambiguous intent requiring broadening or reformulation;
8. multi-hop retrieval;
9. high-distractor environments;
10. exact identifier or title lookup.

The useful outcome is not simply "A3 scored highest." It is a decision surface describing which interface works under which conditions.

## Measuring the whole translation pipeline

The benchmark separates four evaluation layers.

### 1. Query-planning correctness

Did the system translate the user's intent correctly?

Metrics include:

- hard-filter exactness;
- dropped constraints;
- hallucinated constraints;
- temporal normalization correctness;
- constraint violations.

The canonical `SearchPlan` makes these errors directly inspectable.

### 2. Retrieval quality

Given the produced plan, did the backend retrieve the correct evidence?

Metrics include:

- Hit@K;
- Recall@K;
- MRR;
- nDCG@K;
- distractor rate;
- time and tool calls to the first relevant record.

### 3. End-to-end task success

Did the agent actually solve the user's task?

For lookup tasks, the evaluator checks whether the required record IDs were selected. For answer tasks, it checks whether the required facts were recovered and supported by the retrieved records.

### 4. Efficiency

Abstractions are only useful if their cost is visible.

The benchmark therefore records:

- tool-schema tokens;
- agent input/output tokens;
- search reformulations;
- tool calls;
- connector-side planner tokens and cost;
- latency;
- total cost per successful task.

The results should be reported as trade-off frontiers rather than collapsed into one opaque score.

## Failure attribution is the main methodological payoff

A wrong final answer can come from several different systems:

```text
User intent
    ↓
[1] Agent query-compilation failure
    ↓
[2] Connector query-planning failure
    ↓
[3] Search/ranking failure
    ↓
[4] Agent answer-synthesis failure
```

Without an intermediate representation and trace, these failures are easy to confuse.

For example:

- If the user asks for `open` incidents and the agent emits `closed`, that is an agent compilation error.
- If the agent sends the full intent correctly but the connector planner omits the status predicate, that is a connector-planning error.
- If the plan contains the correct status and semantic query but relevant records rank below distractors, that is a retrieval error.
- If the correct evidence is returned and the agent still answers incorrectly, that is an answer-synthesis error.

This attribution matters operationally. Each failure requires a different fix.

## Hypotheses before seeing the results

The benchmark is designed to test, not assume, the following expectations.

### Hypothesis 1: structured interfaces win when hard constraints dominate

Exact identifiers, status filters, numeric ranges, tenant boundaries, and date predicates should favor structured interfaces because the cost of dropping a constraint is high.

### Hypothesis 2: natural-language interfaces help semantic discovery

When the user describes behavior without using the vocabulary present in the corpus, connector-side semantic planning may reduce agent work and increase retrieval recall.

### Hypothesis 3: hybrid interfaces work best for mixed queries

Requests containing both fuzzy meaning and strict predicates may benefit from assigning each to the representation that fits it best.

### Hypothesis 4: decomposition can become over-specification

The most expressive interface may not be the easiest one for an agent to use. Explicitly separating keywords, semantic intent, and filters may increase tool-schema cost and create new opportunities for inconsistency.

### What would falsify these expectations?

Several outcomes would be informative:

- If pure natural language matches structured search on constraint-heavy tasks, typed filters may add less value than expected.
- If structured tools match natural language on semantic tasks, modern agents may already be competent query planners.
- If the decomposed interface does not beat the simpler hybrid contract, exposing retrieval mechanics is unnecessary complexity.
- If connector-side planning improves retrieval but total cost or latency becomes substantially worse, the abstraction may be economically unattractive.

Negative results are first-class results.

## Results

**[BENCHMARK PLACEHOLDER — experimental protocol]**

Fill in after protocol freeze:

- repository/commit;
- corpus seed and manifest digest;
- model and reasoning configuration;
- connector-planner model/configuration;
- SearchService/index configuration;
- number of development and holdout tasks;
- repetitions;
- budget controls;
- statistical treatment.

**[BENCHMARK PLACEHOLDER — overall results]**

Add the main outcome table here.

Suggested columns:

| Interface | Task success | Constraint error rate | Recall@10 | Agent tokens | Planner tokens | Tool calls | Latency | Cost/success |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Structured | TBD | TBD | TBD | TBD | — | TBD | TBD | TBD |
| DSL | TBD | TBD | TBD | TBD | — | TBD | TBD | TBD |
| Natural language | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Hybrid | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Decomposed | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

**[BENCHMARK PLACEHOLDER — results by task class]**

Do not report only aggregate averages. Add per-stratum plots/tables for:

- exact lookup;
- filter-heavy tasks;
- semantic paraphrases;
- mixed semantic + hard constraints;
- temporal language;
- high-distractor tasks;
- multi-hop tasks.

**[BENCHMARK PLACEHOLDER — failure attribution]**

Report how often failures came from:

- agent query compilation;
- connector query planner;
- backend retrieval/ranking;
- final synthesis.

**[BENCHMARK PLACEHOLDER — Pareto analysis]**

Plot or summarize:

- task success vs total tokens;
- task success vs latency;
- task success vs total cost;
- constraint error rate vs schema complexity;
- retrieval quality vs number of reformulations.

## Decision heuristics

**[BENCHMARK PLACEHOLDER — replace this provisional matrix with evidence]**

A plausible pre-result decision matrix is:

| Search problem | Candidate interface |
| --- | --- |
| exact identifier/title lookup | structured or DSL |
| many mandatory metadata predicates | structured |
| fuzzy semantic discovery | natural language |
| semantic intent + mandatory predicates | hybrid |
| explicit lexical + semantic retrieval control | decomposed, if measured benefit justifies complexity |

The benchmark should determine whether this matrix survives contact with data.

## Implications for MCP and agent tool design

If the hybrid model performs well, a useful default search contract may be surprisingly small:

```typescript
type SearchRequest = {
  query: string;
  filters?: SearchFilters;
  scope?: SearchScope;
  limit?: number;
};
```

followed by a separate authoritative fetch step:

```typescript
fetch(id: string): Document
```

This creates a three-stage tool architecture:

```text
search / discover   → semantic-friendly
fetch / inspect     → stable identifier
execute / mutate    → strongly typed
```

The separation matters because the acceptable ambiguity changes by stage.

Search is inherently approximate. Fetch should be exact. Mutations should generally be more strongly typed and governed than either.

A natural-language mutation such as:

```text
restart whatever workers seem unhealthy
```

creates a much more dangerous ambiguity than:

```text
find workers that appear unhealthy
```

Natural language can therefore be valuable at the discovery boundary without becoming the universal interface for an agent system.

## Tool schemas describe syntax; descriptions must describe semantics

One practical lesson follows regardless of which benchmark arm wins.

A JSON schema can tell an agent that a tool accepts a string. It cannot tell the agent whether that string should contain:

- keywords;
- a query DSL;
- a complete question;
- a semantic description of an ideal result;
- or text used only for reranking.

That contract belongs in the tool semantics and documentation.

For agent-facing systems, tool descriptions are not cosmetic API docs. They are part of the execution protocol.

**[RESEARCH PLACEHOLDER — tool-description evidence]**

Ground this claim in primary documentation and any research on tool-description effects, function calling, MCP tool semantics, and agent interface design.

## What this does not mean

Several conclusions would be too broad even if natural-language or hybrid interfaces perform well.

### Natural language does not eliminate schemas

The schema may move behind the connector into the canonical search plan, but some representation of filters, ranking, scope, and result types still exists.

### Semantic search is not the same as natural-language query planning

A connector can accept natural language and still compile it into lexical or structured search. Conversely, a vector retriever can be exposed through a rigid structured API.

### Smaller tool surfaces do not imply simpler systems

A one-field interface can hide a planner, embedding model, filter extractor, reranker, and query-rewriting loop. Complexity has moved, not disappeared.

### Structured search is not automatically more reliable

A structured schema only helps if the agent fills it correctly. The benchmark explicitly measures failures caused by agent-side query compilation.

### Connector-side reasoning is not merely an implementation detail

Moving reasoning across the tool boundary changes observability, cost, failure attribution, portability, and who owns the semantics of the request.

## The broader architectural question

The argument extends beyond search.

Agent systems increasingly sit between humans expressing intent and deterministic systems requiring executable representations. Search makes this boundary easy to study because the outputs are ranked and measurable, but the same pattern appears in:

- analytics;
- workflow configuration;
- infrastructure operations;
- database access;
- policy evaluation;
- planning systems;
- enterprise automation.

The recurring design question is:

> Which parts of intent should remain flexible, which should be compiled into explicit intermediate representations, and which must become deterministic before execution?

Search gives us a controlled environment in which to answer that question empirically.

## Conclusion

The important distinction is not natural language versus structured APIs.

It is where interpretation happens.

```text
User intent
    ↓
Agent reasoning
    ↓
Connector reasoning
    ↓
Deterministic execution
```

Every agent system draws boundaries between those layers, whether intentionally or accidentally.

A good search interface should make that division explicit enough to evaluate. The connector should not silently turn fuzzy intent into correctness-critical constraints. The agent should not be forced to learn unnecessary provider syntax when the connector can own it more effectively. And retrieval should remain independently measurable from both.

The goal of `search-interface-bench` is to replace architectural taste with evidence: hold the model and backend constant, vary the contract, inspect the intermediate search plan, and measure which allocation of reasoning works for which class of request.

**[FINAL PLACEHOLDER — update after research + benchmark]**

Replace the final paragraph with the strongest evidence-supported conclusion. Avoid claiming one universal interface unless the holdout results actually justify it. The likely useful output is a set of decision heuristics describing when query planning belongs in the agent, in the connector, or in a cooperative boundary between them.

## References

**[RESEARCH PLACEHOLDER — commissioned research references]**

Add primary documentation, papers, and relevant production-system writeups here.

**[BENCHMARK PLACEHOLDER — project artifacts]**

- `rmax-ai/search-interface-bench`
- benchmark protocol/design commit: TBD
- corpus/task manifest: TBD
- holdout report: TBD
- raw run artifacts: TBD
