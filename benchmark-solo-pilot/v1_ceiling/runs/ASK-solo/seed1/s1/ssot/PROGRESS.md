# PROGRESS

(maintain this SSOT doc across sessions)

## Done
### S0 — Scaffold
- Created `miniquery.py` with `class Store` per `provided/contract.py` (v1.0).
- Implemented:
  - `add(record)` — stores a shallow copy.
  - `all()` — returns all records as copies, in insertion order.
  - `query()` — no-argument: returns all records as copies.
- `query()` declared with full pinned signature; extra params inert (not implemented).
- Sanity-checked: `import miniquery` OK; verified copy-in / copy-out isolation
  and insertion order via a throwaway `python -c` check.
- SSOT docs initialised: PRODUCT, DATA_MODEL, DECISIONS (D1–D5), PROGRESS.

### S1 — Equality filter (`where`)
- Implemented `query(where={k: v, ...})`: keep records matching ALL key==value
  pairs (AND), `==` comparison, insertion order, returned as copies.
- Empty/None `where` is a no-op (returns all) — S0 behaviour preserved.
- Unknown-field policy (D6): a `where` key absent from EVERY stored record raises
  `KeyError(key)`. A record merely lacking the key is filtered out, not an error.
- Sanity-checked via `python -c`: single/multi-key AND, no-match, KeyError on
  unknown key, copy-out isolation, and missing-key-in-some-records all OK.
- SSOT updated: DECISIONS D6 (+ note on D5), PRODUCT status, this entry.

## Next (future tickets, NOT yet implemented)
- `query(sort_by=...)` — ascending sort; ties keep insertion order.
- `query(limit=..., offset=...)` — pagination.
- `query(select=[...])` — project to listed keys only.
- Decide policy (D5 open item) for params/keys used before/with edge inputs
  (e.g. unknown sort_by key, select of missing key) when those tickets land.

## Invariants to preserve
- Single self-contained file; no deps.
- Pinned signatures unchanged (contract v1.0).
- Copy-in / copy-out; default insertion order.
