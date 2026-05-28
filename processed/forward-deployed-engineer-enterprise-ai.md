# The Forward Deployed Engineer in Enterprise AI: From Integration Specialist to Agentic Control-Plane Builder

Enterprise AI does not fail because language models cannot produce impressive answers. It fails when organizations cannot safely connect model capability to permissions, policies, approvals, systems of record and measurable outcomes. The Forward Deployed Engineer is emerging as the engineer who closes that gap — but the role creates durable value only when local deployment work becomes reusable agent infrastructure.

Enterprise AI is reaching the point where the demo is no longer the difficult part.

A model can summarise a contract, classify a request, search a knowledge base, draft a Jira update or propose a Slack workflow in minutes. The difficult part begins when an organization asks the system to participate in real work: to access governed data, reason according to institutional definitions, act under delegated authority, request approval, execute changes, retain evidence and remain accountable when something goes wrong.

That is why the Forward Deployed Engineer, or FDE, is becoming structurally important in enterprise AI.

The role is often described as an engineer embedded with customers or business teams to deploy AI systems in practice. That description is accurate but incomplete. In the agent era, the strongest FDE is not merely an integration specialist or a technically sophisticated consultant. The FDE is increasingly a builder of the control plane that turns probabilistic model capability into governed operational execution.

This shift matters because models alone do not perform enterprise work. Governed systems do.

## Why Enterprise AI Stalls After the Demonstration

The first wave of enterprise generative AI was dominated by conversational assistance: chat interfaces, document summarisation, internal search and productivity copilots. These systems created genuine value, but they largely remained advisory. A user asked a question; the system returned an answer; the human retained responsibility for deciding and acting.

Agentic workflows change the unit of deployment.

An agent may retrieve information across multiple systems, interpret policy, produce a structured recommendation, invoke tools, create or modify records, request approval, monitor execution and update downstream state. Once AI begins to participate in operational workflows, the relevant questions change.

The enterprise no longer asks only:
Can this model produce a useful answer?

It must also ask:
What data may the agent access?
Under whose authority is it operating?
Which actions may it recommend, propose or execute?
Which policies and business definitions constrain its reasoning?
Which actions require human approval?
What evidence must be retained?
How is quality measured across thousands of executions?
Who owns the failure when an AI-mediated action is wrong?

This is the gap behind Aaron Levie's warning about executive "AI psychosis": leadership can experience an impressive happy-path demonstration while remaining insulated from the integration, exception handling, access-control and governance work required to make the system dependable in production.[1]

The obstacle is not primarily organizational resistance to AI. It is the distance between model capability and institutional operability.

A production agent typically faces five constraints at once.

First, enterprise meaning is fragmented. A term such as "active customer," "material contract change," "approved supplier," "account owner" or "privileged access" may be defined differently across documents, dashboards, systems and teams.

Second, identity and authorization are difficult. Enterprise permissions were designed for human users and conventional applications, not reasoning systems that act conditionally, through tools, on behalf of users.

Third, agent behavior is non-deterministic. Output quality depends on retrieved context, tool state, model version, orchestration decisions, available permissions and changing business conditions.

Fourth, economics are unpredictable. Cost includes more than inference: tool calls, retries, sandbox runtime, human review, trace retention, failures and remediation all contribute to the actual cost of production operation.

Fifth, accountability is fragmented. Platform teams, vendors, security, compliance, operational owners and application teams may each own one layer of the workflow while nobody owns the full outcome.

These constraints cannot be resolved by selecting a stronger model endpoint. They must be resolved inside the workflow itself.

That is the terrain of the Forward Deployed Engineer.

## From Embedded Data Integration to Embedded Agent Operations

The FDE model is most strongly associated with Palantir, which developed an engineering approach based on embedding technical teams close to operational environments where data was fragmented, terminology was local, access was constrained and value depended on deeply understanding how decisions were actually made.

The critical characteristic of the model was not simply proximity to the customer. It was the intended feedback loop:

Local friction → embedded engineering discovery → working deployment → reusable abstraction → improved platform capability

A useful FDE organization does not merely solve an individual deployment. It identifies repeated problems and converts them into platform components, schemas, policy models, deployment methods and reusable product capabilities.

