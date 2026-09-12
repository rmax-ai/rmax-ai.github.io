---
title: "When Everyone Can Build: How AI Changes the Role of the Expert"
slug: everyone-build-ai-expert-role
description: "How falling AI implementation costs shift expert leverage toward experimentation, platforms, evaluation, and safe operational boundaries."
author: Max
site: rmax.ai
section: notes
type: essay
status: published
date: 2026-09-12
updated: 2026-09-12
tags:
  - ai
  - expertise
  - software development
  - platform engineering
  - governance
  - agentic systems
reading_time: "19 min"
canonical_url: https://rmax.ai/notes/everyone-build-ai-expert-role/
license: "CC BY 4.0"
---

# When Everyone Can Build: How AI Changes the Role of the Expert

## Abstract

AI is lowering the cost of software implementation and making working software and workflows accessible to more people outside traditional engineering roles. This note argues that expertise is not disappearing; its highest-leverage location is moving from implementation, to the systems that multiply implementation, and finally to the boundaries that make widespread building safe. In startup exploration, the AI expert should increase the rate at which hypotheses become experiments. In consequential production, the expert should increase the amount of verified change an organization can safely absorb. The operational implication is a shift from centralized review of every artifact toward self-service platforms, explicit permissions, systematic evaluations, observability, and bounded autonomy.

## Core thesis

AI commoditizes execution faster than it commoditizes judgment.

The AI expert's role therefore progresses through three stages:

> **Builder → Builder of Builders → Designer of Boundaries**

When implementation is scarce, experts implement. When implementation becomes cheap, experts build systems that help others implement. When implementation becomes ubiquitous, experts protect the invariants that keep ubiquitous building from becoming ubiquitous failure.

This suggests a deeper economic shift:

> **AI creates an abundance of production and a scarcity of assurance.**

The constraint is not the number of artifacts an organization can generate. It is the amount of change it can verify, integrate, operate, and govern without exceeding its tolerance for failure.

## Context & motivation

Coding agents are narrowing the gap between software professionals and domain experts on implementation tasks. Designers, product managers, analysts, legal teams, and marketers are becoming capable of building working software and workflows. The cited company accounts describe a division of labor between broad participation and centralized assurance.

The important distinction is not simply startup versus enterprise. It is exploration versus consequential production. In a startup searching for product-market fit, the dominant constraint is learning speed. In a large or regulated organization, the dominant constraint increasingly becomes assurance: reliability, security, compliance, operational stability, and reputation.

