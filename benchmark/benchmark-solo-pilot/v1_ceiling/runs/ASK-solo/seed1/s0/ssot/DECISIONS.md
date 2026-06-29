# DECISIONS

(maintain this SSOT doc across sessions)

Numbered, dated-by-session durable decisions. Newest entries appended.

## D1 (S0) — Single self-contained module
`miniquery.py` is one file implementing `class Store`, no external dependencies.
Rationale: matches the task contract and keeps the surface easy to evolve.

## D2 (S0) — Public API is pinned; signature carried in full from session one
`query()` is defined with its complete contract signature
(`where, sort_by, limit, offset, select`) from S0 onward, even though S0 only
implements the no-argument behaviour. Rationale: the contract declares signatures
FIXED across sessions; defining the full signature now avoids a later
signature-changing edit. Unimplemented params are inert at their defaults.

## D3 (S0) — Copy in, copy out
`add()` stores a shallow copy; `all()`/`query()` return shallow copies in a new
list. Rationale: the contract requires callers cannot mutate internal state.
Copies are shallow (sufficient for flat records); revisit if nested records appear.

## D4 (S0) — Default order is insertion order
`all()` and no-arg `query()` return records in insertion order. Rationale: it is
the natural default and the contract specifies insertion order as the tie-break
for future `sort_by`, so it must be preserved.

## D5 (S0) — query() extra params not yet honoured (no future features)
where/sort_by/limit/offset/select are accepted but NOT implemented in S0 per the
"implement only this ticket" rule. They currently have no effect; a no-arg
`query()` returns all records. Behaviour for these params will be defined by the
tickets that introduce them. (Open: decide whether passing them before they are
implemented should raise vs. be silently ignored — deferred until first such ticket.)
