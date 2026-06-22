# Deep Research Is an Evidence Workflow, Not a Long-Running Agent

### Part 3 of the series *From Agent Demos to Governed Systems*

Two systems produce similarly polished reports.

The first retains a conversation, a browsing trajectory, and the final prose. The second retains the research objective, questions asked, sources examined, evidence extracted, claims accepted, contradictions found, approval decisions, and gaps left unresolved.

Their outputs may look similar. Their epistemic and operational properties are not.

The report is an output of the research process. It should not be the process's only durable state.

Serious deep research is not primarily a long-running generation task. It is a governed process for transforming questions and sources into evidence-backed, qualified claims.

That distinction determines whether research can be inspected, challenged, resumed, revised, verified, and reused—or merely read.

## Why the long-running-agent abstraction is insufficient

A long-running research agent is a useful abstraction.

A user submits a prompt. The agent plans, browses, reads, reasons, revises its search, and eventually writes a report.

```
Prompt
  ↓
Agent browses, reasons, and writes
  ↓
Final report
```

This architecture minimizes coordination overhead. It supports flexible exploration and can work well for narrow, low-stakes questions where the user can directly inspect the answer.

OpenAI describes Deep Research as executing multi-step browsing trajectories that can backtrack as it encounters new information. Google's Gemini Deep Research similarly creates a research plan, searches repeatedly, and synthesizes a report with source links. Anthropic's Research system uses a lead agent that delegates parallel searches to subagents. These are more sophisticated than a single linear prompt-response call. They demonstrate that long-horizon search and tool use can materially improve research performance. [1][2][3]

The problem is not that an agent runs for a long time. The problem appears when too much of the research process exists only inside its execution trajectory.

A conventional research trajectory may combine:

* interpreting the request;
* deciding scope;
* generating questions;
* constructing searches;
* selecting sources;
* extracting evidence;
* forming claims;
* resolving contradictions;
* judging completeness;
* writing prose;
* checking its own output.

When these operations do not produce durable intermediate objects, failure diagnosis becomes difficult.

An unsupported conclusion might result from poor scope, weak retrieval, a source-selection error, incorrect extraction, faulty synthesis, or citation drift. A polished paragraph conceals which transformation failed.

The same problem affects resumability. A process cannot safely resume merely by replaying a transcript or asking a model to "continue." It must know which questions were completed, which evidence was accepted, which claims remain contested, which side effects already occurred, and which checkpoint represents committed state.

Long-running agents can produce good research. They are not, however, a sufficient state model for governed research.

## From prose generation to evidence workflow

An evidence workflow externalizes the research process as explicit stages and durable objects.

```
Long-running agent                   Evidence workflow

Prompt                               Intent
  ↓                                    ↓
Opaque research trajectory           Scope and perspectives
  ↓                                    ↓
Report                               Questions
                                       ↓
                                     Search plans and sources
                                       ↓
                                     Evidence fragments
                                       ↓
                                     Claims and contradictions
                                       ↓
                                     Coverage assessment
                                       ↓
                                     Synthesis
                                       ↓
                                     Verification
                                       ↓
                                     Report
```

The important change is not the number of agents. It is the representation of state.

A single model can participate in an evidence workflow. A multi-agent system can remain opaque. Reliability depends less on how many model instances exist than on which decisions become inspectable records.

### Research intent

A topic is not a research intent.

"AI agents in finance" names an area.

"The company should adopt the design" is a recommendation dependent on objectives and trade-offs.

They require different evidence and review standards.

A useful research intent captures the objective, intended audience, decision context, required depth, time horizon, geographic or organizational scope, exclusions, evidence standards, and output form.

Without this object, the system optimizes against an underspecified prompt. It may produce a broad report while failing the decision the report was meant to support.

### Scope

Scope defines the investigation's boundary: included and excluded questions, relevant dates, acceptable source types, required perspectives, depth, and stopping constraints.

Uncontrolled scope expansion is a common failure mode in autonomous research. Each source introduces adjacent concepts, which produce additional questions, which generate more searches. More activity can reduce coherence rather than improve coverage.

