# Prompts Are Contracts, Not Programs: What GPT-5.6 Changes About Agent Design

As language models become more capable, the role of the prompt is changing.

Earlier agent systems often relied on long procedural instructions. Developers tried to specify every step: inspect the repository, make a plan, call tools, review the result, retry failures, run tests, and return an answer in a fixed format.

That approach was understandable. When models were weaker at planning, tool use, and instruction following, detailed scaffolding compensated for those limitations.

But procedural prompting has costs.

Every additional instruction competes for attention. Repeated rules create conflicts. Large tool descriptions consume context. Rigid workflows prevent the model from adapting when the task differs from what the prompt author expected.

OpenAI's prompting guidance for GPT-5.6 suggests a different design principle:

Define the outcome, constraints, available evidence, and completion criteria, then allow the model to determine an efficient path.

The implication is larger than shorter prompts.

Prompts are becoming less like programs and more like contracts governing an adaptive runtime.

## From Procedural Instructions to Declarative Contracts

A procedural prompt describes *how* the model should perform a task:

> Inspect the repository. Identify the relevant files. Create a plan. Implement the change. Review the implementation. Run the tests. Summarize the result.

A declarative prompt describes *what must be true* when the task is complete:

> Implement the requested behavior without changing unrelated functionality.
>
> The requested behavior must work. Existing behavior must remain compatible. Relevant tests must pass. Repository conventions must be preserved. Any remaining uncertainty must be reported.

The second prompt does not eliminate inspection, planning, implementation, or testing. It delegates decisions about their order and scope to the model.

This resembles the difference between imperative and declarative infrastructure.

An imperative deployment script specifies each command that should run. A declarative configuration defines the desired state and leaves the control system responsible for reconciling the current state with that target.

A capable model increasingly acts as that reconciliation engine.

The prompt defines the destination and the boundaries. The model decides how to get there.

## Prompt Simplification Is a Behavioral Change

Prompt reduction is often discussed as a token or latency optimization. That matters, but the larger effect is behavioral.

OpenAI reports that, in an internal sample of coding-agent evaluations, leaner system prompts improved evaluation scores by approximately 10–15%, reduced total token use by 41–66%, and reduced cost by 33–67%. OpenAI presents these numbers as directional rather than universal and recommends validating prompt changes against representative application-specific evaluations.

The mechanism is straightforward: every instruction adds another possible source of interference.

Consider this prompt:

> Always investigate thoroughly.
> Use the fewest possible tool calls.
> Never make assumptions.
> Do not ask unnecessary questions.
> Always verify your conclusions.
> Respond as quickly as possible.

Each instruction sounds reasonable on its own. Together, they create an underspecified optimization problem.

Should the model search more to investigate thoroughly, or stop early to minimize tool calls? Should it ask for missing information to avoid assumptions, or avoid questions? Should it prioritize verification or speed?

A longer prompt is not necessarily more precise. It may simply contain more competing objectives.

The goal is therefore not prompt minimalism for its own sake. The goal is to remove instructions that do not materially improve behavior.

Typical candidates for removal include:

- repeated rules;
- generic process instructions;
- examples that do not change behavior;
- redundant style requirements;
- irrelevant tools;
- tool descriptions that duplicate the schema.

What should remain is the information the model cannot safely infer:

- the desired outcome;
- success criteria;
- stopping conditions;
- evidence requirements;
- permission boundaries;
- validation requirements;
- tool-routing policies;
- required output structure.

The best prompt is not the shortest prompt. It is the smallest prompt that preserves the required behavioral contract.

## Define Completion, Not Activity

Weak prompts often define activities:

> Research this topic.

Stronger prompts define observable completion conditions:

> Produce a report that answers the three research questions, supports material claims with retrieved sources, distinguishes evidence from inference, explains disagreements between reliable sources, identifies missing evidence, and reaches a conclusion tied to the original question.

This changes how the agent operates.

"Research this topic" gives the model no reliable way to determine whether it has done enough. It may stop after one search or continue indefinitely.

