# DATA_MODEL

(maintain this SSOT doc across sessions)

## Record
- A record is an arbitrary `dict` (schema-less). No required keys are enforced
  at this stage. Keys are strings by convention; values are any Python value.

## Store internal state
- `Store._records: list[dict]` — records in INSERTION ORDER.
- Insertion order is significant and must be preserved: it is the default order
  returned by `all()` / `query()`, and (per the contract) the tie-break order
  for future `sort_by`.

## Copy semantics (invariant)
- `add(record)` stores a SHALLOW copy (`dict(record)`), so later mutation of
  the caller's dict does not change stored data.
- `all()` and `query()` return a NEW list of SHALLOW copies of each record, so
  callers cannot mutate internal state via returned values.
- Note: copies are shallow — nested mutable values inside a record would still
  be shared. Not an issue for the current flat-record use; revisit if nested
  records are introduced.
