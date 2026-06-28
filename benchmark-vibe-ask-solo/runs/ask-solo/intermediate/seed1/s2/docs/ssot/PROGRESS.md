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

## S2 (seed1) — DONE
- Defined `where` equality-filter semantics fully (D7): `{field: value}`, multiple
  keys AND, raising `ValueError` when a `where` field is missing from any item under
  test. Precedence (query → where → sort_by → limit) and all prior policies (D2 copy
  -safety, D3 no-arg search, D5/D6 query) preserved.
- Conflict check: no conflict. New behaviour (ValueError on missing field) refines
  the previously-unspecified missing-field handling in D4/D6; prior `item.get` was
  incidental, not a recorded policy.
- Verified via `python -c "import catalog"` plus a smoke test (single/multi-key AND,
  no-match, missing-field ValueError incl. partial presence, query+where AND,
  no-arg search == all, query="" all-match, sort/limit, copy-safety).
- SSOT updated: FEATURES, DECISIONS (D7; D4/D6 refined), PROGRESS.

## Open / deferred
- (none)
