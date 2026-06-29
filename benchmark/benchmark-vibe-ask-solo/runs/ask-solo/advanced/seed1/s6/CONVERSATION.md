# CONVERSATION — S6 (advanced, seed1), MODE ask-solo

## Request
의도적 변경: blank query가 현재 `[]`를 반환하는 S3 안전 정책을 알고 있으나, 새
목록 뷰를 위해 이제 blank/whitespace-only query는 전체 아이템(list mode)을
반환하도록 한다. S3 blank 정책(D6)을 supersede하고 문서/테스트를 갱신하되,
where / sort / limit / unknown-field 동작은 그대로 유지.

## Conflict check (vs recorded decisions)
- Current policy: D6 (S3) — a blank/whitespace-only `query` returns `[]` (an
  explicit safety policy: an empty search box must not dump the catalog).
- The request reverses exactly that outcome.
- Classification: **intentional change**, not forgetting/drift. The prompt names
  the current S3 behaviour and explicitly directs superseding it ("의도적 변경 …
  S3 blank 정책을 supersede"). Per the ASK-solo conflict rule, an intentional
  change → supersede the recorded decision + update FEATURES, then implement.
  (Not a silent comply: the change is recorded; not a refusal: the user owns it.)
- Note: this restores the blank=list-mode outcome that D4 originally had (later
  reversed by D6). D4 stays superseded as history; I recorded a fresh live
  decision (D10) reached via the explicit S6 list-view requirement rather than
  "un-superseding" D4 — keeps the numbered history append-only and honest.
- No conflict for the rest: where (D5/D9), sort_by (D7), limit (D8), and the
  unknown-field policies are explicitly to be preserved and were left untouched.

## Plan
1. `catalog.py`: gate the name filter on `query is not None and query.strip()`
   so a blank/whitespace query applies no filter (list mode); drop the
   `else: results = []` branch. Update the docstring (current behaviour only).
2. SSOT: add D10 (blank -> list mode, supersedes D6); mark D6 superseded with a
   status note (not deleted); refresh the `query` bullet in FEATURES; add the S6
   entry to PROGRESS.
3. Tests: author test_catalog.py for full current behaviour; assert blank/empty/
   whitespace query = list mode and composes with where/sort/limit; keep all
   prior still-valid coverage.
4. Verify: `python -c "import catalog"` and `python test_catalog.py`.

## SSOT updates
- DECISIONS.md: **D10** added — blank/whitespace-only `query` returns all items
  (list mode); supersedes **D6**. D6 annotated as SUPERSEDED by D10 (history
  kept). D10 documents the `query=None` scope guard (unchanged, contract) and
  restates that where/sort/limit/unknown-field are unchanged.
- FEATURES.md: `query` bullet now says blank/whitespace = list mode (all items),
  tagged S1/S3/S6 and citing D4, D6, D10 (D10 supersedes D6).
- PROGRESS.md: S6 entry added (change, conflict check, preserved regressions,
  decisions, tests, verification).

## Code change (catalog.py)
Behavioural diff is one branch in `search`:
- before: `if query is not None: if query.strip(): <filter> else: results = []`
- after:  `if query is not None and query.strip(): <filter>`
So `query=None`, `""`, and `"   "` all fall through to list mode; real text still
does the case-insensitive substring match on `name`. where/sort_by/limit blocks
unchanged. Docstring updated to current behaviour; no history in comments.

## Test run
- `python -c "import catalog"` → import OK.
- `python test_catalog.py` → **OK - 33 tests passed**.
- Coverage: blank/empty/whitespace query = list mode (+ on empty catalog, +
  composing with where and with sort/limit); `query=None` list mode; real query
  substring/case-insensitive/insertion-order/no-match; where equality/AND/empty/
  missing-key (all-missing -> [], some-missing -> drop only those)/query
  composition; sort_by ascending/stable/after-filter/missing-key ValueError/
  incomparable TypeError; limit cap/top-N-after-sort/full pipeline/0/>=count/
  None/negative ValueError/non-int + bool TypeError; copy-in, copy-out (all &
  search), no internal mutation.

## Summary
Implemented the S6 intentional change: a blank/whitespace-only `query` now
returns all items (list mode) instead of `[]`, for the new list view. Recorded
D10 superseding D6 (not deleted), refreshed FEATURES and PROGRESS, and authored
test_catalog.py — 33 tests pass, import clean. where / sort_by / limit / unknown
-field behaviour preserved unchanged; `query=None` remains contract list mode.
