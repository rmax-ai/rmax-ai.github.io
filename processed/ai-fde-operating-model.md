AI FDE Operating Model: Exploration, Pilot, and Production
Version 2 — Evidence-Gated Delivery for AI-Enabled Workflows

Purpose

This operating model helps AI Forward Deployed Engineering (FDE) teams move from uncertain ideas to reliable production workflows without applying full production controls before value is demonstrated or treating experimentation as an exemption from responsible engineering.

The model separates work into three operating modes:

1. Exploration — determine whether an AI capability can create meaningful value.
2. Pilot — determine whether the workflow can create repeatable value for real users under bounded operating conditions.
3. Production — operate the workflow reliably, securely, economically, and accountably at organizational scale.

The core principle is sequencing: prove value, characterize failure, then engineer reliability and governance around the valuable path. This model is an organizational synthesis rather than a formal standard. It applies lifecycle-oriented principles from the NIST AI Risk Management Framework, ISO/IEC 42001, production machine-learning practice, site reliability engineering, human-factors research, and risk-based regulation [1–8].

1. Why this model is necessary

Conventional software and AI-enabled systems differ in an important way. Conventional software can often be tested against relatively explicit behavioral specifications. AI-enabled workflows add empirical capability uncertainty: even when the business task is clear, the team may not know whether a model can perform it reliably across representative cases, which context and tools it needs, how users will adapt their behavior around it, or which failures will dominate in operation.

A successful demonstration therefore establishes possibility, not production readiness. Production ML research has repeatedly shown that model quality is only one part of a larger system that includes data, integrations, configuration, monitoring, ownership, and operational controls [5][6].

Teams commonly make one of two mistakes.

The first is premature productionization. The team applies production architecture, exhaustive edge-case analysis, and broad governance review before establishing whether the workflow creates enough value to justify the investment. This increases cost and cycle time while reducing the number of hypotheses that can be tested.

The second is uncontrolled experimentation. The team moves an impressive prototype into real workflows without defining permissions, observability, ownership, acceptable failure, or termination conditions. This creates operational, security, legal, and reputational risk.

The Exploration–Pilot–Production model avoids both errors by scaling evidence and controls according to the system’s authority, reversibility, blast radius, data sensitivity, user exposure, and usage scale. This is consistent with risk-proportional lifecycle management in the NIST AI RMF and ISO/IEC 42001, and with the EU AI Act’s continuous and iterative treatment of risk for systems within its scope [1][3][4].

2. Operating principles

2.1 Separate capability risk from operational risk

Capability risk asks: can the model-enabled workflow perform the task well enough to matter?

Operational risk asks: what happens when the system is wrong, manipulated, unavailable, misunderstood, or over-trusted?

Exploration should resolve the largest capability uncertainties using the smallest safe experiment. Pilot should characterize both capability and operational risk under realistic but bounded conditions. Production should reduce operational risk to an explicitly accepted level and continuously verify that the accepted operating conditions still hold.

2.2 Bound consequences instead of demanding certainty

Review alone cannot eliminate behavioral uncertainty from probabilistic components. Reliability therefore depends on combining empirical evaluation with deterministic constraints on access, outputs, and actions.

Useful controls include read-only tools, scoped credentials, isolated datasets, action allowlists, schema validation, transaction limits, step and cost limits, human approval, tamper-evident audit records, and reversible or compensating writes. These controls follow established principles of least privilege, separation of duties, traceability, and zero-trust authorization [9][10].

2.3 Increase controls with authority and irreversibility

A workflow that summarizes approved internal documents requires fewer controls than one that modifies payment configuration, communicates externally, changes access rights, or makes a binding financial decision.

Governance should be proportional to the concrete power granted to the workflow, the sensitivity of the data it handles, and the difficulty of correcting a failure—not to how novel or impressive the technology appears.

2.4 Use evidence to move between stages