A workflow should widen scope through an explicit decision, not through accidental topic drift.

### Perspectives

Perspectives are analytical lenses used to generate questions.

A security perspective might ask how a proposed design can be abused. An operational perspective asks how it fails under real workload and ownership constraints. A legal perspective asks which claims depend on jurisdiction. A historical perspective asks whether the apparent novelty has precedents.

Perspectives should alter the research frontier. They should not merely become decorative report headings.

### Research questions

Research objectives must be decomposed into answerable questions, not simply into an outline.

"Architecture," "security," and "limitations" are headings. They do not specify what evidence would resolve them.

A research question should have an identifier, rationale, priority, status, dependencies, candidate queries, supporting evidence, unresolved gaps, confidence, and completion criteria.

Persisting questions matters because a question hidden inside model context cannot be reliably scheduled, inspected, reopened, or resumed.

### Search queries and sources

Queries are attempts to locate evidence. They are not the unit of research progress.

Several queries can serve one question. One query can produce sources relevant to several questions. Counting searches therefore measures activity, not knowledge gained.

Source records should preserve title, author or organization, publication and access dates, location, source type, provenance, authority, possible conflicts, and version information.

Source authority should remain claim-relative. A vendor's documentation may be authoritative for its current API behavior and weak evidence for its product's comparative superiority. A systematic review may be strong evidence for aggregate effects but inappropriate for a recently changed implementation detail.

Reducing source quality to one universal score destroys these distinctions.

### Evidence fragments

An evidence fragment is the smallest source-grounded object used to support or challenge a claim.

It should retain the exact source, location, excerpt or structured fact, extraction method, question served, surrounding context, limitations, version, and whether the fragment represents direct evidence or interpretation.

Source summaries are weaker research objects. A summary compresses the document before the workflow knows every claim for which it may later be used. It can erase qualifiers, populations, dates, exceptions, and negative findings.

### Claims

A claim is an assertion the report asks the reader to accept.

Claims should preserve:

* a precise statement;
* applicable scope;
* supporting and contradicting evidence;
* confidence;
* qualifications;
* derivation type;
* review status.

The workflow should distinguish directly reported, extracted, calculated, inferred, synthesized, and recommended claims.

This distinction matters. "The API returns field X" can be checked against documentation or code. "The design will reduce operational risk" is an inference.

## The claim as the unit of research quality

Paragraph-level fluency is a poor quality metric.

A paragraph may contain five propositions supported by one citation. The citation may support two of them, partially support a third, and say nothing about the remaining two. Because the prose is cohesive, the evidential discontinuity is easy to miss.

The claim, not the paragraph, should be the primary unit of research quality.

Claim-level representation exposes several common defects:

**Unsupported claims.** The statement has no linked evidence.

**Overgeneralization.** Evidence about one population, time period, benchmark, or implementation becomes a universal conclusion.

**Citation mismatch.** A cited source is relevant to the topic but does not entail the statement.

**Missing qualification.** The prose omits conditions or uncertainty retained in the source.

**Contradiction suppression.** Conflicting evidence disappears during synthesis.

Citation evaluation research supports checking correctness and completeness separately. A report can contain valid citations for some statements while leaving other material claims uncited. The ALCE benchmark evaluates long-form answers through citation correctness, completeness, and overall answer quality rather than treating citation presence as sufficient. The RAGAS framework likewise separates dimensions such as faithfulness and context relevance. [4][5]

These evaluation methods are imperfect, particularly when model judges evaluate model-generated claims. But they support the architectural point: research quality decomposes into smaller verifiable properties.

## Questions, evidence, claims, and contradictions as state

A durable research process should not store only the final report. Its authoritative state should include the objects from which the report was derived.

```
ResearchRun
├── Objective and scope
├── Perspectives
├── Questions and dependencies
├── Search plans
├── Sources
├── Evidence fragments
├── Claims
├── Contradictions
├── Coverage metrics
├── Outline and drafts
├── Verification findings
├── Approval decisions
└── Runtime checkpoints
```

