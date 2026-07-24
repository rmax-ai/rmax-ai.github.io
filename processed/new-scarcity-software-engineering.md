<!--
TODO: Verify/resolve URLs for these references:
- Anthropic, "Effective Harnesses for Long-Running Agents", Nov 26, 2025
- Anthropic, "Harness Design for Long-Running Application Development", Mar 24, 2026
- Google Engineering Practices, "The Standard of Code Review"
- Herbert A. Simon, "Designing Organizations for an Information-Rich World" (1971)
- Kevin Storer, "How Generative AI Affects the Value of Development Work"
- Datadog, "Designing MCP Tools for Agents"
- Datadog, "Bring Live Datadog Telemetry into Your AI Agents"

Known URLs (verified):
- openai-harness: https://openai.com/index/harness-engineering/
- anthropic-expertise: https://www.anthropic.com/research/claude-code-expertise
- anthropic-context: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- anthropic-evals: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- dora-2025: https://dora.dev/dora-report-2025/
-->

---
title: "The New Scarcity of Software Engineering in the AI Era"
description: "As code generation becomes abundant, engineering value shifts toward judgment, verification, architecture, context, and organizational design."
date: 2026-07-24
---

The New Scarcity of Software Engineering in the AI Era

> Code is becoming abundant. Understanding is becoming scarce.

For the past several years, discussion about artificial intelligence and software engineering has revolved around one question:

Will AI replace software engineers?

It is increasingly the wrong question.

A more useful one is:

As the marginal cost of producing plausible software continues to fall, what becomes scarce?

Throughout computing history, major technological advances have shifted engineering bottlenecks rather than eliminated them. High-level languages reduced the need to write assembly. Frameworks removed boilerplate. Managed databases abstracted storage administration. Cloud computing reduced the burden of provisioning physical infrastructure.

Software engineering did not disappear after any of these transitions. The limiting factor moved.

Once infrastructure became easier to provision, architecture and operational discipline mattered more. Once frameworks accelerated application development, product judgment and system integration became more important. Once open-source libraries made sophisticated capabilities widely available, selecting, combining, securing, and governing those components became harder than obtaining them.

Large language models are producing another such transition.

Models can already generate functions, tests, migrations, interfaces, infrastructure definitions, and application scaffolds in seconds. Coding agents can inspect repositories, modify files, execute commands, diagnose failures, and iterate over their own work. OpenAI has described an internal experiment in which a small engineering team used Codex to build and operate a substantial application while humans focused primarily on specifying intent and constructing the environment around the agent.[^openai-harness] Anthropic's research on Claude Code similarly suggests that coding agents do not remove the value of expertise: users with greater domain knowledge tend to obtain better outcomes.[^anthropic-expertise]

But the cost of deciding what should exist, determining whether it is correct, and integrating it into a larger system is not falling at the same rate.

Code is becoming abundant.

Judgment is not.

The future of software engineering will therefore be less about manually producing code and more about designing, governing, verifying, and evolving complex socio-technical systems.


## The Economics of Abundance

Software engineering has always been shaped by scarcity.

At different points in computing history, the constrained resource has been processing power, memory, bandwidth, infrastructure, developer time, specialized knowledge, or the organizational capacity to operate complex systems. Engineering practices evolved around whichever resource was most limited.

When memory was scarce, developers optimized for compact representations. When computing power was expensive, algorithms were judged heavily by computational efficiency. When servers required weeks of procurement and configuration, infrastructure planning became a major organizational concern.

Today, frontier language models are reducing one particular scarcity:

The ability to produce code that appears locally plausible.

This is consequential. A capable engineer using modern AI tools can explore more implementation paths, generate routine components faster, translate between languages, create test cases, and work across unfamiliar parts of the stack with less friction.

But AI does not eliminate uncertainty.

Someone must still determine:

- whether the problem is worth solving;
- whether the requirements are coherent;
- whether the architecture fits the surrounding system;
- whether generated code is correct and secure;
- whether it creates hidden operational costs;
- whether it remains understandable after the original context disappears;
- and whether it advances the organization's actual objectives.