Stage transitions should depend on observed results, not enthusiasm, fear, seniority, or architectural preference.

Each initiative should define:

• the hypothesis;
• the user and workflow;
• the current baseline;
• measurable success criteria;
• unacceptable outcomes;
• evidence required for the next stage;
• the owner of the transition decision.

This reflects the measurement-oriented structure of the NIST AI RMF and production-readiness approaches such as the ML Test Score [1][5].

2.5 Treat human oversight as a designed system component

A nominal human-approval step is not sufficient by itself. Oversight effectiveness depends on reviewer competence, information quality, independent verifiability, time pressure, incentives, authority to intervene, and the risk of automation bias.

The team must define what the human reviews, which evidence and uncertainty are shown, how much time is available, what happens after rejection, and whether review quality degrades as volume increases. Systematic reviews of automation bias show that people may accept incorrect automated recommendations or fail to seek contradictory information, especially when verification is costly or the task is complex [7][8]. For regulated high-risk systems, the EU AI Act similarly requires human oversight that is effective, proportionate, and capable of intervention rather than merely nominal [4].

2.6 Evaluate the workflow, not only the model

The unit of evaluation is the socio-technical workflow: user intent, data, retrieval, prompts, model behavior, tools, policies, interfaces, human review, downstream execution, and business outcome.

A technically correct model output can still fail because it reaches the wrong person, arrives too late, lacks evidence, invokes the wrong tool, exceeds cost limits, or encourages inappropriate reliance. Holistic evaluation research and human–AI interaction guidance support evaluating multiple dimensions and the surrounding interaction system rather than relying on a single accuracy score [11][12].

3. Lifecycle overview

Exploration answers: Is there a valuable capability here?

Pilot answers: Can real users obtain repeatable value under bounded and observable conditions?

Production answers: Can the organization operate this workflow safely, reliably, economically, and accountably at scale?

An initiative may stop at any stage. Not every successful exploration should become a pilot, and not every successful pilot should become a production service. The purpose is disciplined learning, not automatic progression.

A workflow may also regress to an earlier stage after a material model, tool, policy, data, or scope change. Production evidence is conditional on the system configuration and operating environment that produced it.

4. Stage 1 — Exploration

4.1 Objective

Exploration establishes whether an AI-enabled workflow can materially improve a real task. The team should maximize learning speed while preventing material harm.

The output is evidence about capability, workflow design, failure modes, and likely value. It is not a production-ready system.

4.2 Typical questions

• Can the model perform the core reasoning, retrieval, generation, or classification task?
• Which context, tools, and instructions materially improve performance?
• Does an agentic loop outperform a simpler prompt, search flow, rules engine, or deterministic workflow?
• What are the dominant failure modes?
• Can a human recognize and correct failures efficiently?
• Is the estimated value large enough to justify a pilot?

4.3 Entry criteria

An exploration may begin when:

• a specific user or business problem has been identified;
• the team can state a falsifiable hypothesis;
• a representative test set or task sample is available;
• the proposed experiment has a bounded blast radius;
• data access is approved for the experimental environment;
• one person owns the experiment and its conclusion.

Example hypothesis:

“An AI workflow can reduce the median time required to investigate a merchant-support case from 25 minutes to under 10 minutes while producing no unauthorized actions and maintaining at least 80% reviewer acceptance on a representative task sample.”

4.4 Required controls

Exploration defaults should include:

• synthetic, sanitized, or explicitly approved data;
• read-only access unless writes are essential to the hypothesis;
• no unsupervised external communication;
• hard limits on tool calls, runtime, and cost;
• sufficient end-to-end traces to reconstruct material decisions and actions, subject to privacy, retention, and secret-redaction requirements;
• a small named group of testers;
• explicit experimental labeling;
• manual review of all consequential outputs;
• a documented stop condition.

Controls may be lighter for local prompt evaluation and stricter for connected agents, but the team must always know the maximum plausible consequence of a failed run.

