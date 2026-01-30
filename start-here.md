# Start here — Agent-first engineering (TL;DR)

Welcome — if you’re new to rMax.ai and the idea of agent-first engineering, start here. This short guide explains the core idea, why it matters, and three concrete steps you can take to adopt it in your team.

## What is agent-first engineering?
Agent-first engineering treats AI agents as first-class members of the development process. Instead of manual typing and handoffs, agents execute well-defined tasks within governed environments. Humans provide intent, constraints, and verification; agents perform repeatable work.

## Why it matters
- Speed: agents can generate and iterate faster than humans on routine tasks.
- Scale: individual engineers can leverage agents to produce more output with consistent quality.
- Focus: humans can shift from typing to judgment—designing boundaries, tests, and failure modes.

## Three practical steps to get started
1) Define small, well-scoped agent tasks: pick a repetitive developer workflow (e.g., testing, scaffolding, dependency updates) and write a short "execution contract" that specifies inputs, outputs, and safety checks.

2) Instrument and verify: add telemetry and acceptance tests so agent outputs are treated as first-class artifacts that must pass automated checks before merging or deploying.

3) Limit authority, iterate autonomy: start agents with read-only or simulated permissions and gradually increase privileges as they demonstrate reliability. Use human-on-the-loop checks initially.

## Quick reading
- Read: [Agent-first software engineering](/notes/agent-first-software-engineering/) — an overview of the workflow.
- Try: turn one unit test or CI task into an agent task this week.

---

If you want, I can create a short excerpt from this file on the home page and add a link. Want me to add a short "Start here" excerpt to index.md?