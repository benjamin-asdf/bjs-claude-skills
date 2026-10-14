---
name: operator-router
description: Meta operator — given a problem, pick which thinking operator(s) fit (bug-layer-analysis, pre-mortem, assumption-stress-test, decision-matrix, review-verify-loop, operator-neighborhood, …), in what order, and state the choice with its reason before applying anything. Use when asked "which method fits this", "how should I approach this", "welchen Skill nehme ich", or when a problem is stated but no operator is named.
---

# Operator Router

Operator on operators: **choose the move before making it.** Selecting the axis is often
the most consequential step; this makes it explicit and revisable.

Input: a problem statement. Result: a chosen operator or short pipeline, with the reason
and the expected output of each step. Then stop and let the user confirm before running it,
unless they asked for execution.

## 1. Classify the problem

Answer from the problem text and the code, not from the wording:

- **Object:** defect, planned change, decision, assumption, finished diff, unknown territory.
- **Time:** has it happened, or not yet?
- **Question:** why did this happen / what else is affected / what will go wrong / which option / does this claim hold / is this correct?

## 2. Match

| Situation | Operator |
|---|---|
| A concrete bug happened; want its class and siblings | `bug-layer-analysis` |
| A change is planned, risk unknown | `pre-mortem` |
| A claim or invariant is relied upon, truth unknown | `assumption-stress-test` |
| Several designs, one decision | `decision-matrix` |
| A diff exists, correctness in doubt | `review-verify-loop` or `code-review` |
| No fitting operator, or a new one is wanted | `operator-neighborhood` |

If two rows fit, name both and the order. Typical pipelines:

- bug → `bug-layer-analysis` → its L2 assumption → `assumption-stress-test`;
- plan → `pre-mortem` → its L2 assumptions → `assumption-stress-test`;
- design question → `decision-matrix` → chosen design → `pre-mortem`.

If no row fits, say so; do not stretch an operator over a problem it was not built for.

## 3. State the choice

Output, short, in the user's language:

1. Problem classified: object / time / question.
2. Chosen operator(s) and order.
3. Why this one, and why the closest alternative was not chosen.
4. What each step produces and where it is written.
5. The assumption behind the choice. If it is wrong, which symptom would show it
   (e.g. the layer analysis finds no new instances at an upper level).

## 4. Revise on evidence

During a run, if the operator's own output signals a mismatch (an upper level that adds
nothing, a matrix whose rows do not discriminate, a stress test with no falsifiable
claim), say so and re-route instead of finishing the ritual.
