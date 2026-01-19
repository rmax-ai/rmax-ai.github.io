---
title: "Designing Agent Workflows as Environments, Not Prompts"
slug: "from-prompting-to-cultivation"
description: "Prompting treats agents as step-by-step trainees; cultivation treats them as actors embedded in environments where tools, constraints, and feedback loops drive reliability."
author: "Max"
site: "rmax.ai"
section: "notes"
type: "technical-note"
status: "published"
date: 2026-01-19
updated: 2026-01-19
tags: ["ai", "agents", "software-engineering", "systems-thinking", "orchestration"]
reading_time: "5–7 min"
canonical_url: "https://rmax.ai/notes/from-prompting-to-cultivation/"
license: "CC BY 4.0"
---

# Designing Agent Workflows as Environments, Not Prompts

## Abstract
Prompting treats an agent like a trainee you must instruct step-by-step; cultivation treats an agent like an actor embedded in an environment whose tools, constraints, and feedback loops determine performance. The thesis of this note is that most operational gains come from designing and iterating the “habitat” around agents (contracts, harnesses, interfaces, review gates), not from increasingly elaborate prompts.

Practically, this implies a two-phase workflow: let the agent explore with minimal scaffolding to reveal real failure modes, then introduce targeted constraints and enforce them hard.

## Context & motivation
Agent tooling has crossed a threshold: agents can now read and change code, run commands, navigate repos, and iterate quickly. That capability makes classic “prompt-as-spec” approaches brittle at scale:

- Teams try to encode their entire mental model up front (architecture, style, test strategy, folder layout).
- The agent optimizes for compliance with the prompt rather than solving the problem.
- Failures become ambiguous: did the agent fail, or did the prompt impose a mismatched framework?

As agents get faster, the limiting factor shifts from “can the agent write code” to “does the surrounding system reliably channel that capability into correct, auditable outcomes.”

## Core thesis
You get more durable reliability by treating agent performance as an emergent property of environment design—goals, tools, constraints, and feedback—than by treating it as a function of prompt quality alone.

## Mechanism / model
A useful working model is to separate an agent workflow into two distinct phases, each with different objectives and artifacts.

### 1) Agency phase (explore the solution space)
Goal: expose what the task actually demands.

- Provide: intent, acceptance criteria, hard constraints (security boundaries, non-negotiables), and success checks.
- Withhold: detailed implementation recipes, prematurely rigid architecture, extensive style micromanagement.
- Observe: where the agent hesitates, invents interfaces, misses edge cases, or produces unverifiable claims.

The output of this phase is not just “a solution attempt.” It is diagnostic data about missing structure in the environment.

### 2) Scaffolding phase (tighten the habitat)
Goal: compress the search space safely.

- Add: test harnesses, linters, typed interfaces, code ownership boundaries, schemas, runbooks, checklists, review gates.
- Encode: the organization’s invariants as executable or enforceable constraints (CI checks, formatters, pre-commit hooks).
- Iterate: constraints respond to observed failure modes, not to anticipated ones.

The key move is ordering: constraints are introduced late (after learning), but enforced hard (once introduced).

### Why this works
Cultivation exploits a simple feedback loop:

1. Declare outcomes (what “done” means).
2. Let the agent act with minimal bias.
3. Capture failures as signals about missing interfaces or missing checks.
4. Update the environment so the next attempt cannot fail in the same way.

Over time, prompts become thinner and more stable because the environment carries the operational knowledge.

### A concrete reference point: “Gas Town”
Steve Yegge’s “Gas Town” framing (as described in his essay) is helpful because it makes the unit of leverage explicit: not a single “hero” agent, but a system of agents coordinated through orchestration, messaging, and shared tooling. In that model, humans improve outcomes primarily by improving the environment—interfaces, contracts, and constraints—based on observed agent behavior, rather than by front-loading detailed instructions.

## Concrete examples

### Example 1: Agentic coding with acceptance criteria, then hard gates
**Scenario:** Implement feature X in an existing repo.

