# Stage 0 Pre-registration — OpsBoard (B7)

> Fixed BEFORE any dev-agent runs (REALWORLD_DESIGN.md §1, §3, §10, §11). Stage 0 is a
> harness-soundness + discrimination-feasibility check, **not** a result.

## Scope
- 1 app (OpsBoard), **groups = {B-limited, ASK}** (+ B-continuing, 1 seed, diagnostic), **1 seed**, **sessions S0–S9** (10).
- Reaches S9 (post-approval freeze first collides with earlier free-edit + permissions + cache) — the first cross-cutting conflict point.

## Groups (memory regime is the ONLY manipulated variable)
- **B-limited** (primary baseline = lossy human memory): every session a *fresh* agent gets the current ticket + the current code on disk + only the **last N=2 sessions' own short notes** (`NOTES.md`). Older notes are dropped. No structured/cumulative decision doc.
- **ASK**: every session a fresh agent gets the current ticket + current code + **all 7 SSOT docs it maintains** (`PRODUCT, DATA_MODEL, API_CONTRACTS, CACHE_POLICY, ARCHITECTURE, DECISIONS, PROGRESS`), carried and updated across all sessions.
- **B-continuing** (diagnostic ceiling): fresh agent + **full concatenated prior session context** (all prior tickets+notes), no structured docs. Implemented by concatenation, not agent-resume APIs. Runs 1 seed only.

Both/all: same capable model, same provided infra (`provided/`) + shared contract, current code handed off on disk, no cross-session conversation memory except as defined above.

## N/K justification (not tuned to favour ASK)
- `N=2` models "a developer recalls the last 2–3 features clearly but older detail fades." Chosen for realism, **not** to widen the ASK gap. Stage 0 fixes N=2; sensitivity over N is a **Stage 1** report item, not Stage 0.

## Ticket ambiguity tags (each scored rule is seeded once)
Every scored invariant is **stated once** in the ticket that introduces its feature (so later sessions test *memory/consistency*, not lucky guessing). Tags: `explicit` (stated), `latent` (derivable from PRD), `open` (free choice → self-consistency only). Per-ticket tags are in each `tickets/sNN.md`.

## Chain-death rule (REALWORLD_DESIGN.md §3.2)
- No evaluator repair of broken hand-offs (repair only happens inside the app's own later sessions). Each session is scored on the code it actually produced.
- A session is `chain-dead` if its code fails to import / the shared interface does not attach / a core prior invariant suite crashes — cascading failures are reported as **chain-death rate**, separating memory drift from plain build failure. Functional gate: per-session functional must average ≥0.8 for the run to be interpretable.

## Headline metrics (pre-registered)
Per session, scored by the hidden harness on the public surface only:
- `functional` (happy-path completion), `invariants` (8 oracle invariants, behavioural), `cross_layer` (E2E FE→BE→DB→cache→FE), `regression` (earlier-session behaviour still passing), `rework` (n/a until S12).
- **Primary read = the per-session *trajectory* of (invariant violations · cross-layer · regression), and whether ASK − B-limited widens in later sessions.**

## What Stage 0 decides
- Does the harness discriminate (no ceiling/floor)? Does B-limited actually drift as features accumulate, or does re-reading the current code keep it consistent (a ceiling — then enlarge scale/sessions per M-pilot lesson)?
- Stage 0 is **not** evidence for/against ASK. Statistical claims require Stage 3+ (single app, single seed here).

## Isolation (P8)
- Agent workspace per session contains ONLY: `provided/`, the agent's own code, its memory artifacts (NOTES or SSOT), and the current ticket. `eval/` (oracle, hidden tests, scorer, negative controls, reference) is never copied in. Post-run, the agent's file reads are audited; out-of-workspace reads void the run.
