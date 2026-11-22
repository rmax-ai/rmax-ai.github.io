---
title: "RMax AI, Year One: From Agents to Verified Work"
slug: rmax-ai-year-one-from-agents-to-verified-work
description: "A first-year field report from a personal agent lab. The November audit counted 77 dated technical notes and 1,078 recorded queue tasks. Verified delivery remains unmeasured."
author: Max
site: rmax.ai
section: notes
type: essay
status: published
date: 2026-11-19
updated: 2026-11-19
tags:
  - year one
  - agent systems
  - governance
  - verification
  - field report
  - agent orchestration
  - retrospective
reading_time: "12-13 min"
canonical_url: https://rmax.ai/notes/rmax-ai-year-one-from-agents-to-verified-work/
license: "CC BY 4.0"
---

# RMax AI, Year One: From Agents to Verified Work

A patch can survive the conversation that produced it. Can the next operator tell who requested it, which revision passed review, and who decided to use it?

November 2025 – November 18, 2026

<aside class="census" aria-label="Year at a glance">
  <dl>
    <div><dt>dated technical notes</dt> <dd>77</dd></div>
    <div><dt>recorded queue tasks</dt> <dd>1,078</dd></div>
  </dl>
  <p><strong>Audit cutoff · November 18, 2026</strong><br>Verified delivery was not established by this census.</p>
</aside>

<nav class="chapters" aria-label="Chapters">
  <a href="#the-year">The year</a>
  <a href="#built">What we built</a>
  <a href="#loop">How it works</a>
  <a href="#priorities">2027</a>
</nav>

The operator dates the lab’s beginning to November 2025 and recalls a narrow question: how much software work can an agent take on? By the following November the operator faced a different set of questions. Who owns an interrupted task? Which revision passed review? Can a useful result be recovered after the conversation that produced it disappears?

**Useful autonomy depends on recoverable state, explicit ownership, and evidence for consequential decisions.** A model can submit a patch. Someone taking over tomorrow needs the request, the revision, the check that ran, and the decision about what happens next.

The evidence base is a November 18, 2026 operational audit of the lab's own repositories, sessions, scheduled jobs, task outcomes, and review findings, plus two public field reports written during the year. The audit is a historical observation of a system inspecting itself, not an independent reproduction. Numbers in this article carry their denominator and their cutoff; where the audit's own figures disagree with each other, this article reports the disagreement rather than resolving it silently. The [evidence appendix](evidence-notes/) records every definition, correction, and unresolved measurement.

<h2 id="the-year">A year of building the system around the model</h2>

The early work assumed the bottleneck was capability. The year's projects, read together, show the bottleneck moving: from whether an agent can produce a change, to whether the change can be judged, attributed, and kept.

