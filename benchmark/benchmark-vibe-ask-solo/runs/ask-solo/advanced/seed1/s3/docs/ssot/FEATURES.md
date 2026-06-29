# FEATURES

Status legend: [done] implemented & tested · [planned] in contract, not yet specified.

## Catalog

- [done] `add(item)` — append an item to the catalog (stored as a deep copy). (S0)
- [done] `all()` — return all items as deep copies, in insertion order. (S0)
- [done] `search()` (no arguments) — return all items as deep copies, in
  insertion order (equivalent to `all()`). (S0)

### search() arguments
- [done] `query` — case-insensitive substring filter on item `name`. `query=None`
  means list mode (all items, per the contract). A blank or whitespace-only
  `query` string returns `[]` (no results — an empty search box does not dump the
  catalog). Matches keep insertion order. (S1/S3, see DECISIONS D4, D6)
- [done] `where` — equality filter on item fields (`{k: v}`); multiple keys are
  AND-ed. Matches keep insertion order and compose with `query`. Policy: a
  `where` key absent from any item in the catalog raises `ValueError`. (S2, see
  DECISIONS D5)
- [done] `sort_by` — ordering field; orders results ascending with a stable sort
  (equal keys keep insertion order). Applied after `query`/`where` filtering.
  Policy: the field must be present on every result item, else `ValueError`;
  incomparable value types raise `TypeError`. (S3, see DECISIONS D7)
- [planned] `limit` — max number of results.

`limit` is still unspecified: passing it raises `NotImplementedError` rather than
silently ignoring it (see DECISIONS D2), including when combined with `query`,
`where`, or `sort_by`. (S0/S1/S2/S3)
