# CONVERSATION

## Request (this session)

(Original prompt, Korean) `search(sort_by=field)` 를 추가해줘. 오름차순, 동점은 안정 정렬(넣은 순서 유지). 그리고 query가 공백/빈 문자열이면 전체가 아니라 빈 리스트를 반환해.

Translated / interpreted:
1. Implement `search(sort_by=field)` — order results by `field` ascending. Ties keep insertion order (stable sort).
2. When `query` is an empty string or only whitespace, return an empty list (instead of matching everything, which is what an empty substring did before).

## Plan

- The `sort_by` parameter already existed in the pinned contract signature but was ignored. Implement it.
- `query=None` must still mean "no text filter" (list mode) per the contract — do NOT change that. Only a non-None blank/whitespace `query` becomes an empty result.
- Preserve existing behaviour: `where` equality filter + ValueError for unknown `where` fields, case-insensitive substring matching, returning copies, insertion-order default.
- Keep `limit` untouched (not requested this session; remains accepted-but-unused as before).
- Order of operations: validate `where` -> apply `query` -> apply `where` -> apply `sort_by` -> copy out.

Implementation details:
- Blank handling: `needle = query.strip().lower()`; if `needle` is empty, return `[]`. This treats `""`, spaces, tabs and newlines uniformly as blank. (Side effect: a non-blank query is also stripped of surrounding whitespace before matching, which is the natural reading of "blank query -> empty".)
- Stable ascending sort: `sorted(items, key=lambda item: item[sort_by])`. `items` is already in insertion order and Python's `sorted` is stable, so ties keep insertion order.

## Test run

`python -c "import catalog"` -> IMPORT_OK.

Ad-hoc behaviour test (4 items, with a deliberate price tie where `apple` is added before `Cherry`):

- `sort_by='price'` -> `['date', 'apple', 'Cherry', 'Banana']` (price 1,2,2,3; the two price=2 items keep insertion order -> stable tie-break confirmed).
- `sort_by='name'` -> `['Banana', 'Cherry', 'apple', 'date']` (ascending by string; uppercase sorts before lowercase, plain ascending).
- `query=''`, `query='   '`, `query='\t\n'` -> `[]` (blank/whitespace returns empty list).
- `query=None` and no-arg `search()` -> all 4 items (list mode preserved).
- `query='A'` -> `['Banana', 'apple', 'date']` (case-insensitive substring preserved).
- `query='  apple '` -> `['apple']` (surrounding whitespace trimmed, then matched).
- `query='a', sort_by='name'` -> `['Banana', 'apple', 'date']` (filter + sort combine).
- `where={'price': 2}, sort_by='name'` -> `['Cherry', 'apple']` (where + sort combine).
- `where={'nope': 1}` -> raises `ValueError` (unknown-field guard preserved).
- `all()` / `search()` return copies; mutating a returned dict does not leak into the store.

Result: ALL TESTS PASSED.

## Summary

Added `sort_by` (ascending, stable on ties) and made a blank/whitespace `query` return an empty list, in `catalog.py`. All previously working behaviour (`query=None` list mode, case-insensitive substring search, `where` filter + unknown-field ValueError, copy-on-return) is preserved. `limit` remains accepted but unused, as it was, since this session's request did not cover it.
