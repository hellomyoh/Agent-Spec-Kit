# PROGRESS

## S0 (seed1) — initial catalog
- Created `catalog.py` with `Catalog`.
- Implemented: `add(item)`, `all()`.
- `search(...)` exposed per contract; list-mode only (other args inert).
- Verified: `python -c "import catalog"` + add/all/copy-safety/list-mode checks pass.
- Decisions recorded: D1-D4.

## S1 (seed1) — name search
- Implemented `search(query=...)`: case-insensitive substring match on `name`
  (`'ap'` matches `'Apple'`); empty query matches all; missing `name` -> `''`.
- List mode (`query=None`) and copy-safety (D3) unchanged.
- Verified: `python -c "import catalog"` + substring/case-insensitive/list-mode/
  empty-query/no-match/copy-safety/missing-name checks pass.
- Decisions recorded: D5 (supersedes D1, D2 for `query`), D6.

## S2 (seed1) — field equality filter (`where`)
- Implemented `search(where=...)`: equality filter on item fields, e.g.
  `where={'category': 'fruit'}`; multiple keys AND together; combines with
  `query` (both must hold).
- Loud-on-mistake: a `where` key present on no item in a non-empty catalog
  raises `KeyError` (catches typos) instead of silently returning nothing; an
  item that merely lacks the key just doesn't match. Empty catalog skips the
  check and returns `[]`.
- List mode, prior `query` behaviour (D5/D6), and copy-safety (D3) unchanged.
- Verified: `python -c "import catalog"` + where-equality / sparse-field /
  unknown-field-raises / query+where AND / multi-key / list-mode / copy-safety /
  empty-catalog checks pass.
- Decisions recorded: D7 (supersedes D1 for `where`), D8.

## S3 (seed1) — stable sort + empty-search shows nothing
- Implemented `search(sort_by=...)`: stable ordering by a field, so equal values
  keep insertion order; items missing the field sort last; an unknown sort field
  raises `KeyError` (mirrors the `where` typo policy, D8).
- Changed empty-search behaviour: `search` now returns `[]` unless a real
  criterion is given. With no `where` and a None/blank/whitespace `query` it
  returns nothing instead of the whole catalog ("don't dump everything; show
  nothing until I type something"). `all()` is unchanged and remains the explicit
  "view the full list" path.
- Prior `query`/`where` matching (D5/D6 matching rules), the unknown-field
  KeyError (D8), and copy-safety (D3) unchanged.
- Verified: `python -c "import catalog"` + 22-check suite — empty/blank/whitespace
  search -> [] / where-only and query+where still return / all() still dumps all /
  unknown where & sort fields raise / sparse fields / empty catalog / stable sort
  with missing-last / sort+where / copy-safety / where-dict-untouched — all pass.
- Decisions recorded: D9 (supersedes D1 for `sort_by`), D10 (supersedes D6 and the
  list-mode-returns-all behaviour for `search`).

## S4 (seed1) — result cap (`limit`)
- Implemented `search(limit=...)`: returns only the first `limit` items of the
  result (the "top N"), applied last — after `where`, `query`, and `sort_by`.
  `limit=None` is no cap (prior behaviour unchanged); `limit=0` returns `[]`; a
  `limit` past the result returns the whole result.
- `limit` does not bypass D10: a criterion-less search is still `[]` (limit is a
  result shaper, not a search criterion).
- Loud-on-mistake: negative `limit` raises `ValueError`, non-integer (incl.
  `bool`) raises `TypeError` (mirrors the `where`/`sort_by` typo policy).
- All S0–S3 behaviour (D3 copy-safety, D5/D6 query, D7/D8 where, D9 sort, D10
  empty-search) unchanged.
- Verified: `python -c "import catalog"` + 32-check suite — limit caps/None/0/
  over-length / limit after sort+where / limit does not dump catalog (criterion-
  less still []) / negative & non-int & bool raise / full S1–S3 regression /
  copy-safety — all pass.
- Decisions recorded: D11 (supersedes D1 for `limit`; D1 now fully superseded).

## S5 (seed1) — `where` on unknown field stops raising (forgiving filter)
- Changed `search(where=...)`: filtering on a field that no item has now returns
  `[]` instead of raising `KeyError`. Removed the catalog-wide existence check
  for `where`; the equality filter alone yields no matches for an absent field.
  Behaves the same on empty and non-empty catalogs. (User found the loud error
  "짜증나네" / annoying in real use and asked to just get an empty result.)
- Preserved deliberately: `sort_by` on an unknown field STILL raises `KeyError`
  (D9) — the user's request named filtering only, and a bogus sort field has no
  sensible empty-result reading. `limit` bad-input raises (D11) also untouched.
  Recorded the resulting `where`-forgiving / `sort_by`-loud asymmetry.
- D7 equality matching, D5/D6 query, D9 sort ordering, D10 empty-search, D11
  limit, and D3 copy-safety all otherwise unchanged.
- Verified: `python -c "import catalog"` + 30-check suite — unknown `where` field
  (single, multi-key, empty-catalog, +query) all return `[]` with no raise /
  existing-field `where` still filters / `sort_by` unknown field still raises /
  full S1-S4 regression (query, where, sort stable+missing-last, limit caps/0/
  None/over-length/negative/non-int/bool, show-nothing rule) / copy-safety — all
  pass.
- Decisions recorded: D12 (supersedes D8), D13 (preserves D9 for `sort_by`).

### Next / deferred
- Persistence (only if a future session asks).
- If a future session needs `search(query=None)` to list everything again,
  revisit D10 (today `all()` is the explicit list-everything path).
