# DECISIONS

Numbered, session-tagged, append-only. Supersede (don't delete) when a decision changes.

## D1 — Copy items in and out; never share references (S0)
The contract requires that callers cannot mutate internal state via returned
lists. We go symmetric: `add` stores a deep copy of the incoming dict, and
`all()`/`search()` return deep copies. This protects internal state from
mutation both before insertion (caller reuses the source dict) and after
retrieval (caller edits a returned item). Deep (not shallow) copy is used so
nested mutable values are also isolated.

## D2 — Out-of-scope search() arguments raise NotImplementedError (S0; superseded for `query` by D4 in S1)
S0 only specifies `search()` with no arguments (return all items). The pinned
signature also declares `query`, `where`, `sort_by`, `limit`, but their
behaviour is not yet specified by any session. Passing any of them raises
`NotImplementedError` rather than being silently ignored. Rationale: silently
returning all items when a caller asked to filter would mask a missing feature
and is the kind of silent policy break throughline-solo forbids. Future sessions will
supersede this per-argument as behaviour is defined.

Status (S1): `query` behaviour is now defined (see D4), so `query` no longer
raises. `where`, `sort_by`, and `limit` remain unspecified and still raise under
this decision.

## D3 — Insertion order is the default order (S0)
`all()` and no-argument `search()` return items in the order they were added.
(`sort_by` will later reorder results; until then, insertion order is the
observable contract.)

## D4 — `query` is case-insensitive substring matching on `name` (S1)
A non-None, non-blank `query` filters items to those whose `name` contains
`query` as a substring, comparing case-insensitively (via `str.casefold()`).
Matching items are returned in insertion order (D3 still governs ordering).
Supersedes D2 for the `query` argument only.

Blank handling: `query=None` is list mode (return every item) per the contract.
We extend the same list-mode behaviour to a blank or whitespace-only `query`
(e.g. `""`, `"   "`): there is no meaningful substring to match on, and a blank
needle would otherwise match every item anyway, so list mode is the natural,
non-surprising result. This is a deliberate choice for an input the prompt left
implicit, not a silent ignore of a requested filter — a caller passing real
search text always gets filtering.

`where`, `sort_by`, and `limit` are still unspecified and still raise
`NotImplementedError` (D2); combining `query` with any of them therefore still
raises, so no requested-but-unsupported filter is silently dropped.
