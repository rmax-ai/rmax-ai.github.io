# The Change Is the Unit of Assurance

AI-generated software needs a persistent evidence model that survives the pull request.
AI can now produce software faster than organizations can understand, verify, and safely deploy it.
DORA’s research describes the resulting tension: AI can increase author velocity while transferring cognitive load to reviewers, and faster code generation can produce larger batches, slower review, and greater instability. DORA: Balancing AI tensions DORA: Impact of Generative AI in Software Development
The usual response is to improve code review: inspect fewer lines, generate better summaries, or add specifications, invariants, test results, security scans, and residual risks to pull requests.
All of that helps, but it starts from the wrong boundary.
The pull request and the diff are not the units of assurance. They are temporary views of a larger object: the persistent software change.
A software change includes not only its implementation, but also its intent, behavioral claims, affected boundaries, invariants, risk, evidence, deployment history, runtime observations, and unresolved uncertainty:
Change
├── intent
├── behavioral claims
├── affected boundaries
├── invariants
├── risk
├── implementation
├── evidence
├── deployment state
├── runtime observations
└── residual uncertainty
The diff is one representation of that change. The pull request is one interface. CI, deployment systems, observability, and incident records are evidence producers.
The change itself should be the unit of assurance.
That distinction matters because assurance does not end when a pull request is approved. Some claims can be supported before deployment. Others require real traffic. Still others may become false weeks later as dependencies, configurations, workloads, or operating conditions change.
The central engineering problem is therefore not how to make reviewers inspect diffs faster. It is how to maintain justified confidence in a change throughout its lifecycle.
This is not only a conceptual shift. It implies concrete changes to engineering practice:
1. Create a durable record for each consequential change.
2. State the change’s intent and claims before implementation is considered complete.
3. Link each important claim to evidence and to the conditions under which that evidence was collected.
4. Define which claims require production validation.
5. Make rollout, monitoring, rollback, and incident response update the same record.
6. Use risk to determine how much evidence and human review are required.
The rest of this article develops that operating model.
Assurance already extends beyond testing
Lifecycle assurance is not new.
NASA’s Software Assurance and Software Safety Standard describes assurance, safety, and independent verification and validation across the software lifecycle, including operations, maintenance, and retirement. NASA-STD-8739.8B
NIST’s Secure Software Development Framework likewise includes preparation, software protection, secure production, and response to vulnerabilities discovered after release. It recommends tracking requirements, risks, design decisions, and provenance rather than treating security as a final check. NIST Secure Software Development Framework
Assurance cases provide the conceptual model: a structured argument connecting claims about a system to evidence and assumptions. ISO/IEC/IEEE 15026-2:2022 applies this model to both developing and maintaining assurance cases. ISO/IEC/IEEE 15026-2:2022
The OMG Structured Assurance Case Metamodel makes such arguments machine-representable and supports evidence including tests, measurements, records, expert judgments, and automatically collected artifacts. OMG Structured Assurance Case Metamodel
The ingredients already exist:
claims
evidence
provenance
lifecycle assurance
runtime monitoring
AI changes the scale at which ordinary software engineering may need to combine them.
It also changes the economics. A heavyweight assurance case for every small documentation edit would be wasteful.
A lightweight, machine-maintained assurance record for a high-impact autonomous change may be practical and necessary.
The goal is not to impose the same process on every change. It is to make the process proportional, persistent, and operationally useful.
AI changes the economics of assurance
Historically, implementation constrained throughput. An engineer building a feature also developed a mental model of its architecture, assumptions, dependencies, and failure modes.
AI weakens that coupling. An agent can create services, schemas, APIs, deployment configuration, tests, telemetry, and documentation without anyone acquiring the same implementation-level understanding.
The generated software may be deterministic. The problem is epistemic: the artifact can appear faster than organizational confidence in it.
software generation throughput
            >
