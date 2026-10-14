---
name: assumption-stress-test
description: Attack one stated assumption or invariant by generating concrete cases that would break it, running them, and reporting which hold and which break. The downward counterpart of bug-layer-analysis (abstract claim → concrete instances). Use when asked for an "Annahmen-Sturmtest", "stress test this assumption", "does this invariant really hold", "try to break this", or to test an L2 assumption from a layer analysis or pre-mortem.
---

# Assumption Stress Test

Operator: **Schichtenanalyse run downward.** `bug-layer-analysis` climbs from an instance to the
assumption; this descends from the assumption to instances chosen to violate it.

Input: one assumption, e.g. "evaluation is a pure function of (document, inputs)", "this id is
always set", "the migration has run before this code". Result: a table of attack cases with
observed outcomes, and the assumption restated at the strength it actually holds.

The value is in cases chosen to **break** the claim, not to illustrate it.

## 1. Make the assumption checkable

- Write it as one sentence with a quantifier: *for all X in S, P(X)*.
- Name S (the domain it is claimed over) and P (what must hold).
- If it cannot be falsified by any observation, it is not an assumption yet; sharpen it or stop.

## 2. Find the boundary of S

List where the claim's domain has edges or holes. Walk, do not recall:

- inputs at the limits (empty, nil, maximal, duplicate, unicode, negative, out of order);
- callers and entry points that bypass the usual path;
- environment and configuration variants;
- state: first run, repeated run, concurrent run, run after partial failure;
- anything the claim depends on that someone else can change.

## 3. Generate attack cases

For each boundary, write the smallest concrete case that would violate P if the assumption
were false. One case per row: input/state, expected-if-true, how to run it (command, test,
REPL form). Prefer many cheap cases over one elaborate one.

## 4. Run them

Run every case that can run now. Record the *observed* outcome. Do not predict outcomes.
Cases that cannot run go in an *unrun* list with the reason.

Respect the project's resource rules for running tests (memory caps, one heavy process at a time).

## 5. Restate the assumption

- All cases hold: the assumption survives *these* cases; say which boundaries were attacked
  and which were not.
- Some break: each breaking case is an instance; feed it into `bug-layer-analysis` as L0,
  and restate the assumption with the exception it needs.

## 6. Output

`notes/<ticket>/stress-<slug>.md` (or the notes directory the project's CLAUDE.md names) in the user's language:

1. The assumption, S, P.
2. Table: boundary | case | expected-if-true | observed | status (held / broke / unrun).
3. The assumption restated, with its known exceptions.
4. Unattacked boundaries.

"Held" means held under these cases, never "is true".
