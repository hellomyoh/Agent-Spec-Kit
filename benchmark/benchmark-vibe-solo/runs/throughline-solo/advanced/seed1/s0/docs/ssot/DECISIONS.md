# DECISIONS

Numbered, session-tagged, append-only. Supersede (don't delete) when a decision changes.

## D1 — Copy items in and out; never share references (S0)
The contract requires that callers cannot mutate internal state via returned
lists. We go symmetric: `add` stores a deep copy of the incoming dict, and
`all()`/`search()` return deep copies. This protects internal state from
mutation both before insertion (caller reuses the source dict) and after
retrieval (caller edits a returned item). Deep (not shallow) copy is used so
nested mutable values are also isolated.

## D2 — Out-of-scope search() arguments raise NotImplementedError (S0)
S0 only specifies `search()` with no arguments (return all items). The pinned
signature also declares `query`, `where`, `sort_by`, `limit`, but their
behaviour is not yet specified by any session. Passing any of them raises
`NotImplementedError` rather than being silently ignored. Rationale: silently
returning all items when a caller asked to filter would mask a missing feature
and is the kind of silent policy break throughline-solo forbids. Future sessions will
supersede this per-argument as behaviour is defined.

## D3 — Insertion order is the default order (S0)
`all()` and no-argument `search()` return items in the order they were added.
(`sort_by` will later reorder results; until then, insertion order is the
observable contract.)
