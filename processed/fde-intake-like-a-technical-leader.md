How to Run an FDE Intake Like a Technical Leader

Today I want to explain a deceptively simple process: how to take an incoming business request and decide whether an engineering team should invest more time in it.

On the surface, this sounds like intake management.

Someone comes with a problem. You ask some questions. You write some notes. Maybe you build something.

But that is not really the job.

The actual job is converting ambiguity into a defensible decision.

And that distinction matters, especially for a Forward Deployed Engineering team.

An FDE team usually sits in an uncomfortable place between business problems and technical capabilities. Stakeholders often arrive knowing that something is painful, but they may not know exactly why it is painful. They may not know how large the problem is. And increasingly, they may arrive with the solution already embedded in the request.

"We need an agent."

"We need an AI assistant."

"We need RAG."

"We need automation."

The first discipline of good intake is separating the requested mechanism from the underlying problem.

So the process I want to describe looks like this:

Request.

Problem clarification.

Business impact.

Prioritization.

Discovery.

Then, only later, solution design and execution.

The important thing is that each stage reduces uncertainty.

---

Stage One: The Request Is Not the Problem

Imagine a stakeholder says:

"We need an AI agent to qualify requests before they reach our team."

The naive engineering reaction is:

Okay. What model do we use?

What tools does the agent need?

Should we use MCP?

What data sources should it access?

But those questions are premature.

The first question should be:

What is happening today that makes you believe you need an agent?

That simple question changes the entire conversation.

Maybe the stakeholder explains that incoming requests are poorly specified.

Different teams provide different information.

Some requests require four meetings before anyone realizes that the opportunity is too small.

Other requests get escalated because the stakeholder does not understand why their request has not been prioritized.

Now the problem looks very different.

The problem is not:

"We don't have an intake agent."

The problem might be:

"We lack a consistent way to turn loosely defined requests into comparable business cases."

That is a much stronger problem definition.

It does not assume a solution.

And more importantly, it tells us what the organization actually needs to improve.

---

Stage Two: Start With a Concrete Example

People are usually bad at describing processes abstractly.

Ask someone how their workflow works and you will often get the idealized version.

So instead of asking:

"How does this process work?"

ask:

"Can we walk through the most recent real example?"

Now reconstruct what actually happened.

What triggered the process?

Who became involved?

Which systems were used?

Where did information come from?

Where were decisions made?

Where were handoffs required?

Where did someone wait?

Where did someone need judgment?

What happened at the end?

A concrete example gives you evidence.

For instance, perhaps six people participated across three meetings over two weeks before deciding that a request should not be pursued.

That is immediately more useful than:

"Our intake process is inefficient."

This is a fundamental principle of good discovery:

Concrete first. Abstract second.

You observe specific cases, then infer the pattern.

---

Stage Three: Translate Operational Pain Into Business Impact

This is probably the most important part of the intake process.

Stakeholders often describe operational problems.

"People spend too much time searching."

"We have too many manual steps."

"The process is slow."

"Requests are badly written."

Those statements may all be true.

But none of them yet explain why the company should allocate engineering capacity to the problem.

You need a causal chain.

Something like:

Fragmented requests lead to multiple discovery meetings.

Multiple discovery meetings consume scarce FDE capacity.

Scarce FDE capacity spent on low-value opportunities reduces the team's ability to investigate higher-value work.

Therefore, the business consequence is not simply wasted time.

It is worse portfolio allocation.

That is the executive-level translation.

Another example:

Account managers spend two hours each week reconciling information across three systems.

That creates slower case resolution.

Slower case resolution affects merchant responsiveness.

Merchant responsiveness may affect customer experience or revenue.

The pattern is:

Operational friction.

Immediate consequence.

Downstream business effect.

Strategic implication.

If you cannot build that chain, you probably do not yet understand the opportunity.

---

Stage Four: Establish Scale

A serious business problem has some form of magnitude.

You do not always need perfect numbers.

But you need enough information to distinguish a local irritation from an economically meaningful problem.

