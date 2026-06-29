# CONVERSATION — S4 (seed1, ask-solo)

## Request
> 결과 개수 좀 제한할 수 있게 해줘. 상위 N개만 보이게.

"Let me limit the number of results. Show only the top N." → implement the
`limit` argument of `search`.

## Conflict check (vs recorded decisions)
- `limit` is part of the FIXED contract (`limit: int | None = None`) and was
  explicitly **deferred**: PROGRESS "Next" listed "Define `limit` cap", and
  FEATURES/catalog.py both said "`limit` is NOT implemented yet."
- D1 (S0) deferred query/where/sort/limit under "keep it simple." Every prior
  session superseded D1 for one feature as the user directed it (query→D5,
  where→D7, sort_by→D9). The user is now directing `limit` → **intentional
  evolution**, so D1 is superseded for `limit` (D11). After this, D1 is fully
  superseded.
- No active policy is broken: `limit=None` (the default) keeps all S0–S3
  behaviour byte-for-byte; `limit` only caps when supplied. D10 (show-nothing)
  and D3 (copy-safety) are explicitly preserved.
- Verdict: **no conflict → implement** (with a recorded supersede of D1 for
  `limit`).

## Plan
1. Add `limit` handling at the END of `search`, after where/query/sort_by, so
   "top N" = first N of the final ordered result.
2. Decide unspecified semantics (contract leaves them to the prompt):
   - `limit=None` → no cap; `limit=0` → `[]`; `limit > len` → whole result.
   - `limit` must NOT bypass D10: a criterion-less search stays `[]`.
   - Bad cap fails loudly (project policy, D8/D9): negative → `ValueError`,
     non-int → `TypeError`; reject `bool` (not a meaningful count).
3. Preserve D3 (slice + per-dict copy → no internal-state leak).
4. Update SSOT; write tests; run them.

## SSOT updates
- DECISIONS.md: added **D11 (S4)** — implement `limit`, supersedes D1 for
  `limit` (D1 now fully superseded). Records top-N-applied-last, None/0/over
  semantics, the "limit does not bypass D10" rule, loud-on-bad-cap, D3 preserved.
- FEATURES.md: replaced "`limit` is NOT implemented yet" with the active `limit`
  behaviour.
- PROGRESS.md: added S4 entry + test summary; removed `limit` from deferred.
- PRODUCT.md: added S4 to "Scope so far".

## Test run
`python -c "import catalog"` → OK.
Inline 32-check suite (all PASS):
- limit: caps to top N; `None` = no cap; `0` = `[]`; `> len` = all; `1` = single.
- limit applied AFTER sort_by and after where.
- limit does NOT dump the catalog: `search(limit=5)`, `search('', limit=5)`,
  `search(None, limit=5)` all `[]` (D10 still wins).
- bad cap: negative → `ValueError`; `1.5`/`'2'`/`2.0` → `TypeError`;
  `True`/`False` → `TypeError`.
- Regression (unchanged): D10 empty/whitespace search → `[]`; `all()` dumps all;
  D5/D6 case-insensitive substring; D7 query+where AND; D8 unknown-where
  `KeyError`; D9 unknown-sort `KeyError` + missing-field-last stable sort; D3
  copy-safety (mutating result or post-add source does not leak); empty catalog
  + limit → `[]`.

## Summary
Implemented `limit` as a top-N cap applied last in `search` (after
filter/sort). `limit=None` preserves all prior behaviour; `0` → none; over-length
→ all; a negative/non-int/bool limit raises (loud-on-mistake). `limit` never
overrides the show-nothing rule (D10) or copy-safety (D3). Recorded D11
(supersedes D1 for `limit`); refreshed FEATURES/PROGRESS/PRODUCT. 32/32 checks
pass.
