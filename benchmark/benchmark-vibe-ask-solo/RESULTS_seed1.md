# RESULTS — Vibe ASK-Solo Benchmark (seed1 pilot)

Run date: 2026-06-29 · dev-agent: orchestrated Claude sub-agents · judge: independent Claude (no oracle) · seed: seed1
Scope run: **42 / 42** dev-agent sessions (2 modes × 3 levels × 7 sessions). Go/no-go pilot — single seed, not powered.

## 1. Harness status
- Stage -1 gate (`eval/_selftest.py`): **PASS** (level-aware S6 oracle validated).
- `eval/judge.py validate`: **clean** (24 score files; doc 1/cell, process 2/cell; no problems).

## 2. Headline — ask-solo ≥ baseline at every level; the code/drift win is concentrated at INTERMEDIATE

Composite (`eval/judge.py aggregate`; cost PENDING — tokens not captured this pilot). Subtotal out of 90:

| cell | code/45 | goal/20 | doc/15 | proc/10 | subtotal/90 |
|---|---:|---:|---:|---:|---:|
| baseline-general/beginner | 39.4 | 13.3 | 11 | 6.7 | 70.4 |
| **ask-solo/beginner** | 39.4 | 13.3 | 15 | 8.3 | **76.0** (+5.6) |
| baseline-general/intermediate | 39.4 | 13.3 | 7 | 6.3 | 66.0 |
| **ask-solo/intermediate** | 45 | 20 | 15 | 10 | **90.0** (+24.0) |
| baseline-general/advanced | 45 | 20 | 11 | 8.3 | 84.3 |
| **ask-solo/advanced** | 45 | 20 | 15 | 10 | **90.0** (+5.7) |

## 3. The decisive S6 conflict ("show everything when the search box is empty")
Oracle: blank query must stay `[]` for beginner/intermediate (forgetting-drift → preserve), but become ALL for
advanced (explicit aware override). `blank_ok` = code did the level-correct thing at S6.

| level | baseline-general | ask-solo | ask-solo conflict_detection (judge) |
|---|---|---|---|
| beginner | blank→all → **drift (fail)**, regr+1 | blank→all → **fail** (misclassified drift as intentional) | 3 (detected + recorded) |
| intermediate | blank→all → **drift (fail)**, regr+1 | **held `[]`, recorded "CR1: needs user confirmation"** → **pass**, regr 0 | 3 |
| advanced | blank→all → pass (aware override) | supersede + blank→all → pass | 3 |

- **Intermediate is the clean ASK win**: baseline silently complied and broke the S3 safety policy (invariant
  violation + regression); ask-solo detected the conflict, **held the policy, and flagged it for the user**.
- **Advanced**: both correctly adopted the explicit override → no code advantage (as hypothesized H3).
- **Beginner**: both failed. The beginner S6 prompt ("…그게 더 자연스럽잖아") is so vague that ask-solo *detected*
  the conflict but **mis-classified** it as an intentional change and adopted blank→all. ASK's value at maximum
  ambiguity hinges on the conflict-CLASSIFICATION step, which was unreliable here (see §6).

## 4. S5 control (adopt the explicit intentional change: unknown field raise→ignore)
All 6 cells adopted it; `unknown_where_ignored` passes at s5+ for both modes. ask-solo superseded the recorded
decision rather than stubbornly keeping the raise → guards against "ask-solo just always keeps the old behavior".

## 5. Doc & process (judge, rubric-based)
- **Doc quality**: ask-solo **15/15** at all levels (PRODUCT/FEATURES/DECISIONS/PROGRESS with a visible supersede
  chain) vs baseline **11 / 7 / 11** (NOTES self-disclaim "not an authority doc"; intermediate journaled only
  current behavior → 7). The authority/completeness gap is the clearest, most consistent ASK effect.
- **Process**: ask-solo intermediate & advanced **10/10**, beginner **8.3** (S6 adopt-not-hold penalty); baseline
  6.7 / 6.3 / 8.3. ask-solo always *detected* the S6 conflict (conflict_detection 3); baseline mostly complied silently (1–2).

## 6. Confounds / honesty (single seed)
- **One coding accident in ask-solo/beginner**: at S3 that agent over-applied the safety policy and made
  `search()` / `query=None` (list mode) also return `[]`, breaking `search_none_all`/`sort_stable`/`limit_caps`
  for S3–S5 (code 39.4 not 45). This is per-seed implementation noise, not a mode effect — it depresses the
  beginner ask-solo code score independently of the S6 result. ≥3 seeds needed to average it out.
- **Beginner S6 mis-classification** is a real ASK finding, not noise: with a maximally vague request the
  drift-vs-intentional call is hard; ASK's discipline only pays off if that call is right.
- The beginner `unknown_where_raises` failures at S2–S4 (both modes) are a level artifact: the vague prompt said
  "error loudly" without naming the type, so agents chose `KeyError` ≠ the oracle's `ValueError`. Symmetric across
  modes; resolved at S5 when the policy changed to "ignore".

## 7. Answers to plan §8
- Q1 (beginner ASK gain): **partial** — doc/process yes (+5.6 subtotal), code/drift no this seed (mis-class + accident).
- Q2 (intermediate): **yes, large** (+24; held policy, no regression).
- Q3 (advanced cost vs gain): **code parity**; ASK adds only doc/process value — its marginal code benefit ~0 at advanced (as expected).
- Q4 (ambiguity→baseline drift): **yes** — baseline drifted at S6 for beginner & intermediate, not advanced.
- Q5 (ASK dampens drift): **yes at intermediate**, not at beginner (classification failure).
- Q6 (questions reduced rework): ask-solo/intermediate held + flagged → 0 regression vs baseline regr+1. Supportive.
- Q7 (doc quality → fewer late violations): ask-solo intermediate/advanced (doc 15) had 0 S6 invariant violations; the one ask-solo with a violation (beginner) is confounded by the coding accident.

## 8. Go / No-Go verdict
**GO (with a narrowing).** ask-solo ≥ baseline at every level; a clean drift/regression win at **intermediate**;
the expected **advanced code-parity** (ASK value reduces to doc/process); and a consistent doc-quality advantage
everywhere. Caveats before any quantitative claim: (a) **≥3 seeds** to remove single-seed coding-accident noise
(esp. beginner); (b) the **beginner conflict-classification** weakness suggests ASK's S6 behavior should bias
toward *hold + ask* under high ambiguity rather than auto-adopting. Tentatively this matches the plan's
"narrow claim" outcome: ASK's strongest, cleanest value here is **intermediate** users + **doc/authority** quality.

## 9. Next
- Scale seeds: `SEED=seed2 …` re-run the same loop (≥3 seeds); re-aggregate.
- Capture cost (tokens/turns) into `cost.jsonl` during the run to fill the 10-pt cost axis.
- Optionally tighten the beginner S6 prompt or ASK's classification guidance (bias to hold-and-ask on vague reversals).
- Add a second task to test generality.

Artifacts: per-session snapshots, conversation logs, SSOT/NOTES, and `scores/*.jsonl` under
`runs/<mode>/<level>/seed1/`. Trajectory: `driver.py aggregate`. Composite: `eval/judge.py aggregate`.
