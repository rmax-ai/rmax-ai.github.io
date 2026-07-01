# New to AI Forward Deployed Engineering

## Source Material — Compilation of rmax.ai FDE Articles

The following is compiled from five rmax.ai technical notes (May–June 2026). Synthesize into a landing page article that introduces AI Forward Deployed Engineering — role, capabilities, operating model, and challenges.

---

## SOURCE 1: "The Forward Deployed Engineer in Enterprise AI: From Integration Specialist to Agentic Control-Plane Builder" (May 30, 2026)

### Core thesis
The durable value of a Forward Deployed Engineer in enterprise AI is not local integration work by itself. It is the conversion of local workflow knowledge into reusable control-plane capability for governed agent execution.

### Context
Enterprise AI doesn't usually fail at the model layer. It fails when organizations cannot connect model capability to permissions, policy, approvals, systems of record, and measurable outcomes. The shift from copilots to agents changes the deployment problem — once AI participates in business processes, questions become about authority, identity, policy interpretation, approval boundaries, reversibility, observability, and cost per outcome.

### Six-layer control plane model
The FDE works across all six layers:
1. Business outcome (KPIs, cycle time, risk reduction)
2. Workflow and evaluation (approvals, traces, escalation, evals)
3. Policy and identity (delegation, scopes, authorization)
4. Semantic and knowledge (entities, evidence, provenance)
5. Tool and integration (APIs, SaaS, MCP, gateways)
6. Model and runtime (routing, context, sandboxing, budgets)

### Identity and delegation
Enterprise permissions were designed for humans and conventional applications, not agents that reason conditionally and act at scale. Production system should separate: read authority, proposal authority, approval authority, and execution authority. A person's broad application access does not automatically define the right authority for an agent acting on that person's behalf.

### FDE operational loop
Production failure → diagnosis → new evaluation case → platform or policy improvement → safer redeployment

### Concrete example: Approval-gated SaaS writes
Seven-step workflow: (1) read relevant system records and policy documents, (2) produce structured proposed change with evidence, (3) determine whether approval is required, (4) route proposal to correct approver if needed, (5) execute only the narrow approved action, (6) verify resulting system state, (7) record requester, evidence, approval, tool response, and outcome.

### External references
- Cristina Criddle, "The New Hot Job in AI: Forward-Deployed Engineers," Financial Times, 1 November 2025.
- OpenAI, "OpenAI Launches the OpenAI Deployment Company to Help Businesses Build Around Intelligence," 11 May 2026.
- OpenAI Careers, "Forward Deployed Engineer and Technical Deployment Lead," 2026.
- Palantir, "Connecting Agents to Decisions," 28 April 2026; "Deploying Full Spectrum AI in Days: How AIP Bootcamps Work," 2023.
- Google Cloud, "Introducing Gemini Enterprise Agent Platform," April 2026.
- Model Context Protocol, "Authorization Specification," 25 November 2025.
- OWASP GenAI Security Project, "OWASP Top 10 for Agentic Applications for 2026," December 2025.
- NIST AI RMF Generative AI Profile, July 2024.

---

## SOURCE 2: "FDE Playbook for Governed Agentic Adoption" (June 6, 2026)

### Core thesis
FDE teams create durable value when they translate messy business work into governed agentic workflows, instrument those workflows, evaluate them, and turn local pilots into reusable operating patterns.

### North star metric
Safely delegated work completed. Not agents created, MCP servers connected, documents indexed, or demos delivered. The real question is whether useful work was completed by AI-assisted or AI-executed workflows under appropriate governance, with measurable business value and human accountability.

### Maturity path (control ladder)
1. Chat-only AI
2. Approved knowledge retrieval
3. Read-only tool use
4. Human-approved write actions
5. Bounded autonomous workflows
6. High-trust domain agents

The mistake is jumping from level 1 to level 5. The goal is not maximum autonomy — it is safe, increasing autonomy.

### The unit of adoption is the workflow, not the agent
Weak starting question: "Which agent should we build?"
Better starting question: "What work should be partially delegated, under what constraints, with which approval points, and with what measurable outcome?"

### FDE discovery questions
- What triggers this workflow?
- Who owns the outcome?
- What systems are involved?
- What data is trusted?
- What decisions are made?
- Where do people wait?
- Where do people copy-paste?
- Where do mistakes happen?
- What judgment is required?
- What would be dangerous to automate?
- What must remain human-owned?

### Governed workflow specification
Every governed workflow should specify: workflow owner, user group, trigger, inputs, approved data sources, allowed tools, forbidden actions, approval gates, output artifact, logging requirements, data retention rules, human override path, failure modes, success metrics, evaluation method, kill criteria.

### Governance as the product
For agentic systems, governance is part of the product. Without governance, the system cannot be trusted with real work.

Actions classified by consequence: Read → Draft → Propose → Write with approval → Write autonomously → External communication → Financial or contractual action. Higher consequence = stronger control.

