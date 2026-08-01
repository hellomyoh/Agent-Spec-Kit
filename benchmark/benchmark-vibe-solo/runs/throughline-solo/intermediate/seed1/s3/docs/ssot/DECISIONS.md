# DECISIONS

Numbered, session-tagged. Supersede (do not delete) when a decision changes.

- **D1 (S0)** — `Catalog` is in-memory: items live in a list, in insertion order.
- **D2 (S0)** — `add(item)` stores a copy of the item dict; `all()` and `search()`
  return copies. Rationale: contract requires reads not to expose mutable internal
  state.
- **D3 (S0)** — `search()` with no arguments returns all items. Implemented as
  `query=None` meaning "no text filter" (list mode), per the contract note.
- **D4 (S0)** — Contract parameters `where` / `sort_by` / `limit` are implemented
  with their plain meaning (equality filter / order-by-field / cap count) so the
  pinned surface is complete and correct. Precise text-search (`query`) semantics
  are deferred to a future session that defines them.
  - *Superseded by D5 (S1):* the deferred `query` semantics are now defined.
    The `where` / `sort_by` / `limit` portion of D4 remains in force.
  - *Refined by D7 (S2):* the `where` equality-filter behaviour is now fully
    defined (missing-field handling). `sort_by` / `limit` portion of D4 remains
    in force.
- **D5 (S1)** — Non-None `query` is a **case-insensitive substring match on the
  item `name`**: an item matches when `query.casefold()` is contained in
  `item["name"].casefold()`. Matching items keep insertion order (no implicit
  sort). Resolves the D4 deferral. `query=None` still means "no text filter"
  (D3 preserved).
- **D6 (S1)** — Filter precedence in `search`: `query` first, then `where`, then
  `sort_by`, then `limit`. `query` and `where` are independent filters (AND); a
  result must satisfy both. `query=""` matches every item (empty string is a
  substring of any name), consistent with treating `query` as a plain substring
  test. Rationale: `None` is the documented "off" signal (D3), so an explicit
  empty string is a real, all-matching query rather than a second "off" value.
  - *Superseded in part by D8 (S3):* a blank `query` (empty/whitespace) now
    returns an empty list, not every item. The precedence ordering and the
    `query`/`where` AND independence in D6 remain in force.
- **D7 (S2)** — `where={field: value}` is an equality filter: an item matches when,
  for every key, `item[field] == value` (multiple keys AND, per D6; precedence
  query → where → sort_by → limit unchanged). A `where` field that is **missing
  from any item under test** raises `ValueError`. Refines D4/D6, which had left
  missing-field handling unspecified (the prior `item.get(field)` treated a missing
  field as `None`, silently non-matching). Rationale: the S2 prompt requires an
  explicit error when a `where` field is absent, so an unknown field is a caller
  mistake to surface, not a silent no-match. The check runs against the items
  remaining after the `query` stage; an empty result set after `query` cannot be
  tested for fields, so an unknown `where` field on an empty set does not raise.
- **D8 (S3)** — A **blank** `query` returns an empty list (matches nothing). "Blank"
  means a non-None `query` whose `str.strip()` is empty — i.e. `""` or any
  all-whitespace string. Supersedes the D6 clause that `query=""` matched every
  item. `query=None` still means "no text filter" (D3 preserved); `None` and a
  blank string are now distinct — `None` lets all items through, a blank string
  filters them all out. A non-blank `query` is still the D5 case-insensitive
  substring match (preserved). Rationale: the S3 prompt intentionally changes the
  empty-query semantics, and folds whitespace-only input into the same "no usable
  search term" case. A blank `query` yields the empty set in the `query` stage and
  flows through the remaining stages unchanged; because no items survive, a later
  `where` field cannot be tested and so does not raise (consistent with D7).
- **D9 (S3)** — `sort_by` orders results in **ascending** order by the field value,
  and ties preserve insertion order (stable sort), implemented via Python's stable
  `sorted`. Makes explicit the order/tie-breaking that D4/D6 left loose ("order-by
  -field"); the existing `sorted(..., key=item.get(sort_by))` already satisfied
  this, so it is a clarification with no behaviour change. Precedence
  (query → where → sort_by → limit) unchanged.
