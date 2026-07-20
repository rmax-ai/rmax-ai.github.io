# The Harness Gap: Measuring Model–Harness Fit in Coding Agents

When an AI coding agent fails, the model usually receives the blame.

The common response is to switch to a larger model, increase the reasoning budget, or wait for the next model release. This assumes that agent performance is primarily a property of the underlying neural network.

But a coding agent is not simply a model answering a prompt. It is a model operating inside an execution system that determines what information it sees, which actions it can take, how tool results are represented, when it should retry, and what evidence it must produce before declaring success.

That surrounding system is the agent harness.

Research on agent–computer interfaces, tool design, context management, and automated harness optimization increasingly suggests that changing the harness can materially change the performance of an otherwise fixed model. Yet the evidence is not conclusive. Some optimized harnesses fail to generalize, exploit characteristics of their evaluation environment, or outperform simpler baselines only because they consume more inference compute.

This leaves three distinct questions:

1. How much does the harness affect agent performance?
2. Can systematic optimization discover better harnesses under a fixed budget?
3. Do different models require different harnesses?

The first question is increasingly supported by evidence. The second remains an active research problem. The third—the hypothesis of **model–harness fit**—requires a more careful experimental design than ordinary model benchmarking.

## The model is only one part of the agent

A production coding agent combines at least two systems.

The first is the model: the learned neural network responsible for interpreting information, reasoning about the task, and proposing actions.

The second is the deterministic execution environment around it:

* System instructions and repository context
* Tool names, descriptions, and schemas
* File-search and navigation interfaces
* Planning and task-decomposition policies
* Context selection and compaction
* Retry and failure-recovery logic
* Test, lint, and type-checking commands
* Completion and evidence requirements
* Cost, latency, permission, and safety controls

The model supplies probabilistic reasoning. The harness controls how that reasoning interacts with the software environment.

This distinction becomes increasingly important as AI systems move from single-turn generation toward long-running work. Anthropic describes part of this transition as a shift from prompt engineering toward [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): the problem is no longer only how to phrase an instruction, but how to decide which information, tool definitions, previous actions, intermediate results, and environmental feedback belong in the model's active context.

The harness makes that decision repeatedly throughout an agent trajectory.

For a coding task, the model may infer the likely cause of a bug. But the harness determines whether it can efficiently inspect the relevant files, search for symbol usage, modify code, execute tests, interpret compiler errors, recover from a failed patch, and verify that the final change satisfies the original request.

A capable model operating through a poor harness resembles an experienced engineer working through an unreliable terminal with incomplete logs, ambiguous commands, and no trustworthy test environment. The underlying competence remains, but much of it becomes operationally inaccessible.

## Interface design changes effective capability