### MCP tool design principle
Tools should be designed around business actions, not raw system access:
- Bad: `query_database(sql)` — Better: `get_customer_risk_summary(customer_id)`
- Bad: `update_ticket(payload)` — Better: `draft_ticket_update_from_approved_summary(summary_id)`
- Bad: `send_message(channel, text)` — Better: `draft_internal_update(workflow_id, audience)`

Every enterprise MCP tool should define: purpose, inputs, outputs, permissions, data classification, side effects, rate limits, failure responses, logging requirements, approval requirement, human owner, version, evaluation method, rollback path.

### Evaluation is the missing discipline
Five evaluation dimensions:
- Quality: accuracy, completeness, relevance, grounding, consistency, business usefulness
- Safety: data boundary violations, unauthorized tool calls, unsupported claims, sensitive data exposure
- Workflow: time saved, handoff reduction, human acceptance rate, cycle-time reduction, cost per completed workflow
- Reliability: tool call success rate, retrieval success rate, latency, failure frequency, regression rate
- Trust: repeat usage, approval rate, rejection reasons, user satisfaction, complaints, abandonment

### Applied workflow scenarios (four concrete examples)
1. Incident review agent — draft postmortems, identify missing context, propose follow-up tickets. Human-approved drafting.
2. Customer support drafting agent — summarize case context, retrieve documentation, draft response. Draft only, no external sending.
3. Sales account briefing agent — produce structured account brief from approved sources. Read-only + draft generation.
4. Ticket enrichment agent — inspect ticket, identify missing information, suggest classification. Read-only + human-approved updates.

### What an internal FDE team should own
The adoption loop: workflow discovery, delegation classification, governed workflow design, minimum useful pilot implementation, tool and MCP design patterns, evaluation design, telemetry requirements, user feedback capture, failure analysis, pattern extraction, business enablement, scaling recommendations.

Reusable organizational assets: workflow templates, intake forms, pilot scoring rubrics, governance checklists, MCP and tool standards, approval patterns, evaluation sets, failure taxonomies, case studies, user onboarding guides, reference implementations.

---

## SOURCE 3: "AI FDE Operating Model: Exploration, Pilot, and Production" (June 16, 2026)

### Core thesis
Teams should sequence evidence and controls rather than choose between speed and governance. AI-enabled workflows carry empirical uncertainty at the start — whether the model can perform well enough, what context it needs, how users will adapt, and which failures will dominate.

### Three operating modes
- Exploration: Is there valuable capability at all? Maximize learning speed while preventing material harm.
- Pilot: Can real users get repeatable value under realistic but bounded conditions?
- Production: Can the workflow run safely, reliably, economically, and accountably at scale?

### Six operating principles
1. Separate capability risk from operational risk
2. Bound consequences — don't demand certainty (deterministic constraints: read-only tools, scoped credentials, allowlisted actions, transaction limits, human approval, audit trails, reversible writes)
3. Increase controls with authority and irreversibility
4. Use evidence to move between stages (hypothesis, baseline, measurable success criteria, unacceptable outcomes, named transition owner)
5. Design human oversight as part of the system (reviewers need time, evidence, context, independence, authority to intervene)
6. Evaluate the whole socio-technical workflow (not just model quality — user intent, context, retrieval, prompts, tools, policies, interfaces, review, execution, business outcome)

### Stage-gate decision framework
Six dimensions evaluated at each transition: Value, Capability, Control, Operability, Economics, Accountability. Valid decisions: Stop, Iterate, Continue within stage, Advance, Regress.

### Risk-based control matrix
Low impact advisory (summaries, internal notes) → light controls: approved data, source attribution, user review, logging, no autonomous external actions.
Moderate impact operational (case recommendations, draft changes, support responses) → moderate controls: least privilege, allowlisted actions, structured logs, quality/cost/latency monitoring, rollback capabilities.
High impact consequential (financial changes, refunds, access changes, binding communication) → strong controls: separation of duties, deterministic validation, policy engines, dual approval, formal governance.

---

## SOURCE 4: "Why AI FDE Teams Must Become Organizational Learning Systems" (June 30, 2026)

### Core thesis
FDE teams must evolve from a high-end delivery service into a distributed organizational learning system. Without a deliberate mechanism to capture field discoveries, each deployment starts from scratch and delivery capacity grows only through headcount.

### The central scaling problem
A team enters a business unit, studies workflow, connects fragmented systems, works around data problems, builds evaluations, discovers trust issues. The system ships. Engineers move on. Months later, another team encounters a structurally similar problem. It rebuilds the same integration, rediscovers the same model failure, creates another version of the same evaluation suite. The organization delivered two systems. It learned almost nothing.

### Why FDE exists
Enterprise AI cannot be fully specified in advance. Constraints emerge only when systems run against real production data: tacit business rules, inconsistent data definitions, permission models encoded across systems, undocumented human exceptions, prompt/context/model-version sensitivity.

### Two outputs of every FDE engagement
1. Local business outcome
2. Evidence — workflow discoveries, data quirks, model failure modes, adoption friction points

