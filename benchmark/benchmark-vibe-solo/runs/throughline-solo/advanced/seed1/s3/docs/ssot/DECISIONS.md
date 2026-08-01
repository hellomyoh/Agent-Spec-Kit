# DECISIONS

Numbered, session-tagged, append-only. Supersede (don't delete) when a decision changes.

## D1 — Copy items in and out; never share references (S0)
The contract requires that callers cannot mutate internal state via returned
lists. We go symmetric: `add` stores a deep copy of the incoming dict, and
`all()`/`search()` return deep copies. This protects internal state from
mutation both before insertion (caller reuses the source dict) and after
retrieval (caller edits a returned item). Deep (not shallow) copy is used so
nested mutable values are also isolated.

## D2 — Out-of-scope search() arguments raise NotImplementedError (S0; superseded for `query` by D4 in S1, for `where` by D5 in S2, for `sort_by` by D7 in S3)
S0 only specifies `search()` with no arguments (return all items). The pinned
signature also declares `query`, `where`, `sort_by`, `limit`, but their
behaviour is not yet specified by any session. Passing any of them raises
`NotImplementedError` rather than being silently ignored. Rationale: silently
returning all items when a caller asked to filter would mask a missing feature
and is the kind of silent policy break throughline-solo forbids. Future sessions will
supersede this per-argument as behaviour is defined.

Status (S3): `query` (D4), `where` (D5), and `sort_by` (D7) behaviour is now
defined, so none of them raise. `limit` remains unspecified and still raises
under this decision, including when combined with `query`, `where`, or
`sort_by`.

## D3 — Insertion order is the default order (S0)
`all()` and no-argument `search()` return items in the order they were added.
(`sort_by` will later reorder results; until then, insertion order is the
observable contract.)

## D4 — `query` is case-insensitive substring matching on `name` (S1; blank handling superseded by D6 in S3)
A non-None, non-blank `query` filters items to those whose `name` contains
`query` as a substring, comparing case-insensitively (via `str.casefold()`).
Matching items are returned in insertion order (D3 still governs ordering).
Supersedes D2 for the `query` argument only.

Blank handling (SUPERSEDED by D6 in S3): `query=None` is list mode (return every
item) per the contract. We extend the same list-mode behaviour to a blank or
whitespace-only `query` (e.g. `""`, `"   "`): there is no meaningful substring to
match on, and a blank needle would otherwise match every item anyway, so list
mode is the natural, non-surprising result. This is a deliberate choice for an
input the prompt left implicit, not a silent ignore of a requested filter — a
caller passing real search text always gets filtering.

Status (S3): the substring-matching rule above still holds. The blank-handling
half is reversed by D6 — a blank/whitespace-only `query` now returns `[]`, not
the full catalog. `query=None` remains list mode (contract). `sort_by` is now
specified by D7; `limit` is still unspecified and still raises (D2).

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
order preserved. `sort_by` is now specified by D7 (S3); `limit` remains
unspecified and still raises `NotImplementedError` (D2), including when combined
with `where`.

## D6 — Blank/whitespace-only `query` returns `[]` (S3; supersedes D4 blank handling)
A blank or whitespace-only `query` string (`""`, `"   "`, etc.) now returns an
empty list — it matches nothing. Rationale (user-directed, explicit safety
policy this session): an empty search box must not dump the entire catalog;
"no search text typed" should surface no results, not everything.

This is an intentional reversal of D4's blank handling, which had treated a blank
`query` as list mode (return all). Because the user stated the new behaviour and
its safety rationale outright, it is a deliberate change, so we supersede D4
(not silently comply, not refuse): D4's blank half is retired and recorded as
superseded, and FEATURES is updated to match.

Scope guard — `query=None` is NOT affected. The contract (CONTRACT_VERSION 1.0)
fixes `query=None` as "no text filter" (list mode), and the user prompt named
only blank/whitespace-only *strings*. So `None` still lists every item; only an
actually-supplied-but-empty string returns `[]`. The distinction is "caller
passed no query" (None, list mode) vs. "caller submitted an empty search box"
(blank string, no results).

## D7 — `sort_by` orders results ascending with a stable sort (S3)
A non-None `sort_by` is a field name; results are ordered by that field
ascending using a stable sort. Stability means items with equal `sort_by` values
keep their relative insertion order (D3 governs the tiebreak), so sorting never
reshuffles equal elements. Implemented with Python's `sorted()` (Timsort, stable)
and the default `<` ordering of the field values. Supersedes D2 for the
`sort_by` argument only.

Ordering pipeline: filtering (`query`, then `where`) runs first; `sort_by` then
orders the surviving results. So `sort_by` sorts exactly the matched set.

Missing-key policy: if the `sort_by` field is absent from any result item,
`search` raises `ValueError` (checked against the post-filter result set).
Rationale: this mirrors D5's `where` missing-key policy and D2's principle —
sorting on a field the data lacks is almost certainly a caller mistake;
substituting a default or partial order would silently mask it. (For `where`
the check spans the whole catalog because the policy predates filtering; for
`sort_by` we only need the items actually being ordered, so the check is over
the result set.)

Type policy: values under `sort_by` must be mutually comparable; if they are not
(e.g. mixing `int` and `str`), Python's `sorted()` raises `TypeError`, which we
let propagate rather than inventing an unspecified coercion or cross-type order.

`limit` remains unspecified and still raises `NotImplementedError` (D2),
including when combined with `sort_by`.
