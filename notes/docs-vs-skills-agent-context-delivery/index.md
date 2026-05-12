---
title: "Agent-Optimized Docs vs Skills: What Actually Improves Coding Agent Performance"
slug: "docs-vs-skills-agent-context-delivery"
description: "An evidence-backed technical note on when passive agent-optimized documentation outperforms skills, and how to structure context delivery for reliable coding-agent workflows."
author: "Max"
site: "rmax.ai"
section: "notes"
type: "technical-note"
status: "published"
date: "2026-05-12"
updated: "2026-05-12"
tags: ["agents", "documentation", "skills", "context-engineering", "reliability", "evaluation"]
reading_time: "6–8 min"
canonical_url: "https://rmax.ai/notes/docs-vs-skills-agent-context-delivery/"
license: "CC BY 4.0"
---

# Agent-Optimized Docs vs Skills: What Actually Improves Coding Agent Performance

Agents do not reliably improve just because they are given more instructions, more tools, or more elaborate skill systems. The narrower operational claim is stronger: coding agents perform better when the right context is available at the right moment, compressed enough to remain usable, and evaluated continuously.

Across reported vendor evals, benchmarks, and workflow studies, passive context layers such as `AGENTS.md` or agent-optimized documentation often outperform skills when skill routing is unreliable or the skill content has drifted. Skills still matter, but only when they are narrow, current, and verified against real tasks.

## Core Thesis

Canonical docs should remain the source of truth. Passive context should provide the always-on orientation layer. Skills should be treated as evaluated accelerators for narrow workflows, not as a replacement for documentation.

A weaker version of this thesis would say only that docs are simpler. That is true but incomplete. The stronger claim is that passive context often wins because it removes an activation step. Skills can outperform docs, but only when they are reliably invoked, aligned with the current system, and continuously validated against baseline behavior.

## Why This Matters

Agent workflows have moved from prompt experiments to production tooling. The question is no longer whether context helps. The practical question is which delivery mechanism remains dependable under operational conditions.

Modern coding agents can consume passive instruction files, retrieve documentation on demand, invoke tools, and load reusable skills. In theory, that should make skills superior because they package task-specific guidance. In practice, each retrieval or routing decision adds another failure point. If the agent does not trigger the skill, or triggers the wrong one, the system loses before the task begins.

Reported results from Wix and Vercel make this visible. Both found that always-available, compressed context can outperform skills when activation is inconsistent. At the same time, benchmarks such as SkillsBench show that good skills do help, provided they are curated, scoped, and tested. The operational question is therefore not "docs or skills?" but "which context layer fails less often in live use?"

## Mechanism

A useful model is to treat agent performance as a function of four properties of context:

1. Accuracy
2. Availability at decision time
3. Compression
4. Ongoing evaluation

Accuracy is the simplest requirement. If the context is stale or mismatched to the actual codebase, it degrades performance even if it is well written.

Availability matters because agents are sensitive to what is present in the working set when they plan the next action. Passive context files such as `AGENTS.md` or compressed documentation indexes are available immediately. Skills, by contrast, depend on routing or explicit invocation. That makes them more powerful in principle, but less reliable in practice.

Compression matters because verbose guidance competes with the task itself. A large body of best practices, examples, and caveats can dilute the signal. Compressed docs or reduced skills often perform better because they present fewer distractions and consume fewer tokens.

Evaluation is the control loop that keeps either mechanism useful. A skill is not good because it reads well. It is good if it improves success rate, token use, turn count, or elapsed time on real tasks without introducing regressions. The same standard applies to docs.

This leads to a simple architecture:

```text
Canonical docs
  -> agent-optimized docs / llms.txt / AGENTS.md index
  -> generated skills for repeatable workflows
  -> eval harness comparing baseline modes
  -> executable guardrails for hard constraints
```

The ordering matters. Docs come first. Skills are derived artifacts, not a second knowledge system maintained by hand.

## Concrete Examples

### Example 1: Passive context beating skills

Vercel's Next.js 16 API evals provide the clearest demonstration. A compressed 8 KB docs index placed in `AGENTS.md` achieved a 100% pass rate. Skills reached 79% only when explicitly instructed, and default skills performed the same as having no docs at all: 53%.

The important lesson is not that skills are useless. It is that passive context removes the routing failure mode. Once the docs index was always present, the agent no longer had to decide whether to fetch or invoke the right auxiliary guidance before acting.

