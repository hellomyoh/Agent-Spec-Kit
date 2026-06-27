# OpsBoard (B7) — Stage 0 Report (micro-pilot)

> Design: [../benchmark/REALWORLD_DESIGN.md](../benchmark/REALWORLD_DESIGN.md) · Pre-registration: [PREREGISTRATION.md](PREREGISTRATION.md)
> Scope: 1 app · groups **B-limited vs ASK** · 1 seed · sessions **S0–S9** (10) · model: Sonnet (capable).
> Purpose (pre-registered): **harness soundness + discrimination feasibility — NOT a result.** Statistical claims require Stage 3+.

## 1. One-line conclusion

**Stage 0 did not discriminate ASK from B-limited on the memory/consistency dimension (a ceiling): both groups held all 8 oracle invariants with zero regressions across 10 sessions.** ASK actually scored *lower*, but only because of a single-seed implementation accident (a `slot` type bug at S4) unrelated to memory. ASK also cost ~29% more dev tokens (SSOT upkeep). This reproduces the small-scale / M-pilot pattern (cost without benefit) and tells us exactly what to fix before Stage 1. **ASK effectiveness is neither shown nor refuted here.**

## 2. Trajectory (active checks per session; `viol` = invariant violations, `regr` = regressions vs earlier passing)

| S | feature | B-limited inv/func/xlayer · viol/regr | ASK inv/func/xlayer · viol/regr |
|---|---|---|---|
| 0 | scaffold | 1.0 / 1.0 / – · 0/0 | 1.0 / 1.0 / – · 0/0 |
| 1 | create/edit | 1.0 / 1.0 / – · 0/0 | 1.0 / 1.0 / – · 0/0 |
| 2 | state machine | 1.0 / 1.0 / – · 0/0 | 1.0 / 1.0 / – · 0/0 |
| 3 | permissions | 1.0 / 1.0 / 1.0 · 0/0 | 1.0 / 1.0 / 1.0 · 0/0 |
| 4 | scheduling | 1.0 / 1.0 / 1.0 · **0**/0 | 0.85 / 0.86 / 1.0 · **2**/0 |
| 5 | cache | 1.0 / 1.0 / 0.5 · 0/0 | 0.88 / 0.86 / 0.5 · 2/0 |
| 6 | comments | 1.0 / 1.0 / 0.5 · 0/0 | 0.88 / 0.86 / 0.5 · 2/0 |
| 7 | audit | 1.0 / 1.0 / 0.5 · 0/0 | 0.88 / 0.86 / 0.5 · 2/0 |
| 8 | search | 1.0 / 1.0 / 0.5 · 0/0 | 0.89 / 0.86 / 0.5 · 2/0 |
| 9 | post-approval freeze | 1.0 / 1.0 / 0.33 · **0**/0 | 0.89 / 0.86 / 0.33 · **2**/0 |

**Regressions = 0 for both groups in every session.** No invariant that once passed was later broken by a new feature — including the two designed conflict points (S8 search tenant-scoping, S9 freeze vs S1 free-edit). Both groups handled them correctly.

## 3. Why no discrimination (the honest diagnosis)

