# FEATURES

(Current behaviour. Update as sessions evolve it.)

## Add item — `add(item)`
- Appends one item (a dict) to the catalog.
- Stored by value (a copy is kept), so later mutation of the caller's dict does
  not change stored data.

## View all — `all()`
- Returns every item in insertion order.
- Returns copies (fresh list of fresh dicts); callers cannot mutate internal
  state through the result.

## Search — `search(query=None, where=None, sort_by=None, limit=None)`
- Part of the fixed contract.
- With `query=None` and `where=None` (list mode) returns all items, same as
  `all()`.
- `query` (text filter): with a non-None `query`, returns items whose `name`
  contains the query as a substring, compared case-insensitively (e.g. `'ap'`
  matches `'Apple'`). An empty query matches every item. Items without a `name`
  are treated as `''`.
- `where` (field equality filter): a dict of field -> expected value. Returns
  items where, for every key, the item's value equals the expected value
  (exact `==`, AND across keys). An item that lacks a given key just doesn't
  match that key.
  - Unknown field = a mistake: if a `where` key is present on no item in a
    non-empty catalog (typically a typo), `search` raises `KeyError` instead of
    silently returning nothing. On an empty catalog the check is skipped and the
    result is `[]`.
- `query` + `where` combine with AND (both must hold).
- Results are copies (D3 preserved); callers cannot mutate internal state.
- `sort_by`/`limit` are NOT implemented yet — to be defined by future sessions.
