# NOTES

(optional free-form notes; not an authority doc)

Current `search` behaviour:
- `query=None` -> no text filter (list mode). Non-None `query` -> case-insensitive
  substring match on `name`; a blank/whitespace `query` returns `[]`.
- `where` -> AND equality filter; unknown field (absent from every item) raises ValueError.
- `sort_by` -> ascending order by that field, stable on ties (insertion order kept).
- `limit` -> present in the contract signature but currently accepted-and-ignored
  (no session has defined its behaviour yet).
- Returns copies; insertion order is the default.
