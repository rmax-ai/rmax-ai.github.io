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

Modern agents increasingly search systems that were designed for humans or conventional software: issue trackers, email, documents, code, messages, observability data, financial systems, and internal knowledge bases. The obvious engineering question is how to expose those systems as tools. A less obvious one is where interpretation of the user's intent should happen.

Should the agent translate a request into structured fields? Should it generate a provider-specific query language? Should the connector accept natural language and perform query planning itself? Should a dedicated retrieval planner sit between agents and storage? Or should the layers cooperate, with natural language carrying fuzzy intent while typed fields enforce hard constraints?

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

They are not equivalent. Each assigns a different amount of reasoning to the agent, the connector, a possible query planner, and the retrieval backend.

The emerging architectural pattern is best understood as a compilation pipeline:

```text
User intent
    ↓
Logical retrieval plan
    ↓
Optimization / backend selection
    ↓
Physical backend queries
    ↓
Retrieval + ranking
    ↓
Evidence
```

The central thesis of this article is therefore not "use semantic search" or "use hybrid RAG." It is:

> Treat agent retrieval as a compilation problem. Keep fuzzy semantic intent separate from deterministic predicates and security boundaries, materialize an inspectable logical plan, and compile that plan into backend-specific execution.

This article combines commissioned research on intent-aware query-planning systems with a controlled benchmark that holds the underlying information universe constant while varying the interface and allocation of planning responsibility.

> **Research status:** This is a working draft. Research findings below still require final citation cleanup against primary documentation. Sections marked **[BENCHMARK PLACEHOLDER]** will be replaced with results from `rmax-ai/search-interface-bench` after the protocol is frozen and the holdout experiment is complete.

## `query: string` is not an architecture

A field named `query` tells us almost nothing about the semantics of a search interface.

Across real systems it can represent at least these distinct operational modes:

1. **Provider-native query syntax** — SQL, Elasticsearch DSL, Lucene-like expressions, Google Drive predicates, GraphQL filters.
2. **Lexical free-text search** — terms interpreted by tokenizers and inverted indexes such as BM25.
3. **Semantic/vector retrieval** — text embedded and compared in a latent space.
4. **Natural-language query planning** — free-form intent parsed into a structured execution plan.
5. **Natural-language-to-structured-query compilation** — text compiled directly into SQL, GraphQL, Cypher, or another typed AST.
6. **Hybrid lexical + semantic retrieval** — multiple retrieval channels fused before or during ranking.
7. **Query decomposition / multi-hop planning** — one request becomes a DAG or iterative sequence of retrieval operations.
8. **Federated retrieval** — one intent is routed across heterogeneous systems with source-specific compilers.

The distinction matters because the agent must know what language the connector expects. A natural-language sentence passed into a provider DSL is not equivalent to a semantic query. A tightly compiled keyword query can discard context useful to a semantic retriever. A natural-language interface may hide an expensive planning system rather than eliminate schemas.

Two tools can therefore expose the same JSON schema:

```json
{"query": "string"}
```

while implementing completely different contracts.

The important point is simple:

> `query: string` is a surface type. It does not tell us who plans, what is deterministic, how constraints are enforced, or how retrieval is executed.

## The problem is separating soft intent from hard constraints

Consider a user asking:

> Find unresolved worker failures related to leases expiring since September in the runtime project.

That request contains several different kinds of information:

- `worker failures` is topical;
- `leases expiring` is semantic and possibly causal;
- `unresolved` maps to a categorical state predicate;
- `since September` is a temporal predicate that must be grounded to a concrete range;
- `runtime project` is a scope or entity constraint;
- the caller's actual permissions are an external security invariant.

Early retrieval architectures often collapse all of this into one text representation. That is convenient, but it conflates two different kinds of semantics:

```text
soft relevance      → graded, fuzzy, semantic
hard correctness    → binary, typed, enforceable
```

Vector similarity is appropriate for the first category. It cannot be allowed to override the second.

A request for "open security incidents from last week" should not return a resolved incident from three years ago merely because its prose is semantically similar. Conversely, forcing the primary agent to generate SQL, YQL, GraphQL filters, Lucene expressions, or provider-specific predicates for every backend pushes storage knowledge into the wrong architectural layer.

A useful default abstraction is therefore:

```text
SearchRequest = ⟨ semantic query, hard predicates, scope, limit ⟩
```

For example:

```json
{
  "query": "worker failures caused by leases expiring unexpectedly",
  "filters": {
    "status": ["open"],
    "created_after": "2026-09-01"
  },
  "scope": ["runtime"],
  "limit": 10
}
```

