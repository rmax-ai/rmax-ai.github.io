---
title: "Prompts Are Contracts, Not Programs: What GPT-5.6 Changes About Agent Design"
slug: prompts-as-contracts-gpt-5-6-agent-design
description: "GPT-5.6's prompting guidance reflects a deeper shift: prompts are becoming contracts that govern adaptive runtimes, not programs that prescribe every step. What that means for agent architecture, authorization, tool design, and evaluation."
author: Max
site: rmax.ai
section: notes
type: essay
status: published
date: 2026-07-15
updated: 2026-07-15
tags:
  - prompting
  - agent-architecture
  - gpt-5-6
  - contracts
  - declarative
  - authorization
  - evals
  - tool-design
reading_time: "18-20 min"
canonical_url: "https://rmax.ai/notes/prompts-as-contracts-gpt-5-6-agent-design/"
license: CC BY 4.0
---

# Prompts Are Contracts, Not Programs: What GPT-5.6 Changes About Agent Design

## Abstract

OpenAI's [prompting guidance for GPT-5.6](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6) points toward a simpler prompt style: define the task clearly, specify what success requires, expose only relevant tools, and avoid unnecessary procedural scaffolding. This article interprets that guidance through a broader architectural lens: prompts are increasingly useful as behavioral contracts rather than procedural programs. A prompt's operational job becomes defining the outcome, constraints, evidence requirements, authorization boundaries, and completion conditions that the model must satisfy. The prompt becomes one control layer inside a larger governed runtime, not the whole program.

## Core Thesis

For GPT-5.6-class models, the prompt should primarily define what must be true at completion, not the exact sequence of actions used to get there.

This article proposes that a good prompt contract specifies:

- the desired outcome;
- success criteria;
- authority and permission boundaries;
- evidence and citation requirements;
- validation requirements;
- output structure;
- stop and escalation rules.

A weak prompt spends too much of its budget on generic activity instructions such as "investigate thoroughly," "use tools carefully," or "respond quickly." Those instructions often conflict, and the system usually reveals the conflict only after it behaves badly.

```mermaid
flowchart TD
    A[User request] --> B{Prompt style}
    B -->|Procedural| C[Specify many steps]
    B -->|Contractual| D[Specify outcome and constraints]
    C --> E[More contradictory instructions]
    C --> F[Less execution flexibility]
    D --> G[Adaptive execution]
    D --> H[Clear completion test]
    G --> I[Governed runtime]
    H --> I
```

## Context and Motivation

The [GPT-5.6 prompting guidance](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6) recommends starting from a working prompt and tool set, then iteratively removing instructions that do not materially improve behavior. Repeated rules, generic process narration, redundant style requirements, irrelevant tools, and duplicated tool descriptions are candidates for removal. The guidance describes what should remain: the user-visible outcome, success criteria, stopping conditions, safety and permission constraints, tool-routing rules where routes depend on context, and required output shape with validation requirements.

Earlier agent systems were often given longer procedural prompts to compensate for perceived weaknesses in planning, tool use, and instruction following. GPT-5.6 can often infer the sequence. It still cannot safely infer permission boundaries, evidence standards, stop conditions, or validation requirements.

The architectural implication is that prompt design becomes less like writing a program in natural language and more like specifying a contract for an adaptive runtime.

## From Procedural Instructions to Declarative Contracts

A procedural prompt says how to work:

> Inspect the repository. Make a plan. Implement the change. Review the result. Run tests. Return a summary.

A contract prompt says what completion requires:

> Implement the requested behavior without changing unrelated functionality. Preserve repository conventions. Validate the change with relevant tests. Report remaining uncertainty.

The second form does not remove planning, inspection, or validation. It delegates the order and scope of those actions to the model.

A useful way to model this is through the lens of declarative infrastructure. An imperative deployment script lists commands. A declarative system defines the desired state and relies on a control loop to reconcile the actual system state with the desired state. In the same way, the prompt defines the destination and the boundaries, while the model and runtime decide how to reconcile the current state against the completion contract.

