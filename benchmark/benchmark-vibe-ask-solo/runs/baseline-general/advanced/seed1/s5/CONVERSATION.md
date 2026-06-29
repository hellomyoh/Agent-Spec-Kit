# CONVERSATION — advanced S5

## Request

Intentional behaviour change: a `where` key that is missing from some items must
no longer `raise`. Instead, missing keys are ignored — items lacking the key do
not match and are filtered out, so a key absent from every item returns `[]`.
The `ValueError` previously raised for missing `where` keys is abolished. The
spec/docs and tests are updated to match; all other policies stay the same.

## Plan

1. Remove the pre-check loop in `search` that raised
   `ValueError("where key ... is missing from some items")`.
2. Change the `where` filter so a missing key is a non-match instead of a
   `KeyError`/error: keep an item only if, for every `(key, value)` pair, the
   item HAS the key AND its value equals `value`
   (`all(key in item and item[key] == value for ...)`).
3. Keep everything else untouched: blank-query guard, `query=None` list mode,
   case-insensitive substring on `name`, stable ascending `sort_by`, `limit`
   (top-N, applied last, `0 -> []`, negative `-> ValueError`), copy-on-return,
   and pipeline order (empty-query guard -> where -> query -> sort_by -> limit).
4. Update module/`search` docstrings and `docs/NOTES.md` to describe the new
   missing-key behaviour. Verify with `python -c "import catalog"` plus a
   behaviour script.

## Test run

`python -c "import catalog"` succeeds. Behaviour script (3 items, one without a
`color` key, then a 4th with `color=None`):

- T1 `where={'color':'red'}` (key missing from some items) -> `[Apple]`
  (no longer raises; the keyless item is filtered out). PASS
- T2 `where={'nope': 1}` (key absent from all items) -> `[]` (no error). PASS
- T3 `where={'color':'yellow'}` -> `[Banana]` (normal equality). PASS
- T4 `where={'color': None}` -> `[Date]` only; the item missing `color` is
  excluded, so missing != `None`. PASS
- T5 `limit=-1` -> `ValueError` (preserved). PASS
- T6 `query='   '` -> `[]` (blank-query guard preserved). PASS
- T7 `where={'name':'Apple','color':'red'}` -> `[Apple]` (multi-key AND). PASS
- T8 `sort_by='name', limit=2` -> `['Apple','Banana']` (sort + top-N). PASS
- T9 `where={}` (falsy) -> no filter applied (all items). PASS

## Summary

`Catalog.search` no longer raises on a missing `where` key. The pre-check loop
was removed and the equality filter now requires the key to be present
(`key in item and item[key] == value`), so keyless items are silently dropped
and an unknown key yields `[]`. The negative-`limit` `ValueError`, blank-query
guard, substring matching, sorting, limiting, and copy-on-return are all
unchanged. Docstrings and `docs/NOTES.md` updated accordingly.
