# The Organizational Stages of AI Adoption

*Why AI-native engineering is primarily an organizational transition—not a model transition.*

Over the past two years, foundation models have improved at extraordinary speed. Modern coding agents can inspect repositories, edit multiple files, execute tests, search documentation, call tools, and continue working across tasks that would previously have required sustained human attention.

Yet many engineering organizations are seeing a different pattern: model capability continues to improve while organizational productivity improves much more slowly.

The limiting factor is no longer simply whether an AI system can perform useful engineering work. Increasingly, it is whether the organization has the processes, infrastructure, and governance required to delegate that work safely.

[Anthropic's Steps of AI Adoption](https://claude.ai/code/artifact/bfdfaef9-bc62-4dfe-ba9e-c58a26c9accf#no_universal_links) framework captures this transition particularly well. It describes a progression from tightly gated access, through one-to-one assistance and parallel orchestration, toward supervised autonomy and eventually AI-native execution. Read this way, the framework is less a maturity model for tools than a maturity model for organizational delegation.

The key question is not: *How capable is the model?*

It is: *How much responsibility can the organization safely transfer to an autonomous system?*

## AI shifts the organizational constraint

Early AI adoption focused on making code generation faster and cheaper. Once generation becomes inexpensive, however, the scarce resource moves elsewhere.

A developer using a coding assistant still needs access to the right repository, documentation, credentials, test environments, and organizational knowledge. Generated changes must still be reviewed, validated, merged, deployed, and monitored. Security and compliance policies still apply. Someone remains accountable for the outcome.

This is why local productivity gains do not automatically become organizational throughput. A task can be generated in minutes while waiting hours or days for review, permissions, integration testing, or cross-team approval.

The pattern is familiar. Continuous integration was not mainly an improvement in compilers; it was an improvement in the system surrounding code changes. Cloud computing did not merely make servers faster; it changed how infrastructure was provisioned, governed, and operated. DevOps research similarly showed that delivery performance depends on technical practices, organizational design, feedback loops, and the ability to move changes safely through the entire system—not on code production alone.

Agentic AI is following the same path. Better models remove one constraint and expose the next.

## The five stages of organizational adoption

Anthropic's framework describes five stages. Each stage increases the amount of work delegated to agents, changes the engineer's role, and exposes a new organizational bottleneck.

| Stage | Human Role | Organizational Capability | Primary Constraint |
|---|---|---|---|
| 0 — Gated | Approval seeker | Controlled experimentation | Governance and access |
| 1 — Assisted | Pair programmer | Individual acceleration | Human attention |
| 2 — Parallel orchestration | Work coordinator | Concurrent execution | Review bandwidth |
| 3 — Supervised autonomy | System supervisor | Trusted delegation | Organizational trust |
| 4 — AI-native | Organizational designer | Continuous autonomous execution | Identifying valuable work and defining acceptable boundaries |

The progression is cumulative. Solving governance makes AI accessible. Solving accessibility exposes review as the next bottleneck. Automating verification exposes trust. Solving trust shifts attention toward deciding which work should be automated at all.

### Stage 0: Gated

Organizations at this stage are primarily concerned with security, procurement, compliance, and basic access.

AI use may be restricted to approved chat interfaces or lighter models behind internal gateways. Tool access is limited. Developers may be able to generate code locally but lack an approved path for running agents against internal systems or moving generated artifacts into production.

The bottleneck is not model capability. It is the organization's inability to expose useful context and actions without violating existing controls.

The goal at this stage should not be unrestricted access. It should be a governed path from experimentation to production: identity-aware access, approved data boundaries, auditability, budget controls, and clear ownership for agent-generated work.

### Stage 1: Assisted

This is where many engineering organizations currently operate.

One developer works with one coding agent. The developer provides the task, monitors the session, inspects most generated changes, and remains directly responsible for merging the result.

The productivity gain can be substantial for bounded work. The Microsoft study [Adoption and Impact of Command-Line AI Coding Agents](https://arxiv.org/abs/2607.01418), based on an early-2026 rollout across tens of thousands of engineers, estimated that adopters merged roughly 24 percent more pull requests than they otherwise would have. The authors explicitly caution that merged pull requests are an output proxy rather than a direct measure of delivered value, but the study provides evidence that agentic coding tools can change engineering throughput at organizational scale.

The constraint at this stage is human attention.

An agent may produce an afternoon's implementation in minutes, but the engineer must still read the diff, understand unfamiliar decisions, verify assumptions, and confirm that the change is safe. Code generation becomes cheap while code comprehension remains expensive.

Research on developer productivity reinforces this distinction. [Beyond the Commit](https://arxiv.org/abs/2602.03593) found that developers often report high satisfaction with AI coding assistants while realizing only modest time savings, and that productivity includes cognitive load, self-sufficiency, ownership, expertise development, and long-term maintainability—not only output volume.

The transition out of assisted use therefore requires more than a better model. It requires agents that can verify their work, environments that can execute those checks automatically, and workflows that allow engineers to review outcomes rather than every intermediate action.

### Stage 2: Parallel orchestration

Parallel orchestration is not simply using more agents. It changes the unit of work.

Instead of collaborating synchronously with one assistant, an engineer decomposes a larger objective into independent tasks and delegates them concurrently. One agent may investigate the repository, another implement a change, another update tests, and another review the result. Isolated worktrees or remote environments prevent concurrent sessions from modifying the same working copy.

Automated builds, tests, type checks, linting, security scanning, and code review run before the work reaches a person. The engineer increasingly reviews completed proposals rather than watching each command.

Anthropic's framework highlights worktree isolation, automated verification, automated review, pre-approved safe commands, and remote monitoring as enabling capabilities for this stage. The architectural analysis [Dive into Claude Code](https://arxiv.org/abs/2604.14228) reaches a similar conclusion: the core model loop is relatively small, while most of the system concerns permissions, context management, extensibility, session state, delegation, and isolation.

This stage represents a shift from programming to orchestration. The engineer writes less of the implementation directly and spends more time specifying tasks, selecting boundaries, resolving conflicts, evaluating evidence, and deciding what should merge.

The new bottleneck is review bandwidth. Multiplying execution without multiplying validation merely creates a larger queue of uncertain changes.

### Stage 3: Supervised autonomy

The transition from parallel orchestration to supervised autonomy is qualitative.

At Stage 2, humans initiate most work and review most completed outputs. At Stage 3, agents begin initiating well-bounded categories of work themselves. Dependency updates, routine maintenance, migrations, documentation repair, flaky-test investigation, and recurring operational tasks can become event-driven rather than manually assigned.

Engineers move from supervising tasks to supervising systems. When a failure occurs, the central question changes from "What line of code is wrong?" to "What context, policy, test, or feedback loop was missing from the system?"

This is also where organizational trust becomes the central constraint.

A person can inspect one pull request in detail. No person can continuously inspect hundreds of agent executions across multiple repositories and services. Direct observation stops scaling. The organization must rely on explicit boundaries, automated controls, reliable telemetry, and historical evidence that the system behaves acceptably when nobody is watching each action.

### Stage 4: AI-native

At the AI-native stage, the organization increasingly operates like a software factory.

Humans define objectives, priorities, policies, risk tolerances, and resource constraints. Agents discover or receive work, coordinate execution, validate results, and escalate exceptions. Engineers monitor outcomes and intervene where uncertainty, novelty, or consequence exceeds the system's delegated authority.

The scarce resource is no longer implementation capacity. It is judgment: identifying valuable work, expressing intent clearly, selecting what can be automated, and deciding where human accountability must remain direct.

This does not imply removing people from engineering. It moves human work toward problem selection, architecture, policy, evaluation, organizational learning, and responsibility for consequences.

## The hidden transition: evidence replaces observation

The most important transition in the model occurs between parallel orchestration and supervised autonomy.

Human observation no longer scales.

Verification answers a narrow question: *Did this particular change pass the available checks?*

Evidence answers a broader question: *Why should the organization trust this execution, and what supports confidence in similar future executions?*

A passing test suite is useful, but insufficient. Tests may be weak, generated from the same mistaken assumptions as the implementation, or disconnected from the real production risk. Scalable autonomy requires evidence about what happened, what information was used, which decisions were made, which policies were enforced, and how the outcome was validated.

- **Execution evidence** includes traces, tool calls, commands, environment details, and the context retrieved during the task.
- **Decision evidence** includes plans, approval points, policy decisions, authority boundaries, and reasons for escalation.
- **Quality evidence** includes test results, static analysis, regression evaluations, adversarial checks, and comparisons against explicit acceptance criteria.
- **Operational evidence** includes failure rates, rollback performance, escaped defects, cost, latency, and reliability by task category.

Evidence transforms opaque automation into an accountable engineering system. It allows reviewers to examine the claims and risks of a change rather than reconstructing the agent's entire process from a diff.

This evidence must also be treated critically. A polished green dashboard can create automation bias just as easily as polished generated code. The evidence itself needs provenance, independence, coverage, and calibration. Tests produced by the same agent that wrote the code are useful, but they should not always be treated as independent confirmation.

## The engineer's role changes

Traditional software work is often summarized as design, implement, review, and deploy.

AI-native engineering adds a higher-order loop:

- Design the execution system.
- Specify intent and acceptance criteria.
- Define permissions and guardrails.
- Automate verification.
- Monitor outcomes and exceptions.
- Feed failures back into context, policies, skills, and evaluations.

This changes the engineer's leverage. The highest-value contribution may be a reusable test harness, a repository-specific skill, an access policy, a context provider, or an evaluation dataset that improves every future execution.

The engineer becomes responsible not only for producing software, but for designing the conditions under which software can be produced reliably by others—including autonomous systems.

## The industry is converging on orchestration

The major AI platforms increasingly reflect this architectural direction.

[OpenAI's Agents SDK](https://platform.openai.com/docs/quickstart) supports tools, handoffs, orchestration logic, guardrails, sessions, and tracing around model calls. [Google's Agent Development Kit and Agents CLI](https://google.github.io/adk-docs/) frame agent development as a lifecycle spanning scaffolding, tools, evaluation, deployment, and observability. [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) distinguishes open-ended agents from explicit graph-based workflows and provides sequential, concurrent, handoff, group-chat, and manager-led orchestration patterns, together with checkpointing and human approval. [Anthropic's Claude Code ecosystem](https://docs.anthropic.com/en/docs/claude-code) emphasizes permissions, worktree isolation, subagents, hooks, context management, and long-running workflows.

These systems differ in implementation, but they point toward the same conclusion: the production abstraction is no longer an isolated prompt. It is a controlled execution system around one or more models.

This also suggests that foundation models will become increasingly interchangeable within larger architectures. Model selection will remain important for capability, latency, and cost, but durable advantage will often come from the surrounding system: context quality, tool design, permissions, evaluation, evidence, workflow ownership, and the ability to learn from failures.

## Organizational leverage replaces individual productivity

Most AI adoption programs begin with individual productivity. They measure suggestion acceptance, tasks completed, tokens consumed, lines changed, or developer sentiment.

These metrics can be useful, but they are insufficient. An organization can generate more code while increasing review queues, operational risk, duplication, and maintenance cost.

The more relevant question is whether AI improves the flow of validated value through the organization.

That requires measuring lead time to a verified outcome, review effort, change failure rate, escaped defects, rollback success, evidence quality, and the proportion of agent work that can proceed without unnecessary human intervention. It also requires distinguishing local speed from system-level performance.

The Microsoft rollout study is instructive here. It found measurable growth in merged pull requests, but it also noted that adoption spread through social networks and that retention correlated more strongly with coding activity than with demographic characteristics. Adoption was not uniform, and access alone did not create sustained use. Organizational learning, visible peer practices, and fit with real work mattered.

The organizations that benefit most from AI will therefore not necessarily be those that deploy the newest model first. They will be those that redesign work so increasingly capable systems can operate safely, efficiently, and accountably.

## Conclusion

AI-native engineering is not primarily a model transition. It is an organizational transition from direct execution toward progressively greater delegation.

Each stage removes one constraint and exposes another. Governance enables access. Access exposes attention. Parallel execution exposes review capacity. Automated verification exposes trust. Trust eventually exposes the hardest question: what work is valuable enough, bounded enough, and safe enough to delegate?

Foundation models will continue to improve. As they do, raw model capability is likely to become less differentiating than the systems organizations build around those models.

The difficult engineering problems increasingly sit outside the model: managing context, enforcing policy, orchestrating execution, collecting evidence, evaluating behavior, allocating authority, and improving the system from experience.

The future of software engineering will not be defined only by who has the best model.

It will be defined by who builds the best organizational system around it.

## References

1. Anthropic — [Steps of AI Adoption](https://claude.ai/code/artifact/bfdfaef9-bc62-4dfe-ba9e-c58a26c9accf#no_universal_links). Boris Cherny, July 16, 2026.
2. Liu, Jiacheng; Zhao, Xiaohan; Shang, Xinyi; Shen, Zhiqiang — [Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems](https://arxiv.org/abs/2604.14228). arXiv:2604.14228, 2026.
3. Murphy-Hill, Emerson; Butler, Jenna; Savelieva, Alexandra — [Adoption and Impact of Command-Line AI Coding Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and GitHub Copilot CLI](https://arxiv.org/abs/2607.01418). arXiv:2607.01418, 2026.
4. Beller, Moritz et al. — [Beyond the Commit: Developer Perspectives on Productivity with AI Coding Assistants](https://arxiv.org/abs/2602.03593). ICSE-SEIP 2026; arXiv:2602.03593.
5. Forsgren, Nicole; Storey, Margaret-Anne; Maddila, Chandra; Zimmermann, Thomas; Houck, Brian; Butler, Jenna — [The SPACE of Developer Productivity: There's More to It Than You Think](https://queue.acm.org/detail.cfm?id=3454124). ACM Queue 19(1), 2021.
6. Forsgren, Nicole; Humble, Jez; Kim, Gene — [Accelerate: The Science of Lean Software and DevOps](https://itrevolution.com/product/accelerate/). IT Revolution, 2018.
7. OpenAI — [Agents SDK and API documentation](https://platform.openai.com/docs/quickstart).
8. Google — [Agent Development Kit and Agents CLI documentation](https://google.github.io/adk-docs/).
9. Microsoft — [Agent Framework documentation: agents, workflows, orchestration, checkpointing, and human-in-the-loop execution](https://learn.microsoft.com/en-us/agent-framework/).
10. NIST — [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework), 2023.

