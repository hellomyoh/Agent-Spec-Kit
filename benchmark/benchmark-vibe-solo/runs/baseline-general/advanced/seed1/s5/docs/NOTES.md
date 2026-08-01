# NOTES

(optional free-form notes; not an authority doc)

- `search(where={k: v})`: equality filter, multiple keys AND-ed together.
- Policy (S5 change): a `where` key missing from an item is NOT an error. Such
  an item simply does not match and is filtered out. A key absent from every
  item therefore yields `[]`. (Old behaviour raised `ValueError`; abolished.)
  - Implication: an item missing key `k` never matches `where={k: None}` —
    only items that actually have `k` set to `None` match.
- `where` is applied before the `query` substring filter so they compose.
- `query`: blank/whitespace-only -> `[]` (empty-search guard). `query=None` is
  still list mode (no text filter). Non-blank -> case-insensitive substring on
  `name`.
- `sort_by`: ascending, stable sort by that field, applied after filtering.
- `limit`: cap to the first N items, applied LAST (after sort) so it is the
  top N. `None` -> no cap; `0` -> `[]`; N > len -> all; negative -> `ValueError`
  (validated up front). This `ValueError` is unchanged.
  Order of the pipeline: empty-query guard -> `where` -> `query` -> `sort_by`
  -> `limit`.
