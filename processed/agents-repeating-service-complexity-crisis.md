# Agents Are Repeating the Service Complexity Crisis

## What Steve Yegge's service critique explains about tool explosion, MCP and Databricks Omnigent

Enterprise agent platforms are accumulating tools faster than they are developing coherent abstractions.

An internal assistant may begin with access to search, Jira and documentation. It soon acquires connectors for GitHub, Slack, databases, cloud infrastructure, CRM systems and internal APIs. Coding agents add shell commands, filesystem operations, package managers and deployment tools. Each integration appears locally useful. Collectively, they produce a capability surface that is difficult for both models and humans to understand.

This is usually framed as a model problem. The agent selected the wrong tool, lost track of the task, called APIs in the wrong order, exceeded its context window or failed to recover from an intermediate error.

But many of these failures originate below the model.

The platform has exposed a poorly structured service surface and asked a stochastic planner to compensate for it.

Steve Yegge's writing on services and complexity provides a useful frame for understanding this failure. His broader service-platform argument is that systems do not become coherent platforms merely by exposing everything through network-accessible interfaces. Poorly chosen service boundaries can relocate complexity rather than remove it. Narrow operations force consumers to reconstruct larger behaviours through deep call graphs, duplicated orchestration and knowledge of implementation details.[1][2]

Agent systems reproduce this problem in a more unstable form.

A traditional software client executes orchestration written and reviewed by engineers. An agent dynamically reconstructs the orchestration from natural-language goals, tool descriptions, context and intermediate responses. What was once deterministic client code becomes an inference-time planning problem.

Model Context Protocol makes capabilities easier to connect, but it does not determine whether those capabilities form a good agent-facing architecture. Databricks Omnigent introduces a control layer above fragmented agent harnesses, but coordinating runtimes does not automatically repair badly designed tools.

The durable architecture therefore needs two distinct interventions:

1. Reduce the semantic complexity exposed to the agent through better capability design.
2. Govern the remaining operational complexity through an agent execution control plane.

The first determines what coherent actions the system exposes. The second controls how agents execute them.

## Yegge's service lesson

Yegge's service arguments are often reduced to the idea that every internal capability should be exposed through an API.

That reading is incomplete.

Exposing a method over a network does not automatically produce a platform. A collection of endpoints can remain tightly coupled, overly procedural or specific to one consumer. When service boundaries reflect implementation details rather than stable capabilities, clients inherit the missing abstraction.

Suppose an application wants to create a customer account. A coherent service might expose:

open_customer_account

A fragmented service surface might instead require:

create_person
create_contact_record
assign_customer_identifier
create_billing_profile
attach_default_terms
create_account_ledger
activate_customer

The second design appears more composable because every operation is smaller. In practice, it transfers the burden of sequencing, validation, error handling and recovery to every consumer.

Each client must know:

- which calls are required;
- the correct order;
- how identifiers flow between calls;
- which operations may be retried;
- which intermediate states are valid;
- what to do after partial failure;
- how to compensate for earlier mutations;
- which business rules apply to the sequence as a whole.

The service provider has not removed complexity. It has exported it.
This was already costly when clients were conventional applications. It becomes substantially more dangerous when the client is an agent.

## The agent is now the service client

A traditional client encodes orchestration as software:

validated input
    ↓
fixed call sequence
    ↓
explicit error handling
    ↓
known transaction semantics

An agentic client operates differently:

natural-language goal
    ↓
tool discovery
    ↓
probabilistic tool selection
    ↓
interpretation of intermediate output
    ↓
dynamic replanning
    ↓
attempted recovery

The agent must infer during execution what application developers would previously have specified in code.

Consider a request such as:

> Create an incident for the payment failure, assign the correct team, notify the merchant-support channel and link the relevant deployment.

A fragmented capability catalog might contain:

- search_logs
- find_payment
- get_deployment
- create_issue
- update_issue_field
- add_issue_label
- assign_issue
- search_user
- search_team
- post_slack_message
- add_slack_reaction
- create_confluence_page
- link_external_resource

The agent must infer the domain workflow from these primitives. It must decide whether the issue should exist before the deployment is linked, whether assignment depends on payment region, which Slack channel is authorized, and what happens if the message succeeds but issue creation fails.

