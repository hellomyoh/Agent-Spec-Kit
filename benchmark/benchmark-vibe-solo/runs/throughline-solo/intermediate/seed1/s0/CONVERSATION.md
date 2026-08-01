# CONVERSATION — S0 (seed1, throughline-solo)

## User request
(Korean) Make a `Catalog` class with `add(item)`, `all()`, `search()`. For now,
calling `search()` with no arguments should return all items.

## Conflict check
SSOT docs (PRODUCT/FEATURES/DECISIONS/PROGRESS) were empty templates — this is the
first session, so there are **no recorded decisions** to conflict with.
Result: **no conflict → implement normally.** No question for the user.

## Plan
1. Implement the full FIXED contract surface from `provided/contract.py`
   (`add`, `all`, `search(query, where, sort_by, limit)`).
2. Make this session's specified behaviour explicit: `search()` with no args
   returns all items (`query=None` = list mode, per contract note).
3. Honour the contract invariant that reads return copies.
4. Implement `where` / `sort_by` / `limit` with their plain meaning so the surface
   is complete; defer precise `query` text-search semantics to a future session.

## SSOT updates
- PRODUCT.md — described the in-memory Catalog product.
- FEATURES.md — listed add / all / search and invariants.
- DECISIONS.md — D1 in-memory list; D2 copy on store & read; D3 no-arg search == all;
  D4 plain where/sort_by/limit, query semantics deferred.
- PROGRESS.md — S0 marked done; open item: query text-search semantics.

## Test command run
`python -c "import catalog"` plus a smoke test:
- `search()` (no args) == `all()` == both inserted items.
- mutating a returned dict does not affect internal state (copy-safety).
Result: **OK**.

## Summary
Delivered `catalog.py` with the complete pinned API. `search()` with no arguments
returns all items, as requested. Reads return copies. SSOT docs initialised and
updated; conflict check clean (first session).
