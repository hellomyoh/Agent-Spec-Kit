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
NOTE (S1): `where` is now implemented (see D6); sort_by/limit/offset/select remain
reserved/inert. The "raise vs. ignore" open item is resolved for `where` by D6;
still deferred for the remaining params until their tickets land.

## D6 (S1) — `where` equality filter + unknown-field policy
`query(where={k: v, ...})` returns records matching ALL key==value pairs (logical
AND), compared with `==` on the stored value, in insertion order, as copies.
- Empty/None `where` is a no-op (returns all records) — preserves D4/S0 behaviour.
- A record that LACKS one of the `where` keys does not match (it is filtered out),
  NOT an error.
- POLICY (hard rule for all future `where` handling): if a `where` key is present
  in NO stored record (not in the union of keys across all records), raise
  `KeyError(key)`. An unknown field is a hard error, not a silent no-match.
  Corollary: on an EMPTY store, any non-empty `where` raises `KeyError` (no record
  contains the key). Rationale: ticket-mandated; surfaces typo'd field names early.

## D7 (S2) — `sort_by` ascending stable sort + missing-field policy
`query(sort_by=field)` returns the (already `where`-filtered) records sorted
ASCENDING by `field`'s value, as copies.
- STABLE sort (ticket-mandated): records with EQUAL sort keys keep their relative
  INSERTION ORDER. Implemented via Python's `sorted()` (guaranteed stable), keyed
  by `r[field]`, over the post-filter result list (which is in insertion order).
- ORDER OF OPERATIONS: `where` filtering happens FIRST, then `sort_by` orders the
  survivors. (Matters once limit/offset land in a later ticket.)
- `sort_by=None` (default) is a no-op: insertion order is preserved (S0/S1 intact).
- MISSING-FIELD POLICY (hard rule, mirrors D6): if `sort_by` names a field present
  in NO stored record, raise `KeyError(sort_by)`. Additionally, if a record that
  SURVIVED filtering lacks the sort key (while the field exists on other records),
  the sort raises `KeyError(sort_by)` — a record's sort position is undefined
  without the key. Rationale: consistency with the D6 unknown-field rule and
  fail-fast on typo'd/absent sort fields; avoids inventing a sentinel ordering.
- Mixed-type values are NOT specially handled: comparison uses the values' native
  `<` (a `TypeError` from incomparable types propagates). No ticket requires
  cross-type ordering; revisit if/when one does.
