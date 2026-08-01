# NOTES

(optional free-form notes; not an authority doc)

- S0: in-memory `Catalog`. `add(item)` appends a copy; `all()` returns copies
  in insertion order. Items are dicts with a string 'name'.
- `search` defaults: `query=None` => list all.
- S1: name search requested. `query` (non-None) => case-insensitive substring
  match on 'name' ('ap' matches 'Apple'). This is now an explicitly-asked
  feature, not just a contract stub.
- S2: filter by arbitrary fields (e.g. `where={'category': 'fruit'}`) confirmed
  as a real feature. (S2 originally raised `KeyError` on a field NO item has;
  see S5, which reversed this.) A field present on only some items is fine:
  items lacking it just don't match the value.
- S3: sort + blank-search policy.
  - `sort_by` must keep equal values in insertion order. `sorted` is already
    stable in Python, so this holds; comment makes the intent explicit.
  - Empty search box => show nothing. A non-None `query` that is empty or
    whitespace-only now returns `[]` (we `strip()` first), instead of matching
    everything. `query=None` stays list mode (the contract's "no text filter"),
    so it is unchanged and still lists all.
- S4: "top N" result limiting confirmed as a real feature.
  - `limit=N` keeps at most the first N items AFTER filter + sort (the top N of
    the final order). `limit=0` => `[]` (show nothing); `limit=None` => no cap
    (lists all), unchanged.
  - `limit` greater than the result count just returns everything (no error).
  - `limit < 0` now raises `ValueError` (a meaningless "top -1"); previously
    Python negative slicing silently dropped items off the end.
- S5: unknown `where` field no longer raises. Filtering on a field that NO item
  has now returns `[]` (the user found the S2 `KeyError` annoying in practice).
  Match test tightened to `field in it and it[field] == value` so an item only
  matches a field it actually carries; this keeps "present on only some items"
  working and stops `where={'field': None}` from spuriously matching items that
  lack the field. `limit < 0` => `ValueError` is unaffected and still stands.
