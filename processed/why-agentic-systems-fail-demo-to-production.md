# Why Agentic Systems Fail Between the Demo and Production

*Part one of the series From Agent Demos to Governed Systems.*

An agent receives a customer-support request. It retrieves the customer's account, checks the relevant policy, drafts a useful response, and updates the ticket. The demonstration succeeds.

Production presents a different problem.

Credentials expire. Customer records contain conflicting identifiers. Policy documents change. Events arrive twice. Tools return partial results. A timeout occurs after an account change succeeds but before the agent receives confirmation. Some requests require judgment; others require authority the agent should not possess.

The demonstration tested whether the model could complete a selected task under favorable conditions. Production tests whether the surrounding system can operate across variable inputs, repeated executions, dependency failures, ambiguous state, cost constraints, and consequential actions.

Model capability remains necessary. Better reasoning, planning, instruction following, and tool selection increase the probability of successful execution. They do not provide durable state, transaction semantics, permission boundaries, recovery procedures, or operational visibility.

Many incidents attributed broadly to "the model" originate elsewhere: retrieval supplied obsolete evidence, a tool schema invited the wrong call, the harness repeated an action, or the product granted excessive autonomy.

The engineering problem is larger than the prompt-model pair.

## A demo samples a path; production exposes a distribution

A successful demonstration establishes that one configuration of the model, prompt, context, tools, and environment can complete one selected task.

It does not establish reliability across the distribution of conditions the deployed system will encounter.

Agents generate trajectories rather than isolated responses. They select tools, interpret results, revise plans, recover from errors, and decide when to stop. Two executions of the same task can follow different paths, even when they produce similar final answers.

Nondeterminism does not make a system unreliable by definition. It changes what engineers must measure.

OpenAI's [evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices/) treats evaluations as structured tests for measuring model and system behavior under nondeterminism. Anthropic's [guidance on agent evaluations](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) recommends realistic tasks, multiple trials, and graders aligned with the properties that matter in deployment.

The relevant questions are therefore broader than "Did the demo work?":

* How often does the system complete this class of task?
* Which inputs produce divergent or unsafe trajectories?
* How does performance change when tools fail or context is incomplete?
* What happens after interruption?
* What costs and side effects occur along successful paths?

A demo provides evidence of possibility. Production readiness requires evidence about a distribution.

## Final answers conceal execution failures

A correct final response can result from an unacceptable process.

Google's agent-evaluation framework distinguishes [final-response evaluation from trajectory evaluation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents). Final-response evaluation asks whether the agent produced the desired result. Trajectory evaluation examines the sequence of tool calls and actions used to produce it.

This distinction matters because a plausible answer can conceal:

* unnecessary tool calls;
* access to an unauthorized data source;
* incorrect intermediate conclusions;
* failed calls that were silently ignored;
* duplicated mutations;
* excessive latency or cost;
* accidental success that will not survive a small input change.
OpenAI's [trace-grading documentation](https://developers.openai.com/api/docs/guides/trace-grading/) makes the same shift in evaluation scope. A trace exposes the sequence of decisions, tool calls, and observations that produced an outcome. Teams can then identify failure patterns and detect regressions across executions rather than inspecting only the final response.

### Example A: the customer-support agent

Suppose the agent produces an accurate response and closes the ticket. An output-level evaluator gives it a high score.

The trace shows a different result.

The agent first queried the wrong customer record. It recovered after finding a contradiction, but then retrieved an obsolete policy page. When the account-update tool timed out, it repeated the request. The underlying service had already applied the first update, so the customer's account changed twice.

The final response was correct. The execution was not.

The missing controls were authoritative identity resolution, versioned policy retrieval, an idempotency key for the mutation, explicit handling of ambiguous tool outcomes, and human approval before an irreversible change.

A prompt can tell an agent not to repeat an action. An idempotency key prevents the infrastructure from applying the same action twice.

## Prompt improvements cannot repair missing system controls

