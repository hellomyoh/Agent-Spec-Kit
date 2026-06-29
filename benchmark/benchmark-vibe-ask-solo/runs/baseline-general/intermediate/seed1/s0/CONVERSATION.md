# CONVERSATION

## User request
Create a `Catalog` class with `add(item)`, `all()`, and `search()`. For now,
calling `search()` with no arguments returns all items.

## Plan
- Implement `Catalog` in `catalog.py` using the FIXED signatures from
  `provided/contract.py` (the `search` keyword params are kept in the signature
  but only the requested no-arg behaviour is implemented this session).
- Store items in insertion order; return copies from `all()` and `search()` so
  callers cannot mutate internal state (fixed by the contract).
- `search()` with no arguments returns all items.

## Test command run
```
python -c "import catalog; ..."   # run inside the work dir
```
Smoke test: empty catalog returns `[]`; after two `add()`s, `all()` and
`search()` return both items in insertion order; mutating a returned item does
not affect internal state (copies verified). All assertions passed.

## Summary
`catalog.py` implements `Catalog.add`, `.all`, and `.search`. `search()` with no
arguments returns all items as copies, matching the request and the pinned
contract surface.
