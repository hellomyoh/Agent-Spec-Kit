# CONVERSATION — advanced S4

## Request

`limit` 추가 (정렬 후 상위 N개로 cap). 회귀: where/sort/blank/unknown-field 동작이 모두 유지돼야 함.

Add a `limit` parameter to `Catalog.search` that caps results to the top N
**after** sorting. Regression: existing where / sort / blank-query /
unknown-field behaviours must all be preserved.

## Plan

- The contract already fixes `limit: int | None = None` in the `search`
  signature, and the parameter was already present but ignored. Implement it.
- Place the cap **last** in the pipeline, after sorting, so it yields the top N:
  `empty-query guard -> where -> query -> sort_by -> limit`. Slicing before the
  copy step means we only copy the rows we return.
- Semantics chosen:
  - `limit=None` -> no cap (default, prior behaviour unchanged).
  - `limit=N (N >= 0)` -> `results[:N]`; `N` larger than the result set returns
    all of it; `limit=0` -> `[]` (top 0).
  - Negative `limit` -> `ValueError`. A negative cap is meaningless for "max
    results", and Python slicing would silently drop from the end — so fail
    fast, matching the codebase's existing validate-and-raise style (`where`).
    Validation runs up front, before the blank-query guard, so a bad argument is
    rejected regardless of the other arguments.
- Touch only `catalog.py`; keep docstrings describing current behaviour.

## Test run

Ran a script (kept in scratchpad, outside the work dir) exercising the new
behaviour plus every regression case:

- limit: cap after sort = top-N (`sort_by="price", limit=2` -> banana, Carrot);
  `limit` > len -> all; `limit=None` -> all; `limit=0` -> `[]`; applied after
  sort (top-N of sorted, stable); composes with `where`+`query`; negative ->
  `ValueError`.
- blank/None query: `"   "` and `""` -> `[]`; `None` and no-arg -> list mode (all).
- query: case-insensitive substring match.
- where: AND across keys, insertion order preserved; unknown key -> `ValueError`;
  empty catalog vacuously valid.
- sort_by: stable ascending after filtering; unknown field -> `KeyError`
  (pre-existing behaviour).
- copies returned (mutating a result does not change the catalog).

Result: `ALL TESTS PASSED`. `python -c "import catalog"` -> `import OK`.

## Summary

Implemented `limit` as the final pipeline stage (cap to top N after sorting):
`None` = no cap, `0` = empty, oversize = all, negative = `ValueError`. All prior
where/sort/blank/unknown-field behaviour is unchanged. Only `catalog.py` was
modified.
