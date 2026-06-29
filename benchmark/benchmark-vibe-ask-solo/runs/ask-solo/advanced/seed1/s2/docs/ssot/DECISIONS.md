# DECISIONS

Numbered, session-tagged, append-only. Supersede (don't delete) when a decision changes.

## D1 — Copy items in and out; never share references (S0)
The contract requires that callers cannot mutate internal state via returned
lists. We go symmetric: `add` stores a deep copy of the incoming dict, and
`all()`/`search()` return deep copies. This protects internal state from
mutation both before insertion (caller reuses the source dict) and after
retrieval (caller edits a returned item). Deep (not shallow) copy is used so
nested mutable values are also isolated.

## D2 — Out-of-scope search() arguments raise NotImplementedError (S0; superseded for `query` by D4 in S1, for `where` by D5 in S2)
S0 only specifies `search()` with no arguments (return all items). The pinned
signature also declares `query`, `where`, `sort_by`, `limit`, but their
behaviour is not yet specified by any session. Passing any of them raises
`NotImplementedError` rather than being silently ignored. Rationale: silently
returning all items when a caller asked to filter would mask a missing feature
and is the kind of silent policy break ASK-solo forbids. Future sessions will
supersede this per-argument as behaviour is defined.

Status (S2): `query` (D4) and `where` (D5) behaviour is now defined, so neither
raises. `sort_by` and `limit` remain unspecified and still raise under this
decision, including when combined with `query` or `where`.

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
(S2: `where` is now specified by D5.)

## D5 — `where` is equality filtering with AND, keys must exist on every item (S2)
A non-None `where` dict keeps items whose fields equal every given key/value
pair; multiple keys are combined with AND (an item must match all of them).
Equality is Python `==`. Matches keep insertion order (D3). Supersedes D2 for
the `where` argument only.

Missing-key policy (user-directed this session): if any `where` key is absent
from any item in the catalog, `search` raises `ValueError`. Rationale: a key the
data never carries is almost certainly a caller mistake, and treating "missing"
as "not equal" (silently returning fewer/zero results) would hide that mistake —
the same silent-drop failure mode D2 guards against. The check is over the whole
catalog, not just query-matched items, so the error does not depend on which
items a co-supplied `query` happens to select. An empty `where` dict (`{}`)
imposes no constraints and lists all items (no key to be missing).

`where` composes with `query`: the catalog is filtered by both (intersection),
order preserved. `sort_by` and `limit` remain unspecified and still raise
`NotImplementedError` (D2), including when combined with `where`.