Explicit success criteria provide a completion predicate.

After each action, the agent can evaluate:

- Which required conditions are already satisfied?
- Which conditions remain unsatisfied?
- What is the smallest useful action that could close the gap?
- Is the missing evidence obtainable?
- Should the system continue, ask, narrow the answer, or stop?

This suggests that robust agent loops should not be organized only around a generic sequence such as:

> Plan → Act → Observe → Reflect

They should be organized around state reconciliation:

> Current evidence
> → evaluate against the completion contract
> → identify the smallest material gap
> → select an action
> → update evidence and state
> → repeat or terminate

The stopping condition is not an afterthought. It is part of the architecture.

## Separate Invariants, Policies, and Preferences

Prompt authors often use words such as *always*, *never*, *must*, and *only* to make instructions appear stronger.

This can create brittle behavior.

"Always search before answering" forces unnecessary retrieval even when the relevant evidence is already available. "Never ask questions" encourages guessing when a missing field blocks a correct or authorized action. "Always use the CRM" produces pointless tool calls when the answer does not depend on customer data.

Absolute instructions should be reserved for actual invariants:

- never expose secrets;
- do not execute destructive actions without approval;
- do not claim that an action succeeded unless a tool confirmed it;
- every external write requires authorization;
- output must conform to the required schema.

Contextual decisions should be expressed as policies:

- Search when a material claim is unsupported by available evidence or may have changed.
- Ask a clarification question only when missing information prevents a correct or authorized action.
- Use account tools when the answer depends on account-specific state.

The distinction matters:

- **Invariants** must always hold.
- **Policies** describe how to choose between valid actions.
- **Preferences** influence behavior but should not override correctness.
- **Examples** clarify ambiguous cases.

Many prompt stacks mix these categories together. The result is accidental conflict disguised as thoroughness.

## Authorization Is Part of the Contract

More capable models are increasingly proactive. They inspect context, use multiple tools, validate results, and continue until they believe the task is complete.

That makes authorization semantics essential.

An agent must distinguish between:

- reading and modifying;
- planning and executing;
- local and external effects;
- reversible and irreversible actions;
- task completion and scope expansion.

A compact authorization policy might state:

> For review, diagnosis, explanation, or planning, inspect available materials and report findings without making changes.
>
> For implementation or repair, make necessary in-scope local changes and run relevant non-destructive validation.
>
> Require explicit approval before external writes, destructive actions, purchases, production changes, or material expansion of scope.

This is more reliable than scattering repeated "ask first" instructions throughout the prompt.

A simple action policy can be represented as follows:

| Action class | Default policy |
|---|---|
| Read or analyze | Allowed |
| Local in-scope modification | Allowed by an implementation request |
| Non-destructive validation | Allowed |
| External write | Requires approval |
| Destructive or irreversible operation | Requires approval |
| Material scope expansion | Requires approval |

The prompt communicates this policy, but high-consequence systems should not rely on the model alone to enforce it.

The runtime should independently classify tool calls and apply deterministic gates. The model may propose an action; the control plane decides whether it is allowed, denied, masked, or routed for approval.

The prompt is one layer of the authorization system. It is not the authorization system itself.

## Tools Are Part of the Prompt

Tool use is often treated as an implementation detail separate from prompting.

In practice, the tool set and its descriptions strongly shape model behavior.

The available tools define the model's action space. Giving an agent twenty vaguely described tools is not neutral. It increases the number of possible decisions and the probability of unnecessary or incorrect calls.

OpenAI recommends exposing only tools relevant to the current task. Tool descriptions should explain:

- what the tool does;
- when it should be used;
- what it returns;
- important limitations;
- expected errors.

For example:

> `search_customer_accounts`
>
> **Purpose:** Find customer accounts using an email address, external ID, or legal name.
>
> **Use when:** The task requires account-specific state and no exact account ID is available.
>
> **Returns:** A ranked list containing account ID, legal name, status, and match confidence.
>
> **Errors:** Returns `NOT_FOUND` when no reasonable match exists and `AMBIGUOUS` when multiple high-confidence matches require user selection.

