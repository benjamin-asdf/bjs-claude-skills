---
name: claim-check
description: Falsifying operator for prose — list every checkable claim in a text (blog post, paper, design doc, PR description, issue comment), send one verifier agent per claim against the primary source (paper, code, data, run), and return a verdict table plus an errata list and the corrected text. The prose counterpart of review-verify-loop. Use for "check the claims", "do they hold", "is this novel", "check the paper", "errata", "prüf die Studien mit Verifier-Agents", or before publishing or sending a text.
---

# Claim Check

Input: one text, plus where its sources are (paper PDFs, repo, data, URLs). Result: a table
claim → verdict → evidence, an errata list, and the text with the fixes applied.

Evidence: 11 messages in 8 sessions, mostly in research and blog sessions: vector-symbolic-clj
("make a list of claims it makes. do they hold", "check the errata"), joshi-2025 ("write up of
the errata we found"), the skills blog post ("prüf die Studien mit Verifier-Agents"), an errata
email to paper authors. Overclaims were corrected by the user ("7.7 is not 10-20x").

## 1. Extract claims

Number every sentence that could be false. Keep its exact wording and location. Kinds:

- **cited:** "X showed Y" — check against X itself, not a summary of X;
- **numeric:** speedups, counts, percentages — check against the run or table that produced them;
- **code:** "the implementation does Y" — check against the code at `file:line`;
- **novelty:** "nobody has done Y" — needs a related-work search; at best it is "not found";
- **inference:** "therefore Y" — check that the premises above support it.

Skip opinions and framing. Do mark hedges that hide a claim ("probably", "it seems").

## 2. Verify, one agent per claim

Each verifier gets the claim, its kind and the sources, and must return one of:
**holds** (with quote or output), **overstated** (what does hold), **wrong** (what is true),
**unverifiable** (what was tried). It does not see the other claims. Run them in parallel.
Batch claims of the same kind on the same source only when there are more than ~15.

For numeric and code claims, rerun the measurement or read the code. Do not just re-read the prose.

## 3. Refute the verdicts

For every **holds** on a cited or novelty claim, a second agent tries once to find the
counter-source. For every **wrong**, it checks whether the verifier misread the source. Keep
the surviving verdict.

## 4. Output

1. A table: # | claim (short) | kind | verdict | evidence (quote, `file:line`, URL, output).
2. Errata: each non-holding claim with the corrected sentence. If the text is someone else's
   (a paper), write the errata as a polite list for its authors.
3. The text with the corrections applied, unless told only to report. A number gets its exact
   value or is removed. Weaken a claim only when the evidence supports the weaker one.

A text whose claims all hold is a valid result. Do not invent findings.
