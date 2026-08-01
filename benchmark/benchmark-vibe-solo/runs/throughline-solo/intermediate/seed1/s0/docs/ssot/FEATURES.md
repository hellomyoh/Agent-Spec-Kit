# FEATURES

## Catalog
- **add(item)** — appends an item dict to the catalog (stored as a copy).
- **all()** — returns every item, as copies.
- **search(query=None, where=None, sort_by=None, limit=None)** — returns matching
  items as copies.
  - `query=None` (no text filter) → list mode.
  - `search()` with no arguments → returns all items. *(S0)*
  - `where` → equality filter across the given fields.
  - `sort_by` → orders results by that field.
  - `limit` → caps the number of results.

## Invariants (from contract)
- Items are dicts; every item has a string `name`.
- Reads (`all`, `search`) return list-of-dict **copies**; callers cannot mutate
  internal state.