**Agency phase input**
- “Add feature X with these acceptance criteria.”
- “Do not change public API surface.”
- “Must have tests for edge cases A/B.”
- “Run the test suite; failures block completion.”

**What you learn from the first attempt**
- The agent may propose an unexpected decomposition (sometimes better than your default).
- Common misses show up quickly: no tests, shallow tests, unclear boundaries, duplicated logic, or changes that “work” but break invariants.

**Scaffolding phase changes**
- Add or tighten: a test harness pattern, repo conventions, lint rules, and a small checklist the agent must satisfy (e.g., “new code paths have tests,” “no new public exports,” “update docs for new flags”).
- Convert guidelines into enforceable gates.

**Outcome you should expect**
- Second-iteration output becomes more predictable without requiring you to dictate architecture up front.
- The environment carries the guardrails; the prompt stays focused on outcomes.

### Example 2: Knowledge organization that starts with clustering, then introduces taxonomy rules
**Scenario:** Organize a pile of notes into a usable structure.

**Agency phase**
- Ask the agent to cluster and summarize by theme.
- Require the agent to explain why each cluster exists and what belongs / does not belong.

**What you learn**
- Some clusters are naturally coherent; others are “junk drawers.”
- Naming collisions and boundary disagreements become visible.

**Scaffolding phase**
- Introduce naming conventions, exclusion rules, and an index format.
- Define a schema for what “a note” must contain (required fields, allowed tags, canonical headings).
- Add validation (even lightweight) so structure stays consistent over time.

**Outcome**
- The taxonomy is informed by real material rather than by a speculative ontology.
- Future ingestion becomes cheaper because constraints are standardized.

## Trade-offs & failure modes
Cultivation is not a free win. Common failure modes:

- **Unsafe exploration:** Minimal scaffolding can allow actions you would never permit in production (e.g., broad filesystem access, credential exposure). The agency phase still requires hard safety boundaries.
- **Delayed standardization:** If you postpone constraints too long, you accumulate inconsistent patterns that become harder to unify later.
- **Misreading the signal:** Early agent errors can tempt you to over-constrain the system, collapsing useful exploration.
- **Environment drift:** Tooling and policies accrete; if you don’t prune, the “habitat” becomes bureaucratic and slow.
- **Evaluation gap:** Without clear acceptance criteria and automated checks, you’ll confuse “plausible output” with “verified outcome.”

### What this approach does not attempt to solve
- High-assurance correctness without tests/specs.
- Policy compliance without explicit enforcement mechanisms.
- Organizational alignment problems that are fundamentally about incentives and ownership rather than tooling.

## Practical takeaways
- Separate workflows into an explicit agency phase (learn) and scaffolding phase (lock in).
- Treat each agent failure as a design input: add a check, an interface, or a constraint so the failure cannot repeat silently.
- Prefer enforceable constraints (tests, schemas, CI gates) over “please remember” prompt text.
- Keep prompts outcome-focused and stable; put evolving operational knowledge in versioned environment artifacts (contracts, checklists, harnesses).
- Periodically prune the environment: remove constraints that no longer pay for their maintenance cost.

## Positioning note
This note is deliberately tool-agnostic and is about workflow mechanics—how to structure constraints and feedback—rather than features of any specific agent product.

It is not academic research: it does not propose new theory or formal proofs; it offers a pragmatic control loop for improving agent reliability in real systems.

It is not a blog opinion: the claims are operational and testable (e.g., does adding a gate reduce recurrence of a failure mode; does a thinner prompt remain effective across tasks).

It is not vendor documentation: it is tool-agnostic by design and focuses on workflow mechanics.

## Status & scope disclaimer
This note reflects exploratory, practice-driven work in a personal lab setting. It is not authoritative guidance, and it is not validated across all org sizes, safety regimes, or regulatory environments. Treat it as a durable workflow pattern to test locally: adopt the feedback loop, measure outcomes, and keep only what demonstrably improves reliability.