assurance throughput
DORA’s research captures this at the review layer: creation and verification are different cognitive tasks, and AI-generated changes can turn author velocity into reviewer load. DORA: Balancing AI tensions
Making humans read generated code faster is unlikely to scale. The more useful question is:
What persistent object would let machines and humans accumulate justified confidence in a software change without requiring human comprehension to grow linearly with generated code volume?
The answer is the change itself.
That answer becomes practical only when the change has an explicit lifecycle. A useful minimum lifecycle is:
proposed
   ↓
specified
   ↓
implemented
   ↓
verified
   ↓
deployed progressively
   ↓
observed
   ↓
accepted, remediated, rolled back, or superseded
Each transition should have an owner, an entry condition, an exit condition, and recorded evidence. Without those controls, “persistent assurance” risks becoming another documentation layer that no one trusts or maintains.
A change is a collection of claims
Consider an agent modifying payment retry logic.
A traditional pull request might show:
PR #4831

47 files changed
+2,318
-614
Those numbers say little about acceptability. A more useful representation is:
Change: modify payment retry policy

Intent:
Reduce failures caused by transient PSP errors.

Claims:
C1. A payment can never be captured twice.
C2. Retry amplification remains bounded.
C3. Existing authorization semantics are unchanged.
C4. p99 payment latency increases by less than 5%.
C5. Payment success rate does not regress.

Affected boundaries:
- payment orchestration
- PSP client
- retry scheduler
- idempotency store

Risk:
financial: high
availability: medium
privacy: unchanged

Residual uncertainty:
behavior during prolonged partial PSP degradation
has not been reproduced realistically.
The implementation realizes these claims, but the claims are closer to what the organization needs to know. This is the central idea behind assurance cases: confidence is organized around claims and evidence, not artifact inspection alone. (ISO)
In ordinary development, this structure is fragmented across issue trackers, design documents, Git, CI, delivery systems, observability, and incident records.
AI gives us a reason to reconstruct it as one persistent object.
Write claims before reviewing implementation
A practical rule follows:
Do not ask reviewers to determine whether a large generated change is safe before stating what “safe” is supposed to mean.
For consequential changes, the author or agent should produce a short change brief before implementation is approved for merge. It should contain at least:
intent
in-scope behavior
out-of-scope behavior
affected system boundaries
top risks
behavioral claims
required evidence
known uncertainty
rollback strategy
Claims should be specific enough to test or observe. Compare:
Weak:
Improve payment reliability.

Stronger:
Under transient PSP failures, retryable payment attempts
eventually succeed or fail without creating duplicate captures.

Operational:
During canary and full rollout, duplicate captures remain zero,
payment success rate does not decline, and p99 latency increases
by less than 5% relative to the control population.
The stronger claims are not necessarily formal proofs. They are decision-relevant statements that can guide test design, rollout policy, monitoring, and incident analysis.
Separate claims from assumptions
A claim is something the organization wants to establish. An assumption is a condition under which the argument is valid.
For example:
Claim:
A payment is captured at most once.

Assumptions:
- payment_id is globally unique
- the idempotency store is durable
- PSP responses are correctly classified
- clock skew remains within the supported bound
Assumptions deserve explicit treatment because they are common sources of assurance failure. A test may pass while an unstated assumption is false in production.
A useful change record should therefore distinguish:
claims
assumptions
evidence
known gaps
Evidence arrives at different times
Assurance cannot always be completed before merge.
For example:
C1: The new retry policy cannot produce duplicate captures.
Pre-deployment evidence might include:
property tests
concurrency tests
integration tests
static analysis
model checking
PSP simulator results
But consider:
C5: Payment success rate does not regress under real traffic.
No unit test or static analyzer can establish that. Pre-production environments may not reproduce real traffic distributions, dependency behavior, load, configuration, network effects, and failure modes.
Google’s SRE guidance addresses this with canarying: expose a change to a bounded subset of production, evaluate it, and use the results to decide whether rollout should continue. Google SRE: Canarying Releases
Evidence therefore accumulates across phases:
Before execution:
types, tests, formal checks, architecture constraints,
dependency and security analysis, provenance

Bounded execution:
canary metrics, runtime invariants, shadow traffic,
SLO comparisons, error rates, performance distributions