4.5 Required artifacts

The exploration owner produces:

• problem statement;
• hypothesis and expected value;
• workflow sketch;
• permission and data inventory;
• evaluation dataset or representative task sample;
• baseline comparison;
• experiment log;
• failure taxonomy;
• recommendation: stop, iterate, or request pilot.

4.6 Evaluation

Exploration metrics should primarily test capability and user value:

• task completion rate;
• reviewer acceptance rate;
• factual or procedural correctness;
• time saved against the baseline;
• number and severity of human corrections;
• tool-selection and tool-execution success;
• policy-compliance rate;
• cost and latency per task;
• qualitative user feedback;
• failure categories and recurrence.

Averages alone are insufficient. The team should inspect individual failures and identify whether they originate from the model, missing or stale context, retrieval, tool design, authorization, ambiguous policy, user interaction, or system integration. Evaluation should include representative cases and known difficult cases, and should record model, prompt, tool, policy, and dataset versions [5][11].

4.7 Exit criteria

Move to Pilot when:

• the workflow demonstrates meaningful improvement over the baseline;
• dominant failure modes are understood well enough to design controls;
• the expected business value justifies further investment;
• a real user group and business owner agree to participate;
• the pilot can be bounded by scope, permissions, volume, and duration;
• no unresolved risk makes real-world testing unacceptable.

Stop or redesign when:

• a simpler deterministic approach performs as well;
• users do not value the outcome;
• required accuracy is beyond demonstrated capability;
• critical failures cannot be detected or contained;
• data or access requirements are disproportionate to expected value.

5. Stage 2 — Pilot

5.1 Objective

The Pilot validates whether the workflow produces repeatable value for real users under realistic but constrained operating conditions.

A pilot is not merely a larger demo. It introduces real users, real workflow variation, operational responsibilities, and controlled exposure to organizational systems.

5.2 Typical questions

• Do users adopt the workflow without intensive support?
• Does performance hold across realistic task variation?
• Which errors occur in practice, and how severe are they?
• Are human review and escalation procedures effective?
• Are latency, cost, and operational effort acceptable?
• What controls and product changes are required for production?

5.3 Entry criteria

A pilot may begin when:

• Exploration exit criteria are satisfied;
• a business owner accepts the pilot objectives and boundaries;
• pilot users and workflow scope are named;
• success, failure, and termination criteria are documented;
• data, privacy, security, and access owners approve the bounded setup;
• support and incident ownership are assigned;
• the team can monitor every material action and outcome.

5.4 Pilot boundaries

Every pilot should define:

• start and end dates;
• participating users or teams;
• task types included and excluded;
• data sources;
• tool permissions;
• maximum transaction or action volume;
• human approval points;
• model, prompt, policy, retrieval, and tool versions;
• fallback process;
• incident and escalation path.

Boundaries convert vague risk into an inspectable operating envelope.

5.5 Required controls

Pilot controls generally include:

• least-privilege identity and scoped credentials;
• approved production-like data access;
• allowlisted tools and actions;
• human approval before consequential or external actions;
• structured logs and trace retention;
• monitoring for quality, cost, latency, and policy violations;
• rollback or compensating-action procedures;
• user feedback and issue-reporting channels;
• defined support hours and owner;
• versioned prompts, policies, tools, retrieval configurations, and models;
• explicit handling of sensitive data;
• periodic review of representative successful and failed runs.

For higher-risk workflows, add dual approval, transaction thresholds, environment isolation, policy engines, deterministic validation before execution, and stronger separation of duties. These controls align with established access-control and audit principles in NIST SP 800-53 and zero-trust architecture [9][10].

5.6 Required artifacts

The pilot owner produces:

• pilot charter;
• scope and operating boundaries;
• user journey and workflow definition;
• risk register and control mapping;
• evaluation plan;
• runbook and escalation procedure;
• monitoring dashboard;
• change log;
• user feedback summary;
• production-readiness assessment;
• recommendation: stop, extend, redesign, or promote.

