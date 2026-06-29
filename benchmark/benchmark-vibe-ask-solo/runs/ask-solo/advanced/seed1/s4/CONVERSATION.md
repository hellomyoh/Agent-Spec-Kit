# CONVERSATION — S4 (advanced, seed1), MODE ask-solo

## Request
Add `limit` to `search()`: cap to the top N **after** sorting. Regression
requirement: `where` / `sort` / blank-query / unknown-field behaviour must all be
preserved.

## Conflict check (vs recorded decisions)
- `limit` is the final `[planned]` slot in FEATURES, governed by **D2** (out-of-scope
  args raise `NotImplementedError`). D2 explicitly says "future sessions will supersede
  this per-argument as behaviour is defined" — so specifying `limit` is the intended
  evolution, **not** a conflict. Action: implement + supersede D2 for `limit`. With all
  four args now defined, D2 is fully retired (kept as history, not deleted).
- No conflict with D1 (copy in/out), D3 (insertion order), D4/D6 (query/blank),
  D5 (where), or D7 (sort_by). These are preserved unchanged; `limit` is appended as
  the last pipeline stage and does not alter them.
- The prompt fixed only "top N after sort". The remaining edge cases (0, negative,
  >count, non-int) are unspecified, so I chose them deliberately and recorded them in
  D8, following the SSOT's established anti-silent-surprise stance (D2/D5/D7): surface
  likely caller mistakes rather than silently mask them.

## Plan
1. Replace the `limit` `NotImplementedError` guard with real behaviour: validate the
   type/sign, then slice the (filtered, sorted) results to the first N as the **last**
   step of the pipeline (query -> where -> sort_by -> limit), before the deep-copy out.
2. Edge cases: `None` = no cap (contract list-mode); `0` -> `[]`; `>=` count -> all
   (no-op slice); `< 0` -> `ValueError` (a `[:-n]` slice would silently drop from the
   end); non-`int` incl. `bool` -> `TypeError` (contract types it `int | None`).
3. Update SSOT (D8 added; D2 superseded/retired; D5/D7 trailing notes; FEATURES;
   PROGRESS). Refresh tests, preserving all regression cases. Run them.

## SSOT updates
- **DECISIONS.md**: added **D8** (limit = top N after sort + edge cases). Updated D2
  header/status to "fully retired" and superseded for `limit`. Updated the trailing
  "limit still raises" notes in D5 and D7 to reference D8.
- **FEATURES.md**: `limit` moved `[planned]` -> `[done]` (S4) with full semantics;
  replaced the "limit still unspecified / raises NotImplementedError" paragraph with the
  final pipeline (`query -> where -> sort_by -> limit`) and the note that `search()` no
  longer raises `NotImplementedError`.
- **PROGRESS.md**: added the S4 entry; refreshed the "Next" list.

## Test run
- `python -c "import catalog"` -> IMPORT OK.
- `python test_catalog.py` -> **32 tests passed**.
- Coverage: new `limit` cases (cap; top-N-after-sort; full query+where+sort+limit
  pipeline; `limit=0` -> []; `>= count` -> all; negative -> ValueError; non-int & bool
  -> TypeError; None -> no cap; no internal mutation) plus preserved regressions
  (insertion order, copy-on-add/read isolation, query substring + None/blank, where
  equality/AND/empty/missing-key, sort ascending/stable/after-filter/missing/incomparable).

## Summary
Implemented `limit` as the final pipeline stage capping the filtered+sorted results to
the top N, with deliberate, recorded edge-case policy. All prior behaviour preserved;
D2 superseded for `limit` and now fully retired. SSOT (D8, FEATURES, PROGRESS) updated;
32/32 tests green.
