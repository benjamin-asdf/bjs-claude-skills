---
name: done-check
description: Closure operator — before reporting a work unit as finished, walk the full definition of done (seen working in the real running thing, review loop run, committed and pushed, PR/issue/docs updated to the current state, tracking moved, scratch cleaned up, result opened for the user) and either do each open step or list it as open. Use at the end of any implement/fix/deploy task, and when asked "done?", "anything open?", "did we …?", "is everything pushed", "state?".
---

# Done Check

Input: the work unit just finished (issue, PR, post, deploy, experiment). Result: a short
table of the closure steps, each **done** (with evidence), **done now**, **open** (with reason)
or **n/a**.

Evidence: in 100 sessions the user asked "did we/you …?" 14 times in 11 sessions and sent
22 status pings in 17 sessions. Typical ones: "did we run review verify loop?", "did you
push", "did you post the review?", "did we update the blog posts", "did you test s4a on
cad-b?". Each is a step that was skipped and then reported as done.

## The steps

Go through all of them. Skip none silently: write n/a with a reason.

1. **Seen working.** Exercised in the real running thing (running app, deployed env, real
   mail client, phone, headless browser), not only compiled or unit-tested. Say how. If the
   user can see it, also check the exact path they will take: the URL they will click,
   "next page", a second use, other clients.
2. **Reviewed.** If code changed: review-verify-loop run on the final diff, and surviving
   findings fixed or turned into follow-up issues.
3. **Committed and pushed.** `git status` clean, branch pushed, CI on the pushed SHA green
   or watched.
4. **Outward text current.** PR body, issue comment, docs, blog post, README: they describe
   the *current* state (not the path there), link the artifacts, and contain no local paths
   or local-only references. Before/after numbers if it is a fix or a perf change, unless the
   project's outward-text rules keep evidence out of outward text. Then it goes in the report.
5. **Tracking moved.** Issue/board status, release table, superseded PRs marked draft with a
   link, follow-up issues for deferred findings.
6. **Cleaned up.** Throwaway JVMs, test stacks, worktrees of merged branches, temp configs
   holding secrets.
7. **Handed over.** The result is opened for the user (PR in the browser, file in Emacs, the
   page) or its path or URL is the last line of the report.

## Rules

- Do the cheap open steps right away. Ask only for outward-facing ones the user has not
  authorized in this task, such as posting, deploying, merging or re-requesting a reviewer.
- "Done" in the report means all steps are done or n/a. Otherwise say "done except: …".
- Never claim a step without its evidence (command output, URL, SHA, screenshot).

Deletion rule: if after ~20 uses the user still asks "did we …?" about steps this list
covers, the list is not being followed. Fix the trigger, or turn the list into a hook.