Code production is only one stage of the software lifecycle. Lowering its cost exposes constraints in the stages around it.

This is a familiar economic pattern. When one input becomes cheaper, demand for complementary inputs often rises. Cheap computing increased demand for software. Cheap cloud infrastructure increased demand for distributed-systems expertise. Information abundance increased the value of attention, filtering, and interpretation. Herbert Simon made the underlying point decades ago: an abundance of information consumes attention, making attention the scarce complementary resource.[^simon]

Cheap code will similarly increase the demand for verification, architectural coherence, and system-level judgment.

The bottleneck moves from production to evaluation.


## Constraint Migration

The transition can be understood through the Theory of Constraints: a system's throughput is limited by its most restrictive bottleneck. Improving a non-bottleneck may increase local output without improving the performance of the whole system.

For much of software history, implementation capacity was a central constraint. Translating an idea into executable software required substantial human effort. Developers had to understand syntax, libraries, tools, build systems, and platform conventions before they could produce even a modest application.

Generative AI compresses much of this work.

But increasing upstream throughput does not automatically improve the whole delivery system. When one stage accelerates while downstream stages remain unchanged, work accumulates.

In manufacturing, this produces inventory.

In AI-assisted development, it produces:

- larger pull requests;
- more generated branches;
- duplicated abstractions;
- partially implemented features;
- tests of uncertain relevance;
- additional dependencies;
- more code requiring review;
- and more possible failure paths.

The result can be higher apparent velocity alongside lower systemic confidence.

An organization may generate twice as many changes without doubling its ability to review, integrate, deploy, observe, and maintain them. At that point, code generation is no longer the constraint. Verification capacity is.

This distinction matters because many AI adoption programs optimize the wrong metrics. They measure task-completion speed, lines of code, agent sessions, or pull requests opened. These measurements capture local activity, not necessarily system throughput.

DORA's research has repeatedly emphasized that delivery performance emerges from the broader technical and organizational system rather than from isolated output measures.[^dora-2025] Its 2025 research on AI-assisted development describes AI primarily as an amplifier: it can magnify the strengths of high-performing organizations and the dysfunctions of struggling ones.[^dora-2025]

The relevant question is not how quickly code can be generated.

It is how quickly trustworthy change can move from intent to production without increasing long-term fragility.


## The New Scarcity Hierarchy

As implementation becomes cheaper, engineering work does not vanish. It moves upward and outward.

A new hierarchy of scarce capabilities is emerging.

### 1. Problem Framing

Before an AI system writes code, someone must determine what problem the code is supposed to solve.

Many software failures originate before implementation begins. Teams build the wrong workflow, optimize the wrong metric, automate a process that should have been redesigned, or encode ambiguous organizational assumptions into software.

AI amplifies the consequences of ambiguous framing because it can rapidly produce a coherent implementation of an incorrect interpretation. A human developer confronted with unclear requirements may stop, ask questions, and negotiate scope.
A coding agent may instead generate a polished solution around the wrong assumption, allowing the error to survive until integration or production.

Probabilistic models behave like high-gain amplifiers. Precise constraints often produce useful implementations. Vague intent produces confident guesses.

Problem framing therefore becomes an engineering discipline in its own right. It includes:

- identifying the decision or workflow being improved;
- separating symptoms from root causes;
- clarifying users, constraints, and failure costs;
- defining observable success;
- identifying assumptions;
- determining what must remain under human control;
- and deciding whether software is the appropriate intervention at all.

Increasingly, the scarce engineer is not merely someone who can answer, "How should we implement this?"

They can ask, "What should exist, and why?"

### 2. Systems Thinking

Modern software rarely exists in isolation.

A seemingly local change can influence data flows, security boundaries, user behavior, operational load, organizational responsibilities, regulatory obligations, infrastructure costs, downstream analytics, and future development paths.

Generative models are often strong at local transformation. They can modify a function, create an endpoint, or imitate an existing repository pattern.