This is not simply tool use. It is runtime reconstruction of distributed business logic.

The deeper the tool trajectory, the larger the failure surface:

- more network round trips;
- more intermediate outputs in context;
- more opportunities for invalid arguments;
- more partial state mutations;
- more authorization decisions;
- more chances for planning drift;
- more difficult replay and debugging.

The resulting system resembles the client-side orchestration Yegge warned about, except that the client code is regenerated probabilistically for every task.

## Tool explosion is service explosion for models

Tool explosion is often discussed as a prompt-size problem. Every tool schema consumes tokens, so a large catalog leaves less room for the user request, retrieved context and execution history.

That is real, but it is not the whole problem.

Tool catalogs also create an abstraction problem. Many tools overlap semantically, operate at different levels of granularity or become valid only at particular workflow states.

Recent research supports the narrower empirical claim that tool-list construction materially affects downstream performance. Repantis and colleagues studied adaptive shortlist sizing across registries ranging from 20 to 3,251 tools. On one benchmark, an adaptive policy presented approximately seven tools on average while approaching the coverage of a fixed fifty-tool shortlist. Their downstream evaluation also found that shorter adaptive lists improved correct selection when the relevant tool was available.[3]

A related paper, ToolChoiceConfusion, argues that semantic relevance alone is insufficient. A tool can be related to a task while still being unnecessary or premature. Its Causal Minimal Tool Filtering method uses precondition-and-effect contracts to expose the minimal next-step frontier. In its main benchmark, the method reduced visible tools from 100 to one per step and cut token consumption by roughly 90 percent relative to exposing all tools, while retaining comparable aggregate success to the strongest causal baseline.[4]

These results should not be interpreted as a universal maximum number of tools. Tool quality, model capability, task structure and semantic overlap all matter.

The architectural lesson is more important:

> An agent should not see every available capability merely because the platform can expose it.

Tool discovery should consider at least four dimensions:

1. Semantic relevance
   Is the capability related to the user's goal?
2. Authorization
   May this actor use it against this resource?
3. Causal validity
   Is the capability valid at the current workflow state?
4. Risk
   Should the capability be available without additional controls?

This is already more than ordinary tool retrieval. It resembles planning over a governed capability graph.

## More atomic tools are not necessarily more composable

Agent-platform teams often respond to unreliable tools by making them smaller.

The intuition is understandable. A narrow tool should be easier to describe, test and authorize. But shrinking tools indefinitely creates the same teller-call pattern that damaged earlier distributed systems.

A task that requires four independent mutations is not automatically safer because each mutation has its own schema.

Suppose an expense workflow exposes:

create_expense
attach_receipt
assign_cost_center
submit_for_approval

The agent can still leave the system in a partially valid state. It may create the expense and attach the receipt, then fail before assigning the cost centre. A retry may create a duplicate. A changed intermediate response may cause the agent to abandon the original plan.

The real abstraction may be:

submit_expense_report

That operation can validate the complete request, enforce idempotency and execute within an owned transaction or durable workflow.

This does not mean that every tool should be broad. It means tool granularity should follow domain semantics rather than the implementation structure of the underlying API.

A useful rule is:

> When several calls collectively represent one business state transition, composition should usually occur behind the capability boundary.

The agent should express intent. Deterministic software should own the transaction.

## Context over-fetching is the opposite failure

The opposite of tool fragmentation is returning too much data.

A generic tool may retrieve an entire issue, customer record, API response or database result even when the agent needs two fields. The model then performs projection, filtering and joining inside its context.

This creates several costs:

- unnecessary tokens;
- irrelevant information competing for attention;
- greater exposure to embedded prompt injection;
- repeated retrieval of the same metadata;
- weaker data minimization;
- hidden client-side query logic.

Large context windows do not make this design free. Capacity and reliable use of capacity are different properties.

The better pattern is a declarative read interface that allows the agent to request only the necessary projection:

query {
  incident(id: "INC-1842") {
    severity
    owningTeam {
      name
      slackChannel
    }
    relatedDeployment {
      version
      status
    }
  }
}