### The field-to-platform learning loop (six stages)
Observe → Preserve → Compare → Validate recurrence → Productize → Measure/deprecate

### Rule of Three
1. Solve the first occurrence locally
2. Reuse or adapt in a second environment
3. Abstract only when repeated use clarifies what remains stable

### Danger of premature abstraction
In AI systems, the risk is greater because underlying models, APIs, prompting methods, and orchestration techniques change rapidly. A candidate for productization should demonstrate: recurrence across independent deployments, clear invariant behavior, bounded and understandable variation, meaningful reduction in duplicated effort or risk, maintainability by a stable owner, sufficient stability in underlying interfaces, credible path to adoption.

### Measure leverage, not activity
- Delivery acceleration: time to first validated production outcome, engineering effort per deployment
- Reuse and bypass: adoption across independent environments, duplicate-implementation rate
- Repeated failure reduction: recurrence of known incidents, regressions caught before production
- Capability transfer: support requests after handover, production changes completed without FDE assistance

### Minimum viable FDE learning system
Small set of connected mechanisms: structured evidence capture during engagement, recurring cross-deployment comparison, governed pattern registry, productization decision forum, named ownership for shared capabilities, reuse and outcome measurement, feedback into future deployments and handovers.

### Key references
- Jason Martin, Databricks — "Forward Deployed Engineering: Delivering Business Outcomes with AI"
- James G. March — "Exploration and Exploitation in Organizational Learning," Organization Science, 1991
- Ikujiro Nonaka — "The Knowledge-Creating Company," Harvard Business Review
- Wesley M. Cohen and Daniel A. Levinthal — "Absorptive Capacity: A New Perspective on Learning and Innovation," Administrative Science Quarterly, 1990

---

## SOURCE 5: "MCP Design Best Practices for Agents" (June 8, 2026) — FDE-relevant section

### What This Means for Forward Deployed Engineers
An FDE working on enterprise AI should not merely connect systems or configure assistants. The higher-value work is to identify operational workflows, redesign them as agent-native interfaces, and turn field-specific deployment lessons into reusable platform patterns.

A strong FDE should ask:
- What workflow is the agent actually trying to complete?
- Which decisions require business context?
- Which actions are safe to automate?
- Which actions require approval?
- What evidence should be attached before execution?
- What should the agent never see?
- What should the agent never be allowed to mutate?
- How will we measure success?
- How will we debug failures?
- How will this pattern become reusable?

The FDE becomes a bridge between model capability and institutional reality: part systems engineer, part workflow architect, part governance implementer, and part product feedback loop.

---

## INSTRUCTIONS FOR SYNTHESIS

Synthesize the above source material into a landing page article titled "New to AI Forward Deployed Engineering" (slug: `new-to-ai-fde`).

**Target audience:** Engineers and technical leaders who've heard "FDE" mentioned alongside enterprise AI but don't yet understand what the role actually entails, what capabilities FDEs bring, and what makes the work challenging.

**Tone:** Direct, technical, authoritative. Not marketing. Not academic. Written for someone who builds systems.

**Structure the article as:**
1. **What is an AI Forward Deployed Engineer?** — Role definition and why it exists now. Use the FT article reference and the Databricks model as anchoring context.
2. **Why the role matters** — The shift from copilots to agents, from chat interfaces to governed delegation.
3. **Core capabilities** — What FDEs actually do: workflow discovery, governed workflow design, MCP/tool design, evaluation, pattern extraction, organizational learning.
4. **The FDE operating model** — Exploration → Pilot → Production, the six principles, the stage-gate framework.
5. **Real FDE workflows** — Concrete examples: incident review, support drafting, sales briefing, ticket enrichment.
6. **Key challenges** — Premature abstraction, learning system gaps, human review bottlenecks, identity/delegation misdesign, the delivery-vs-learning tension.
7. **Further reading** — Two subsections:
   - **Internal references** — Link to the five rmax.ai notes used as sources
   - **External references** — Link to the industry references from across all five sources

**Internal links to include:**
- /notes/forward-deployed-engineer-enterprise-ai/
- /notes/fde-playbook-governed-agentic-adoption/
- /notes/ai-fde-operating-model/
- /notes/ai-fde-organizational-learning-systems/
- /notes/mcp-design-best-practices-for-agents/

**External references to include (at minimum):**
- Cristina Criddle, FT — "The New Hot Job in AI: Forward-Deployed Engineers" (Nov 2025)
- Databricks — FDE model blog post
- OpenAI FDE careers / deployment company announcement
- Palantir AIP Bootcamps
- NIST AI RMF GenAI Profile

**Include 2–3 Mermaid diagrams** from the source material (adapt them — the operating model lifecycle, the control ladder, the learning loop — pick the most impactful ones).

**Format requirements:**
- YAML frontmatter with slug: `new-to-ai-fde`, section: `notes`, type: `guide`
- Use `[N]` inline citation format with a `## References` section at end
- Wrap Mermaid diagrams in ` ```mermaid` fenced code blocks
