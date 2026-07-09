# Workflow-Centered Agent Deployment: What Uber's Agentic Pods Reveal About Enterprise AI Adoption

The next phase of enterprise AI adoption is not just better copilots, faster code completion, or more permissive access to frontier models. It is the redesign of work itself around agents, tools, controls, and reusable workflow artifacts. Uber's recent description of "Agentic Pods" is useful because it makes this shift concrete: AI-proficient engineers are embedded with domain experts, observe how work actually happens, build agents against real systems, validate those agents with the people doing the job, and then ship them into production workflows. Andy Berman's response from Runlayer is equally revealing because it shows the vendor-side version of the same operating model: pair an FDE with an internal AI champion, map existing AI/MCP usage, build agents live, make good workflows reusable, optimize runs, and progressively turn on governance.

This matters because most enterprise AI programs still confuse access with adoption. Giving employees Claude, ChatGPT, Gemini, Cursor, or Codex may improve individual productivity, but it does not automatically transform operations. The harder problem is converting tacit work into reliable, governed, reusable workflows.

## The facts: Uber's internal model and Runlayer's externalized version

Uber CTO Praveen Neppalli described an internal model called Agentic Pods, intended to bring agentic AI beyond engineering into functions like finance, legal, operations, marketing, customer support, HR, and procurement. In the post, he says that 99% of Uber engineers use AI tools, more than 70% of pull requests are attributed to local or cloud agents, and Uber engineers have built more than 2,500 agent skills across the software development lifecycle. Those are self-reported company figures, but they indicate a meaningful internal shift: Uber is no longer treating AI as a side tool for engineers; it is treating agentic AI as an operating capability.

The Agentic Pod structure is simple. Uber selected roughly 30 highly AI-proficient engineers with deep internal systems knowledge and paired each with a domain expert from a business function. Each pod had two weeks. The cycle was: shadow the expert, understand every step, document the workflow, prioritize opportunities by scale and business impact, build a working agent beside the person doing the job, validate it with other people doing similar work, and ship.

The claimed results are the kind of numbers that make this model worth examining: capital allocation across 150 cities reduced from 15 hours to 30 minutes, financial pacing reports reduced from two days to ten minutes, marketing web QA reduced from two weeks to 50 minutes, and support workflow creation moved from thousands of manual workflows toward self-service automation. Business Insider independently summarized the same claims and reported that Uber has run 16 Agentic Pods across 16 business functions while planning to form a dedicated team to scale the model further.

Runlayer CEO Andy Berman then framed Uber's model as close to what Runlayer enables for customers. His version is more explicitly productized: embed a forward-deployed engineer with the customer's AI champion, scan the organization's AI clients, MCP servers, and shadow connectors, build agents live with the customer team, make successful agent skills reusable across the organization, optimize each run for tool usage and model choice, and then turn on controls in stages.

The distinction is important. Uber is describing an internal operating model. Runlayer is describing a commercial deployment pattern around the same idea.

## The core shift: workflow becomes the unit of automation

The most important sentence in Neppalli's post is not about 99% AI usage or 70% AI-attributed pull requests. It is this: "The workflow becomes the unit of automation — not the individual task."

That is the real shift.

A task-level automation mindset asks, "Can AI help this person complete a step faster?" A workflow-level automation mindset asks, "Why does this step exist, what upstream and downstream systems constrain it, and can the whole flow be redesigned now that an agent can read, reason, call tools, and produce auditable traces?"

That distinction explains why the pod model is more interesting than a standard productivity announcement. The work is not outsourced to AI. The work is reconstructed around AI.

## Why process diagrams are not enough

Enterprise workflows are usually not what the documentation says they are. The real workflow lives in spreadsheets, Slack messages, undocumented exceptions, local scripts, approval habits, personal judgment, and institutional memory. This is why Uber's model starts with shadowing rather than solution design.

Process diagrams capture the official path. Operators know the actual path.

This is also where embedded engineers have leverage. A central AI platform team can provide models, connectors, identity, logs, policies, and deployment paths. But it usually cannot infer the deep structure of operational work from the outside. The embedded engineer can observe the work directly, identify where judgment is being applied, distinguish useful friction from accidental friction, and build with the person who owns the problem.

That is why this resembles forward-deployed engineering more than classic platform engineering. The engineer is not merely delivering a reusable platform primitive. They are translating situated domain knowledge into a working system.

## What is actually new vs. recycled

None of the ingredients are entirely new. Embedded engineering is not new. Business process automation is not new. RPA is not new. Internal platforms are not new. Workflow mining is not new. Domain-expert shadowing is not new. Forward-deployed engineering is not new.

What is new is the recombination.

