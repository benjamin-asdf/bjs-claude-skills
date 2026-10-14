---
name: bug-layer-analysis
description: Layered generalization analysis of one concrete bug — list the bug and its blast radius, find its siblings, then generalize the kind of error level by level (L0 concrete → L1 mechanism class → L2 broken assumption → L3 process/design gap), naming at each level the mistake we made that let it through, its blast radius and a countermeasure. Use when asked for a "Schichtenanalyse", "generalize this bug", "what kind of error is this", "blast radius of this bug and its class", or a post-mortem of a single defect.
---

# Bug Layer Analysis

Input: one concrete bug (a repro, a failing case or a finding). Result: one document that goes
from that bug to the class of bugs it belongs to. Each layer is backed by verified instances
and ends in a countermeasure. Fixing the bug is a separate step; this analysis decides
*what else* to fix and *how to stop the class*.

The value is in the generalization being **checked**. A layer that only restates the one
known bug in more abstract words is useless. Every layer must have been used to *search*
for further instances, and every claimed instance must have been verified.

## 0. Pin the concrete bug (L0)

- **Symptom:** the exact input, the observed result and the expected one. Include a one-line
  repro command or test.
- **Mechanism:** the precise causal chain, with `file:line` for each link.
- **Blast radius:** every place where the symptom shows up or could show up. List them as
  components, features or code paths, each with how bad it is there (wrong result shown, wrong
  data stored, divergence between two sides, cache poisoning, security). Verify each entry:
  run it, grep the call sites, read the code. Mark anything unverified as such.

## 1. Find the siblings (L1: same mechanism)

Name the mechanism without the specific identifier. For example, "the sandbox realm reads
the host clock" becomes "expressions can observe ambient host state". Then enumerate *every*
member systematically, not from memory:

- Walk the relevant surface: all globals and built-ins, all host imports, all library
  functions, all call sites of the primitive.
- Check each candidate with a test or a repro, not by reasoning alone.
- Each confirmed sibling gets its own blast radius.

A sibling that cannot be confirmed goes into an "unverified" list with the reason.

## 2. Generalize upward (L2, L3, …)

At each level ask: *what had to be true for the level below to happen, and what else does
that allow?* Typical progression:

| Level | Question | Example |
|---|---|---|
| L0 | What exactly broke? | `new Date()` in an expression returns the wall clock |
| L1 | What mechanism class? | ambient host state (clock, randomness, timezone, locale) is observable from the realm |
| L2 | Which assumption/invariant was broken? | "evaluation is a pure function of (document, inputs)" was claimed but never enforced at the boundary |
| L3 | Which design or process gap allowed it? | invariants written in prose and design docs without a test or construction that enforces them; the sandbox was designed around capabilities (escape), not observability (determinism) |

For **every** level write:

- **Kind of error:** one sentence, no specific identifiers above L0.
- **Instances:** concrete ones found by searching *with this level's description*, each with
  `file:line` and a verified or unverified mark. An upper level must surface instances the
  lower one could not; otherwise it is not a real level, so merge it.
- **Blast radius at this level:** what is at risk across the whole class, not just the known
  instance.
- **Our mistake:** what *we* did or assumed that let this level's error through. Be concrete:
  which decision, which missing test, which review step, which claim written without
  evidence. Name decisions, not people.
- **Countermeasure:** the cheapest thing that makes the whole level impossible or detectable.
  Prefer construction (the design cannot express the bug) over a test, a test over a lint,
  and a lint over a checklist. Say where it lives.

Stop when the next level becomes a platitude that suggests no new search and no new
countermeasure. Usually that happens after 3–4 levels.

## 3. Verify the analysis

Before writing it up, try to refute it, in the spirit of the review-verify loop:

- Is each sibling really a member of the class, or a different mechanism?
- Does each countermeasure really cover the level, including the siblings?
- Is the "our mistake" entry an actual decision visible in the history (commit, design doc,
  test gap), or a guess? Check with `git log -S`, the design notes and the test files.

## 4. Output

Write `notes/<ticket>/bug-layers-<slug>.md` (or the notes directory the project's CLAUDE.md names) in the user's language. Structure:

1. L0: symptom, repro, mechanism, blast radius table.
2. One section per level: kind of error, instances table (`file:line`, verified?, blast radius),
   our mistake, countermeasure.
3. A summary table with one row per level: level | kind of error | our mistake |
   countermeasure | status (done / open, with commit hash if done).
4. Open items, ordered by blast radius.

Keep it factual. No narrative, no blame, and no claims without a check behind them.
Outward-facing versions (issue, PR) follow the repo's outward-text rules and stay short.