Contradictions require first-class representation.

Disagreement does not automatically indicate that one source is wrong. Sources may use different definitions, populations, periods, causal assumptions, or measurement methods. A contradiction record should therefore capture the competing claims, source relationships, possible explanations, temporal or definitional differences, and resolution status.

Flattening such conflict into "some experts disagree" discards the structure needed to investigate it.

Provenance standards offer a useful conceptual foundation. W3C PROV represents entities, activities, agents, derivations, and usage relationships involved in producing an artifact. A research system need not implement PROV directly to benefit from its central idea: an output becomes more assessable when the transformations and actors that produced it remain explicit. [6][7]

## Applying loop engineering

The previous article introduced loop engineering as a deterministic control structure around probabilistic workers:

```
DISCOVER → PLAN → EXECUTE → VERIFY → COMMIT → REFLECT → DECIDE
```

Deep research is one application of that loop.

```
DISCOVER
Inspect questions, sources, evidence, contradictions, approvals, and gaps
    ↓
PLAN
Choose the next bounded research increment
    ↓
EXECUTE
Search, retrieve, extract evidence, and propose claims
    ↓
VERIFY
Check relevance, fidelity, entailment, policy, and quality
    ↓
COMMIT
Persist accepted objects and updated statuses
    ↓
REFLECT
Diagnose weak evidence, bias, stagnation, and missing perspectives
    ↓
DECIDE
Continue, reframe, request review, synthesize, publish, or stop
```

**Discover.** The workflow inspects current state rather than relying on a model's recollection: completed questions, existing sources, unresolved contradictions, changed sources, coverage gaps, and approval status.

**Plan.** It selects a bounded next increment. This may mean investigating one question, adding a missing perspective, resolving a contradiction, finding a primary source, or strengthening a material claim.

**Execute.** Models and tools generate queries, retrieve sources, read documents, extract evidence, and propose claims.

**Verify.** The workflow checks source relevance, extraction fidelity, claim entailment, citation alignment, source policy, scope compliance, and numerical or temporal consistency.

Deterministic checks should run first where possible: schema validity, identifier integrity, duplicate detection, citation targets, date formats, arithmetic, policy rules, and graph constraints. Model judgment remains useful for semantic entailment, causal overreach, relevance, and qualification preservation.

**Commit.** Only accepted objects become authoritative state: approved sources, verified evidence, supported claims, resolved question statuses, and updated coverage.

This boundary prevents speculative model output from silently becoming established research state.

**Reflect.** The system diagnoses weak strategies, source concentration, low information gain, unresolved disagreement, missing viewpoints, and search saturation.

**Decide.** The workflow explicitly chooses whether to continue, reframe, widen scope, narrow scope, request human input, synthesize, publish, or stop.

"Continue researching" should be a decision based on specific gaps and expected information gain, not a model's vague preference for more information.

## Building the Evidence Workflow: deep-research-assistant

