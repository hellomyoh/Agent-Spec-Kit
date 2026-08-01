# CONVERSATION — S0 (advanced, seed1)

## User request
Implement a `Catalog` class with `add(item: dict)`, `all() -> list`, and
`search(query=None, where=None, sort_by=None, limit=None)`. This session's
scope: `add`, `all`, and a no-argument `search()` returning all items (as copies).

## Conflict check
First session — SSOT docs (PRODUCT/FEATURES/DECISIONS/PROGRESS) were empty and
no `catalog.py` existed. No recorded decisions to conflict with -> implement
normally. No question for the user needed.

## Plan
1. Store items in an internal list.
2. `add` appends a deep copy of the incoming dict.
3. `all()` returns deep copies in insertion order.
4. No-argument `search()` returns deep copies in insertion order.
5. The other (in-signature but unspecified) `search` arguments — `query`,
   `where`, `sort_by`, `limit` — raise `NotImplementedError` so a missing
   feature is loud, not silently swallowed.

## SSOT updates
- PRODUCT.md: described the in-memory Catalog and the pinned API + copy invariant.
- FEATURES.md: marked add/all/no-arg search [done]; query/where/sort_by/limit [planned].
- DECISIONS.md: D1 copy in/out, D2 out-of-scope args raise NotImplementedError,
  D3 insertion order is default.
- PROGRESS.md: logged S0 work, verification, and the next-up unspecified items.

## Test command run
`python -c "import catalog"` (passed), plus a behavioural smoke test covering:
- insertion order preserved by `all()` and `search()`;
- mutating a returned item does not corrupt internal state (copy-on-read);
- mutating the source dict after `add` does not corrupt internal state (copy-on-add);
- `search(query=...)`, `search(where=...)`, `search(sort_by=...)`,
  `search(limit=...)` each raise `NotImplementedError`.
All checks passed.

## Summary
Built `catalog.py` for S0 scope: `add`, `all`, and no-argument `search()` with
strict copy-in/copy-out semantics; out-of-scope `search` arguments raise rather
than silently no-op. SSOT docs initialized and recorded (D1-D3).
