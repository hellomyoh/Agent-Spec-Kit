# CONVERSATION (S2)

## Request
"카테고리 같은 필드로도 거를 수 있게 해줘. 아 그리고 없는 필드로 거르면 그건
실수니까 조용히 이상한 거 주지 말고 그냥 에러로 빵 터뜨려서 바로 알게 해줘."

In short:
1. Let me filter by fields like `category` too (not just name).
2. Filtering by a non-existent field is a mistake — don't quietly return weird
   results, raise an error immediately so I know.

## Plan
- `search(where=...)` already does generic equality filtering on any field, so
  filtering by `category` works via `where={'category': 'fruit'}`. Keep that and
  confirm it as a real, intended feature.
- Add the guard: before filtering, compute the set of fields that actually exist
  across all items. If any `where` key is not in that set, raise `KeyError` with
  a clear message instead of silently filtering (which would give empty/odd
  results because missing fields read as None).
- "Exists" = present on at least one item. A field present on only some items is
  legitimate filtering, not a mistake, so it must NOT raise.
- Contract signatures are FIXED — only behaviour changes. No new params.

## Test run
`python -c "import catalog; ..."` exercised:
- `where={'category':'fruit'}` -> ['Apple', 'Banana']        (category filter)
- `query='a', where={'category':'fruit'}` -> ['Apple','Banana'] (combined)
- `where={'category':'dairy'}` -> []                          (known field, no match)
- `where={'color':'red'}` -> raised KeyError                  (unknown field blows up)
- `where={'price':2}` with price on one item -> ['Milk']      (partial presence OK)
- `search()` -> lists all 4                                   (query=None unchanged)
All passed.

## Summary
`search` now treats a `where` filter on a field that no item has as an error
(raises `KeyError`) rather than silently returning misleading results. Filtering
by real fields such as `category` works as before. Name search, sorting, limit,
copy-on-return, and list-all behaviour are unchanged.