Prompts influence model behavior. They can clarify objectives, define tool-use policies, request verification, and describe stopping heuristics.

They cannot implement properties that belong to the runtime.

A prompt cannot create:

* durable persistence after a process crashes;
* atomic updates across external systems;
* service-level authorization;
* reliable timeout handling;
* retry budgets;
* circuit breaking;
* resource isolation;
* an audit trail the agent cannot rewrite.

Established reliability patterns remain relevant. Microsoft's [Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry) recommends retrying only failures likely to be transient and constraining retry frequency and duration. Its [Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) prevents a system from repeatedly calling a dependency that remains unhealthy.

These are executable runtime policies. They are not instructions the model may choose to follow.

The model can participate in recovery. The system must bound that recovery.

## State turns a conversation into a system

Agent implementations often conflate four forms of state.

Model context is the information available in the current inference call. It is temporary, capacity-limited, and frequently reconstructed.

Workflow state records the current execution position: completed steps, pending operations, retry counts, approvals, intermediate artifacts, and remaining budgets.

Durable memory stores information intended to influence future sessions, such as user preferences, prior decisions, or learned procedures.

External system state exists in databases, ticket systems, repositories, payment platforms, and other services the agent can inspect or modify.

These state layers have different consistency, ownership, and retention requirements.

Treating the conversation transcript as the workflow database forces the model to infer what has already happened. Treating a retrieved document as authoritative external state allows obsolete evidence to drive decisions. Treating an unconfirmed tool call as a failed call can duplicate a successful mutation.

Anthropic's [work on long-running agent harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) describes the use of progress files, source-control history, structured feature lists, and initialization procedures to preserve continuity across context windows. This is operational evidence from coding agents rather than a universal architecture. It nevertheless demonstrates a general requirement: critical execution state must survive outside the model's immediate context.
Weak state management produces familiar distributed-systems failures through a new interface: lost progress, repeated actions, stale decisions, inconsistent recovery, and concurrent actors overwriting one another.

## Autonomy creates loops, and loops require boundaries

Agents operate through loops. The model observes the current state, chooses an action, receives a result, and determines the next step.

A system may contain several loops:

* a planning loop decomposes the task;
* a tool-use loop gathers information or changes external state;
* a retry loop responds to failures;
* a reflection loop evaluates intermediate work;
* a delegation loop assigns work to another agent.

Looping is not the defect. It is the mechanism that allows an agent to adapt when the full solution cannot be specified in advance.

The defect is an unbounded loop without progress criteria, state transitions, retry limits, resource budgets, or termination conditions.

A temporary API failure can produce hundreds of repeated calls. A planner can reformulate the same unsuccessful strategy without generating new evidence. Two agents can delegate the same unresolved task to one another. A reflection step can continue revising an answer after additional work no longer improves it.

Microsoft's [agent-orchestration guidance](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) therefore includes iteration limits for iterative patterns and distinguishes workflows with deterministic control flow from those that permit dynamic agent decisions.

This reveals the missing control system. The relevant unit is not only the agent's prompt. It is the loop governing observation, action, verification, recovery, and termination.

The next article in this series develops that control structure in detail.

## More agents do not remove complexity

Specialized agents can improve decomposition, parallel search, and context isolation.

Anthropic reports that its [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) benefited from parallel execution and separate contexts for open-ended research. The same engineering account describes substantial challenges in coordination, evaluation, reliability, and token consumption.

Adding agents creates additional interfaces:

* responsibility must be assigned;
* results must be merged;
* disagreements must be resolved;
* shared state must remain consistent;
* failures must propagate or remain isolated;
* permissions must not expand through delegation;
* traces must preserve causal relationships.

A multi-agent system can therefore solve one form of complexity by introducing another.

Anthropic's [containment engineering](https://www.anthropic.com/engineering/how-we-contain-claude) identifies a related security risk: a system may incorrectly trust a sub-agent's output even when that output was derived from untrusted material. Delegation can obscure the provenance of information without making that information safer.

