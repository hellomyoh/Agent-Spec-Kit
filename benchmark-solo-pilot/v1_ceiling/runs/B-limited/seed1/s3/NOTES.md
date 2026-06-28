# S3 — Pagination (`limit`, `offset`)

Implemented `query(limit, offset)`, applied AFTER sorting (so order: where -> sort_by -> paginate -> copy out).

Decisions:
- `offset` (default 0) skips leading results; `limit` (default None => no cap) caps count.
- Used list slicing `records[offset:stop]` where stop = offset+limit (or None). Slicing handles out-of-range safely: offset past end => [], limit > remaining => all remaining.
- Guard `if offset or limit is not None:` so the no-pagination path is untouched.
- S1 `where` KeyError policy + S2 stable-sort policy preserved. Only `select` remains unimplemented.