This becomes even more important with enterprise agents.

Earlier generations of embedded engineers connected fragmented data to applications and decision makers. AI-era FDEs increasingly connect reasoning systems to governed organizational action.

Market signals now support this shift. In November 2025, the Financial Times reported that job listings for forward deployed engineers had grown by more than 800 percent between January and September 2025, as companies including OpenAI, Anthropic and Cohere expanded roles focused on deploying AI directly into customer environments.[2]

In May 2026, OpenAI launched the OpenAI Deployment Company, explicitly describing its mission as helping businesses build and deploy AI systems they can rely on in important work. The company stated that successful AI deployment requires integrating systems into the infrastructure and workflows that power organizations, and it acquired Tomoro to bring experienced Forward Deployed Engineers into the new company from day one.[3]

OpenAI's own FDE job descriptions make the intended compounding mechanism explicit: engineers are expected not only to ship deployments, but to codify working patterns into reusable tools, playbooks and building blocks, while feeding real-world signals back into product and research teams.[4]

The Palantir analogy, however, should not be overextended. Palantir developed its approach through years of expensive, deeply integrated deployments and a platform built around operational ontology and governed action. Renaming implementation consultants as "FDEs" does not automatically recreate the same leverage.

The value of the role depends on whether field engineering compounds.

## Three FDE Models Are Emerging

The term Forward Deployed Engineer is now applied to several different organizational functions. They should be distinguished because they have different incentives, strengths and failure modes.

### Vendor FDE: Deploying a Product Into Customer Reality

A vendor FDE works inside customer environments to deploy the vendor's models, applications or agent infrastructure. Their job is to identify valuable workflows, integrate customer systems, build production deployments and transmit recurring implementation patterns back into the vendor platform.

This model is rational when each customer relationship is economically significant and deployment requires extensive adaptation to local systems and processes.

The risk is familiar: customer-facing engineering becomes unbounded custom work. The vendor may win individual deployments while accumulating a services business disguised as a software platform.

### Consulting FDE: Coordinating Transformation Across Systems

A consulting or systems-integration FDE helps enterprises orchestrate multiple vendors, legacy systems, data platforms, access models, compliance requirements and redesigned business processes.

This role can be valuable in large organizations where deploying AI requires cross-functional coordination beyond any single product.

Its weakness is incentive alignment. A consulting organization may be rewarded for extending the transformation programme rather than simplifying the customer's operating architecture. Without deliberate internal capability transfer, the enterprise may end up dependent on external deployment capacity.

### Internal FDE: Building Institutional Capability

The internal FDE is the most strategically interesting model for enterprises that expect agents to participate in important business workflows.

An internal FDE works close to operational teams but builds on shared internal foundations: identity, tool gateways, evaluation infrastructure, policy controls, audit systems and knowledge layers.

This role is not equivalent to assigning an "AI engineer" to Legal, Finance or Sales Operations. A mature internal FDE converts local workflow knowledge into controlled, reusable capabilities.

For example, an internal FDE may:
model an approval-gated SaaS write workflow;
connect an agent to enterprise search, policy repositories and ticketing systems;
distinguish read, propose-write and execute-write permissions;
implement policy checks and approval flows;
build representative evaluation datasets from workflow cases;
measure cost, latency, override rate and failure frequency;
feed reusable requirements back into a central agent platform.

This creates a bridge between local operational reality and institutional engineering leverage.

## What an AI FDE Actually Builds

The strongest version of the FDE role is not centred on prompting. It is centred on translating business work into governed agent execution.

### 1. A Concrete Workflow Contract

The first task is not choosing a model. It is defining what work is actually being improved.

Consider a bounded example: approval-gated write operations in enterprise SaaS applications such as Jira, Slack or Confluence.

An employee asks an agent to modify a record: create a Slack channel, update a Jira issue, change a workflow status, edit a Confluence policy page or assign an operational request.

A weak deployment starts with a chat prompt: "Help users update Jira using AI."

A strong deployment begins with an operational contract:

