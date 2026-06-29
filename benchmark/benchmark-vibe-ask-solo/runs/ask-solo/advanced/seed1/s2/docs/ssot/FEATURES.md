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
- [done] `where` — equality filter on item fields (`{k: v}`); multiple keys are
  AND-ed. Matches keep insertion order and compose with `query`. Policy: a
  `where` key absent from any item in the catalog raises `ValueError`. (S2, see
  DECISIONS D5)
- [planned] `sort_by` — ordering field.
- [planned] `limit` — max number of results.

`sort_by` and `limit` are still unspecified: passing either raises
`NotImplementedError` rather than silently ignoring it (see DECISIONS D2),
including when combined with a `query` or `where`. (S0/S1/S2)