5.7 Evaluation

Pilot metrics should cover five dimensions.

Business value:
• cycle-time reduction;
• throughput increase;
• avoided manual effort;
• quality improvement;
• financial or operational impact.

User value:
• adoption and repeat usage;
• completion without expert intervention;
• user trust calibrated to actual performance;
• satisfaction and reported friction.

Quality:
• successful task completion;
• severity-weighted error rate;
• human override and rejection rate;
• unsupported claims or policy violations;
• recovery rate after failure;
• tool-selection, argument, and execution correctness.

Operations:
• availability;
• latency;
• cost per successful task;
• support burden;
• incident frequency and mean time to recovery.

Risk:
• unauthorized-action attempts;
• access-control violations;
• sensitive-data exposure;
• prompt-injection or tool-manipulation events;
• audit completeness;
• effectiveness of human approval.

5.8 Exit criteria

Move to Production when:

• business value is demonstrated across a representative operating period;
• quality meets a documented threshold for the workflow;
• severe failures are rare, detectable, and contained;
• users can operate the workflow with sustainable support;
• cost and latency are acceptable;
• production ownership and funding are established;
• security, privacy, compliance, and operational reviews are complete;
• monitoring, rollback, incident response, and change management are ready;
• residual risks are explicitly accepted by accountable owners.

A pilot should not enter production merely because users like it. Production requires operational ownership, evidence of control effectiveness, and accepted residual risk.

6. Stage 3 — Production

6.1 Objective

Production delivers sustained organizational value while maintaining reliability, security, accountability, and controlled evolution.

Production is an operating commitment, not a deployment event.

6.2 Production requirements

Production workflows require:

• named business and technical owners;
• service-level objectives appropriate to business impact;
• documented data classification and retention;
• least-privilege access with periodic review;
• production-grade observability and tamper-evident audit trails;
• incident response and rollback procedures;
• version and change management;
• regression and safety evaluations;
• cost monitoring and capacity controls;
• user documentation and support model;
• periodic reassessment of model, tool, retrieval, data, and policy performance;
• retirement criteria and a decommissioning process.

These requirements are consistent with AI management-system practice, production ML readiness, and site reliability engineering [3][5][13][14].

6.3 Change management

AI behavior can change when the model, prompt, retrieved knowledge, embedding or ranking configuration, tool implementation, authorization policy, user interface, or surrounding workflow changes. Production teams should therefore treat these as versioned system components.

Material changes should trigger proportionate regression testing. High-impact changes may require shadow evaluation, canary deployment, renewed approval, or a temporary return to pilot conditions. Production ML literature identifies configuration, data dependencies, and changing external conditions as major sources of hidden technical debt [6].

6.4 Production evaluation

Production evaluation should combine:

• offline regression suites;
• sampled human review;
• automated policy, schema, and format checks;
• outcome-based business metrics;
• incident analysis;
• user feedback;
• input and population-shift monitoring;
• knowledge-base and retrieval-quality monitoring;
• model, tool, and policy change detection;
• red-team or adversarial testing for relevant threats.

The team should measure the entire socio-technical workflow, not only model accuracy. A technically correct output can still fail because it reaches the wrong user, arrives too late, lacks necessary evidence, invokes an unauthorized action, or encourages inappropriate reliance [11][12].

6.5 Production stop conditions

Pause, restrict, or regress the workflow when:

• a severe unauthorized or harmful action occurs;
• quality falls below the accepted threshold;
• monitoring or auditability is unavailable;
• model, data, retrieval, policy, or tool changes invalidate prior evidence;
• costs exceed agreed limits;
• policy, legal, or data requirements change;
• user behavior creates unacceptable over-reliance;
• ownership is no longer clear.

7. Stage-gate decision framework

At each transition, reviewers should assess six dimensions.

Value: Does the workflow materially improve an important outcome?