Agents now make it possible to package workflow knowledge into semi-autonomous executable artifacts rather than only dashboards, scripts, SOPs, or brittle RPA flows. MCP-style tool integration gives agents a more standard way to connect to external tools and data sources; Anthropic introduced the [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) as an open standard for connecting AI systems to data sources and tools, and the official [MCP specification](https://modelcontextprotocol.io/specification) defines it as a protocol for integrating LLM applications with external context and tools. That standardization matters because enterprise agent workflows depend less on the chat interface and more on controlled access to operational systems.

The Uber and Runlayer posts point toward a new deployment shape:

1. Find the people already using AI effectively.
2. Pair them with domain experts.
3. Observe the real workflow.
4. Build against live systems.
5. Validate against multiple operators.
6. Promote the result into a reusable skill or agent.
7. Add governance, visibility, and cost controls.
8. Repeat across functions.

The novelty is not "agents." The novelty is treating agent deployment as an operating model.

## Why governance comes after observation, but before scale

Berman's Runlayer post contains a subtle but important governance claim: "Now (and only now) do we turn controls on. Never as a hard stop: start in alert mode, build the allow-list, flip to enforce once a better path exists."

This is a pragmatic view of enterprise AI governance. If controls arrive too early as blanket prohibition, employees route around them. Shadow AI appears. Unapproved connectors appear. Credentials get pasted into tools. Local agents become invisible infrastructure.

But if controls arrive too late, the organization ends up with unbounded agentic access to production systems, data stores, and communication channels.

The staged model is better: observe first, understand real usage, classify risk, create a better paved road, then enforce.

That matters especially because MCP-style systems expand the attack surface. Official [MCP security guidance](https://modelcontextprotocol.io/docs/concepts/security) describes risks and best practices for authorization and secure implementation. Recent research has also argued that tool-integrated LLM agents introduce protocol-level security risks such as prompt injection, implicit trust propagation, and weak capability attestation [1]. Another paper, focused on attested MCP tool-server admission, argues that unmediated third-party MCP connections create trust gaps around which servers may be used and which tools are in bounds [2].

Uber itself has also become a useful reference point for agent security. A 2026 paper on Agentic Detection and Response describes a production enterprise security framework deployed at Uber, processing more than 10,000 agent sessions daily across more than 7,200 hosts, with telemetry designed to capture agent reasoning, prompts, causal chains, and tool execution [3]. That is the kind of control plane implied by serious enterprise agent adoption. Logs are not enough. You need causal observability over the agent run.

## Cost becomes a design constraint

The other constraint is cost. Agentic workflows can burn tokens, tool calls, cloud compute, and human review time. The Business Insider coverage around Uber notes both the productivity narrative and the cost anxiety: Uber leadership has reportedly questioned whether AI spend is producing enough visible return, and Uber had already exhausted some AI tool budgets earlier than expected.

This is why Berman's "agent optimizer" point matters. Once agents are used operationally, every run has an economic profile: model choice, prompt length, tool-call count, retry behavior, latency, failure rate, and review burden. A workflow that looks impressive in a demo can be too expensive or too fragile at production volume.

The enterprise pattern therefore becomes: discover the workflow, build the agent, instrument the run, evaluate quality, downshift models where possible, cache or precompute where possible, restrict unnecessary tool access, and keep humans only where their judgment changes the outcome.

This is not a side concern. It is the difference between agentic AI as transformation and agentic AI as tokenmaxxing.

## Who benefits

This model benefits AI-proficient engineers who can move across product, infrastructure, security, and domain workflows. It also benefits domain experts whose tacit knowledge becomes leverage rather than a bottleneck. In a good implementation, the expert is not replaced; their workflow knowledge becomes encoded into reusable systems that other people can use.

It benefits internal AI platform teams if they can provide the paved road: identity, connectors, audit logs, evals, deployment templates, model routing, approval workflows, and observability.

It benefits vendors building enterprise agent control planes: MCP gateways, policy engines, run tracing, agent security, eval platforms, cost optimizers, and workflow registries.

It is less favorable to generic copilot vendors without deep workflow integration. It also pressures traditional RPA vendors because agents can operate across messier, more language-heavy workflows than deterministic UI automation, though serious enterprises will still need the same discipline RPA programs often learned painfully: ownership, monitoring, exception handling, and change management.

## Who loses

The weakest position is the "AI enablement" function that only distributes licenses, runs training sessions, and measures adoption by seat activation. Usage is not value. Prompting is not workflow redesign. Demos are not operating capability.

The second weak position is centralized automation without embedded discovery. If the team does not sit with the work, it will automate the documented process rather than the real process.

The third weak position is uncontrolled bottom-up adoption. It may generate early wins, but it accumulates security, cost, and maintenance debt. As MCP usage expands, the tool layer becomes a governance surface. Research on public MCP tool usage found that software development dominates current tool creation, but the share of "action" tools rose substantially over the observed period, including tools capable of modifying external environments [4]. That is the critical boundary: once agents act, not just answer, the organization needs controls.

## Why this matters for engineering careers

The engineer with leverage in this model is not simply the best prompt writer. It is the engineer who can do five things well:

1. Understand real operational workflows.
2. Translate tacit domain knowledge into system boundaries, tools, prompts, policies, and evals.
3. Build agent workflows that interact safely with enterprise systems.
4. Instrument and evaluate those workflows.
5. Package successful patterns into reusable capabilities.

This is a hybrid of product engineering, platform engineering, security engineering, and field engineering. It is close to what forward-deployed engineers do, but with stronger emphasis on agent reliability, tool governance, and workflow transformation.

The career implication is blunt: the value moves away from isolated implementation and toward situated system design. Engineers who can only produce code faster may get some productivity lift. Engineers who can redesign workflows around agents can change the cost structure of a function.

## The operating model implied by Uber and Runlayer

A mature enterprise agent program will likely need four layers.

**First, the discovery layer:** map where AI is already being used, which teams have capable internal champions, what tools and MCP servers already exist, and where shadow workflows are forming.

**Second, the embedded delivery layer:** small pods or FDE-like teams that sit with domain experts, observe the work, build agents against real systems, validate with operators, and ship.

**Third, the platform layer:** reusable skills, connectors, identity, RBAC, logging, model routing, prompt/version management, evals, approval flows, and deployment paths.

**Fourth, the governance layer:** policy, risk classification, auditability, security scanning, cost controls, incident response, and lifecycle ownership.

Most companies over-invest in layer three before they understand layer one. Uber's post is interesting because it starts with embedded discovery. Runlayer's post is interesting because it tries to turn that discovery-to-governance loop into a repeatable customer motion.

## What could happen next

**Best case:** Agentic Pods become a durable operating model. Uber and similar companies build internal agent factories where domain workflows are continuously discovered, instrumented, improved, and governed. AI adoption becomes less about individual productivity and more about organizational throughput.

**Base case:** The model produces strong local wins but scaling remains uneven. Some functions get durable workflow automation; others produce demos that decay because ownership, evals, maintenance, and integration quality are weak.

**Failure case:** The productivity claims remain anecdotal, costs rise faster than value, governance trails adoption, and organizations end up with a new generation of fragile automation debt. The labels change from RPA bots to AI agents, but the failure mode is familiar.

## What to watch

The real evidence will not be view counts or screenshots. It will be operational metrics.

Watch whether Uber or similar companies publish cost per workflow run, failure rates, human review rates, model mix, tool-call volume, incidents, function-level adoption, and retention of agent workflows after the initial pod ends. Watch whether agent skills are reused across teams or remain bespoke. Watch whether business functions own the workflows after launch or whether everything depends on a small group of AI-proficient engineers. Watch whether governance is enforced at the tool layer rather than only through acceptable-use policy.

The strongest confirmation signal would be a public postmortem of one workflow: the original process, the redesigned process, the agent architecture, the tools used, the eval method, the observed failure modes, the cost profile, and the governance model.

Until then, the correct stance is measured interest. Uber's Agentic Pods are not proof that agents have transformed enterprise operations. They are evidence that the serious frontier of enterprise AI is moving from tool adoption to workflow-centered deployment.

## References

1. Narek Maloyan and Dmitry Namiot — [Breaking the Protocol: Security Analysis of the Model Context Protocol Specification and Prompt Injection Vulnerabilities in Tool-Integrated LLM Agents](https://arxiv.org/abs/2601.17549)
2. Alfredo Metere — [Attested Tool-Server Admission: A Security Extension to the Model Context Protocol](https://arxiv.org/abs/2605.24248)
3. Chenning Li, Pan Hu, et al. — [ADR: An Agentic Detection System for Enterprise Agentic AI Security](https://arxiv.org/abs/2605.17380) (MLSys 2026, deployed at Uber)
4. Merlin Stein — [How are AI agents used? Evidence from 177,000 MCP tools](https://arxiv.org/abs/2603.23802) (UK AI Security Institute, 2026)
5. Praveen Neppalli Naga, Uber CTO — Agentic AI adoption and Agentic Pods at Uber (LinkedIn post, July 2026; summarized by [The State of AI](https://www.thestateofai.com/news/uber-unveils-agentic-pods-structure))
6. Andy Berman, Runlayer CEO — Runlayer's FDE-led enterprise agent rollout model (LinkedIn post, 2026)
7. Business Insider — Uber's CTO embedded top AI engineers in HR, finance, and legal (2026)
8. Anthropic — [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
9. Model Context Protocol — [Official MCP specification](https://modelcontextprotocol.io/specification)
10. Model Context Protocol — [Security Best Practices](https://modelcontextprotocol.io/docs/concepts/security)