> Given a user request to create or modify a SaaS record, the system retrieves relevant context and policy, generates a structured proposed change with supporting evidence, determines whether approval is required, executes only within delegated authority, verifies the resulting state and records a durable audit trace.

That formulation identifies the real engineering problem. It specifies:
the initiating actor;
the business object being changed;
relevant evidence sources;
permitted forms of reasoning;
applicable policies;
approval boundaries;
tool interactions;
irreversible actions;
outcome definitions;
rollback or remediation paths;
audit requirements.

Without this decomposition, organizations automate vague aspirations such as "make support faster" or "use agents for operations." Such goals are impossible to govern, evaluate or finance rigorously.

### 2. A Semantic and Knowledge Layer

Retrieval alone is insufficient when an agent must act according to authoritative operational meaning.

An agent may retrieve a page mentioning "approved owner," but it still needs to know what qualifies as approval, which system holds the authoritative record, whether the policy is still valid, which business entity is affected and which action is permissible under that interpretation.

For approval-gated SaaS writes, even a minimal operational knowledge layer needs concepts such as:

| Concept | Operational purpose |
|---------|-------------------|
| Actor | Human, service or agent initiating work |
| Role | Authority held within a business context |
| Action | Read, propose, approve, execute or reverse |
| Tool | Interface through which an action is performed |
| Policy | Constraint governing the action |
| Approval | Explicit authorization for a controlled operation |
| Evidence | Material supporting the proposal |
| Execution | The actual write made to a system |
| Outcome | Verified result and business consequence |
| Audit Record | Durable account of what happened and why |

This is not knowledge-graph theatre. It is a method of separating what is plausible from what is permitted.

Palantir expresses this as a decision-centric ontology: an operational model in which actions can be staged, governed through access controls and written back into enterprise systems under explicit control.[5] The broader lesson is not that every enterprise should reproduce Palantir's platform. It is that agents need more than documents and embeddings when they participate in decisions and actions.

An operational agent requires a governed model of entities, relationships, policy, authority, evidence and consequences.

### 3. Identity, Delegation and Least-Privilege Execution

Once agents can invoke tools, enterprise identity becomes considerably harder.

A human initiates a request. An agent interprets it. A tool server exposes operations. An executor writes to a downstream system. Another human may approve the action. Each boundary changes what authorization means.

A production system must distinguish among:
user identity;
agent identity;
delegated authority;
tool identity;
downstream credential;
approval authority;
execution authority.

Suppose an employee requests an update to a Jira issue. The agent may be allowed to read the issue, retrieve the applicable workflow policy and prepare a proposed modification. It should not automatically inherit the full interactive privileges of the human user.

Instead, the architecture should distinguish:
Read authority: inspect relevant records and supporting policy.
Proposal authority: generate a structured intended change, with evidence and justification.
Approval authority: allow a qualified human or policy engine to authorize controlled execution.
Execution authority: issue a narrow, auditable write to the target system.

This separation matters because autonomous delegation is not identical to human access. A user may possess broad permissions because they are expected to apply judgment continuously. An agent executing at scale should receive narrower authority, stricter constraints and better traces.

This is increasingly visible in platform architecture. Google's Gemini Enterprise Agent Platform presents Agent Identity, Agent Gateway and Agent Observability as foundational governance capabilities for enterprise agents.[6] The Model Context Protocol authorization specification formalises OAuth-based authorization for remote tool servers, providing important primitives for protected tool access.[7]

Yet protocols alone do not decide which actions should be exposed, when approval is mandatory or how delegated authority should be constrained. Those questions are workflow-specific. They are precisely the kind of questions an embedded FDE encounters in production.

### 4. Human-Gated Write Operations

The most important architectural boundary in enterprise agents is the difference between reading information and changing systems.

Many enterprise experiments implicitly treat tool access as binary: either the agent can use a system or it cannot. In practice, controlled autonomy needs a more precise progression:

Read → Analyse → Propose Write → Validate Policy → Request Approval → Execute Narrow Action → Verify Result → Record Outcome

This sequence allows organizations to automate aggressively in low-risk areas while preserving deliberate friction around material operations.

Return to the SaaS write example.