This description gives the model routing information, output semantics, and failure behavior.

A description such as "searches customers" does not.

Tool schemas and descriptions should therefore be treated as executable interface contracts.

## Let the Runtime Choose the Execution Pattern

Agent frameworks often encode patterns such as chaining, routing, parallelization, planning, reflection, and multi-agent delegation as fixed workflows.

These patterns remain useful. The design question is *where* the decision should live.

- When the correct sequence is known and important, encode it in the runtime.
- When the sequence depends on context, define a policy and allow the model to choose.
- When a model decision carries material risk, place a deterministic gate around it.

OpenAI's GPT-5.6 guidance recommends resolving prerequisites before dependent actions, parallelizing independent reads, keeping dependent operations sequential, synthesizing parallel results before acting, and attempting a small number of meaningful fallbacks when retrieval produces empty or suspiciously narrow results.

This can be expressed compactly:

> Resolve prerequisites before dependent actions. Run independent reads concurrently when useful. Keep dependent operations sequential. Synthesize parallel results before acting. When retrieval is unexpectedly empty, try up to two materially different fallbacks before concluding that evidence is unavailable.

The model can then construct an execution graph appropriate to the task.

This does not mean every workflow should become dynamic.

Stable, regulated, or well-understood business processes may remain better represented as deterministic graphs. Adaptive orchestration is useful where the correct sequence depends on context, not where the process is already known.

## Use Deterministic Code for Deterministic Work

OpenAI distinguishes direct tool calling from Programmatic Tool Calling.

The important boundary is not the number of calls. It is whether a bounded deterministic processing stage can reduce a large amount of structured data into a smaller, more useful representation.

Programmatic processing is well suited to:

- filtering;
- sorting;
- joining;
- ranking;
- deduplication;
- aggregation;
- repeated validation;
- processing large collections of similar records.

Direct model-controlled calls are preferable when:

- each result may change the next decision;
- semantic judgment is required;
- approval may be needed;
- intermediate outputs are small;
- citations or native artifacts must be preserved.

A useful architecture is:

> probabilistic interpretation and orchestration
> → deterministic processing
> → probabilistic synthesis and judgment
> → deterministic validation and policy enforcement

Consider an incident investigation.

The model decides which log sources are relevant. Tools retrieve records from several systems. Deterministic code normalizes, deduplicates, groups, and orders the results. The model interprets the resulting timeline, forms hypotheses, and chooses follow-up queries. Deterministic checks then verify the final output against required evidence and policy constraints.

The model should not spend tokens manually sorting thousands of records when ordinary code can do it more reliably.

Likewise, deterministic code should not be expected to decide whether a pattern in those records constitutes a causal explanation.

The two modes should cooperate.

## Grounding Must Be Explicit

Giving an agent access to search or retrieval does not guarantee grounded answers.

The prompt should define:

- which claims require evidence;
- what sources are allowed;
- what counts as sufficient support;
- where citations should appear;
- how conflicts should be represented;
- how inference should be labeled;
- what to do when evidence is missing.

A useful evidence contract might state:

> Every material external claim must be supported by retrieved evidence.
>
> Attach each citation directly to the claim it supports.
>
> Distinguish directly supported facts, synthesis across sources, inference from evidence, and unresolved uncertainty.
>
> When reliable sources disagree, describe the disagreement.
>
> When required evidence is unavailable, narrow the conclusion or report the evidence gap. Do not convert absence of evidence into a factual negative.

This last distinction is critical.

"No supporting document was found" does not mean "the event did not happen."

Evidence absence is an observation about the retrieval process. It is not automatically evidence of absence.

## Keep the Contract Stable and Task State Compact

Long-running agents accumulate user messages, tool outputs, plans, hypotheses, failed approaches, validation results, and summaries.

Keeping all of this in the active context creates pressure and can anchor the model to obsolete assumptions.

Agent state should distinguish three layers.