This is deliberately smaller than a database query language. It is an agent-facing contract, not a physical execution plan.

## The design space has three independent axes

An earlier version of this article described agent-side planning, connector-side planning, cooperative planning, and iterative retrieval as alternatives on one spectrum. That mixes different architectural questions.

The design space is cleaner when split into three orthogonal axes.

### Axis A — interface abstraction

What representation does the caller produce?

```text
provider-native DSL
        ↓
structured search fields
        ↓
NL query + typed constraints
        ↓
logical QueryPlan IR
```

Provider-native DSL gives maximum backend control and maximum coupling. A high-level query contract gives less direct control but allows backend evolution without changing the agent.

### Axis B — planning ownership

Which component interprets the user's information need?

```text
agent-owned
connector-owned
dedicated planner
cooperative
```

These are not merely implementation details. They determine context cost, observability, portability, failure ownership, and how many systems must understand backend schemas.

### Axis C — execution strategy

How is the resulting plan executed?

```text
single retrieval
hybrid sparse+dense retrieval
query decomposition
iterative / exploratory retrieval
```

This axis is independent from planning ownership. A cooperative interface can still use iterative retrieval. A dedicated planner can issue one query or build a multi-hop DAG. An agent-owned query can target a hybrid search engine.

This separation matters for benchmarking. Otherwise an experiment can accidentally attribute the value of iterative search to connector-side planning, or the value of hybrid ranking to natural-language interfaces.

## Planning ownership: four practical models

### Model A — agent-owned planning

The primary agent sees enough schema or query-language documentation to compile the request itself.

```text
User intent
   ↓
Agent
   ↓
SQL / GraphQL / provider DSL / structured filters
   ↓
Thin connector
   ↓
Backend
```

This is attractive because the connector remains simple and visible. It can work well for bounded schemas and expert agents.

Its weaknesses appear when the number of systems grows. The agent must carry field vocabularies, date semantics, query operators, pagination rules, joins, ranking behavior, and provider quirks in context or discover them dynamically. Schema changes become agent-facing changes.

### Model B — connector-owned planning

The agent sends a high-level natural-language request and the connector interprets it internally.

```text
User intent
   ↓
search(query: string)
   ↓
Connector planner
   ↓
Backend query
```

This shields the agent from provider details and lets the connector encapsulate domain-specific search knowledge.

The main failure mode is opacity. If the planner silently drops `unresolved`, misinterprets `since September`, or adds an unjustified `team = platform` filter, the agent may receive plausible but incomplete results without knowing why.

### Model C — dedicated retrieval planner

A separate subsystem converts natural language and explicit constraints into a normalized logical plan, then backend adapters compile that plan into provider-native queries.

```text
Agent
   ↓
Retrieval planner
   ↓
Logical QueryPlan
   ↓
Optimizer / adapters
   ↓
Backends
```

This becomes compelling for federated retrieval, shared governance, schema catalogs, or environments where many agents use the same data plane.

It also creates additional infrastructure and a new distributed-system boundary. A dedicated service should not be the starting point merely because the abstraction exists.

### Model D — cooperative planning

The primary agent supplies fuzzy semantic intent and explicit constraints separately. The retrieval layer owns backend-specific compilation and optimization.

```text
Agent
  │
  │ query + explicit predicates + requested scope
  ▼
Retrieval boundary
  │
  ▼
Planner / compiler
  │
  ▼
Backend adapters
```

This divides labor according to what each layer knows best:

- the agent understands the user's conversation and can preserve explicit intent;
- the retrieval layer understands searchable fields, indexes, joins, and ranking capabilities;
- the trusted execution layer understands identity and authorization;
- the backend enforces hard predicates as close to the data as possible.

This is the strongest architectural candidate in the commissioned research, but the benchmark below treats it as a hypothesis rather than a conclusion.

## Natural language is not a substitute for determinism

Natural-language interfaces are useful where relevance itself is fuzzy:

- "incidents that look like cascading retries";
- "design discussions where people were worried about ownership";
- "runbooks relevant to a partial regional outage";
- "issues describing symptoms similar to this customer report".

Other constraints are not fuzzy:

- status must be open;
- timestamp must be after a cutoff;
- amount must exceed a threshold;
- result type must be an incident;
- an identifier must match exactly;
- execution must remain inside the caller's authorized scope.

A useful working hypothesis is:

> Use natural language where relevance is graded. Use typed predicates where correctness is binary. Enforce authorization outside the generative plan entirely.

The last sentence is important. A model may propose a requested scope; it should not decide what the caller is authorized to see.

