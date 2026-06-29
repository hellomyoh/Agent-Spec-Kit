# CONVERSATION — S5 (advanced, seed1)

## Request
의도적 변경 (intentional change): a `where` key that is absent from the items
should no longer raise — it should be ignored, returning `[]` (the `ValueError`
is abolished, "ValueError 폐기"). Update the spec/tests to match; keep the rest of
the policy the same ("나머지 정책은 그대로").

## Conflict check
- Conflicts with **D5** (S2), whose missing-key policy raised `ValueError` when a
  `where` key was absent from any item. The new request is the inverse.
- Classification: **intentional change → supersede.** The prompt explicitly labels
  it "의도적 변경" and states the new behaviour and that the ValueError is retired,
  so this is a deliberate policy change, not forgetting/ambiguous drift. Per the
  ASK-solo rule I supersede the recorded decision (record, don't delete) and update
  FEATURES, then implement — rather than silently complying or refusing.
- Ambiguity resolved: "모든 아이템에 없는 where 키" names the all-missing case, but
  the stated mechanism ("ignore / treat as non-match → []") applies uniformly. I
  adopt a single rule — a missing key is a non-match — so all-missing yields `[]`
  and some-missing simply drops the items lacking the key. This fully retires the
  ValueError as directed and avoids an inconsistent all-vs-some split. Documented
  in D9.
- Out of scope (unchanged): `sort_by`'s own missing-key `ValueError` (D7) is a
  separate decision; only `where`'s missing-key handling changed.

## Plan
1. `catalog.py`: remove the `where` missing-key `ValueError` pre-check; change the
   equality filter to `key in item and item[key] == value` (missing key → drop the
   item). Leave query, sort_by, limit, copy-in/out, and ordering untouched.
2. SSOT: add **D9** (where missing key → non-match/`[]`, supersedes D5 missing-key
   half); mark D5's missing-key half superseded; refresh FEATURES `where` entry;
   add S5 PROGRESS entry.
3. Tests: author `test_catalog.py` covering full current behaviour; change the
   missing-key expectations to `[]` (all-missing) / drop-only (some-missing) and
   add a missing-key + query composition case; keep all other still-valid tests.

## SSOT updates
- **DECISIONS.md**: added D9; D5 header + missing-key paragraph marked superseded
  (kept as history). D7 (sort_by missing-key) deliberately left as-is.
- **FEATURES.md**: `where` bullet now describes missing key → non-match → `[]`
  (no error), empty `{}` lists all; tagged S2/S5, D5+D9.
- **PROGRESS.md**: added S5 entry (change, conflict-check, preserved regressions,
  decisions, tests, verification); added a "Next" note that `where` (D9) and
  `sort_by` (D7) missing-key policies now intentionally differ.

## Test run
- `python -c "import catalog"` → import OK.
- `python test_catalog.py` → **33 tests passed.**
- Manual sanity: `where={'size':'big'}` (missing on all) → `[]`;
  `where={'color':'red','size':'big'}` → `[]`; `where={}` → all items;
  `where={'color':'red'}` → matches; some-missing key drops only the lacking item.

## Summary
Superseded D5's missing-key `ValueError` with D9: a `where` key absent from the
items is now treated as a non-match, so a key missing from every item returns `[]`
(ValueError retired). All other behaviour (query, where equality/AND/empty,
sort_by, limit, copy isolation) preserved. SSOT updated and 33 tests pass.