Those apparently different projects — agent runtimes, research assistants, evaluation harnesses, knowledge pipelines, and the publication workflow itself — all explore the same question: how do you turn uncertain model output into an inspectable process? The January notes on [agent-first software engineering](https://rmax.ai/notes/agent-first-software-engineering/) stated the direction early. The September [control-plane field report](https://rmax.ai/notes/from-human-orchestrated-agent-to-autonomous-control-plane/) described what it cost to operate.

## The chronology, including the gaps

<p>Figure 1 — Milestones are spaced by category. The distance between them does not represent elapsed time.</p>
<ol class="timeline">
  <li><span class="period">November 2025</span>
    <div><h3>The operator dates the beginning</h3>
      <p>The operator recalls starting the lab that November. The audit located no artifact for the month.</p>
      <small>Operator account</small></div>
  </li>
  <li><span class="period">Dec 2025 – Jan 2026</span>
    <div><h3>The work leaves a record</h3>
      <p>The first surviving repository evidence dates to December 23. Public notes began January 3 and set out principles for granting agents authority. Workspace records survive from January 31.</p>
      <small>Repository and runtime records</small></div>
  </li>
  <li><span class="period">Feb – Mar 2026</span>
    <div><h3>Experiments reach applications</h3>
      <p>The portfolio grew to include an editing workflow, a book project and an application prototype. Their commits record work in progress.</p>
      <small>Repository records</small></div>
  </li>
  <li><span class="period">April 2026</span>
    <div><h3>Heartbeats without indexed work</h3>
      <p>The audit found no indexed organization commits or issues in the inspected records. All 30 inspected sessions contained only heartbeats. The cause remains unknown.</p>
      <small>Repository and runtime records</small></div>
  </li>
  <li><span class="period">May – Jul 2026</span>
    <div><h3>The runtime changes</h3>
      <p>The assistant moved to Hermes on May 11. Scheduled knowledge work expanded, and repositories began documenting bounded research loops. Their maturity varied.</p>
      <small>Runtime and repository records</small></div>
  </li>
  <li><span class="period">Aug – Oct 2026</span>
    <div><h3>Handoffs come under review</h3>
      <p>Telemetry and a tool gateway preceded a second-model request channel. A September field report traced lost handoffs. October benchmark reruns tested earlier results.</p>
      <small>Repository records and operator account</small></div>
  </li>
  <li><span class="period">Nov 1 – 18, 2026</span>
    <div><h3>The audit closes</h3>
      <p>Maintenance and evaluation continued through the November 18 cutoff. The audit counted queue states and left deployment and subsequent use unmeasured.</p>
      <small>Runtime and repository records</small></div>
  </li>
</ol>

See the [detailed chronology in the evidence appendix](evidence-notes/#chronology) for the monthly records and their limits.

April posed a practical problem for the operator. A heartbeat could confirm that a recurring process was alive even when the inspected records showed no work advancing. The distinction matters when choosing what to monitor after a restart. The audit cannot establish the cause of the pause or describe activity outside the records it inspected.

<h2 id="built">What the year produced</h2>

The November audit counted **145 repositories** across the organization, including experiments, scaffolds, supporting infrastructure, and imported upstream history. That is a measure of portfolio size, not a count of finished applications. Grouping the work by what it demonstrates is more useful.

**Governed application workflows.** [Deep Research Assistant](https://github.com/rmax-ai/deep-research-assistant) documents a 27-node workflow with 14 bounded agents, persisted checkpoints, approval branches, and claims linked to evidence; continuous research remains partial, and live-model validation is separate from its deterministic checks. [Relocation Scout](https://github.com/rmax-ai/relocation-scout) makes a related boundary visible in a smaller application: the prototype assigns state transitions and approval checks to code, agents assess listings and draft messages, and a human authorizes external action. It remains a proof of concept with mock email and no production authentication.

**Reusable execution patterns.** [ADK Loop Lab](https://github.com/rmax-ai/adk-loop-lab) implements document refinement, evidence research, and resumable coding examples; its contribution is the surrounding loop of persisted state, verification, budget controls, and explicit stopping decisions. The [portable skills repository](https://github.com/rmax-ai/skills) captures reusable procedures as versioned artifacts. Those artifacts make adoption possible; their existence does not show that every workflow uses them correctly.

**Research and evaluation.** [Jev versus Clef](https://github.com/rmax-ai/jev-vs-clef) supplies dated runs and raw calls for a concrete model-substitution question; other laboratories investigate recursive execution, retrieval choices, regeneration, and model–harness fit. The transferable accomplishment is an experimental structure that can preserve a negative or changed result — a repository name or evaluation scaffold alone does not demonstrate that a hypothesis succeeded.

**Knowledge and publication.** Video-insight processing, knowledge-graph work, and the [static insights explorer](https://github.com/rmax-ai/yt-insights-explorer) connect source material to inspectable artifacts; extracted claims still need verification. On the writing side, the corrected census found **77 dated technical notes** plus one redirect page — **78 published note pages**, not 78 distinct articles. January's 17 notes are the publication peak, not June's 14. The public [notes index](https://rmax.ai/notes/) makes the writing accessible; the audit obtained no readership or adoption data.

**An operating coordination system.** The most consequential integration joins a persistent rmax-10 orchestrator, ChatGPT for analysis and review, bounded Codex and Droid execution, GitHub state, and human review. The agent runtime is an upstream framework adopted and extended for this system; the lab's contribution lies in the integration, protocols, experiments, and operational practice, and imported upstream history is not original output.

<h2 id="loop">How the coordination loop works</h2>

The architecture separates communication from durable state. Chat and Slack are places to request attention. GitHub holds the task, its ownership, implementation artifacts, and review history. A local delegation queue manages attempts through coding-agent execution paths. A second model supplies an additional reasoning and review surface through a structured request channel. The operator retains consequential approval decisions.

<img src="figures/fig-2-control-loop.svg" alt="Scope enters GitHub from the operator. Execution returns a checked revision for review and a merge decision. Failed checks can retry locally. A new task is a proposed follow-up.">

*Figure 2 — Where authority changes hands. The [September field report](https://rmax.ai/notes/from-human-orchestrated-agent-to-autonomous-control-plane/) documents the responsibilities and observed handoff failures.*

<ol class="architecture-key">
  <li><strong>Human authority.</strong> The operator sets the initial scope. After review, the operator decides whether to merge or adopt a consequential change.</li>
  <li><strong>Durable coordination and state.</strong> rmax-10 dispatches bounded attempts. GitHub holds the task, owner, revision, review and disposition. A proposed follow-up needs its own decision and owner.</li>
  <li><strong>Execution and verification.</strong> A Codex or Droid lane returns a revision. A failed local check can return it to execution. Check evidence goes to independent review, where ChatGPT can supply a second assessment.</li>
</ol>

The separation makes asynchronous collaboration recoverable. A new session can inspect the task instead of reconstructing intent from fragments of chat. An execution attempt can fail while the work item survives. A reviewer can reject a change without losing the original request. None of that is automatic: it holds only where the state is written down at the moment authority changes hands.

The audit contains acceptance verdicts. It does not track whether a reviewer’s finding later changed another task’s acceptance criteria or the instructions used by the next agent.

### When an answer leaves work open

The September field report describes a failure in which a response was marked consumed while follow-up work remained unresolved. Successful delivery had been treated as successful completion. Similar failures included tools that existed but did not run in their intended workflow, and ownership lost across handoffs.

The correction is a stronger completion model. A received answer needs an explicit disposition: implemented and verified, delegated with a new owner, waiting on a named decision, or closed with a recorded reason. The acknowledgement belongs to the communication protocol; the disposition belongs to the work lifecycle. Both need evidence.

That lesson changes how the annual numbers should be read. The November queue census recorded **1,078 tasks**: 809 in `SUCCEEDED`, 210 failed, 58 cancelled, and one still running. Those states sum correctly, and they are still not 809 deployed improvements. The system has documented hollow completion — a lane reporting success with a valid task record and no committed change — so a success label is a statement about the queue, not about the software.

<img src="figures/fig-3-outcomes.svg" alt="Queue snapshot of 1,078 tasks. Of these, 809 succeeded, 210 failed, 58 were cancelled and one was running.">

*Figure 3 — Recorded task states on November 18. The running task was still open at collection. A success label alone supplies no independent evidence of deployment or use.*

### What a preserved rerun lets a reader check

The [Jev/Clef benchmark](https://github.com/rmax-ai/jev-vs-clef) preserves the questions, raw calls and dated results from two runs of the same 159-call battery. Only 24 of the 159 calls in each run tested decisions against the author’s labels. On that subset Jev’s reported agreement fell from 92% on October 3 to 83% on October 6. Clef 27B scored 96% on both dates. The second result changed what a reader could say about substituting Jev for Clef on those questions.

A reader comparing the runs needs the execution date as well as the directory name. The second directory says October 4, while the run took place on October 6. The raw calls also let a reader distinguish two models giving the same answer from either model matching the label. Neither test establishes a universal model ranking. The author supplied the labels for synthetic decisions. Timing depended on the measurement environment, and a November follow-up separately corrected a client-path latency measurement.

## Where the system still falls short

**Verification requires its own verification.** The audit reported 518 acceptance failures against a stated total of 1,375 attempts, or 37.7%. Its listed category counts sum to 1,380. The original query was not rerun and neither figure was independently recounted. The difference of five does not identify which records belong to either total.

The audit did not classify causes. Unclear criteria, an incorrect working directory, a missing artifact, a faulty evaluator and an implementation defect are hypotheses a reviewer could test against individual attempts. The aggregate rate cannot tell an operator which repair to make.

**Detection has outpaced demonstrated learning.** The audit recorded 155 system-review findings, with silent degradation the largest category at 41. Detecting a problem, proposing a repair, and retaining a lesson are three different achievements. A convincing improvement trace needs a failing observation, a reviewed change, evidence that the changed system ran, and a later observation showing the failure was reduced. A new skill file or another report establishes one part of that trace, usually the first.

**Coordination creates maintenance work.** The audit counted 291 open request-channel issues against 844 requests over 59 days; the three status labels account for 834 of those requests (590 consumed, 241 answered, 3 pending), and the remaining ten are unaccounted for by any supplied cross-tabulation, so this article leaves them unclassified. Open does not mean abandoned: some work legitimately awaits review or another owner. The concern is whether each item has a meaningful next state. Growth creates a similar obligation — with 145 repositories and 317 installed skills in the snapshot, discovery, overlap, ownership, and retirement become engineering problems of their own.

**The economic picture is incomplete.** The audit reports $298.27 of tracked agent cost for September through the November cutoff. That is neither the year's total expenditure nor a return-on-investment calculation. Earlier cost attribution, infrastructure, operator time, and the value of outcomes remain unmeasured. Reported token counts include context reuse and cannot be converted into unique billed consumption.

These limitations constrain the claim. The evidence supports a substantial supervised system capable of sustained delegation and self-observation. It does not establish dependable end-to-end self-improvement, or independence from human recovery and judgment.

<h2 id="priorities">A proposed 90-day scorecard for 2027</h2>

Day 1 after operator approval opens the proposed measurement window. The historical counts identify work to inspect. Owners would establish the starting populations, record their inclusion rules and retain the identifiers needed to follow a request across retries. The first review would use the following artifacts.

<div class="scorecard">
  <section>
    <h3>Reliable delivery</h3>
    <dl>
      <dt>Owner</dt> <dd>Queue maintainer and independent reviewer</dd>
      <dt>Baseline</dt> <dd>Unresolved baseline for attempt membership and verified outcomes.</dd>
      <dt>First artifact</dt> <dd>Reconciled attempt ledger with a cause review of sampled failures.</dd>
      <dt>90-day measure</dt> <dd>Acceptance failures / all reconciled attempts during days 1–90. Proposed target of 10%. Also report independently verified deliveries / implementation tasks opened in the window.</dd>
      <dt>Safeguard</dt> <dd>Keep check versions and review samples of passes as well as failures. Count retries separately from tasks.</dd>
    </dl>
  </section>
  <section>
    <h3>Handoff ownership</h3>
    <dl>
      <dt>Owner</dt> <dd>Request-channel operator</dd>
      <dt>Baseline</dt> <dd>Historical snapshot of 291 open issues. Unresolved baseline for time to disposition.</dd>
      <dt>First artifact</dt> <dd>Answer register linking each response to an owner, timestamp and disposition.</dd>
      <dt>90-day measure</dt> <dd>Answers dispositioned within 48 hours / all requests answered on days 1–88. The proposed 95% target allows each answer its full 48 hours before day 90.</dd>
      <dt>Safeguard</dt> <dd>Inspect transfers and reasons for closure. The proposed 60-open target is secondary to resolving the work.</dd>
    </dl>
  </section>
  <section>
    <h3>Reusable results</h3>
    <dl>
      <dt>Owner</dt> <dd>Portfolio maintainers</dd>
      <dt>Baseline</dt> <dd>Historical inventory of 145 repositories. Unresolved baseline for maintained, reproducible outcomes.</dd>
      <dt>First artifact</dt> <dd>Results index naming an owner, runnable example, expected result and limitation for each candidate.</dd>
      <dt>90-day measure</dt> <dd>Entries independently reproduced with a current maintainer / all entries nominated at the start, assessed by day 90.</dd>
      <dt>Safeguard</dt> <dd>Retain failed reproductions and missing owners in the denominator. The proposed 110-repository ceiling is secondary to maintained results.</dd>
    </dl>
  </section>
</div>

A delivery reviewer would begin with the revision the executor actually used. The command, working directory and expected artifact are part of the record. A failing check against the wrong directory calls for a different response from a valid rejection of an incomplete implementation. An unresolved case should keep its place in the ledger until someone can distinguish those explanations.

For the handoff review, start with the oldest unresolved answers. A disposition can document verified completion, a linked transfer accepted by the next owner, deliberate deferral, or a reason that no action is needed. A consumed response on its own answers none of those questions. Record enough of the handoff for someone outside the original conversation to follow it.

For portfolio review, distinguish maintained systems, supporting components, active experiments and potential archives. Check consumers and unfinished work before proposing a retirement, and preserve a restoration path. A rarely used skill may still support an important recovery procedure. Reproducing a result from its recorded inputs gives the maintainer a concrete test of whether consolidation preserved what another operator needs.

## Practical takeaways

- **Define completion before delegation.** Name the artifact, its verification, the decision owner, and the condition for stopping or handing back.
- **Keep communication and work states distinct.** A delivered message, an accepted task, a merged change, a deployed revision, and a useful outcome each require different evidence.
- **Preserve failed and changed results.** A rerun that weakens a claim improves the research if the comparison stays reproducible.
- **Audit the measurement path.** A status label or green check is informative only when its source, coverage, and failure behaviour are known.
- **Budget for maintenance.** Every repository, job, skill, and agent adds obligations for ownership, diagnosis, and eventual retirement.

At day 90 the operator could take the implementation tasks opened during the window and ask how many produced a result an independent reviewer could verify and a named maintainer could still use. Keep unfinished work in that denominator. Year one supplied task records and dated artifacts from which to start asking that question. It left the answer open.

## Positioning note

This is an applied field report from a personal lab. It is not a controlled study of autonomous software engineering, vendor documentation, or a claim that the architecture is universally optimal.

## Status and scope

Project implementations range from early prototypes to operational components; historical deployment does not certify present reliability. The operational aggregates are a November 18, 2026 snapshot of the lab's own audit, with corrections and limitations retained in the [evidence appendix](evidence-notes/); they are not live counters. AI assistance contributed to the research synthesis, the operational audit, and the editorial revision.

## Sources

1. [Evidence appendix: metric definitions, denominators, and corrections](evidence-notes/).
2. [RMax AI public notes](https://rmax.ai/notes/) and the [publication repository](https://github.com/rmax-ai/rmax-ai.github.io).
3. [Agent-First Software Engineering](https://rmax.ai/notes/agent-first-software-engineering/).
4. [From Human-Orchestrated Agent to Autonomous Control Plane](https://rmax.ai/notes/from-human-orchestrated-agent-to-autonomous-control-plane/).
5. [Deep Research Assistant](https://github.com/rmax-ai/deep-research-assistant), [Relocation Scout](https://github.com/rmax-ai/relocation-scout), and [ADK Loop Lab](https://github.com/rmax-ai/adk-loop-lab).
6. [Portable skills](https://github.com/rmax-ai/skills) and [YT Insights Explorer](https://github.com/rmax-ai/yt-insights-explorer).
7. [Jev/Clef experiment: dated runs, raw calls, and caveats](https://github.com/rmax-ai/jev-vs-clef).
