# ASK-solo DriftBench — Stage-1 pilot RESULTS v2 (seed1, `miniquery`, value-restoration)

Run date: 2026-06-29 · dev-agent: orchestrated Claude sub-agents · Orchestrator: Claude Code
Scope: **1 task · 4 groups · seed1 · 7 sessions (s0–s6) = 28 dev-agent sessions.**
v2 redesign of the v1 task (see `v1_ceiling/RESULTS.md`), which ceilinged because the scored
decision leaked into code docstrings. This is a **go/no-go discrimination pilot**, not a powered result.

## Headline — DISCRIMINATION ACHIEVED

The task now separates the groups on the decisive memory event (S6 = "restore the default page
size to its original S1 value"). The original value (**7**) was overwritten twice (→25 at S3, →40
at S5) and, under a uniform "no change-history in code comments" coding norm, survived **only in a
memory artifact**. Result at S6:

| Group | memory regime | S6 default set | target 7? |
|---|---|---|---|
| **ASK-solo** | structured SSOT (DECISIONS append-only) | **7** | ✅ restored |
| **P-notes** | free notes, ~2600-char cap | **7** | ✅ restored |
| **B-limited** | last 2 sessions' notes, 600-char cap | **25** | ❌ wrong value |
| **B-code** | no memory | **10** | ❌ guessed |

Trajectory (`default_ok` = default page size correct for that session):

```
            S0  S1  S2  S3  S4  S5  S6
ASK-solo    --  OK  OK  OK  OK  OK  OK     (6/6 at S6, inv_viol 0)
P-notes     --  OK  OK  OK  OK  OK  OK     (6/6 at S6, inv_viol 0)
B-code      --  OK  OK  OK  OK  OK  XX     (5/6 at S6, inv_viol 1)
B-limited   --  OK  OK  OK  OK  OK  XX     (5/6 at S6, inv_viol 1)
```

(Raw: `runs/<group>/seed1/scores.jsonl`, `runs/aggregate.json`.)

## What each group did at S6 (with self-reported reasoning)

- **B-code** set `10` and **honestly flagged it as a guess**: *"this value was inferred rather than
  recovered from history — no in-sandbox source preserved it."* (zero memory → cannot restore.)
- **B-limited** confidently set `25` — its 2-session window (S4 sort note + S5 "25→40" note) made it
  believe the *pre-S5* value (25) was the original. The true original (7) was 5 sessions back, outside
  the cap. **This is the dangerous failure mode: a silent, confident restoration to the WRONG value.**
- **P-notes** set `7`, tracing its free-form note lineage "7 → 25 → 40".
- **ASK-solo** set `7`, tracing the DECISIONS lineage D5(7)→D7(25)→D9(40), then recording D10 (restore).

## Why v2 discriminates where v1 did not

- **v1** changed a policy once and the dev agent documented "was KeyError" in the module docstring, so
  even the memoryless B-code recovered it from its own code → ceiling.
- **v2** (a) overwrites the original value **twice** so it is no longer in the current code, and
  (b) applies a uniform, realistic norm — *history lives in the memory artifact / version control, not
  in code comments*. The original therefore survives **only** for groups whose memory artifact retained
  it. Memory became necessary, so the groups separated.

## Interpretation (honest)

1. **Memory of the original decision is necessary** — the two groups without it (B-code, B-limited)
   failed; the two with it (P-notes, ASK-solo) succeeded. The benchmark now measures the intended thing.
2. **Lossy memory is not just weaker — it can be actively misleading.** B-limited didn't fail to answer;
   it restored a *plausible wrong value* (25) with confidence. A bounded window that drops the original
   produces silent drift, which is harder to catch than an admitted "I don't know" (B-code).
3. **Structure (ASK-solo) vs disciplined free notes (P-notes) did NOT separate here** — both retained the
   lineage and restored 7. This mirrors the prior B3 finding (memory effect clear; structure-vs-notes not
   separated at small scale). **This pilot demonstrates the memory-retention effect, not yet the ASK
   structural effect.**

## Go / no-go verdict (review §6.6)

**GO** (the task discriminates): B-code/B-limited fail the late invariant while memory-bearing groups
pass — no ceiling, no floor. The harness + task are ready to scale on the **memory dimension**.

To additionally isolate the **structural** advantage of ASK-solo over P-notes (the actual ASK claim),
the next iteration must create conditions where *free notes lose the decision but structured SSOT keeps
it* — e.g., many competing decisions saturating P-notes' capped budget, or a longer horizon where
free-form notes get re-summarized lossily while an append-only DECISIONS doc does not. As designed, at
this scale a disciplined note-taker matches SSOT.

## Honest scope / limitations

- **1 seed.** B-limited's "25" and B-code's "10" are single-seed point outcomes; the *direction*
  (no-memory/lossy fail, retained-memory pass) is clear, but magnitudes need **≥3 seeds**.
- The decisive metric is a single value-restoration event; a fuller run would include several such
  events plus cross-cutting invariants.
- P-notes retained the original partly because the agent kept a compact lineage; a noisier or longer
  task could push it out of the cap — that is exactly the ASK-vs-P-notes test deferred above.

## Harness validity

Stage -1 self-test (`eval/_selftest.py`) GREEN: the battery passes the reference (default restored=7)
and catches the negative control (left at 40). Oracle isolation held (agents sandboxed to `work/`,
never saw `eval/`). 28 sessions ran clean (no chain deaths, no import errors).

## Reproduce

```
cd benchmark/benchmark-solo-pilot
PYTHONIOENCODING=utf-8 python eval/_selftest.py
# per (group, session): prepare -> fresh dev-agent edits runs/<group>/seed1/work/ -> score
PYTHONIOENCODING=utf-8 python driver.py prepare <group> <n>
PYTHONIOENCODING=utf-8 python driver.py score   <group> <n>
PYTHONIOENCODING=utf-8 python driver.py aggregate
```

v1 (ceiling) is preserved under `v1_ceiling/` for comparison.