[deep-research-assistant](https://github.com/rmax-ai/deep-research-assistant) is an experimental governed research runtime built to test this architecture.

We designed the project around a simple premise: generated prose should be a projection over research state, not the authoritative research state itself.

The deployed site exposes architecture, implementation-phase, and API documentation. It links to the public `rmax-ai/deep-research-assistant` repository. The inspected repository contains Python source, tests, architecture and threat-model documents, a specification, and CI configuration.

The deployed site is documentation-oriented rather than an interactive hosted research UI. Its API examples target `localhost:8080`; no public API base URL or runnable web form was exposed during inspection. I could therefore inspect the documented API and source implementation but could not execute live research runs against the deployed service. No live-run results are inferred below.

### Actual architecture

The implementation separates three planes.

```
┌───────────────────────────────────────────────────┐
│ Governance plane                                  │
│ Identity · policy · approval · audit · publication│
└───────────────────────┬───────────────────────────┘
                        │ constrains
┌───────────────────────▼───────────────────────────┐
│ Workflow plane                                    │
│ State · tasks · budgets · checkpoints · stopping  │
└───────────────────────┬───────────────────────────┘
                        │ invokes
┌───────────────────────▼───────────────────────────┐
│ Cognitive plane                                   │
│ Questions · search · extraction · claims · prose  │
└───────────────────────────────────────────────────┘
```

The architecture document assigns identity, authorization, approval, and audit to deterministic governance components. The workflow plane handles orchestration, scheduling, budgets, stopping, persistence, and recovery. The cognitive plane contains bounded model-backed roles.

The source implementation supports this separation, although not perfectly.

`src/deep_research/workflow/graph.py` defines an ADK workflow and maps nodes to roles including research director, question architect, query planner, evidence curator, claim builder, counter-evidence agent, section writer, and verifier. The graph also invokes deterministic modules for scheduling, coverage calculation, deduplication, source clustering, policy evaluation, checkpoints, and stopping decisions.

The same graph file instruments node execution with run identifiers, phases, question context, workflow versions, logical-input hashes, idempotency keys, persisted audit events, node execution records, and checkpoints. It handles approval pauses by setting the run to `awaiting_approval` and recording the checkpoint from which execution should resume.

This is stronger evidence than a diagram alone: the runtime code treats persistence, approvals, identity propagation, and recovery as execution concerns rather than prompt instructions.

Some responsibilities remain coupled. The main workflow graph is large and coordinates routing, instrumentation, persistence, event publication, approval exceptions, and cognitive execution. This concentrates substantial operational behavior in one module. The separation is conceptual and partly modular, but the orchestration layer is not yet minimal.

### Implemented lifecycle

The deployed architecture documents a 27-node lifecycle:

```
scope_classify
  → perspective_generate
  → question_graph_build
  → approve_plan
  → scheduler_select
  → search_plan_create
  → source_retrieve
  → source_policy_apply
  → evidence_extract
  → claims_construct
  → knowledge_organize
  → contradictions_search
  → coverage_calculate
  → moderator
  → interventions_apply
  → scope_change_apply
  → stop_evaluate
  → outline_build
  → approve_outline
  → draft_generate
  → verify_draft
  → repair_draft
  → final_gate_check
  → render_output
```

Compared with the conceptual evidence lifecycle, intent, scope, perspectives, questions, search, sources, evidence, claims, contradictions, coverage, synthesis, verification, and publication all have direct or close matches.

Some stages are collapsed. Source retrieval and source appraisal sit close together in the workflow. Synthesis is split across outline construction, section generation, repair, and rendering. Publication is represented through the final gate and export rather than a complete publishing subsystem.

Continuous updating remains partial. The implementation-phases page states that watch-mode primitives exist but are not wired into the public API as a completed capability.

### Primary domain objects

The project specification defines typed state for research runs, objectives, scopes, perspectives, questions, search plans, sources, evidence fragments, claims, contradictions, outlines, drafts, verification findings, approval decisions, and metrics.

The architecture follows several deliberate constraints:

* questions persist as graph objects;
* exact evidence excerpts are intended to remain immutable;
* claims link to evidence identifiers;
* material inferred or causal claims trigger counter-evidence work;
* section writers receive approved claims and evidence rather than unrestricted browsing tools;
* verification runs after drafting;
* approval gates sit at semantic boundaries.

These constraints matter because they reduce the authority of prose. A section can be regenerated while preserving the claims and evidence on which it depends.

### Workflow state and resumability

The deployed architecture reports four durable runtime record classes:

* `research_runs`;
* `workflow_checkpoints`;
* `workflow_node_executions`;
* `approval_decisions`;
* append-only `audit_events`.

The workflow source creates a logical input hash and an idempotency key from the run, node, workflow version, and input. During resume, it can reuse a completed node execution rather than rerunning it. After node completion, it creates a checkpoint and associates the node result with that checkpoint.

This provides a concrete basis for resumability.

It does not yet establish exactly-once semantics for every external tool. Search and retrieval are usually safe to repeat, but future workflows that invoke mutable systems will require explicit side-effect boundaries, provider idempotency support, or compensating actions.

### Evidence, claims, and provenance

The project's intended provenance path is:

```
Report text
  → cited claim
  → evidence fragment
  → source record
```

The API documentation exposes run, graph, frontier, progress, events, concept-map, approval, intervention, log, and export endpoints. The current export implementation returns the report body and requested format; dedicated JSON evidence packages and richer provenance exports are documented as not yet implemented.

That limitation is consequential. Internal provenance can exist without being fully visible to report consumers. A system becomes inspectable only to the extent that its interfaces expose the retained state.

### Coverage and stopping

The project treats coverage as more than source count. Its architecture includes question completion, perspective balance, contradiction resolution, evidence novelty, and information gain.

The documented information-gain formula combines new claims, evidence, knowledge, contradiction resolution, and duplication penalties. The stopping logic considers coverage, budget, deadlines, and diminishing information gain.

This is a useful architecture hypothesis, not yet a validated definition of research completeness.

Coverage remains domain-dependent. A legal review, scientific evidence synthesis, architecture survey, and market analysis require different source classes and stopping criteria. A weighted formula can organize judgment but cannot eliminate it.

### Contradictions

The workflow includes a counter-evidence stage and explicit contradiction records. Deterministic source clustering attempts to identify evidence that appears independent but originates from the same publisher or dependency cluster.

This is more defensible than counting repeated claims as corroboration.

It remains possible to miss contradictions because query generation, search-provider ranking, source access, and extraction are incomplete. The system can only represent disagreements it discovers.

### Human review

Four documented gates cover scope, research planning, evidence and outline, and publication.

API-created runs use strict approval behavior by default. When a gate requires review, the workflow transitions to `awaiting_approval`, persists the decision, and resumes from a checkpoint after approval.

This places human review at semantic boundaries rather than after every model call. That reduces review burden while preserving control over decisions that materially change research direction or publication status.

The trade-off is latency. A strict workflow can remain blocked indefinitely when ownership is unclear or reviewers lack enough context to decide.

### Models, tools, and deterministic code

The project uses Google ADK and Gemini-backed agents for semantic tasks. The inspected `pyproject.toml` declares Google ADK, Pydantic, SQLAlchemy, FastAPI, HTTPX, structured logging, SQLite support, and optional PostgreSQL dependencies.

Deterministic code handles policy evaluation, source deduplication, clustering, scheduling, budget accounting, checkpoints, stopping rules, and some citation checks. Model-backed workers handle scope interpretation, question and query generation, evidence extraction, claim construction, contradiction analysis, outlining, drafting, and semantic verification.

The verifier uses a separate prompt and lower-temperature configuration from the writer. This reduces direct coupling but does not provide full epistemic independence. Generator and verifier may still share model-family biases, training data, and failure modes.

### Relationship to adk-loop-lab

`adk-loop-lab` demonstrates the general control loop around probabilistic workers. `deep-research-assistant` applies the same principle to an epistemic workflow.

The connection is structural:

| Loop engineering primitive | Deep-research application |
|---|---|
| Discover | Inspect frontier and retained evidence |
| Plan | Select a bounded research task |
| Execute | Search, extract, and propose claims |
| Verify | Check evidence and entailment |
| Commit | Persist accepted research objects |
| Reflect | Diagnose gaps and weak strategies |
| Decide | Continue, reframe, synthesize, or stop |

The research system adds domain-specific objects—questions, evidence, claims, contradictions, and coverage—but preserves the same separation between proposal and committed state.

### Implementation-evidence matrix

| Architectural claim | Project evidence | Status | Limitation |
|---|---|---|---|
| Research intent is explicit | Objective fields in API and specification | Implemented | Intent richness depends on input and scope agent |
| Questions persist as workflow state | Question objects and app:questions state in workflow | Implemented | Public UI does not expose a complete editable question workspace |
| Evidence is separate from prose | Evidence objects and evidence-extraction stage | Implemented | No public evidence-package export |
| Claims link to evidence | Claim schema and documented citation path | Implemented | End-to-end live trace could not be inspected on deployed service |
| Contradictions are searched | Counter-evidence node and contradiction state | Implemented | Discovery remains search- and model-dependent |
| Coverage is evaluated | Coverage node and stopping metrics | Implemented | Metric validity has not been demonstrated against a benchmark |
| Human approval exists | Four gates and persisted approval decisions | Implemented | Review ownership and burden remain operational questions |
| Runs are resumable | Checkpoints, node executions, idempotency keys | Implemented | External side-effect semantics require further validation |
| Final prose preserves provenance | Claim and citation architecture | Partial | Current export does not expose a complete machine-readable evidence package |
| Verification is separate from synthesis | Writer and verifier stages use distinct prompts/configuration | Partial | Model-family independence is not established |

### One research run, traced end to end

A live end-to-end run could not be executed through the deployed site. The site exposes documentation and local API instructions but no public research endpoint or interactive runner.

The API documentation contains an illustrative run concerning enterprise controls for a Google ADK research assistant. It demonstrates the intended request and approval flow, but it does not expose enough generated artifacts to trace a substantive claim through question, query, source, evidence, qualification, final prose, and citation.

The correct artifact table is therefore:

| Research object | Example from the inspected deployment |
|---|---|
| Intent | "How should a Google ADK-based research assistant govern tool usage safely in an enterprise environment?" |
| Question | Unavailable from a completed live run |
| Source | Unavailable from a completed live run |
| Evidence fragment | Unavailable from a completed live run |
| Claim | Unavailable from a completed live run |
| Contradiction or qualification | Unavailable from a completed live run |
| Coverage gap | Unavailable from a completed live run |
| Final report section | Unavailable from a completed live run |

This absence is not merely a documentation inconvenience. It identifies a product and research gap.

A system that claims inspectability should publish at least one sanitized, complete trace showing how an objective becomes questions, queries, evidence fragments, claims, contradictions, verification findings, and final citations. Tests can establish structural behavior. A worked trace establishes whether the structures remain meaningful in practice.

## What the architecture buys us

An evidence workflow offers seven concrete advantages.

**Inspectability.** Reviewers can challenge a claim without reconstructing the entire agent trajectory.

**Resumability.** The workflow resumes from committed objects and checkpoints instead of relying on conversational memory.

**Targeted verification.** Expensive model judgment can focus on material or uncertain claims.

**Evidence reuse.** Verified fragments and claims can support multiple reports without repeating all retrieval and extraction.

**Explicit uncertainty.** Contradictions and unresolved gaps remain part of state rather than disappearing into prose.

**Human review.** Approval can occur at scope, plan, evidence, and publication boundaries.

**Failure diagnosis.** Teams can distinguish search failure from extraction failure, claim-formation failure, synthesis failure, and rendering failure.

These benefits become more valuable when research informs consequential decisions, spans many sources, must survive multiple sessions, involves disagreement, or operates under organizational governance.

## What it costs

The additional structure is not free.

An evidence workflow requires schemas, databases, identifiers, orchestration, migrations, checkpoints, review interfaces, evaluators, and operational telemetry.

It increases latency and model usage. Extracting evidence and constructing claims separately may require more calls than asking one model to write a report directly.

Schemas can become rigid. A representation designed for technical reports may fit historical interpretation or exploratory science poorly.

Human gates can become queues. Inspectability can produce an overwhelming amount of material unless the interface prioritizes material claims and unresolved uncertainty.

The architecture can also become process theater. A claim with three identifiers, two scores, and a verification status is not necessarily true. Structured errors remain errors.

A simpler agent is often sufficient when the question is narrow, low stakes, disposable, straightforward to source, and easy for the user to verify directly.

The evidence workflow becomes justified when the cost of an unsupported conclusion exceeds the cost of maintaining the workflow.

## What remains unsolved

A structured workflow does not make research true. It makes the path from question to conclusion more visible and therefore more contestable.

Several problems remain.

### Search-provider dependence

The workflow inherits ranking biases, indexing gaps, personalization effects, and crawler restrictions from its search provider. A 2026 study comparing Google Search, AI Overviews, and Gemini found substantial differences in retrieved source sets and instability under small query variations within its experimental setting. [8]

This risk is implied by the architecture. It was not measured in the inspected project.

### Source access and modality

PDFs, tables, paywalled sources, dynamic pages, datasets, images, and multimedia require different extraction strategies. The available project evidence does not establish robust handling across these formats.

### Citation drift

A correct evidence link can become incorrect when prose is rewritten, claims are merged, or qualifiers are removed. Claim identifiers reduce this risk but do not eliminate it.

### Model-judge bias

A verifier based on the same model family may reproduce the writer's assumptions. Distinct prompts and temperatures provide procedural separation, not independent ground truth.

### Incomplete contradiction discovery

Counter-evidence search improves the workflow only when the system generates effective adversarial queries and can access relevant sources. Absence of discovered contradiction is not evidence of consensus.

### Coverage validity

The project implements coverage and information-gain metrics, but the inspected materials do not demonstrate that those metrics predict answer completeness or decision quality. Its specification proposes compute-matched comparison against one-shot retrieval, but no benchmark results were found.

### Cost escalation

Each explicit stage creates additional computation. Iterative counter-evidence work and repair loops may produce high marginal cost after the major questions are already answered.

Another research cycle has positive expected value only when the expected reduction in decision-relevant uncertainty exceeds its cost, delay, and risk of introducing noise. Current systems approximate this through coverage, novelty, materiality, and budget rules. They do not calculate it reliably.

### Ground truth

Open research questions often lack an authoritative answer. Verification can test entailment, provenance, consistency, and method. It cannot manufacture ground truth where the evidence remains incomplete.

### Reuse and invalidation

Claims can be reused only if their scope, dependencies, versions, and source freshness remain explicit. When a source changes, the workflow must identify which evidence and derived claims are affected.

The project's watch-mode primitives point toward this capability, but the deployed materials classify continuous research as partial.

### Evaluation

A strong evaluation program should separately test:

* question decomposition;
* retrieval recall and source diversity;
* extraction fidelity;
* claim atomicity;
* claim–evidence entailment;
* citation correctness and completeness;
* contradiction discovery;
* calibration;
* coverage decisions;
* resume correctness;
* approval enforcement;
* final decision usefulness.

No single benchmark captures all of these properties. Systems such as Salesforce's Enterprise Deep Research, Stanford's STORM, and its collaborative extension Co-STORM provide useful architectural and evaluation references, but their results should not be generalized beyond their tasks, datasets, and judge configurations. [9][10][11]

The project currently answers many architectural questions with implemented mechanisms. It has not yet validated that those mechanisms produce better research outcomes than simpler alternatives under matched budgets.

That is the next research problem.

## Conclusion: research as inspectable transformation

Deep research should be understood as an inspectable transformation:

```
Intent
  ↓
Questions
  ↓
Sources
  ↓
Evidence
  ↓
Claims
  ↓
Qualified conclusions
```

Models remain essential throughout this process. They interpret intent, generate questions, navigate unfamiliar material, extract evidence, propose claims, identify disagreements, and construct readable arguments.

But the reliability of the result depends on the workflow that preserves, verifies, and governs the transformations between those stages.

The durable state of research should not be a long conversation or a polished report. It should be the structured record of what was asked, what was found, what the sources support, what remains contested, and why the workflow decided to stop.

This completes the architectural progression of the series:

```
Agent reliability
  ↓
Loop engineering
  ↓
Evidence workflows
```

The first article argued that a successful demonstration does not establish production reliability.

The second argued that probabilistic workers require deterministic control loops.

This third argument follows directly: when the work is research, the loop must control not only execution but evidence.

The report is the rendered artifact.

The research is the governed path that makes the artifact defensible.

## References

[1] "Introducing Deep Research" — OpenAI, February 2, 2025; updated February 10, 2026. Describes OpenAI's multi-step browsing, reasoning, source citation, progress, and intervention model.

[2] "Try Deep Research in Gemini" — Dave Citron, Google, December 11, 2024. Describes research-plan generation, iterative web research, report synthesis, and source links.

[3] "How We Built Our Multi-Agent Research System" — Anthropic, June 13, 2025. Provides engineering evidence on parallel research agents, coordination, evaluation, and production reliability.

[4] "ALCE: Enabling Large Language Models to Generate Text with Citations" — Gao et al., 2023. Separates citation correctness, completeness, and response quality in long-form generation.

[5] "RAGAS: Automated Evaluation of Retrieval-Augmented Generation" — Es et al., 2023. Provides evaluation dimensions for retrieval relevance, faithfulness, and answer quality.

[6] "PROV-Overview" — Paul Groth and Luc Moreau, W3C, April 30, 2013. Defines provenance concepts for entities, activities, agents, derivations, versioning, and reproducibility.

[7] "PAV Ontology: Provenance, Authoring and Versioning" — Ciccarese et al., 2013. Presents a lightweight model for distinguishing source, authoring, curation, and representation provenance.

[8] "How Generative AI Disrupts Search" — Grossman et al., April 30, 2026. Examines source-selection differences and instability across conventional and generative search systems.

[9] "Enterprise Deep Research: Steerable Multi-Agent Deep Research for Enterprise Analytics" — Akshara Prabhakar et al., October 20, 2025. Presents a steerable multi-agent architecture with planning, specialized search, reflection, enterprise tools, and benchmark evaluation.

[10] "STORM: Synthesis of Topic Outlines through Retrieval and Multi-Perspective Question Asking" — Shao et al., 2024. Introduces perspective-guided question generation and iterative retrieval for long-form knowledge synthesis.

[11] "Co-STORM: Collaborative Knowledge Curation through Dynamic Discourse" — Jiang et al., 2024. Explores collaborative steering and evolving knowledge structures during research.

[12] "PRISMA 2020 Statement" — Page et al., March 29, 2021. Provides established guidance for transparent reporting of systematic-review search, selection, exclusion, and synthesis processes.

[13] "GRADE Handbook" — GRADE Working Group. Describes structured evaluation of evidence certainty without reducing every judgment to source prestige alone.

[14] Deep Research Assistant — rmax.ai, inspected June 22, 2026. Deployed project documentation describing the runtime, workflow, and exposed capabilities.

[15] Deep Research Assistant source repository — rmax-ai, inspected June 22, 2026. Primary implementation source for workflow orchestration, schemas, governance, persistence, and tests.

[16] Deep Research Assistant: System Architecture — rmax-ai, 2026. Defines the three-plane architecture, workflow topology, agent responsibilities, and data model.

[17] Deep Research Assistant: Specification — rmax-ai, 2026. Defines intended features, acceptance criteria, and research-quality requirements.

[18] "Deep Research System Card" — OpenAI, February 25, 2025. Documents safety evaluation and risks including prompt injection, hallucination, privacy, bias, and code execution.

### Project materials inspected

* Deployed landing page
* Deployed architecture page
* Deployed implementation-phases page
* Deployed API reference
* GitHub repository
* Repository README.md
* Repository SPEC.md
* Repository docs/ARCHITECTURE.md
* Repository pyproject.toml
* Repository src/deep_research/workflow/graph.py
* Workflow checkpoint, approval, persistence, identity, policy, scheduling, coverage, deduplication, and stopping integrations imported and invoked by the workflow graph
* Documented REST routes for run creation, inspection, graph, frontier, progress, events, logs, interventions, approvals, and export
* Documented phase status and roadmap boundaries, including partial continuous-research support
* Repository-level deterministic and opt-in live-validation strategy

No completed public live research run, generated evidence package, trace, or final report was exposed by the deployed application during inspection. The API documentation points to a local service, so the two requested representative live runs could not be executed against the deployment. No run artifacts were fabricated.
