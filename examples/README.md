# Examples

Sample `REQUIREMENTS.md` files you can run the kit against — useful for trying THROUGHLINE
on something disposable before pointing it at real work, and for recording a walkthrough.

| Sample | What it is | Language |
|---|---|---|
| [habit-tracker/](habit-tracker/REQUIREMENTS.md) | A static single-page habit tracker (HTML + CSS + JS, localStorage, no build) | English |
| [habit-tracker/](habit-tracker/REQUIREMENTS.ko.md) | Same sample, Korean | 한국어 |

Both versions describe the same project. Use the one that matches the kit you copied —
`en/THROUGHLINE` with `REQUIREMENTS.md`, `ko/THROUGHLINE` with `REQUIREMENTS.ko.md`.

## How to use one

```bash
mkdir my-demo && cd my-demo && git init
cp -r <THROUGHLINE repo>/en/THROUGHLINE ./THROUGHLINE          # or ko/THROUGHLINE
cp <THROUGHLINE repo>/examples/habit-tracker/REQUIREMENTS.md \
   THROUGHLINE/SOURCES/REQUIREMENTS.md                          # or REQUIREMENTS.ko.md
```

Then paste the [initialization prompt](../README.md#2-one-time-only-project-initialization-prompt)
into your agent, and the [development prompt](../README.md#5-prompt-to-start-actual-development)
once it finishes.

## What each sample is built to exercise

A sample is only useful if it makes the framework's mechanisms visible. Every sample here is
seeded with three things on purpose:

1. **Deliberate ambiguity** — questions the requirements do *not* answer, so the agent stops and
   asks instead of guessing ([KICKOFF §3](../README.md#3-when-requirements-are-ambiguous-at-the-initialization-step)).
2. **A cross-cutting contract** — rules that span more than one feature, so `ARCHITECTURE.md`
   has real content rather than boilerplate.
3. **A pinned decision** — one policy stated as fixed, recorded during initialization, that a
   later change request can plausibly contradict. This is what lets you see the conflict check
   fire in a later session rather than take it on faith.

### habit-tracker

- **Ambiguity**: when does a "day" start (midnight or 4am)? can you back-fill a past date?
  Both are left unanswered in §13 and both change the data model, so the agent should ask.
  Habit-count limit is marked `[AI-delegated]` / `[AI 위임]` — non-core, so it gets decided
  silently and logged to `ASSUMPTIONS.md` instead.
- **Cross-cutting contract**: local-timezone `YYYY-MM-DD` date keys, a single versioned
  localStorage key, one-way `state → save → render` flow, and shared name validation.
- **Pinned decision**: *"a single missed day resets the streak to 0 — no grace day."*
  Later in the session, ask for `"I forgot yesterday — make it still count if I do it today"`
  (`"어제 깜빡했는데 오늘 하면 이어지게 해줘"`).
  That contradicts the recorded decision, so the agent should surface
  the conflict and ask whether you are knowingly overriding it — rather than quietly
  implementing it and leaving the spec and the code disagreeing.
- **Persona review**: streak semantics at the midnight boundary is genuinely contentious
  (timezone, DST, back-fill interaction), so it should trigger a multi-persona review and
  leave a log under `discussion/`.
