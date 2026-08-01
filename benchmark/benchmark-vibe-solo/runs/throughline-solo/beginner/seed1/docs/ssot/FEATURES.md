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
- Empty search shows everything: with no `where` AND a None or blank (empty `""`
  or whitespace-only) `query`, `search` applies no filter and returns every item
  in insertion order — an ordinary list, the same items `all()` returns. (So
  `search()`, `search(query=None)`, `search("")`, `search("   ")` all return the
  whole catalog.) Supplying a real criterion (`where`, or a non-blank `query`)
  narrows the result. `all()` remains the direct unfiltered list-everything path.
  (Changed in S6/D14, which superseded S3/D10's "empty search shows nothing" and
  restored the empty -> full-set effect of the original D6.)
- `query` (text filter): with a non-blank `query`, returns items whose `name`
  contains the query as a substring, compared case-insensitively (e.g. `'ap'`
  matches `'Apple'`). Items without a `name` are treated as `''`. A blank query
  applies no text filter (so on its own it yields the whole catalog, per the
  empty-search rule above).
- `where` (field equality filter): a dict of field -> expected value. Returns
  items where, for every key, the item's value equals the expected value
  (exact `==`, AND across keys). An item that lacks a given key just doesn't
  match that key. Supplying a `where` counts as a real criterion, so a
  `where`-only search (even with a blank/None `query`) returns its matches.
  - Unknown field is forgiving (not an error): filtering on a field that no item
    has simply yields no matches (`[]`) — `search` does NOT raise. (A missing
    field's value is treated as absent, so it doesn't equal a non-None expected
    value.) A multi-key `where` with one unknown key likewise returns `[]`. This
    holds the same way on an empty catalog. (Changed in S5/D12, which superseded
    the earlier raise-on-unknown-field policy.)
- `query` + `where` combine with AND (both must hold).
- `sort_by` (ordering field): when given, the surviving items are returned
  ordered by that field. The sort is stable, so items with an equal value keep
  their insertion order. Items missing the field sort after those that have it
  (keeping their insertion order among themselves). A `sort_by` field present on
  no item raises `KeyError` (sort still fails loudly on an unknown field — a
  bogus sort field has no sensible empty-result reading; note `where` is NOT loud
  anymore, see D12/D13); on an empty result there is nothing to order. Sort-field
  values are assumed mutually comparable (mixing incomparable types raises
  `TypeError`, as any sort would).
- `limit` (max results): caps how many items are returned — the "top N" of the
  result, applied last (after `where`, `query`, and `sort_by`). `limit=None`
  means no cap (all surviving items). `limit=0` returns `[]`. A `limit` larger
  than the result simply returns the whole result. Because an empty search now
  yields the full catalog (D14), a criterion-less `search(limit=N)` returns the
  first N items of the catalog (e.g. `limit=2` -> first two), and
  `search(sort_by=f, limit=N)` the top N by that field. (Superseded S4/D11's
  clause that a criterion-less `search(limit=5)` was `[]`; that only held because
  the old show-nothing rule made the result empty — see D15.) A negative `limit`
  raises `ValueError` and a non-integer `limit` raises `TypeError` (a malformed
  cap is a caller mistake — fail loudly, like a `sort_by` typo; this is about a
  bad cap value, not a missing field, so the S5 `where` change does not touch it).
  `bool` is rejected as non-integer (it is not a meaningful count).
- Results are copies (D3 preserved); callers cannot mutate internal state.
