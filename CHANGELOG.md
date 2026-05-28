# Changelog

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" and this project adheres to Semantic Versioning.

- https://keepachangelog.com/en/1.0.0/
- https://semver.org/

## [Unreleased]

### Added

- 2026-05-27: Published technical note: [enterprise-ai-agents-knowledge-layer-beyond-rag](notes/enterprise-ai-agents-knowledge-layer-beyond-rag/). Argues that enterprise agents need a permission-aware knowledge layer beyond vector search and vanilla RAG so they can resolve entities, relationships, policies, approvals, provenance, and outcomes before acting.
  - *Warnings*: Publish with caution — the note can be over-read as a broad prescription for all enterprise AI deployments rather than for governed, cross-system workflows; the architecture assumes substantial organizational maturity around identity, permissions, policy modeling, and data freshness; the graph and ontology framing could be misread as endorsing a specific vendor or storage pattern when the stronger claim is about a knowledge control plane.

### Changed

- 2026-05-27: Retitled and reframed [enterprise-ai-agents-knowledge-layer-beyond-rag](notes/enterprise-ai-agents-knowledge-layer-beyond-rag/) as a Glean-centered analysis. Updated the intro and conclusion to make the primary source framing explicit and to position the note as an interpretation of Glean’s knowledge graph approach to enterprise AI search rather than a standalone manifesto.

- 2026-05-24: Published technical note: [stateful-enterprise-cognition](notes/stateful-enterprise-cognition/). Argues that enterprise agents need a governed knowledge layer to externalize canonical identity, provenance, relationships, constraints, and temporal state before autonomy can be trusted.
  - *Warnings*: Publish with caution — the note’s framing can be over-read as a broad enterprise mandate rather than guidance for workflows with high coordination and governance costs; the knowledge-layer prescription assumes meaningful organizational maturity around ownership, source authority, and policy hygiene; the knowledge-graph discussion could be misread as product selection guidance when the stronger claim is about semantic coordination, not a single storage technology.

- 2026-05-20: Published technical note: [enterprise-ai-needs-harness-engineering](notes/enterprise-ai-needs-harness-engineering/). Argues that enterprise AI advantage will come less from better chatbots and more from harness engineering: governed execution, shared state, verification, approvals, and auditable traces.
  - *Warnings*: Publish with caution — the thesis is strong enough to be read as a general enterprise mandate rather than a scoped interpretation for complex, governed workflows; the examples can be mistaken for portable operating templates even where teams lack the process maturity, state infrastructure, and review capacity they assume; the note leans more on systems interpretation and one recent paper than on comparative evidence, so readers may overstate the certainty of its conclusions.

- 2026-05-12: Published technical note: [docs-vs-skills-agent-context-delivery](notes/docs-vs-skills-agent-context-delivery/). Examines when passive agent-optimized documentation outperforms skills in coding-agent workflows and argues for deriving narrow, evaluated skills from canonical docs.
  - *Warnings*: Publish with caution — readers may over-generalize vendor eval results beyond coding-agent workflows; the note assumes some eval and instrumentation maturity; some readers may treat the architecture ordering as prescriptive beyond the bounded evidence presented.

- 2026-03-22: Published technical note: [mlops-agent-harness-engineering](notes/mlops-agent-harness-engineering/). Argues that reliable agent systems depend less on the model alone and more on the surrounding harness for context assembly, tool interfaces, verification, observability, and execution control.
  - *Warnings*: Publish with caution — the note argues from current agent-operating patterns and selected vendor research, so some readers may over-read it as a stable systems principle rather than a time-bounded framing; several recommendations assume a team already has enough operational maturity to build and maintain harness controls without creating more complexity than they remove; the MLOps analogy is useful but can mislead readers into treating agent behavior as operationally equivalent to conventional ML systems even though the control dynamics are materially different; external citation URLs include tracking/query parameters such as utm_source=chatgpt.com and ref=ds3lab.ghost.io and are worth normalizing in a later cleanup.

- 2026-03-17: Published technical note: [from-task-automation-to-goal-driven-systems](notes/from-task-automation-to-goal-driven-systems/). Examines the shift from task-level automation toward goal-driven systems coordinated by harnesses, policies, and human oversight.
  - *Warnings*: Publish with caution — the note makes a strong architectural claim that may be read as generally applicable guidance rather than as a model that depends on organizational maturity and domain constraints; several operational prerequisites remain implied, especially observability quality, rollback capability, policy design, and human oversight; readers may over-apply the harness framing to domains where the cost of building and maintaining the harness exceeds the value of agent autonomy.

