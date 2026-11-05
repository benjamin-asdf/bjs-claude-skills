---
name: go-ahead
description: Go ahead — debug the issue or implement the feature, check the design first, prove it works, review-verify it, then move the issue forward. Use for "go ahead", "take this issue", "debug and fix it", "implement it".
---

# Go ahead

Input: an issue, bug report or feature request. Work it to the point where the next step
is someone else's (review, merge, a product decision).

1. **Understand.** Read the issue and the code it names. For a bug, reproduce it first:
   write a failing test or harness that shows the bug. No fix without a repro.
   For a bug, run `bug-layer-analysis` on it: siblings and the broken assumption shape
   the fix (fix the class, not only the instance).
2. **Check the design before building it.** Pick one:
   - one round of `pre-mortem` on the planned change, or
   - one slim `decision-matrix` (status quo plus 1–3 options, the few criteria that decide).
   Pick the option and say in one line why. Ask only when the choice changes scope.
3. **Implement** on a branch, following the project's own conventions (CLAUDE.md, the
   project's start/branch skill if it has one).
4. **Test harness.** The repro from step 1 now passes; add tests for the new behaviour.
5. **`review-verify-loop`** on the diff until a round has no surviving findings.
6. **Showcase.** Show it working in the real thing with whatever skills the project has
   (run the app, e2e/screenshot showcase, bench, a live REPL check). One piece of evidence
   per claim.
7. **Move the issue forward**, whatever fits the project: a PR (`ship-pr` or the project's
   equivalent), an issue comment with the result, or a follow-up issue. Outward text follows
   the user's outward-text rules. Gates stay: no merges, no shared deploys, no unasked posts.
8. Finish with `done-check`.
