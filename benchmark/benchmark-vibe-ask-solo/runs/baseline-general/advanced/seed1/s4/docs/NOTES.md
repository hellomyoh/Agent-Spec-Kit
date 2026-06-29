# NOTES

(optional free-form notes; not an authority doc)

- `search(where={k: v})`: equality filter, multiple keys AND-ed together.
- Policy: every `where` key must exist on every catalog item, else `ValueError`.
  (Empty catalog: vacuously valid -> no error, empty result.)
- `where` is applied before the `query` substring filter so they compose.
- `query`: blank/whitespace-only -> `[]` (empty-search guard). `query=None` is
  still list mode (no text filter). Non-blank -> case-insensitive substring on
  `name`.
- `sort_by`: ascending, stable sort by that field, applied after filtering.
- `limit`: cap to the first N items, applied LAST (after sort) so it is the
  top N. `None` -> no cap; `0` -> `[]`; N > len -> all; negative -> `ValueError`
  (validated up front).
  Order of the pipeline: empty-query guard -> `where` -> `query` -> `sort_by`
  -> `limit`.