Capability: Can the system perform the task across representative cases?

Control: Can failures be prevented, detected, contained, corrected, or reversed?

Operability: Can the organization support, monitor, change, and recover the system?

Economics: Are implementation, inference, review, and support costs justified?

Accountability: Is there a named owner authorized to accept residual risk?

The decision options are:

• Stop — evidence does not justify continued investment.
• Iterate — revise the hypothesis, workflow, context, or controls.
• Continue within stage — gather more representative evidence.
• Advance — evidence and ownership satisfy the next stage’s entry criteria.
• Regress — return a production or pilot workflow to an earlier stage after a material change or failure.

8. Risk-based control matrix

8.1 Low-impact advisory workflow

Examples: document summarization, drafting internal notes, knowledge discovery.

Typical controls:
• approved data access;
• clear source attribution;
• user review;
• logging;
• no autonomous external actions.

8.2 Moderate-impact operational workflow

Examples: preparing case recommendations, drafting Jira changes, proposing merchant-support responses.

Typical controls:
• scoped tool permissions;
• required human approval;
• structured validation;
• rollback or correction path;
• monitoring and sampled review.

8.3 High-impact consequential workflow

Examples: changing financial configuration, issuing refunds, modifying access, or communicating binding decisions.

Typical controls:
• deterministic policy checks;
• strict transaction limits;
• dual approval where appropriate;
• strong identity and authorization;
• tamper-evident, access-controlled audit records with defined retention;
• continuous monitoring;
• tested rollback or compensating actions;
• formal risk acceptance.

This internal impact classification is an operating tool. It should not be confused with legal classifications such as “high-risk AI system” under the EU AI Act, which have specific statutory definitions [4].

9. Roles and decision rights

Business owner

Defines the outcome, provides users, accepts process change, and owns realized business value.

FDE or initiative lead

Owns the hypothesis, experiment design, integration, evidence, and stage recommendation.

Platform owner

Provides approved models, tools, identity, observability, evaluation infrastructure, and operational standards.

Security, privacy, legal, or compliance partners

Evaluate concrete data, access, and action risks at the level appropriate to the stage.

Pilot users

Test the workflow, report failures, and validate whether it fits real work.

Production service owner

Owns reliability, incidents, changes, support, cost, and decommissioning after launch.

Stage decision authority

Makes the formal stop, continue, advance, or regress decision. For low-risk initiatives this may be the FDE and business owner. Higher-impact workflows require broader accountable approval.

Clear responsibility and continual improvement are central to ISO/IEC 42001 and the Govern function of the NIST AI RMF [1][3].

10. Recommended governance cadence

Exploration review — weekly

Focus on capability evidence, failure analysis, and whether another iteration is justified.

Pilot review — every one or two weeks

Focus on user outcomes, incidents, emerging risks, support burden, and boundary changes.

Production review — monthly or quarterly, depending on impact

Focus on service health, business value, quality degradation, incidents, costs, access, and material changes.

These cadences are operating defaults, not universal evidence-based intervals. Teams should shorten them for rapidly changing or high-impact workflows and lengthen them only when evidence and operational stability justify it.

Governance meetings should review evidence and decisions, not repeat abstract debates about whether agents are safe.

11. Worked example: internal support-case investigation

Exploration

The team tests whether an AI workflow can gather relevant policy, account, and historical case information and produce an investigation brief. It uses a curated dataset, read-only tools, twenty representative cases, and sufficient trace capture to reconstruct each result.

Success criteria:
• at least 80% reviewer acceptance;
• at least 40% reduction in investigation time;
• no fabricated source references;
• no access outside the approved dataset.

Pilot

Ten support specialists use the workflow for four weeks. The agent can query approved internal systems but cannot modify cases or contact merchants. Users approve the final brief, rate usefulness, and classify corrections. The team measures quality, adoption, support burden, cost, latency, and the effectiveness of review.

Production