Ask:

How often does this happen?

How many cases are involved?

How many people touch each case?

How much time is spent?

How long does the process take end to end?

Is the volume increasing?

Does the same pattern exist in other teams?

Suppose a stakeholder says:

"We get around twelve requests a month. Each typically involves three or four people and several hours of combined work."

That does not give you an exact ROI calculation.

But it gives you an order of magnitude.

And order of magnitude is often enough for a first-stage decision.

A useful rule here is:

Prefer an honest range over fake precision.

"Ten to fifteen requests per month" is better than inventing "12.3 requests."

---

Stage Five: Understand Strategic Relevance

Not every painful problem deserves investment.

This is where engineering intake becomes portfolio management.

Ask:

Why does this matter now?

Which organizational priority does it support?

What competing work would this displace?

Is this problem specific to one team, or does it reveal a reusable pattern?

If we improved only one part of the workflow, what change would create the most value?

This forces prioritization.

A stakeholder may genuinely have a problem.

But if solving it consumes three months of engineering capacity and affects five people, while another opportunity affects three hundred people and supports an explicit strategic priority, those opportunities should not be treated equally.

Leadership begins when you stop evaluating problems in isolation.

You start evaluating them relative to alternatives.

---

Stage Six: Define Success Before Designing the Solution

Before discussing architecture, ask:

"If we revisit this after an intervention, what would make you say it worked?"

This is surprisingly powerful.

Maybe success means:

Decision time drops from two weeks to two days.

The number of meetings before a go or no-go decision falls by half.

Requests arrive with the information needed for prioritization.

Stakeholder escalations decrease.

Human effort per request falls by thirty percent.

Now you have something that can later be evaluated.

And notice something important.

None of those metrics mention AI.

That is exactly what you want.

The outcome should be independent of the implementation.

An agent is successful only if it improves the business outcome.

The existence of an agent is not itself success.

---

Stage Seven: Separate Facts, Hypotheses, and Unknowns

This is one of the most important habits in senior technical work.

During the meeting, maintain three mental buckets.

Facts.

Hypotheses.

Unknowns.

A fact might be:

"Twelve requests arrived last month."

A hypothesis might be:

"Poor request quality is the primary cause of long decision times."

An unknown might be:

"We do not know whether delays mostly come from incomplete requests or internal decision-making."

These categories should not be mixed.

Weak decision-making often happens because an assumption quietly turns into a fact as it moves through documents and meetings.

Someone says:

"I think most of the delay comes from missing information."

Three weeks later, the architecture document says:

"The main bottleneck is missing information."

Nobody notices the transformation.

Good FDE work prevents that.

You make uncertainty visible.

---

Stage Eight: Park Solutions Without Dismissing Them

This is especially important when working with senior stakeholders.

If someone says:

"We should build an agent."

You do not need to say:

"No, that's premature."

That creates unnecessary resistance.

Instead say:

"That sounds like one plausible intervention. I'll capture it. Before deciding on the mechanism, I want to understand the outcome and what information actually determines whether a request is valuable."

That response does three things.

It acknowledges the stakeholder.

It preserves the idea.

And it keeps control of the discovery process.

You are not opposing the solution.

You are sequencing the decision correctly.

---

Stage Nine: Synthesize Before the Meeting Ends

The final three minutes are critical.

Do not finish with:

"Great, thanks. I'll write this up."

Instead, construct a shared representation of the problem while everyone is still present.

Something like:

"Let me play back what I've understood.

The core problem is that loosely defined requests cannot currently be compared consistently.

That affects the FDE intake process and consumes significant discovery capacity.

The primary business consequence appears to be inefficient allocation of engineering attention.

We have an initial estimate of the volume, but we still need stronger evidence on the amount of effort per request.

A meaningful improvement would reduce the effort and time required to reach a prioritization decision.

The main unknown is which information actually predicts whether an opportunity is worth pursuing.

My proposed next step is to validate that using a small sample of previous requests.

Is that an accurate characterization?"

