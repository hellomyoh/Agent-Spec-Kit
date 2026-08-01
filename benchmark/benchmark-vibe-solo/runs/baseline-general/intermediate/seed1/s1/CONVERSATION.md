# CONVERSATION

## Request
Add text search: `search(query=...)` matches against an item's `name` field using
case-insensitive substring matching.

## Plan
- Keep the FIXED contract surface (`add`, `all`, `search`) unchanged.
- In `search`, when `query is not None`, filter `_items` to those whose `name`
  contains `query` as a case-insensitive substring (`query.lower() in name.lower()`).
- `query=None` stays list mode (return all). An empty string `""` is a substring of
  every name, so it returns all items.
- Preserve insertion order and the copy-on-return behaviour (no internal-state leaks).
- `where`, `sort_by`, `limit` remain accepted but unused this session (no request to
  implement them yet).

## Test run
`python -c "import catalog"` plus an inline harness covering:
- no query -> all items in insertion order; `search() == all()`
- `query='ap'` / `'AP'` -> `['Apple','Apricot']` (case-insensitive substring)
- `query='an'` -> `['banana']`; `query='rr'` -> `['Cherry']`
- `query=''` -> all items
- `query='zzz'` -> `[]`
- mutating a returned dict does not affect stored items

Result: ALL TESTS PASSED.

## Summary
Implemented case-insensitive substring search on `name` in `catalog.py`. Other params
(`where`, `sort_by`, `limit`) are still accepted per the contract but not yet active.
Prior `add`/`all`/list-mode behaviour is preserved.