GraphQL is one implementation, not a universal answer. Governed SQL views, OData, semantic-layer APIs, knowledge graphs and typed query languages can provide similar properties.

The key requirements are:

- projection;
- filtering;
- pagination;
- cost limits;
- stable semantic entities;
- field-level authorization;
- server-side joins;
- bounded result sizes.

Reads benefit from expressiveness because users will ask unanticipated questions. Writes require the opposite posture.

## Queries and commands should be asymmetric

A single generic tool model for both retrieval and mutation is structurally weak.

Read operations often need flexible composition. An agent may need to inspect different combinations of records, fields and relationships depending on the question.

Write operations interact with business invariants. They require stronger control over identity, preconditions, effects, retries and approvals.

The resulting architecture should be asymmetric.

### The read path

The read path should expose declarative, bounded queries.

It should support:

- field projection;
- governed filtering;
- stable pagination;
- query-cost estimation;
- semantic entities decoupled from storage schemas;
- data minimization;
- authorization before execution.

### The write path

The write path should expose explicit domain commands.
Examples include:

- approve_refund
- submit_purchase_request
- cancel_order
- grant_temporary_access
- create_production_change

Each command should carry a known contract:

- actor;
- target;
- parameters;
- preconditions;
- expected effects;
- approval requirements;
- idempotency semantics;
- compensation behaviour;
- verification criteria.

The model may propose the command. The platform remains authoritative over its execution.

## MCP solves connectivity, not service design

Model Context Protocol is an important response to integration fragmentation.

Its architecture defines hosts, clients and servers, with servers exposing capabilities such as tools, resources and prompts through standardized protocol messages.[5] This reduces the need to build a custom integration for every combination of AI application and external system.

That is a meaningful infrastructure improvement.

But MCP does not determine whether a capability is cohesive, correctly scoped or transactionally safe.

A badly designed API exposed through MCP remains badly designed. It may simply become easier to connect to more agents.

MCP does not inherently answer:

- Is this tool too narrow?
- Should these five calls become one domain command?
- Is this operation valid at the current workflow state?
- Should the result be joined server-side?
- Is the overall sequence transactionally safe?
- What compensation follows partial failure?
- Does the user have authority over the combined effect?
- How is the final business outcome verified?

These concerns may be implemented in an MCP server, gateway, workflow engine or surrounding platform. They are not resolved merely by adopting the protocol.

This distinction matters because protocol success can accelerate capability sprawl. Once teams can publish integrations easily, the tool catalog can grow faster than the organization's ability to govern its semantics.

MCP solves an integration graph problem:

many clients × many systems

It does not automatically solve the service-complexity problem inside each integration.

## The emergence of the meta-harness

A second type of fragmentation appears above tools.

Coding-agent harnesses such as Claude Code, Codex, Pi and custom SDK agents differ in their:

- session formats;
- prompts;
- model integrations;
- context strategies;
- filesystem assumptions;
- built-in tools;
- execution loops;
- recovery behaviour;
- safety controls.

Organizations increasingly run several harnesses at once. Users copy information between them, maintain separate workspaces and lose session state when moving from one system to another.

Databricks introduced Omnigent in June 2026 as an open-source "meta-harness" that sits above these heterogeneous agents. Databricks describes three main objectives:

- Composition: combine or switch among different models, harnesses and custom agents.
- Control: apply stateful, contextual policies outside model prompts.
- Collaboration: share live sessions, files and agent control with other users.[6]

Omnigent wraps terminal agents and agent SDKs behind a common interface. Databricks describes the shared boundary as messages and files entering the harness, with text streams and tool calls leaving it. The project adds session sharing, multiple user interfaces, hosted sandbox execution, cost policies, contextual security policies, network interception and multi-harness configurations.[6]

The open-source project is currently described as alpha software.[6][7]

Omnigent matters because it gives a concrete shape to an emerging architectural layer: the agent execution control plane.

## What the meta-harness solves

A meta-harness addresses operational fragmentation.

It can provide a common home for:

- session lifecycle;
- runtime selection;
- process supervision;
- workspace attachment;
- event normalization;
- human collaboration;
- sandbox provisioning;
- runtime budgets;
- policy decisions;
- network controls;
- temporary credentials;
- execution telemetry.

