# ASK-solo DriftBench — Stage-1 pilot (compact `miniquery` task)

> **STATUS / VERSION.** The task was iterated:
> - **v1** (restoration of a *policy*) hit a ceiling — the decision leaked into code docstrings, so even the
>   memoryless group recovered it. Archived under `v1_ceiling/` (see `v1_ceiling/RESULTS.md`).
> - **v2 (current)** restores an *arbitrary value* (default page size 7→25→40, then "restore original"),
>   overwriting the original twice under a "no change-history in code comments" norm. **v2 discriminates** —
>   see **`RESULTS_v2.md`** for the current design, the decisive S6 outcome, and interpretation.
>
> The detailed table just below describes the original **v1** design (kept for context). The live harness
> files (`tickets/`, `eval/tests.py`, `provided/contract.py`, `driver.py`) and `runs/` are **v2**.

This folder runs the **ASK-solo** benchmark described in
`benchmark/ASK_PROMPT_AND_BENCHMARK_REVIEW.md` §6 (Solo-only revision), with the 4 review
recommendations baked in. It is a **compact, runnable pilot** — not the full M-scale OpsBoard
program — built to be executable in one sitting while still answering the core question:

> Does a **self-maintained structured SSOT** (`ASK-solo`) preserve an early decision that a
> **memoryless** agent (`B-code`) loses, and beat **lossy memory** (`B-limited`) / **free notes**
> (`P-notes`) on drift/regression?

## Task: `miniquery` (a tiny in-memory record filter/sort library)

7 sessions (s0–s6). The decisive, **memory-required** invariant is a *restoration*
(the B3-proven discriminator):

| S | feature (ticket) | scored checks introduced | note |
|---|---|---|---|
| 0 | scaffold add/all/query() | add_all, query_all | |
| 1 | `where=` equality | where_eq, **where_unknown_raises** | decision stated **once**: unknown field → `KeyError` |
| 2 | `sort_by=` | sort_stable | decision: equal keys keep insertion order |
| 3 | `limit/offset` | limit_offset | |
| 4 | `select=` projection | select_proj | unknown-field policy **NOT** restated (must still hold) |
| 5 | change: unknown field → `[]` | where_unknown_empty (raises retired) | policy flip |
| 6 | **revert S5** (original behaviour **unstated**) | where_unknown_raises **reactivated** | memoryless agent cannot know "raise" |

At **S6** the on-disk code shows the S5 behaviour (returns `[]`) and the ticket only says
"revert S5". Only an agent that *remembered* the S1 decision can restore `raise KeyError`.
This is what separates the groups.

## Groups (review §6.2 / §6.2.1) — single manipulated variable = memory regime

- **B-code** — fresh agent, current code + ticket only (no memory). *Floor / B-code pre-check (review rec 1).*
- **B-limited** — last N=2 sessions' `NOTES.md`, each capped to `K_B=600` chars (lossy).
- **P-notes** — all prior `NOTES.md` concatenated, capped to `K_P=2600` chars (~ASK SSOT budget; logged each session) (record-effect control).
- **ASK-solo** — 4 SSOT docs (PRODUCT/DECISIONS/DATA_MODEL/PROGRESS) carried + updated every session.

Token-budget parity between P-notes and ASK-solo is logged by `driver.py prepare` (review rec 2).

## Metrics

- `where_unknown_raises` pass at S6 = **decision restoration fidelity** (the decisive memory signal).
- `invariant_violations`, cumulative `regr`, per-session `func` (active-check pass rate).
- Restoration is **the** pilot metric here (review rec 3: restoration is otherwise a fuller-design metric; this compact task includes one explicit restoration event so the pilot can measure it).

## How it was run (orchestrator model)

For each (group, session): `python driver.py prepare <group> <s>` → a **fresh dev-agent** edits
only `runs/<group>/<seed>/work/` (reads TICKET.md + carried code + `_MEMORY_FOR_PROMPT.txt`,
and for ASK the `ssot/`) → `python driver.py score <group> <s>` snapshots + runs the hidden
battery. Agents never see `eval/` (oracle isolation). Then `python driver.py aggregate`.

## Files

- `provided/contract.py` — pinned API (given every session).
- `tickets/s00..s06.md` — per-session tickets (invariants stated once).
- `eval/tests.py` — hidden battery + `active_in()` ranges (never copied into a workspace).
- `eval/ref_correct_s6/`, `eval/nc_no_restore/` + `eval/_selftest.py` — Stage-1 harness gate.
- `driver.py` — prepare / score / aggregate.
- `runs/<group>/<seed>/` — work/, sNN/ snapshots, scores.jsonl (produced by the run).
- `RESULTS.md` — the run's findings + go/no-go.

## Scope honesty

This pilot runs **seed1** of the 4 groups on **1 compact task**. The reviewed design calls for
**≥3 seeds** and (for statistical claims) multiple apps/sizes. This run is a **discrimination /
go-no-go** check (review §6.6), not a powered result.
