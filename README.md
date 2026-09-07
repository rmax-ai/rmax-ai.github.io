# rMax.AI — Agent-driven research lab

rMax.AI is an agent-first research lab focused on building, evaluating, and publishing reproducible research about AI-native systems and agent architectures. This repository contains the public site, research notes, agent prompts and minimal operational artifacts used to run, audit, and iterate on agent-driven workflows.

## Why rMax.AI

- Agent-first engineering: treat agents as modular specialists that can be composed, tested, and audited.
- Authority-first design: give agents clear, scoped authority and explicit success criteria to reduce risky open-ended behavior.
- Failure-oriented orchestration: build workflows that detect, contain, and recover from partial failures.
- Earned autonomy: grant more responsibility to agents only after human-reviewed performance and safety checks.
- Transparency & reproducibility: store prompts, drafts, and publish artifacts in the repo so research is auditable and repeatable.

## Repository layout (high level)
- .agent/: agent and mode definitions describing responsibilities and orchestration.
- .agent/prompts/: reusable prompt templates for writing, reviewing, and publishing notes.
- inbox/: captured ideas and raw inputs that feed agent workflows.
- processed/: agent-produced drafts and intermediate artifacts.
- notes/: published notes and essays (public output).
- research/: longer-form projects, experiments and notebooks.
- scripts/: helper scripts (e.g., scripts/generate-sitemap.py).
- docs/: supporting documentation and operational playbooks.
- images/: site and asset images.
- index.md / index.html: static site entry points.

## Agent workflow (high-level)
1. Idea captured in inbox/.
2. Orchestration agent decomposes the idea into tasks and assigns subagents.
3. Subagents synthesize drafts, run experiments, or generate artifacts and drop them into processed/.
4. Human reviewers use review prompts (see .agent/prompts/) to audit and iterate.
5. After approval, artifacts are published to notes/ and the site is updated.

## Adding or changing agents
1. Add a mode / metadata file in .agent/mode/<name>.agent.md describing inputs, outputs, responsibilities and failure modes.
2. Add or update prompt templates in .agent/prompts/ (use existing prompts as examples).
3. Prefer small, testable behaviors with explicit success criteria and recovery paths.
4. Test changes by running the agent orchestration in a controlled environment or via manual prompt simulations.

## Local development

The site is built with Astro and deployed as static HTML. Markdown notes in
`notes/<slug>/index.md` are the publication source; Astro renders the note
pages and index during the build.

- `npm install`
- `npm run dev` for a local preview
- `npm run check` for Astro diagnostics
- `npm run build` to create the production artifact in `dist/`

GitHub Pages deploys the `dist/` artifact with the custom-domain `CNAME` and
`.nojekyll` files from `public/`.

## Contributing
- Open issues or PRs on GitHub: https://github.com/rmax-ai/rmax-ai.github.io
- Add new ideas to inbox/ to feed agent workflows.
- Propose changes to modes and prompts with examples and expected outputs.

## Safety & governance
- All agent actions producing public artifacts go through human review before publication.
- Failure-mode reviews and review prompts are first-class artifacts in .agent/prompts/.
- The project prioritizes reproducibility, auditability and clear, testable agent behavior.

## Contact & links
- Website: https://rmax.ai
- Repo: https://github.com/rmax-ai/rmax-ai.github.io
- Issues: https://github.com/rmax-ai/rmax-ai.github.io/issues

## License
- No license specified in this repository. Add a LICENSE file or contact the project owner if you need reuse terms.