The workflow becomes an integrated support tool with managed identity, access review, quality monitoring, regression evaluations, incident ownership, versioned changes, and quarterly value assessment. Any later request to let the agent modify cases or send messages is treated as a material capability expansion and must pass through a bounded pilot.

12. Anti-patterns

Production review during ideation

The team attempts to resolve every production edge case before establishing value.

Demo-driven promotion

A compelling demonstration is treated as evidence of repeatable performance.

Permanent pilot

The workflow runs indefinitely with real users but without production ownership, support, or risk acceptance.

Human-in-the-loop theatre

A human approval step exists, but reviewers lack time, context, independent evidence, or incentives to detect errors.

Governance by imagination

Discussions focus on agents “going rogue” without specifying permissions, failure paths, likelihood, or impact.

Architecture before evidence

The team builds a general platform before validating the first valuable workflows.

Accuracy-only evaluation

The team ignores workflow fit, user behavior, cost, latency, support burden, tool use, and downstream consequences.

Trace-everything without data governance

The team captures prompts, outputs, tool arguments, secrets, or personal data without a defined purpose, access model, retention period, or redaction policy.


15. Leadership principle

The objective is not to choose between innovation and safety. The objective is to sequence them correctly.

Exploration creates evidence about what is possible. Pilot creates evidence about what is useful and controllable. Production converts that evidence into an accountable operating system.

References

[1] National Institute of Standards and Technology. Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST AI 100-1, January 2023. https://doi.org/10.6028/NIST.AI.100-1

[2] National Institute of Standards and Technology. Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile. NIST AI 600-1, July 2024. https://doi.org/10.6028/NIST.AI.600-1

[3] International Organization for Standardization. ISO/IEC 42001:2023 — Information technology — Artificial intelligence — Management system. December 2023. https://www.iso.org/standard/42001.html

[4] European Union. Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence. Official Journal of the European Union, 12 July 2024. https://eur-lex.europa.eu/eli/reg/2024/1689/oj

[5] Breck, E., Cai, S., Nielsen, E., Salib, M., and Sculley, D. The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction. IEEE International Conference on Big Data, 2017. https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/

[6] Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., Chaudhary, V., Young, M., Crespo, J.-F., and Dennison, D. Hidden Technical Debt in Machine Learning Systems. Advances in Neural Information Processing Systems 28, 2015. https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems

[7] Goddard, K., Roudsari, A., and Wyatt, J. C. Automation Bias: A Systematic Review of Frequency, Effect Mediators, and Mitigators. Journal of the American Medical Informatics Association 19(1), 2012. https://doi.org/10.1136/amiajnl-2011-000089

[8] Lyell, D., and Coiera, E. Automation Bias and Verification Complexity: A Systematic Review. Journal of the American Medical Informatics Association 24(2), 2017. https://doi.org/10.1093/jamia/ocw105

[9] National Institute of Standards and Technology. Security and Privacy Controls for Information Systems and Organizations. NIST SP 800-53 Rev. 5, September 2020, updated 2023. https://doi.org/10.6028/NIST.SP.800-53r5

[10] Rose, S., Borchert, O., Mitchell, S., and Connelly, S. Zero Trust Architecture. NIST SP 800-207, August 2020. https://doi.org/10.6028/NIST.SP.800-207

[11] Liang, P. et al. Holistic Evaluation of Language Models. Transactions on Machine Learning Research, 2023. https://arxiv.org/abs/2211.09110

[12] Amershi, S. et al. Guidelines for Human-AI Interaction. Proceedings of CHI 2019. https://doi.org/10.1145/3290605.3300233

[13] Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds. Site Reliability Engineering: How Google Runs Production Systems. O’Reilly Media, 2016. https://sre.google/sre-book/table-of-contents/

[14] Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K., and Thorne, S., eds. The Site Reliability Workbook. O’Reilly Media, 2018. https://sre.google/workbook/table-of-contents/

