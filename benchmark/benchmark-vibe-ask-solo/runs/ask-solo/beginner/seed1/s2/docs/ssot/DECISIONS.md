# DECISIONS

(Numbered, session-tagged. Supersede — do not delete.)

## D1 (S0) — Keep S0 scope to add + list only
User asked for "add items and view the full list" and "keep it simple."
We implement `add` and `all` only; we do NOT build query/where/sort/limit yet,
even though they exist in the pinned contract. Rationale: honour the explicit
"keep it simple" ask and avoid speculative behaviour.

## D2 (S0) — `search` exposed but list-mode only
The contract fixes the `search` signature, so `Catalog.search` exists from S0.
For now it returns all items (equivalent to `all()`) and ignores the filter/sort/
limit arguments. Their semantics are deferred to the sessions that introduce them.

## D3 (S0) — Return and store copies (no internal-state leakage)
`add` stores a copy of the given dict; `all`/`search` return fresh copies.
Rationale: the contract requires callers must not be able to mutate internal
state, and it keeps behaviour predictable as features grow.

## D4 (S0) — In-memory storage, no persistence
Items live in a list on the instance; nothing is written to disk. No
persistence was requested.

## D5 (S1) — Implement `query` text search (supersedes D1, D2 for `query`)
User asked to make items searchable by name ("type 'ap' -> apple", "don't be
too strict about case"). This is the deferred `query` behaviour PROGRESS listed
as Next, now directed by the user — an intentional evolution, not drift.
- D1 (S0) deferred query/where/sort/limit under "keep it simple": superseded
  only for `query`. `where`/`sort_by`/`limit` remain deferred.
- D2 (S0) had `search` in list-mode only: superseded for `query`; list mode
  (`query=None`) is unchanged.

## D6 (S1) — Search semantics: case-insensitive substring on `name`
- Matching is substring (not prefix/exact), so `'ap'` matches `'Apple'`.
- Case-insensitive via `casefold()` ("don't be too strict about case").
- An empty `query` (`""`) matches every item (empty string is in everything).
- An item missing `name` is treated as `''` (no crash; simply won't match a
  non-empty query). Rationale: contract says items have a string `name`, but we
  stay robust rather than raising.
- D3 preserved: results are copies.

## D7 (S2) — Implement `where` equality filter (supersedes D1 for `where`)
User asked to filter by fields like `category` too. This is the deferred `where`
behaviour PROGRESS listed as Next, now directed by the user — an intentional
evolution, not drift.
- `where` is a dict of field -> expected value. An item is kept only when, for
  every key in `where`, the item's value for that field equals the expected
  value (exact `==`; AND across keys).
- An item that simply lacks one of the `where` keys does not match that key, so
  it is excluded (it is not an error — see D8 for what counts as an error).
- Combines with `query`: when both are given, both must hold (AND). `where` is
  applied before `query`; order does not affect results.
- `where=None` is unchanged (no field filter).
- D1 (S0) deferred query/where/sort/limit under "keep it simple": superseded
  for `where` (D5 already superseded it for `query`). `sort_by`/`limit` remain
  deferred.
- D3 preserved: results are copies; the `where` dict and stored items are not
  mutated.

## D8 (S2) — Filtering on an unknown field fails loudly (raises KeyError)
User: "if I filter by a field that doesn't exist, that's a mistake — don't
silently give something weird, blow up with an error so I know right away."
- "Unknown field" = a `where` key that is present on NO item in the catalog
  (catalog-wide check). Such a key is almost certainly a typo, so we raise
  `KeyError` rather than silently returning `[]`.
- A field that exists on at least one item is a real field. An individual item
  missing it is normal (heterogeneous items) and just fails to match (D7), NOT
  an error. Rationale: a per-item "must have the field" rule would wrongly error
  on legitimate sparse data; the catalog-wide rule targets the typo the user
  described.
- Empty catalog: the existence check is skipped (a typo is indistinguishable
  from a valid field when there is no data); a filtered search simply returns
  `[]`. This avoids a confusing error before any items exist.
