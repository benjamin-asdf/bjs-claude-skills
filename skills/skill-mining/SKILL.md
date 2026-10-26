---
name: skill-mining
description: Meta operator — mine the user's own Claude Code history for recurring requests, run a layer analysis over them (L0 concrete requests → L1 request classes → L2 unmet need / broken assumption → L3 process gap) and derive new skills, edits to existing skills, or memory rules, each backed by counted instances. Use when asked to "look at my last N conversations", "which skills do I use", "what do I keep asking for", "turn my patterns into skills", "Schichtenanalyse meiner Requests", or to review whether existing skills still earn their place.
---

# Skill Mining

Operator on the user's work history: **requests → classes → needs → skills.**

The bug-layer-analysis applied to a different object. There the object is one defect. Here it
is the stream of things the user had to *say* to Claude. A request the user types again and
again is a symptom: some step was not done without being asked. The question at each level
is the same: what had to be true for the user to have to say this?

## 1. Extract

```bash
python3 ~/.claude/skills/skill-mining/scripts/extract_requests.py 100 <scratchpad>/requests.txt --skip <current-session-id>
```

It prints skill, slash-command and tool counts and sessions per project. Its output file holds
only the user's own messages, with harness noise removed. For more than ~100 KB, split it on
`===` boundaries into ≤ 120 KB chunks, and run one agent per chunk in parallel. Each agent
returns:

1. one line per session: project, goal in ≤ 15 words, skills used;
2. recurring request patterns: name, count, 2–3 verbatim quotes with session id;
3. repeated manual sequences that no existing skill covers (give it the skill list);
4. corrections: what Claude got wrong and the user had to fix.

Ask for quotes, not paraphrase. A pattern without a verbatim instance does not count.

## 2. Layer the patterns

| Level | Question | Example |
|---|---|---|
| L0 | What exactly did the user type? | "did you push", "did we run review verify loop?" |
| L1 | Which request class? | follow-up asking whether a step happened |
| L2 | Which need was not met, or which assumption was wrong? | Claude treats "code written" as done; the user's "done" includes verified, pushed, posted, tracked |
| L3 | Which process or design gap allowed that? | skills cover single steps; nothing owns the end of a work unit |

For each L1 class: count the instances across all chunks (merge near-duplicates across chunk
reports), and name the skill that should have prevented it, or "none". Treat corrections
(§1.4) as their own L1 classes. They show where Claude's priors are off (effort estimates,
risk, scope, complexity, wording), and a skill or memory rule can fix that.

Go up a level only if it groups several L1 classes *and* suggests a countermeasure the lower
level did not. Stop when the next level is a platitude.

## 3. Choose the countermeasure per class

Prefer the cheapest form that makes the request unnecessary:

1. **Edit an existing skill** when the class is a missing step or trigger of one, e.g. a
   mode, a trigger phrase, or a final step.
2. **Memory / CLAUDE.md rule** when it is a single preference with no procedure
   ("never print secrets", "I am Benjamin, not Benni").
3. **New skill** only when there is a multi-step procedure seen in **≥ 3 sessions**, or one
   recurring correction that needs a procedure to prevent it.

Before writing a new skill, run the operator-neighborhood check: does its trigger overlap an
existing description? Is its output checkable? Generic skills go to the public skills repo;
project-specific ones go to that project's skill repo (symlinked into `.claude/skills`).

## 4. Verify

- Recount each claimed frequency by grepping the extract (`grep -c -i '<phrase>'`). Subagent
  counts are estimates.
- Each new skill names the sessions it was derived from (an **Evidence** line) and a deletion
  rule: if it has not been triggered after N sessions, or a bare prompt does as well, delete it.
- Do not repeat secrets, OTP codes or customer data from the transcripts in the output.

## 5. Output

1. A report (in the user's notes or blog directory, user's language): data base (N sessions,
   date range, projects), skill usage table, L1 table (class | count | quotes | covered by),
   the layer table up to L3, and the countermeasure list.
2. The skill files and edits themselves, uncommitted, for the user to review.
3. Proposed memory rules as a list. Write them only after the user agrees.