## Prompt Simplification Is a Behavioral Change

Prompt reduction is not only a latency or token optimization. It changes behavior.

OpenAI reports that, in internal coding-agent evaluations, configurations with leaner system prompts improved evaluation scores by roughly 10–15% while reducing total token use by 41–66% and cost by 33–67%. These ranges are directional results from particular prompt migrations, not universal benchmarks or guaranteed gains. The guidance recommends validating any prompt change against representative application-specific evaluations.

The mechanism is straightforward: every instruction adds another possible source of interference. A prompt that says "always investigate thoroughly," "use the fewest tool calls," "never make assumptions," "do not ask unnecessary questions," and "respond quickly" does not define a coherent policy. It defines competing objectives.

The practical goal is not minimalism. The goal is to remove instructions that do not materially improve behavior.

One practical interpretation of the guidance is to keep the information the model cannot safely invent:

- outcome;
- completion criteria;
- permission model;
- evidence rules;
- validation requirements;
- tool-routing policy;
- output schema.

And to remove repeated rules, generic process narration, redundant style demands, irrelevant tools, and duplicated tool descriptions.

## Define Completion, Not Activity

GPT-5.6 is generally better directed by observable completion conditions than by vague activity instructions.

"Research this topic" does not tell the system when to stop. "Produce a report that answers three questions, supports material claims with retrieved sources, distinguishes evidence from inference, and identifies unresolved gaps" does.

An architectural implication of this guidance is that the runtime gains a usable completion predicate. After each action, the system can compare current evidence against the contract and decide whether to continue, ask, narrow the result, or stop.

```mermaid
flowchart TD
    A[Current evidence] --> B[Evaluate against completion contract]
    B --> C{Any material gap left?}
    C -->|Yes| D[Choose smallest useful action]
    D --> E[Retrieve / inspect / validate]
    E --> A
    C -->|No| F[Terminate and report result]
```

For GPT-5.6-class agents working against evolving evidence, this article proposes that contract-based state reconciliation is usually a better organizing model than a generic "plan, act, observe, reflect" loop. The central question is not "what step comes next?" The central question is "what contract condition is still unsatisfied?"

## Separate Invariants, Policies, and Preferences

Prompt stacks often become brittle because they mix hard rules with softer guidance. The GPT-5.6 guidance advises against absolute rules such as `ALWAYS`, `NEVER`, `must`, and `only` unless they express true invariants. For judgment calls — when to search, ask, use a tool, or keep iterating — the guidance recommends decision rules instead.

This article proposes a three-way separation:

**Invariants** — use absolute language only where it must always hold:

- never expose secrets;
- never claim an action succeeded without tool confirmation;
- never perform destructive actions without approval;
- output must match the required schema.

**Policies** — express context-sensitive behavior as decision rules:

- search when available evidence is insufficient or may be stale;
- ask only when missing information blocks a correct or authorized action;
- use account tools only when the answer depends on account state.

**Preferences** — treat separately and never let them override correctness:

- concise tone;
- preferred validation order;
- favored output style.

This separation matters operationally. Invariants must always hold. Policies guide decisions between valid options. Preferences should never override correctness.

## Authorization Is Part of the Prompt Contract

GPT-5.6 can behave proactively and persist across multi-step tasks, which makes explicit authorization boundaries and stopping conditions more important.

A working contract should distinguish:

- read versus write;
- planning versus execution;
- local versus external effects;
- reversible versus irreversible actions;
- task completion versus scope expansion.

A compact policy often works better than repeated "ask first" language scattered throughout the prompt:

| Action class | Default policy |
|---|---|
| Read or analyze | Allowed |
| Local in-scope modification | Allowed by implementation request |
| Non-destructive validation | Allowed |
| External write | Requires approval |
| Destructive or irreversible action | Requires approval |
| Material scope expansion | Requires approval |

