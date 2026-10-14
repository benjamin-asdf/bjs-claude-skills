---
name: decision-matrix
description: Build a decision matrix in Rich Hickey's sense ("Design in Practice") to compare a status quo and alternative designs — criteria as rows, approaches as columns, each cell a short factual aspect of how that approach handles that criterion, with the judgment (good / bad / neutral) kept separate from the fact. Use when asked for a "decision matrix", "Entscheidungsmatrix", "compare designs/approaches/alternatives", "design review against alternatives", or to make a design decision explicit.
---

# Decision Matrix (Rich Hickey, "Design in Practice")

A decision matrix is a thinking tool for making a design decision visible and arguable.
It is not a scoring sheet. Its value comes from forcing every approach to answer every
criterion in writing, so gaps, hidden costs and unexamined assumptions show up.

## Shape

| | **Status quo** (what exists today) | Approach A | Approach B | … |
|---|---|---|---|---|
| *Criterion 1* | aspect | aspect | aspect | |
| *Criterion 2* | aspect | aspect | aspect | |

- **Columns are approaches.** The first column is always the **status quo**, the current
  design. "Do nothing" or "keep it" is a real option and has to be judged like the others.
  Then come the proposed design and genuine alternatives, including the obvious one
  somebody will ask about. Two to five approaches; do not invent strawmen.
- **Rows are criteria.** These are the problems, requirements, qualities and costs that
  matter for *this* decision. They come from the problem statement, not from a generic
  quality list. The first rows are the problem the decision must solve. After that come
  forces such as correctness, simplicity, performance, operability, migration, risk,
  team cost and reversibility. Write each criterion as a short noun phrase. It may carry a
  one-line explanation of what "good" means.
- **Cells are aspects, not scores.** Each cell says in a few words *how* that approach
  handles that criterion, as a fact: "keeps sessions in Redis with a 30-minute
  TTL", not "fast". No numbers out of 10, no weighted sums.
  Concrete numbers, mechanisms and file references are welcome when they are known.
- **Judgment is separate from fact.** Mark each cell as good, bad, neutral/unclear, or
  not applicable, with colour or a symbol (✓ / ✗ / ~ / –). The cell text stays neutral,
  so a reader can disagree with the judgment without arguing about the facts.
- **Empty or "unknown" cells are findings.** They show what was not investigated.
  Either fill them by investigating, or leave them visibly as "unknown" in the open
  questions.

## Process

1. **State the problem** in one or two sentences above the matrix: what decision, why
   now, what goes wrong without it.
2. **Collect criteria** from the problem, the requirements and the known pain points.
   Separate *problem criteria* (does it solve the problem?) from *force criteria* (what
   does it cost or risk?).
3. **Collect approaches.** Status quo first, then the proposal, then real alternatives.
   For each, write a one-line description below the matrix.
4. **Fill every cell with evidence:** code, measurements, docs, issues, history. Mark
   assumptions as such.
5. **Judge each cell** with the colour or symbol, separately from the text.
6. **Read the matrix by row and by column.**
   - Rows where all approaches are equal do not discriminate, so collapse them.
   - Rows where only one approach is good are the reasons for the decision.
   - Columns with a "bad" in a must-have row are out, however good the rest is.
7. **Write the decision and its trade-offs** under the matrix: which approach, which
   "bad" cells we accept and why, and what would change the decision.

## Output

- Markdown or HTML table. For HTML, use `✓` / `✗` / `~` with a coloured cell background
  that works in light and dark themes.
- Below the table:
  - a short description of each approach;
  - the decision, the accepted trade-offs and the open questions (unknown cells);
  - sources for the facts.
- Keep the cells short (≤ ~15 words). Detail goes into footnotes or the text below.

## Pitfalls

- **Scoring and summing.** That hides the reasoning the matrix exists to expose.
- **Leaving out the status quo, or making it a strawman.**
- **Criteria that only fit the preferred approach,** chosen to make it win.
- **Cells that are judgments** ("better", "simple") instead of aspects.
- **Mixing levels,** for example "uses Redis" (mechanism) next to "is maintainable"
  (quality) as rows. Prefer criteria at the level of the decision.
