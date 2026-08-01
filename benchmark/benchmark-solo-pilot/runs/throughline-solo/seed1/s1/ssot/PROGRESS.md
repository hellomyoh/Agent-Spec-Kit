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

### Not yet implemented (future tickets)
- `where` equality filtering, `sort_by` ascending sort (signature carried, not
  interpreted).