Sustained operation:
long-tail behavior, dependency failures, real workloads,
security findings, incidents, drift, unexpected interactions
The confidence attached to a claim evolves with the evidence.
Make evidence claim-specific
A test suite should not merely report “passed.” It should identify which claims it supports and what it does not establish.
For example:
evidence:
  - id: concurrency-suite-1842
    type: automated_test
    status: passed
    supports:
      - no_duplicate_capture
      - bounded_retry_amplification
    conditions:
      - 1,000 concurrent payment attempts
      - simulated PSP timeout and retry responses
    limitations:
      - does not model prolonged PSP partition
      - does not validate production traffic distribution
This prevents a common failure mode: treating a large green test suite as evidence for claims it was never designed to evaluate.
Every important claim should have one of three explicit statuses:
supported
not yet supported
not applicable
“Not yet supported” is valuable information. It tells the rollout system and reviewers what remains to be learned.
Record evidence immutably enough to trust
Evidence should be linked to the exact inputs that produced it:
source revision
agent or human actor
tool and version
configuration
environment
dependency versions
timestamp
result
artifact location
The record does not need to be immutable in an absolute sense, but changes to evidence should be auditable. A later reviewer should be able to distinguish:
the original result
a corrected result
a superseded result
a manually entered judgment
This is where supply-chain provenance practices are useful. The same discipline applied to build artifacts can be applied to assurance evidence.
Assurance is a state, not a Boolean
Delivery systems often reduce acceptance to:
not approved
    ↓
approved
or:
CI failed
    ↓
CI passed
A more useful model is:
proposed
   ↓
supported by analysis
   ↓
verified under test
   ↓
validated under bounded production exposure
   ↓
validated under sustained operation
At any point:
claim falsified
      ↓
rollback / remediation / new investigation
The goal is not to assign artificial probabilities to every judgment. It is to preserve three distinctions:
what we claim
what evidence supports it
under which conditions that evidence was obtained
Runtime verification provides a formal precedent: execution traces can be evaluated against specifications while a system is running rather than only before deployment. Survey of Runtime Verification
Recent research similarly explores updating confidence in safety arguments with runtime evidence. Runtime confidence updates in safety arguments, SAC 2026
The general pattern is:
design-time evidence
        +
runtime evidence
        ↓
updated assurance state
AI-native software engineering may need a lightweight operational version of this model.
Define explicit state transitions
A practical assurance state machine might look like this:
proposed
  └─ claims and risk recorded

ready_for_review
  └─ required design and evidence plan present

verified
  └─ pre-deployment evidence satisfies policy

approved_for_canary
  └─ rollback, monitoring, and exposure limits configured

canarying
  └─ bounded production evidence being collected

approved_for_rollout
  └─ canary gates satisfied

observing
  └─ full deployment complete; post-deployment window active

accepted
  └─ required observation period complete

blocked
  └─ required evidence missing or contradictory

falsified
  └─ a claim violated or a critical assumption failed

rolled_back
  └─ exposure reduced or removed

superseded
  └─ a later change replaces the current behavior
The exact names are less important than the discipline. A change should not move from one state to another merely because someone clicked a button. The transition should be tied to evidence and policy.
For example:
verified → approved_for_canary
might require:
all critical checks passed
no unresolved critical security findings
rollback tested
required dashboards exist
claim-to-evidence coverage complete
And:
canarying → approved_for_rollout
might require:
minimum exposure duration met
minimum event count met
no critical invariant violations
error-rate comparison within threshold
latency comparison within threshold
business metric comparison within threshold
Do not confuse absence of evidence with evidence of safety
A runtime monitor that reports no violations has not necessarily established that the invariant is true. It may have observed too few relevant events, monitored the wrong population, or failed silently.
Every runtime claim should therefore include observability conditions:
metric coverage
event volume
sampling rate
monitor health
alert latency
known blind spots
For example:
Claim:
No duplicate captures occurred during canary.

Evidence:
zero duplicate-capture events observed.

