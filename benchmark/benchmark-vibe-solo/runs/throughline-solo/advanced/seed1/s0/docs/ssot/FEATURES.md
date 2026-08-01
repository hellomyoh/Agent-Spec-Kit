# FEATURES

Status legend: [done] implemented & tested · [planned] in contract, not yet specified.

## Catalog

- [done] `add(item)` — append an item to the catalog (stored as a deep copy). (S0)
- [done] `all()` — return all items as deep copies, in insertion order. (S0)
- [done] `search()` (no arguments) — return all items as deep copies, in
  insertion order (equivalent to `all()`). (S0)

### search() arguments — in the pinned signature, behaviour not yet specified
- [planned] `query` — text filter on item `name`.
- [planned] `where` — equality filter on item fields.
- [planned] `sort_by` — ordering field.
- [planned] `limit` — max number of results.

Until a session defines them, passing any of these arguments raises
`NotImplementedError` rather than silently ignoring the filter (see DECISIONS D2). (S0)
