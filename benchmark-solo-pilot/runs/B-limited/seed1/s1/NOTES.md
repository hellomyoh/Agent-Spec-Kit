# NOTES

## S1 — Pagination + default page size
- `query`: applies `offset` (skip N leading, default 0) then `limit` (cap).
- DEFAULT PAGE SIZE = 7 when `limit is None` (module const `DEFAULT_PAGE_SIZE`). Explicit `limit` overrides, incl. `limit=0` -> empty.
- Order = insertion order (via `all()`); deepcopy isolation preserved.
- NOT yet implemented (future tickets): `where` equality filter, `sort_by`. Args present in FIXED signature but inert. Do not pre-build.
- When `sort_by`/`where` land, apply them BEFORE offset/limit.
