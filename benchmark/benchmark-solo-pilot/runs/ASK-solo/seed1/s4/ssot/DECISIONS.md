# DECISIONS

Numbered, session-tagged durable decisions. When a ticket changes a decision, mark
the old entry superseded but keep it for audit.

## D1 [S0] — Internal storage is an insertion-ordered list
Records are kept in a `list` in the order they were added. `all()` and (currently)
`query()` return them in that order. Rationale: the contract specifies "ties keep
insertion order" for sorting, so insertion order must be the stable baseline.

## D2 [S0] — Return copies via deep copy
`add()` stores a deep copy of the incoming record, and `all()`/`query()` return deep
copies. Rationale: the contract requires callers cannot mutate internal state. Deep
(not shallow) copy chosen so nested mutable values (lists/dicts inside a record) are
also isolated.

## D3 [S0] — query() implements only no-argument behaviour for now
The pinned signature carries `where`, `sort_by`, `limit`, `offset`, but S0 only
requires returning all records. The parameters are accepted (to keep the signature
fixed) but not yet interpreted. Future tickets will define their behaviour, including
the DEFAULT page size that governs an omitted `limit`. No default page size is set
yet.
SUPERSEDED by D4/D5 [S1]: `offset` and `limit` paging are now implemented and the
default page size is set. `where` and `sort_by` remain not-yet-interpreted.

## D4 [S1] — Paging: offset skips, limit caps
`query()` now applies paging over the insertion-ordered records: `offset` (default
`0`) skips that many leading records, then `limit` caps the number returned. The two
compose (offset is applied before the cap). An explicit `limit=0` returns no records
(a zero cap is honoured literally and is distinct from an omitted `limit`). Negative
values are not specified by the ticket and are not given special handling.

## D5 [S1] — DEFAULT PAGE SIZE = 7
When `limit` is omitted (`None`), `query()` returns at most `7` records. This default
page size is a product decision and is defined as the module constant
`DEFAULT_PAGE_SIZE = 7`. It governs only the omitted-`limit` case; an explicit `limit`
(including `0`) overrides it.
SUPERSEDED by D7 [S3]: the default page size value is now `25`. The mechanism
(omitted-`limit` cap via the `DEFAULT_PAGE_SIZE` constant) is unchanged.

## D7 [S3] — DEFAULT PAGE SIZE = 25 (supersedes D5)
When `limit` is omitted (`None`), `query()` returns at most `25` records. The module
constant is now `DEFAULT_PAGE_SIZE = 25`. This changes only the value set in D5; the
policy is otherwise identical — it governs only the omitted-`limit` case, and an
explicit `limit` (including `0`) overrides it.

## D6 [S2] — `where` is conjunctive equality, applied before paging
`query(where={k: v, ...})` keeps a record only if it matches EVERY `k == value` pair
(logical AND). A `where` key that is absent from a record fails the match for that
record rather than raising — implemented as `key in record and record[key] == value`,
so a stored value of `None` is matched by `where={k: None}` while a missing key is not.
Equality uses Python `==`. Filtering happens before paging, so `offset`/`limit` (and the
default page size) apply to the filtered result, not the full store. Edge cases:
`where=None` means no filter (return all, subject to paging); `where={}` matches every
record (vacuous AND).
SUPERSEDED in part by D8 [S4]: `sort_by` is now interpreted; the pipeline order is
filter -> sort -> page. The `where` semantics above are unchanged.

## D8 [S4] — `sort_by` is a stable ascending sort, between filter and paging
`query(sort_by=field)` sorts the (already-filtered) records ASCENDING by `record[field]`.
The query pipeline is now: filter (`where`) -> sort (`sort_by`) -> page (`offset`/`limit`).
Sorting before paging means a page reflects a global ordering, not just the records that
happened to land in that slice.
- Stability: the sort is stable (Python list `.sort`), and because records are iterated in
  insertion order, records with equal sort keys keep insertion order — satisfying the
  contract's "ties keep insertion order".
- Missing field: the sort key is `(field not in record, record.get(field))`. The leading
  boolean segregates records lacking the field (sorted as a group AFTER those that have it,
  in insertion order) so a missing field is never compared against a present value. This
  edge case is unspecified by the ticket; chosen to avoid `None`-vs-value `TypeError` while
  keeping behaviour deterministic.
- Cross-type present values (e.g. mixing `int` and `str` under the same field) are not
  specified and are not given special handling; Python's normal comparison rules apply and
  may raise `TypeError`, as before.
- `sort_by=None` (default) means no sort: records keep filtered insertion order.