**Stable contract**

- role;
- permissions;
- business rules;
- evidence policy;
- output schema;
- completion criteria.

**Current task state**

- objective;
- active constraints;
- retrieved evidence;
- completed actions;
- remaining gaps;
- unresolved blockers.

**Historical trace**

- previous plans;
- discarded hypotheses;
- verbose tool outputs;
- failed attempts;
- superseded reasoning.

The stable contract should remain reusable and cache-friendly.

The current task state should remain compact and authoritative.

The historical trace should remain available for audit and debugging, but it does not need to remain inside the active context.

This separates system memory from working context. An agent can preserve a complete evidence trail without continuously exposing every historical detail to the model.

## More Reasoning Is Not Better Architecture

It is tempting to treat reasoning effort as a universal quality dial: when outputs are weak, increase the setting.

OpenAI advises against globally maximizing reasoning effort.

Before increasing reasoning, developers should first inspect whether the system is missing:

- a success criterion;
- a dependency rule;
- a tool-routing policy;
- an authorization boundary;
- a verification loop.

A model cannot reliably reason around an undefined completion condition. It cannot compensate for missing permission semantics. It cannot validate an implementation without access to validation tools. It cannot retrieve evidence from an unavailable source.

Reasoning effort amplifies the model operating inside the architecture.

It does not replace the architecture.

## Validation Defines Completion

Producing an artifact is not the same as completing the task.

For a software change, completion may require:

- targeted tests;
- type checking;
- linting;
- an affected-package build;
- a smoke test;
- explicit disclosure when validation could not be performed.

For a visual artifact, completion may require rendering and inspecting clipping, spacing, hierarchy, missing content, responsive behavior, and visual consistency.

The prompt should tell the model which checks matter before the task can be considered complete.

This aligns with an evidence-first view of agentic work.

The primary output should not be only a patch, document, or decision. It should be a result accompanied by evidence that the defined completion conditions hold.

A software change might return:

```json
{
  "change_summary": "Added authentication enforcement to the endpoint.",
  "files_changed": [
    "src/routes/account.ts",
    "tests/account-auth.test.ts"
  ],
  "claims": [
    {
      "claim": "Unauthenticated requests are rejected.",
      "evidence": [
        "account-auth test passed"
      ]
    }
  ],
  "validation": {
    "targeted_tests": "passed",
    "type_check": "passed",
    "smoke_test": "passed"
  },
  "remaining_uncertainty": []
}
```

The prompt defines the completion contract. The runtime gathers and checks the evidence. The final response communicates the result.

## Prompts Should Evolve Through Evals

Prompt development is still often conducted through informal inspection:

1. Edit the prompt.
2. Try several examples.
3. Read the outputs.
4. Decide whether they feel better.

This is insufficient for production systems.

OpenAI recommends a controlled migration process:

1. Change the model while preserving the existing reasoning setting.
2. Run representative evaluations before changing the prompt.
3. Remove obsolete scaffolding, repeated instructions, and irrelevant tools.
4. Add only the smallest targeted instruction needed to fix a measured regression.
5. Rerun evaluations after every prompt or reasoning change.

The key principle is experimental isolation.

If the model, prompt, tools, reasoning effort, and runtime all change simultaneously, it becomes difficult to identify what caused an improvement or regression.

Prompt changes should be treated like code changes:

- linked to a measured failure mode;
- evaluated against a regression suite;
- reviewed for unintended effects;
- deployed incrementally;
- observed in production.

This creates a tighter optimization loop:

> production trace
> → failure classification
> → representative eval case
> → small prompt, tool, or runtime change
> → regression evaluation
> → controlled deployment

The result is not a perfect prompt.

It is a prompt stack that evolves through evidence.

## A Compact Contract for Complex Agents

A practical prompt can be organized into a small number of sections:

**Role**
What function does the agent perform?

**Goal**
What user-visible outcome should exist?

**Success criteria**
What must be true before the task is complete?

**Constraints**
What safety, business, evidence, permission, and side-effect limits apply?

