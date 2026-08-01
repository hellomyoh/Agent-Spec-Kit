# FEATURES

## Catalog
- **add(item)** — appends an item dict to the catalog (stored as a copy).
- **all()** — returns every item, as copies.
- **search(query=None, where=None, sort_by=None, limit=None)** — returns matching
  items as copies. Filters apply in order: `query`, then `where`, then `sort_by`,
  then `limit`.
  - `query=None` (no text filter) → list mode.
  - `search()` with no arguments → returns all items. *(S0)*
  - `query` (non-None) → case-insensitive substring match on item `name`; an item
    matches when `query` (casefolded) is contained in its `name` (casefolded).
    Matches keep insertion order. `query=""` matches every item. *(S1)*
  - `where` → equality filter across the given fields (`{field: value}`); multiple
    keys combine with AND. Combines with `query` (AND). A `where` field that is
    missing from any item under test raises `ValueError`. *(S2)*
  - `sort_by` → orders results by that field.
  - `limit` → caps the number of results.

## Invariants (from contract)
- Items are dicts; every item has a string `name`.
- Reads (`all`, `search`) return list-of-dict **copies**; callers cannot mutate
  internal state.
