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
- Part of the fixed contract; exposed now in list mode only.
- With `query=None` (and no other args) returns all items, same as `all()`.
- `query`/`where`/`sort_by`/`limit` filtering, sorting, and limiting are NOT
  implemented yet — to be defined by future sessions.
