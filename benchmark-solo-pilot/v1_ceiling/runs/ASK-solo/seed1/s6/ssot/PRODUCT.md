# PRODUCT

(maintain this SSOT doc across sessions)

## What this is
`miniquery` — a tiny, single-file, in-memory record store (`class Store` in
`miniquery.py`). Records are plain `dict`s. The store provides insertion,
bulk retrieval, and a `query()` method that will grow filtering / sorting /
pagination / projection over successive sessions.

## Goals / principles
- Single self-contained module: `miniquery.py` (no external deps).
- Public API is PINNED by `provided/contract.py` — method names and signatures
  are FIXED across sessions; only behaviour evolves per the per-session ticket.
- Copy in, copy out: callers must never be able to mutate internal state.
- Each session implements ONLY its ticket; no pre-building future features.

## Public surface (from contract.py, CONTRACT_VERSION 1.0)
- `Store.add(record: dict) -> None`
- `Store.all() -> list[dict]`
- `Store.query(where=None, sort_by=None, limit=None, offset=0, select=None) -> list[dict]`

## Status
- S0 scaffold complete: `add`, `all`, and no-argument `query` implemented.
- S1 complete: `query(where=...)` equality filter (AND across all key==value
  pairs). Unknown-field handling: an unknown field raises `KeyError`. (History:
  D6 raise → D10/S5 changed to no-match → D11/S6 REVERTED back to raise; the
  current rule is the original D6 raise rule. See S5/S6 notes below.)
- S2 complete: `query(sort_by=field)` — STABLE ascending sort (ties keep
  insertion order), applied after `where`. Field absent from every record (or
  from a surviving record) raises `KeyError` (D7).
- S3 complete: `query(offset=, limit=)` — pagination applied after `where`
  then `sort_by`. Slice-based with clamping: out-of-range values yield fewer/no
  rows rather than erroring; defaults (`offset=0`, `limit=None`) are a no-op (D8).
- S4 complete: `query(select=[field, ...])` — project each returned row to ONLY
  the selected keys PRESENT on that row (missing keys silently dropped, never an
  error; unlike `where`/`sort_by`, `select` does NOT validate field names).
  Applied LAST (after `where`, `sort_by`, pagination). `select=None` returns full
  records; `select=[]` yields empty dicts (D9).
- S5 complete: CHANGED `where` unknown-field handling — a `where` field absent
  from every stored record yields NO match (`query()` returns `[]`) instead of
  raising `KeyError` (D10, superseded D6's raise rule). [REVERTED in S6.]
- S6 complete: REVERTED S5 — `where` unknown-field handling restored to the
  pre-S5 (S1/D6) behaviour: a field absent from every stored record raises
  `KeyError` again, and empty store + non-empty `where` raises again (D11,
  reverts D10). Scope was `where` only; `sort_by`'s `KeyError` (D7) and
  `select`'s no-validation (D9) are unchanged, so `where`/`sort_by` are again
  consistent (both raise on unknown fields).
- query() implements its full pinned parameter set (where, sort_by, limit,
  offset, select).