- 2026-03-15: Published technical note: [building-an-autonomous-development-loop](notes/building-an-autonomous-development-loop/). Describes software development as a controlled GitHub production loop using issues, draft pull requests, labels, CI checks, and isolated worktrees.
  - *Warnings*: Publish with caution — GitHub-centered, experiment-scoped workflow may still be over-read as a broadly portable operating model; key prerequisites remain implicit (strong issue hygiene, accurate dependency modeling, trustworthy CI, and human conflict-resolution capacity); do not treat the note as support for expanding automation authority around review suggestion application or merge decisions.

- 2026-03-03: Published technical note: [ai-native-sdlc-proposal](notes/ai-native-sdlc-proposal/). A blueprint for an AI-native SDLC built on intent-first specs, multi-agent competitive generation, deterministic guardrails, adversarial verification, and continuous validation.
  - *Warnings*: Publish with caution — W1: readers without spec discipline may apply the framework to under-specified intent packages, degrading all downstream verification; W2: teams may simulate breaker isolation with shared-context agents, reducing adversarial value without realising it; W3: note is orphaned from notes/index.html (no inbound navigation link).

- 2026-03-01: Published technical note: [agent-oriented-clis-teach-themselves](notes/agent-oriented-clis-teach-themselves/). A guide to agent-oriented CLIs: versioned command contracts, safe validate/plan/apply, deterministic JSON outputs, stable error codes, and replayable provenance.
  - *Warnings*: Publish with caution — examples are illustrative (not tied to a specific vendor CLI); contract drift between schemas and backend behavior can cause confident failures; Mermaid diagram renders as a code block in HTML unless a renderer is added.

- 2026-02-18: Published technical note: [harness-new-model-agent-systems-2026](notes/harness-new-model-agent-systems-2026/). Argues that agent reliability is primarily improved by harness engineering (constraints, tooling, feedback, and evaluation), not bigger models alone.
  - *Warnings*: Publish with caution — benchmark references can drift; avoid reading “determinism” as a literal guarantee; some framing is necessarily directional and may over-generalize across domains.

- 2026-02-08: Published technical note: [tests-not-silver-bullet-resilience-first-observability](notes/tests-not-silver-bullet-resilience-first-observability/). In AI-assisted, high-velocity codebases, tests stay necessary but cannot be the primary safety system; survivability comes from observability, constraints, and recovery.
  - *Warnings*: Publish with caution — operational complexity and "more instrumentation" can compete with feature velocity; risk of over-engineering guardrails for non-critical paths.

