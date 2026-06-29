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