The evidence cited here is not limited to anecdotes. Anthropic analyzed roughly 400,000 Claude Code sessions and found that people still make most of the planning decisions while Claude makes most of the execution decisions. On coding tasks, major occupational groups achieved success rates close to those of software engineers. Expertise still mattered: users with stronger domain knowledge were able to get more work from Claude per instruction and recover more effectively from failures. [Anthropic, *Agentic coding and persistent returns to expertise*](https://www.anthropic.com/research/claude-code-expertise)

Figma reports a related erosion of role boundaries. In its 2026 survey, the share of designers participating in development rose from 21% to 41%, while developers participating in design rose from 44% to 60%. Its conclusion is that when the ability to build becomes broadly available, the scarce capability becomes deciding what deserves to be built and what good looks like. [Figma, *2026 AI Report*](https://www.figma.com/blog/2026-ai-report/)

Microsoft's 2026 Work Trend Index describes a similar shift from a broader knowledge-work perspective. Among surveyed AI users, 50% said quality control of AI output is becoming more important and 46% named critical thinking. Eighty-six percent said they treat AI output as a starting point rather than a final answer. Microsoft characterizes the human role as moving toward intent-setting, judgment, quality standards, and workflow design. [Microsoft, *2026 Work Trend Index*](https://www.microsoft.com/en-us/worklab/work-trend-index/agents-human-agency-and-the-opportunity-for-every-organization)

OpenAI's enterprise data indicates that agentic coding is also spreading beyond engineering, with rapid growth in Codex use across functions such as legal, recruiting, sales, and marketing. [OpenAI, *Enterprise Signals*](https://openai.com/signals/enterprise-data/)

The implication is not that expertise disappears. Implementation becomes less exclusive, while judgment and assurance remain comparatively scarce.

## Mechanism / model

### 1. Move from implementation to experimentation

For an early-stage startup, AI changes the economics of product development. The traditional loop was relatively expensive:

```text
idea
→ specification
→ implementation
→ deployment
→ user feedback
→ iteration
```

AI allows teams to instantiate several versions of an idea in parallel:

```text
hypothesis
    ↓
many implementations
    ↓
instrumented experiments
    ↓
user evidence
    ↓
selection
```

When implementation costs fall, a startup can search a much larger product space before committing. The highest-leverage work is no longer simply writing a feature faster. It is creating an app factory for experimentation:

- reusable project scaffolds;
- agentic coding workflows;
- disposable environments;
- synthetic data;
- analytics and instrumentation by default;
- fast feature flags and deployment;
- automated feedback capture;
- cheap generation of alternative UX and workflow variants.

Figma explicitly argues that AI makes it cheaper to explore several product directions before converging on one, shifting the advantage toward teams that search the option space well. [Figma, *What matters when anyone can build*](https://www.figma.com/blog/what-matters-when-anyone-can-build/)

The acceptable quality bar can therefore be lower for truly disposable experiments. But the critical variable is not company size; it is consequence.

```text
required assurance
≈ blast radius
× irreversibility
× regulatory / reputational exposure
```

A two-person medical startup may need stricter controls than an internal prototype at a 50,000-person company. Disposable systems can accept a lower quality bar only when they are genuinely disposable and isolated. Consequential systems require controls proportionate to their consequences.

### 2. The bottleneck migrates downstream

As AI increases implementation throughput, the bottleneck moves into the systems that validate, integrate, and operate all that output.

Google's DORA research is relevant here. Its 2025 report found AI adoption associated with increased throughput and product performance while delivery stability remained a challenge. DORA's interpretation is that AI acts as an amplifier: organizations with strong testing, fast feedback, version control, architecture, and internal platforms gain more; weak delivery systems have their weaknesses exposed more quickly. [Google Cloud / DORA, *State of AI-assisted software development*](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)

This produces a structural asymmetry:

```text
generation capacity
        grows rapidly
             ↓
review capacity
test capacity
security capacity
operational capacity
governance capacity
        grow much more slowly
```

Even if a company can suddenly produce five times as many changes, it has not automatically created five times as much verification capacity. This is why “AI productivity” can become misleading at scale.

The useful question is not:

> How much more code can we generate?

It is:

> How much more **verified change** can the organization safely absorb?

Google SRE has long treated change as a major source of instability; its error-budget guidance states that changes account for roughly 70% of outages in its model. Error budgets exist precisely to balance innovation velocity against reliability. [Google SRE, *Error Budget Policy*](https://sre.google/workbook/error-budget-policy/)

AI turns that old SRE problem into a larger organizational one.

### 3. Encode the quality boundary into the system

AI-generated software can look correct long before it has been proven safe or robust. Agents are optimized to produce something that appears to satisfy a task. Functional success is not equivalent to secure implementation, maintainability, policy compliance, or operational safety.

Anthropic's engineering guidance reflects this transition. Its work on agent evaluations argues that informal testing and dogfooding can work early, but once agents reach production, teams need systematic evals because failures otherwise appear reactively in user traffic. [Anthropic, *Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

Anthropic's containment work goes further. As agents receive more capability and access, their potential blast radius increases even if model reliability improves. Anthropic therefore treats isolation, tool permissions, network controls, and environment boundaries as core engineering mechanisms. It distinguishes between trying to supervise every action and limiting what the agent is structurally capable of affecting. [Anthropic, *How we contain Claude across products*](https://www.anthropic.com/engineering/how-we-contain-claude)

An enterprise AI function cannot scale by manually reviewing every generated artifact. It has to encode the quality boundary into the system.

The scalable architecture is:

```text
AI experts
    ↓
design the operating environment
    ↓
identity and permissions
approved tools
data boundaries
eval suites
policy checks
security scanning
observability
cost controls
human escalation
rollback / containment
    ↓
many humans and agents build independently within those controls
```

The expert moves from being the person who performs every high-skill action to the person who defines the invariants within which those actions can safely happen.

NIST's Generative AI Risk Management Profile takes this lifecycle view explicitly: trustworthiness should be incorporated across design, development, deployment, use, and evaluation rather than bolted on as a final compliance review. [NIST, *AI RMF: Generative AI Profile*](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

OWASP's Top 10 for Agentic Applications similarly treats autonomy, identity, tools, permissions, and downstream actions as architectural security concerns. [OWASP, *Top 10 for Agentic Applications 2026*](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

The dominant scarcity changes with organizational stage:

| Stage | Dominant scarcity | Highest-leverage AI expertise |
|---|---|---|
| Exploration | learning | build experiments |
| Early PMF | repeatability | build reusable workflows |
| Scaling | coordination | build platforms and paved roads |
| Enterprise | assurance | encode controls and evaluation |
| Critical systems | tolerable failure | bound autonomy and prove invariants |

### 4. Move governance upstream

Traditional governance often works as a gate:

```text
team builds something
        ↓
security / legal / compliance review it
        ↓
approve or reject
```

That model stops scaling when thousands of employees and agents can continuously create workflows. The scalable version moves governance upstream:

```text
security
legal
compliance
platform
domain experts
      ↓
encode policies and constraints
      ↓
self-service execution
      ↓
telemetry + evals + exceptions
```

OpenAI's interviews with European enterprise leaders found this pattern: organizations moved faster when security, legal, compliance, and IT participated early as design partners rather than appearing only at the final approval stage. [OpenAI, *How enterprises are scaling AI*](https://openai.com/business/guides-and-resources/how-enterprises-are-scaling-ai/)

This is the difference between governance as review and governance as architecture. Governance embedded in the operating environment scales better than review alone.

## Concrete examples

The organizational pattern appears in reported accounts of companies taking different approaches to AI adoption and operating risk. These examples illustrate the division of labor between distributed building and centralized platforms, standards, and controls; they are not presented as proof that one model works everywhere.

### How to read the evidence

The company examples and industry reports in this note document reported practices, measurements, and interpretations. They are useful evidence that the organizational pattern is emerging, but they do not by themselves establish a universal causal law or prove that one operating model will work in every organization. The relevant variables remain consequence, authority, workflow design, delivery maturity, and the organization's ability to produce continuous evidence.

### Shopify: AI moves into the operating model

Shopify's shift is one of the most explicit in the cited accounts. CEO Tobi Lütke made “reflexive AI usage” a baseline expectation and told teams that before requesting additional headcount or resources, they should demonstrate why the work could not be accomplished using AI. AI usage was also incorporated into performance expectations. [TechCrunch summary of Lütke's public memo](https://techcrunch.com/2025/04/07/shopify-ceo-tells-teams-to-consider-using-ai-before-growing-headcount/)

The policy matters structurally. In the account described, AI is no longer framed as a specialist capability owned by an AI team; it becomes a default operating assumption for every team. That pushes the organization toward decentralized building.

### Microsoft: decentralize creation, centralize the operating system

Inside Microsoft Digital, employees outside conventional software roles are using an internal “Frontier Forge” harness to build agents and automate work. Instead of requiring every useful workflow to enter an engineering backlog, the company is trying to make agent construction available directly to knowledge workers. [Microsoft Inside Track, *The Frontier Firm: how knowledge workers are forging their own AI tools*](https://www.microsoft.com/insidetrack/blog/the-frontier-firm-how-knowledge-workers-are-forging-their-own-ai-tools-at-microsoft/)

At the same time, Microsoft Digital describes a company-wide operating model for agent governance, implementation, adoption, support, and measurement. Its internal guidance focuses on helping employees participate in agent creation safely rather than concentrating creation in a small specialist team. [Microsoft Inside Track, *Becoming a Frontier Firm*](https://www.microsoft.com/insidetrack/blog/becoming-a-frontier-firm-a-guide-for-deploying-ai-agents-based-on-our-experience-at-microsoft/)

This is the two-layer architecture:

```text
distributed builders
        +
central platform / governance
```

A later Microsoft account of its software-development transformation reports that ad-hoc AI adoption initially increased individual developer productivity without equivalent improvement in team productivity. The response was to redesign the surrounding software-development process rather than simply push harder on tool usage. [Microsoft Inside Track, *Engineering the Frontier Firm*](https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/)

This illustrates the bottleneck moving from execution to system design.

### Spotify: when coding stops being the constraint

Spotify describes a related phenomenon from an engineering-platform perspective. More than 99% of Spotify engineers reportedly use AI coding tools weekly, accompanied by a large increase in pull-request frequency. Spotify's framing is explicit: coding is no longer the constraint. In its account, long-running investment in internal developer platforms and engineering standards allows teams and agents to operate at higher speed without making every engineer reconstruct the delivery environment themselves. [Spotify Engineering, *Coding Is No Longer the Constraint*](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint)

Internal developer platforms were originally built to abstract cloud and operational complexity from human developers. In this model, they become the execution environment for human-plus-agent development.

### BBVA: democratized creation inside a governed bank

BBVA is a useful example because the stakes are much higher than in a startup prototype. The bank expanded generative AI access across roughly 100,000 employees while organizing adoption around security, legal, compliance, and technology from the beginning. It created an organization-wide network of AI champions and advanced “wizards” while letting teams across legal, risk, engineering, finance, marketing, and customer service develop specialized GPTs. [OpenAI / BBVA case study](https://openai.com/index/bbva/)

An earlier account reported more than 20,000 custom GPTs created inside the bank, with thousands seeing regular use. Instead of preventing distributed experimentation, BBVA supplied a trusted environment, governance, and training intended to turn shadow AI into controlled AI. [OpenAI, *How BBVA is scaling AI from pilot to practice*](https://openai.com/index/bbva-2025/)

This is a direct implementation of the thesis:

> **Let the edge innovate; make the center responsible for the envelope in which innovation happens.**

### Endava and Atos: from tool rollout to workflow redesign

Endava describes its AI transition not as a tooling project but as a redesign of software delivery, leadership behavior, and workflows. It is embedding agents into daily work and changing how teams collaborate around them. [OpenAI, *How Endava is redesigning software delivery around AI agents*](https://openai.com/index/endava-frontiers/)

Atos provides an even more explicit large-scale control-plane example. Microsoft reports that Atos is building and governing an ecosystem of roughly 19,000 agents through a unified operating model spanning productivity, security, compliance, and agent governance. [Microsoft, *From AI experimentation to Frontier Transformation*](https://blogs.microsoft.com/blog/2026/07/28/looking-back-on-microsofts-fy26-from-ai-experimentation-to-frontier-transformation/)

Taken together, these accounts point toward an organizational pattern that looks less like a traditional AI Center of Excellence and more like platform engineering for intelligence.

### Platform engineering as the historical precedent

A related transition happened with cloud infrastructure. Cloud infrastructure initially gave development teams much more autonomy. That autonomy eventually created enough complexity that organizations needed internal developer platforms, paved roads, and golden paths.

The goal of platform engineering was not to take deployment away from developers again. It was to make autonomous deployment safe, repeatable, and cheap.

The CNCF describes platform engineering as providing standardized self-service infrastructure and workflows for development, testing, deployment, rollback, and operations. [CNCF, *What is platform engineering?*](https://www.cncf.io/blog/2025/11/19/what-is-platform-engineering/)

Its 2026 platform-maturity guidance captures the organizational transition particularly well. At lower maturity, the platform team manually fulfills requests. At higher maturity, the platform team owns the interface and guardrails while product teams self-service capabilities independently. [CNCF, *Platform engineering maturity: From toolchain to self-service*](https://www.cncf.io/blog/2026/09/01/platform-engineering-maturity-from-toolchain-to-self-service/)

That is almost exactly what is now happening to AI expertise:

```text
AI team builds AI applications
```

toward:

```text
AI platform team builds the environment
in which the organization builds AI applications
```

And eventually:

```text
AI assurance / platform team defines
the invariants within which humans and agents
can safely act autonomously
```

## Trade-offs & failure modes

### Manual review becomes the new bottleneck

A common enterprise response is:

```text
everyone uses AI
      ↓
central AI experts review everything
```

That merely creates a new bottleneck. Requiring humans to inspect every generated artifact does not scale with generation capacity. The practical response is to move repeatable checks into platforms, policies, evals, and automated controls while reserving human attention for consequential decisions and exceptions.

### Plausible output can outrun verification

Generated software can appear functional without being secure, maintainable, compliant, observable, or safe to operate. Informal testing may be sufficient for early exploration, but production systems need systematic evaluations and a way to detect failures before they become user-visible incidents. Functional success should not be treated as evidence of operational readiness.

### Lower implementation cost does not lower consequence

AI makes it cheaper to build, but it does not make an irreversible action reversible or reduce the blast radius of a permissioned system. The quality bar can be lower for disposable experiments only when the systems are genuinely disposable and isolated. Regulatory, reputational, safety, and reliability exposure still require controls proportionate to consequence.

### Governance can become either a gate or a bypass

Late review by security, legal, compliance, or platform teams creates queues and encourages shadow systems. Removing those controls entirely creates operational risk. Upstream policy design, self-service interfaces, telemetry, evals, exception handling, and explicit escalation are the middle path described by the source material.

### Centralization can recreate ticket-driven platform failure

A boundary-setting role can be misread as requiring experts to stand between users and production. That reproduces the old ticket-driven central-platform failure mode. The better objective is:

> **Make the safe path the easiest path.**

The AI expert's leverage increasingly comes from deciding:

- what context an agent may see;
- which tools it may call;
- which actions require approval;
- what evidence constitutes success;
- what gets logged;
- what gets evaluated before deployment;
- which failures automatically stop execution;
- how rollbacks occur;
- which responsibilities remain human;
- how successful workflows become reusable organizational capabilities.

## Practical takeaways

1. **Classify work by consequence, not by company size.** Estimate blast radius, irreversibility, and regulatory or reputational exposure before choosing the quality bar and approval path.
2. **Optimize for verified change.** Track whether the organization can safely test, review, secure, deploy, observe, and roll back the changes it generates—not only how much code or how many workflows it can produce.
3. **Build a self-service app and agent factory.** Provide reusable scaffolds, disposable environments, instrumentation, deployment paths, feature flags, and feedback capture so teams can explore without rebuilding the delivery system each time.
4. **Encode boundaries before scaling autonomy.** Make identity, permissions, approved tools, data boundaries, evaluation suites, policy checks, observability, cost controls, escalation, and rollback part of the operating environment.
5. **Make successful local workflows reusable.** Treat platform improvements, evaluations, controls, and operational lessons as organizational capabilities so lessons from one deployment can inform the next.

## Positioning note

This is an applied technical note and a structured synthesis of industry reports, engineering guidance, and company accounts. It is not an academic paper: it does not present original data, a controlled experiment, or a causal evaluation of the claims. Its thesis is tied to cited evidence and concrete operating mechanisms rather than anecdotes alone. It is not vendor documentation: the linked vendor and company material is used as source evidence, not as an instruction to adopt a particular product or operating model.

The note's durable claim is narrower than “AI will replace expertise.” It is that falling implementation costs move scarce expertise toward experimentation systems, platforms, evaluation, and boundaries. The appropriate implementation of that claim depends on the authority and consequences of the systems involved.

## Status & scope disclaimer

**Status:** Exploratory and applied research synthesis; not a validated empirical study.

This is personal lab work from rmax lab and is intended for discussion, design exploration, and operational reflection. It is non-authoritative and should not be treated as legal, compliance, security, safety, hiring, or organizational advice. The cited reports and company accounts are time-bound source material; their measurements, descriptions, and interpretations may change.

The scope is the changing role of AI expertise in software building, experimentation, platform engineering, governance, assurance, and agentic operations. It does not attempt to provide a complete labor-market forecast, compare vendors, define a universal governance framework, or establish that the cited organizational patterns generalize to every startup, enterprise, or regulated system.

## Conclusion

AI turns everyone into a potential builder. That does not make engineers, AI specialists, or platform experts irrelevant. It changes where their expertise compounds.

In a startup searching for product-market fit, the AI expert should maximize the rate at which hypotheses become experiments. As the organization scales, the expert increasingly builds the factory: reusable tools, agent harnesses, knowledge systems, and deployment paths.

Once AI-assisted creation becomes ubiquitous and consequential, the expert's highest-leverage responsibility moves again: designing the boundaries, evaluations, platforms, and control systems that allow thousands of humans and agents to build without requiring thousands of manual reviewers.

The trajectory is therefore not:

> **experts → no experts**

It is:

> **Builder → Builder of Builders → Designer of Boundaries**

AI makes production abundant. The scarce resource becomes confidence that what was produced deserves to run.

## References

1. [Anthropic — Agentic coding and persistent returns to expertise](https://www.anthropic.com/research/claude-code-expertise)
2. [Figma — 2026 AI Report](https://www.figma.com/blog/2026-ai-report/)
3. [Microsoft — 2026 Work Trend Index](https://www.microsoft.com/en-us/worklab/work-trend-index/agents-human-agency-and-the-opportunity-for-every-organization)
4. [OpenAI — Enterprise Signals](https://openai.com/signals/enterprise-data/)
5. [Figma — What matters when anyone can build](https://www.figma.com/blog/what-matters-when-anyone-can-build/)
6. [Google Cloud — 2025 DORA Report](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)
7. [Google SRE — Error Budget Policy](https://sre.google/workbook/error-budget-policy/)
8. [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
9. [Anthropic — How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude)
10. [NIST — Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
11. [OWASP — Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
12. [TechCrunch — Shopify CEO AI/headcount memo](https://techcrunch.com/2025/04/07/shopify-ceo-tells-teams-to-consider-using-ai-before-growing-headcount/)
13. [Microsoft Inside Track — Frontier Forge](https://www.microsoft.com/insidetrack/blog/the-frontier-firm-how-knowledge-workers-are-forging-their-own-ai-tools-at-microsoft/)
14. [Microsoft Inside Track — Becoming a Frontier Firm](https://www.microsoft.com/insidetrack/blog/becoming-a-frontier-firm-a-guide-for-deploying-ai-agents-based-on-our-experience-at-microsoft/)
15. [Microsoft Inside Track — AI-native software development](https://www.microsoft.com/insidetrack/blog/engineering-the-frontier-firm-sharing-our-ai-native-approach-to-software-development/)
16. [Spotify Engineering — Coding Is No Longer the Constraint](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint)
17. [OpenAI — BBVA puts AI at the core of banking](https://openai.com/index/bbva/)
18. [OpenAI — BBVA scaling AI from pilot to practice](https://openai.com/index/bbva-2025/)
19. [OpenAI — Endava redesigning software delivery around agents](https://openai.com/index/endava-frontiers/)
20. [Microsoft — FY26 Frontier Transformation](https://blogs.microsoft.com/blog/2026/07/28/looking-back-on-microsofts-fy26-from-ai-experimentation-to-frontier-transformation/)
21. [CNCF — What is platform engineering?](https://www.cncf.io/blog/2025/11/19/what-is-platform-engineering/)
22. [CNCF — Platform engineering maturity](https://www.cncf.io/blog/2026/09/01/platform-engineering-maturity-from-toolchain-to-self-service/)
23. [OpenAI — How enterprises are scaling AI](https://openai.com/business/guides-and-resources/how-enterprises-are-scaling-ai/)
