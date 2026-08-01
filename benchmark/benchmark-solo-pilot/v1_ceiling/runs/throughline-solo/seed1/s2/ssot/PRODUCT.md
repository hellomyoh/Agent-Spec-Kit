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
  pairs). Unknown field (absent from every record) raises `KeyError` (D6).
- S2 complete: `query(sort_by=field)` — STABLE ascending sort (ties keep
  insertion order), applied after `where`. Field absent from every record (or
  from a surviving record) raises `KeyError` (D7).
- query() limit/offset/select params exist on the signature but are not yet
  implemented (reserved for future tickets).