The prompt should communicate this policy, but high-consequence systems should not rely on prompting alone. This article proposes that runtime gates should independently classify and allow, deny, or route proposed actions for approval. The prompt is one layer of the authorization system. It is not the authorization system itself.

## Tools Are Part of the Prompt

Tooling is not separate from prompting. The tool set defines the model's action space, and tool descriptions are part of the behavioral contract.

The GPT-5.6 guidance treats tools as part of the prompt simplification process: expose only the tools relevant to the current task, and describe them with routing and failure semantics rather than vague labels. The guidance recommends trimming tool descriptions that duplicate the schema and keeping only descriptions that materially change tool selection.

A useful tool description explains:

- what the tool does;
- when to use it;
- what it returns;
- important limitations;
- expected errors.

Tool schemas and descriptions should be treated as executable interface contracts. A vague tool name increases decision entropy. A precise description reduces it.

## Let the Runtime Choose the Execution Pattern

Fixed workflow graphs still have value, but they work best where the sequence is known and stable.

Where sequence depends on context, the prompt should define execution policy rather than a rigid script. The GPT-5.6 guidance can be interpreted as a simple execution policy: resolve prerequisites first, parallelize independent reads, and keep dependent steps sequential. Then synthesize those results before acting, and if retrieval comes back empty, try one or two materially different fallbacks.

That policy lets the model construct a task-specific execution graph without hard-coding every sequence in the prompt.

```mermaid
flowchart TD
    A[Task arrives] --> B{Prerequisites resolved?}
    B -->|No| C[Resolve prerequisites]
    C --> B
    B -->|Yes| D{Independent reads available?}
    D -->|Yes| E[Run reads in parallel]
    D -->|No| F[Run dependent step]
    E --> G[Synthesize results]
    G --> F
    F --> H{Retrieval empty or suspiciously narrow?}
    H -->|Yes| I[Try up to two materially different fallbacks]
    I --> G
    H -->|No| J[Proceed or finish]
```

Dynamic orchestration is not automatically better. Regulated or repetitive business processes may still fit deterministic graphs better. Adaptivity matters when the right path depends on local context.

## Use Deterministic Code for Deterministic Work

