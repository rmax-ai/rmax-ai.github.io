---
title: "From Prompting to Cultivation: Designing Environments Where Agents Thrive"
slug: from-prompting-to-cultivation
description: A shift from encoding instructions into prompts to designing environments where agents discover solutions through agency, observation, and iterative scaffolding.
author: Max
site: rmax.ai
section: notes
type: essay
status: published
date: 2025-01-30
updated: 2025-01-30
tags:
  - agent-engineering
  - cultivation
  - system-design
  - agentic-workflows
  - gas-town
reading_time: 3–5 min
canonical_url: https://rmax.ai/notes/from-prompting-to-cultivation/
license: CC BY 4.0
---

# From Prompting to Cultivation: Designing Environments Where Agents Thrive

## Executive summary

The dominant mental model for working with AI agents has been *projection*: encoding our own mental frameworks into prompts and expecting agents to execute like apprentices. A more powerful paradigm is emerging—*cultivation*. In this model, we declare goals first, grant agents real agency, observe their behavior, and then iteratively design the environment—tools, processes, constraints—that allows them to thrive. This shift reframes engineering from instruction to habitat design. Systems like **Gas Town**, described by Steve Yegge, demonstrate this transition: leverage comes not from better prompts, but from better environments.

---

## The old model: projection

Most early agent workflows follow an implicit assumption:

> "I know how this should be done, so I'll encode my framework into the agent."

Architectures, conventions, folder structures, test strategies, and even stylistic preferences are imposed *before* the agent attempts the task. The agent becomes a mirror of the human's habits and biases.

This model has clear limits:
- Premature constraints collapse the search space.
- The agent optimizes for compliance rather than discovery.
- Failures are hard to interpret: did the agent fail, or did the framework misfit the task?

At scale, projection leads to diminishing returns. You debug your own thinking twice—once in your head, once in the prompt.

---

## The inflection point

The shift begins when you reverse the order:

1. You state **what** you want, not **how** to do it.
2. You let the agent attempt the task with minimal scaffolding.
3. You observe where it struggles, hallucinates, or asks for clarification.
4. You introduce tools and constraints *in response* to those signals.

This moment is subtle but irreversible. Your role changes. You are no longer transferring knowledge; you are *learning from the agent's interaction with the problem*.

---

## The new model: cultivation

Cultivation treats agents as autonomous actors embedded in an environment. Performance emerges from the interaction between:
- Goals and incentives
- Available tools and APIs
- Feedback loops
- Constraints introduced over time

Instead of asking "How do I prompt better?", the core question becomes:

> "What environment would make this agent succeed?"

This mirrors how effective human organizations scale. They do not micromanage every action. They define missions, establish feedback, and evolve structures that reward good behavior and dampen failure modes.

---

## Gas Town as a concrete reference point

Steve Yegge's **Gas Town** makes this model tangible.

Gas Town is not a single super-agent. It is a *colony* of coding agents coordinated through messaging, orchestration layers, and shared tooling. Agents are given work, allowed to attempt solutions, communicate results, and surface needs. Humans respond by improving the environment—adding better interfaces, clearer contracts, richer APIs.

Crucially:
- Agents are not over-instructed upfront.
- Constraints evolve as the system observes real failure modes.
- Leverage comes from orchestration and environment design, not individual prompt cleverness.

Gas Town demonstrates that the future of engineering is not "AI writes all the code," but "humans design ecosystems where code-writing agents operate productively."

---

## Practice: how cultivation looks day to day

### Example 1: Agentic coding

- **Goal first**: "Implement feature X with these acceptance criteria."
- **Agent attempt**: The agent proposes an architecture you did not expect.
- **Observation**: Missing tests, unclear interfaces, duplicated logic.
- **Scaffolding**: You introduce a test harness, lint rules, and a repo structure.
- **Result**: The second iteration is dramatically more reliable—without having imposed your architecture prematurely.

### Example 2: Knowledge organization

- **Goal first**: "Cluster and summarize this body of notes."
- **Agent attempt**: The agent forms organic thematic groupings.
- **Observation**: Some clusters are useful, others noisy.
- **Scaffolding**: You introduce naming conventions, exclusion rules, and indices.
- **Result**: A taxonomy informed by the data, not imposed ahead of time.

---

## Why this is a real mental-model shift

This is not just a workflow tweak. It changes:
- **What expertise means**: from writing code to shaping systems.
- **What artifacts matter**: from prompts to reusable habitats (AGENTS.md, schemas, checklists).
- **Where learning happens**: not only in humans, but in the human–agent feedback loop.

You stop asking agents to think like you.
You start letting them show you what the problem *demands*.

---

## Implications

- Engineers become orchestrators and environment designers.
- Constraints are introduced *late*, but enforced *hard*.
- Productivity compounds through reusable environments, not one-off prompts.
- Multi-agent systems outperform single "hero" agents.

---

## Actionable next steps

1. Explicitly separate **agency phase** and **scaffolding phase** in your workflows.
2. Instrument agent feedback: ask what blocked progress and what would have helped.
3. Treat environments as versioned products—iterate on them deliberately.

---

## Want to go further?

- Compare cultivation with mission-command doctrines in organizational theory.
- Explore when early constraint is still necessary (safety-critical systems).
- Experiment with agents that can propose changes to their own environments under governance.

---

**Reference**: Steve Yegge, ["The Future of Coding Agents"](https://steve-yegge.medium.com/the-future-of-coding-agents-e9451a84207c)
