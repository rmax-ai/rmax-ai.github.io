# Evidence-Carrying Changes: From AI Code Production to Verifiable Software Delivery

## Abstract

AI coding systems can produce implementations, tests, migrations, and pull requests faster than many existing software-delivery processes can evaluate them. This does not establish that software engineering has become uniformly faster. It suggests that, for some classes of work, implementation capacity is increasing faster than verification, review, integration, security assurance, and operational validation capacity.

This article proposes treating every consequential code change as a claim that must arrive with structured evidence. An evidence-carrying change contains the implementation, its intended specification, functional and non-functional verification results, provenance, unresolved uncertainty, and a policy decision governing what may happen next. The design draws on software assurance cases, proof-carrying code, supply-chain attestations, mutation testing, independent verification, and policy-as-code, while stopping short of equating ordinary test results with formal proof.

The central hypothesis is that competitive advantage in AI-assisted engineering may increasingly depend less on access to code-generating models and more on an organisation's ability to specify acceptable behaviour, generate independent evidence, disclose uncertainty, and make disciplined decisions from that evidence.

---

## 1. Code is becoming cheaper; justified change is not

AI coding systems can inspect repositories, modify multiple files, run commands, repair test failures, and prepare pull requests with limited human intervention. For sufficiently bounded tasks, the marginal effort required to produce a plausible implementation has fallen sharply.

The effect on total engineering productivity is less settled.

Controlled studies, observational telemetry, surveys, and benchmark evaluations measure different things. In a randomized trial involving experienced open-source developers working on real issues in repositories they knew well, METR found that the early-2025 AI tools tested increased completion time by approximately 19 percent. The study population was narrow, the tools have since changed, and the result should not be generalized to all developers or tasks. It nevertheless shows why local code-generation speed cannot be assumed to translate into system-level delivery speed.

A 2026 mixed-methods study at BNY Mellon, based on 2,989 survey responses and 11 interviews, similarly found that developer productivity could not be represented adequately by a single activity measure. Participants described effects on expertise, ownership, quality, and long-term maintainability that commit counts or immediate task completion do not capture. The evidence is primarily self-reported and organizationally specific, but it reinforces a broader methodological point: generated output is not equivalent to delivered value.

The practical question is therefore not whether AI "improves productivity" in the abstract. It is where capacity is added, where new queues form, and which constraints become binding.

A useful delivery model is:

```
Requirements → Specification → Implementation → Verification → Review → Deployment → Operation
```

For explanatory purposes, end-to-end throughput can be approximated as being constrained by the slowest meaningful stage:

```
T_delivery ≈ min(T_spec, T_generation, T_verification, T_review, T_deployment)
```

This is not a precise empirical law. It is a constraint-oriented model. Amdahl's Law provides a related analogy: accelerating one portion of a system has diminishing effect when the remaining portions dominate total time. Queueing theory adds a second warning: when arrival rates approach or exceed a stage's service capacity, waiting time can increase non-linearly. If an agent produces three times as many proposed changes but verification and review capacity remain unchanged, the result may be a larger review queue rather than three times as much production value. More generated code can also create more integration paths, more dependency interactions, and more states requiring operational validation.

The hypothesis is not that implementation has ceased to matter. It is that verification and integration are increasingly likely to become binding constraints where code generation accelerates more rapidly than the surrounding delivery system.

## 2. Code as a claim

A proposed code change is not merely a collection of modified files. It is an assertion about a system.

It claims that:

* the system should behave differently;
* the implementation satisfies an intended requirement;
* existing behaviour remains acceptably preserved;
* the change complies with architectural and organisational constraints;
* the change is sufficiently safe to deploy;
* failures, if they occur, can be observed and handled.

Let:

```
C = claim introduced by a proposed change
```

The delivery system evaluates that claim using evidence:

```
E = E_f + E_s + E_a + E_o + E_p + E_h
```

where:

* E_f: functional evidence;
* E_s: security evidence;
* E_a: architectural evidence;
* E_o: operational evidence;
* E_p: provenance evidence;
* E_h: human-judgement evidence.

The crucial distinction is:

```
Evidence exists ≠ The artifact is correct
```

Instead, evidence changes confidence:

```
P(acceptable change | E)
```

This probability need not be computed numerically. The expression makes the epistemic relationship explicit: a test report, scan, approval, or attestation changes what can reasonably be believed about a change, but none establishes universal correctness.

The strength of that belief depends on more than the number of checks. Relevant properties include:

* Coverage: Which behaviours and failure modes were exercised?
* Oracle strength: Would the check distinguish correct from incorrect behaviour?
* Independence: Could the implementation and verifier share the same misunderstanding?
* Reproducibility: Can another system recreate the result?
* Relevance: Does the evidence address the actual claim?
* Freshness: Was it produced against the exact artifact and environment under review?
* Provenance: Who or what produced it, using which tools and inputs?
* Resistance to gaming: Can an implementation pass the check without satisfying the underlying intent?
* Residual uncertainty: What remains unknown?