[Programmatic Tool Calling](https://platform.openai.com/docs/guides/tools-programmatic-tool-calling) draws a cleaner boundary: use deterministic code when a bounded stage can transform structured data more reliably than the model can, and keep the model in control when each result may change the next decision.

Deterministic code is well suited to:

- filtering;
- sorting;
- joining;
- ranking;
- deduplication;
- aggregation;
- repeated validation;
- bulk processing of similar records.

Direct model-controlled calls are better when:

- each result changes the next decision;
- semantic judgment is required;
- approval may be needed;
- intermediate artifacts are small;
- citations or native outputs must be preserved.

This article proposes a layered architecture:

probabilistic interpretation and orchestration  
→ deterministic processing  
→ probabilistic synthesis and judgment  
→ deterministic validation and policy enforcement

In an incident investigation, the model can decide which systems matter, deterministic code can normalize and order thousands of records, the model can interpret the timeline, and deterministic checks can verify the final output against policy.

## Grounding Must Be Explicit

Retrieval access does not automatically create grounded answers. The contract must define what counts as evidence.

That includes:

- which claims require support;
- which sources are allowed;
- how citations attach to claims;
- how disagreement is represented;
- how inference is labeled;
- what to do when evidence is missing.

A strong evidence contract requires retrieved support for every material external claim, places citations beside the claims they support, labels synthesis as synthesis, and leaves unresolved gaps visible.

The most operationally important distinction is between absence of evidence and evidence of absence. "No supporting document was found" is a retrieval observation. It is not automatically proof that an event did not happen.

## Keep the Contract Stable and Task State Compact

Long-running agents can accumulate obsolete plans, verbose tool outputs, failed attempts, and superseded assumptions. OpenAI's GPT-5.6 guidance recommends compacting after meaningful milestones, keeping reusable prompt prefixes stable, and avoiding persisted reasoning when it has become stale.

Building on the guide's recommendations around compaction, reusable prompt prefixes, [prompt caching](https://platform.openai.com/docs/guides/prompt-caching), and persisted reasoning, a useful architecture separates three forms of state:

**Stable contract** — durable goals, permissions, evidence policy, output requirements, and completion criteria.

**Current task state** — the active objective, retrieved evidence, completed actions, remaining gaps, and blockers.

**Historical trace** — prior attempts, verbose tool results, discarded plans, and superseded reasoning.

This three-layer model is not an OpenAI-defined standard. It is a practical design pattern derived from the guide's recommendations on prompt stability, compaction, caching, and persisted state.

Prompt caching then becomes architecturally useful as well as financially useful: stable instructions can remain in a reusable prefix, while compact task state changes as the work progresses.

## More Reasoning Is Not Better Architecture

Increasing reasoning effort is not a substitute for missing system design. The GPT-5.6 guidance recommends checking for missing success criteria, dependency rules, tool-routing rules, and verification loops before increasing reasoning effort.

An architectural inference from this guidance is that reasoning amplifies the model operating inside the architecture. It does not replace the architecture.

A model cannot reliably compensate for undefined completion, missing permissions, absent validation tools, or unavailable evidence sources. Raising reasoning effort may make a broken design slower and more expensive without making it safer or more correct.

## Validation Defines Completion

Producing an artifact is not the same as completing a task. Completion requires evidence that the required conditions hold.

For software changes, that evidence may include targeted tests, type checks, linting, builds, or smoke tests. For visual work, it may include rendering and checking layout, spacing, clipping, responsive behavior, and content integrity.

The prompt contract should define which checks matter before completion can be claimed. The runtime should gather the evidence. The final response should report both the result and the validation status.

[Function calling](https://platform.openai.com/docs/guides/function-calling) and [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) make it easier to require a consistent result-and-evidence schema, although the runtime must still validate whether the evidence is relevant, accurate, and sufficient. Schema compliance does not guarantee evidentiary validity.

## Prompts Should Evolve Through Evals

Prompt development should be treated more like engineering change management than copywriting.

The GPT-5.6 guidance recommends an iterative, eval-driven process: start from a working prompt, remove one group of instructions at a time, and re-evaluate after each change. OpenAI's [Evaluate agent workflows](https://platform.openai.com/docs/guides/agent-evals) documentation provides trace grading and dataset-based evaluation tools for this purpose. The older [Working with evals](https://platform.openai.com/docs/guides/evals) page describes API-specific evaluation features, though OpenAI notes that the Evals platform is transitioning.

A disciplined migration loop aligns with this guidance:

1. Change the model while preserving the current reasoning setting.
2. Run representative evaluations before changing the prompt.
3. Remove obsolete scaffolding, repeated instructions, and irrelevant tools.
4. Add only the smallest targeted instruction needed to fix a measured regression.
5. Rerun evaluations after each prompt or reasoning change.

This sequence isolates variables. If the model, prompt, tools, reasoning level, and runtime all change at once, regressions become hard to diagnose and improvements become hard to trust.

A companion project, [PromptBench](https://rmax.ai/promptbench/), explores eval-driven prompt development for GPT-5.6-class agents in practice.

## Concrete Examples

### Example 1: Repository implementation agent

A weak prompt for a coding agent often says:

> Inspect the repo, make a plan, implement, review your work, run tests, and summarize.

A stronger contract says:

- implement the requested behavior;
- preserve unrelated behavior and repository conventions;
- stay within requested scope;
- do not perform external writes or destructive actions;
- validate with relevant tests or checks;
- report changed behavior, evidence, and remaining uncertainty.

The model can still inspect the repo, plan, implement, and validate. The difference is that the completion contract implies those activities instead of scripting them manually.

### Example 2: Research agent with retrieval

A weak prompt says:

> Research this topic thoroughly.

A stronger contract says:

- answer three specified questions;
- support material claims with retrieved sources;
- distinguish evidence from inference;
- describe disagreements between reliable sources;
- identify missing evidence;
- narrow conclusions when support is incomplete.

The second form provides a stop condition and a reporting standard. It also prevents a common failure mode: the system returns a confident synthesis with unclear provenance.

## Trade-offs and Failure Modes

This approach does not solve every agent problem.

- A contract that is too compact can omit critical business rules or authority boundaries.
- A contract without runtime enforcement still relies too heavily on model compliance.
- Poor tool design can degrade behavior even when prompt design is strong.
- Some workflows fit deterministic graphs better than adaptive loops.
- Completion contracts can be hard to define for open-ended creative or exploratory tasks.
- Overly abstract contracts can hide sequence dependencies that should be explicit in code.

The transition also carries risk. Teams that are used to long prompts may remove structure too aggressively and discover that some of that structure was compensating for gaps elsewhere in the system. Simplify prompts only when evals show that the change improves results.

## Practical Takeaways

1. Write prompts around completion conditions, not activity sequences.
2. Separate invariants, policies, and preferences so the model is not asked to optimize conflicting instructions.
3. Treat tool exposure and tool descriptions as part of the prompt contract.
4. Push deterministic work into code and keep probabilistic judgment with the model.
5. Evaluate prompt changes the way you evaluate code changes: against representative regressions, one variable at a time.

## Positioning Note

This note is not academic research. It does not propose a formal theory of agent cognition or a new benchmark.

It is also not a blog-style opinion piece. Its claims are operational and architectural. They are meant to help practitioners design systems that behave better under real tool, permission, and validation constraints.

It is not vendor documentation either. Although the argument is grounded in current OpenAI documentation, the point is broader than any single endpoint or product surface. The useful abstraction is the contract model itself: prompts define governed behavioral boundaries inside a larger runtime.

## Status and Scope Disclaimer

This is exploratory but evidence-informed lab work, not authoritative guidance. It reflects a practical reading of current OpenAI documentation and the design implications suggested by the source material, not a universal law of agent engineering.

The architectural interpretations in this article — including prompts as contracts, completion predicates, governed runtimes, invariant/policy/preference categories, and the three-layer state model — are the article's own synthesis. OpenAI's guidance provides the foundation; this article builds on it.

The note is scoped to GPT-5.6-class tool-using agents operating in software and research workflows. It does not attempt to cover all model classes, all safety regimes, or highly regulated deployment environments.

## References

1. OpenAI — [Prompting guidance for GPT-5.6](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6). OpenAI API Documentation. Accessed July 15, 2026.
2. OpenAI — [Programmatic Tool Calling](https://platform.openai.com/docs/guides/tools-programmatic-tool-calling). OpenAI API Documentation. Accessed July 15, 2026.
3. OpenAI — [Evaluate agent workflows](https://platform.openai.com/docs/guides/agent-evals). OpenAI API Documentation. Accessed July 15, 2026.
4. OpenAI — [Prompt caching](https://platform.openai.com/docs/guides/prompt-caching). OpenAI API Documentation. Accessed July 15, 2026.
5. OpenAI — [Function calling](https://platform.openai.com/docs/guides/function-calling). OpenAI API Documentation. Accessed July 15, 2026.
6. OpenAI — [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs). OpenAI API Documentation. Accessed July 15, 2026.
7. OpenAI — [Reasoning best practices](https://platform.openai.com/docs/guides/reasoning-best-practices). OpenAI API Documentation. Accessed July 15, 2026.
8. OpenAI — [Working with evals](https://platform.openai.com/docs/guides/evals). OpenAI API Documentation. Accessed July 15, 2026. Note: the Evals platform is transitioning; see Evaluate agent workflows for current evaluation guidance.