Qualification:
the monitor processed 99.98% of capture events;
the remaining 0.02% are pending reconciliation.
This level of precision may seem excessive for low-risk changes. That is why risk-based tiers matter.
The change should survive the pull request
Merging a pull request often destroys the conceptual boundary that matters.
The repository retains the commit. The deployment platform knows what is running. Observability records telemetry. Incident systems record failures. But the claims that justified the change rarely connect these systems as first-class objects.
Imagine that every consequential change receives a persistent identifier:
change://payments/retry-policy/4831
Its assurance record might look like:
change:
  id: payment-retry-policy-4831
  intent: reduce transient PSP failures
  owner: payments-team
  created_at: 2026-03-08T10:15:00Z
  source_revision: 7f3a91c
  risk_tier: high

claims:
  - id: no_duplicate_capture
    statement: capture_count(payment_id) <= 1
    criticality: critical
    validation:
      pre_merge: required
      canary: required
      sustained_operation: required

  - id: latency_regression
    statement: p99_delta < 0.05
    criticality: medium
    validation:
      pre_merge: required
      canary: required

  - id: success_rate
    statement: success_rate_delta >= 0
    criticality: high
    validation:
      canary: required
      sustained_operation: required

evidence:
  pre_merge:
    - id: property-test-1842
      status: passed
      supports:
        - no_duplicate_capture
        - bounded_retry_amplification

    - id: integration-suite-1843
      status: passed
      supports:
        - authorization_semantics

  canary:
    traffic: 5%
    duration: 2h
    duplicate_capture_violations: 0
    p99_delta: 0.021
    success_rate_delta: 0.004
    status: passed

  production:
    status: observing

uncertainty:
  - prolonged_partial_psp_outage

rollback:
  mechanism: feature_flag
  owner: payments-oncall
  tested_at: 2026-03-08T09:30:00Z
The pull request becomes one view of this object.
CI appends evidence. Deployment changes exposure state. Runtime monitors append observations. Incidents can invalidate claims. Rollbacks change operational state. Later changes can reference or supersede earlier claims.
This creates a causal thread from why a change was made to what justified deployment to what happened after deployment.
Start with a minimum viable record
Organizations do not need to build a complete assurance platform before adopting the model. A practical first version can be implemented with existing tools.
For every medium- or high-risk change, require:
change ID
owner
intent
risk tier
affected services
three to five key claims
evidence plan
rollback mechanism
monitoring links
deployment status
residual uncertainty
Store the record in a version-controlled file, an issue tracker, or a deployment metadata store. The important properties are:
durable
searchable
linked to the deployed revision
updated by automation where possible
visible during review and operations
A simple repository file might be enough to begin:
change_id: payments-retry-policy-4831
owner: payments-team
risk_tier: high
intent: reduce transient PSP failures

claims:
  - id: no_duplicate_capture
    statement: capture_count(payment_id) <= 1
    evidence_required:
      - concurrency_tests
      - canary_invariant
      - reconciliation_report

rollback:
  mechanism: feature_flag
  owner: payments-oncall

uncertainty:
  - prolonged_partial_psp_outage
The record can later be enriched by CI, deployment automation, and observability integrations.
Make the record operational, not ceremonial
A record that no system reads will become stale.
At minimum, integrate it with delivery controls:
missing critical claim → block approval
missing rollback plan → block canary
missing runtime monitor → block rollout
critical invariant violation → pause or roll back
unresolved high-severity finding → require explicit exception
This is the difference between documentation and assurance infrastructure.
The record should influence what the system permits.
Provenance shows that persistent evidence is plausible
Software supply-chain systems already demonstrate that engineering evidence can be structured, machine-generated, persistent, and independently verifiable.
SLSA defines provenance as verifiable information about where, when, and how an artifact was produced. SLSA Provenance
in-toto records metadata for supply-chain steps and establishes a chain that can later be validated. in-toto: Getting Started
Those systems ask:
Where did this artifact come from?
Who or what produced it?
Which source and build process were used?
Were required steps followed?
Change assurance asks broader questions:
Why was this change made?
What is it supposed to preserve?
What could go wrong?
Which evidence supported deployment?
What happened under real execution?
Which assumptions remain unresolved?
The relevant lesson is not a particular format. It is the feasibility of maintaining verifiable evidence across a lifecycle.
Preserve the chain from intent to runtime
A useful provenance chain for a software change should connect:
intent
  ↓