This framing resembles an assurance case more than a conventional CI status page. Goal Structuring Notation, for example, represents relationships between claims, supporting arguments, contextual assumptions, and evidence. A diagram does not itself prove safety; it exposes how the argument is constructed and where it depends on incomplete or contested evidence.

It also resembles proof-carrying code in a limited conceptual sense. In proof-carrying code, an untrusted producer supplies code together with a machine-checkable proof that it satisfies a defined safety policy. An ordinary evidence package is much weaker: tests, scans, and review approvals are not mathematical proofs. The transferable design principle is that the producer should carry the burden of supplying verifiable support for its claims rather than asking the consumer to reconstruct that support from scratch.

## 3. What counts as software evidence

Evidence is useful only relative to a claim. "All tests passed" is weak evidence when the requirement is ambiguous, the tests cover only the happy path, or the test oracle reproduces the same mistaken assumption as the implementation.

An evidence-carrying change should therefore distinguish evidence classes rather than collapse everything into one green status.

### 3.1 Functional evidence

Functional evidence addresses whether the implementation behaves according to its specification.

Examples include:
* unit tests;
* integration tests;
* end-to-end tests;
* property-based tests;
* differential testing;
* regression tests;
* mutation testing;
* formal specifications;
* model checking or theorem proving where justified.

Different techniques expose different defect classes.

Unit tests can isolate local behaviour but often miss interactions. End-to-end tests exercise realistic paths but may be slow, flaky, and difficult to diagnose. Property-based testing explores families of inputs rather than individual examples, but its value depends on whether the stated properties capture meaningful correctness. Differential testing compares implementations or versions and is useful when a reliable reference exists.

Mutation testing evaluates the test suite rather than the implementation directly. It introduces controlled faults—such as changing a comparison operator or deleting a branch—and asks whether the tests detect them. A high mutation score does not guarantee correctness, but a low score indicates that many plausible faults can survive the suite.

Formal methods can establish stronger claims within explicit assumptions, but their cost and applicability vary. A proof can still certify the wrong specification. Evidence strength therefore depends on both the verification method and the validity of the property being verified.

### 3.2 Security evidence

Security evidence addresses bounded classes of vulnerability and policy violation.

Examples include:

* static application security testing;
* taint analysis;
* dependency and supply-chain scanning;
* secret detection;
* privilege checks;
* policy checks;
* adversarial inputs;
* sandbox execution;
* dynamic security testing;
* authorization-path analysis.

A clean scan is evidence of non-detection under a particular tool, configuration, rule set, and code path. It is not proof that vulnerabilities are absent.

NIST's Secure Software Development Framework treats secure development as a set of practices integrated throughout the software lifecycle rather than a final scan attached to a release. It deliberately describes outcomes and practices at a high level rather than prescribing a single toolchain.

Security evidence should record tool versions, rule configurations, suppressions, scan coverage, and unresolved findings. Otherwise, "security passed" communicates almost nothing about what was actually evaluated.

### 3.3 Architectural evidence

Architectural evidence establishes whether the change conforms to system structure and repository-specific constraints.

Examples include:

* dependency-direction rules;
* forbidden imports;
* module boundaries;
* layering constraints;
* API compatibility;
* schema compatibility;
* performance budgets;
* repository conventions;
* data residency constraints;
* approved integration patterns.

This category matters because a functionally correct local change can still be systemically unacceptable. It may couple domains that were intentionally isolated, bypass an authorization layer, introduce a new dependency class, or violate an operational ownership boundary.

Executable constraints are often more dependable than lengthy procedural prompts. A prompt can tell an agent not to import a storage client into a domain module. A conformance test can make the violation unmergeable.

