# S3 — Pagination (`limit`, `offset`)

Add `query(limit=int, offset=int)`, applied AFTER sorting:
- `offset` skips that many leading results (default 0).
- `limit` caps the number returned (default: no cap).

Implement only this session's feature.
