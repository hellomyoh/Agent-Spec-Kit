# PROGRESS

## S0 (advanced, seed1) — initial Catalog
- Implemented `catalog.py` with `Catalog`: `add`, `all`, and no-argument `search()`.
- Decisions recorded: D1 (copy in/out), D2 (out-of-scope search args raise), D3 (insertion order).
- Verified: `python -c "import catalog"` plus a behavioural smoke test
  (insertion order, copy-on-read, copy-on-add isolation, NotImplementedError for
  each of query/where/sort_by/limit). All passed.

### Next (not yet specified by a user prompt)
- Define `query` text-search semantics (matching, blank/None handling).
- Define `where` equality filtering.
- Define `sort_by` ordering (field, direction, missing-key handling).
- Define `limit` semantics.
