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

## S3 (advanced, seed1) — sort_by ordering + blank-query safety policy
- Implemented `sort_by`: orders the post-filter results ascending with a stable
  sort (equal keys keep insertion order). Missing field on any result item raises
  `ValueError` (mirrors `where` policy); incomparable types raise `TypeError`.
- Changed blank-query handling (user-directed safety policy): a blank/whitespace-only
  `query` string now returns `[]` instead of listing all items. `query=None`
  remains list mode (contract preserved).
- Conflict check: the blank-query change conflicts with D4 (which had blank = list
  mode). The user stated the new behaviour and its safety rationale explicitly, so
  it is an intentional change → superseded D4's blank half (recorded, not deleted)
  and updated FEATURES, then implemented. `sort_by` was a `[planned]` slot (D2), so
  no policy conflict — D2 superseded for `sort_by`.
- Decisions: D6 (blank query -> []) and D7 (sort_by ascending/stable + missing-key
  ValueError) added; D4 blank handling superseded; D2 superseded for `sort_by`.
- Tests: refreshed test_catalog.py — blank/empty `query` now asserts `[]`;
  `query=None` still asserts list mode; added sort_by cases (ascending, stability
  with equal keys, sort after query/where filtering, missing-key ValueError,
  incomparable-type TypeError, sort_by+limit NotImplementedError). Preserved all
  still-valid prior tests (insertion order, copy isolation, query substring, where
  equality/AND/missing-key).
- Verified: `python -c "import catalog"` plus `python test_catalog.py` — all green.

### Next (not yet specified by a user prompt)
- Define `limit` semantics (clamping, interaction with sort, negative/zero values).
- Possibly: `sort_by` descending direction; explicit missing-value ordering.
