# CONVERSATION

## User request
Implement a `Catalog` class with `add(item: dict)`, `all() -> list`, and
`search(query=None, where=None, sort_by=None, limit=None)`. Scope for this
session: `add`, `all`, and a no-argument `search()` that returns all items
as copies.

## Plan
- Back the catalog with an internal `list` of item dicts.
- `add`: append the item.
- `all`: return shallow copies of every item in insertion order (so callers
  cannot mutate internal state, per the contract).
- `search`: keep the full fixed signature from the contract; for this session
  the no-argument call (list mode) returns the same copies as `all()`. The
  other parameters (`where`, `sort_by`, `limit`, non-None `query`) are part of
  the pinned signature but their behaviour is not in scope yet.

## Test command run
`python -c "import catalog"` plus an inline sanity script asserting:
empty state, insertion order for `all()`/`search()`, and that both `all()` and
`search()` return copies (mutating results does not change internal state).

## Summary
`catalog.py` implements `Catalog` with `add`, `all`, and no-arg `search()`.
All sanity checks pass, including copy isolation. Signature matches the pinned
contract exactly.
