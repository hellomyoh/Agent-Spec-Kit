# NOTES

(optional free-form notes; not an authority doc)

Current `search` behaviour:
- `query=None` -> no text filter (list mode). A blank/whitespace `query` is treated the same
  way: no text filter, so an empty search behaves like a plain list view and returns all items
  (in insertion order, subject to where/sort_by/limit). A non-blank `query` -> case-insensitive
  substring match on `name`.
- `where` -> AND equality filter; an unknown field (absent from every item) is NOT an
  error — it matches nothing, so the result is `[]`.
- `sort_by` -> ascending order by that field, stable on ties (insertion order kept).
- `limit` -> caps result count. Applied LAST, after query/where filtering and
  sort_by ordering: returns the first `limit` items. `limit=None` -> no cap;
  `limit=0` -> `[]`; `limit` > match count -> all matches.
- Returns copies; insertion order is the default.
