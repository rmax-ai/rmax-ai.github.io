# Changelog

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" and this project adheres to Semantic Versioning.

- https://keepachangelog.com/en/1.0.0/
- https://semver.org/

## [Unreleased]

### Added

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

- 2026-01-19: Published technical note: [from-prompting-to-cultivation](notes/from-prompting-to-cultivation/index.md). Explores the shift from encoding instructions into prompts to designing environments where agents discover solutions through agency, observation, and iterative scaffolding.
  - *Warnings*: High: Heavy reliance on single external reference (Gas Town); paradigm shift claims may read as overstated; hypothetical examples vs documented case studies; term "cultivation" could be misinterpreted. Medium: Note not discoverable from main navigation (pending Phase 8 resolution); external reference link could not be verified.

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