This is valuable even when the underlying agents remain different.

For example, a meta-harness can enforce that:

- all coding agents run inside isolated environments;
- agents cannot access production credentials directly;
- network requests pass through an egress policy;
- a human must approve a push after dependency installation;
- session costs cannot exceed a defined budget;
- collaborators can inspect and steer the same live run.

These are difficult concerns to implement independently in every harness.

The meta-harness lifts them into a shared control layer.

## Syntactic portability is not semantic portability

A common runtime API creates syntactic portability.

The platform can normalize:

- starting a session;
- sending a message;
- attaching a workspace;
- reading an output stream;
- cancelling execution;
- capturing tool events;
- sharing session state.

It cannot guarantee that different harnesses will interpret and complete the same task equivalently.

Harnesses differ in:

- system prompts;
- model behaviour;
- context construction;
- history compaction;
- available tools;
- repository discovery;
- error recovery;
- safety defaults.

Changing the harness may change the result even when the external request is identical.

The correct goal is therefore not transparent semantic interchangeability. It is governed heterogeneity.

A serious meta-harness should make these differences measurable through conformance evaluation:

- Did both harnesses obey the same path restrictions?
- Did both preserve the user's requested scope?
- Did either invoke unnecessary tools?
- Were the resulting code changes equivalent?
- Did both preserve the same approval boundary?
- How did cost, latency and recovery differ?
- Did both produce the expected outcome?

A one-line harness switch is operationally useful. It is not evidence of behavioural equivalence.

## What Omnigent does not solve

Omnigent addresses the control-plane problem. It does not remove the underlying service-complexity problem.

A meta-harness does not automatically repair:

- excessively granular tools;
- unclear business capabilities;
- hidden client-side joins;
- long tool-call trajectories;
- missing transactions;
- absent compensation semantics;
- over-broad database access;
- semantically ambiguous commands.

It can supervise an agent that is still operating over a badly designed capability surface.

This is the central relationship between Yegge's critique and Omnigent:

> A meta-harness can govern complexity operationally without eliminating it semantically.

Suppose a coding agent must call twelve internal tools to complete a deployment. Omnigent can isolate the process, record the session, restrict network access and require approval before production mutation.

Those controls are useful.

But if the twelve calls collectively represent one owned business operation, the service surface remains wrong. The durable improvement is to create a coherent deployment capability or workflow behind the boundary.

Operational governance cannot substitute for semantic design.

## The two-layer solution

Enterprise agent systems need both capability architecture and runtime control.

### Layer one: semantic capability architecture

This layer reduces the complexity exposed to the model.

It owns:

- stable domain entities;
- declarative read interfaces;
- cohesive write commands;
- precondition and effect contracts;
- server-side composition;
- transaction boundaries;
- idempotency;
- compensation semantics.

Its question is:

> What meaningful operation is being requested, and under what domain rules may it occur?

### Layer two: meta-harness control plane

This layer governs the agents that execute approved work.

It owns:

- sessions;
- harness adapters;
- workspaces;
- process lifecycle;
- sandboxes;
- runtime policies;
- credentials;
- collaboration;
- event streams;
- cost controls.

Its question is:

> Which runtime should perform the work, and under what operational constraints?

The combined architecture looks like this:

User goal
    ↓
Agent planner
    ↓
Semantic capability layer
    ↓
Typed query or domain command
    ↓
Policy and approval validation
    ↓
Meta-harness control plane
    ↓
Selected harness
    ↓
Sandboxed runner
    ↓
System of record
    ↓
Outcome verification

This separates probabilistic interpretation from deterministic authority.

## The role of a capability compiler

For consequential writes, a domain command alone may not be enough. The platform may need to compile natural-language intent into a typed, non-executable plan before anything runs.

For example:

{
  "operation": "CreateProductionChange",
  "actor": "user-1842",
  "service": "payments-api",
  "target_environment": "production",
  "change_set": "commit:8f97c2",
  "allowed_resources": [
    "deployment/payments-api"
  ],
  "required_checks": [
    "unit-tests",
    "integration-tests",
    "security-scan"
  ],
  "approval_policy": "service-owner",
  "expected_effects": [
    "deployment_created",
    "health_checks_passed"
  ],
  "rollback": {
    "strategy": "previous_revision"
  }
}

