# DECISIONS

Numbered, session-tagged durable decisions. When a ticket changes a decision, mark
the old entry superseded but keep it for audit.

## D1 [S0] — Internal storage is an insertion-ordered list
Records are kept in a `list` in the order they were added. `all()` and (currently)
`query()` return them in that order. Rationale: the contract specifies "ties keep
insertion order" for sorting, so insertion order must be the stable baseline.

## D2 [S0] — Return copies via deep copy
`add()` stores a deep copy of the incoming record, and `all()`/`query()` return deep
copies. Rationale: the contract requires callers cannot mutate internal state. Deep
(not shallow) copy chosen so nested mutable values (lists/dicts inside a record) are
also isolated.

## D3 [S0] — query() implements only no-argument behaviour for now
The pinned signature carries `where`, `sort_by`, `limit`, `offset`, but S0 only
requires returning all records. The parameters are accepted (to keep the signature
fixed) but not yet interpreted. Future tickets will define their behaviour, including
the DEFAULT page size that governs an omitted `limit`. No default page size is set
yet.