The correct conclusion is not that multi-agent systems are inherently defective. It is that their additional complexity must earn its place through measurable improvements in task quality, latency, context management, or fault isolation.

When a deterministic workflow or a single agent can satisfy the requirement, additional agents may enlarge the failure surface without delivering a corresponding benefit.

## Diagnosis requires separating failure domains

Calling every incorrect outcome a hallucination prevents useful diagnosis.

A production investigation should separate at least six failure domains.

Model failures include incorrect reasoning, weak planning, instruction-following errors, hallucinated facts, and poor tool selection.

Context and retrieval failures include missing evidence, stale information, excessive context, incorrect ranking, and prompt injection through retrieved content.
Tool-interface failures include ambiguous descriptions, invalid parameters, weak schemas, misleading return values, and unhandled partial success.

Harness and orchestration failures include absent stopping conditions, repeated calls, recursive delegation, state corruption, uncontrolled concurrency, and defective retry policies.

Runtime and infrastructure failures include timeouts, rate limits, network errors, unavailable services, duplicate delivery, and persistence failures.

Product and governance failures include inappropriate autonomy, excessive permissions, absent approvals, unclear ownership, weak success criteria, and no escalation path.

These domains interact.

A model may choose the wrong tool because its description is ambiguous. Retrieval may return an obsolete procedure that the model follows correctly. A tool may complete an operation while the runtime reports a timeout, causing the harness to repeat the action.

The purpose of classification is not to excuse model errors. It is to identify the control that can prevent recurrence.

### Example B: the coding agent

A coding agent receives a bug report, modifies the repository, and passes the regression test supplied with the task.

The patch appears successful.

Inspection shows that the agent also changed unrelated configuration files, ignored a failing type-check command, attempted the same unsuccessful fix three times, and left generated artifacts in the working tree. The repository remains in a partially modified state.

The narrow test established that one expected behavior now works. It did not establish that the repository is coherent.

The missing controls were a clean-worktree checkpoint, file-scope constraints, bounded strategy retries, mandatory validation of command results, a broader verification suite, and rollback after unsuccessful attempts.

A stronger model may reduce the frequency of these failures. It does not make the controls unnecessary.

## Production requires evidence, not confidence

Evaluation-driven development turns failures into reusable evidence.

Anthropic recommends constructing evaluations from representative tasks and using observed failures to expand the test set. OpenAI similarly describes eval-driven development as a cycle in which teams collect traces, identify failure modes, add representative examples to evaluation datasets, and test system changes against those datasets.

A credible evaluation program combines:

* representative task sets;
* repeated executions;
* malformed and adversarial inputs;
* tool-contract tests;
* outcome and trajectory scoring;
* human review for consequential cases;
* latency, token, cost, and tool-call measurements;
* regression suites;
* controlled rollout;
* explicit failure classification.

This differs from reactive prompt patching.

Reactive patching begins with one visible failure, adds language intended to prevent it, and redeploys. Without a regression set, the team cannot determine whether the change fixed the broader failure class, overfitted to one example, or degraded another part of the system.

Observability supplies the evidence required after deployment. Google's [agent-observability guidance](https://docs.cloud.google.com/stackdriver/docs) combines logs, metrics, traces, and prompt-response data to expose execution behavior, resource use, errors, and quality signals.

Conventional telemetry remains necessary, but agent systems add new questions:

* Which evidence influenced the decision?
* Why was this tool selected?
* How many times was it called?
* Which component initiated the action?
* What state changed before the failure?
* Did the system succeed through a valid process or through accidental error cancellation?

Without traces, teams can observe an incorrect outcome but struggle to reconstruct its cause. Without evaluations, they can patch an incident but cannot determine whether the system improved.

## A minimum production-readiness test

