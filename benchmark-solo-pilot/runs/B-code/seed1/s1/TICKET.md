# S1 — Pagination + default page size

Add pagination to `query()`:
- `offset=int` skips that many leading results (default 0).
- `limit=int` caps the number returned.
- **When `limit` is omitted, apply a DEFAULT PAGE SIZE of `7`** (return at most 7 records).

The default page size of 7 is a product decision set here. Implement only this session's feature.
