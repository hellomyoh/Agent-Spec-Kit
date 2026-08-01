# CONVERSATION — S0 (seed1, throughline-solo)

## User request
(Korean) "작은 카탈로그 검색 같은 거 만들고 싶어. 일단 아이템 추가하고 전체 목록
보는 것만 되면 돼. 복잡하게 말고 간단하게."

Translation: "I want to make a small catalog-search type thing. For now I just
need adding items and viewing the full list. Keep it simple, not complex."

## Conflict-check result
No conflict. DECISIONS.md was empty (fresh S0) — there is no prior recorded
policy to contradict. Implemented normally. No question needed for the user.

Note on the contract: `provided/contract.py` pins the full `Catalog` surface,
including `search(query, where, sort_by, limit)`. The user only asked for add +
list, and said "keep it simple." Resolution: implement `add`/`all` fully, expose
`search` (signature is fixed by the contract) in list mode only, and defer its
filter/sort/limit behaviour to the sessions that introduce it (see D1, D2).

## Plan
1. Read SSOT + USER_PROMPT + contract (no catalog.py existed yet).
2. Implement `Catalog` with `add` and `all`; minimal `search` (list mode).
3. Store/return copies so callers can't mutate internal state.
4. Verify import and behaviour; update SSOT + write this file.

## SSOT updates
- PRODUCT.md: described the product, pinned surface, S0 scope.
- FEATURES.md: documented current behaviour of add / all / search.
- DECISIONS.md: added D1 (scope = add+list), D2 (search list-mode only),
  D3 (store/return copies), D4 (in-memory, no persistence).
- PROGRESS.md: logged S0 work, verification, and deferred items.

## Test command run
`python -c "import catalog"` (plus an inline add/all/copy-safety/list-mode check).
Result: import OK; all() returns items in insertion order; external mutation of
the returned list/dicts does not affect internal state; search() returns all.

## Summary
Created `catalog.py` with a simple in-memory `Catalog`: `add(item)` appends a
copy, `all()` returns copies in insertion order. `search` is present per the
fixed contract but list-mode only for now. SSOT updated; scope kept intentionally
small per the user's "keep it simple" request.
