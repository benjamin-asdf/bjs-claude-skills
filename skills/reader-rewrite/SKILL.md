---
name: reader-rewrite
description: Translation operator — rewrite a result (analysis, PR body, issue comment, design doc, perf report) for one named reader (colleague in chat, reviewer, business/stakeholder, customer, public blog, paper authors) by applying fixed rules - current state not history, written-out names, URLs not ids, no local references, the reader's question first, length that fits the channel. Use for "write it up for my colleagues", "so I can paste it in Teams/chat", "for business", "external guide", "less terse", "make it shorter", "remove the history", or before posting any outward text.
---

# Reader Rewrite

Input: a text or a finished piece of work, and the reader. Result: one text for that reader,
ready to paste, in the reader's language.

Evidence: 28 messages in 17 sessions asked for a write-up, comment or guide for someone else.
The corrections repeat: "die brauchen keine implementation histories, sondern den stand",
"instead of uuids, urls", "written out names for alternatives instead of 'C', 'E'",
"'read-full-app' doesn't mean anything for them", "public facing text should not refer to
local work", "a bit less terse because it is hard to understand", "just in bullet points",
"make it shorter".

## 1. Name the reader and their question

One line each: who reads it, what they will do with it (decide, test, review, merge, learn),
and what channel it goes into (chat message, GitHub comment, PR body, HTML guide, blog).

| Reader | Their question | Shape |
|---|---|---|
| colleague in chat | what happened, what do I do | ≤ 8 bullets, pasteable, links |
| reviewer | what changed, why, how was it checked | PR body: summary, decisions, verification, before/after |
| business | what does the user feel, how much better | per user action (open designer, next page …), before → after, monospace bars; technical details collapsed |
| tester / customer | how do I try it | numbered steps with real URLs and accounts, expected result per step |
| public / blog | what is the idea, how sure are you | claims with their support, no internal names, an AI attribution line where the user requires it |
| paper authors | what is wrong, how sure | polite errata list, each with evidence |

The project's own outward-text rules (CLAUDE.md / CLAUDE.local.md: length limits, language,
attribution footer, what must stay out) override this table.

## 2. Apply the rules

1. **Current state, not history.** Cut "first we tried X, then Y". Keep a rejected
   alternative only if the reader would otherwise propose it again, in one line.
2. **Names, not codes.** Write out what "C", "E", "approach 3", internal function names and
   branch names mean, or drop them. Use clickable URLs instead of UUIDs, issue numbers and
   local paths.
3. **No local references** in outward text: no `/home/…`, no `notes/…`, no "our local
   branch", no artifacts the reader cannot open. If needed, bundle or attach them.
4. **Numbers exact,** with their baseline and conditions. No rounding up of speedups.
5. **Their question first.** The answer or the action comes in the first two lines.
6. **Length** fits the channel. A chat message must not need scrolling.
7. Follow the user's style rules from CLAUDE.md, e.g. language, no gendering, name.

## 3. Check

Read it once as that reader with no context from this session. Every term they would have
to ask about gets explained or removed. Every link must resolve. Run `claim-check` if the
text makes factual claims that go public.

Hand over the text in a form that can be pasted: a fenced block, or opened in Emacs or the
browser. Post nothing without the user's go.
