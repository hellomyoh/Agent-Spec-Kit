# PROGRESS

## S0 (seed1) — DONE
- Created `catalog.py` with the full pinned contract surface: `Catalog.add`,
  `.all`, `.search(query, where, sort_by, limit)`.
- This session's behaviour: `search()` with no arguments returns all items.
- Verified via `python -c "import catalog"` plus a smoke test (no-arg search == all,
  copy-safety).
- SSOT updated: PRODUCT, FEATURES, DECISIONS (D1–D4).

## S1 (seed1) — DONE
- Implemented `query` text search: case-insensitive substring match on item `name`
  (D5), applied before `where`/`sort_by`/`limit` (D6). `query=None` (D3) and
  copy-safety (D2) preserved.
- Conflict check: no conflict. Resolves the D4 deferral (D4's `where`/`sort_by`/
  `limit` meaning stays in force); D3 (`None` = no filter) preserved.
- Verified via `python -c "import catalog"` plus a smoke test (case-insensitive
  substring, no-arg search == all, combination with where/sort/limit, copy-safety).
- SSOT updated: FEATURES, DECISIONS (D5, D6; D4 deferral superseded), PROGRESS.

## Open / deferred
- (none)
