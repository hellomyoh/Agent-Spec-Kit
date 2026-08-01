# CONVERSATION — S2 (seed1, throughline-solo)

## Request
Add a `search(where={field: value})` equality filter (multiple keys → AND).
If a `where` field is absent from any item, raise `ValueError`.

## Conflict check
No conflict.
- `where` already existed as an AND equality filter (D4, D6, FEATURES) — preserved.
- The new part is **raising `ValueError` when a `where` field is missing**. This
  refines behaviour that prior decisions left unspecified: the old code used
  `item.get(field)` (missing field → `None`, silent non-match), which was incidental,
  not a recorded policy. Refining it does not break any recorded decision.
- All recorded policies preserved: D2 (copy-safety), D3 (`query=None` no-arg search
  returns all), D5 (case-insensitive substring `query`), D6 (precedence query → where
  → sort_by → limit; AND of query and where; `query=""` matches all).

## Plan
1. In `search`, when `where` is given, validate each key exists on every item under
   test (post-`query`); raise `ValueError` for the first missing field.
2. Switch the match test from `item.get(field) == value` to `item[field] == value`
   (safe after validation).
3. Keep precedence and all other stages unchanged.

## SSOT updates
- FEATURES: documented `where` AND semantics + missing-field `ValueError` (S2).
- DECISIONS: added **D7 (S2)**; annotated D4/D6 as refined by D7 (supersede-not-delete).
- PROGRESS: added S2 entry.

## Test run
- `python -c "import catalog"` → IMPORT_OK.
- Smoke test (all passed):
  - single-key `where` equality; multi-key AND; AND with no match;
  - missing `where` field → `ValueError` (also when only one item lacks the field);
  - `query` + `where` combine (AND);
  - no-arg `search()` == `all()` (D3);
  - `query=""` matches all (D6);
  - `sort_by` + `limit`;
  - copy-safety: mutating a returned dict does not affect internal state (D2).

## Summary
Implemented the missing-field `ValueError` for `where` while preserving the existing
AND equality filter and all prior policies. SSOT refined via D7 (D4/D6 annotated, not
deleted). Verified by import + smoke test.
