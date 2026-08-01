# PROGRESS

## S0 (advanced, seed1) — initial Catalog
- Implemented `catalog.py` with `Catalog`: `add`, `all`, and no-argument `search()`.
- Decisions recorded: D1 (copy in/out), D2 (out-of-scope search args raise), D3 (insertion order).
- Verified: `python -c "import catalog"` plus a behavioural smoke test
  (insertion order, copy-on-read, copy-on-add isolation, NotImplementedError for
  each of query/where/sort_by/limit). All passed.

## S1 (advanced, seed1) — query text search
- Implemented `query`: non-None, non-blank query does case-insensitive substring
  matching on `name`; `None`/blank/whitespace-only stays in list mode. Matches keep
  insertion order; copy-on-read preserved.
- Decisions: D4 (query semantics + blank handling) added; D2 superseded for `query`
  only (`where`/`sort_by`/`limit` still raise, including when combined with `query`).
- Verified: `python -c "import catalog"` plus behavioural smoke tests (case-insensitive
  substring, insertion order among matches, None/blank list mode, no-match empty,
  copy-on-read isolation, NotImplementedError for where/sort_by/limit and for
  query+limit). All passed.

### Next (not yet specified by a user prompt)
- Define `where` equality filtering.
- Define `sort_by` ordering (field, direction, missing-key handling).
- Define `limit` semantics.
