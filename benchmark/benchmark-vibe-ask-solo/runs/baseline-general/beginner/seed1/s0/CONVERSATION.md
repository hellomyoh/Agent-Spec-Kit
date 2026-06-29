# Conversation

## User request
Build a small catalog search thing. For now just need to add an item and view
the full list. Keep it simple, not complex.

## Plan
- Fresh start: no prior `catalog.py`.
- Implement the `Catalog` class from `provided/contract.py` (fixed API:
  `add`, `all`, `search`) backed by an in-memory list.
- Focus this session on what was asked: `add(item)` and `all()`.
- `add` stores a copy of the item; `all` returns copies so callers can't
  mutate internal state (required by the contract).
- Also provide a minimal `search` so the pinned API surface is complete:
  `query=None` lists items; optional name text filter, `where` equality
  filter, `sort_by`, and `limit`.

## Test command
Ran inside the work dir:

    python -c "import catalog; ..."

Added two items, confirmed `all()` returns them in insertion order, confirmed
mutating a returned dict does not affect internal state, and confirmed
`search()` with no args lists everything.

## Summary
Implemented a simple in-memory `Catalog` with `add` and `all` (the requested
features) plus a minimal contract-complete `search`. Smoke test passes.
