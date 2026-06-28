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

## S2 (advanced, seed1) — where equality filter
- Implemented `where`: `{k: v}` equality filter, multiple keys AND-ed, matches keep
  insertion order and compose with `query`. Policy: a `where` key missing from any
  item in the catalog raises `ValueError` (checked over the whole catalog, before
  query selection); empty `{}` lists all.
- Decisions: D5 (where semantics + missing-key ValueError) added; D2 superseded for
  `where` only (`sort_by`/`limit` still raise, including when combined with `where`).
- Tests: added test_catalog.py covering single-key match, multi-key AND (incl. a
  tightened value dropping a non-match), no-match empty, where+query composition,
  copy-on-read, ValueError for a key missing on all items and on some items, and
  where+sort_by still raising. Preserved prior tests (insertion order, copy
  isolation, query, sort_by/limit NotImplementedError).
- Verified: `python -c "import catalog"` plus `python test_catalog.py` — 14 tests passed.

### Next (not yet specified by a user prompt)
- Define `sort_by` ordering (field, direction, missing-key handling).
- Define `limit` semantics.