This is not just summarization.

This is stakeholder alignment.

You are giving everyone a chance to correct your mental model before it becomes the written record.

That is one of the highest-value leadership behaviors in the entire process.

---

Stage Ten: Turn the Meeting Into an Assessment

After the meeting, you should not produce twenty pages of notes.

You should compress what you learned into a one-page opportunity assessment.

That assessment should answer:

What is the problem?

Who is affected?

What is the business impact?

What is the scale?

Why does it matter strategically?

What does success look like?

What evidence do we have?

What remains unknown?

What constraints matter?

What solutions were suggested?

And what do we recommend next?

The recommendation should usually fall into one of four categories:

Proceed to deeper discovery.

Gather specific missing evidence first.

Redirect the problem elsewhere.

Or decline.

This is important because intake should be a gate.

It should not be an automatic path into engineering.

---

Stage Eleven: Use a Scorecard to Make the Decision Inspectable

As the number of opportunities grows, intuition is no longer enough.

You need a lightweight assessment framework.

You might evaluate:

Business impact.

Scale.

Strategic alignment.

AI leverage.

Feasibility.

Reusability.

Risk.

Evidence confidence.

The purpose of the scorecard is not mathematical truth.

The purpose is to expose your reasoning.

Why did opportunity A proceed while opportunity B did not?

Because A had high business impact, strong strategic alignment, reusable potential, and sufficient evidence.

B had enthusiastic stakeholders but weak evidence and limited scale.

Now the decision becomes inspectable.

That matters for trust.

Especially when stakeholders disagree.

---

Stage Twelve: Discovery Is Its Own Phase

If an opportunity passes intake, you still should not jump immediately into implementation.

Create a short discovery plan.

What questions must be answered?

What evidence is required?

Which users should we interview?

Which systems should we inspect?

Which hypotheses should we test?

Do we need a prototype?

What evaluation would tell us whether the idea works?

What decision will we make at the end?

And what is the timebox?

For example:

"Determine whether AI-assisted qualification can reduce intake effort by at least thirty percent while preserving prioritization quality."

That is a discovery objective.

"Build an intake agent" is not.

One is a question.

The other already assumes the answer.

---

The Larger Mental Model

Now step back.

The entire process is a funnel.

A stakeholder begins with ambiguity.

Maybe they have a complaint.

Maybe they have a request.

Maybe they already have a technical idea.

Your job is progressively to compress that ambiguity.

Conversation becomes evidence.

Evidence becomes a problem definition.

The problem definition becomes a business-impact hypothesis.

That becomes an opportunity assessment.

The assessment produces a prioritization decision.

The prioritization decision, if positive, becomes a discovery plan.

Discovery produces evidence.

Evidence eventually supports an implementation decision.

And implementation is evaluated against the success criteria defined at the beginning.

So the full loop is:

Request.

Clarify.

Quantify.

Prioritize.

Discover.

Build.

Measure.

Learn.

That is the FDE operating system.

---

Why This Matters for Leadership

There is also a deeper leadership lesson here.

A senior engineer often creates value by solving difficult problems.

A technical leader creates value by ensuring that the organization is solving the right difficult problems.

That requires a different skill.

You have to resist the intellectual reward of immediately designing the system.

You have to tolerate ambiguity longer.

You have to ask questions that sometimes feel less technically sophisticated.

You have to understand incentives, impact, constraints, and organizational priorities.

And then you have to turn all of that into a decision that other people can understand and defend.

That is stakeholder management in a technical organization.

It is not simply being polite.

It is creating a reliable decision process across people who have different information, incentives, and mental models.

And when you can do that consistently, something important changes.

People stop seeing you only as someone who can build sophisticated systems.

They start trusting you with deciding which systems should exist in the first place.

That is the transition from senior engineer to technical leader.

The core principle is simple:

Do not optimize for having the answer fastest.

Optimize for creating a process that reliably produces a defensible answer.

As Peter Drucker put it:

"There is nothing so useless as doing efficiently that which should not be done at all."
