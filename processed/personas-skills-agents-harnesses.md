# Personas, Skills, Agents, and Harnesses in AI System Design

Persona prompting became popular because it is ergonomic.
"Act as a senior software architect" is easy to write, easy to remember, and easy to teach. It compresses tone, vocabulary, priorities, and expected behavior into a familiar human label. That compression is useful. It is also the problem.
A persona is not a procedure. It does not define what evidence counts, what checks must be performed, which tools are allowed, when the task is complete, or how failure should be recovered from. It gives the model a role to imitate, not a system of work to execute.
That distinction matters more as AI systems move from chat interfaces into tool-using agents. In a chatbot, a vague persona usually produces a vague answer. In an agentic system, the same vagueness can produce bad tool calls, unsafe confidence, role-play over execution, and traces that are difficult to audit.
The useful abstraction is not "persona prompting." It is a stack:
persona → lens → skill → agent → harness
A persona shapes interaction style. A lens defines a viewpoint. A skill encodes a repeatable procedure. An agent gives that procedure tools, state, and branching behavior. A harness surrounds the agent with tracing, guardrails, recovery, and evaluation.
The engineering question is not whether personas work. Sometimes they do. The better question is:
What is the cheapest abstraction that satisfies the task's reliability requirement?
Persona prompting is useful, but easy to overinterpret
Most teams have used prompts like these:
Act as a senior software architect.
Act as a skeptical reviewer.
Act as a product strategist.
Act as a legal expert.
These prompts often work well enough to feel powerful. The model changes tone. It uses different vocabulary. It may emphasize different risks. It may become more structured, cautious, or domain-specific.
That effect is real. The prompt-pattern literature helped formalize persona prompting as a reusable technique; White et al.'s Prompt Pattern Catalog explicitly includes a Persona pattern, turning "act as X" from an ad hoc trick into a teachable recipe. Shanahan, McDonell, and Reynolds later argued in Nature that dialogue-agent behavior can be usefully understood as role-play, without implying that the model literally has a stable self.
But the evidence does not support the stronger claim that personas reliably improve core capability.
Zheng et al. tested 162 roles across 2,410 factual questions and found that personas in system prompts did not improve overall performance in When "A Helpful Assistant" Is Not Really Helpful. Kong et al. found that role-play prompting can improve zero-shot reasoning on some benchmarks in Better Zero-Shot Reasoning with Role-Play Prompting, but the result is task-dependent. Kim et al. describe persona prompting as a double-edged sword in Persona is a Double-Edged Sword: sometimes helpful, sometimes harmful, and strongest when persona and neutral outputs are compared rather than blindly trusting one role prompt.
A more recent study, When Does Persona Prompting Actually Help?, points to a useful interpretation: persona prompting often changes response characteristics, such as depth, caution, and framing, but does not universally improve answers. In some domains and task types, especially advisory interactions, expert role prompting can add useful depth. In other cases, neutral prompting produces clearer explanations.
That is the right reading: personas are useful as lightweight lenses for style, salience, and conversational UX. They are not reliable substitutes for procedures, tools, checks, or evals.
Persona prompting is often a sophisticated way of being vague.
What personas actually control
Personas mostly control the interaction layer.
They influence tone, vocabulary, framing, salience, conversational posture, and implied priorities. They are useful when the primary problem is communicative: make this more executive, review this as a teacher, challenge this as a skeptical engineer, explain this like a patient tutor.
That is a legitimate use. A persona is a UX primitive. It helps users tell the system what kind of interaction they expect.
But personas do not reliably control correctness, reasoning process, evidence quality, safety behavior, tool choice, reproducibility, or recovery from failure. For those properties, role labels are too soft. They suggest behavior; they do not constrain execution.
This distinction is now visible in official engineering guidance. OpenAI's prompt guidance separates personality from collaboration style and states that personality should shape user experience, while collaboration instructions shape task behavior; neither should replace goals, success criteria, tool rules, or stopping conditions. Anthropic's effective context engineering argues that building agents is becoming less about finding the right prompt wording and more about configuring the right context: instructions, tools, external data, message history, and state. Google's ADK safety guidance lists ambiguous agent instructions, prompt injection, and indirect prompt injection via tool use as core risks in agent systems.
The conclusion is not that personas are useless.
The conclusion is that personas are useful at the wrong layer if treated as the core architecture.
A persona is interface design. Reliability needs work design.
The stack: persona, lens, skill, agent, harness
A better way to design AI systems is to separate five layers.
Persona
A persona defines role and interaction style.
Sound like a principal engineer.
This mostly affects tone, vocabulary, implied seniority, and conversational posture. It is helpful for UX. It is weak as a control mechanism.
Lens
A lens defines a constrained viewpoint.
Review this from the perspective of production readiness.
A lens is narrower than a persona. It does not ask the model to role-play a person. It asks the model to privilege a specific evaluative angle: security, maintainability, product risk, user empathy, compliance, operational readiness.
A lens is often the useful part hidden inside a persona prompt.
"Act as a principal engineer" might really mean: "look for production risks, coupling, unclear ownership, observability gaps, and rollback issues."
If that is what you want, say that.
Skill
A skill defines a repeatable procedure with checks.
Extract assumptions, identify coupling, inspect failure modes, check rollback and observability, then return blocking issues and next steps.
A skill turns an implied capability into an explicit work contract. It defines the goal, inputs, procedure, output schema, and checks. It can be versioned. It can be tested. It can be improved.
This matches OpenAI's framing in Testing Agent Skills Systematically with Evals, where an eval is described as a prompt, a captured run with trace and artifacts, a set of checks, and a score that can be compared over time.
A persona says, "be good at this."
A skill says, "do these steps and satisfy these checks."
Agent
An agent gives the skill tools, state, and branching behavior.
Use the repository, architecture docs, issue tracker, and deployment notes to complete the review.
At this layer, the system is no longer just producing text. It is retrieving context, calling tools, deciding what to inspect, handling partial information, and adapting the path based on observations.
LangChain's workflows and agents distinction is useful here: workflows follow predetermined paths, while agents dynamically decide their own process and tool usage. Once the system has that freedom, prompt wording alone is not enough. The system needs tool policies, trajectory evaluation, state management, and failure handling.
Harness
A harness surrounds the agent with orchestration, tracing, guardrails, recovery, and evaluation.
Trace every step, enforce tool permissions, check claims against retrieved evidence, run a critic pass, and store the result for regression comparison.
This is the reliability layer.
The harness defines what the agent is allowed to do, what must be recorded, what requires verification, when to retry, when to stop, and how to compare behavior across versions.
The harness is where agentic work becomes inspectable.
If you cannot inspect the trajectory, you do not have a reliable agent.
If you cannot rerun the eval, you do not have an engineering artifact.
The central failure mode: collapsing layers
The common bad pattern is to collapse all layers into a single role prompt.
You are a principal engineer. Review this system.
That prompt may be fine for informal use. It might produce a useful answer. The problem is not that it is wrong. The problem is that it hides too much.
It hides the lens. It hides the procedure. It hides the evidence standard. It hides the output contract. It hides the tool policy. It hides the stopping condition. It hides the difference between observed facts, inferred risks, and speculative recommendations.
A better design separates the layers:
Persona: principal engineer
Lens: production readiness
Skill: architecture review
Agent tools: repository search, documentation retrieval, issue lookup
Harness: trace capture, claim grounding, critic pass, permission policy, regression comparison
The first version is easy to demo. The second version is easier to debug.
This is the same pattern software teams have seen before. Scripts become workflows. Workflows become services. Services need observability, tests, deployment discipline, rollback, and ownership. The cheap abstraction becomes dangerous when it starts carrying operational responsibility.
AI systems follow the same path.
A persona is cheap. A lens is still cheap. A skill adds structure. An agent adds runtime power. A harness adds supervision and reliability machinery. The goal is not to maximize abstraction. The goal is to choose the cheapest abstraction that meets the task's reliability requirement.
Why this matters more for agents than chatbots
In plain chat, a bad persona prompt usually produces a bad answer.
In an agentic system, a bad role instruction can produce bad actions.
The model may call the wrong tool. It may call a tool unnecessarily. It may infer state that does not exist. It may confuse advice with execution. It may continue after a recoverable error because the persona says to be "proactive." It may role-play confidence instead of checking evidence.
Tool use changes the risk profile.
Google's ADK safety documentation explicitly names ambiguous instructions, prompt injection, jailbreak attempts, and indirect prompt injection via tool use as sources of agent risk. Recent MCP security research also points in the same direction: AI-assisted development tools with tool access can be exposed to prompt-injection and tool-poisoning attacks, especially when external content and tool descriptions become part of the agent's context. See Are AI-assisted Development Tools Immune to Prompt Injection?.
Once a model can act, persona prompting becomes part of the attack surface.
A role prompt can create unsafe confidence. It can blur permissions. It can make the model behave as if it has authority it does not have. It can also interact badly with prompt injection, retrieved documents, tool descriptions, and developer instructions.
This does not mean personas should disappear. It means they should be demoted to the UX layer.
For agentic AI, reliability has to live in the harness.
Evaluation is the missing layer
The taxonomy becomes useful only if it can be tested.
That is the purpose of PromptStackBench.
PromptStackBench evaluates when a persona should become a skill, when a skill should become an agent, and when an agent needs a harness. It runs the same task through five control abstractions — persona, lens, skill, agent, harness — and compares the outputs on correctness, clarity, stability, safety, tool-use quality, cost, latency, and trace quality.
The important part is the experimental design.
Same task.
Same model.
Same input.
Different control layer.
The first treatment is persona-only:
Act as a principal engineer and review this design.
The second treatment is lens-only:
Review this design from the perspective of production readiness.
The third treatment is a skill card:
Identify assumptions, coupling, failure modes, data boundaries, observability gaps, rollout risks, rollback gaps, and unresolved ownership questions. Return blocking issues, non-blocking risks, and next steps.
The fourth treatment is an agent spec:
Use repository search, architecture docs, issue history, and deployment notes. Retrieve evidence before making claims.
The fifth treatment is a harnessed agent:
Enforce tool permissions. Trace every step. Mark unsupported claims. Run a critic pass. Validate output schema. Store the trace and final result for regression comparison.
This turns the taxonomy into something measurable. The question is no longer:
Which prompt gets the best answer?
The better question is:
At what task complexity does each abstraction stop being enough?
That is a different kind of evaluation. It treats prompting as systems design, not wordsmithing.
What PromptStackBench explores
PromptStackBench is a proof-of-concept benchmark for the prompt stack.
The current project is designed as a Python CLI tool backed by SQLite. It loads task suites and taxonomy specs from YAML, runs prompt/control variants through LLM providers, captures outputs and traces, scores them with an evaluator pipeline, and generates comparison reports.
The core architecture is intentionally simple:
datasets/         Task suites
specs/            Taxonomy specs
src/              Python source
tests/            Test suite
SQLite            Run, output, trace, and score storage
HTML/Markdown     Comparison reports
The design goal is not to build a full agent platform. The goal is to produce a small, reproducible benchmark that can answer one narrow question: when does an additional control layer pay for itself?
The repo explores four practical dimensions.
First, it explores control abstraction. Persona, lens, skill, agent, and harness are treated as competing treatments, not vague conceptual categories.
Second, it explores task-conditional value. The benchmark is not trying to prove that one layer is always superior. It asks whether a layer is sufficient for a class of tasks: architectural review, explanation, advisory work, research synthesis, document-grounded QA, tool-use planning, and eventually adversarial or malformed-input tasks.
Third, it explores promotion value. The planned promote command compares the improvement from moving up a layer against the added operational cost. That matters because adding structure is not free. Skill cards cost more to design than persona prompts. Agents cost more to run than static prompts. Harnesses add latency, evaluation complexity, and implementation overhead.
Fourth, it explores reproducibility. PromptStackBench is designed around repeated runs, paraphrases, trace, and reports. That directly addresses one of the main weaknesses of persona prompting: a single good demo does not prove stability.
The roadmap is phased.
The v0.1.0 milestone focuses on static prompt comparison: persona, lens, and skill. It includes task loading from YAML, an LLM runner, CLI commands, final-answer evaluators, schema validity, hallucinated-claim checks, instruction adherence, paraphrase stability, and Markdown/HTML reports.
The v0.2.0 milestone adds tool-using agents. This introduces mock tools, research synthesis, document-grounded QA, tool-use planning, correct tool choice, unnecessary tool-call detection, evidence grounding, and trajectory quality.
The v0.3.0 milestone adds harness evaluation. This introduces retry, critic passes, schema repair, prompt-injection checks, tool-permission checks, trace scoring, recovery rate, safety violations, trace completeness, auditability, and cost increase.
That sequence is important. It avoids jumping straight into agent orchestration before the lower layers are measurable.
Start with persona vs lens vs skill.
Then add tools.
Then add harness behavior.
That is the right order if the point is evaluation rather than demo-building.
A concrete example: architecture review
Consider a design review task.
A product team shares a short architecture proposal for a new internal tool. They want feedback before implementation.
A persona-only prompt might say:
Act as a principal engineer. Review this architecture.
The output may sound senior. It may mention scalability, maintainability, observability, and security. It may be useful.
But there is no guarantee it checked the important things.
A lens-only prompt improves the direction:
Review this architecture from the perspective of production readiness.
Now the answer is more focused. It is less about sounding senior and more about evaluating a specific property.
A skill prompt makes the work inspectable:
Extract explicit assumptions. Identify hidden coupling. Check failure modes, rollback, observability, security, cost, and ownership. Separate blocking issues from non-blocking risks. Cite evidence from the proposal for every blocking issue. Do not invent requirements not present in the brief.
This is now closer to a review procedure.
An agent spec becomes useful when the review depends on external context:
Use repository search, architecture docs, previous incident notes, and deployment history. Retrieve evidence before making claims. Separate observed evidence from inference.
Now the system can do work beyond the provided prompt.
A harness becomes necessary when the result matters operationally:
Enforce read-only tools. Record every retrieval and tool call. Mark unsupported claims. Run a critic pass for missing failure modes. Validate the output schema. Store the trace for future regression comparison.
At that point, the review is no longer just a text response. It is an auditable work product.
The promotion rule
The taxonomy needs a decision framework.
Use a persona when the task is mostly about voice.
Use a lens when the task needs a viewpoint.
Use a skill when the task is repeatable.
Use an agent when the task needs tools, state, or branching.
Use a harness when failure must be traced, recovered from, or prevented.
The sharper version:
If you cannot define checks, you do not have a skill.
If you cannot inspect the trajectory, you do not have a reliable agent.
If you cannot rerun the eval, you do not have an engineering artifact.
This rule prevents two opposite mistakes.
The first mistake is under-engineering: using personas for tasks that need procedures, evidence, tools, or auditability.
The second mistake is over-engineering: building agents and harnesses for tasks where a simple persona or lens would be enough.
Both are expensive. Under-engineering creates hidden failure. Over-engineering creates unnecessary machinery.
The right abstraction is the cheapest one that meets the required reliability bar.
What this changes for AI teams
The practical implication is that teams should stop treating prompt libraries as the main artifact.
A prompt library full of "act as…" templates can improve UX, but it does not create a durable capability system. Teams need a capability registry instead.
That registry should include:
personas for interaction style
lenses for review perspectives
skill cards for repeatable procedures
tool permission policies
agent specifications
eval suites
trace stores
regression reports
promotion criteria from skill to agent to harness
This changes the operating model.
From prompt library to capability registry.
From role-play to repeatable work.
From impressive demos to inspectable behavior.
From "which prompt sounds better?" to "which abstraction satisfies the reliability requirement?"
This also changes how AI teams should work with business teams. Business users often describe needs in persona language: "I want a legal reviewer," "I want a product strategist," "I want a senior engineer looking at this."
That language is useful as a starting point. But the AI engineering job is to translate the request downward.
What does this role actually need to check?
What evidence does it need?
What tools does it need?
What state does it need to remember?
What failures are acceptable?
What failures require escalation?
What traces must exist after execution?
The business asks for a persona. The engineering team ships a capability.
Conclusion
Personas are not obsolete. They are just not the unit of reliability.
They remain useful as an interface layer. They help shape tone, framing, and expectations. They make systems easier to use. But they should not be confused with procedures, tools, state, evaluation, or control.
The future is not better personas.
The future is structured capabilities: skills for repeatable work, agents for tool- and state-bearing execution, and harnesses for traceability, safety, recovery, and improvement.
PromptStackBench is a small proof of concept for that shift. It treats persona, lens, skill, agent, and harness as testable control layers rather than prompt-writing styles. It asks when each layer is enough, when it stops being enough, and when the additional structure is justified.
That is the real prompt stack.
Not because abstraction should make systems vaguer, but because the right abstraction gives us a place to be precise.
As Dijkstra put it:
"The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise."
References
White et al., A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT
Shanahan, McDonell, Reynolds, Role play with large language models
Zheng et al., When "A Helpful Assistant" Is Not Really Helpful
Salewski et al., In-Context Impersonation Reveals Large Language Models' Strengths and Biases
Kong et al., Better Zero-Shot Reasoning with Role-Play Prompting
Kim et al., Persona is a Double-Edged Sword
Lutz et al., The Prompt Makes the Person(a)
Yang et al., What Prompts Don't Say
Sclar et al., Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design
Liang et al., Holistic Evaluation of Language Models
OpenAI, Prompt guidance
OpenAI, Testing Agent Skills Systematically with Evals
OpenAI, Agents SDK
Anthropic, Effective context engineering for AI agents
Google ADK, Safety and Security for AI Agents
Google AI for Developers, Prompt design strategies
LangChain, Workflows and agents
LangChain, Application-specific evaluation approaches
rmax-ai, PromptStackBench
