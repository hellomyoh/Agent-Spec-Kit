# DATA_MODEL

## Record
A record is an arbitrary `dict`. No schema is enforced; keys and value types are
caller-defined. Records may contain nested mutable values (lists/dicts).

## Store state
- `Store._records: list[dict]` — the stored records as deep copies, in insertion
  order. This is the single source of truth for stored data.

## Copy boundary
Data crossing the Store boundary is always deep-copied:
- in on `add()` (caller's dict is not aliased), and
- out on `all()` / `query()` (returned dicts are independent of internal state).
