# PROGRESS

## S0 — Scaffold (done)
Created `miniquery.py` with the `Store` class per contract v2.0.
- Implemented: `add()` (store deep copy), `all()` (return deep copies, insertion
  order), `query()` with no arguments (returns all records as copies).
- `query()` carries the full pinned signature (`where`, `sort_by`, `limit`,
  `offset`) but does not yet interpret those parameters.
- Verified `python -c "import miniquery"` imports cleanly; smoke-checked add/all/
  query and copy isolation (nested mutation of a caller's record does not affect
  stored data).

## S1 — Pagination + default page size (done)
Added paging to `query()`:
- `offset` (default 0) skips leading records; `limit` caps the number returned; the
  two compose.
- Omitted `limit` applies the DEFAULT page size of 7 (module constant
  `DEFAULT_PAGE_SIZE = 7`). Explicit `limit` (including 0) overrides the default.
- Verified `python -c "import miniquery"` imports cleanly; smoke-checked: omitted
  limit -> first 7, `limit=3` -> first 3, `offset=8` -> last 2 of 10, `offset=2,
  limit=3` -> records 2-4, `limit=0` -> empty.

## S2 — Equality filter (`where`) (done)
Added `where` filtering to `query()`:
- `where={k: v, ...}` returns records matching ALL key==value pairs (conjunctive);
  a key absent from a record fails the match (no error), via the helper
  `Store._matches`.
- Filtering is applied before paging, so `offset`/`limit`/default page size operate
  on the filtered set. `where=None` filters nothing; `where={}` matches everything.
- Verified `python -c "import miniquery"` imports cleanly; smoke-checked: single-key
  and multi-key (AND) matches, absent-key -> empty (no error), `where` + offset/limit
  compose, `limit=0` still empty, and no-`where` default page size unchanged.

## S3 — Adjust default page size (done)
Changed `DEFAULT_PAGE_SIZE` from 7 to 25 (see D7, supersedes D5). This is the cap
applied when `limit` is omitted; explicit `limit` (including 0) still overrides it.
No other behaviour changed.
- Verified `python -c "import miniquery"` imports cleanly and
  `miniquery.DEFAULT_PAGE_SIZE == 25`.

## S4 — Sorting (`sort_by`) (done)
Implemented `sort_by` ascending sort in `query()` (see D8):
- Pipeline is now filter -> sort -> page. `query(sort_by=field)` sorts the filtered
  records ascending by `record[field]` before `offset`/`limit` are applied.
- Stable sort: records with equal sort keys keep insertion order. Records missing the
  field are grouped after those that have it (in insertion order), via the sort key
  `(field not in record, record.get(field))`, avoiding None-vs-value comparison errors.
  `sort_by=None` leaves records in filtered insertion order.
- Verified `python -c "import miniquery"` imports cleanly; smoke-checked: ascending sort
  with ties preserving insertion order, sort applied before paging (limit/offset over the
  sorted set), `where`+`sort` compose, missing-field grouping, and no-`sort_by` unchanged.

## S5 — Adjust default page size again (done)
Changed `DEFAULT_PAGE_SIZE` from 25 to 40 (see D9, supersedes D7). This is the cap
applied when `limit` is omitted; explicit `limit` (including 0) still overrides it.
No other behaviour changed.
- Verified `python -c "import miniquery"` imports cleanly and
  `miniquery.DEFAULT_PAGE_SIZE == 40`.

### Not yet implemented (future tickets)
- None outstanding: the full pinned `query()` surface (`where`, `sort_by`, `limit`,
  `offset`, default page size) is now implemented.
