# Recursive Execution Is the Missing Layer for Long-Running Agents

External state -> recursive execution -> verification -> traceable answer

This is the missing layer between a model and a production system. It is also the layer that makes long-running work economically viable. If the model has to reason through every tool invocation on every run, the cost grows with the number of actions. If the model can produce a reusable workflow blueprint, subsequent executions can be deterministic, cheaper, and easier to audit.

A recent MCP Workflow Engine paper makes this separation explicit. It argues for decoupling intelligence from execution: the agent reasons once to create a declarative workflow blueprint containing tool calls, templates, loops, branches, and data piping; later runs execute the workflow without re-involving the model at every step. In its Kubernetes CMDB synchronization case study, the system reduced per-execution token cost by more than 99% while executing a 67-step workflow deterministically. (arXiv)

That result should not be read as a universal benchmark. It should be read as a design signal: once a task has a stable structure, the model should stop improvising the whole procedure. It should compile the procedure into an execution artifact.

## Long-running agents need bounded interfaces

One reason coding agents improved quickly is that software gives agents feedback. Code can compile. Tests can pass. Linters can reject invalid edits. Git diffs can be inspected. These are not just developer conveniences; they are control surfaces.

The SWE-agent paper made this point through the idea of an Agent-Computer Interface. Instead of exposing the model to an unconstrained shell, SWE-agent gives it a specialized interface for navigating repositories, editing files, and running checks. The paper's broader lesson is that models are not only sensitive to prompts; they are sensitive to the shape of the environment in which they act. A better interface can make the same model behave more reliably. (arXiv)

That is the same principle behind recursive execution. The agent should not be given a raw operating system, raw database, raw document dump, or raw enterprise API surface. It should be given typed, bounded, inspectable operations.

A useful long-running agent interface should have five properties:

1. It should expose references instead of raw blobs.
2. It should limit action space.
3. It should validate outputs structurally.
4. It should record every meaningful transition.
5. It should make unsafe actions impossible or explicitly gated.

This is not anti-agent. It is the condition under which agents become useful.

## Skill libraries are externalized memory

Voyager showed an early version of this pattern in an embodied environment. It used an automatic curriculum, iterative prompting, environment feedback, and a growing library of executable skills. The important part is not Minecraft. The important part is that learned behavior was stored as executable code, not as vague conversational memory. This allowed the system to reuse behaviors and compound capability without updating model weights. (arXiv)

That is a critical distinction for enterprise systems. "Memory" should not mean dumping a summary into the next prompt. Some memory should be code. Some should be evidence. Some should be policy. Some should be workflow state. Some should be user preference. Some should be provenance metadata.

Recursive execution makes these distinctions explicit. It asks: what kind of state is this, who owns it, how is it retrieved, how is it verified, and when is it safe to reuse?

## AutoHarness points to the next step

Harnesses are the control code around the model. They filter actions, validate outputs, retry failures, constrain search, and sometimes replace model decisions with deterministic procedures.

AutoHarness pushes this idea further. The paper shows that an LLM can synthesize a custom code harness from environment feedback, preventing illegal actions across TextArena games. In some settings, the generated harness becomes strong enough to replace model calls at decision time. (arXiv)

The deeper implication is not that every agent should synthesize its own production harness unsupervised. That would be reckless. The deeper implication is that many agent failures are not intelligence failures. They are control failures.

The model may know the right kind of thing to do, but the execution environment lets it do impossible, invalid, unsafe, redundant, or unverified actions. A harness turns those failure modes into software boundaries.

This matters for long-running agents because failures compound. A single invalid move in a short task is annoying. A single invalid move inside a six-hour workflow can corrupt the entire run. Recursive execution reduces the blast radius by forcing work through bounded steps, typed outputs, and verification gates.

## The problem with long-running agents

The more an agent runs, the more it accumulates: user instructions, retrieved documents, tool outputs, failed attempts, intermediate plans, policy constraints, code diffs, logs, test results, and summaries of summaries. Eventually the session becomes less like a clean workspace and more like a polluted terminal scrollback.

Large context windows help, but they do not remove the problem. They increase how much text can be passed to the model; they do not guarantee that the model can retrieve, reason, and act reliably across the whole span. In agent systems, the problem is worse than simple retrieval. The agent must preserve causal state: what it already tried, which evidence supports which claim, what tools were called, which actions are still pending, which permissions apply, and which verification checks failed.

This is why final-answer evaluation is insufficient. For real agents, we need to know how an output was produced: which evidence supported it, which tools were used, how memory affected later decisions, where failure originated, and whether the final answer is traceable to the execution path. Recent work on evidence tracing and execution provenance frames this explicitly: agent trust requires connecting retrieved evidence, tool outputs, memory items, intermediate claims, actions, and final answers into an auditable execution graph. (arXiv)

Long-running agents therefore need something stronger than conversation history. They need an execution substrate.