The plan can be evaluated before execution:

- Is the actor authorized?
- Does the commit belong to the approved repository?
- Did the required checks pass?
- Is the target environment allowed?
- Does the operation require additional approval?
- Is rollback available?
- What exact effect is being authorized?

The model proposes the plan. A deterministic system validates it.

The meta-harness then executes the approved plan through an appropriate runtime.

This is the division of labour:

> The capability compiler determines what may happen. The meta-harness governs how and where it happens.

## Policy must exist at multiple boundaries

Agent governance is not one policy check.

At least four policy layers are needed.

### Semantic policy

- Is the requested business operation allowed?
- Are its preconditions satisfied?
- Is the resource in scope?
- Does it require approval?

### Runtime policy

- Which files may be accessed?
- Which commands may run?
- Which network destinations are permitted?
- What budget may the session consume?

### Transaction policy

- Is the operation idempotent?
- Can it be retried safely?
- How is partial failure compensated?
- How long may an approval remain valid?

### Verification policy

- Did the system reach the approved state?
- Were only approved resources modified?
- Did the tests and health checks pass?
- Does observed output match expected effects?

Prompt instructions are insufficient for these controls. They may guide model behaviour, but they are not authoritative enforcement boundaries.

## Credentials are capabilities

Omnigent's network-interception model illustrates another important distinction.

Databricks describes an OS sandbox capable of intercepting and transforming network requests, allowing a credential such as a GitHub token to be injected through an egress proxy rather than exposed directly to the agent process.[6]

This reduces secret-exfiltration risk.

But hiding the token does not eliminate the authority represented by the token. An agent may still attempt to cause an approved proxy to send a harmful authenticated request.

The platform must validate more than the destination. It should validate the complete delegated capability:

- actor;
- operation;
- resource;
- request parameters;
- credential scope;
- approval;
- expiration;
- session;
- expected effect.

For high-risk operations, approval should be bound to the exact plan rather than granted broadly to the tool or session.

Conceptually:

approval_token =
sign(
    actor
    + operation
    + resource_scope
    + parameters
    + expected_effects
    + expiry
)

A material change should invalidate the authorization.

This moves approval from "the user clicked continue" to a verifiable execution contract.

## Durable execution remains a separate concern

A live agent session is not the same as a durable workflow.

Meta-harnesses can preserve conversation history, workspaces and process state. But long-running business operations need stronger guarantees:

- authoritative execution history;
- retries;
- timers;
- recovery after worker failure;
- idempotent activities;
- versioned workflows;
- compensation;
- long-lived human approvals.

Temporal's sandbox orchestration pattern explicitly separates durable workflow state from ephemeral sandbox execution. The workflow engine owns the reliable history, while the sandbox performs potentially unsafe or model-generated computation.[8]

This distinction prevents the agent process from becoming the authoritative source of business state.

The complete platform may therefore involve:

- MCP for capability transport;
- a semantic capability layer;
- a capability compiler;
- a meta-harness;
- sandbox infrastructure;
- a durable workflow engine;
- independent outcome verification.

These are not necessarily separate products. They are separate architectural responsibilities.

## A practical design test

Before exposing a new agent tool, a platform team should ask:

1. Does this tool represent a coherent domain capability or an implementation detail?
2. Will an agent need several related calls to complete one state transition?
3. Can projection, filtering or joining occur server-side?
4. Is the operation a query or a command?
5. Are preconditions and expected effects explicit?
6. Can the operation be retried safely?
7. What happens after partial failure?
8. Which identity and authorization apply?
9. What evidence proves completion?
10. Does the model need to see this tool at the current workflow state?

These questions are more important than whether the tool schema is concise or whether it can be published through MCP.

## An applied research programme

A useful reference implementation would test the combined architecture on one bounded workflow.

For example:

> Implement an approved Jira issue in a Git repository and create a pull request.

The semantic layer would expose:

- issue queries;
- repository queries;
- ProposeCodeChange;
- ExecuteApprovedChange;
- CreatePullRequest.

The capability compiler would produce a typed plan containing:

