# Changelog

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" and this project adheres to Semantic Versioning.

- https://keepachangelog.com/en/1.0.0/
- https://semver.org/

## [Unreleased]

### Added

- 2026-01-04: Published technical note: [failure-oriented-orchestration](notes/failure-oriented-orchestration/index.md). Outlined a governance-first approach to agent orchestration prioritizing predictability, containment, and recoverability.
  - *Warnings*: The primitives 'Invariant Maps' and 'Phase Ledgers' require significant underlying infrastructure to be effective (Step 3). Discrepancy in index.md navigation (Step 6).
- Published technical note: [earned-agent-autonomy](notes/earned-agent-autonomy/index.md). Introduced the Earned Agent Autonomy (EAA) governance framework and the five-level Autonomy Ladder.
- Published technical note: [agent-execution-contracts](notes/agent-execution-contracts/index.md). Defined execution contracts as machine-readable boundaries unifying specification, testing, and labor for autonomous agents.
  - *Content Update*: Expanded "Trade-offs & Failure Modes" to include the "Buggy Law" paradox, Test-Suite Corruption, and Contract-Induced Deadlock.
  - *Warnings*: Missing canonical tag in HTML and root index.md out of sync (Step 6) - *Resolved*.

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

