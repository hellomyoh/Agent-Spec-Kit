# FEATURES

## Catalog
- **add(item)** — appends an item dict to the catalog (stored as a copy).
- **all()** — returns every item, as copies.
- **search(query=None, where=None, sort_by=None, limit=None)** — returns matching
  items as copies. Filters apply in order: `query`, then `where`, then `sort_by`,
  then `limit`.
  - **Empty search = list view**: a search with **no text term** (`query=None`,
    including the no-argument `search()`) applies no text filter and returns **all
    items** (insertion order, subject to any `where`/`sort_by`/`limit`). *(S0/S6;
    `query=None` is the documented "off" signal.)*
  - `query` (non-None) → case-insensitive substring match on item `name`; an item
    matches when `query` (casefolded) is contained in its `name` (casefolded).
    Matches keep insertion order. *(S1)*
  - A **blank** `query` *string* — empty `""` or all-whitespace
    (`query.strip() == ""`) — returns an empty list (matches nothing). *(S3;
    supersedes the S1 rule that an empty `query` matched every item.)* This is
    distinct from `query=None`: `None` (no term) shows all; a blank **string**
    matches nothing. **Open conflict (S6, CR1):** the S6 "empty search shows all"
    request may intend this blank-string case to show all too; D8 is preserved
    pending user confirmation — see DECISIONS CR1.
  - `where` → equality filter across the given fields (`{field: value}`); multiple
    keys combine with AND. Combines with `query` (AND). A `where` field that is
    missing from any item under test → returns an empty list (matches nothing).
    *(S5; supersedes the S2 rule that a missing `where` field raised `ValueError`.)*
  - `sort_by` → orders results in **ascending** order by that field; ties keep
    insertion order (stable sort). *(S3)*
  - `limit` → caps the result to the **first `n`** items, applied last (after
    `query`/`where`/`sort_by`). `limit=None` → no cap (all items). A non-positive
    `limit` (`0` or negative) → empty list. *(S4)*

## Invariants (from contract)
- Items are dicts; every item has a string `name`.
- Reads (`all`, `search`) return list-of-dict **copies**; callers cannot mutate
  internal state.
