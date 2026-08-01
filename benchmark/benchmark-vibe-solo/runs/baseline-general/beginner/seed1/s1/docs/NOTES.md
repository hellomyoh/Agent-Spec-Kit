# NOTES

(optional free-form notes; not an authority doc)

- S0: in-memory `Catalog`. `add(item)` appends a copy; `all()` returns copies
  in insertion order. Items are dicts with a string 'name'.
- `search` defaults: `query=None` => list all.
- S1: name search requested. `query` (non-None) => case-insensitive substring
  match on 'name' ('ap' matches 'Apple'). This is now an explicitly-asked
  feature, not just a contract stub.