One of the clearest demonstrations of the harness effect came from the [SWE-agent](https://arxiv.org/abs/2405.15793) project.
Rather than exposing a repository through a generic shell interface alone, the researchers designed an Agent–Computer Interface around the strengths and limitations of language models. The interface shaped how the model navigated repositories, viewed files, edited code, and executed commands.

The important finding was not merely the benchmark score. It was that interface design changed the model's effective ability to act on a software repository. The same underlying model could behave differently depending on how the environment presented files, commands, observations, and editing operations.

The result established a broader principle:

> Model capability and agent capability are not the same thing.

Anthropic has reported similar observations in its work on [designing tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents). Tool names, parameter descriptions, response formats, error messages, namespaces, and the amount of information returned can all influence whether an agent selects and uses a tool correctly.

A tool designed for a human developer may not be a good tool for a language model. Humans can often resolve ambiguous names, scan long terminal output, remember earlier failures, and infer undocumented conventions. Models are more sensitive to how those details are represented inside a limited context window.

Tool design is therefore part of capability engineering, not merely API ergonomics.

A useful development process is iterative:


Build the interface
        ↓
Run representative evaluations
        ↓
Inspect traces and failures
        ↓
Modify tools or context policy
        ↓
Evaluate on held-out tasks


This is already a basic form of harness optimization. The object being improved is not the model's weights, but the deterministic boundary through which the model perceives and changes the world.

## From prompt optimization to harness optimization

Prompt optimization searches for better instructions, examples, or demonstrations while keeping the surrounding program mostly fixed.

Harness optimization expands the search space to include the execution program itself.

A harness configuration might specify:


Context:
    Generate a compact repository map
    Load only likely relevant files
    Summarize long command output

Planning:
    Require an explicit plan before editing

Tools:
    Use strict argument schemas
    Return diagnostic error information

Validation:
    Run focused tests after meaningful edits
    Run the complete required suite before completion

Recovery:
    Retry with a structured failure summary
    Start a fresh context after repeated failure

Completion:
    Require test evidence
    Report changed files and residual risks


Another harness might use no explicit planning, generic tools, raw terminal output, continuous conversational history, and validation only at the end.

Both harnesses can run the same model on the same task while producing different trajectories, costs, and outcomes.

The 2026 paper [Meta-Harness: End-to-End Optimization of Model Harnesses](https://arxiv.org/abs/2603.28052) extends this idea by searching over executable harness code. Its proposer can inspect previous harness implementations, execution traces, scores, and results before generating a new candidate.

The paper reports improvements across classification, mathematical reasoning, and coding tasks while keeping the solver models fixed. It also reports that a harness discovered for mathematical reasoning improved average accuracy across several held-out models, suggesting that some harness improvements may capture reusable execution principles rather than model-specific tricks.

Conceptually, this moves optimization from model parameters into the surrounding system:


Start with harness H₀
        ↓
Run evaluation tasks
        ↓
Inspect failures and traces
        ↓
Modify one or more harness components
        ↓
Measure correctness, cost, and latency
        ↓
Retain credible improvements
        ↓
Repeat
The resulting harness is not universally optimal. It is a configuration preferred under a particular model, workload, budget, search process, and evaluation procedure.

## Three separate harness hypotheses

It is useful to distinguish three claims that are often grouped together.

### 1. The harness-effect hypothesis

Changing the harness changes the performance of a fixed model.

Evidence from SWE-agent, tool-interface research, context engineering, and long-running agent systems provides substantial support for this claim. Interfaces influence what information reaches the model, which actions are available, and how effectively errors become corrective feedback.

### 2. The harness-optimization hypothesis

A systematic search process can discover a better harness than a reasonable manually designed baseline.

This claim is more demanding. It requires showing that the optimizer discovers structural improvements rather than merely spending more tokens, retries, model calls, or benchmark feedback.

### 3. The model–harness-fit hypothesis

Different models have materially different optimal harness configurations.

This is the strongest and least established claim.

Models differ in pretraining data, post-training methods, tool-use formats, context behaviour, instruction sensitivity, and tendencies around planning or self-correction. They may consequently respond differently to:

* Concise versus detailed instructions
* Explicit versus implicit planning
* Narrow versus broad tool collections
* JSON, XML, Markdown, or plain-text results
* Raw versus summarized command output
* Continued versus fresh-context retries
* Frequent versus final-only validation
* Strict versus permissive output schemas

A configuration that helps one model could be unnecessary or actively harmful for another. Detailed instructions may stabilize one model while constraining another. A fresh-context retry might remove accumulated noise for one model while discarding valuable state for another.

The existence of a harness effect does not automatically prove model-specific fit. Harness improvements may instead be universal, task-specific, repository-specific, or primarily a consequence of additional compute.

That distinction requires cross-model evaluation.

## Defining the harness gap

Let:

* (M_i) be a model;
* (H_0) be a common baseline harness;
* (H_i^*) be a harness optimized for model (M_i);
* (D) be a held-out task distribution;
* (U(M,H,D)) be the measured utility of model (M) using harness (H).

Utility should include more than task success:

[
U =
\text{success}
-\lambda_c\text{cost}
-\lambda_l\text{latency}
-\lambda_s\text{instability}
]

The first useful quantity is the optimization gap:

[
\Delta_{\text{optimization}}(M_i)
=================================

U(M_i,H_i^*,D) - U(M_i,H_0,D)
]

This measures how much a model improves when moving from the common harness to its optimized harness.

But it does not establish model specificity. An optimized harness might work equally well for every model.

The second quantity is therefore the matching gap:

[
\Delta_{\text{matching}}(M_i)
=============================

## U(M_i,H_i^*,D)

\max_{j \neq i} U(M_i,H_j^*,D)
]

This measures whether the harness optimized for (M_i) outperforms harnesses optimized for other models.

A third useful quantity is cross-model transfer:

[
T_{i \rightarrow j}
===================

U(M_j,H_i^*,D) - U(M_j,H_0,D)
]

This measures whether a harness optimized for model (M_i) improves or degrades model (M_j) relative to the common baseline.

Together, these measurements distinguish general harness quality from model-specific coupling.

## Measuring model–harness fit

A credible experiment needs three stages.

### Stage 1: Common-harness baseline

Several models execute the same held-out tasks using one reasonable generic harness.

This resembles an ordinary model comparison:


Model A + generic harness
Model B + generic harness
Model C + generic harness
The results show how the models perform under a common interface. They do not establish intrinsic model quality, because the shared harness may align better with one model's learned interaction patterns.

A model leaderboard is therefore always partly a model–interface leaderboard.

### Stage 2: Independent harness optimization

The same bounded harness search space is optimized independently for each model.

The optimization process may alter context presentation, planning policy, tool descriptions, validation timing, retry behaviour, or completion requirements. The model, task dataset, execution environment, and total resource ceilings remain controlled.

This produces one fitted harness per model:


H*A = harness optimized for Model A
H*B = harness optimized for Model B
H*C = harness optimized for Model C


Comparing each fitted harness with the generic baseline measures the optimization gap.

### Stage 3: Cross-model transfer

Every optimized harness is then evaluated with every model.

| Harness | Model A | Model B | Model C |
| ------- | ------: | ------: | ------: |
| Generic |       — |       — |       — |
| A-fit   |       — |       — |       — |
| B-fit   |       — |       — |       — |
| C-fit   |       — |       — |       — |

This transfer matrix can reveal several different outcomes.

Universal harness

One configuration performs well across all models. The dominant improvements are general principles of agent design.

Model-family harness

Configurations transfer well among related models but less effectively outside the family.

Model-specific harness

Each model performs materially better with its own fitted configuration.

Task-specific harness

Harness choice depends primarily on task category rather than model identity.

No meaningful harness advantage

Observed differences disappear under matched budgets, repeated trials, or held-out evaluation.

A good experiment must remain capable of producing any of these findings. It should test model–harness coupling rather than assume it.

## Why harness optimization can produce false gains

Automatic harness optimization is vulnerable to the same broad problem as model training: overfitting.

A search process may repeatedly evaluate candidate harnesses on the same tasks until it discovers a workflow that exploits benchmark-specific patterns. It may tune around verifier quirks, repository conventions, public tests, or accidental information leakage without learning a generally useful execution strategy.

There are several distinct forms of overfitting.

Task overfitting

The harness adapts to particular benchmark instances rather than the broader task distribution.

Repository overfitting

The harness exploits one repository's structure, naming conventions, test layout, or development workflow.

Model overfitting

The harness improves one model but transfers poorly to other models. This may be the intended object of study, but it must be distinguished from general progress.

Optimizer overfitting

Repeated candidate evaluation selects configurations that benefited from random variation rather than genuine improvement.

Compute is another major confounder.

An evolved harness may appear better simply because it uses more model calls, retries, tokens, test executions, or environmental feedback than the baseline. A complex recovery strategy that makes five attempts should not be compared only with one zero-shot attempt.

The recent paper [Rethinking the Evaluation of Harness Evolution for Agents](https://arxiv.org/abs/2607.12227) directly examines this problem. Under comparable feedback and inference budgets, the authors found that automatic harness evolution did not consistently outperform simpler test-time scaling strategies and showed limited generalization to held-out tasks and models.

This does not establish that harness optimization is useless. It establishes a stricter comparison standard.

The relevant comparison is not:

> Optimized harness versus one baseline attempt.

It is:
> Optimized harness versus simpler search and retry strategies using comparable information and total compute.

## Fair evaluation requires two separate budgets

Harness experiments should distinguish the execution budget from the optimization budget.

The execution budget determines how much resource a harness may consume while solving one task:

* Maximum model calls
* Maximum input and output tokens
* Maximum tool calls
* Maximum retries
* Maximum test executions
* Maximum wall-clock runtime
* Maximum context size

The optimization budget determines how much resource may be spent searching for a harness:

* Number of candidate configurations
* Number of tasks used per candidate
* Number of repeated trials
* Number of optimizer iterations
* Total model and execution cost

Both budgets should be reported.

A candidate harness may optimize how a fixed execution budget is allocated. For example, it might replace one long context with two shorter attempts, or reserve validation calls for high-risk edits. It should not silently receive a larger total budget than the baseline.

## What a credible evaluation should include

A rigorous model–harness-fit experiment needs:

* Separate optimization, validation, and held-out task sets
* At least one completely held-out repository
* Fixed tool permissions and execution environments
* Matched token, model-call, and tool-call budgets
* Simple repeated-sampling and sequential-refinement baselines
* Multiple trials for stochastic configurations
* Paired comparisons on identical tasks
* Confidence intervals and minimum effect-size thresholds
* Storage of rejected as well as accepted harness candidates
* Hidden tests outside the agent's writable environment
* Controls against test deletion or validation weakening
* Controls against access to future commits or benchmark solutions
* Cost and latency reporting alongside success
* Ablations showing which harness changes produced the gain

These controls matter because harness optimization is a search process. If many candidates are evaluated and only the best score is reported, ordinary evaluation noise can look like architectural progress.

## HarnessFit as a proof of concept

[HarnessFit](https://github.com/rmax-ai/harness-fit) is a small open-source proof of concept for studying this problem.

The project is intended to compare several coding models under a common harness, search a constrained set of harness variations independently for each model, and then evaluate the resulting configurations through a cross-model transfer matrix.

The goal is not to build a universal agent framework or an unconstrained system that rewrites its own orchestration code.

It is to create a controlled environment for asking a narrower question:

> When models receive the same tasks, tools, validation signals, and total resource budget, do they benefit from different execution configurations?

The proof of concept focuses on observable harness dimensions such as context presentation, planning policy, tool-result representation, validation timing, recovery strategy, and completion requirements.

Its value lies less in discovering one high-scoring harness than in making the experiment falsifiable. A useful result could show strong model-specific coupling, broad transfer of one universal harness, task-dependent configurations, or no meaningful advantage over simpler retry strategies.

## The practical consequence for engineering teams

If the harness gap survives controlled evaluation, it changes how organizations should compare and deploy coding models.

A public model benchmark measures performance inside someone else's scaffold. It may not predict performance inside an organization's repositories, tools, policies, context systems, and validation environment.

Teams should therefore evaluate complete agent systems:


Model
+ Context strategy
+ Tool interface
+ Execution policy
+ Recovery behaviour
+ Validation gates
+ Cost controls
This does not make model capability irrelevant. Better models can expand the range of tasks an agent can solve and reduce the scaffolding required for some workflows.

But model selection alone is incomplete.

A smaller or cheaper model operating through a well-matched harness may outperform a stronger model inside a poorly matched environment on a specific workload. Conversely, a harness tuned aggressively around a weaker model may become unnecessary or counterproductive when the model changes.

Model upgrades should therefore be treated as system changes. Teams should rerun agent evaluations, inspect traces, and reconsider tool descriptions, context policies, retry logic, and validation rules rather than assuming that the existing harness will remain optimal.

## Where engineering leverage accumulates

As code generation becomes cheaper, engineering leverage increasingly shifts toward the deterministic environment around generation:

* Executable acceptance criteria
* Fast and reproducible test suites
* Architectural constraints
* Static analysis and custom linting
* Safe, well-described tool interfaces
* Repository maps and context retrieval
* Trace collection and failure analysis
* Evaluation datasets
* Cost-aware model routing
* Evidence-based completion gates

This resembles control-system design more than conventional prompt writing.

The engineer does not prescribe every implementation step. They shape the observations available to the model, the actions it may take, the feedback it receives, the constraints it must respect, and the conditions under which execution stops.

The output is not one carefully written response. It is an environment in which many possible solutions can be proposed, tested, rejected, and improved.

## A falsifiable question

The strongest reason to study model–harness fit is not that the thesis has already been proven.

It is that the thesis has become plausible and experimentally testable.

We have evidence that agent–computer interfaces matter, tool design changes model behaviour, context management influences long-running execution, and executable harnesses can be optimized. We also have evidence that harness-evolution results can shrink under matched compute budgets and fail to generalize beyond the search environment.

A serious experiment must sit directly inside that disagreement.

The model-specific harness hypothesis would be weakened if:

* one harness consistently performs best across models;
* task category predicts the optimum better than model identity;
* gains disappear on held-out repositories;
* repeated sampling matches optimized harnesses under equal budgets;
* fitted configurations are unstable across repeated runs;
* most improvements come from additional compute rather than execution structure.

It would receive support if matched model–harness pairs produce repeatable gains across held-out tasks while using equivalent resources—and if those gains diminish when the same harness is transferred to other models.

The future of coding agents may not be determined solely by which organization trains the strongest model. It may also depend on whether we can build environments that expose each model's capabilities reliably, efficiently, and safely.

The important question is no longer only:

> Which model is best?

It is:

> Which combination of model, interface, context, execution policy, and validation system works best for this workload—and does the result continue to hold when the benchmark changes?

---

## References

1. Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K. and Press, O. [SWE-agent: Agent–Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793). *Advances in Neural Information Processing Systems*, 2024.

2. Anthropic. [Writing Effective Tools for Agents—With Agents](https://www.anthropic.com/engineering/writing-tools-for-agents). Anthropic Engineering, 2025.
3. Anthropic. [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Anthropic Engineering, 2025.

4. Anthropic. [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents). Anthropic Engineering, 2025.

5. Lee, Y., Nair, R., Zhang, Q., Lee, K., Khattab, O. and Finn, C. [Meta-Harness: End-to-End Optimization of Model Harnesses](https://arxiv.org/abs/2603.28052). arXiv, 2026.

6. Wang, Y., Zhu, H., Hu, Z., Yuan, Y., Chen, Z., Senthil, S., Hajishirzi, H., Tsvetkov, Y., Dasigi, P. and Xiao, T. [Rethinking the Evaluation of Harness Evolution for Agents](https://arxiv.org/abs/2607.12227). arXiv, 2026.

7. Nie, J., Zhang, Y., Song, J., Cai, Q., Yu, D., Guo, Y., Tian, X. and Han, B. [TTHE: Test-Time Harness Evolution](https://arxiv.org/abs/2607.08124). arXiv, 2026.

8. Jimenez, C. E. et al. [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770). *International Conference on Learning Representations*, 2024.

9. SWE-bench. [SWE-bench Verified](https://www.swebench.com/verified.html).

10. Khattab, O. et al. [DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines](https://arxiv.org/abs/2310.03714). *International Conference on Learning Representations*, 2024.

11. Yuksekgonul, M. et al. [TextGrad: Automatic Differentiation via Text](https://arxiv.org/abs/2406.07496). *Nature*, 2025.

12. Anthropic. [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). Anthropic Engineering, 2026.