## Recursive execution, not recursive chatting

Recursive execution means the agent does not carry the whole world in its prompt. It operates over references.

Instead of pasting ten thousand documents into a context window, the system stores those documents externally and gives the agent handles. Instead of asking the model to remember every previous action, the system writes actions and observations into a trace store. Instead of letting one agent perform a fragile sequence of tool calls, the system decomposes the task into bounded workers, each with a narrow input, narrow output, and explicit verification step.

The pattern looks like this:

```
Task
  -> plan
  -> create references
  -> dispatch bounded subtasks
  -> collect evidence
  -> verify intermediate outputs
  -> synthesize final result
  -> emit trace
```

This is close to how serious software systems already work. A database query does not paste the entire database into the application. A workflow engine does not rely on a worker process remembering every prior step. A compiler does not keep source code, intermediate representation, optimization passes, and machine code as one giant natural-language transcript. It externalizes state and passes structured artifacts between phases.

Agents need the same move.

## The core architectural shift

The old pattern is:

```
More context -> better answer
```

The new pattern is:

```
External state -> recursive execution -> verification -> traceable answer
```

## Durable execution is the production boundary

A long-running agent cannot depend on process memory. Processes crash. Networks fail. Model providers rate-limit. Tool calls time out. Humans take hours or days to approve an action. If the agent's state lives only inside an in-memory loop or chat session, the system is fragile by design.

Durable execution systems solve this by separating deterministic workflow logic from non-deterministic activities. In Temporal's model, workflows coordinate state and control flow, while activities perform side effects such as network calls, file operations, model calls, or database writes. The workflow can be replayed from recorded history, while activities are retried and managed separately. (arXiv)

For AI agents, this separation is not optional. Model calls are non-deterministic activities. Tool calls are non-deterministic activities. Human approvals are delayed external events. Sandboxes are provisioned resources. Retrieval calls may return changing results. The orchestration layer must survive all of that.

A production long-running agent should therefore look less like this:

```
while not done:
    ask model what to do next
    execute whatever it says
    append result to chat
```

And more like this:

```
workflow:
    load task state
    call planner activity
    persist plan
    dispatch worker activities
    persist observations
    run verification activities
    request human approval if needed
    commit only after policy and verification pass
```

The agent may still reason. But the system owns execution.

## Policy belongs outside the prompt

Prompt-based rules are weak control mechanisms. They are useful for shaping behavior, but they should not be the enforcement boundary for actions that touch files, money, customer data, infrastructure, or production systems.

Policy-as-code moves authorization decisions out of the model and into a deterministic policy engine. Open Policy Agent uses Rego for policy evaluation over structured input, while Cedar was designed as a fast, analyzable authorization language with a formal model and an open-source Rust implementation. (arXiv) (arXiv)

For agents, this means every tool call should be evaluated as a structured decision:

```json
{
  "user": "alice",
  "agent": "research-agent",
  "tool": "send_email",
  "resource": "customer-thread",
  "action": "write",
  "risk": "external_side_effect",
  "evidence": ["approval-123", "policy-check-456"]
}
```

The model can propose. The policy engine decides whether the action is allowed. The workflow engine decides when it executes. The trace store records what happened. The human approval layer intervenes when accountability cannot be delegated.

That is the difference between an agent demo and an agent system.

## MCP is useful, but not sufficient

The Model Context Protocol matters because it gives agents a common way to connect to tools, resources, and external systems. It standardizes part of the boundary between model clients and tool servers. But MCP alone does not solve governance. It exposes capability; it does not automatically define safe execution.

The useful pattern is MCP plus recursive execution:

- MCP exposes tools.
- The workflow engine sequences them.
- The policy layer gates them.
- The evidence store traces them.
- The verifier checks their outputs.
- The human approval layer handles high-risk decisions.

This is why MCP-native workflow engines are interesting. They shift the model from repeatedly deciding every tool call to producing reusable execution blueprints. (arXiv)

But once agents can call tools across enterprise systems, provenance becomes more important, not less. Recent work on source-aware verification for MCP agents highlights a subtle failure mode: an answer can be supported somewhere but attributed to the wrong source. The authors call this cross-source conflation and propose checking claims against source-specific evidence captured in MCP traces. (arXiv)

That is exactly the kind of bug recursive execution should make visible. If every claim, tool output, and source reference is stored as a traceable artifact, source confusion becomes diagnosable. If everything is compressed into a chat transcript, it becomes guesswork.

## Observability is part of the control plane

Traditional observability tracks requests, latency, errors, and resource usage. Agent observability must track more: model calls, token usage, tool calls, retrieved chunks, intermediate decisions, policy checks, verification results, retries, human approvals, and final claims.

This is why OpenTelemetry GenAI conventions and OpenInference-style tracing matter. They point toward a shared vocabulary for tracing LLM calls, tool use, retrieval, and agent workflows. The document you produced correctly identifies this as a core production requirement: without traces, teams cannot debug runaway loops, cost explosions, hallucinated claims, failed tool calls, or policy violations.