An employee requests a new Slack channel for a project involving customer information. The agent can:
interpret the request;
retrieve channel-naming policy, data-handling policy and relevant project context;
produce a structured proposed channel configuration;
identify that the action requires approval because external collaboration or sensitive information may be involved;
route the proposal to an approver;
execute the approved action through a controlled service;
verify that the correct configuration was created;
record requester, evidence, policy evaluation, approval, execution response and resulting state.

The FDE's contribution is not merely wiring together a workflow engine and an API. It is deciding:
which actions require approval;
what evidence an approver must see;
which operations should be reversible;
how the system records authority and execution;
which low-risk actions might later become automatically executable;
how the organization proves that controlled actions remained within policy.

This turns human review from an afterthought into part of the architecture.

### 5. Evaluation and Observability

Agent deployments cannot be evaluated through anecdotal success.

A system may perform well on ten curated demonstrations and still fail systematically when policies change, permissions differ, retrieved context is incomplete, tool arguments are malformed or users describe the same task in unfamiliar language.

A production-grade FDE therefore builds evaluation and observability into the workflow from the beginning.

For an approval-gated SaaS write workflow, the evaluation suite should include scenarios such as:
permitted read-only requests;
valid proposed writes;
writes requiring approval;
writes that policy must deny;
requests with insufficient evidence;
malformed or ambiguous user requests;
expired approval attempts;
execution failures;
duplicate requests;
attempts to exceed delegated authority;
post-execution verification failures;
requests involving conflicting policies.

Evaluation should measure more than whether the final text "looks right."

| Dimension | Example measure |
|-----------|----------------|
| Task success | Correctly completed, escalated or refused workflow |
| Grounding | Proposal supported by authoritative evidence |
| Authorization | No action outside delegated authority |
| Approval discipline | Controlled writes never bypass approval |
| Tool correctness | Correct tool, arguments and sequencing |
| Reliability | Retry, timeout and recovery rate |
| Efficiency | Cost and latency per successful outcome |
| Human impact | Approval burden, override rate and trust |
| Auditability | Complete evidence-to-outcome trace |

OpenAI's macro-evaluation work for agentic systems is significant here because it shifts attention from individual outputs to behaviour across populations of traces: systemic handoff errors, review bottlenecks, repeated specialist failures and operational patterns that only emerge across many runs.[8]

The FDE sits in the loop that turns these failures into engineering assets:

Production failure → diagnosis → evaluation scenario → policy or platform improvement → safer subsequent deployment

That loop is where embedded deployment work begins to compound.

## The Missing Layer: An Agentic Control Plane

Enterprise discussion often frames FDEs as solving integration problems. In the agent era, the deeper architectural requirement is a control plane for governed execution.

Skills may package repeatable model expertise. Tools may expose APIs. Workflows may coordinate actions. But dependable enterprise autonomy emerges only when these components are bound to identity, policy, evidence, approval, state, cost and outcome measurement.

A useful control-plane model has six layers:

| Layer | Core responsibility |
|-------|-------------------|
| Business outcome layer | Task success, cycle time, risk reduction, review effort |
| Workflow and evaluation layer | State machines, approvals, traces, evals, escalation rules |
| Policy and identity layer | User delegation, agent identity, scopes, authorization and audit |
| Semantic and knowledge layer | Entities, definitions, evidence, policies and provenance |
| Tool and integration layer | MCP tools, APIs, SaaS applications and execution gateways |
| Model and runtime layer | Model routing, context assembly, sandboxing and budgets |

The FDE operates vertically through this stack.

A model engineer may improve reasoning performance. A platform engineer may build an agent gateway. A security engineer may design authorization controls. A business analyst may document workflow rules. A product owner may define the desired outcome.

The distinctive responsibility of the FDE is to make these layers resolve into a working operational system in a real business environment.

This is why internal FDE work is particularly relevant to enterprise applications, finance operations, support operations, legal operations and other functions where agent value depends on connecting messy institutional reality to controlled execution.

## Token Economics: Cost per Controlled Outcome

Enterprise AI spending is often discussed in terms of token consumption. That is necessary but insufficient.