Local correctness, however, does not guarantee system correctness.

A generated feature may satisfy its immediate test while increasing coupling elsewhere. It may introduce a second representation of an existing concept, bypass an authorization boundary, create an operational dependency, or place business logic in a layer where the organization cannot govern it.

Systems thinking provides a defense against this local optimization. Rather than viewing software as a collection of independent components, it examines relationships, feedback loops, delays, incentives, and emergent behavior.[^meadows] It asks how a change propagates and how the surrounding environment responds.

As AI makes local implementation easier, global reasoning becomes more valuable.

The engineer increasingly designs interactions:

- between services;
- between teams;
- between humans and agents;
- between policies and execution;
- between short-term delivery and long-term maintainability.

The scarce capability is no longer producing an isolated component. It is anticipating how that component changes the behavior of the whole.

### 3. Architectural Judgment

Models can generate architectural proposals.

Given a prompt, a model can recommend a monolith, a microservice decomposition, an event-driven platform, a serverless design, or a multi-agent workflow. It can summarize standard trade-offs and reproduce patterns from existing systems.

What it cannot reliably determine is which trade-off is appropriate for a particular organization over time.

Architecture is not the production of diagrams. It is the management of consequential decisions under uncertainty.

Architectural judgment balances:

- present complexity against future flexibility;
- scalability against operational burden;
- standardization against local autonomy;
- performance against comprehensibility;
- central governance against team ownership;
- consistency against speed;
- and technical ideals against the capabilities of the organization that must operate the system.

These choices are contextual.

A technically elegant microservice architecture may be a poor choice for a small team without operational maturity. A modular monolith may be preferable even when distributed components appear more sophisticated. A highly abstract platform may reduce duplication while making simple changes prohibitively difficult.

Models can summarize these trade-offs. They do not bear their consequences.

They also lack complete organizational memory.
A model may not know why a system was deliberately constrained, which failed migration shaped an existing rule, which team is overloaded, which dependency is politically difficult to replace, or which regulatory interpretation governs a particular boundary.

Architectural judgment depends on history, incentives, strategy, and accountability.

That remains scarce.

#### Architecture as Context Efficiency

Architecture gains a new economic dimension in agent-assisted development.

For an AI agent, a poorly structured codebase is expensive to understand.

If responsibilities are scattered across dozens of files, terminology is inconsistent, dependencies are implicit, and business rules are duplicated, the agent must load more context before it can make a reliable change.

More context means:

- higher inference cost;
- more irrelevant information;
- a greater probability of missing a dependency;
- a higher risk of reproducing inconsistent patterns;
- and more opportunities for reasoning to drift.

This suggests a useful architectural quality for AI-assisted engineering:

**Context efficiency:** how much relevant information must a human or agent load to make a correct change?

A modular, cohesive system reduces that burden. Clear boundaries, small interfaces, explicit schemas, architecture decision records, focused documentation, and executable constraints make a repository more legible to both humans and machines.

A well-designed system does not merely run efficiently. It can also be understood and modified efficiently.

In an AI-native environment, legibility becomes part of system economics. Anthropic's work on context engineering makes a related argument at the agent level: reliability depends on curating the information placed in the model's limited working context rather than simply maximizing the amount of available information.[^anthropic-context]

### 4. Code Review Becomes More Important Than Code Generation

As AI increases implementation speed, organizations encounter an obvious consequence:

Much more code.

Generated code still requires interpretation.

A responsible review must determine:

- Is the behavior correct?
- Does the implementation satisfy the real requirement?
- Is the change secure?
- Does it preserve architectural boundaries?
- Does it duplicate an existing abstraction?
- Are the tests meaningful?
- What assumptions does the implementation encode?
- What happens under partial failure?
- Will another engineer understand it six months later?
- Is the additional code worth owning?

These questions cannot be answered through syntax inspection alone.

AI-assisted development therefore increases the importance of program comprehension: the ability to reconstruct intent, trace behavior across layers, identify hidden coupling, and reason about consequences that are not visible in the immediate diff.