claims
  ↓
source revision
  ↓
build artifact
  ↓
deployment
  ↓
runtime population
  ↓
observations
  ↓
decision
For example:
change://payments/retry-policy/4831
        ↓
commit 7f3a91c
        ↓
artifact payments-api@sha256:...
        ↓
deployment production/payments revision 42
        ↓
canary cohort 5%
        ↓
metrics and invariant events
        ↓
rollout approved
Without this chain, a metric may be associated with the wrong version, a test may be attributed to the wrong source revision, or an incident may be unable to identify which assurance claim failed.
Treat agent activity as provenance
When an agent contributes to a change, record more than the final diff.
Useful metadata includes:
agent identity and version
model or policy version
tools invoked
repositories and files accessed
prompts or task specification
human approvals
generated artifacts
verification commands
This does not mean preserving every token forever. It means preserving enough information to answer:
What did the agent do?
What constraints did it receive?
Which tools did it use?
What did a human verify?
Agent provenance is especially important when the same agent can generate implementation, tests, documentation, and evidence. Independent validation becomes harder if the entire assurance package is produced by one opaque process.
Correctness becomes partly temporal
Some claims are stable relative to an artifact. A type checker can establish a type-system property; a proof can establish an invariant under an explicit model.
Operational claims are different.
Consider:
This migration does not materially increase checkout failures.
At merge time:
We have evidence suggesting this migration is unlikely to materially increase checkout failures under the conditions we tested.
After a successful 5% canary:
The claim is supported under bounded real traffic.
After a week across multiple traffic peaks:
The claim has substantially stronger operational support.
After an unexpected database interaction creates failures:
The claim has been falsified under a previously untested condition.
The software did not become nondeterministic. Our knowledge changed.
Canarying and DevSecOps models make this lifecycle explicit: evidence collection, deployment monitoring, operation, and feedback continue after build and release. Google SRE NIST DevSecOps reference model
Define observation windows
A claim should not move to “accepted” immediately after deployment merely because the first few minutes look healthy.
For each operational claim, define:
minimum exposure
minimum duration
minimum event volume
comparison population
success thresholds
failure thresholds
observation owner
For example:
claim: success_rate
observation:
  minimum_traffic: 100000 requests
  minimum_duration: 24h
  comparison: previous_version_same_region
  acceptable_delta: ">= -0.2%"
  owner: payments-oncall
