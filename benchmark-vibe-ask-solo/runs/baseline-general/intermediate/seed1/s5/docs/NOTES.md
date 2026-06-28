# NOTES

(optional free-form notes; not an authority doc)

Current `search` behaviour:
- `query=None` -> no text filter (list mode). Non-None `query` -> case-insensitive
  substring match on `name`; a blank/whitespace `query` returns `[]`.
- `where` -> AND equality filter; an unknown field (absent from every item) is NOT an
  error — it matches nothing, so the result is `[]`.
- `sort_by` -> ascending order by that field, stable on ties (insertion order kept).
- `limit` -> caps result count. Applied LAST, after query/where filtering and
  sort_by ordering: returns the first `limit` items. `limit=None` -> no cap;
  `limit=0` -> `[]`; `limit` > match count -> all matches.
- Returns copies; insertion order is the default.