Google's engineering guidance defines the purpose of code review in terms of improving the overall health of the codebase, not merely detecting syntactic mistakes.[^google-review] That standard becomes more important as the marginal cost of generating a plausible diff falls.

This creates an asymmetry.

Models can generate code much faster than humans can understand it.

A coding agent may produce hundreds of lines in seconds. A responsible reviewer still needs time to understand the problem, inspect the change, evaluate the tests, and connect the implementation to the wider system.

The result is a supervision bottleneck. Organizations can increase production without increasing the number of people capable of reviewing the output deeply.

Increasingly, the scarce engineer is the person who can read systems, not merely write them.

#### The Supervision Paradox

This transition creates a deeper workforce problem.

Verifying AI-generated software requires experienced engineers. Effective supervision depends on pattern recognition, debugging ability, architectural intuition, domain understanding, and knowledge of common failure modes.
Historically, those capabilities were developed through years of implementation work.

Junior engineers learned by writing straightforward functions, debugging incorrect assumptions, maintaining existing systems, reviewing feedback, resolving incidents, and gradually taking responsibility for larger decisions.

If organizations automate most entry-level implementation work, they may remove the apprenticeship path through which senior judgment is formed.

This is the supervision paradox:

> AI systems increase the demand for expert supervision while reducing the work through which future experts acquire that expertise.

The solution is not to preserve boilerplate for its own sake. It is to redesign engineering education and organizational apprenticeship.

Junior engineers may need to spend more time on:

- code reading;
- failure analysis;
- test design;
- architecture reconstruction;
- incident investigation;
- model-output critique;
- controlled implementation exercises;
- and explicit comparison between generated solutions.

The goal should be to retain cognitive participation even when mechanical production is automated.

Otherwise, organizations may optimize short-term throughput while eroding their future ability to evaluate what their systems produce.

### 5. Verification Becomes the New Bottleneck

Writing software is becoming cheaper.

Proving that software behaves correctly is not.

For deterministic software, verification already requires substantial effort. Unit tests, integration tests, static analysis, code review, staging environments, observability, and incident response exist because plausible code is not necessarily correct code.

AI expands the problem.

When models participate in system behavior, failures are often non-binary. A conventional function may return the wrong value for a defined input. An AI system may perform well across most cases while failing unpredictably under subtle variations in phrasing, context, tool state, or environment.

Verification must therefore operate across distributions rather than isolated examples.

Modern AI engineering increasingly depends on:

- evaluation datasets;
- regression suites;
- trajectory inspection;
- tool-call validation;
- adversarial testing;
- groundedness checks;
- failure taxonomies;
- evaluator calibration;
- continuous production monitoring;
- and evidence collection.

Anthropic's guidance on agent evaluations recommends combining code-based, model-based, and human graders because no single evaluation mechanism captures all relevant properties of an agent's behavior.[^anthropic-evals]

The question changes from:

> Does the program pass its tests?

to:

> What evidence justifies confidence that this system will behave acceptably across the conditions that matter?

This is a more demanding standard.

It requires engineers to define acceptable behavior, model uncertainty, identify high-risk scenarios, measure regressions, and establish escalation paths for ambiguous outcomes.

Software engineering increasingly becomes the discipline of producing justified confidence.

#### From Testing to Evidence

Tests remain essential, but tests alone may not be sufficient.

An agent can satisfy a unit test while violating the intended user experience. It can produce the correct output through an unsafe tool path. It can modify the correct file while silently breaking an architectural boundary. It can declare success after validating only the easiest case.

Reliable agentic systems therefore need evidence-oriented completion criteria.

A consequential change may require:

- passing deterministic tests;
- producing a valid build;
- demonstrating expected behavior in a running environment;
- showing that the relevant user flow works;
- proving that no forbidden systems were modified;
- recording tool calls;
- attaching logs, traces, or screenshots;
- and undergoing independent review from a fresh context.

The result is an evidence-carrying change: an implementation accompanied by machine-checkable evidence that its important claims have been examined.