The correct window depends on the behavior being evaluated. A payment change may need to span business peaks, settlement cycles, retries, and dependency degradation. A configuration change affecting batch processing may need to span a complete batch cycle rather than an arbitrary number of hours.
Reopen assurance when conditions change
A previously supported claim may need reevaluation when its operating conditions change.
Triggers might include:
major dependency upgrade
traffic pattern change
new region
new data scale
configuration change
infrastructure migration
security advisory
incident involving an adjacent component
monitoring coverage degradation
This does not mean rerunning every test for every environmental change. It means identifying which claims depended on the changed condition and reopening those claims selectively.
A persistent change record makes that possible. Without it, teams must reconstruct dependencies from memory and scattered history.
Risk determines how much assurance we buy
A persistent change-level model allows assurance effort to follow risk rather than line count.
Compare an agent-generated documentation change with one that modifies payment authorization and ledger mutation. Both might contain 5,000 lines, but their assurance needs differ.
A useful risk model considers:
potential consequence
×
novelty
×
blast radius
×
uncertainty
×
irreversibility
The formula is not intended to produce a scientifically precise score. It is a forcing function for discussing why a change deserves more or less assurance.
Use practical risk tiers
A simple tiering scheme is often more useful than a complex numerical model.
Tier 0: routine and reversible
Examples:
documentation
formatting
internal tooling with no production data
nonfunctional test cleanup
Typical controls:
automated verification
standard review
standard deployment
Tier 1: limited production impact
Examples:
isolated UI behavior
noncritical configuration
internal workflow changes
low-blast-radius service changes
Typical controls:
explicit intent
basic claims
automated evidence
targeted review
standard rollback
Tier 2: material operational impact
Examples:
customer-facing API behavior
database schema changes
authentication flows
performance-sensitive paths
changes affecting availability or privacy
Typical controls:
explicit claims and assumptions
architecture review
security analysis
targeted implementation inspection
automated evidence
canary or progressive rollout
runtime monitoring
documented rollback
Tier 3: high-consequence or difficult-to-reverse
Examples:
payment authorization
ledger mutation
safety-related control
identity and access boundaries
irreversible data migration
changes with regulatory consequences
Typical controls:
independent review
threat model or hazard analysis
formalized invariants where practical
independent evidence
progressive rollout
runtime enforcement
explicit residual-risk acceptance
post-deployment observation
The tiers should be calibrated to the organization’s actual consequences. A small configuration change can be Tier 3 if it controls access to sensitive data. A large generated refactor can be Tier 1 if it is isolated, well-tested, and easily reversible.
Let risk control evidence requirements
Risk classification should determine not only who reviews the change, but also what evidence is required.
For example:
risk_policy:
  tier_2:
    required:
      - claims
      - rollback_plan
      - security_scan
      - canary
      - runtime_dashboard

  tier_3:
    required:
      - claims
      - assumptions
      - independent_review
      - threat_model
      - invariant_monitor
      - progressive_rollout
      - explicit_risk_acceptance
This makes assurance policy executable. It also prevents teams from arguing about process from scratch for every change.
Make exceptions explicit
No policy will fit every situation. The answer is not to bypass the policy informally.
An exception should record:
requirement waived
reason
risk introduced
compensating control
approver
expiration date
follow-up action
This preserves organizational learning. If the same exception appears repeatedly, the policy or platform may need to change.
Human review moves toward the argument
This model does not remove humans from review. It changes what they review.
Instead of reconstructing everything from 15,000 lines of generated code, reviewers can first evaluate:
Is the intent correct?

Are the important claims explicit?

Are we missing an invariant?

Is the architecture acceptable?

Is the risk classification credible?

Does the evidence support the claims?

Which uncertainty remains?

What evidence must still come from production?
Implementation inspection then focuses on high-consequence areas such as authorization, persistence, concurrency, and financial state.
A reviewer might inspect 300 critical lines inside a 20,000-line generated implementation. That is not weaker review. It is review at a more useful semantic level.
Give reviewers a claim-to-code map
Reviewers should not have to search the entire diff to find the implementation relevant to a claim.
A useful review interface can show:
claim: no_duplicate_capture
affected code:
- retry_policy.go:44-118
- idempotency_store.go:72-161
- capture_worker.go:203-287

supporting evidence:
- concurrency-test-1842
- PSP-simulator-1844
- canary-invariant-991

known uncertainty:
- prolonged PSP partition
This allows a reviewer to move from:
claim
  ↓
argument
  ↓
evidence
  ↓
critical implementation
rather than from:
diff
  ↓