## Query planning should look more like a compiler

The most useful abstraction from the research is the query plan as an explicit artifact.

```text
User intent                ≈ source language
Logical QueryPlan          ≈ intermediate representation
Physical execution plan    ≈ optimized target plan
Backend query              ≈ target code
```

But one `SearchPlan` object should not mix all four concerns.

### Logical plan

The logical plan should preserve meaning without committing to storage mechanics.

```typescript
type LogicalQueryPlan = {
  semanticIntent: {
    raw: string;
    normalizedTerms?: string[];
  };

  predicates: Array<{
    field: string;
    operator: "eq" | "neq" | "in" | "contains" | "gt" | "gte" | "lt" | "lte" | "prefix";
    value: unknown;
    origin: "explicit" | "normalized" | "inferred";
    confidence?: number;
  }>;

  requestedScopes: string[];

  output: {
    limit: number;
    fields?: string[];
  };
};
```

The `origin` field is not cosmetic. A predicate copied directly from the user and a predicate inferred by a model are epistemically different.

For example:

```json
{
  "field": "team",
  "operator": "eq",
  "value": "platform",
  "origin": "inferred",
  "confidence": 0.71
}
```

A planner may decide that this is too weak to use as a hard pre-filter and preserve it as a ranking hint instead.

This gives us a principled way to measure over-filtering rather than treating all generated filters as equally justified.

### Physical plan

The physical plan belongs after optimization and backend selection.

```typescript
type PhysicalQueryPlan = {
  operations: Array<{
    source: string;
    backend: "sql" | "bm25" | "vector" | "graph" | "api";
    strategy: "exact" | "sparse" | "dense" | "hybrid" | "graph_traversal";
    backendQuery: unknown;
    dependsOn?: string[];
  }>;

  ranking?: {
    fusion?: "rrf" | "relative_score" | "linear";
    reranker?: string;
    candidateLimit: number;
  };
};
```

Choosing HNSW versus exact scan, BM25 versus dense retrieval, cross-encoder reranking, RRF, or a source-specific query form is a physical planning decision. Those details should not leak into the logical IR unless the user explicitly asked for them.

### Security context is not generated query state

Authorization should be modeled separately:

```typescript
type ExecutionContext = {
  principalId: string;
  tenantId?: string;
  groups: string[];
  credentialsRef: string;
  policyContext: Record<string, unknown>;
};
```

The effective query is therefore:

```text
LogicalQueryPlan
      +
Trusted ExecutionContext
      ↓
Policy enforcement
      ↓
PhysicalQueryPlan
```

The planner can request `scope = runtime`. The policy layer decides whether the authenticated principal may search it.

This avoids a dangerous design in which an LLM-generated plan carries supposedly authoritative ACLs or tenancy keys.

## What production systems suggest

The commissioned research found a spectrum rather than one universal pattern.

### Provider-native query languages still matter

Google Drive's `q` parameter is a domain-specific predicate language, not a general natural-language query. Elasticsearch and Vespa expose expressive query languages that combine filtering, ranking, and retrieval primitives. Linear exposes strongly typed GraphQL filtering over its domain.

These interfaces are deterministic and expressive, but they require the caller—or an intermediate compiler—to understand provider semantics.

**[RESEARCH CITATION PASS — verify exact examples against current primary docs before publication]**

### Search systems increasingly separate semantic intent from constraints

Slack's assistant-oriented search APIs, vector databases such as Qdrant, and hybrid search engines expose variants of the same principle: semantic or lexical retrieval is combined with metadata constraints rather than treating metadata as merely more text.

Qdrant is especially instructive because filtering is part of vector execution rather than a cosmetic post-processing layer. Payload indexes and filter cardinality can influence how vector search is executed.

This is the database principle we want at the agent boundary: hard constraints should reduce the candidate space before relevance ranking whenever correctness depends on them.

**[RESEARCH CITATION PASS — Slack, Qdrant, Vespa, Weaviate primary docs]**

### Enterprise NL-to-data systems behave like specialized planners

Databricks Genie and Snowflake Cortex Analyst are not merely "RAG over tables." They translate natural-language questions into structured analytical queries grounded in schemas or semantic models.

The important architectural detail is validation. Databricks documents an Inspect process that can issue auxiliary SQL to test assumptions such as filters, joins, and date ranges. Snowflake supports verified query examples that constrain and evaluate generated SQL behavior.

The lesson is broader than text-to-SQL:

> Once natural language becomes executable retrieval logic, planning needs validation artifacts, not just a good prompt.

