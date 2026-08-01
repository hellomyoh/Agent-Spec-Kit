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
- Shows nothing until you search: results appear only once you supply a real
  criterion. If `where` is None AND `query` is None or blank (empty `""` or
  whitespace-only), `search` returns `[]` — it does NOT dump the whole catalog.
  To deliberately view everything, call `all()`. (So `search()`,
  `search(query=None)`, `search("")`, `search("   ")` all return `[]`.)
- `query` (text filter): with a non-blank `query`, returns items whose `name`
  contains the query as a substring, compared case-insensitively (e.g. `'ap'`
  matches `'Apple'`). Items without a `name` are treated as `''`. A blank query
  applies no text filter (and on its own yields nothing, per the rule above).
- `where` (field equality filter): a dict of field -> expected value. Returns
  items where, for every key, the item's value equals the expected value
  (exact `==`, AND across keys). An item that lacks a given key just doesn't
  match that key. Supplying a `where` counts as a real criterion, so a
  `where`-only search (even with a blank/None `query`) returns its matches.
  - Unknown field = a mistake: if a `where` key is present on no item in a
    non-empty catalog (typically a typo), `search` raises `KeyError` instead of
    silently returning nothing. On an empty catalog the check is skipped and the
    result is `[]`.
- `query` + `where` combine with AND (both must hold).
- `sort_by` (ordering field): when given, the surviving items are returned
  ordered by that field. The sort is stable, so items with an equal value keep
  their insertion order. Items missing the field sort after those that have it
  (keeping their insertion order among themselves). A `sort_by` field present on
  no item raises `KeyError` (same loud-on-typo policy as `where`); on an empty
  result there is nothing to order. Sort-field values are assumed mutually
  comparable (mixing incomparable types raises `TypeError`, as any sort would).
- `limit` (max results): caps how many items are returned — the "top N" of the
  result, applied last (after `where`, `query`, and `sort_by`). `limit=None`
  means no cap (all surviving items). `limit=0` returns `[]`. A `limit` larger
  than the result simply returns the whole result. `limit` does NOT bypass the
  show-nothing rule: a criterion-less search returns `[]` regardless of `limit`.
  A negative `limit` raises `ValueError` and a non-integer `limit` raises
  `TypeError` (a bad cap is a caller mistake — fail loudly, like `where`/`sort_by`
  typos). `bool` is rejected as non-integer (it is not a meaningful count).
- Results are copies (D3 preserved); callers cannot mutate internal state.