Inference costs may decline per unit while total AI expenditure rises because organizations run more workflows, provide more context, invoke more tools, store more traces, perform more verification and require more human review.

For an agentic workflow, the meaningful economic object is not token spend alone. It is the cost of producing a trustworthy operational outcome.

A simplified model is:

Total workflow cost = model inference + retrieval and data processing + tool execution + runtime and sandboxing + observability and audit retention + human review + failure remediation + compliance overhead

This changes optimization strategy.

A cheap model that produces poorly grounded proposals requiring repeated human correction may be more expensive than a more capable model whose outputs are consistently approved and executed successfully.

Conversely, using the most expensive model for every classification, retrieval decision, routing operation and policy check may waste budget without improving business outcomes.

An FDE responsible for production workflows should therefore establish:
cost attribution per workflow and business owner;
model-routing policies by task type and risk level;
execution budgets and maximum loop limits;
approval-cost measurement;
retry and remediation tracking;
experiment-versus-production budget separation;
evaluation-linked cost reporting.

The FinOps Foundation now frames AI cost management in terms of faster development cycles, spend unpredictability, policy, governance, forecasting and alignment between consumption and business value.[9] That framing becomes more important as agents begin to incur costs across entire workflows rather than individual model calls.

The relevant management question is not:
How do we minimize tokens?

It is:
What is the least expensive architecture that reliably produces an approved, auditable and useful business outcome?

That is a far harder question. It is also the correct one.

## Headless Enterprise Software: Agents Operate, Humans Govern

Agentic workflows increase the importance of software that can be operated reliably through APIs, tool contracts and machine-readable policies. This is the substance behind the emerging idea of the "headless enterprise."

But headless should not be misunderstood as humanless.

For high-impact workflows, enterprise software is likely to expose two coordinated interfaces:

| Interface | Primary user | Purpose |
|-----------|-------------|---------|
| Execution interface | Agent or controlled automation service | Query, propose, write, verify and retry |
| Oversight interface | Human approver, operator or auditor | Review, approve, inspect, override and reverse |

Consider a contract-analysis workflow. Agents may retrieve agreements, classify clauses, identify policy deviations and draft risk assessments in the background. But legal users still need to inspect evidence, understand which policy definitions were applied, accept or reject recommendations and review the resulting audit history.

Likewise, an internal operations agent may prepare a Jira workflow change or propose an access modification. Humans do not need to perform every low-level lookup and formatting step, but they may still need to govern consequential decisions.

Future-proof enterprise systems therefore require more than APIs. They need:
narrow, typed operations rather than broad write access;
stable tool semantics;
machine-readable schemas;
identity-aware authorization;
policy hooks;
approval workflows;
event histories and provenance;
reversible actions where feasible;
verified outcome reporting.

FDEs become valuable because they encounter the difference between an application that technically exposes an API and an application that can participate safely in agent-mediated work.

## The Central Risk: FDEs Can Create Leverage or Technical Debt

The FDE model has an obvious failure mode: expensive bespoke implementation that never becomes reusable capability.

A weak FDE organization behaves like this:
every customer or business unit receives custom code;
workflow knowledge remains trapped in individuals;
integrations bypass shared controls;
security exceptions accumulate;
evaluation practices vary by deployment;
the platform does not improve;
business teams remain dependent on field engineers for routine operation.

This model may produce impressive demonstrations and short-term adoption. It does not create durable leverage.

A strong FDE organization behaves differently:
repeated workflow patterns are identified and documented;
integrations are routed through shared gateways and identity models;
local failures become shared regression tests;
working deployments produce templates and reusable components;
policy decisions are codified rather than remembered informally;
cost and outcome metrics are standardized;
business units can operate deployed systems without permanent rescue.

This produces the decisive rule for enterprise AI deployment:

> Forward deployed engineering is strategically valuable only when local deployment work is converted into reusable institutional capability.

For an AI vendor, that means improving the product platform.

For an enterprise, it means strengthening the internal agent control plane: its identity model, tool gateway, semantic layer, policy framework, approval patterns, evaluation infrastructure and operational standards.

Without this conversion mechanism, the FDE becomes a premium implementation consultant.

With it, the FDE becomes the sensor and builder through which the organization learns how to deploy agents safely at scale.