**[RESEARCH CITATION PASS — Databricks Genie and Snowflake Cortex Analyst primary docs]**

### Ontology and graph systems move the boundary upward

Palantir AIP and graph-oriented retrieval systems illustrate another direction: the LLM does not target raw tables directly. It operates over typed objects, relations, or graph neighborhoods.

This reduces low-level schema coupling but does not remove planning. It changes the intermediate language.

**[RESEARCH CITATION PASS — Palantir AIP / Foundry and Microsoft GraphRAG primary docs]**

## Query planning is not task planning

A retrieval planner should answer:

> What information should be retrieved, from which sources, under which constraints, and using which execution strategy?

It should not decide:

> What real-world action should the agent take to achieve the user's goal?

Those concerns can interact, but collapsing them creates an overly powerful planner with weak boundaries.

A useful separation is:

```text
Task planner
    ↓ decides what information/action is needed
Retrieval planner
    ↓ compiles information need
Execution layer
    ↓ reads governed data
Task planner
    ↓ decides next step
```

This becomes particularly important when iterative retrieval is enabled. Iteration is an execution strategy available to the task or retrieval loop; it is not a reason to let the retrieval planner mutate external state.

## Failure modes worth designing for

The research identifies several recurring failure modes that the benchmark should make visible.

### Semantic retrieval violates hard filters

The correct topic in the wrong state, tenant, date range, or project is still wrong.

### LLM-generated filters reduce recall

A model can over-specify an intent. "Platform updates on the scheduler" might become `team = Platform Engineering`, excluding relevant records tagged under another team.

This is why inferred predicates need provenance and why over-filter rate belongs in the benchmark.

### Temporal grounding is wrong

"Last quarter," "recent," and "since Tuesday" depend on the current clock, timezone, fiscal calendar, and conversation context.

### Schema entities are hallucinated

A planner can invent fields, enum values, joins, or object relationships that do not exist.

### Hidden query rewriting drifts semantically

Expansion, HyDE, synonyms, and rewriting can improve recall while deleting crucial exact terms.

### Authorization is inferred instead of enforced

No prompt should be responsible for remembering tenancy or ACL constraints. Authorization must be bound from trusted session context and pushed into the data-access layer.

### Simple queries are over-planned

A sophisticated planner can turn an exact ID lookup into several model calls, rewrites, and retrieval stages. This may reduce reliability while increasing latency.

### Plans are unstable across runs

Probabilistic planners can produce different predicates or execution paths for identical or paraphrased requests. Stability is therefore an evaluation dimension, not an implementation footnote.

## Pre-filtering is both a security and retrieval-quality property

Authorization and non-negotiable predicates should be enforced before or during candidate generation whenever the backend supports it.

Post-filtering creates a subtle quality failure:

```text
Global top-k candidates
      ↓
Remove unauthorized / invalid rows
      ↓
Possibly empty result set
```

The system can return no results even though relevant authorized documents exist below the original top-k boundary.

Pre-filtering instead constrains the search space:

```text
Authorized + valid candidate space
      ↓
Similarity / lexical scoring
      ↓
Top-k
```

Relational systems achieve this through predicates and row-level security. Search engines use filter bitsets or structured conditions. Vector engines use payload filters integrated into ANN or exact scoring.

This is one reason the query-planning abstraction cannot stop at relevance ranking.

## Observability should expose plans without leaking internals

Explicit query plans create better debugging, but raw traces can leak schemas, internal identifiers, security scopes, or confidential values.

The system should therefore maintain at least two trace views.

### Agent-facing trace

Safe enough to help the caller understand behavior:

```json
{
  "interpreted_intent": "worker lease failures",
  "applied_filters": {
    "status": "open",
    "created_after": "2026-09-01"
  },
  "searched_sources": ["issues", "runbooks"],
  "candidate_count": 42
}
```

### Internal execution trace

Available only to trusted observability systems:

```text
logical plan
policy decisions
backend queries
index statistics
latency by stage
ranking configuration
cost
model/version
```

The planner should be observable enough to evaluate while avoiding the mistake of exposing full backend query traces to every agent or end user.

## Why comparing products is not enough

Suppose we compare:

```text
System A:
structured filters → Elasticsearch

System B:
natural language → embeddings + reranker
```

If System B retrieves better results, we cannot conclude that natural-language interfaces are better. We changed several variables simultaneously:

- tool contract;
- planning ownership;
- lexical representation;
- retriever;
- ranking policy;
- possibly the index and corpus.

The experiment we want is narrower:

> If the user intent, agent, information universe, and underlying retrieval capabilities are held constant, how does the interface and allocation of query planning change correctness, retrieval quality, stability, latency, and cost?

