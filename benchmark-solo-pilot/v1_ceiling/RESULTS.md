# ASK-solo DriftBench — Stage-1 pilot RESULTS (seed1, `miniquery`)

Run date: 2026-06-28 · Model (dev-agent): orchestrated Claude sub-agents · Orchestrator: Claude Code
Scope: **1 compact task · 4 groups · seed1 · 7 sessions (s0–s6) = 28 dev-agent sessions.**
This is a **discrimination / go-no-go pilot** (review §6.6), NOT a powered result.

## Headline

**No discrimination — a ceiling.** All four groups (B-code, B-limited, P-notes, ASK-solo)
held every active invariant with **zero violations and zero regressions across all 7 sessions**,
including the decisive **S6 restoration** (`where_unknown_raises` correctly restored).

Crucially, even **B-code (zero carried memory)** restored the pre-S5 policy at S6 — not from
memory, but by **reading the decision history out of its own module's docstring**. The scored
invariant turned out to be **re-derivable from the current code**, so a memoryless agent matched
the memory-bearing ones.

## Trajectory (identical for all 4 groups)

| S | active pass | func | inv_viol | regr | `where_unknown_raises` |
|---|---|---|---|---|---|
| 0 | 2/2 | 1.0 | 0 | 0 | (not active) |
| 1 | 4/4 | 1.0 | 0 | 0 | ✅ (decided: raise) |
| 2 | 5/5 | 1.0 | 0 | 0 | ✅ |
| 3 | 6/6 | 1.0 | 0 | 0 | ✅ |
| 4 | 7/7 | 1.0 | 0 | 0 | ✅ (not restated; still held) |
| 5 | 7/7 | 1.0 | 0 | 0 | (retired; `where_unknown_empty` ✅) |
| 6 | 7/7 | 1.0 | 0 | 0 | ✅ **restored by ALL groups** |

(Per-group raw data: `runs/<group>/seed1/scores.jsonl`.)

## Root cause (evidenced)

The dev agents — as capable agents naturally do — **documented the policy change in the module
docstring**. B-code's own S5 snapshot (`runs/B-code/seed1/s5/miniquery.py`) contains:

```
`where` policy (S1, REVISED in S5):
  - S5 change: a `where` key not present in ANY stored record now yields []
    (S1 originally raised KeyError(key) for such an unknown field; S5 replaces ...)
```

So at S6 ("revert S5; restore the prior behaviour"), the **zero-memory** B-code agent read this
docstring and reinstated `KeyError`. Behavioural check confirms B-code S6 raises again.

→ The restoration invariant was **not memory-required**; it was **re-derivable from current code**.
This is exactly the make-or-break feasibility risk flagged in the review (rec 1 / §6.1.2): *below a
scale threshold, the current code — including the comments capable agents write — IS sufficient
memory.* The discriminator leaked into the codebase.

## Go / no-go verdict (review §6.6)

**REVISE TASK.** B-code passed the late invariant ⇒ the task is a ceiling. Per the B-code
pre-check rule (rec 1), do **not** scale this task to 3 seeds / more groups; redesign first.

What would make it discriminate (candidate fixes for the next iteration):
1. **Make the decision non-derivable from code+comments.** The revert target must be a fact that
   cannot be reconstructed from the current module. Options: revert to a policy *two changes back*
   whose explanatory comment was itself overwritten by the intervening change; or anchor the
   decision on an **externally-specified value** (e.g., a magic threshold the user set in S1 that
   never appears verbatim in code) so the comment can't carry it.
2. **Scale up** (more sessions / larger codebase) so agents cannot keep the full decision history
   in docstrings and the current code stops being sufficient memory.
3. Optionally strip agent-authored comments before handing the snapshot to the next session — but
   this is unrealistic (real devs comment), so (1)/(2) are preferred.

## What this pilot DID validate (positive outcomes)

- **Harness is sound.** The Stage -1 self-test gate (`eval/_selftest.py`) confirmed the battery
  *passes* a correct restoration and *catches* a no-restore negative control — so the null result
  is a real ceiling, not a broken scorer.
- **End-to-end pipeline works.** prepare → fresh dev-agent (sandboxed to `work/`) → score → aggregate
  ran cleanly for 28 sessions across 4 memory regimes; oracle isolation held (agents never saw `eval/`).
- **Memory-carry mechanics work and are visibly differentiated**: B-limited's K=600 cap truncated
  notes mid-word (lossy as intended); ASK-solo maintained an auditable decision chain
  (`DECISIONS.md` D6 → `[SUPERSEDED by D10]` → `D11 revert`); B-code carried nothing.
  The *mechanism* differences were real; they just didn't matter because the **code carried the decision**.
- **The B-code pre-check earns its place.** It caught the ceiling in 28 sessions — before any
  investment in the full ~90–108-session 3-seed pilot. That is precisely its intended payoff.

## Honest scope / limitations

- 1 compact task, 1 seed → **not** a statistical result; a go/no-go probe only.
- The chosen discriminator (a behavioural policy) is the *wrong kind* for a code-resident task,
  as this run demonstrated. The fix is task design, not more seeds.
- P-notes/ASK token-budget parity is instrumented in `driver.py` (`[budget]` line) but was not
  persisted this run; capture it in the next iteration.

## Reproduce

```
cd benchmark-solo-pilot
PYTHONIOENCODING=utf-8 python eval/_selftest.py            # Stage -1 gate
# per (group, session): prepare -> dev-agent edits runs/<group>/seed1/work/ -> score
PYTHONIOENCODING=utf-8 python driver.py prepare <group> <n>
#   <orchestrator runs a fresh dev-agent in that work/ dir>
PYTHONIOENCODING=utf-8 python driver.py score   <group> <n>
PYTHONIOENCODING=utf-8 python driver.py aggregate
```
