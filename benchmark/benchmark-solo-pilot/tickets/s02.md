# S2 — Equality filter (`where`)

Add `where` support: `query(where={k: v, ...})` returns records matching ALL key==value pairs.
A `where` key absent from a record simply fails the match for that record (no error).

`where` is applied before sorting/pagination. Implement only this session's feature.
