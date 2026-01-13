Title: Code Is the New Assembly

For most of computing history, progress meant not writing code at the level the machine actually executes. We stopped writing in assembly not because it was impossible, but because it was inefficient, error-prone, and cognitively expensive. Higher-level languages didn’t make computers more powerful; they made humans more effective by moving us away from instruction-by-instruction control and toward intent.

We are at the same inflection point again.

Today, writing and reviewing code manually increasingly resembles writing and reading assembly. It is technically precise, locally correct, and globally exhausting. With agents now able to generate, refactor, and review code at inference speed, insisting that humans remain in the loop at the level of syntax is a category error. We are clinging to the wrong abstraction.

The real shift is not “AI writes code.”
The shift is that code has become a compilation target, not the primary artifact of human thought.

From Instructions to Contracts

In the assembly era, programmers specified how the machine should do something: move this register, jump here, compare that value. Higher-level languages changed the contract. You described what you wanted—data structures, control flow, invariants—and the compiler handled the rest.

Large language models introduce a new abstraction boundary. The primary artifact is no longer source code, but a human–agent contract: a specification of intent, constraints, and acceptable behavior. Today, that contract often takes the form of a “mega prompt,” but prompts are just the first crude syntax of this layer.

These contracts encode:
	•	What problem is being solved (and which are explicitly not)
	•	Constraints and invariants the solution must respect
	•	Quality bars: performance, safety, style, risk tolerance
	•	Stopping conditions: when work is considered done

Agents consume this contract and emit code the way compilers emit machine instructions. Complaining about unreadable AI-generated code is like complaining that assembly is hard to reason about. That is precisely why we invented higher-level abstractions in the first place.

Why Code Review No Longer Scales

If agents can produce and review code faster than humans can read it, then human-level code review becomes a bottleneck, not a safeguard. This does not mean quality disappears; it means validation must move up the stack.

We already know this pattern:
	•	We don’t validate compilers by reading their output.
	•	We validate them by testing semantics, invariants, and edge cases.

The same must happen with agent-generated systems. Humans should validate:
	•	Whether the system satisfies the stated intent
	•	Whether invariants hold under stress
	•	Whether failure modes are acceptable
	•	Whether the system aligns with business, ethical, or social constraints

Line-by-line inspection is replaced by property-based trust.

Intent Becomes the Source of Truth

In an agent-native world, the most important files in a repository are no longer *.go or *.ts. They are documents that answer:
	•	What are we trying to do?
	•	Why does this system exist?
	•	What must never be violated?
	•	What trade-offs are we consciously accepting?

Code is an implementation detail—necessary, but secondary.

This also reframes engineering skill. The scarce capability is no longer typing speed or API recall. It is:
	•	Framing problems correctly
	•	Defining crisp constraints
	•	Detecting when the system is solving the wrong problem very efficiently
	•	Knowing when to stop, ship, or kill a project

Agents are excellent at filling in solution space. Humans remain responsible for shaping that space.

The New Division of Labor

Agents operate at inference speed, optimizing within a given frame.
Humans operate at decision speed, choosing the frame itself.

This is not a loss of agency. It is a relocation of agency upward.

Just as higher-level languages did not “dumb down” programmers, agent-driven development does not eliminate engineers. It eliminates unnecessary proximity to the machine. The work that remains is harder, not easier: judgment, taste, responsibility, and intent.

We didn’t stop writing assembly because it stopped working.
We stopped because we found something better to think about.

“The purpose of abstraction is not to hide complexity, but to make the right complexity visible.”