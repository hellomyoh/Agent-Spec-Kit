# S1 — Equality filter (`where`)

Implemented `query(where={k:v,...})`: returns records where ALL key==value match.

Decisions:
- POLICY (applies to ALL future `where`): a key absent from EVERY stored record raises `KeyError(key)` (hard error, not silent no-match). Check is per-key: if no record contains the key, raise.
- A key missing from SOME (but not all) records just fails the match for those records (no error).
- Falsy `where` ({} or None) => no filtering, returns all.
- Still returns deep copies in insertion order. sort_by/limit/offset/select remain unimplemented (future tickets).