That is the purpose of `rmax-ai/search-interface-bench`.

## Benchmark architecture

The benchmark should make both logical and physical planning observable.

```text
Synthetic user intent
        ↓
Fixed agent harness + fixed model
        ↓
Condition-specific MCP tool contract
        ↓
Optional planner
        ↓
LogicalQueryPlan
        ↓
Shared optimizer / adapters
        ↓
Shared search services over one frozen corpus
        ↓
Results
```

The corpus, index snapshot, task set, model configuration, budgets, and evaluation code remain fixed across the primary experiment.

The independent variable is the tool/planning architecture.

## Benchmark treatments

The original design compared five parameter shapes. The revised benchmark should compare six architectural treatments.

### T0 — raw search string, no intent planner

The agent receives the smallest possible interface:

```text
search(query: string)
```

The string is sent directly to the baseline retrieval service without structured constraint extraction.

This establishes the cost of having no explicit query-planning layer.

### T1 — agent-generated provider DSL

The agent compiles the user request into a deterministic query language.

```text
worker lease failures status:open after:2026-09-01 project:runtime
```

This tests maximum planning responsibility in the primary agent.

### T2 — cooperative structured search

The agent sends semantic intent and typed hard constraints separately:

```json
{
  "query": "worker failures caused by leases expiring unexpectedly",
  "filters": {
    "status": ["open"],
    "created_after": "2026-09-01"
  },
  "scope": ["runtime"],
  "limit": 10
}
```

The connector compiles these into backend-specific queries but does not reinterpret explicit predicates.

### T3 — connector-owned natural-language planning

The agent sends a natural-language request:

```text
Find unresolved worker failures caused by lease expiry since September in the runtime project.
```

A connector-side planner produces the logical plan.

This tests whether schema encapsulation compensates for planner opacity and extra model cost.

### T4 — explicit QueryPlan IR

The tool exposes planning as a first-class lifecycle:

```text
plan(intent) → LogicalQueryPlan
execute(plan) → ranked candidates
fetch(id) → authoritative record
```

The plan is validated before execution and can be inspected by the harness.

This tests the value of materializing the compiler boundary rather than hiding it behind `search()`.

### T5 — QueryPlan + iterative retrieval

The same plan/execution interface is available, but the agent can inspect results and issue follow-up plans until a fixed budget is exhausted.

This treatment is expected to help multi-hop and investigative tasks while costing more latency, tokens, and tool calls.

Importantly, T5 is not "a better planner." It adds a different execution strategy. Reporting it separately prevents iterative search from being confused with interface quality.

## Synthetic corpus with known ground truth

Real enterprise data is attractive because it is realistic. It is difficult to evaluate cleanly because relevance, hidden constraints, and permissions are often poorly labeled.

The benchmark therefore starts with a deterministic synthetic enterprise-like corpus containing thousands of linked records across several entity types:

- issues and incidents;
- runbooks and documents;
- messages and threads;
- change records;
- people/teams or organizational entities where relational tasks require them.

Each record contains realistic structured metadata—project, status, team, owner, labels, severity, timestamps, numeric fields—as well as generated text with known latent topics and relationships.

The corpus deliberately contains distractors:

- right keywords, wrong project;
- right topic, wrong status;
- semantic equivalents with low lexical overlap;
- stale document versions;
- near duplicates;
- negated or conflicting concepts;
- temporal distractors;
- unauthorized records with high lexical/semantic similarity;
- cases requiring one result to determine the next query.

Consider:

> Find unresolved checkout failures after the August rollout.

A task can contain:

```text
INC-142  checkout timeout after rollout     OPEN     September   ← relevant
INC-102  checkout timeout after rollout     CLOSED   September   ← status distractor
DOC-33   checkout rollout guide             —        August      ← type distractor
INC-189  checkout timeout                   OPEN     July        ← temporal distractor
INC-201  inventory timeout after rollout    OPEN     September   ← semantic distractor
```

Because the generator owns the latent facts, we can score not only whether the final answer is correct but exactly where a plan deviated from intended semantics.

## Ten intent classes

A single aggregate leaderboard would hide the main result. The benchmark should stratify tasks by intent type.

1. **Exact lookup** — identifiers, error codes, commit hashes, exact titles.
2. **Fuzzy conceptual search** — semantic queries with little lexical overlap.
3. **Temporal search** — explicit and relative time windows.
4. **Entity search** — people, projects, services, or other named entities.
5. **Relational search** — joins or graph relationships.
6. **Multi-hop search** — downstream criteria depend on an earlier result.
7. **Ambiguous query** — multiple plausible interpretations or missing constraints.
8. **Negative constraints** — explicit exclusions and negation.
9. **Subjective criteria** — relevance cannot be reduced to boolean filters alone.
10. **Mixed hard + soft constraints** — fuzzy intent combined with mandatory predicates.

