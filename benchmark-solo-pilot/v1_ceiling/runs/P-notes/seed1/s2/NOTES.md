# NOTES (miniquery)

## State / contract
- Single file `miniquery.py`, `class Store`. Signatures PINNED in
  provided/contract.py — never change them; only add behaviour per ticket.
- query() full signature: where, sort_by, limit, offset, select.

## Implemented so far
- S0: add(record) deep-copies in; all() returns deep copies; query() no-arg -> all.
- S1: query(where={k:v,...}) -> records matching ALL key==value pairs.
- S2: query(sort_by=field) -> ASCENDING sort by record[field], STABLE (ties keep
  insertion order). Uses builtin `sorted` (already stable). Applied AFTER where.

## Key decisions / invariants
- `copy.deepcopy` on BOTH add and read so callers can never mutate internal
  state (records may hold nested dicts/lists). Keep for EVERY future feature
  (e.g. select-projection must also return fresh dicts).
- Records in private list `self._records`; insertion order is the source of
  truth (contract: "ties keep insertion order" for sort_by).

## WHERE policy (S1 — DECIDED ONCE, applies to ALL future where handling)
- Unknown field = HARD ERROR: if a where key is in NO stored record, raise
  `KeyError(key)`. NOT a silent no-match. Validate keys BEFORE filtering.
- A record that simply lacks a present key fails the equality test (excluded),
  but is NOT an error — because the key exists in *some* record.
- Empty/None where = no filtering. `if where:` guards this, so where={} is a
  no-op too. Matching is ALL pairs (AND), using `==`.
- Key-existence check is against the FULL store, independent of sort/limit/etc.

## SORT policy (S2 — DECIDED)
- `if sort_by is not None:` guards it (so sort_by=None / omitted = no sort).
  Used `is not None` (not truthiness) so a falsy field name like "" still sorts.
- Ascending only; stability via builtin `sorted`. Sort key is `r[sort_by]`.
- Combined order locked in: where -> sort_by (-> offset/limit -> select later).
- OPEN (decide when a ticket needs it): behaviour if a record LACKS sort_by, or
  values are mixed/uncomparable types. Current code does `r[sort_by]` -> would
  KeyError on a missing key / TypeError on uncomparable. No ticket forced a
  choice yet; don't pre-build. Mirror the where-policy style (validate up front)
  when S-? specifies it.

## TODO future tickets (NOT yet implemented — do not pre-build)
- limit / offset: pagination (apply offset then limit; offset default 0).
- select: project to listed keys only (must still deep-copy / fresh dicts).
- Likely combined order: where -> sort_by -> offset/limit -> select.