This shifts engineering from artifact production toward assurance production.

### 6. Harness Engineering

A crucial distinction is emerging between AI models and the systems surrounding them.

A raw model is not an autonomous software engineer. It is a probabilistic inference component.

It becomes an agent only when embedded in an execution environment that provides instructions, state, tools, memory, planning, stopping conditions, recovery behavior, permissions, observability, and feedback.

This environment is the agent harness.

The model provides generative capability.

The harness determines how that capability is directed and constrained.

A strong model inside a weak harness can produce unreliable outcomes. It may lose track of the task, call inappropriate tools, repeat failed actions, consume unbounded resources, modify the wrong files, or declare completion without adequate verification.

A cheaper or smaller model inside a carefully designed harness may perform better because the environment reduces ambiguity and detects failure. Anthropic's long-running-agent experiments explicitly found that harness design, progress artifacts, and structured handoffs materially affect whether an agent can continue useful work across context boundaries.[^anthropic-long-running] OpenAI's Codex case study similarly emphasizes repository structure, feedback loops, observability, and machine-enforced constraints around the model.[^openai-harness]

Harness engineering includes several concerns.

**Control**

How is a long task decomposed? What determines the next action? When should the system stop, retry, escalate, or request human input?

**Context**

What information is loaded, when, and why? How does the agent recover relevant history without overwhelming its context window?

**Tool mediation**

Which capabilities are available? What permissions do they carry? How are side effects validated before execution?

**Runtime**

Where does the agent operate? Is the environment isolated? Can it inspect running software? Can concurrent attempts interfere with one another?

**Verification**

How does the system test its own work? What evidence is required before completion? Is evaluation performed independently?

**Recovery**

How does the agent respond to failures, partial progress, lost context, conflicting changes, or tool errors?

**Governance**

Who authorized the action? What policies apply? What is logged? Which decisions require human approval?

These concerns are often more consequential than prompt wording.

The future of agentic software will not be determined solely by which organization has access to the strongest model. It will also be shaped by who can build the most reliable control environment around increasingly substitutable models.

### 7. Organizational Knowledge

Foundation models contain broad general knowledge.

Organizations compete on what those models do not know:

- internal processes;
- operational policies;
- customer history;
- product decisions;
- organizational relationships;
- exception-handling procedures;
- domain terminology;
- local constraints;
- and the tacit knowledge held by experienced employees.

This knowledge is usually fragmented.

Some exists in databases. Some is recorded in documents, tickets, chat threads, meeting transcripts, and source code. Much of it lives only in people's memories or in habits that were never formally documented.

Giving an AI system access to these records does not automatically give it understanding.

A ticket describes an event. It may not explain why the issue mattered.

A database contains fields. It may not encode the organizational meaning of those fields.

A repository records what changed. It may not explain the business decision that caused the change.

Organizations therefore need more than retrieval. They need structured context.

This may include:

- shared taxonomies;
- entity and relationship models;
- ontologies;
- architecture decision records;
- organizational graphs;
- data lineage;
- policy representations;
- temporal histories;
- and systems that connect decisions to the artifacts they produced.

The strategic asset is not merely access to information. It is a model of meaning.

Organizations that externalize tacit knowledge into machine-usable representations can create agents that better understand workflows, priorities, ownership, constraints, and historical rationale.

Organizations that do not will deploy agents that can retrieve records but cannot reliably interpret them.

#### Systems of Record and Systems of Context

Traditional enterprise software is organized around systems of record.

A CRM records customers. A project tracker records tasks. A source-control system records commits. A document platform stores files.

These systems answer questions such as:

- What happened?
- Who changed this?
- What value is stored?
- When was the record created?

Agents often need to answer different questions:

- Why does this matter?
- What should happen next?
- Which constraint takes precedence?
- Who is accountable?
- Which historical decision governs this situation?
- What is unusual relative to normal behavior?

These are questions of context.

A system of context does not replace systems of record. It connects them through meaning.

