# NOTES (miniquery)

## State / contract
- Single file `miniquery.py`, `class Store`. Signatures are PINNED in
  provided/contract.py — never change them; only add behaviour per ticket.
- query() full signature already declared: where, sort_by, limit, offset, select.

## Implemented so far
- S0: add(record) stores a copy; all() returns list of copies; query() (no args)
  returns all records (copies).

## Key decisions / invariants
- Use `copy.deepcopy` on BOTH add and read so callers can never mutate internal
  state (records may hold nested dicts/lists). Keep this invariant for every
  future feature (e.g. select-projection must also return fresh dicts).
- Records kept in a private list `self._records`; insertion order is the source
  of truth (contract: "ties keep insertion order" for sort_by).

## TODO for future tickets (NOT yet implemented — do not pre-build)
- where: equality match on ALL key==value pairs.
- sort_by: ascending, stable (ties keep insertion order).
- limit / offset: pagination (apply offset then limit; offset default 0).
- select: project to listed keys only.
- Likely order when combined: where -> sort_by -> offset/limit -> select.