guess what matters
Require independent challenge for high-risk claims
If the same agent generates the implementation, tests, evidence summary, and assurance argument, the process may become self-confirming.
For high-risk changes, require at least one independent challenge:
different reviewer
different model or tool
different test strategy
production shadowing
formal checker
adversarial scenario generation
Independence does not guarantee correctness, but it reduces correlated blind spots.
Review uncertainty, not only confidence
A review that asks only “does this look safe?” encourages overconfident summaries.
A better review asks:
What do we know?
What do we infer?
What have we not tested?
Which assumption is most fragile?
What observation would change our decision?
This makes residual uncertainty a legitimate review output rather than an embarrassing omission.
Developer platforms become assurance infrastructure
An AI-native platform should not optimize only for generation throughput:
better coding agents
faster environments
larger contexts
more tools
parallel workers
It should also reduce the cost of establishing justified confidence:
approved architectural primitives
standard identity libraries
policy enforcement
dependency constraints
provenance
test harnesses
property checks
runtime invariants
standard observability
canary infrastructure
automatic rollback
evidence capture
change-level assurance records
Strong paved roads reduce the space of possible implementations. That matters especially for agents. If every autonomous system invents its own authentication, retry semantics, deployment strategy, telemetry, persistence, and security controls, assurance becomes expensive.
If agents generate within constrained, well-understood platforms, much of the assurance argument can be inherited.
The platform becomes an assurance substrate, not merely an implementation accelerator.
Build the platform around reusable controls
The most valuable platform features are not only code-generation features. They are reusable assurance controls:
claim templates for common change types
risk classification rules
standard rollback mechanisms
automatic canary configuration
invariant libraries
service-level dashboards
dependency and provenance capture
policy-as-code gates
evidence retention
incident-to-change linking
For example, a database migration template might automatically require:
forward migration
rollback or mitigation plan
backward compatibility check
data-volume estimate
lock-duration test
replication impact
canary or staged execution
post-migration validation
An authentication change template might require:
threat model
authorization invariants
negative test cases
audit-log verification
session invalidation behavior
runtime denial-rate monitoring
rollback procedure
Templates turn organizational knowledge into executable defaults.
Make safe behavior the easiest behavior
Agents optimize against the interfaces they are given. If the platform makes it easier to deploy an unmonitored change than to define a claim and attach a dashboard, the system will produce unmonitored changes.
The platform should therefore make the safe path the shortest path:
create change
  ↓
select risk tier
  ↓
generate claim template
  ↓
attach standard evidence
  ↓
configure rollout and rollback
  ↓
deploy with monitoring
The agent should not need to invent the assurance workflow from scratch.
Measure assurance throughput
If assurance is a production capability, it needs operational metrics.
Useful measures include:
time from change proposal to verified state
percentage of changes with explicit claims
percentage of claims with linked evidence
percentage of high-risk changes with tested rollback
time from invariant violation to rollout pause
time from incident to affected change identification
percentage of changes with post-deployment observation completed
rate of assurance exceptions
rate of claims later falsified
These metrics should not become simplistic targets.
For example, maximizing the percentage of changes with claims could encourage meaningless claims. The purpose is to identify bottlenecks and failure modes in the assurance system.
The pull request becomes a projection
The diff is not the unit of engineering consequence, so it should not be the unit of assurance.
The persistent software change is the unit of assurance:
                  ┌─ specification
                  │
                  ├─ implementation
                  │
Persistent        ├─ CI evidence
change object ────┼─ security evidence
                  │
                  ├─ deployment state
                  │
                  ├─ runtime evidence
                  │
                  └─ incidents / residual risk
Different tools expose different projections of the same change.
GitHub might show:
claims
risk
architecture delta
critical implementation
pre-merge evidence
The deployment system might show:
required production evidence
current exposure
canary comparison
rollout decision
Observability might show:
runtime invariants
claim-linked metrics
unexpected behavior
An incident system might show:
which prior assurance claim failed
which assumption was wrong
which evidence failed to predict it
That is more valuable than adding a better AI summary to a pull request.
Design interfaces around decisions
Each interface should answer the decision relevant to its users.
For reviewers:
Should this change be merged?
What claims matter?
What evidence is missing?
What code deserves attention?
For release engineers:
Should exposure increase?
Which gates remain unsatisfied?
What is the rollback trigger?
For operators:
What changed?
Which claims are being monitored?
What behavior would invalidate them?
For incident responders:
Which change introduced the behavior?
Which claim failed?
What assumption was wrong?
What evidence should have detected it?
A single giant assurance dashboard will not serve all these needs. The persistent object should be shared, but the views should be purpose-specific.
What is actually new here
Claims, evidence, assurance cases, runtime verification, canary deployments, provenance, and continuous monitoring are not new.
The proposed contribution is their combination under a different software-engineering abstraction:
Treat a consequential software change as a persistent assurance object whose claims, evidence, risk, provenance, deployment state, runtime observations, and residual uncertainty evolve throughout its lifecycle.
Historically, building this for every ordinary change would have been expensive.
AI increases the need because implementation can outrun human comprehension. It may also reduce the cost because agents can generate specifications, derive candidate invariants, classify affected boundaries, execute verification tools, collect evidence, correlate telemetry, and maintain the assurance record.
Practices associated with high-assurance engineering may therefore become economically viable further down the software stack.
Not every CRUD service needs a safety case. But a 20,000-line autonomous change should not be represented merely as:
+20,431
-1,372