The useful outcome is not "T2 wins." It is a decision surface showing where additional planning machinery starts paying for itself.

## Evaluation layers

### 1. Logical-plan correctness

Did the system preserve the information need?

Measure:

- exact predicate correctness;
- dropped constraints;
- hallucinated constraints;
- temporal normalization correctness;
- entity-resolution correctness;
- over-filter rate;
- under-filter rate;
- explicit-vs-inferred predicate provenance correctness;
- abstention/clarification correctness on ambiguous tasks.

### 2. Constraint and policy adherence

Measure separately from relevance:

- hard-constraint violation rate;
- scope violation rate;
- authorization violation rate;
- invalid enum/field rate.

For security-critical constraints the target violation rate is zero.

### 3. Physical-query correctness

Did the logical plan compile into a query that executes and returns the intended set?

Measure:

- backend compilation success;
- execution accuracy;
- adapter errors;
- unsupported-plan rate.

### 4. Retrieval quality

Given a valid physical query, did retrieval rank the right evidence?

Measure:

- Hit@K;
- Recall@K;
- Precision@K;
- MRR;
- nDCG@K;
- distractor rate;
- first relevant rank.

### 5. End-to-end task success

Did the agent solve the task using the returned evidence?

For lookup tasks, score required record IDs. For synthesis tasks, score required facts and evidence support.

### 6. Stability and robustness

A planner that succeeds once but changes semantics under paraphrasing is fragile.

Measure:

- result stability across repeated identical runs;
- logical-plan stability;
- semantic robustness across paraphrases;
- variance in tool-call count;
- variance in retrieved evidence.

### 7. Efficiency

Record:

- tool-schema tokens;
- agent input/output tokens;
- planner tokens;
- number of LLM calls;
- number of retrieval calls;
- reformulations;
- end-to-end latency;
- backend compute;
- monetary cost per task;
- cost per successful task.

### 8. Unnecessary planning

This is a new metric prompted by the research.

For tasks where a direct lookup is sufficient, measure whether the system unnecessarily invokes:

- an LLM planner;
- query decomposition;
- multiple retrieval passes;
- reranking;
- broad source federation.

Call this the **unnecessary planning rate**.

A planner that improves difficult tasks but turns `ENG-1234` into a five-call workflow is not universally better.

## Failure attribution is the methodological payoff

A wrong final answer can originate at several boundaries:

```text
User intent
    ↓
[1] Agent intent/constraint extraction
    ↓
[2] Logical planning
    ↓
[3] Backend compilation
    ↓
[4] Retrieval/ranking
    ↓
[5] Agent synthesis
```

Examples:

- User asks for `open`; agent emits `closed` → agent compilation error.
- Agent sends the correct intent; connector planner drops status → logical planning error.
- Logical plan is correct; SQL adapter compiles the wrong predicate → backend compilation error.
- Physical query is correct; relevant evidence ranks below distractors → retrieval error.
- Correct evidence is returned; agent answers incorrectly → synthesis error.

Most end-to-end evals collapse these into one score. An explicit plan gives us a causal debugging boundary.

## Hypotheses before the results

The benchmark should test, rather than assume, the following.

### H1 — structured/cooperative interfaces win when hard constraints dominate

Exact identifiers, categorical states, numeric ranges, tenant boundaries, and time predicates should benefit from explicit structure.

### H2 — natural-language planning helps semantic discovery

When the user describes behavior without using corpus vocabulary, connector-side planning may improve recall or reduce agent burden.

### H3 — explicit logical plans help mixed queries and debugging

Materializing `LogicalQueryPlan` should improve observability and make semantic/constraint failures easier to catch, but may add planning overhead.

### H4 — iterative retrieval wins primarily on tasks where criteria emerge during search

T5 should help multi-hop investigation more than exact lookups or straightforward filter-heavy tasks.

### H5 — richer planning can hurt simple queries

The best architecture on complex tasks may have the worst unnecessary-planning rate on direct lookups.

### What would falsify these expectations?

Useful negative results include:

- pure natural language matching structured search on constraint-heavy tasks;
- agent-generated DSL matching connector planning while using less infrastructure;
- explicit QueryPlan IR adding observability without improving correctness;
- iterative retrieval failing to justify its latency/token cost;
- inferred filters reducing recall more than semantic search improves it.

