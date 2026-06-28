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

### Not yet implemented (future tickets)
- `where` equality filtering, `sort_by` ascending sort, `limit`/`offset` paging.
- DEFAULT page size for an omitted `limit` (no default set yet).