Building such systems may become one of the most important areas of enterprise AI engineering. It requires combining data engineering, knowledge representation, security, retrieval, organizational design, and human governance.

The competitive advantage will not come from attaching a generic chatbot to every database.

It will come from constructing an organizational model that allows AI systems to reason without bypassing the institution's accumulated knowledge and constraints.

### 8. Domain Expertise

As implementation becomes cheaper, domain expertise becomes more valuable.

This may seem counterintuitive. If models can produce code across many domains, why should specialization matter more?

Because implementation is rarely the hardest part of a high-stakes system.

In healthcare, the challenge is not merely producing an application. It is understanding clinical workflows, patient risk, evidence standards, privacy obligations, and the consequences of incorrect recommendations.

In finance, the difficulty lies not only in writing a model or service. It lies in understanding incentives, market structure, regulatory constraints, tail risk, and how apparently reasonable assumptions fail under stress.

In logistics, local optimization can degrade the whole network. A change that reduces transportation cost in one region may increase delays, warehouse congestion, or inventory volatility elsewhere.

In manufacturing, generated control software must respect physical constraints. A locally plausible decision can damage equipment or endanger workers.

AI can accelerate the translation of expertise into software.

It cannot supply accountability for the domain.

The specialist of the future may spend less time implementing routine algorithms and more time expressing domain knowledge as:

- constraints;
- simulations;
- policies;
- ontologies;
- evaluation criteria;
- decision rules;
- and auditable workflows.

The more capable the implementation machinery becomes, the more valuable it is to know what that machinery should do.

### 9. Communication

Software engineering has always been collaborative.

AI increases rather than decreases the importance of communication.

When an engineer works directly on a system, some intent remains implicit in their thought process. When work is delegated to agents, implicit knowledge becomes invisible.

An agent cannot reliably act on undocumented conventions, decisions buried in meetings, assumptions held by one senior engineer, vague instructions such as "make it production-ready," or organizational nuances that have never been externalized.

Anything important must be expressed in a form the system can retrieve and apply.
This raises the engineering value of:

- design documents;
- architecture decision records;
- precise issue descriptions;
- operational playbooks;
- interface contracts;
- evaluation rubrics;
- policy definitions;
- and structured handoff artifacts.

Technical writing becomes part of system control.

A good document does not merely explain a decision after the fact. It shapes the behavior of humans and agents before implementation occurs.

This also changes how repositories are designed.

Rather than relying on one enormous instruction file, agent-ready systems can use progressive disclosure: a compact high-level map pointing to focused documentation, schemas, constraints, and examples that are loaded only when relevant.

The purpose is not maximal documentation.

It is precise, retrievable intent.

### 10. Fundamentals

Perhaps the greatest misconception surrounding AI-assisted development is that technical fundamentals matter less.

The opposite is more likely.

Programming languages evolve. Frameworks change. Models improve. Interfaces become easier.

But abstractions continue to leak.

When an AI-generated system fails because of a race condition, memory leak, network partition, transaction anomaly, cache inconsistency, or unexpected load pattern, someone must understand what is happening beneath the generated surface.

Models can assist with diagnosis, but they can also propose plausible explanations unsupported by the actual system state. Without a strong conceptual model, the engineer cannot distinguish a useful hypothesis from a confident hallucination.

Durable foundations include:

- algorithms and data structures;
- operating systems;
- databases;
- networking;
- distributed systems;
- programming-language semantics;
- security;
- probability and statistics;
- control theory;
- optimization;
- and formal reasoning.

These concepts outlast individual tools.

The purpose of learning fundamentals is not to compete with a model at recalling syntax. It is to develop the mental structures required to evaluate generated systems.

Abstraction increases the leverage of fundamentals because failures become less visible.

Understanding survives automation.


## From Code Production to Judgment Production

Traditional software organizations often optimized for implementation efficiency.

They measured lines of code, tickets completed, pull requests merged, story points, release frequency, and feature throughput.

Some of these metrics remain useful, but AI makes them easier to inflate.

