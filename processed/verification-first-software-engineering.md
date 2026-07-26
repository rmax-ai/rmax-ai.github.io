---
title: "Verification-First Software Engineering: Durable Specifications and Regenerable Code"
description: "As AI coding agents reduce implementation cost, executable specifications, verification systems, policies, and operational constraints become the durable assets of software engineering."
date: 2026-07-26
---

# Verification-First Software Engineering: Durable Specifications and Regenerable Code

> As implementation becomes cheaper, the durable engineering asset shifts from a particular codebase toward the system that defines and verifies acceptable behavior.

## Introduction

Large language models are changing the economics of software engineering.

Coding agents can inspect repositories, generate patches, execute commands, run tests, diagnose failures, and revise their own work. Research from [METR on task-completion time horizons](https://metr.org/time-horizons/) suggests that frontier systems are becoming capable of completing progressively longer software-engineering tasks, although success remains highly dependent on the task, environment, model, and evaluation method.

This changes an assumption that has shaped software engineering for decades.

Historically, source code was expensive to create and modify. Teams therefore treated the implementation itself as the primary engineering asset: preserve the codebase, minimize rewrites, and evolve it carefully over many years.

As agents reduce the cost of producing candidate implementations, the constraint begins to move.

The scarce resource is increasingly not the ability to generate code. It is the ability to determine whether generated code is correct enough, secure enough, operationally acceptable, and consistent with the system's intended behavior.

This suggests a different way to organize software development.

Rather than treating source code as the only authoritative artifact, we can treat it as one implementation constrained by a more durable verification system: executable specifications, contracts, invariants, policies, operational budgets, provenance, and regression knowledge.

I refer to this approach as **verification-first software engineering**.

The claim is not that source code becomes disposable everywhere. It is that, for well-specified classes of systems, implementations can become increasingly replaceable while the assets used to generate, evaluate, and govern them become more durable.

---

## The bottleneck is moving

Modern coding agents are already capable of substantial implementation work. Depending on the repository and available tools, they can:

- implement APIs;
- refactor modules;
- migrate frameworks;
- repair failing tests;
- update dependencies;
- generate infrastructure definitions;
- write documentation;
- and iterate across build and test failures.

The difficult question is no longer merely:

> Can the agent produce a plausible implementation?

It is:

> What evidence justifies accepting that implementation?

An experienced engineer must still determine:

- whether important edge cases were preserved;
- whether the change introduces security regressions;
- whether it violates architectural constraints;
- whether performance remains within acceptable bounds;
- whether the agent weakened or bypassed the tests;
- whether dependencies and build inputs are trustworthy;
- whether the resulting system remains operable;
- and whether the implementation satisfies the actual requirement rather than only its most visible examples.

Implementation is becoming relatively cheap.

Acceptance is not.

This is an instance of constraint migration. Increasing throughput in one stage does not automatically increase throughput in the whole delivery system. When code generation accelerates faster than review, verification, integration, and operational validation, the downstream stages become the limiting factors.

The practical unit of progress is therefore not generated code. It is **accepted change supported by credible evidence**.

---

## Software repositories contain two kinds of assets

Traditional repositories mix two fundamentally different kinds of information.

The first describes how the current implementation works.

The second describes what must remain true regardless of implementation.

These assets have different lifetimes.

Implementation artifacts include:

- source files;
- framework wiring;
- dependency-injection configuration;
- internal abstractions;
- helper functions;
- generated code;
- build scripts;
- and deployment-specific adapters.

These may change substantially during a rewrite or migration.

More durable artifacts include:

- API contracts;
- behavioral specifications;
- domain invariants;
- formal models;
- property-based tests;
- regression suites;
- authorization policies;
- performance budgets;
- service-level objectives;
- architecture decisions;
- dependency rules;
- and software-supply-chain attestations.

These artifacts define acceptable behavior and constraints with less dependence on one implementation.

The distinction is useful:

> Code describes how the system currently behaves.  
> Specifications and constraints describe what acceptable implementations must preserve.

This separation is not absolute. Tests can encode accidental implementation details. Architecture decisions can become obsolete. Operational targets may change. Specifications can be incomplete or internally inconsistent.

The objective is therefore not to pretend that specifications are timeless. It is to make the intended behavior, constraints, and evidence explicit enough that they can survive implementation changes and be revised independently.

---

## The specification bundle

A verification-first repository can organize its durable assets into a **specification bundle**.

The bundle does not need to be one file or one formal language. It is the versioned collection of artifacts required to generate and assess an implementation.

A practical specification bundle may contain six layers.

### 1. Interface contracts

Interface contracts define observable interactions without prescribing internal structure.

Examples include:

- [OpenAPI descriptions](https://spec.openapis.org/) for HTTP APIs;
- GraphQL schemas;
- Protocol Buffers or other interface-definition languages;
- event schemas;
- database contracts;
- command-line interface definitions;
- and compatibility requirements.

The [OpenAPI Specification](https://spec.openapis.org/oas/v3.2.0.html), for example, defines a language-independent description of an HTTP API that can be consumed without reading the service's source code.

A contract describes the shape of an interaction. It does not, by itself, establish that the implementation is semantically correct, secure, or operationally sound.

### 2. Behavioral examples

Example-based tests capture known scenarios:

- public unit tests;
- integration tests;
- end-to-end workflows;
- historical regression cases;
- and reproductions of previously observed failures.

These examples are concrete and easy to understand, but they cover only the cases selected by the test author.

### 3. General properties and invariants

Properties describe behavior across classes of inputs rather than individual examples.

The original [QuickCheck paper](https://dl.acm.org/doi/10.1145/351240.351266) introduced automated checking of program properties over generated inputs. Property-based testing is particularly useful when a system should preserve algebraic laws, state-machine rules, round-trip behavior, ordering constraints, or domain invariants.

Examples include:

- decoding an encoded value returns the original value;
- account balances never become negative;
- authorization cannot be gained by changing request order;
- retries do not duplicate externally visible effects;
- and sorting preserves the input multiset.

Properties improve coverage, but their usefulness depends on the quality of the property, generators, state model, and oracle.

### 4. Policy constraints

Policies define what an implementation is permitted to do.

Examples include:

- authorization rules;
- allowed dependencies;
- network-access restrictions;
- deployment requirements;
- data-residency constraints;
- resource limits;
- and approval requirements.

[Open Policy Agent](https://www.openpolicyagent.org/) provides one implementation of policy as code: policy decisions can be represented separately from application logic and evaluated against structured inputs.

Security requirements should also include process and supply-chain controls. The [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final) defines high-level practices for integrating security into the software-development lifecycle. The [SLSA provenance specification](https://slsa.dev/spec/v1.0/provenance) defines attestations connecting software artifacts to the build process that produced them.

### 5. Operational constraints

Functional correctness is insufficient if regenerated software is too slow, too expensive, unobservable, or unreliable.

Operational constraints may include:

- latency percentiles;
- memory and CPU budgets;
- throughput targets;
- availability objectives;
- error budgets;
- startup-time limits;
- logging and tracing requirements;
- rollback requirements;
- and compatibility with production infrastructure.

These measurements are often environment-dependent and noisy. They should therefore specify test conditions, acceptable variance, and statistical thresholds rather than pretending to be perfectly deterministic.

### 6. Design and provenance records

Some constraints cannot be expressed completely as executable tests.

Architecture decision records, threat models, data-lineage descriptions, dependency manifests, signed build attestations, and human approvals preserve the rationale and origin of a change.

These artifacts help reviewers answer not only whether a candidate passed, but also:

- what produced it;
- which inputs and tools were used;
- which assumptions governed the decision;
- which evidence remains incomplete;
- and who accepted the residual risk.

Together, these layers form an implementation-independent description of acceptable software—imperfect, evolving, but more durable than any single generated codebase.

---

## Verification is more than testing

Verification-first engineering should not be reduced to "write more unit tests."

A test suite is one evidence source among several.

Different verification mechanisms reveal different failure classes:

- example tests detect known incorrect behavior;
- property-based tests search broader input spaces;
- static analysis detects selected structural defects;
- type systems exclude classes of invalid programs;
- model checking explores state-transition systems;
- mutation testing assesses whether tests detect injected changes;
- fuzzing searches malformed or unexpected inputs;
- security scanners identify known vulnerability patterns;
- policy engines enforce organizational constraints;
- performance tests measure operational behavior;
- provenance attestations record how artifacts were produced;
- and human review evaluates ambiguity, intent, and consequences that automated oracles do not capture.

For systems with complex concurrency or distributed behavior, formal specifications can expose design errors before implementation. Leslie Lamport describes [TLA+](https://lamport.azurewebsites.net/tla/tla.html) as a language for modeling programs and systems, especially concurrent and distributed systems; its tools are intended to identify fundamental design errors that are difficult to discover in code.

The central principle is heterogeneous evidence.

No single verifier provides complete assurance. Confidence comes from combining partially independent mechanisms whose failure modes do not fully overlap.

---

## Why passing tests is not enough

Passing a visible test suite does not prove correctness.

An implementation can satisfy every example while remaining defective outside the tested region. It can also satisfy the letter of the test while violating the intent behind it.

This problem becomes more important when the implementation process can inspect and modify its own verification environment.

An agent may:

- overfit visible examples;
- exploit weak assertions;
- hard-code expected values;
- delete or weaken failing tests;
- bypass intended code paths;
- introduce unnecessary complexity;
- preserve outputs while violating authorization boundaries;
- degrade performance outside the measured workload;
- or change an architectural assumption not represented in the test suite.

This resembles benchmark overfitting in machine learning: success on an observed evaluation does not necessarily imply robust performance on the underlying task.

Verification assets should therefore be designed with adversarial pressure in mind.

Useful techniques include:

- hidden tests unavailable during generation;
- independent validation in a clean environment;
- checks preventing unauthorized test modification;
- property-based and metamorphic tests;
- mutation testing;
- differential testing against a reference implementation;
- static and dynamic security analysis;
- production-like performance tests;
- explicit dependency and permission policies;
- and review by an evaluator that did not generate the implementation.

Mutation testing is especially relevant because it evaluates the sensitivity of the test suite. It introduces controlled changes into the program and checks whether the tests detect them. Research has found evidence that mutation testing can expose gaps related to real faults, although equivalent mutants, computational cost, and operator quality remain practical limitations.

The goal is not to construct one enormous test suite. It is to build an evidence portfolio with diverse and partially independent failure-detection mechanisms.

---

## Separate generation from acceptance

A central architectural principle is to separate software generation from software acceptance.

The generator may be probabilistic. The acceptance process should be independently specified, reproducible where possible, resistant to modification by the generator, and explicit about residual uncertainty.

```text
Specification Bundle
        │
        ▼
Generation Harness
        │
Candidate Implementation
        │
        ▼
Independent Verification Pipeline
        │
        ├── Contract checks
        ├── Public and hidden tests
        ├── Properties and invariants
        ├── Static and dynamic analysis
        ├── Security and policy checks
        ├── Performance and reliability checks
        ├── Provenance validation
        └── Human review where required
        │
        ▼
Evidence Package
        │
        ▼
Acceptance Policy
        │
        ├── Accept
        ├── Reject
        └── Escalate
```

This separation creates several useful controls.

First, the agent should not have unrestricted authority to rewrite the criteria used to judge its work.

Second, verification should run in a clean environment with controlled dependencies and inputs.

Third, the pipeline should produce an evidence package rather than a binary "tests passed" signal.

That package may include:

- test and analysis results;
- coverage and mutation reports;
- benchmark distributions;
- build provenance;
- changed permissions and dependencies;
- traces and logs;
- known verification gaps;
- waived failures;
- reviewer decisions;
- and residual risks.

Fourth, acceptance policy should vary by risk. A disposable internal script, a financial ledger, and medical-device software should not require the same evidence.

The implementation is not accepted because the model claims success. It is accepted because the organization's acceptance policy determines that the available evidence is sufficient for the intended use.

This still does not prove total correctness. It converts an opaque claim into a reviewable engineering decision.

---

## The compiler analogy—and where it stops

Compilers offer a useful but limited analogy.

Compilers allowed developers to express programs at a higher level while automating translation into machine code. They made generated lower-level artifacts routine and reproducible.

Verification-first engineering similarly raises the abstraction boundary. Engineers increasingly express contracts, invariants, constraints, and policies while agents generate candidate implementations.

But the analogy stops at an important point.

A compiler translates a comparatively precise source language according to defined semantics. Natural-language requirements, behavioral examples, architectural policies, and operational goals are usually incomplete, ambiguous, or conflicting. A coding agent is therefore not a compiler for specifications in the strict sense.

The more accurate model is:

> A coding agent proposes an implementation from an incomplete specification; the verification system determines whether the proposal is acceptable under the evidence available.

This framing avoids mistaking generation for proof.

---

## Regenerability is a spectrum

Verification-first engineering does not imply that all software should be regenerated from scratch.

Regenerability depends on how completely the system's behavior, constraints, state, and operating environment have been captured.

A system is more regenerable when:

- its interfaces are explicit;
- its domain rules are encoded as invariants;
- its persistent data semantics are documented;
- its regression suite represents important historical failures;
- its dependencies and permissions are constrained;
- its operational envelope is measurable;
- its build is reproducible;
- and its acceptance process is independent from its implementation.

Good early candidates may include:

- stateless internal APIs;
- command-line tools;
- data-transformation pipelines;
- protocol adapters;
- service migrations;
- deterministic batch jobs;
- infrastructure automation;
- and reference implementations of well-defined standards.

Harder candidates include:

- legacy systems containing undocumented operational knowledge;
- interactive products whose quality depends heavily on subjective user experience;
- systems with complex external side effects;
- systems whose behavior depends on mutable third-party services;
- highly optimized systems with hardware-specific behavior;
- and safety-critical software requiring regulatory, process, and formal assurance beyond automated testing.

The objective is not universal disposable software.

It is to identify the boundary at which an implementation becomes replaceable because the durable constraints around it are sufficiently complete and strong.

---

## What makes a specification durable?

A specification is durable not because it is written in a formal notation, but because it continues to capture the properties that matter as implementations change.

Durable verification assets tend to have several qualities.

### They describe externally meaningful behavior

A test that asserts the name of a private helper function is fragile. A property that asserts idempotent payment processing is durable.

### They separate intent from implementation

A contract should specify required behavior without unnecessarily fixing framework structure, internal class names, or storage mechanisms.

### They include failure behavior

Specifications should cover timeouts, retries, invalid inputs, partial failure, concurrency, degraded dependencies, and recovery—not only the happy path.

### They preserve discovered knowledge

Every production incident, security defect, and compatibility failure can become a regression artifact, invariant, policy, or operational check.

### They are versioned and reviewable

A specification change can alter system behavior as significantly as a source-code change. It should therefore receive explicit review, provenance, and compatibility analysis.

### They resist self-modification

The generator should not be able to weaken its own acceptance criteria without producing a visible, separately reviewed specification change.

### They expose uncertainty

The bundle should record unverified properties, environmental assumptions, flaky measurements, unsupported platforms, and accepted risks.

A durable specification is not merely a frozen contract. It is accumulated organizational knowledge expressed in a form that can constrain future implementations.

---

## A practical experiment: the Regenerable Software Lab

The hypothesis is empirical.

Rather than debating whether software will become disposable, we can measure how reliably current coding agents regenerate implementations from fixed specifications.

This is the motivation behind the **Regenerable Software Lab**.

The experiment fixes the specification bundle while allowing implementations, models, and harnesses to vary.

Each coding agent receives the same inputs:

- API or protocol contracts;
- behavioral specifications;
- public examples;
- domain invariants;
- dependency and permission policies;
- build requirements;
- and performance budgets.

The agent generates a fresh implementation in an isolated environment.

The candidate is then evaluated against progressively stronger verification profiles.

### Profile A: visible examples

- public unit tests;
- basic build checks;
- and formatting or linting.

This measures whether the agent can satisfy an observed specification.

### Profile B: independent behavioral validation

- hidden tests;
- integration tests;
- and differential tests against a reference implementation.

This measures generalization beyond visible examples.

### Profile C: property and fault sensitivity

- property-based tests;
- state-machine tests;
- fuzzing;
- and mutation testing.

This measures whether the implementation and test suite survive broader or adversarial variation.

### Profile D: policy and supply-chain constraints

- dependency allowlists;
- permission checks;
- secret scanning;
- static security analysis;
- reproducible-build checks;
- and provenance validation.

This measures whether the implementation is acceptable beyond functional behavior.

### Profile E: operational validation

- latency and throughput distributions;
- memory and CPU use;
- failure recovery;
- observability checks;
- and behavior under degraded dependencies.

This measures whether the implementation is viable in its intended environment.

The benchmark should report more than a pass rate.

Useful metrics include:

- acceptance rate by verification profile;
- hidden-test generalization gap;
- mutation score;
- policy-violation rate;
- performance-budget compliance;
- security findings;
- regeneration variance across repeated runs;
- human review time;
- verification cost;
- implementation complexity;
- and the proportion of failures caused by incomplete specifications rather than weak generation.

This supports more useful research questions:

- Which verification assets contribute most to robust regeneration?
- How much do hidden evaluations reduce specification overfitting?
- Which properties are difficult to express but critical in practice?
- How much reliability comes from the model, the harness, and the specification bundle?
- At what point does strengthening verification cost more than maintaining the existing implementation?
- How stable are regenerated implementations across repeated runs?
- Which domains remain resistant to regeneration because essential knowledge is tacit or subjective?
- How often does the experiment reveal defects in the specification itself?

These are systems-engineering questions, not merely model-comparison questions.

This article describes an architectural direction rather than a finished methodology. As a proof of concept, we are developing the [Regenerable Software Lab](http://regenerable-software-lab.rmax.tech), an open research project that explores verification-first software engineering in practice. Rather than treating source code as the primary long-lived artifact, the project investigates workflows where durable specifications, executable verification, evaluation harnesses, and operational constraints define software behavior, while implementations can be regenerated, revalidated, and replaced as models and tooling improve. The project serves as an experimental platform for evaluating these ideas, benchmarking regenerability, and exploring practical techniques for building AI-native software engineering systems.

---

## Verification becomes the durable asset

Software engineering has repeatedly moved its abstraction boundaries.

Assembly gave way to higher-level languages.

Manual translation gave way to compilers.

Hand-managed integration and deployment gave way to automated build and delivery pipelines.

AI coding agents may move the boundary again.

Implementation becomes increasingly automated.

Verification, specification, and governance become increasingly valuable.

This does not make source code irrelevant. Production systems still run code, engineers still debug it, and many implementations contain performance, safety, or domain knowledge not captured elsewhere.

The shift is in relative durability.

A particular implementation may become easier to replace. The accumulated system that defines acceptable behavior becomes harder—and more valuable—to recreate.

That durable system includes:

- executable specifications;
- regression knowledge;
- domain invariants;
- formal models where justified;
- security and authorization policies;
- operational budgets;
- architecture decisions;
- provenance requirements;
- and risk-based acceptance rules.

Organizations that invest in these assets can benefit from improving models without rebuilding their engineering process around every new coding agent.

They can also compare implementations on a common basis, change models or vendors, regenerate selected components, and preserve institutional knowledge independently of one codebase.

As implementation becomes cheaper, engineering moves toward a more explicit discipline of defining, verifying, and governing what software is allowed to become.

The future repository may contain code.

The durable product is the evidence system that makes the code trustworthy enough to use.

---

## References

### AI coding agents and evaluation

- Model Evaluation & Threat Research, ["Task-Completion Time Horizons of Frontier AI Models"](https://metr.org/time-horizons/).
- Anthropic, ["Demystifying Evals for AI Agents"](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).
- Anthropic, ["Effective Harnesses for Long-Running Agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
- Anthropic, ["Harness Design for Long-Running Application Development"](https://www.anthropic.com/engineering/harness-design-long-running-apps).
- Factory, ["Agent Native Development"](https://factory.ai/news/build-with-agents).

### Specifications and formal methods

- OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/).
- Leslie Lamport, [TLA+](https://lamport.azurewebsites.net/tla/tla.html).
- Leslie Lamport, [*Specifying Systems*](https://lamport.azurewebsites.net/tla/book.html).
- Koen Claessen and John Hughes, ["QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs"](https://dl.acm.org/doi/10.1145/351240.351266).

### Verification and testing

- Kent Beck, [*Test-Driven Development: By Example*](https://www.pearson.com/en-us/subject-catalog/p/test-driven-development-by-example/P200000009421).
- A. Jefferson Offutt and Roland H. Untch, ["Mutation 2000: Uniting the Orthogonal"](https://www.albany.edu/faculty/offutt/research/papers/mut00.pdf).
- Goran Petrović, Marko Ivanković, Gordon Fraser, and René Just, ["Does Mutation Testing Improve Testing Practices?"](https://arxiv.org/abs/2103.07189).

### Policy, security, and provenance

- Open Policy Agent, [Documentation](https://www.openpolicyagent.org/docs/).
- National Institute of Standards and Technology, [*Secure Software Development Framework (SSDF), SP 800-218*](https://csrc.nist.gov/pubs/sp/800/218/final).
- SLSA, [Provenance Specification](https://slsa.dev/spec/v1.0/provenance).

> "Program testing can be used to show the presence of bugs, but never to show their absence."  
> — Edsger W. Dijkstra
