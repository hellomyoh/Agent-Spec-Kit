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
  `query` string ALSO means list mode (all items) — the blank query is the list
  view, not a filter. Matches keep insertion order. (S1/S3/S6, see DECISIONS D4,
  D6, D10; D10 supersedes D6 — blank now lists all instead of returning `[]`)
- [done] `where` — equality filter on item fields (`{k: v}`); multiple keys are
  AND-ed. Matches keep insertion order and compose with `query`. An empty `{}`
  lists all items. Policy: an item that lacks a `where` key is treated as a
  non-match (filtered out), so a key absent from every item returns `[]` — no
  error. (S2/S5, see DECISIONS D5, D9; D9 supersedes D5's missing-key `ValueError`)
- [done] `sort_by` — ordering field; orders results ascending with a stable sort
  (equal keys keep insertion order). Applied after `query`/`where` filtering.
  Policy: the field must be present on every result item, else `ValueError`;
  incomparable value types raise `TypeError`. (S3, see DECISIONS D7)
- [done] `limit` — non-negative `int` capping results to the first N, applied
  **last** (after `query`/`where` filtering and `sort_by`): the top N. `limit=None`
  means no cap. `limit=0` returns `[]`; a `limit` at or above the result count
  returns all results. A negative `limit` raises `ValueError`; a non-`int` `limit`
  (`bool` included) raises `TypeError`. (S4, see DECISIONS D8)

Full search pipeline: `query` -> `where` -> `sort_by` -> `limit`, then results
are returned as deep copies. All four `search()` arguments are now specified, so
`search()` no longer raises `NotImplementedError` (D2 fully superseded). (S4)
