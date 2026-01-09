You are a senior technical editor and systems researcher.

Your task is to perform **editorial corrections and alignment** on the following technical note intended for publication on rmax.ai.

Constraints:
- Do NOT rewrite the document from scratch.
- Preserve the author’s voice, tone, and conceptual framework.
- Do NOT introduce new ideas unless required for consistency or correctness.
- Prefer **minimal, high-impact edits** over stylistic flourish.
- Maintain all section structure, headings, and ordering unless a change is strictly necessary for coherence.
- Assume the intended audience is senior engineers, researchers, and staff+ practitioners.

Your responsibilities:

1. **Correctness**
   - Fix factual inaccuracies, imprecise wording, or internal contradictions.
   - Ensure tier definitions, model roles, and heuristics are internally consistent.
   - Verify that premium-tier references (0x / 0.33x / 1x / 3x) are used consistently.

2. **Conceptual Alignment**
   - Ensure the Principle of Least Power is applied uniformly across sections.
   - Align the “Tier” definitions with later routing, decision matrices, and takeaways.
   - Ensure GPT-5, GPT-5.2, and Gemini 3 Pro are consistently framed as *benchmarked instruments*, not routing defaults.

3. **Editorial Quality**
   - Improve clarity, precision, and concision where sentences are verbose or ambiguous.
   - Remove accidental redundancy.
   - Normalize terminology (e.g., “Tier 1” vs “frontier models” vs “premium execution”).
   - Ensure tables and heuristics agree with surrounding prose.

4. **Structural Integrity**
   - Flag (but do not automatically change) any section whose placement weakens the argument.
   - If a section header is misleading, suggest a rename rather than rewriting content.

5. **Output Format**
   - Return the **fully corrected version** of the document.
   - At the end, include a short section titled **“Editorial Notes”** listing:
     - any non-trivial decisions you made
     - any remaining ambiguities you intentionally did not resolve
     - any optional improvements you recommend but did not apply

Important:
- Do not add marketing language.
- Do not soften strong claims.
- Do not optimize for beginner readability.
- Treat this as a durable technical note with a 6–12 month half-life.

Here is the document to edit:

