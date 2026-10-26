---
name: dev-cycle
description: The full development cycle for one work item, run end to end on a single go — intake → branch → implement → seen working → review-verify-loop → ship → feedback → merge-ready → close — with a state file, a one-line status at each stage change, and stops only at fixed gates (merge, shared deploys, unauthorized outward posts, open product decisions). Abstract version; a project skill (e.g. nc-dev-cycle) maps the stages to concrete commands. Use for "do that", "do the cycle", "go ahead with the whole thing", "implement and ship it", "take it from issue to PR", "mach den ganzen Zyklus".
---

# Dev Cycle

Input: one work item (issue, bug, feature, post, experiment) and the go. Result: the item
taken through every stage up to the next gate. Then a short report, and the state file
pointing at the next stage.

**"Do that" / "go ahead" means: run all stages, don't ask between them.** Stop only at a gate
(§ Gates). A question that is not a gate gets the most obvious answer. The assumption is
noted in the state file and the report, and the work goes on.

Derived from `skill-mining` over 100 sessions. The user asked for each of these steps by hand,
again and again ("implement, review verify loop, then pr", "did you push", "open the pr",
"state?").

## State

Keep `<notes>/<item>/cycle.md`, where `<notes>` is the project's notes dir, by default
`notes/` or whatever CLAUDE.md names. One line per stage: `stage | status | evidence | date`.
Add assumptions and open questions. Update it at every stage change. It lets you answer
"state?" from the file, and lets a later session resume the cycle.

At every stage change, write one status line in the chat: `[stage n/9] <stage>: <result>`.

## Stages

1. **Intake.** Read the item and its thread. Restate the goal in one sentence and define its
   scope (what is out). List the assumptions you make and the open questions, each with a
   recommended answer. If the item is too vague to start, go to the gate *open decision*.
   Otherwise go on with the recommended answers.
2. **Branch.** Use a fresh branch or worktree off the right base (project skill says which).
3. **Implement.** Choose the simplest design that does the job. Before writing much code,
   check it: no complecting of concerns, and nothing beyond scope. Estimate in agent time
   (see memory). Add tests for the behavior. Commit in coherent steps.
4. **Seen working.** Run it in the real running thing, along the path a user takes, headless.
   If something is wrong, go back to 3. Bugs found here are worth a `bug-layer-analysis`
   only if they are surprising.
5. **Review.** Run `review-verify-loop` on the whole branch against its base. Fix the
   survivors. Findings that are valid but out of scope become follow-up items.
6. **Ship.** Push. Open the PR, or publish to staging, with outward text per the project's
   rules (`reader-rewrite`). Watch CI and move tracking.
7. **Feedback.** If reviewers or testers respond: `address-review` and the project's handoff
   skill. Loop 3–6 as needed.
8. **Merge-ready.** Bring the branch up to date with its base, compile and test the merge
   result, and report "ready". **Gate: the user merges.**
9. **Close.** After the merge: bookkeeping (release table, board, linked issues),
   cleanup (worktree, processes), and `done-check` over the whole item.

Skip a stage only when it does not apply (no reviewer feedback yet, so 7 is skipped). Say
"n/a" in the state file.

## Gates: stop and ask here, nowhere else

- **Merge** into a shared branch. The user always does this.
- **Deploy** to an environment that is not explicitly the user's, or to anything prod-like.
- **Outward posts the user has not authorized in this task:** comments to customers or
  external people, re-requesting a reviewer the user did not name, closing others' items.
- **Open decision:** product or scope choices with no obvious default, a reviewer conflict,
  or a disagreement with a review comment.
- **Resources:** a step needs more memory/disk than the safety margin allows, or secrets
  the user must type (OTP).

At a gate: write the question with your recommendation into the state file, report, and stop.
Independent work that does not depend on the answer may continue.

## Report at the end of a run

1. Stage reached, and the gate it stopped at (or "closed").
2. Evidence per stage (SHAs, CI run, PR URL, screenshots, numbers), from the state file.
3. Assumptions made and follow-ups created.
4. The one thing needed from the user.

Open the main result (PR, page) for the user.