**Tools**
Which tools are available, when should they be used, and what are their limits?

**Output**
What format and level of detail are required?

**Stop rules**
When should the agent retry, ask, abstain, escalate, or finish?

For example:

> **Role**
> You are an engineering agent working inside an existing repository.
>
> **Goal**
> Implement the requested change while preserving unrelated behavior.
>
> **Success criteria**
> - The requested behavior is implemented.
> - Relevant tests pass.
> - Repository conventions are preserved.
> - Changed behavior and remaining uncertainty are reported.
>
> **Constraints**
> - Stay within the requested scope.
> - Do not perform external writes or destructive actions.
> - Do not claim success without validation evidence.
>
> **Tools**
> - Inspect relevant repository files before modifying them.
> - Run independent reads concurrently when useful.
> - Use targeted tests, type checks, and builds for validation.
> - Retry unexpectedly empty retrieval once using a materially different query.
>
> **Output**
> Return the change summary, files changed, validation performed, and blockers.
>
> **Stop rules**
> Stop when all success criteria are satisfied. Ask only when missing information blocks a correct implementation. Report a blocker when required evidence or access is unavailable.

The prompt says little about the exact sequence of operations.

It says much more about what correct completion means.

## The Architectural Shift

GPT-5.6's prompting guidance reflects a broader transition in agent engineering.

The first generation of LLM applications treated prompts as strings.

The next treated prompts as programs: long procedural scripts attempting to control every intermediate action.

The emerging generation treats prompts as contracts inside a larger control system.

That control system includes:

- tool schemas;
- authorization gates;
- deterministic processing stages;
- state management;
- retrieval;
- evidence tracking;
- validation;
- evaluations;
- observability;
- human approval.

The model is neither a simple function nor the entire application.

It is an adaptive decision component operating inside a governed runtime.

The prompt defines the objective and behavioral boundaries. Tools expose possible actions. Deterministic components enforce invariants. Evidence determines whether claims are justified. Validation determines whether work is complete. Evals determine whether system changes improve behavior.

As models become more capable, the goal should not be to encode more intelligence into the prompt.

The goal should be to specify the contract clearly enough that the system can exercise intelligence without violating its boundaries.

## Conclusion

The main lesson from GPT-5.6 prompting guidance is not merely that prompts should be shorter.

It is that prompts should contain a different kind of information.

Remove procedural detail that the model can infer. Preserve the outcome, constraints, authority, evidence requirements, validation rules, and completion conditions that the model cannot safely invent.

Use deterministic code for deterministic processing. Use runtime gates for authorization. Use tools for interaction with the world. Use evidence to support claims. Use validation to establish completion. Use evaluations to change the system deliberately.

The prompt is no longer the program.

It is the contract governing an adaptive program.

## References

1. OpenAI — [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering). OpenAI API Documentation. Accessed July 15, 2026.
2. OpenAI — [Using tools](https://platform.openai.com/docs/guides/tools). OpenAI API Documentation. Accessed July 15, 2026.
3. OpenAI — [Programmatic Tool Calling](https://platform.openai.com/docs/guides/tools-programmatic-tool-calling). OpenAI API Documentation. Accessed July 15, 2026.
4. OpenAI — [Working with evals](https://platform.openai.com/docs/guides/evals). OpenAI API Documentation. Accessed July 15, 2026.
5. OpenAI — [Prompt caching](https://platform.openai.com/docs/guides/prompt-caching). OpenAI API Documentation. Accessed July 15, 2026.
6. OpenAI — [Function calling](https://platform.openai.com/docs/guides/function-calling). OpenAI API Documentation. Accessed July 15, 2026.
7. OpenAI — [Reasoning best practices](https://platform.openai.com/docs/guides/reasoning-best-practices). OpenAI API Documentation. Accessed July 15, 2026.
8. OpenAI — [Evaluate agent workflows](https://platform.openai.com/docs/guides/agent-evals). OpenAI API Documentation. Accessed July 15, 2026.
