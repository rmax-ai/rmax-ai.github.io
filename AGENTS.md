# Agent Operating Manual

Welcome to the **rmax.ai** research lab. This repository is an agent-native environment designed for autonomous collaboration, auditability, and safety.

## 1. Core Principles
- **Authority-First**: Agents strictly operate within the scopes defined in [docs/contracts/](docs/contracts/) and [.agent/mode/](.agent/mode/). Authority is granted, not assumed.
- **Failure-Oriented**: Plan for failures. If a success criterion (KPI) isn't met, or an invariant is violated, **halt execution immediately**. Do not attempt to "fix" a contract violation with more prose.
- **Artifact-Locked**: All public notes must adhere to the [notes/schema.yaml](notes/schema.yaml).
- **Transparency**: Every major decision or state transition should be detectable via file changes or logs in [.agent/runs/](.agent/runs/).

## 2. Repository Conventions

### Workflow Folders
- [inbox/](inbox/): Incoming notes, raw ideas, and triggers for agent workflows.
- [processed/](processed/): Staging area for drafts, intermediate artifacts, and archived inbox items.
- [notes/](notes/): The public notes output. Each note is a directory: `notes/<slug>/index.md`.
- [docs/contracts/](docs/contracts/): Formal execution contracts that define the "rules of the game" for specific tasks.

### Agent Configuration ([.agent/](.agent/))
- [.agent/mode/](.agent/mode/): Domain-specific identities (e.g., `publishing-orchestrator`). These files define your role, authority (read/write access), and mandatory subagents.
- [.agent/prompts/](.agent/prompts/): Standardized, versioned instructions for specific tasks like writing, auditing, or code refactoring.

## 3. Primary Workflow: Publishing
The standard "hot path" for agents in this repo is transforming an idea into a technical note. Refer to [publishing-orchestrator.agent.md](.agent/mode/publishing-orchestrator.agent.md) for the orchestrator workflow.

## 4. Guardrails & Safety
- **No Self-Modification**: Agents must not modify their own `.agent/mode/*.md` or `.agent/prompts/*.md` files.
- **Human-in-the-loop**: High-impact changes (like publishing to `notes/`) require an explicit "passing" verdict from a review subagent or human approval.
- **Schema Validation**: All frontmatter i `notes/*/index.md` files MUST be validated against [notes/schema.yaml](notes/schema.yaml).

## 5. Escalation
If you encounter a state not covered by a contract, or if two instructions conflict:
1. **Stop.**
2. **Document** the conflict.
3. **Escalate** to the human user for clarification.
