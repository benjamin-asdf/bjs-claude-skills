---
name: operator-neighborhood
description: Meta operator — take one thinking operator (a skill, a heuristic, a method) and span the space it lives in: decompose it into axes, locate it, mark the occupied points, and derive free neighbor operators by varying one axis at a time. Use when asked for "Nachbarschaftssuche", "what other skills are there like this", "map the space of this skill", "which operators are missing", or when designing a new skill from an existing one.
---

# Operator Neighborhood

Operator on operators: **Instanz → Achsen → Nachbarn.**

Input: one thinking operator (a skill file, a named heuristic, a procedure). Result: its
axes, its position, the occupied neighbors, and free neighbors worth building, each with a
sketch of what it would do.

## 1. Decompose the operator

Read the operator in full. Fill in, in one line each:

- **Object:** what it is applied to (defect, decision, diff, design, code region, goal).
- **Move:** the cognitive operation (generalize, specialize, compare, refute, trace, compress, invert).
- **Direction in time:** backward (what happened) or forward (what will happen).
- **Direction in abstraction:** upward, downward, or lateral.
- **Stance:** constructive, falsifying, comparing.
- **Coverage:** which axis it sweeps completely (levels, alternatives, timeline, causes).
- **Output form:** document, table, test, decision.

Add axes if the operator needs them. Do not force these defaults onto it.

## 2. Locate the occupied points

List the existing operators (installed skills, known heuristics, e.g. Pólya's) and place
each on the same axes. A table: operator | object | move | time | abstraction | stance.
Read every candidate's description; do not place from the name.

## 3. Vary one axis at a time

For each axis, flip or shift only that axis and ask: does an operator at that point exist?

- occupied → note it as neighbor;
- free and meaningful → sketch it (name, input, steps in one line each, output);
- free and meaningless → say why, so the point is not re-proposed.

Also try pair moves: two axes flipped together, and compositions (operator A's output as B's input).

## 4. Check the proposal

For each free neighbor:

- Does it tell you to do something the nearest occupied operator does not? If not, it is the
  same operator under a new name; drop it.
- Is its output checkable (a test, a grep, a run), or only fluent text?
- Would its trigger description overlap with an existing skill's? Name the overlap and how
  to separate them.

## 5. Output

`notes/<topic>/neighborhood-<operator>.md` (or the notes directory the project's CLAUDE.md names) in the user's language:

1. Axes and the operator's position.
2. Table of occupied neighbors.
3. Free neighbors: name, one-line purpose, input, output, overlap risk.
4. Recommendation: which one or two to build first, and why.

Build nothing here. Writing a skill is a separate step.
