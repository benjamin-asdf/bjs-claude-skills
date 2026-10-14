---
name: review-verify-loop
description: Adversarial code review — one reviewer agent proposes candidate findings, one verifier agent per finding tries to refute it, surviving findings get fixed, repeat until a round produces no survivors. Use for "review-verify loop", "adversarial review", "review my branch and verify the findings", or before merging a non-trivial diff.
---

# Review / Verify Loop

Input: a branch (default: current) and its base. Result: a diff whose findings have each
survived an attempt to refute them, and are fixed.

The point is the refutation step. A single reviewer pass produces confident-sounding findings
that are often wrong — the code already handles the case, the call is unreachable, the line is
someone else's from three months ago. Verifiers kill those before they cost an edit.

## Project constraints come first

Before spawning any agent, read the project's own rules (CLAUDE.md, CLAUDE.local.md, a
project skill or addendum for this loop) and extract:

- **Base branch** — how to find it.
- **Resource limits** — whether agents may run builds/tests/JVMs at all, and the cap if so.
  Default when unknown: agents read code only; you run tests yourself, once, after fixes.
- **Legitimate finding sources** — project rules a reviewer may cite (comment discipline,
  logging in catch blocks, i18n, style).
- **Explicit non-findings** — e.g. missing e2e coverage on feature branches.
- **Test command** for the fix step.

Put the relevant ones into every agent prompt. Agents do not see your context.

## 0. Scope

```bash
BASE=<base from project rules, else origin/main or origin/master>
git diff --stat $BASE...HEAD
```

Everything below reviews `$BASE...HEAD` (three dots — the branch's own commits, not the base's).

## 1. Reviewer agent

One agent. It returns CANDIDATE findings, not conclusions.

Every finding must carry a `file:line`, a one-sentence claim, a concrete FAILURE scenario
(specific input/state → specific wrong outcome) and the EVIDENCE that shows it. A finding
without a failure scenario cannot be verified or refuted, so it is not a finding — reject it
and make the reviewer redo it.

Tell the agent, explicitly, in the prompt:

- **No heavy processes** unless project rules allow them (no builds, test runs, JVMs, dev
  servers). Reading code is the job. Native linters are fine.
- **No edits.** Review only.
- The project rules that are legitimate finding sources, and the explicit non-findings.
- **Only lines this branch touched** — `git blame` first; a pre-existing line is not a finding.
- What the feature is *supposed* to do, in enough detail that "does not match spec" is
  checkable. Without this the reviewer invents a spec.

## 2. Verifier agents

One agent **per finding**, in parallel, in a single message (respect any project cap on
concurrent agents). Each gets that one finding and nothing else — a verifier that sees the
whole list starts agreeing with the list.

Their job is to **refute**, not to confirm. Frame it that way: "here is a claim another
reviewer made; find the reason it is wrong." A verifier that cannot find one has confirmed it.

Same constraints as the reviewer. Each returns exactly one verdict:

- `REFUTED` — with the specific reason (guard exists at X, path unreachable because Y,
  `git blame` says the line predates this branch, the framework already does it)
- `CONFIRMED` — with the mechanism restated concretely enough to fix from
- `WEAKER` — real but smaller than claimed (e.g. cosmetic, not the claimed crash); it survives
  at the reduced severity

Verifiers are not always right either. When a verdict turns on a claim you can check cheaply
yourself (a `git blame`, a grep for the guard it says exists), check it. Prefer the evidence
over the verdict.

## 3. Fix

Fix CONFIRMED and WEAKER findings. Drop REFUTED ones — and say in the final report what was
dropped and why, because "the reviewer raised it and it was wrong" is information.

After fixing, run the affected tests yourself, once, with the project's resource caps.
Never let the agents do this.

## 4. Loop

Re-run from step 1 against the *updated* diff. Fixes introduce findings — that is the whole
reason this loops rather than running once.

Stop when a full round yields no surviving findings. Two to four rounds is typical; if
survivors keep appearing past round four, the branch may have a structural problem and that
is worth saying out loud while continuing.

Cap the loop at eight rounds. Report what is still open instead of looping silently.

## 5. Report

Per round: candidates raised, refuted (with reasons), survived, fixed. Then the test result.

The refuted list is the most useful part of the output — it is what stops the same wrong
finding being raised again by the next reviewer.

## What this loop actually catches

- **Fixes relocate bugs.** A timer moved from a component into the event layer stopped leaking
  and immediately started starving a different consumer's queue. Round 2 exists to catch
  round 1's fix.
- **Verifiers disagree across rounds.** The same finding can be called benign in round 1 and
  re-raised with a stronger argument in round 4. When that happens, prefer the one with the
  concrete mechanism, and say in the report that it was contested.
- **A reviewer's severity is usually one step too high.** Most "high" findings come back WEAKER
  because another part of the branch already covers the user. Verify before fixing; the fix
  is the expensive part.
- **Check the compiler, not just the tests.** A fix can introduce compiler warnings (e.g.
  type-inference warnings) that no test and no linter sees. Query the build tool's warning
  output and compare against the base: a warning only in your build is yours.