Recent agent-development experiments provide preliminary support for this distinction. In [TDAD](https://arxiv.org/abs/2603.17973), an AST-derived code–test graph was used to surface likely affected tests to coding agents. In the reported SWE-bench Verified experiments with two local models, this structural context reduced measured regressions relative to the authors' baseline, whereas procedural test-driven-development prompting alone performed worse. The evaluation was limited to particular models, subsets, and a benchmark environment; it is evidence for a promising mechanism, not a universal law.

### 3.4 Operational evidence

Pre-merge correctness is not production correctness.

Operational evidence addresses behaviour under deployment and runtime conditions:
* load and stress tests;
* canary results;
* rollback verification;
* observability coverage;
* alert validation;
* service-level-objective impact;
* production anomaly detection;
* fault injection;
* capacity margins;
* compatibility with real traffic and data distributions.

Many important properties are observable only after integration or deployment. Provider timeouts may differ from simulations. Data cardinality may invalidate local performance assumptions. A retry mechanism may pass integration tests but amplify load during an outage.

An evidence-carrying change should therefore support evidence that matures over time. Before merge, it may contain simulated fault-injection results. After canary deployment, the same change record can be extended with production latency, error rate, and rollback evidence.

The status is not permanently "passed." Confidence evolves as evidence is produced, expires, or becomes invalid because the artifact or environment changes.

### 3.5 Provenance evidence

Provenance establishes where an artifact and its supporting evidence came from.

Examples include:

* source revision;
* model and harness version;
* human principal;
* agent or workload identity;
* tool-call trace;
* referenced sources;
* dependency versions;
* environment hash;
* artifact hash;
* authorization decisions;
* build identity;
* evidence timestamps.

Supply-chain systems already provide useful primitives. [SLSA](https://slsa.dev/provenance) defines provenance as verifiable information describing where, when, and how an artifact was produced. Its stronger requirements separate trusted provenance generation from user-controlled build steps so that the artifact producer cannot freely falsify the attestation.

[in-toto](https://in-toto.io/) records what software-supply-chain steps were performed, by whom, and in what order. [Sigstore](https://www.sigstore.dev/) provides mechanisms for signing and transparency. These systems do not establish semantic correctness, but they make evidence attributable and tamper-evident.

The same principle should apply to AI-generated changes. A text field claiming that tests passed is weak provenance. A signed attestation bound to an artifact hash, runner identity, test command, environment, and output is substantially stronger.

### 3.6 Human-judgement evidence

Some claims cannot be reduced reliably to deterministic checks.

Human judgement may still be required for:

* product acceptance;
* domain interpretation;
* legal and regulatory analysis;
* architecture trade-offs;
* user-experience quality;
* ethical impact;
* risk acceptance;
* interpretation of ambiguous requirements.

Human approval should not be treated as an undifferentiated checkbox. The record should state what the reviewer evaluated, the information available, unresolved objections, and the scope of the approval.

A domain expert approving payment retry semantics is not necessarily approving the dependency graph. A security reviewer approving privilege boundaries is not validating product behaviour. Evidence packages should preserve these distinctions.

## 4. Evidence quality: coverage, oracles, independence, and provenance

Evidence volume is easy to optimize and easy to game. Evidence quality is harder.

A harness could generate hundreds of tests that execute lines without asserting meaningful properties. It could run multiple scanners with overlapping rule sets and present the result as independent confirmation. It could ask five agents based on the same model to review the same patch and count five approvals.

The relevant question is not "How much evidence was produced?" It is "How strongly does this evidence discriminate between an acceptable and unacceptable change?"

Four properties deserve particular emphasis.

### Coverage

Coverage asks whether the evidence addresses the important parts of the claim.

Code coverage can reveal unexecuted paths but cannot determine whether executed paths were evaluated correctly. Requirement coverage is often more valuable: which acceptance criteria, invariants, threat scenarios, and operational assumptions have corresponding evidence? A change claiming idempotent payment retries requires more than coverage of the retry function. It may require evidence about duplicate requests, process restarts, provider timeouts, concurrent workers, stale idempotency records, and database transaction boundaries.

### Oracle strength

An oracle decides whether observed behaviour is acceptable.

Weak oracles are common in generated tests. They may assert that a function returns a value without checking its semantics, snapshot an incorrect output, or merely verify that execution does not throw.

Mutation testing is useful because it measures whether the suite notices plausible faults. Hidden behavioural tests add another layer: the implementation and its visible tests cannot tailor themselves directly to every evaluation case.

A 2026 test-driven agent-definition study combined visible and hidden tests with semantic mutation testing. Across 24 trials on four deeply specified agents, the authors reported strong hidden-test and mutation results for the initial specifications, but lower compilation success when the specifications evolved. The study is small, uses purpose-built specifications, and concerns agent prompts rather than general software; its broader contribution is methodological. Visible tests alone can overstate compliance, and verifier quality should itself be evaluated.

### Independence

Evidence is stronger when its failure modes are not tightly correlated with the implementation process.

Independence is not binary. It exists on a spectrum:

1. Same model, same context, same agent.
2. Same model, separate role, with parts of the implementation context withheld.
3. Different model family or independently constructed verifier.
4. Deterministic or externally grounded verification.

The fourth arrangement is generally strongest for properties that can be encoded deterministically. A compiler, type checker, policy engine, database constraint, or reproducible benchmark does not share a language model's conversational interpretation in the same way another agent might.

But deterministic tools can still share a flawed specification or incomplete rule set. Independence reduces some correlated failures; it does not remove specification risk.

Research on N-version programming provides a useful warning. Diverse implementations can improve fault tolerance only when their failures are sufficiently independent. Experiments have found correlated failures even among separately developed implementations because difficult inputs and shared specifications create common fault patterns.

The same issue applies to multi-agent verification. Different agent names, roles, or system prompts do not guarantee meaningful diversity if all use the same base model, examples, repository summary, and mistaken requirement.

### Provenance

Evidence without provenance is difficult to evaluate or reproduce.

A report should bind each result to:

* the exact source and artifact revisions;
* the command or procedure executed;
* the environment;
* the tool and rule versions;
* the producing identity;
* the timestamp;
* the raw output;
* any transformations used to summarize it.

The summary should be treated as a view over primary evidence, not the evidence itself.

## 5. Why self-generated tests can provide false confidence

Consider a requirement:

> Expired sessions must be rejected after 30 minutes of inactivity.

An agent interprets this as "30 minutes after creation," implements an absolute lifetime check, and generates tests using the same interpretation. All tests pass.

The implementation, tests, and explanation are internally consistent. They are also wrong.

This is a correlated-failure problem:

1. The model misunderstands the requirement.
2. It generates an implementation from that misunderstanding.
3. It generates tests encoding the same misunderstanding.
4. The tests pass.
5. The system reports high confidence.

Self-generated tests still have value. They can catch implementation mistakes relative to the model's interpretation, exercise edge cases, and improve local regression protection. What they cannot do by themselves is validate the interpretation from which both code and tests were derived.

A stronger arrangement separates specification, implementation, and evaluation:

* Human- or policy-owned acceptance criteria are established first.
* Some behavioural tests remain hidden from the implementation agent.
* Deterministic constraints evaluate architectural and security properties.
* A verifier is given the requirement and resulting behaviour, but not the implementation agent's rationale.
* Mutation testing measures whether the suite detects plausible defects.
* Residual uncertainty records properties that cannot yet be tested.

Different model families may increase diversity, but model diversity should be measured rather than assumed. The verifier's effectiveness can be evaluated using seeded defects, historical incidents, adversarial cases, and false-acceptance rates.

The goal is not maximal disagreement between agents. It is useful independence from the change generator's blind spots.

## 6. Risk-calibrated evidence requirements

Uniform verification is inefficient.

Requiring formal review, adversarial testing, signed attestations, and staged deployment for a documentation typo would create process without proportional risk reduction. Allowing a payment-authorization change to merge after linting and self-generated unit tests would be reckless.

Evidence requirements should increase with risk:

```
R = f(expected_harm, reversibility, blast_radius, data_sensitivity, privilege, customer_proximity, regulatory_impact, novelty, observability)
```

This function need not initially be numerical. A rule-based classifier may be more transparent and easier to audit.

### Tier 1: Low-risk and reversible

Examples:
* local scripts;
* internal prototypes;
* documentation;
* isolated developer tooling;
* non-production examples.

Possible requirements:
* basic execution;
* formatting and linting;
* targeted tests;
* artifact and actor provenance;
* explicit declaration of affected files.

Autonomous merge may be acceptable where changes are readily reversible and isolated.

### Tier 2: Operational or customer-facing

Examples:
* production SaaS features;
* API changes;
* dependency upgrades;
* service configuration;
* user-facing workflows.

Possible requirements:
* unit and integration tests;
* architecture checks;
* security and dependency scanning;
* mutation threshold for critical logic;
* rollback evidence;
* human review;
* provenance attestations.

A policy engine may permit deployment only after human approval.

### Tier 3: High-impact or regulated

Examples:
* payment logic;
* identity and authorization;
* database migrations;
* personal-data processing;
* compliance controls;
* irreversible state transitions.

Possible requirements:
* independent verification;
* hidden behavioural tests;
* adversarial testing;
* formal approval by named roles;
* signed attestations;
* policy-engine enforcement;
* staged deployment;
* runtime monitoring;
* explicit rollback or compensating actions;
* separation of duties.

These tiers are a proposed engineering model, not an empirically validated universal standard. Organizations should calibrate them using incident history, regulatory obligations, architecture, and operational maturity.

The policy decision should be deterministic where practical. [Open Policy Agent](https://openpolicyagent.org/docs), for example, evaluates declarative policies against structured input and can be integrated into CI/CD pipelines. An LLM may classify ambiguous evidence or identify gaps, but it should not be the sole authority deciding whether its own output satisfies the release policy.

## 7. The evidence-carrying change format

An evidence-carrying change can be represented as a machine-readable artifact:

```yaml
claim:
  intent: "Add idempotent payment retry handling"
  specification_version: "payments-spec@8b71ac"
  changed_artifacts:
    - src/payments/retry.ts
    - tests/payments/retry.test.ts

evidence:
  functional:
    unit_tests: passed
    integration_tests: passed
    mutation_score: 0.83

  architectural:
    dependency_policy: passed
    forbidden_imports: passed

  security:
    static_analysis: passed
    secret_scan: passed

  operational:
    load_test_report: artifacts/retry-load.json
    rollback_verified: true

  provenance:
    model: "<model name and version>"
    harness_version: "0.1.0"
    human_principal: "user://..."
    agent_identity: "agent://..."
    environment_hash: "sha256:..."
    artifact_hash: "sha256:..."

residual_uncertainty:
  - "Provider timeout behaviour is simulated"
  - "No production traffic evidence is available yet"

decision:
  risk_tier: 2
  policy_result: "REQUIRE_HUMAN_APPROVAL"
```

The residual_uncertainty field is not an optional disclaimer. It is part of the core data model.

A binary pass/fail interface encourages epistemic compression. It hides the difference between "the property was verified," "the tool did not detect a violation," "the property was simulated," and "the property was not evaluated."

Residual uncertainty should be structured where possible:

```yaml
residual_uncertainty:
  - claim: "Retries remain safe under provider-side partial failure"
    reason: "Provider sandbox cannot reproduce partial commit behaviour"
    impact: "Possible duplicate external charge"
    mitigation: "Canary limited to internal merchant accounts"
    owner: "payments-platform"
    expires_after: "production canary"
```

This turns uncertainty into something that can be owned, monitored, and resolved.

## 8. Architecture of an evidence-carrying change harness

```
Task or issue
      ↓
Specification extraction
      ↓
Risk classification
      ↓
Implementation agent
      ↓
Independent evidence producers
 ┌────────────┬──────────┬──────────────┬────────────┐
 │ Functional │ Security │ Architecture │ Operations │
 └────────────┴──────────┴──────────────┴────────────┘
      ↓
Evidence aggregator
      ↓
Adversarial verifier
      ↓
Policy decision
      ↓
Autonomous action, human review, or rejection
```

### Specification extractor

The extractor converts a task into explicit claims, acceptance criteria, invariants, non-goals, and unresolved questions.

It should distinguish source material from inferred requirements. An agent-generated assumption must not silently become an authoritative acceptance criterion.

The output might include:
* required behaviours;
* preserved behaviours;
* prohibited behaviours;
* relevant interfaces;
* operational constraints;
* security properties;
* evidence obligations.

### Risk classifier

The classifier determines the provisional risk tier.

Some signals can be deterministic:
* files under identity or payment modules;
* schema or migration changes;
* privilege modifications;
* customer-facing APIs;
* personal-data access;
* irreversible actions.

An LLM can assist with semantic interpretation, but the final tier should be explainable and subject to policy rules. Uncertain classification should move upward in risk rather than silently default downward.

### Implementation worker

The worker produces the proposed change.

It receives the specification and repository context, but it should not control all evidence production. It may generate candidate tests and explanations, which remain producer-supplied evidence rather than independent validation.

### Deterministic verification tools

These include:
* compiler and type checker;
* linters;
* unit and integration runners;
* dependency analyzers;
* mutation testing;
* static security analysis;
* architecture tests;
* API and schema compatibility checks;
* reproducible build checks.

Tool outputs should be retained as primary artifacts and normalized into the evidence schema.

### Independent model-based verifier

The verifier challenges the proposed change rather than improving it. Its inputs may include the specification, diff, selected repository context, test results, and historical incidents. It should search for:

* untested requirements;
* specification ambiguity;
* incorrect assumptions;
* missing failure modes;
* inconsistent evidence;
* suspiciously weak assertions;
* paths through which the implementation can satisfy tests while violating intent.

Its findings are advisory unless converted into deterministic policy conditions or accepted by an accountable reviewer.

### Evidence normalizer and aggregator

Evidence producers will emit incompatible formats. The normalizer maps them into a common schema containing:

* claim addressed;
* producer;
* method;
* result;
* artifact binding;
* timestamp;
* raw evidence location;
* limitations;
* confidence;
* expiry conditions.

The aggregator should not average heterogeneous evidence into an unexplained score. A 92-percent "confidence" label can conceal more than it communicates. The interface should expose the argument connecting claims to evidence.

### Provenance recorder

The recorder binds:
* source revision;
* artifact hashes;
* model and harness versions;
* tool invocations;
* identities;
* environment;
* evidence outputs;
* policy decisions.

It should adopt established attestation formats where possible rather than inventing incompatible signing and provenance mechanisms.

### Policy engine

The policy engine evaluates structured evidence against risk-dependent requirements.

Example:

```
IF risk_tier == 3
AND independent_verification != passed
THEN decision = REJECT

IF risk_tier >= 2
AND rollback_verified != true
THEN decision = REQUIRE_REMEDIATION

IF residual_uncertainty contains "possible irreversible loss"
THEN decision = REQUIRE_NAMED_RISK_OWNER
```

Possible outcomes include:
* autonomous action;
* human approval required;
* additional evidence required;
* rejected;
* deployment restricted to a canary;
* accepted with monitored uncertainty.

### Human approval interface

The interface should show:
* the claims introduced;
* evidence supporting each claim;
* contradictory or missing evidence;
* provenance;
* risk tier;
* residual uncertainty;
* the exact decision requested from the reviewer.

A polished summary should never replace access to the underlying diff, logs, reports, and assumptions.

## 9. Human review, skill, and organizational design

AI-assisted development changes the human role from pure solution generation toward a mixture of generation, supervision, diagnosis, and evaluation.

That transition creates several risks.

### Automation bias

Reviewers may over-trust a system because it appears systematic. A detailed evidence report, signed attestation, or green dashboard can increase confidence even when the underlying oracle is weak.

The harness must therefore expose evidence limitations as prominently as successful checks.

### Instant-gratification bias

Generated solutions reduce the delay between a question and a plausible answer. This can encourage early commitment before the problem has been understood adequately.

A small mixed-methods study of 14 observed developers and a follow-up survey of 22 participants identified multiple cognitive biases in LLM-assisted programming, including instant gratification and preference for the model's suggestion. The reported action-level percentages should be interpreted cautiously because of the small, exploratory sample and qualitative coding process. The stronger conclusion is that AI-assisted programming introduces identifiable supervisory biases that tool design should address.

### Fixation and surface plausibility

The first generated design can anchor subsequent reasoning. Review then becomes a search for obvious defects rather than an independent evaluation of alternatives.

Evidence independence helps by forcing at least one verifier to reason from the claim rather than from the implementation's rationale.

### Reviewer fatigue

Increasing the volume or size of generated changes without improving evidence can overwhelm reviewers. Fatigued reviewers are more likely to rely on summaries, familiar patterns, or CI status.

The correct response is not necessarily more human review. It is better allocation of human attention: deterministic checks for machine-verifiable properties, independent evidence for likely correlated failures, and human judgement for ambiguous or consequential decisions.

### Cognitive offloading and skill decay

When implementation is delegated, engineers may lose some of the mental model normally acquired by constructing the solution.

Aviation automation is a useful but limited analogy. Research on flight-deck automation has examined how reduced manual practice can degrade certain cognitive and manual skills. Software engineering is not aviation, and the operational stakes and tasks differ substantially. The transferable concern is that supervisors may become less able to detect rare failures when routine execution is delegated.

Organizations may need deliberate practices for maintaining system knowledge:
* manual investigation of selected incidents;
* design reconstruction exercises;
* rotation through verification and operations;
* review of rejected agent changes;
* explicit testing of engineers' system models;
* pairing human reviewers with evidence gaps rather than only successful outputs.

The goal is not to preserve manual coding for its own sake. It is to preserve the capacity to understand, challenge, and recover from automated decisions.

## 10. Metrics for validated engineering progress

AI-assisted engineering should not be evaluated primarily by:

* lines of code;
* commits;
* pull-request volume;
* suggestion acceptance;
* story points;
* agent tokens;
* tasks attempted.

These metrics may measure activity while rewarding larger changes, fragmented commits, superficial task decomposition, or unnecessary generation.

More useful metrics include:

* lead time to validated production value;
* escaped defect rate;
* change failure rate;
* review time;
* evidence-generation cost;
* mutation score;
* false-acceptance rate;
* false-rejection rate;
* rollback success;
* percentage of claims with adequate provenance;
* percentage of material uncertainty disclosed;
* reviewer confidence calibration;
* evidence freshness;
* evidence reuse rate.

No single metric is sufficient.

Mutation score can be gamed by writing tests around easy mutants. Low escaped-defect rates may reflect conservative release policies that suppress useful change. Reviewer time can fall because reviews become superficial. Evidence reuse can improve efficiency or propagate stale assumptions.

Metrics should therefore be treated as a balanced measurement system. Goodhart's Law applies: when a measure becomes a target, pressure grows to optimize the measure rather than the underlying outcome.

The most important organizational unit may be the validated change, not the generated patch.

## 11. Limits of the evidence

The empirical literature on modern coding agents is young, fast-moving, and difficult to compare.

First, tool capability changes rapidly. Results produced using early-2025 models may not describe 2026 systems. The METR slowdown study is rigorous within its setting but concerns experienced contributors working on mature repositories they already understood. It does not estimate effects for greenfield development, less experienced developers, or newer tools.

Second, benchmarks and production environments differ. SWE-bench-style evaluations offer reproducibility but cannot capture all integration, operational, security, and organizational costs. METR separately found that some apparently correct benchmark solutions required additional work because of formatting, test coverage, or code-quality issues, illustrating how automatic scoring can omit practical acceptance criteria.

Third, observational studies face attribution problems. A 2026 study of explicitly identified AI-authored commits found many static-analysis issues and tracked a portion persisting in later repository revisions. However, it captures only commits with explicit AI metadata, depends on static analyzers' definitions, and does not establish how equivalent human-authored changes would have performed under matched conditions. The revised dataset also differs slightly from the first preprint version, which is another reason not to overstate individual percentages.

Fourth, vendor telemetry is informative but usually not randomized. Teams that adopt AI heavily may differ in maturity, task mix, review culture, and tooling. Correlations between AI usage and pull-request activity do not establish causal effects on delivered value.

Fifth, evidence-carrying changes remain an architectural proposal. Supply-chain attestations, assurance cases, mutation testing, policy engines, and independent verification are established ideas, but their combination into an AI coding harness has not yet been validated across organizations.

Open questions include:
* Which evidence classes reduce escaped defects most cost-effectively?
* How much verifier diversity is required to reduce correlated failures?
* Can evidence requirements be calibrated without creating excessive process?
* How should confidence be represented without misleading numerical precision?
* When should evidence expire?
* How should runtime evidence update pre-merge assurance?
* Can reviewers accurately calibrate confidence from evidence reports?
* Does an evidence package reduce review effort, or merely move effort into evidence interpretation?
* How often do agents learn to satisfy the verifier without satisfying intent?
* Which residual uncertainties are routinely omitted?

Evidence-first engineering can increase confidence. It cannot prove total correctness, eliminate human responsibility, or make an invalid specification valid.

## 12. Companion experiment and open-source implementation

### Evidence-Carrying Changes: A Verification Harness for AI-Generated Software

The companion project is an intentionally narrow verification harness built to test the central hypothesis:

> Do evidence-carrying changes reduce reviewer effort and escaped defects compared with conventional agent-generated pull requests?

The initial implementation is available in the [rmax-ai/evidence-first-harness](https://github.com/rmax-ai/evidence-first-harness) repository.

The experiment should compare four conditions:
1. Human implementation with conventional CI.
2. Agent implementation with conventional CI.
3. Agent implementation with self-generated tests.
4. Agent implementation with independently produced evidence.

The evaluation should measure:
* task completion rate;
* escaped defects;
* mutation score;
* reviewer time;
* reviewer confidence;
* confidence calibration;
* false acceptance;
* false rejection;
* evidence-generation cost;
* total lead time;
* model cost;
* change failure rate.

The first version should remain deliberately constrained:
* one language ecosystem;
* one test framework;
* static analysis;
* type checking;
* mutation testing;
* a machine-readable evidence.json;
* an HTML evidence report;
* GitHub pull-request integration;
* two or three risk tiers.

It should explicitly exclude:
* generic enterprise workflow orchestration;
* distributed schedulers;
* complex policy administration;
* broad multi-language support;
* Kubernetes;
* Temporal;
* production deployment automation;
* autonomous merging of high-risk changes.

The research design should seed known defects and specification ambiguities so that false acceptance can be measured. Reviewers should be blinded where practical to the experimental condition. Reviewer confidence should be collected before and after viewing the evidence package to test whether the package improves calibration or merely increases confidence.

The project's purpose is not to demonstrate a polished autonomous engineering platform. It is to determine whether structured, independently generated evidence changes measurable software-delivery outcomes.

## 13. Conclusion

The declining cost of producing plausible code does not remove the need for specification, verification, review, integration, security assurance, or operational judgement. It changes their relative importance.

A code-generating agent should not hand a reviewer only a patch and a statement that tests pass. It should produce an evidence-carrying change: a structured claim about intended behaviour, the implementation, evidence from multiple relevant and sufficiently independent sources, provenance, residual uncertainty, and a deterministic policy result describing what may happen next.

This architecture does not guarantee correctness. Tests can encode the wrong specification. Scanners can miss vulnerabilities. Independent agents can share correlated blind spots. Human reviewers can over-trust polished reports. Production can invalidate pre-deployment assumptions.

The value of the evidence-carrying approach is therefore not certainty. It is disciplined uncertainty management.

The article's central hypothesis is that competitive advantage in AI-assisted engineering may increasingly lie not in privileged access to code-generating models, which are becoming broadly available, but in an organisation's capacity to specify acceptable behaviour, generate independent evidence, expose what remains unknown, and make disciplined decisions from that evidence.

That hypothesis is supported by established assurance principles and emerging evidence about AI-assisted development, but it remains to be tested directly. The next step is not another demonstration of how much code an agent can produce. It is a controlled evaluation of how reliably an engineering system can justify the changes it proposes.

---

## Five key claims and confidence assessment

### 1. Increasing implementation capacity does not necessarily increase end-to-end software-delivery throughput proportionally.

Confidence: High.

This follows from well-established constrained-system reasoning and is consistent with empirical findings showing that local task speed, perceived productivity, review work, and delivered value can diverge. The exact bottleneck differs by organization and task.

### 2. Self-generated tests can create correlated false confidence when implementation and tests share the same mistaken requirement interpretation.

Confidence: High as a logical failure mode; Moderate regarding prevalence.

The mechanism is straightforward and consistent with established common-mode failure research. Its frequency in production AI-assisted development has not been measured adequately.

### 3. Independent and deterministic evidence is generally stronger than additional evaluations produced from the same model, context, and specification.

Confidence: Moderate.

The claim is supported by software diversity, testing, formal verification, and assurance principles. The optimal combination of model diversity and deterministic verification for coding agents remains unresolved.

### 4. Risk-calibrated evidence requirements are preferable to uniform verification requirements.

Confidence: Moderate.

Risk-based assurance is established in security and regulated engineering. The specific three-tier model proposed here is an engineering hypothesis rather than a validated standard.

### 5. Evidence-carrying changes can reduce reviewer effort and escaped defects.

Confidence: Speculative.

This is the companion project's primary research hypothesis. Existing work supports several component mechanisms, but the integrated outcome requires controlled evaluation.

---

## Proposed architecture-diagram caption

An evidence-first software-delivery harness separates implementation from evidence production, aggregates functional, security, architectural, operational, and provenance evidence, exposes residual uncertainty, and applies a risk-calibrated policy before autonomous action or human approval.

---

## Claims removed or softened during fact-checking

1. Removed: "AI code generation costs approach zero."
   Reason: Generation still incurs model, infrastructure, context preparation, integration, and supervision costs. The rate of decline also differs by task.

2. Softened: "The bottleneck has shifted from coding to verification."
   Revised: Verification and integration are increasingly likely to become binding constraints in environments where implementation capacity grows faster than surrounding delivery capacity.
   Reason: Bottlenecks remain organization- and task-dependent.

3. Removed: "AI-generated code is less secure than human-written code."
   Reason: Existing benchmark, vendor, and observational results do not establish a universal matched comparison across real development settings.

4. Softened: "Larger models do not improve code security."
   Revised: Some evaluated reports have not found a reliable security improvement from model scale under their tested tasks and models.
   Reason: Results depend on benchmark design, model families, prompting, and vulnerability categories.

5. Removed: "Evidence-first systems achieve very high throughput while retaining safety."
   Reason: No verified production study was found establishing this as a general result.

6. Softened: "AI tools make developers slower."
   Revised: One randomized trial found an approximately 19-percent slowdown for experienced open-source developers using early-2025 tools on realistic tasks in repositories they knew well.
   Reason: The result has a specific population, tool generation, and task setting.

7. Removed: "Multiple agents provide independent verification."
   Reason: Agents sharing a model, context, training distribution, or specification may have strongly correlated failure modes.

8. Softened: "Mutation score measures test quality."
   Revised: Mutation score measures whether a suite detects a defined set of synthetic faults and can expose weak oracles.
   Reason: It does not measure all dimensions of test-suite quality or application correctness.

9. Removed: "A signed provenance record proves the code is trustworthy."
   Reason: Attestation establishes attributable production history and integrity, not semantic correctness.

10. Softened: "Evidence-first engineering prevents automation bias."
    Revised: Evidence-first interfaces can reduce some information gaps but may also produce automation bias when summaries appear more authoritative than the underlying evidence warrants.
    Reason: Presentation quality can amplify unjustified confidence.

---

## References

1. Sabry E. Farrag, ["The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development"](https://arxiv.org/abs/2605.01160), 2026.

2. Valerie Chen et al., ["Beyond the Commit: Developer Perspectives on Productivity with AI Coding Assistants"](https://arxiv.org/abs/2602.03593), 2026.

3. METR, ["Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity"](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), 2025.

4. METR, ["Research Update: Towards Reconciling Slowdown with Time-Horizon Evaluations"](https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/), 2025.

5. Stanford Software Engineering Productivity Research, [research programme](https://softwareengineeringproductivity.stanford.edu/).

6. Yue Liu et al., ["Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild"](https://arxiv.org/abs/2603.28592), 2026.

7. Xinyi Zhou et al., ["Cognitive Biases in LLM-Assisted Software Development"](https://arxiv.org/abs/2601.08045), 2026.

8. Pepe Alonso, ["TDAD: Test-Driven Agentic Development—Reducing Code Regressions in AI Coding Agents via Graph-Based Impact Analysis"](https://arxiv.org/abs/2603.17973), 2026.

9. Tzafrir Rehan, ["Test-Driven AI Agent Definition: Compiling Tool-Using Agents from Behavioral Specifications"](https://arxiv.org/abs/2603.08806), 2026.

10. George C. Necula, ["Proof-Carrying Code"](https://dl.acm.org/doi/10.1145/263699.263712), POPL, 1997.

11. S. S. Brilliant, J. C. Knight, and N. G. Leveson, ["Analysis of Faults in an N-Version Software Experiment"](https://ntrs.nasa.gov/citations/19900041359), IEEE Transactions on Software Engineering, 1990.

12. Assurance Case Working Group, [Goal Structuring Notation Community Standard](https://scsc.uk/gsn).

13. NIST, [Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf).

14. NIST, [SP 800-218: Secure Software Development Framework Version 1.1](https://csrc.nist.gov/pubs/sp/800/218/final), 2022.

15. SLSA, [Provenance specification](https://slsa.dev/provenance).

16. in-toto, [Software supply-chain integrity framework](https://in-toto.io/).

17. Sigstore, [Software signing and transparency project](https://www.sigstore.dev/).

18. Open Policy Agent, [official documentation](https://openpolicyagent.org/docs).

19. Open Policy Agent, [Using OPA in CI/CD Pipelines](https://openpolicyagent.org/docs/cicd).

20. SPIFFE and SPIRE, [workload-identity documentation](https://spiffe.io/docs/latest/spire-about/).

21. GitHub, [Spec Kit](https://github.com/github/spec-kit).

22. NIST, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework).

23. OWASP, [Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

24. rmax-ai, [Evidence-First Harness companion project](https://github.com/rmax-ai/evidence-first-harness).