Vercel also found that compressing an initial 40 KB docs injection down to 8 KB preserved the 100% pass rate. That reinforces a second point: more context is not automatically better. Better compression can improve reliability without reducing effectiveness.

### Example 2: Docs and skills helping in different ways

Wix's evals show a more balanced pattern. Agent-optimized docs improved CLI task completion from 67% to 87%, while reducing average token use by 35% and wall-clock time by 9%. Skills helped on aligned tasks, reducing tokens by 30% to 50% and time by 30%, but stale or misaligned skills underperformed docs-optimized runs.

Their REST API tasks are especially informative. Docs and skills both reached 80% completion, but the docs path was 31% faster with 33% fewer turns, while the skills path used 29% fewer tokens. That is not a clean win for either side. It shows that the right mechanism depends on what is being optimized and how reliably the agent can apply the context.

## Trade-offs and Failure Modes

Passive docs are not a complete solution. They improve orientation, but they do not guarantee policy compliance. Natural-language instructions can still be ignored, displaced by local context, or lost in long trajectories. ContextCov's results support this limit: executable guardrails substantially outperformed prompt-only instruction files for constraint compliance.

Skills fail differently. Their main risks are routing failure, staleness, and bloat.

If the agent never invokes the skill, the skill has no value. If the skill reflects a previous system state, it becomes harmful. If it is overloaded with reference material, examples, and generic advice, it wastes tokens and distracts the agent. SkillReducer's analysis of publicly available skills suggests that these are common problems rather than edge cases.

There is also a maintenance hazard. A team that hand-maintains both canonical docs and a parallel layer of skills documentation creates two drifting systems. That is expensive to review and difficult to trust. In practice, that duplication usually degrades before anyone notices.

Skills are also not a substitute for measurement. SkillsBench shows that curated skills can improve success rates, but that result depends on quality gates and controlled evaluation. Without that discipline, "skill" becomes a packaging format rather than a performance improvement.

## Practical Takeaways

1. Keep canonical docs as the source of truth and derive all agent-facing artifacts from them.
2. Use `AGENTS.md`, `llms.txt`, or similarly compressed passive context as the always-on orientation layer.
3. Treat skills as narrow, versioned accelerators for repeatable workflows, not as a general knowledge layer.
4. Benchmark at least `docs-only`, `optimized-docs`, `passive index`, `skill`, and `skill + explicit trigger` against the same task set.
5. Track success rate, token use, turn count, elapsed time, and whether the intended docs, tools, or skills were actually used.
6. Move hard constraints into executable guardrails rather than relying on prose instructions alone.

## Scope and Positioning

This is not academic research. It does not propose a general theory of agent cognition or a universal law about documentation systems.

It is also not a blog-style opinion piece. The claims here are operational and bounded: passive context often wins when retrieval or skill activation is unreliable, and skills help when they are aligned and evaluated.

It is not vendor documentation either. Vendor material usually explains how to use a feature correctly. This note is about how these mechanisms behave under practical failure conditions when integrated into real engineering workflows.

This note reflects exploratory but evidence-backed lab work. The claims are grounded in reported evals, benchmarks, and implementation guidance, but they are not presented as authoritative or final.

The scope is intentionally narrow: coding-agent context delivery, skill reliability, and documentation strategy for production-adjacent workflows. It does not attempt to settle broader questions about agent architecture, model capability, or governance beyond the specific operational limits discussed here.

## Sources

- [Vercel: AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [Wix Engineering: We Ran 250 AI Agent Evals to Find Out if Skills Beat Docs](https://www.wix.engineering/post/we-ran-250-ai-agent-evals-to-find-out-if-skills-beat-docs-the-answer-is-more-complicated-than-we-ex)
- [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://arxiv.org/abs/2601.20404)
- [SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks](https://arxiv.org/html/2602.12670v1)
- [SkillReducer: Optimizing LLM Agent Skills for Token Efficiency](https://arxiv.org/html/2603.29919v1)
- [OpenAI Developers: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)
- [LangChain: Evaluating Skills](https://www.langchain.com/blog/evaluating-skills)
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [ContextCov: Deriving and Enforcing Executable Constraints from Agent Instruction Files](https://arxiv.org/abs/2603.00822)
