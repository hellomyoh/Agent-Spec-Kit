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