Before describing an agent as production-ready, a team should be able to answer:
* What task and input distribution was evaluated?
* What constitutes successful task completion?
* Which trajectories are unacceptable even when the final result is correct?
* What state is persisted, where, and for how long?
* Which actions are safe to retry?
* How is idempotency enforced?
* What are the retry, time, token, tool-call, and cost budgets?
* Which actions require human approval?
* What permissions does the agent possess?
* Can every consequential action be attributed and traced?
* Can execution resume safely after interruption?
* How are model, retrieval, tool, harness, and infrastructure failures distinguished?
* What triggers rollback, escalation, circuit breaking, or shutdown?

No checklist proves reliability. This one establishes whether the team has defined the conditions under which reliability can be tested.

## The missing control system

The gap between a demo and production is not closed by refining the prompt until the agent appears consistent.

A demonstration shows that a probabilistic worker can perform a task. Production engineering determines when that worker may act, what it may access, how long it may continue, which evidence it must collect, how its actions are verified, and what happens when a component fails.

The next step is not another prompt template. It is to engineer the loop that controls how models, tools, state, verification, budgets, and stopping conditions interact.

The second article in this series develops that idea as loop engineering: the design of deterministic control structures around probabilistic workers.

## References

1. [**Demystifying evals for AI agents**](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Anthropic, January 9, 2026. Provides engineering guidance on representative tasks, multiple trials, graders, and evaluation design for agents.

2. [**How we built our multi-agent research system**](https://www.anthropic.com/engineering/multi-agent-research-system) — Anthropic, June 13, 2025. Reports operational experience with parallel agents, coordination, tool design, evaluation, and resource consumption.

3. [**Effective harnesses for long-running agents**](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Anthropic, November 26, 2025. Describes external progress tracking and initialization procedures used to preserve continuity across long-running coding tasks.

4. [**How we contain Claude across products**](https://www.anthropic.com/engineering/how-we-contain-claude) — Anthropic, May 25, 2026. Documents containment boundaries and trust-escalation risks in systems that process untrusted content.

5. [**Building effective agents**](https://www.anthropic.com/research/building-effective-agents) — Anthropic, December 19, 2024. Distinguishes workflows from agents and recommends using the simplest architecture that satisfies the task.

6. [**Writing effective tools for agents—with agents**](https://www.anthropic.com/engineering/writing-tools-for-agents) — Anthropic, September 11, 2025. Provides operational guidance on tool descriptions, schemas, testing, and agent-tool interface design.

7. [**Evaluation best practices**](https://developers.openai.com/api/docs/guides/evaluation-best-practices/) — OpenAI, current documentation accessed June 2026. Explains structured evaluation for nondeterministic model applications and recommends evaluation-driven development.

8. [**Trace grading**](https://developers.openai.com/api/docs/guides/trace-grading/) — OpenAI, current documentation accessed June 2026. Describes evaluation over agent execution traces rather than final responses alone.

9. [**Testing agent skills systematically with evals**](https://developers.openai.com/blog/eval-skills/) — OpenAI, January 22, 2026. Presents a workflow for defining success, collecting test cases, and evaluating reusable agent skills.
10. [**Evaluate generative AI agents**](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents) — Google Cloud, current documentation accessed June 2026. Defines final-response and trajectory evaluation and provides metrics for both.

11. [**Agent observability**](https://docs.cloud.google.com/stackdriver/docs) — Google Cloud, current documentation accessed June 2026. Describes logs, metrics, traces, token measurements, and prompt-response data for observing agent behavior.

12. [**AI agent orchestration patterns**](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — Microsoft, February 12, 2026. Documents orchestration trade-offs, iteration limits, shared-state risks, and architecture-selection criteria.

13. [**Retry pattern**](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry) and [**Circuit Breaker pattern**](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) — Microsoft, current documentation accessed June 2026. Provide established mechanisms for bounded recovery from transient and persistent dependency failures.

14. [**Agent system design patterns**](https://docs.databricks.com/aws/en/agents/agent-system-design-patterns) — Databricks, current documentation accessed June 2026. Presents a continuum from deterministic workflows to autonomous and multi-agent systems, with associated complexity trade-offs.
