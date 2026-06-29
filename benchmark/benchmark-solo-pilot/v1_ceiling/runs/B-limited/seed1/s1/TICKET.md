# S1 — Equality filter (`where`)

Add `where` support: `query(where={k: v, ...})` returns records matching ALL key==value pairs.

POLICY (decided once here; applies to ALL future `where` handling):
- If a `where` key is NOT present in ANY stored record, raise `KeyError(key)`.
  An unknown field is a hard error — not a silent no-match.

Implement only this session's feature.
