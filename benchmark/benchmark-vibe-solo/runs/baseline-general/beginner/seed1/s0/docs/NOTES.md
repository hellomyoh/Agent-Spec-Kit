# NOTES

(optional free-form notes; not an authority doc)

- S0: in-memory `Catalog`. `add(item)` appends a copy; `all()` returns copies
  in insertion order. Items are dicts with a string 'name'.
- `search` exists to satisfy the fixed contract but only `add`/`all` were
  requested so far. Current `search` defaults: `query=None` => list all;
  non-None `query` => case-insensitive substring match on 'name'.
