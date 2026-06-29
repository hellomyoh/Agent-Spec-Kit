# FEATURES

Status legend: [done] implemented & tested · [planned] in contract, not yet specified.

## Catalog

- [done] `add(item)` — append an item to the catalog (stored as a deep copy). (S0)
- [done] `all()` — return all items as deep copies, in insertion order. (S0)
- [done] `search()` (no arguments) — return all items as deep copies, in
  insertion order (equivalent to `all()`). (S0)

### search() arguments
- [done] `query` — case-insensitive substring filter on item `name`. A blank or
  whitespace-only `query` (and `query=None`) means list mode (all items). Matches
  keep insertion order. (S1, see DECISIONS D4)
- [planned] `where` — equality filter on item fields.
- [planned] `sort_by` — ordering field.
- [planned] `limit` — max number of results.

`where`, `sort_by`, and `limit` are still unspecified: passing any of them raises
`NotImplementedError` rather than silently ignoring the filter (see DECISIONS D2),
including when combined with a `query`. (S0/S1)