- issue identifier;
- repository;
- allowed paths;
- expected files;
- test requirements;
- prohibited operations;
- approval policy;
- expected outcome.

The meta-harness would:

- select between two coding-agent harnesses;
- create isolated worktrees;
- inject only approved context;
- restrict filesystem and network access;
- capture normalized execution events;
- manage credentials;
- pause for approval.

A durable workflow would:

- provision the sandbox;
- run the harness;
- execute tests;
- request review;
- create the pull request;
- verify the resulting state;
- recover after interruption.

The evaluation would measure:

- success rate;
- unauthorized action attempts;
- tool calls per task;
- token cost;
- latency;
- recovery after sandbox failure;
- semantic differences between harnesses;
- policy compliance;
- outcome correctness.

This would test a more important question than whether an agent can complete the demo:

> Which guarantees remain stable when the model, harness or execution environment changes?

## Conclusion

Agent systems are repeating the service complexity crisis because platforms are exposing implementation-level operations and expecting models to reconstruct coherent workflows at runtime.

MCP improves connectivity, but connectivity is not abstraction. A standardized interface can still expose the wrong capabilities.

Meta-harnesses such as Databricks Omnigent address a second problem: the fragmentation of agent runtimes, sessions, policies, workspaces and execution environments. They provide an emerging operational control plane above heterogeneous harnesses.

But runtime coordination is not a substitute for service design.

The durable architecture needs both:

- a semantic capability layer that exposes declarative reads and cohesive, policy-bound commands;
- a meta-harness control plane that governs which agent executes the work and under what operational constraints.

Yegge's service lesson therefore remains relevant in the agent era:

> Do not export complexity merely because you can expose it through an interface.

The goal is not to give agents every available operation. It is to design a capability surface that preserves flexibility while keeping business semantics, transactions, policy and recovery inside deterministic system boundaries.

Models should interpret goals.

Platforms should own execution.

## References

1. Steve Yegge. "Services and Complexity." Yegge.ai.
   https://yegge.ai/listings/services-and-complexity

2. Steve Yegge. "Stevey's Google Platforms Rant." 2011. Archived copy.
   https://gist.github.com/chitchcock/1281611

3. Vyzantinos Repantis, Ameya Gawde, Harshvardhan Singh and Joey Blackwell. "How Many Tools Should an LLM Agent See? A Chance-Corrected Answer." arXiv, 2026.
   https://arxiv.org/abs/2605.24660

4. Rahul Suresh Babu and Laxmipriya Ganesh Iyer. "ToolChoiceConfusion: Causal Minimal Tool Filtering for Reliable LLM Agents." arXiv, 2026.
   https://arxiv.org/abs/2606.06284

5. Model Context Protocol. "Architecture." MCP Specification.
   https://modelcontextprotocol.io/specification/2025-06-18/architecture

6. Matei Zaharia, Kasey Uhlenhuth and Corey Zumar. "Introducing Omnigent: A Meta-Harness to Combine, Control and Share Your Agents." Databricks, June 13, 2026.
   https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents

7. Omnigent. "A Meta-Harness for All Your AI Agents." GitHub repository.
   https://github.com/omnigent-ai/omnigent

8. Temporal. "Temporal Sandbox Orchestration Harness: The Missing Layer for Running Agents." 2026.
   https://temporal.io/blog/temporal-sandbox-orchestration-harness-the-missing-layer-for-running-agents

9. Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab and Chelsea Finn. "Meta-Harness: End-to-End Optimization of Model Harnesses." arXiv, 2026.
   https://arxiv.org/abs/2603.28052

10. Apollo GraphQL. "Connect AI Agents to Your GraphQL API Using MCP and Type-Safe Tool Configuration."
    https://www.apollographql.com/blog/connect-ai-agents-to-your-graphql-api-using-mcp-and-type-safe-tool-configuration

11. Berkeley Function Calling Leaderboard. Gorilla LLM.
    https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html

12. Temporal. "From Agent Zoo to Agent Orchestra: The Benefits of Temporal as Your Enterprise Agentic Control Plane."
    https://temporal.io/blog/from-agent-zoo-to-agent-orchestra-temporal-agentic-control-plane