## The Internal FDE as an Enterprise Capability Builder

For large enterprises, the internal FDE is a credible operating model, particularly where workflows cross systems, involve approvals, contain regulatory or customer risk and recur across multiple business areas.

The role should not be created as an undefined "AI transformation" position. It should own bounded workflow outcomes.

Examples include:
reducing employee-support resolution time while preserving escalation quality;
safely automating proposals for controlled SaaS changes;
improving document-analysis turnaround while retaining evidence;
reducing manual investigation work without increasing erroneous decisions;
deploying business-unit agents on shared authorization, observability and approval infrastructure.

A mature organizational pattern might look like this:

**Central Agent Platform Team**
agent identity and delegated authorization;
tool gateway and execution runtime;
shared observability and audit;
policy framework;
evaluation infrastructure;
model routing and cost controls.

**Embedded Internal FDEs**
finance operations workflows;
legal and compliance workflows;
enterprise applications workflows;
employee-support workflows;
sales and customer-operations workflows.

The platform team prevents duplication and uncontrolled risk. The embedded FDEs prevent the platform from becoming elegant infrastructure that does not fit real work.

Neither is sufficient alone.

## When an FDE Function Is Justified

Not every enterprise AI project needs an embedded engineering model.

An FDE function becomes justified when several conditions are present:
The workflow crosses multiple systems of record.
Access control, approval and auditability matter.
Business meaning cannot be recovered reliably from raw documents alone.
The agent may initiate operational changes rather than only return text.
Failure carries financial, regulatory, customer-facing or reputational consequences.
Similar workflows are expected to recur across teams.
Central platform teams are too distant from users to observe real failure modes.
Vendor prototypes are not becoming internally owned production systems.

An FDE is less justified for a bounded assistant over low-risk documents, an isolated summarisation workflow or an experiment whose outputs remain purely advisory and easily checked by humans.

The decision should be based on operational complexity and repeatability, not on AI enthusiasm.

## What Organizations Commonly Get Wrong

1. **Treating the FDE as a Prompt Specialist** — Prompting is useful, but it is not the hard part of production agent deployment. Systems fail through missing authorization boundaries, unstable business definitions, incomplete evaluation, poorly designed approvals and unclear ownership of outcomes.

2. **Automating Before Defining the Workflow** — A model demo is not an operational specification. Before execution begins, the enterprise must define actors, actions, evidence, policies, approval boundaries, success criteria and failure recovery.

3. **Giving Agents Broad Access Because Humans Already Have It** — A person's application permissions do not automatically become appropriate agent permissions. Agents require narrow scopes, explicit delegation, controlled execution and durable traces.

4. **Measuring Tokens Instead of Outcomes** — Low inference cost is irrelevant when the workflow creates expensive correction, approval burden, incidents or compliance exposure. Cost must be evaluated against successful, approved and auditable outcomes.

5. **Assuming Custom Work Automatically Becomes Platform Capability** — It does not. Without deliberate extraction of reusable schemas, tool contracts, policy patterns, evaluations and runtime controls, field engineering becomes accumulated technical debt.

6. **Confusing Headless With Humanless** — For important workflows, the correct shift is not removing people. It is moving people from manually performing every step to governing evidence-backed automated execution.

## A Practical Evolution Path

The transition from AI assistance to governed agent operations should be staged.

**Phase 1: Bounded Read and Analysis**
Select a narrow workflow. Restrict the agent to retrieval, analysis and structured recommendations. Require source attribution and human verification. Capture representative cases and common failures.

**Phase 2: Proposal-Based Actions**
Introduce structured proposed writes without direct execution. Define policy distinctions between read, propose and execute. Add approval queues. Capture trace, latency and cost data.

**Phase 3: Controlled Execution**
Introduce agent identity and delegated authorization. Execute approved actions only through controlled services or gateways. Record evidence, policy decisions, approvals, tool responses and resulting state. Require regression evaluation before model or workflow changes.

**Phase 4: Reusable Platform Capability**
Generalize tool contracts, approval patterns, policy schemas, evidence models and audit structures. Provide shared observability and evaluation infrastructure. Deploy internal FDEs against a common platform rather than allowing each team to build an isolated agent stack.