Recursive execution depends on observability because it treats traces as first-class artifacts. A trace is not just a log. It is the evidence needed to answer four questions:

1. What did the agent know?
2. What did it do?
3. Why was it allowed?
4. How was the result verified?

If a system cannot answer those questions, it is not ready for serious long-running work.

## Continual learning comes after the harness

There is a temptation to jump from agent traces directly to fine-tuning. That is premature.

Trace collection is necessary for continual improvement, but model training is only one possible use of traces. Often the first improvements should be made in the harness: better tool schemas, narrower action spaces, stronger validators, clearer state machines, better retrieval, stricter policy checks, or more precise verification metrics.

Fine-tuning becomes attractive only when the task is stable, repetitive, high-volume, measurable, and expensive enough to justify model adaptation. Before that, the smarter move is eval-driven harness improvement.

The sequence should be:

1. Build recursive execution.
2. Capture traces.
3. Define process-level evals.
4. Improve harness and tools.
5. Only then consider fine-tuning or reinforcement learning.

This is the practical version of continual learning for enterprise agents. The organization learns first through traces and harness changes. The model learns later, if the economics justify it.

## The software project: Recursive Execution Harness Lab

The companion proof of concept should compare two ways of solving the same long-running task.

The baseline is a long-context agent:

- Put all available material into context.
- Ask the model to solve the task.
- Let the session grow.
- Evaluate the final answer.

The experimental system is a recursive execution harness:

- Store material externally.
- Give the agent references.
- Generate a plan.
- Dispatch bounded workers.
- Write evidence.
- Verify intermediate outputs.
- Synthesize the final answer.
- Emit a provenance trace.

A minimal architecture:

```
Task Intake
  -> Planner
  -> Reference Store
  -> Recursive Executor
  -> Worker Runs
  -> Evidence Store
  -> Verifier
  -> Policy Gate
  -> Final Answer + Trace Report
```

The first benchmark should be multi-document research synthesis because it naturally exposes the weaknesses of long-context execution.

The same task can be run in two modes: one model with a large prompt, and one model using references, workers, evidence storage, and verification.

The evaluation should measure:

- Correctness
- Evidence coverage
- Unsupported claims
- Source attribution errors
- Token cost
- Wall-clock time
- Number of tool calls
- Retries
- Trace completeness
- Failure recoverability

The point is not to prove that recursive execution always wins. The point is to identify when it wins, why it wins, and which failure modes remain.

A second benchmark can use codebase investigation. A third can use policy-constrained enterprise workflows such as expense approval or support-ticket routing. Those domains matter because they include side effects, permissions, and audit requirements.

## The practical thesis

The future of long-running agents is not one giant agent with one giant context window. It is a smaller orchestrator operating over externalized state.

The agent should not remember every document. It should hold references.

The agent should not manually repeat every workflow. It should compile reusable execution plans.

The agent should not enforce policy through self-discipline. It should pass through deterministic gates.

The agent should not ask us to trust the final answer. It should produce the trace.

Recursive execution is the missing layer because it changes the unit of reliability. The unit is no longer the prompt. It is the execution path.

That shift matters. Prompting made agents impressive. Recursive execution will make them inspectable, recoverable, governable, and cheap enough to run.

## References

- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/abs/2606.04990) — Yiqi Wang et al., arXiv, 2026.
- [Separating Intelligence from Execution: A Workflow Engine for the Model Context Protocol](https://arxiv.org/abs/2605.00827) — Abhinav Singh Parmar, arXiv, 2026.
- [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) — John Yang et al., arXiv, 2024.
- [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) — Guanzhi Wang et al., arXiv, 2023.
- [AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness](https://arxiv.org/abs/2603.03329) — Xinghua Lou et al., arXiv, 2026.
- [ProvenanceGuard: Source-Aware Factuality Verification for MCP-Based LLM Agents](https://arxiv.org/abs/2606.18037) — Ander Alvarez et al., arXiv, 2026.
- [Cedar: A New Language for Expressive, Fast, Safe, and Analyzable Authorization](https://arxiv.org/abs/2403.04651) — Joseph W. Cutler et al., arXiv, 2024.
- [Prose2Policy: A Practical LLM Pipeline for Translating Natural-Language Access Policies into Executable Rego](https://arxiv.org/abs/2603.15799) — Vatsal Gupta and Darshan Sreenivasamurthy, arXiv, 2026.
- [Temporal: Durable Execution Solutions](https://temporal.io/)
- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/)
- [Open Policy Agent documentation](https://www.openpolicyagent.org/)
- [Continual Learning for Long-Running Agents: Agents That Keep Getting Better](https://youtu.be/SVWmuJx0hHM) — Jackmanong (Founding Research Engineer at Prime Intellect), hosted by NVIDIA Developer.