Negative results are first-class results.

## Results

**[BENCHMARK PLACEHOLDER — experimental protocol]**

Fill in after protocol freeze:

- repository/commit;
- corpus seed and manifest digest;
- model and reasoning configuration;
- planner model/configuration;
- backend/index configuration;
- development and holdout task counts;
- repetitions;
- budgets;
- statistical treatment.

**[BENCHMARK PLACEHOLDER — overall results]**

Suggested summary table:

| Treatment | Task success | Hard violations | Plan accuracy | Recall@10 | Tokens | Tool calls | Latency | Cost/success |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| T0 Raw string | TBD | TBD | n/a | TBD | TBD | TBD | TBD | TBD |
| T1 Agent DSL | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| T2 Cooperative | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| T3 Connector NL planner | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| T4 Explicit QueryPlan | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| T5 QueryPlan + iterative | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

**[BENCHMARK PLACEHOLDER — results by intent class]**

Do not report only aggregate averages. Include per-class results for all ten intent categories.

**[BENCHMARK PLACEHOLDER — stability]**

Report repeated-run variance and paraphrase robustness for plans and result sets.

**[BENCHMARK PLACEHOLDER — failure attribution]**

Report how failures distribute across:

- agent intent extraction;
- logical planner;
- backend compiler;
- retrieval/ranking;
- synthesis.

**[BENCHMARK PLACEHOLDER — Pareto analysis]**

Plot or summarize:

- task success vs total tokens;
- task success vs latency;
- task success vs cost;
- constraint violations vs interface complexity;
- plan accuracy vs planner cost;
- multi-hop success vs tool calls;
- simple-task success vs unnecessary planning rate.

## Provisional decision heuristics

These should be replaced or refined after the holdout benchmark.

```text
Exact lookup
    → direct structured retrieval

Semantic search + mandatory predicates
    → cooperative query + filters

Several heterogeneous sources
    → logical plan + backend adapters

Criteria depend on previous results
    → decomposition / iterative retrieval

Ambiguous inferred constraint
    → preserve as soft signal, abstain, broaden, or ask
```

The most important heuristic is not to promote inferred structure into a hard filter without evidence.

## A staged implementation path

The article's architecture should not be read as a recommendation to deploy a distributed query-planner service on day one.

A simpler evolution path is:

### V0 — minimal cooperative search

```text
search(query, filters, scope, limit)
```

Implement it in-process inside the MCP/server boundary.

### V1 — explicit logical IR

Add:

```text
intent → LogicalQueryPlan → adapter
```

Persist plans in benchmark traces. Add predicate provenance and validation.

### V2 — optimizer and heterogeneous adapters

Introduce:

- backend capability registry;
- sparse/dense routing;
- filter pushdown;
- hybrid fusion;
- plan validation;
- cost/latency telemetry.

### V3 — iterative and cost-aware retrieval

Only after evidence shows it is useful, add:

- decomposition;
- iterative retrieval;
- information-gain heuristics;
- dynamic source selection;
- cost-aware planning.

Service extraction should happen only when independent scaling, federation, governance, or organizational ownership makes the network boundary useful.

## Implications for MCP and agent tool design

A useful minimal MCP search contract may be surprisingly small:

```typescript
type SearchRequest = {
  query: string;
  filters?: SearchFilters;
  scope?: SearchScope;
  limit?: number;
};
```

For systems that need inspectable planning, expose lifecycle primitives as well:

```text
retrieval_plan(intent, explicit_filters?, requested_scope?)
retrieval_execute(plan_id | plan)
retrieval_fetch(document_id)
```

The convenience path and explicit path can coexist:

```text
search(...)             → common one-shot retrieval
plan → execute → fetch  → debugging, evals, complex workflows
```

This also supports a useful three-stage capability architecture:

```text
search / discover   → approximate, semantic-friendly
fetch / inspect     → exact, stable identifier
execute / mutate    → strongly typed and governed
```

The acceptable ambiguity decreases as we move toward mutation.

Natural language is useful at discovery boundaries without becoming the universal interface for an agent system.

## Tool schemas describe syntax; descriptions must describe semantics

A JSON schema can tell an agent that a tool accepts a string. It cannot tell the agent whether that string should contain:

- keywords;
- provider DSL;
- a complete question;
- a semantic description of the ideal result;
- exact identifiers;
- text used only for reranking.

That contract belongs in tool semantics and documentation.

For agent-facing systems, descriptions are part of the execution protocol, not cosmetic API documentation.

**[RESEARCH CITATION PASS — function calling, MCP tool semantics, tool-description effects]**