An organization can generate more artifacts without producing more value. It can merge more code while increasing fragility. It can shorten implementation time while extending review, integration, and maintenance time.

AI-native engineering must optimize for decision quality.

That means rewarding:

- clear problem framing;
- smaller and more reversible changes;
- architectural coherence;
- high-quality evaluations;
- explicit evidence;
- controlled blast radius;
- rapid recovery;
- organizational learning;
- and long-term system legibility.

The objective is not maximal generation.

It is the conversion of uncertainty into justified action.

This is judgment production.

An effective engineering process produces more than software. It produces confidence that the software is worth deploying, behaves as intended, and can continue to evolve.


## The Engineer as a System Designer

The most important shift may be conceptual.

Software engineers increasingly design systems composed of:

- humans;
- AI agents;
- deterministic software;
- data platforms;
- policies;
- organizational processes;
- evaluation systems;
- and shared knowledge.

The unit of engineering is no longer just a program.

It is an evolving socio-technical system.

A coding agent may generate an implementation. A policy engine determines whether it is permitted. A test harness evaluates deterministic behavior. An AI evaluator examines qualitative outcomes. A human reviewer handles ambiguity. An organizational knowledge layer supplies context.

Observability systems determine whether the result remains reliable in production.

The engineer's role is to design how these components interact.

This requires answering questions such as:

- Which decisions can be delegated?
- Which require deterministic enforcement?
- Which require human accountability?
- How should uncertainty be represented?
- What evidence is required before an action becomes binding?
- How does the system learn from failures?
- How are conflicting objectives resolved?
- How does knowledge remain current?
- What happens when the model, tool, or environment changes?

These are not merely programming questions.

They are questions of system design, control, governance, epistemology, and institutional architecture.


## A More Skeptical Interpretation

The argument that judgment becomes scarce should not be treated as certainty.

AI systems may improve enough to automate parts of architecture, review, evaluation, and problem decomposition that currently appear dependent on human experts. Verification tools may become substantially more capable. Models may gain larger working memories, better environmental grounding, stronger self-correction, and more reliable long-horizon execution.

Some current bottlenecks may therefore be temporary.

There is also a risk of romanticizing human judgment. Human engineers routinely produce insecure systems, misread requirements, approve flawed architectures, and accumulate technical debt without AI assistance.

The relevant comparison is not between imperfect models and ideal humans.

It is between complete engineering systems.

A well-designed human–AI system may outperform either humans or models working alone. Conversely, a poorly governed agentic workflow may scale existing organizational dysfunction.

The strongest conclusion is therefore not that particular human tasks will remain permanently protected.

It is that abundance at one layer creates demand for control at another.

Even if models become capable of more judgment, organizations will still need mechanisms for allocating authority, validating outcomes, resolving conflicting objectives, and assuming responsibility.

Scarcity may continue to migrate.

Engineering will continue to follow it.


## What Engineering Organizations Should Do

Organizations adopting AI-assisted development should avoid treating generated code volume as the primary measure of success.

A more durable strategy is to invest in the complementary systems that turn generation into reliable change.

**Strengthen repository legibility**

Use clear module boundaries, explicit interfaces, consistent domain language, architecture decision records, and focused files with coherent responsibilities.

**Build verification capacity**

Create regression suites, representative evaluation datasets, adversarial cases, production monitoring, and independent review mechanisms.

**Design agent harnesses**

Control permissions, context loading, task decomposition, stopping conditions, recovery behavior, and evidence requirements.

**Preserve apprenticeship**

Give junior engineers structured responsibility for understanding, testing, reviewing, and diagnosing systems rather than reducing their role to accepting generated output.

**Externalize organizational knowledge**

Connect policies, decisions, ownership, terminology, workflows, and historical context into representations that both humans and agents can use.

**Measure trustworthy throughput**

Track the time and cost required to move a change from intent to validated production behavior, including review, rework, incidents, and maintenance.

The organizations that benefit most from AI will not necessarily be those that generate code fastest.

They will be those that can absorb synthetic output without losing coherence.


## Conclusion

