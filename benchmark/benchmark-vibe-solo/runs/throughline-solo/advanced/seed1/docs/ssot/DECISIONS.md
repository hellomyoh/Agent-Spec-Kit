# DECISIONS

Numbered, session-tagged, append-only. Supersede (don't delete) when a decision changes.

## D1 — Copy items in and out; never share references (S0)
The contract requires that callers cannot mutate internal state via returned
lists. We go symmetric: `add` stores a deep copy of the incoming dict, and
`all()`/`search()` return deep copies. This protects internal state from
mutation both before insertion (caller reuses the source dict) and after
retrieval (caller edits a returned item). Deep (not shallow) copy is used so
nested mutable values are also isolated.

## D2 — Out-of-scope search() arguments raise NotImplementedError (S0; superseded for `query` by D4 in S1, for `where` by D5 in S2, for `sort_by` by D7 in S3, for `limit` by D8 in S4 — now fully retired)
S0 only specifies `search()` with no arguments (return all items). The pinned
signature also declares `query`, `where`, `sort_by`, `limit`, but their
behaviour is not yet specified by any session. Passing any of them raises
`NotImplementedError` rather than being silently ignored. Rationale: silently
returning all items when a caller asked to filter would mask a missing feature
and is the kind of silent policy break throughline-solo forbids. Future sessions will
supersede this per-argument as behaviour is defined.

Status (S4): all four arguments are now specified — `query` (D4), `where` (D5),
`sort_by` (D7), and `limit` (D8) — so `search()` no longer raises
`NotImplementedError` for any argument. This decision is fully superseded and
retained only as history.

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

## D5 — `where` is equality filtering with AND (S2; missing-key ValueError superseded by D9 in S5)
A non-None `where` dict keeps items whose fields equal every given key/value
pair; multiple keys are combined with AND (an item must match all of them).
Equality is Python `==`. Matches keep insertion order (D3). Supersedes D2 for
the `where` argument only.

Missing-key policy (SUPERSEDED by D9 in S5): originally (S2, user-directed), if
any `where` key was absent from any item in the catalog, `search` raised
`ValueError`, on the rationale that an unknown key is likely a caller mistake and
treating "missing" as "not equal" would hide it. As of S5 (D9) this is reversed:
a missing key is treated as a non-match, not an error. See D9.

An empty `where` dict (`{}`) imposes no constraints and lists all items (this
half is unchanged by D9).

`where` composes with `query`: the catalog is filtered by both (intersection),
order preserved. `sort_by` is specified by D7 (S3); `limit` is specified by D8
(S4) and caps the (filtered, sorted) result set.

## D6 — Blank/whitespace-only `query` returns `[]` (S3; supersedes D4 blank handling — itself SUPERSEDED by D10 in S6)
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

Status (S6): SUPERSEDED by D10. A blank/whitespace-only `query` now returns the
full catalog (list mode) again, for a new list-view requirement. The substring
matching for real query text and the `query=None` list-mode rule are unchanged;
only the blank-string outcome flipped back from `[]` to list mode. See D10.

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

`limit` is specified by D8 (S4): it is applied after `sort_by`, capping the
ordered results to the first N (the top N).

## D8 — `limit` caps the filtered, sorted results to the top N (S4; supersedes D2 for `limit`)
A non-None `limit` is a non-negative `int` that caps `search` to the first N
results, applied **last** — after filtering (`query`, then `where`) and after
`sort_by` ordering. So with `sort_by` present it is literally the top N of the
sorted set; without it, the first N in the existing (filtered, insertion) order.
`limit=None` is no cap (every surviving result), per the contract's list-mode
default. Implemented with a plain slice `results[:limit]`. Supersedes D2 for the
`limit` argument; with this, D2 is fully retired (all four args specified).

Edge cases (prompt said only "cap to top N", so these are chosen deliberately,
consistent with the SSOT's anti-silent-surprise stance — D2/D5/D7):
- `limit == 0` -> `[]`. A cap of zero means zero results; unambiguous.
- `limit >= len(results)` -> all results. A cap at/above the available count is a
  no-op (standard slice semantics); not an error, since asking for "up to N" when
  fewer exist is a normal, well-defined request.
- `limit < 0` -> `ValueError`. A negative cap has no "top N" meaning; Python's
  slice would instead silently drop items from the *end* (`[:-1]`), exactly the
  kind of silent, surprising data loss D5/D7 guard against. A negative limit is
  almost certainly a caller mistake, so we surface it rather than mask it.
- non-`int` `limit` (e.g. `float`, `str`) -> `TypeError`. The contract types it
  `int | None`; we reject other types rather than rely on / coerce to slice
  behaviour. `bool` is rejected too (though it is an `int` subclass) so
  `limit=True`/`False` is not silently read as `1`/`0`.

Composition: `limit` composes with everything. The full pipeline is
query -> where -> sort_by -> limit. The result is still returned as deep copies
(D1), and limit slicing happens before that copy.

## D9 — A missing `where` key is a non-match, not an error (S5; supersedes D5 missing-key policy)
A non-None `where` filter now treats an item that lacks a given key as simply not
matching that constraint: the item is filtered out rather than triggering an
error. Implemented as `key in item and item[key] == value` per key, AND-ed across
keys. Consequently a `where` key that is absent from **every** item in the
catalog matches nothing and `search` returns `[]`. The `ValueError` D5 raised for
missing keys is retired.

Rationale (user-directed this session, explicit intentional change): the prompt
states that a `where` key not present on the items should no longer raise — it
should be ignored, yielding `[]` — and that the `ValueError` is abolished
("ValueError 폐기"). This is the inverse of D5's original stance (which treated an
unknown key as a likely caller mistake worth surfacing). Because the user stated
the new behaviour and its intent outright, it is a deliberate supersede (not a
silent drift): D5's missing-key half is recorded as superseded and FEATURES is
updated to match.

All-missing vs. some-missing: the prompt names the all-missing case ("모든
아이템에 없는 where 키" -> `[]`), but the mechanism it specifies — ignore the
missing key / treat it as non-matching — applies uniformly. So when a key is
present on some items but absent from others, the items lacking it are dropped
(non-match) and the rest filter normally; no error in either case. A single,
consistent "missing == not equal" rule is cleaner than splitting behaviour by how
many items happen to lack the key, and it fully retires the `ValueError` as the
prompt directs.

Scope — "나머지 정책은 그대로" (rest of the policy unchanged): equality is still
Python `==`, multiple keys are still AND-ed, matches keep insertion order (D3),
empty `{}` still lists all items, and composition with `query`/`sort_by`/`limit`
is unchanged. `sort_by`'s own missing-key policy (D7) is a separate decision and
still raises `ValueError` — only `where`'s missing-key handling changed.

## D10 — Blank/whitespace-only `query` returns all items (list mode) (S6; supersedes D6)
A blank or whitespace-only `query` string (`""`, `"   "`, etc.) now returns every
item — list mode — instead of `[]`. Implemented by gating the substring filter on
`query is not None and query.strip()`: with no real search text, no name filter is
applied, so all items pass through (subject to `where`/`sort_by`/`limit`).

Rationale (user-directed this session, explicit intentional change): the prompt
introduces a new list view in which a blank query is meant to show the full list,
and explicitly states it knows the current S3 safety policy returns `[]` and wants
that superseded ("의도적 변경 … 이제 blank query는 전체 아이템을 반환 … S3 blank
정책을 supersede"). Because the user named the current behaviour and directed the
reversal outright, this is a deliberate supersede (not silent compliance, not
refusal): D6's blank-string outcome is recorded as superseded (not deleted) and
FEATURES is updated to match.

This restores the blank-handling outcome D4 originally had (blank = list mode), but
D4 remains superseded as history; D10 is the live decision for blank handling, now
arrived at via the explicit S6 list-view requirement.

Scope guard — `query=None` is unchanged: it was always list mode (contract,
CONTRACT_VERSION 1.0) and stays so; D10 only changes the blank/whitespace-only
*string* case. The two are now observationally identical (both list mode), but the
contract-fixed `None` path and the prompt-driven blank-string path remain distinct
rules so a future session can move one without the other.

Scope — rest of the policy unchanged (prompt: "where/sort/limit/unknown-field
동작은 그대로 유지"): real (non-blank) `query` text is still a case-insensitive
substring match on `name` (D4); `where` equality/AND/empty-`{}`/missing-key
non-match (D5, D9); `sort_by` ascending stable sort with its own missing-key
`ValueError` and incomparable-type `TypeError` (D7); and `limit` top-N with its
edge cases (D8) all stand. The full pipeline is still query -> where -> sort_by ->
limit, returned as deep copies (D1).