CI passed.
There is a large design space between those extremes.
The practical test is whether the organization can answer, after deployment:
What was this change intended to do?
Which claims justified shipping it?
What evidence supported those claims?
What conditions did that evidence cover?
What remains uncertain?
What happened in production?
Which claim would be reopened if the environment changed?
If those answers require reconstructing history from chat messages, CI logs, dashboards, and memory, the organization does not yet have persistent change assurance.
From software production to justified confidence
AI coding is often framed as a software-production revolution. That framing is incomplete because it treats generated code as the primary object of progress.
The primary object should be the software change and the confidence we can justify in it.
If generation becomes nearly instantaneous while assurance remains proportional to human reading, organizations will not achieve proportional delivery gains. They will simply move the bottleneck.
The solution is not to make the pull request or diff carry ever more information while leaving them as the unit of assurance. The solution is to make the change persistent across the entire lifecycle and attach its claims, evidence, risk, deployment state, runtime observations, and residual uncertainty to it.
That means moving from:
write
↓
review
↓
test
↓
merge
toward:
intent
↓
claims
↓
implementation
↓
evidence
↓
bounded execution
↓
runtime evidence
↓
updated confidence
↓
continuous observation
For organizations adopting this model, a practical sequence is:
1. Assign durable IDs to consequential changes.
2. Require intent, risk, claims, and uncertainty before merge.
3. Link evidence to specific claims rather than only to commits.
4. Define rollout and observation gates for operational claims.
5. Connect runtime monitors and incidents back to the change record.
6. Use risk tiers to scale review and evidence requirements.
7. Automate the record and enforce it through delivery controls.
8. Review falsified claims and exceptions to improve the platform.
Start small. Choose one high-impact workflow—payments, authentication, data migrations, or production configuration—and implement the full loop there. Do not begin by building a universal assurance ontology. Begin by making one class of consequential change traceable from intent to runtime outcome.
The diff still exists. The pull request still exists. Tests and human inspection still matter.
But they are views and activities within the assurance process, not the assurance object itself.
The persistent software change is the unit of assurance.
In an engineering world where software can be generated faster than humans can understand it, the greatest advantage may belong not to organizations that produce the most code, but to those that can establish, update, and defend confidence in each change throughout its lifecycle.

## Resolved References (verified 2026-09-05)

1. DORA: Balancing AI tensions → https://dora.dev/insights/balancing-ai-tensions/
2. DORA: Impact of Generative AI in Software Development → https://dora.dev/ai/gen-ai-report/
3. NASA-STD-8739.8B → https://standards.nasa.gov/standard/NASA/NASA-STD-87398
4. NIST Secure Software Development Framework → https://csrc.nist.gov/pubs/sp/800/218/final
5. ISO/IEC/IEEE 15026-2:2022 → https://www.iso.org/standard/80625.html
6. OMG Structured Assurance Case Metamodel → https://www.omg.org/spec/SACM/
7. Google SRE: Canarying Releases → https://sre.google/workbook/canarying-releases/
8. Survey of Runtime Verification → https://arxiv.org/abs/1811.06740 (Sánchez et al., FMSD 2019)
9. Runtime confidence updates in safety arguments, SAC 2026 → https://arxiv.org/abs/2605.22530 (Herd et al.)
10. SLSA Provenance → https://slsa.dev/spec/v1.0/provenance
11. in-toto: Getting Started → https://in-toto.io/docs/getting-started/
12. NIST DevSecOps reference model → https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
