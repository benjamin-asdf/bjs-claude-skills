---
name: pre-mortem
description: Forward-looking failure analysis of a planned change, design or feature — assume it has already failed, enumerate the failure causes, generalize them by level (mechanism class → broken assumption → process gap) and turn each into a check made before shipping. The forward counterpart of bug-layer-analysis. Use when asked for a "pre-mortem", "Pre-Mortem", "what could go wrong with this", "how will this fail", or before merging/deploying a risky change.
---

# Pre-Mortem

Operator: **Schichtenanalyse with the time arrow reversed.** `bug-layer-analysis` starts from a
failure that happened; this starts from one that has not happened yet, and states it as if it had.

Input: one planned change (diff, design, ticket, deployment plan). Result: failure causes
found *before* the fact, each with a check that can be run now.

The value is in the failure being stated as a **fact in the past tense** ("it broke because …").
"What could go wrong" produces a list of worries; "it failed, why?" produces causes.

## 1. Pin the object

- One sentence: what changes, for whom, where it runs.
- The success condition: what must hold afterwards. A failure is a violation of this.
- The blast surface: components, data, callers and environments the change touches.
  Read the diff or design; do not work from the title.

## 2. Declare the failure

Write: "It is [date + horizon]. The change failed. [The concrete observable symptom]."
Pick the worst *plausible* symptom per surface: wrong data stored, divergence between two
sides, outage, silent wrong result, security. Several declarations are fine, one per surface.

## 3. Enumerate causes (L0)

For each declared failure, list the concrete causes that would produce it. Each cause must be
a specific mechanism pointing at code, data or configuration (`file:line` where it exists),
not a category. Sources to walk, not to recall:

- every caller / consumer of the touched code;
- every environment difference (dev vs test vs prod, config, data volume, versions);
- every ordering and concurrency path;
- every input class the code never saw before;
- everything the change assumes about code it does not own.

## 4. Generalize (L1 → L3)

Same ladder as `bug-layer-analysis`, forward:

| Level | Question |
|---|---|
| L1 | Which mechanism class do these causes share? Search the change for *more* members. |
| L2 | Which assumption, if wrong, makes the whole class fail? State it as a checkable claim. |
| L3 | Which gap in our process would let that go unnoticed (no test, no review step, no monitor)? |

An upper level must surface causes the lower one did not. Otherwise merge it.

## 5. Make each cause cheap to check

For each cause or class, give the cheapest check that can run **now**: a test, a grep, a
query against real data, a dry run, a monitor alert. Mark each: *checked-ok*, *checked-found*,
*unchecked*. Run the cheap ones; do not claim a cause is excluded without a run.

An L2 assumption that should be attacked systematically goes to `assumption-stress-test`.

## 6. Output

`notes/<ticket>/pre-mortem-<slug>.md` (or the notes directory the project's CLAUDE.md names) in the user's language:

1. Object, success condition, blast surface.
2. Table: declared failure | cause (`file:line`) | class | check | status.
3. Assumptions (L2) with the check that would falsify each.
4. Open items ordered by blast radius × (1 − confidence it is excluded).

Keep it factual. A cause without a check is a worry, not a finding; list it as *unchecked*.
