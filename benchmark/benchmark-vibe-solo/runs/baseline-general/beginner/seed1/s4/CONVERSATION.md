# CONVERSATION — S4

## Request
"결과 개수 좀 제한할 수 있게 해줘. 상위 N개만 보이게."
(Let me limit the number of results — show only the top N.)

## Plan
- The contract already fixes `limit: int | None = None` on `search`, and the
  current code already does `results = results[:limit]`, so the happy path
  ("top N") was effectively present. S4 makes "top N" an explicitly-requested
  feature, so I pinned its semantics and closed the one surprising edge case.
- Decisions:
  - `limit=N` (N >= 0): keep at most the first N items, applied AFTER filtering
    and sorting, so it really is the "top N" of the final result order.
  - `limit=0`: show nothing (`[]`). Consistent and unsurprising.
  - `limit=None`: no cap (lists all) — unchanged.
  - `limit > len(results)`: just returns everything (no error).
  - `limit < 0`: previously Python negative-slicing silently returned
    all-but-the-last-|N| items (e.g. `limit=-1` dropped the last item). That is
    a meaningless "top -1" and a caller mistake, so it now raises `ValueError`,
    matching how the catalog already rejects other mistakes (unknown filter
    field -> `KeyError`).
- Did NOT over-engineer: no new params, no max-cap, no clamping; just one guard
  plus a docstring that states the behaviour.

## Test run (`python -c` against current code)
- `search(limit=2)` on 5 items -> first 2. OK
- `search(limit=0)` -> `[]`. OK
- `search(limit=None)` -> all 5. OK
- `search(limit=99)` -> all 5 (no error). OK
- `search(query='a', limit=2)` -> top 2 of the matches. OK
- `search(where={'cat':'fruit'}, sort_by='name', limit=3)` -> top 3 of sorted
  matches: `['Apple','Banana','Cherry']`. OK (limit applies after sort)
- `search(limit=-1)` -> raises `ValueError`. OK
- Regression: blank query -> `[]`; unknown `where` field -> `KeyError`;
  stable sort preserved. OK
- `python -c "import catalog"` -> import OK.

## Summary
Top-N result limiting is now an explicit, documented feature. The happy path
(`limit=N` keeps the first N after filter+sort; `0` shows nothing; `None` =
no cap) was preserved as-is, and the only change is rejecting a negative
`limit` with `ValueError` instead of silently returning a strange subset.
All prior behaviour (search, where/KeyError, stable sort, blank-query) is intact.