- 2026-02-01: Published technical note: [agency-vs-privilege-high-agency-agents-infrastructure](notes/agency-vs-privilege-high-agency-agents-infrastructure/). An operator-focused case for separating an agent’s autonomy from its permissions and secrets to limit blast radius under prompt injection and model variability.
  - *Warnings*: Publish with caution — scope boundaries around "low privilege" prerequisites; risk of over-generalization. Low: minor nav consistency difference (#about vs /#about). Low: external link durability (https://www.moltbook.com/heartbeat.md).

- 2026-01-28: Published technical note: [trust-patience-craft-working-modern-agentic-ai](notes/trust-patience-craft-working-modern-agentic-ai/). An operator-focused guide to earning trust in agentic AI through constraints, instrumentation, and iterative verification loops.
  - *Warnings*: Low: Some claims are generalized; Low: occasional anthropomorphic phrasing.

- 2026-01-25: Published technical note: [human-loop-orientation](notes/human-loop-orientation/). An analysis of the shift from 'human-in-the-loop' execution to 'human-on-the-loop' orientation in autonomous software systems.

- 2026-01-20: Published technical note: [personal-software-factory](notes/personal-software-factory/index.md). Defines a personal software factory as an individual-scale system for turning intent into deployed software through repeatable, automated pipelines.
  - *Warnings*: High: “Hardened path to production” may imply rollback/secrets discipline without guardrails; High: Delegating security-critical edits to agents risk; Medium: Solo overreach in payments/auth/security/privacy contexts; Medium: False confidence from green checks; acceptance depth unclear; Medium: Toolchain/agent drift not tied to mitigations; Low: Premature process complexity; Low: CSV→JSON example misapplied to PII flows; Resolved: Link audit — duplicated frontmatter removed from notes/personal-software-factory/index.md.

- 2026-01-17: Published technical note: [personal-operating-systems-micro-apps](notes/personal-operating-systems-micro-apps/index.md). Explores how multi-agent coding assistants enable individuals to build personal operating systems that encode decision rules and execution mechanisms into custom micro-apps, shifting knowledge work from passive memory toward active execution.
  - *Warnings*: High: Over-generalization risk — Readers may apply this to team or organizational contexts despite explicit individual scope; High: Premature optimization risk — Under-specifies when workflow patterns are 'stable enough' beyond '5-10 repetitions' heuristic; High: Operational misuse — Manual override paths mentioned but not detailed; risk of over-automation without safeguards; Medium: Hidden assumptions — Assumes technical fluency, system design tolerance, and AI assistant access without defining thresholds; Medium: Authority misreading — Phrases like 'architectural principle' and structured guidance may be read as prescriptive best practice; Medium: Longevity risk — 'Multi-agent coding assistants' phrase may age poorly; specific assistant capabilities assumed but not bounded.

- 2026-01-17: Published technical note: [open-source-after-coding-agents](notes/open-source-after-coding-agents/index.md). Argues that as code generation approaches zero cost, open source value shifts from contribution volume to governance and curation capacity.

- 2026-01-13: Published technical note: [code-is-the-new-assembly](notes/code-is-the-new-assembly/index.md). Explores how AI agents shift source code from a human artifact to a compilation target, requiring a move from syntax-based review to intent-based validation.
  - *Warnings*: Verification Tooling Gap: Adopting the 'code as assembly' mindset without rigorous property-based testing and semantic validation in place poses a high risk of subtle logic bugs; Safety-Critical Non-compliance: The principle that reading every line of generated code is 'impractical' may violate safety standards in regulated or mission-critical environments; Hidden Assumptions on Agent Consistency: The note assumes the 'compiler' (the LLM) behaves with the same determinism and reliability as a traditional binary compiler.
- 2026-01-09: Published technical note: [the-software-replacement-age](notes/the-software-replacement-age/index.md). Explored the shift toward software replaceability over longevity in the era of zero-cost code generation.
  - *Warnings*: Conditional publish due to potential "Semantic Gaps" in schemas and "Operational Drift via Regeneration." Best applied to Data/Web glue-code rather than System Core (Step 3).
- 2026-01-09: Updated technical note: [github-copilot-model-selection-guidelines](notes/github-copilot-model-selection-guidelines/index.md). Added the GitHub Copilot Model Selection Table image to both Markdown and HTML versions for improved visual tiering guidance.
- 2026-01-08: Published technical note: [github-copilot-model-selection-guidelines](notes/github-copilot-model-selection-guidelines/index.md). Introduced a tiered selection framework for GitHub Copilot based on the Principle of Least Power and reasoning horizons.
  - *Warnings*: Risk of "Heuristic Fatigue" due to meta-decision overhead; "Silent Regression" in Tier 3 models (Step 3).
- 2026-01-05: Published technical note: [ai-native-engineering](notes/ai-native-engineering/index.md). Explored the transition from AI-augmented to AI-native engineering, focusing on context orchestration and the systemic verification crisis.
  - *Warnings*: Shifting to orchestration without matching validation rigor risks architectural debt; potential "talent pipeline collapse" due to automated inner loops (Step 3). Orphaned research summaries reported (Step 6).
- 2026-01-05: Implemented a scroll-based reveal for the header logo on the home page to avoid visual redundancy with the hero logo.
- 2026-01-05: Added a larger hero logo to the main index page and updated the hero section layout for better visual impact.
- 2026-01-05: Added official logo (dark version) across the site, replacing the placeholder text logo.
- 2026-01-04: Published technical note: [authority-first-agent-architecture](notes/authority-first-agent-architecture/index.md). Introduced an authority-first architecture model for AI agents, decoupling permission logic from reasoning loops.
  - *Warnings*: Architecture does not mitigate intent-based failures or sequence-based attacks (Step 3). Missing reference in root index.md (Step 6).
- 2026-01-04: Published technical note: [failure-oriented-orchestration](notes/failure-oriented-orchestration/index.md). Outlined a governance-first approach to agent orchestration prioritizing predictability, containment, and recoverability.
  - *Warnings*: The primitives 'Invariant Maps' and 'Phase Ledgers' require significant underlying infrastructure to be effective (Step 3). Discrepancy in index.md navigation (Step 6).
- Published technical note: [earned-agent-autonomy](notes/earned-agent-autonomy/index.md). Introduced the Earned Agent Autonomy (EAA) governance framework and the five-level Autonomy Ladder.
- Published technical note: [agent-execution-contracts](notes/agent-execution-contracts/index.md). Defined execution contracts as machine-readable boundaries unifying specification, testing, and labor for autonomous agents.
  - *Content Update*: Expanded "Trade-offs & Failure Modes" to include the "Buggy Law" paradox, Test-Suite Corruption, and Contract-Induced Deadlock.
  - *Warnings*: Missing canonical tag in HTML and root index.md out of sync (Step 6) - *Resolved*.
- 2026-01-15: Published technical note: [evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc](notes/evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc/index.md). Traces the evolution of AI coding agents from autocomplete-era copilots to autonomous SDLC systems, with milestones, capability shifts, and operational implications.
  - *Warnings*: High: Orphaned content in notes/index.html — link /notes/evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc/ has no inbound listing; Medium: Nav discoverability in index.html — link /notes/evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc/ should have a prominent inbound path; Medium: Sitemap missing entry in sitemap.xml — https://rmax.ai/notes/evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc/ not present; regenerate sitemap to include URL and update lastmod.
- 2026-01-16: Published technical note: [evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc](notes/evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc/index.md). Traces the evolution of AI coding agents from autocomplete-era copilots to autonomous SDLC systems, with milestones and capability shifts from 2013–2026.
  - *Warnings*: High: notes/index.html — /notes/evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc/ not listed (nav_discoverability_orphaned_note_not_listed_in_notes_index); Medium: index.html — /notes/evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc/ not featured in home notes section (nav_discoverability_not_featured_on_home_notes_section); Medium: index.md — /notes/evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc/ not featured in home notes section (nav_discoverability_not_featured_on_home_notes_section); Low: notes/evolution-of-ai-coding-agents-autocomplete-to-autonomous-sdlc/index.md — anchor #milestones-20132026 may not resolve in standard Markdown renderers (within_page_anchor_may_not_resolve_in_standard_markdown_renderers).

- 2026-01-19: Published technical note: [from-prompting-to-cultivation](notes/from-prompting-to-cultivation/index.md). Argues that reliability gains come from designing the agent’s environment (tools, constraints, feedback loops), not from increasingly elaborate prompts.
  - *Warnings*: High: Heavy reliance on a single external reference (“Gas Town”); paradigm-shift framing may read as overstated; examples are illustrative rather than documented case studies; the term “cultivation” could be misinterpreted. Medium: External reference availability was not network-verified.

- 2026-02-15: Published technical note: [rx-lean-agent-kernels-beat-general-coding-frameworks](notes/rx-lean-agent-kernels-beat-general-coding-frameworks/). Introduces `rx`, a microkernel-style agent architecture with an explicit control loop, narrow tool contracts, append-only event state, and replaceable transport for predictable cost and behavior.
  - *Warnings*: Publish with caution — determinism framing risk (could be misread as true determinism), premature optimization risk, authority model misreading risk, operational misuse risk. Release with followups — note not linked from /notes/ yet (orphan risk), canonical URL not present in sitemap.xml yet (SEO discoverability), analytics/CTA scripts may be blocked but content should still render.

---

---

## [0.1.0] - 2026-01-04

### Added

- Initial public release of rmax-ai.github.io
  - Site skeleton with index pages and routing
  - Notes and research content (notes/, research/)
  - Agent prompts and tooling (.agent/prompts)
  - Basic README and project metadata

### Changed

- N/A

### Fixed

- N/A

## 2026-05-28

### Added

- Published technical note: notes/forward-deployed-engineer-enterprise-ai/ — The Forward Deployed Engineer in Enterprise AI: From Integration Specialist to Agentic Control-Plane Builder
