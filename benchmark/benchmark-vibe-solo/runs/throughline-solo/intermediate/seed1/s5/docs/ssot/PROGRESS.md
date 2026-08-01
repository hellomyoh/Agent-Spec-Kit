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

## S3 (seed1) — DONE
- `sort_by`: documented as ascending with stable tie-breaking (insertion order), via
  Python's stable `sorted` (D9). No behaviour change — clarifies D4/D6.
- `query` blank handling changed: a non-None blank `query` (empty or all-whitespace,
  `query.strip() == ""`) now returns an empty list instead of all items (D8).
- Conflict check: the blank-`query` change **conflicts with D6** (which had `query=""`
  matching every item). The S3 prompt requests this change intentionally, so D6's
  empty-string clause is **superseded** by D8 (precedence + query/where AND in D6
  remain). `query=None` (D3), D5 substring match, D2 copy-safety, D7 `where` all
  preserved.
- Verified via `python -c "import catalog"` plus a smoke test (sort ascending + stable
  ties, query=""/whitespace → [], query=None → all, non-blank substring match,
  where AND + missing-field ValueError, query+where AND, limit, copy-safety).
- SSOT updated: FEATURES, DECISIONS (D8, D9; D6 empty-string clause superseded), PROGRESS.

## S4 (seed1) — DONE
- `limit`: pinned the count-cap semantics (D10). `limit=n` keeps the first `n`
  results, applied last (after query/where/sort_by); `limit=None` → no cap; a
  non-positive `limit` (`0`/negative) → empty list. Positive-`limit`, sort, and
  filter behaviour all unchanged (the S4 prompt asks to keep sort/filter as-is).
- Conflict check: no conflict. The requested behaviour (limit the result count,
  sort/filter unchanged) was already in force via D4/D6; this session clarifies the
  loosely-defined cap, fixing only the previously-undefined non-positive edge
  (negative limit no longer falls through to a misleading negative-index slice).
  This mirrors how D9 clarified `sort_by`.
- Verified via `python -c "import catalog"` plus a smoke test (limit cap / =0 / <0 →
  empty / =None → all / >len → all, limit after sort and after query, no-arg search
  == all, query=None → all, blank query → [], ci substring, where AND + missing-field
  ValueError, sort ascending + stable ties, copy-safety).
- SSOT updated: FEATURES, DECISIONS (D10; D4 "cap count" clarified), PROGRESS.

## S5 (seed1) — DONE
- `where` missing-field handling changed: a `where` field missing from any item under
  test now returns an empty list instead of raising `ValueError` (D11). D7's equality
  -match, multi-key AND, and precedence (query → where → sort_by → limit) preserved.
- Conflict check: the change **conflicts with D7** (which raised `ValueError` on a
  missing `where` field). The S5 prompt requests this change intentionally, so D7's
  raise-clause is **superseded** by D11 (D7's match/AND/precedence remain). All other
  policies preserved: D2 copy-safety, D3 no-arg search / `query=None` off, D5 ci
  substring, D8 blank-query → [], D9 sort ascending+stable, D10 limit cap.
- Verified via `python -c "import catalog"` plus a smoke test (missing where field →
  [] no longer raises, incl. partial presence and missing field combined with query;
  present-field equality single/multi-key AND + no-match; query+where AND; no-arg
  search == all; query=None → all; blank query → []; ci substring; sort ascending +
  stable ties; limit cap / =0 / <0 → [] / =None → all; copy-safety).
- SSOT updated: FEATURES, DECISIONS (D11; D7 raise-clause superseded), PROGRESS.

## Open / deferred
- (none)