**Phase 5: Selective Autonomy**
Allow automatic execution only for actions whose low-risk status has been demonstrated through evidence. Keep high-impact operations approval-gated. Monitor overrides, incidents, drift and cost per outcome. Use production evidence to update policies and evaluations continuously.

The trigger for progressing through these phases should not be executive enthusiasm or a new benchmark result. It should be evidence that the previous phase operates reliably under real organizational constraints.

## Open Questions for Enterprise Agent Engineering

The FDE model addresses a real deployment gap, but several questions remain unresolved.

How much embedded work should become platform work? Productising too little creates dependency and debt; abstracting too early can prevent engineers from understanding the workflow deeply enough to build the right platform.

Where should internal FDEs sit organizationally? Enterprise applications, business enablement, central IT, data platforms, security and dedicated agent-platform organizations each offer different advantages and incentives.

How should agent outcomes be valued? Productivity gains may appear as avoided work, faster decisions, fewer escalations, reduced risk or new operational capacity rather than simple headcount savings.

How should liability be distributed? When a vendor provides the model, an enterprise configures the tools, an employee approves an action and a controlled executor performs it, responsibility for failure becomes difficult to assign.

Which forms of autonomy are economically and socially acceptable? Approval-gated systems impose latency and review cost; fully autonomous systems may appear efficient until a rare failure creates disproportionate harm.

Can forward deployment scale without reproducing consulting economics? The model compounds only when recurring deployment work becomes reusable platform capability.

These are not abstract research questions. They determine whether enterprise agents become dependable infrastructure or merely a new category of difficult-to-govern automation.

## Conclusion: From Impressive Agents to Governed Systems

The Forward Deployed Engineer should not be understood as a temporary implementation role created by AI hype. Nor should every enterprise respond by embedding large numbers of expensive engineers in business units.

The role is better understood as a response to an architectural fact: models do not perform enterprise work on their own. They require identity, authority, semantic grounding, policy, approval, tools, evidence, evaluation, observability and economic accountability.

As AI moves from answering questions to participating in workflows, these surrounding systems become decisive. The FDE matters because this engineer works at the boundary where abstract platform capability meets actual institutional constraint.

The strategic objective is therefore not to maximize FDE headcount. It is to build a learning system in which field engineering converts operational friction into reusable agent infrastructure.

Enterprises that achieve this will move beyond scattered prototypes toward controlled, measurable and selectively autonomous workflows.

Those that do not will accumulate impressive demonstrations, expensive integrations and fragile automation — systems capable of generating answers, but not of earning authority.

## References

[1] Aaron Levie and Matt Turck, State of Enterprise AI 2026: Tokenmaxxing, Rise of Headless, and AI-Proofing Your Job, The MAD Podcast, 2026.

[2] Cristina Criddle, The New Hot Job in AI: Forward-Deployed Engineers, Financial Times, 1 November 2025.

[3] OpenAI, OpenAI Launches the OpenAI Deployment Company to Help Businesses Build Around Intelligence, 11 May 2026.

[4] OpenAI Careers, Forward Deployed Engineer and Technical Deployment Lead, Forward Deployed Engineering, 2026.

[5] Palantir, Connecting Agents to Decisions, 28 April 2026; Palantir, Deploying Full Spectrum AI in Days: How AIP Bootcamps Work, 2023.

[6] Google Cloud, Introducing Gemini Enterprise Agent Platform, April 2026; Google Cloud, Gemini Enterprise Agent Platform Release Notes, April 2026.

[7] Model Context Protocol, Authorization Specification, 25 November 2025; Model Context Protocol, Understanding Authorization in MCP, 2025–2026.

[8] OpenAI Developers Cookbook, Macro Evals for Agentic Systems, 19 May 2026.

[9] FinOps Foundation, FinOps for AI Overview and Cost Estimation of AI Workloads, 2025–2026.

[10] OWASP GenAI Security Project, OWASP Top 10 for Agentic Applications for 2026, December 2025.

[11] NIST, Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile, NIST AI 600-1, July 2024.