## What people usually get wrong

### "Natural-language search" means vector search

It does not. Natural language can be compiled into BM25, SQL, GraphQL, graph traversal, hybrid retrieval, or a multi-source plan.

### A smaller tool schema means a simpler system

A one-field interface can hide an LLM planner, embeddings, filter extraction, several indexes, fusion, and reranking. Complexity moved; it did not disappear.

### Structured search is automatically deterministic

Only the execution is deterministic. The agent can still populate the wrong field or invent the wrong enum.

### More planning is always better

Planning has cognitive, latency, monetary, and failure-surface costs. Exact lookups should remain exact lookups.

### Authorization is just another filter

It is not. User-requested scope can appear in a logical plan. Effective authorization must come from trusted identity context and policy enforcement.

### Iterative retrieval is an alternative to cooperative planning

It is an execution strategy, not a planning-ownership model. The two can coexist.

## Open research questions

Several questions remain genuinely unresolved.

### How should planners price information gain?

In federated retrieval, one source may be cheap and slow, another expensive and precise. A planner needs a cost model that balances expected marginal evidence against latency, API limits, and compute cost.

### How can schema grounding scale?

Enterprise schemas can contain tens of thousands of fields and rapidly changing object types. Copying them into the primary agent prompt does not scale.

### Can generated query plans be verified semantically?

Syntax validation is easy. Verifying that an LLM-generated AST preserved the user's semantics—especially negation and security-relevant constraints—is much harder.

### When should inferred predicates become hard filters?

This may be the key practical problem. A probabilistic planner can infer useful structure, but using a low-confidence inference as a pre-filter destroys recall.

### How much observability is safe?

Plans and traces are valuable for debugging but can leak sensitive schemas, values, or policy context. The right split between agent-visible and internal traces needs systematic treatment.

## The broader architectural question

Search is only one instance of a larger problem.

Agent systems increasingly sit between humans expressing intent and deterministic systems requiring executable representations. The same pattern appears in:

- analytics;
- workflow configuration;
- infrastructure operations;
- database access;
- policy evaluation;
- enterprise automation.

The recurring design question is:

> Which parts of intent should remain flexible, which should be compiled into explicit intermediate representations, and which must become deterministic before execution?

Search gives us a controlled environment in which to answer that question empirically.

## Conclusion

The important distinction is not natural language versus structured APIs.

It is the architecture of interpretation.

```text
Human intent
    ↓
Agent context
    ↓
Logical retrieval plan
    ↓
Trusted policy enforcement
    ↓
Physical query planning
    ↓
Deterministic backend execution
    ↓
Ranked evidence
```

The emerging pattern resembles a small database compiler more than a conventional RAG wrapper: natural language specifies an information need, typed plans preserve semantics and constraints, optimizers choose execution strategies, backend adapters compile provider-specific queries, and the data layer enforces security invariants.

The open empirical question is how much of that machinery is worth paying for.

`search-interface-bench` should answer a narrower and more useful question than "which search API is best?":

> At what complexity of user intent does an explicit query-planning abstraction begin to outperform simpler tool interfaces enough to justify its additional machinery?

That is the decision surface we want: not one universal search contract, but evidence for when planning belongs in the agent, in a connector, in a shared compiler boundary, or in an iterative retrieval loop.

**[FINAL PLACEHOLDER — replace after benchmark]**

Replace the final evidence claim after the holdout run. Keep the conclusion conditional if different task classes favor different architectures.

## References

**[RESEARCH CITATION PASS — convert commissioned research sources to primary references]**

Priority primary sources to verify and cite in the publication version:

- Spider 2.0 benchmark and paper;
- Slack search / assistant search documentation;
- Google Drive `files.list` query documentation;
- Linear GraphQL filtering documentation;
- Databricks Genie / Genie Agents documentation;
- Snowflake Cortex Analyst and verified-query documentation;
- Palantir AIP / Foundry ontology and tool documentation;
- Microsoft GraphRAG documentation/papers;
- Qdrant filtering and query-planning documentation;
- Vespa YQL and ranking documentation;
- Elasticsearch ES|QL / vector search documentation;
- Weaviate hybrid search documentation;
- LangChain structured/self-query retrieval implementation as an implementation precedent;
- Apache Calcite as a query-IR and optimizer precedent.

**[BENCHMARK PLACEHOLDER — project artifacts]**

- `rmax-ai/search-interface-bench`
- benchmark protocol/design commit: TBD
- corpus/task manifest: TBD
- holdout report: TBD
- raw run artifacts: TBD
