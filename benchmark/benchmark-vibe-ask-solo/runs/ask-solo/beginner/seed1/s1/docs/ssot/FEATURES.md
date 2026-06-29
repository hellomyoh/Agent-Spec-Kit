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
- With `query=None` (list mode) returns all items, same as `all()`.
- With a non-None `query`, returns items whose `name` contains the query as a
  substring, compared case-insensitively (e.g. `'ap'` matches `'Apple'`). An
  empty query matches every item. Items without a `name` are treated as `''`.
- Results are copies (D3 preserved); callers cannot mutate internal state.
- `where`/`sort_by`/`limit` are NOT implemented yet — to be defined by future
  sessions.
