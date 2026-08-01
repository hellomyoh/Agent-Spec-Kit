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