The claim that AI will replace software engineers misunderstands how technological revolutions reshape engineering work.

Automation rarely removes the need for expertise. It relocates expertise toward the remaining constraints.
As implementation becomes abundant, scarce value migrates toward:

- problem framing;
- systems thinking;
- architectural judgment;
- program comprehension;
- verification;
- harness design;
- organizational knowledge;
- domain expertise;
- precise communication;
- and technical fundamentals.

The future software engineer is not primarily a faster programmer.

They are an architect, evaluator, systems thinker, knowledge modeler, and organizational designer.

They construct the environments in which humans, models, tools, policies, and software can work together without sacrificing reliability or accountability.

The most valuable engineers of the next decade will not be those who generate the most code.

They will be those who most effectively transform uncertainty into justified engineering decisions.

> "The performance of a system depends on how its parts interact, not on how they perform separately."  
> — Russell L. Ackoff


## References and Further Reading

**Systems, organizations, and architecture**

- Donella H. Meadows, *Thinking in Systems: A Primer*.
- Peter M. Senge, *The Fifth Discipline*.
- Eliyahu M. Goldratt and Jeff Cox, *The Goal*.
- Herbert A. Simon, "Designing Organizations for an Information-Rich World".
- Martin Kleppmann, *Designing Data-Intensive Applications*.
- Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate*.
- Matthew Skelton and Manuel Pais, *Team Topologies*.
- Neal Ford, Mark Richards, Pramod Sadalage, and Zhamak Dehghani, *Software Architecture: The Hard Parts*.
- Neal Ford, Rebecca Parsons, and Patrick Kua, *Building Evolutionary Architectures*.
- Gregor Hohpe, *The Software Architect Elevator*.
- Melvin E. Conway, "How Do Committees Invent?".

**Software delivery and review**

- Titus Winters, Tom Manshreck, and Hyrum Wright, eds., *Software Engineering at Google*.
- Google Engineering Practices, "Code Review Developer Guide".
- Betsy Beyer et al., eds., *Site Reliability Engineering*.
- Google Cloud, DORA 2025 State of AI-Assisted Software Development Report.
- Kevin Storer, "How Generative AI Affects the Value of Development Work".

**Agents, harnesses, context, and evaluation**

- Anthropic, "Building Effective Agents".
- Anthropic, "Effective Context Engineering for AI Agents".
- Anthropic, "Effective Harnesses for Long-Running Agents".
- Anthropic, "Harness Design for Long-Running Application Development".
- Anthropic, "Demystifying Evals for AI Agents".
- Anthropic, "Writing Effective Tools for Agents—with Agents".
- Anthropic, "How Claude Code Is Used in Practice".
- OpenAI, "Harness Engineering: Leveraging Codex in an Agent-First World".
- OpenAI, "Unlocking the Codex Harness: How We Built the App Server".
- Datadog, "Designing MCP Tools for Agents".
- Datadog, "Bring Live Datadog Telemetry into Your AI Agents".

[^openai-harness]: OpenAI, "Harness Engineering: Leveraging Codex in an Agent-First World", February 11, 2026.
[^anthropic-expertise]: Anthropic, "How Claude Code Is Used in Practice", June 16, 2026.
[^simon]: Herbert A. Simon, "Designing Organizations for an Information-Rich World" (1971).
[^goal]: Eliyahu M. Goldratt and Jeff Cox, *The Goal*.
[^dora-2025]: Google Cloud, DORA 2025 State of AI-Assisted Software Development Report.
[^meadows]: Donella H. Meadows, *Thinking in Systems*.
[^anthropic-context]: Anthropic, "Effective Context Engineering for AI Agents", September 29, 2025.
[^google-review]: Google Engineering Practices, "The Standard of Code Review".
[^anthropic-evals]: Anthropic, "Demystifying Evals for AI Agents", January 9, 2026.
[^anthropic-long-running]: Anthropic, "Effective Harnesses for Long-Running Agents", November 26, 2025, and "Harness Design for Long-Running Application Development", March 24, 2026.