1. **Lossy memory never bit.** B-limited (fresh agent + only the last 2 sessions' notes) was supposed to forget early rules. It didn't, for two reasons: (a) the agents wrote *comprehensive rolling notes* that re-summarised the data model / multi-tenant / cache rules each session, so within a 2-session window little was actually lost; (b) the codebase is small enough to **re-read in full**, so any rule not in the notes was re-derived from the existing code. At this scale the current code *is* sufficient memory. This is the M-pilot lesson recurring: below a scale/complexity threshold, structured memory has nothing to add.
2. **Both groups front-loaded the whole app in S0.** Both agents implemented all 13 endpoints in S0 "for future sessions," so most later sessions were verifying/patching, not building under accumulating context — further suppressing drift.
3. **The two designed traps were defused by explicit tickets.** S8 ("results scoped to the actor's org") and S9 (named the frozen fields) stated the rule, and the pre-existing org-scoped code already satisfied S8 — so neither required *remembering* an unstated earlier decision.

## 4. The ASK regression is noise, not signal (important)

ASK's `viol=2` from S4 onward is **one coding bug, not a memory failure**: the ASK agent declared the `tasks.slot` column as `str` and passed the API's integer slot straight through, so the provided DB rejected it (`expected str, got 5`) and **scheduling broke** (`schedule`, `schedule_approved_ok`, `other_slot_ok` fail). B-limited coerced the slot and passed. No later ASK session happened to touch scheduling, so the bug persisted to S9 (per the pre-registered **no-repair** rule). This is the *opposite* of the ASK hypothesis and is a textbook example of why a **single seed** is uninterpretable: per-session implementation variance dwarfs any memory-regime effect. Multiple seeds (Stage 1+) are required to average it out.

## 5. The cross-layer drop is a harness gap, not a behavioural or memory effect

`cross_layer` falls 1.0 → 0.5 (S5) → 0.33 (S9) **identically for both groups**. Cause: the shared contract pins request shapes but **not the `render()` output shape**. Both agents' `render("dashboard")` returns `data=None` (dashboard counts surfaced elsewhere), and both expose locked fields as `locked_fields` rather than the reference's `disabled_fields`. The underlying behaviour is correct (API freeze works; dashboard counts are right via `get_dashboard`). Because it hits both groups equally it does **not** bias the comparison — but it must be fixed for Stage 1 (see §7). `perm_fe_api_consistent` passed throughout (the `available_actions` key happened to match).

## 6. Cost

Approximate dev tokens (subagent telemetry, S0–S9): **ASK ≈ 376k vs B-limited ≈ 292k → ASK +~29%.** ASK pays a roughly fixed SSOT-maintenance overhead every session. At this scale that buys no measured consistency benefit — the same "cost without benefit" seen at small scale and in the M-pilot. (Per §3 of the design, this cost comparison is vs the lossy baseline; ASK-as-context-compression would only pay off against an exploding-context `B-continuing`, not run here.)

## 7. What Stage 0 decided (its actual job)

- **Harness is sound.** Reference passes 50/50 hidden checks; 14 negative controls (incl. 5 cheat-apps an independent adversarial reviewer proved could fool the *first* harness) are all caught; isolation structural check passes. The harness survived adversarial review after hardening (C1–C4, I1–I5).
- **The task does not yet discriminate** — it ceilings on memory at this scale. Per the design's M-pilot lesson, Stage 1 must change the conditions, not just add seeds.

### Required fixes before Stage 1
1. **Pin the `render()` output shape in the shared contract** (`data`, `available_actions`, `disabled_fields`) so cross-layer checks attach to any implementation.
2. **Make lossy memory actually bite**: add a **K-token cap** on B-limited's carried notes (not just a 2-session window — comprehensive rolling notes defeated the window), and/or **enlarge scale** (more sessions / more entangled invariants / a codebase too large to fully re-read) so the current code stops being sufficient memory.
3. **Discourage S0 front-loading** (tickets should require building only the session's feature) so consistency cost accumulates.
4. **Multiple seeds** (≥3) so single-session coding accidents like ASK's slot bug average out.

## 8. Bottom line (no overclaim)

At Stage 0 scale, **structured SSOT (ASK) showed no consistency advantage over lossy-memory baseline and cost ~29% more** — consistent with the project's standing finding that ASK's benefit, if any, lives at larger scale. This is a **null/ceiling pilot result**, exactly the outcome the design anticipates Stage 0 may produce, and it yields a concrete, pre-registered list of harness/condition changes for Stage 1. It is **not** evidence against ASK at mid-scale; the conditions that would test that were not reached here.

## 9. Reproduce
```
PYTHONIOENCODING=utf-8 python eval/harness/stage_minus1_gate.py     # harness validation (must PASS)
PYTHONIOENCODING=utf-8 python eval/harness/run_tests.py eval/reference  # reference 50/50
PYTHONIOENCODING=utf-8 python driver.py aggregate                    # per-session trajectory from runs/
```
Per-session snapshots in `runs/<group>/seed1/sNN/` (code + memory artifacts); scores in `runs/<group>/seed1/scores.jsonl`.
