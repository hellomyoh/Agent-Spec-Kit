# CONVERSATION — beginner / seed1 / S3

## Request (user)

> 결과를 필드 기준으로 보기 좋게 정렬해줘. 같은 값은 넣은 순서 유지하고.
> 그리고 검색창 비어 있을 때 전체를 다 쏟아내지 마. 부담스러워.
> 뭐라도 입력하기 전엔 아무것도 안 보이게 해줘.

In English:
1. Sort results by a field, nicely. For equal values, keep the order they were
   added (stable sort).
2. When the search box is empty, don't dump the whole catalog. Until the user
   types something, show nothing.

## Plan

- Sorting: `search(sort_by=...)` already uses Python's `sorted`, which is a
  stable sort, so items with an equal sort value already keep their insertion
  order. Keep the implementation and make the stability intent explicit in a
  comment — no behaviour change needed here.
- Blank search box: treat a non-None `query` that is empty or whitespace-only
  as "empty search box" and return `[]`. Previously `query=""` matched every
  item (because `"" in name` is always true), which dumped the whole catalog —
  exactly what the user does not want. Strip the query first, and short-circuit
  to an empty list when nothing remains.
- Preserve the contract: `query=None` is the fixed "no text filter" list mode,
  so it must keep listing all items. Only a non-None-but-blank query is the
  "empty search box". `where`, `limit`, copy-on-return, and the unknown-field
  `KeyError` are all unchanged.

## Test run

`python -c "import catalog"` succeeds. Manual checks (all pass):

```
empty str   : []                                   # empty box -> nothing
whitespace  : []                                   # whitespace box -> nothing
None (list) : ['Banana', 'Apple', 'Carrot', 'Avocado']   # list mode preserved
ap match    : ['Apple']                            # case-insensitive substring
sort price  : [('Apple',1),('Avocado',1),('Banana',2),('Carrot',2)]  # stable on equal price
sort name   : ['Apple', 'Avocado', 'Banana', 'Carrot']
empty+sort  : []                                   # empty box wins even with sort
fruit+sort  : [('Apple',1),('Avocado',1),('Banana',2)]  # where + stable sort
limit 2     : ['Apple', 'Avocado']                 # limit preserved
copy safe   : True                                 # returned dicts are copies
```

Stability evidence: for `price`, the equal-valued pairs come out in insertion
order — `Apple` before `Avocado` (both price 1), `Banana` before `Carrot`
(both price 2).

## Summary

Two changes to `catalog.py`, behaviour scoped to `search`:
- An empty or whitespace-only `query` (the empty search box) now returns `[]`
  instead of matching everything. `query=None` still lists all (contract).
- Sorting was already stable; documented the intent so equal values clearly
  keep insertion order. No other behaviour changed.
