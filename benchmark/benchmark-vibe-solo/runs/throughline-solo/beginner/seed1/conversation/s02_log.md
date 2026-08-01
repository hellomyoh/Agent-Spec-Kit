# CONVERSATION — S2 (throughline-solo, beginner, seed1)

## Request
User (Korean): "카테고리 같은 필드로도 거를 수 있게 해줘. 아 그리고 없는 필드로 거르면
그건 실수니까 조용히 이상한 거 주지 말고 그냥 에러로 빵 터뜨려서 바로 알게 해줘."

Translation / intent:
1. Allow filtering by fields like `category` too (i.e. activate the `where`
   equality filter from the fixed contract).
2. Filtering by a field that doesn't exist is a mistake — don't silently return
   something weird; raise an error loudly so the caller notices immediately.

## Conflict check
- `where` was listed under PROGRESS "Next / deferred" and was deferred by D1 (S0)
  under "keep it simple". The user now explicitly directs it → intentional
  evolution, not forgetting/drift. Same pattern as D5 (S1) for `query`.
  Resolution: SUPERSEDE D1 for `where` (D7); `sort_by`/`limit` stay deferred.
- No recorded policy is broken. Preserved: D3 (copies / no internal-state
  leakage), D5/D6 (`query` semantics), D2-as-superseded list mode for
  `query=None`/`where=None`.
- New policy added (D8) for the "loud error on unknown field" ask; consistent
  with D6's robustness stance but deliberately distinguishes a typo'd field
  (error) from an item that legitimately lacks a real field (no match).

## Plan
- Implement `where` in `search`: dict of field -> expected value; keep an item
  when all keys match exactly (`==`); AND with `query` when both given.
- Loud-on-mistake: if a `where` key exists on NO item in a non-empty catalog,
  raise `KeyError`. An item merely missing a real field is not an error — it
  just doesn't match. Empty catalog: skip the check, return `[]` (a typo is
  indistinguishable from a valid field with no data).
- Preserve D3 copy-safety and all prior behaviour. Write complete `catalog.py`.

## SSOT updates
- DECISIONS.md: added D7 (implement `where`, supersedes D1 for `where`) and
  D8 (unknown-field raises KeyError; per-item missing field is not an error;
  empty-catalog exemption).
- FEATURES.md: documented current `where` behaviour, the unknown-field error,
  and query+where AND combination.
- PROGRESS.md: added S2 entry; trimmed deferred list to `sort_by`/`limit` +
  persistence.
- PRODUCT.md: extended "Scope so far" with S1 and S2.

## Test run
`python -c "import catalog"` → import OK.
Behaviour suite (all pass):
1. `where={'category':'fruit'}` → Apple, Banana.
2. Item missing `category` (Mystery) excluded from `category='veg'`; no crash.
3. Typo field `where={'categry':...}` → raises KeyError ("no item has it").
4. `query` + `where` combine with AND.
5. Multi-key `where` (category+color) → only the item matching all keys.
6. List mode and prior `query` ('ap' → Apple) unchanged.
7. Copy-safety (D3): mutating results does not change stored items.
8. Empty catalog + `where` → `[]` (no spurious error).
9. `add`/`all` intact.

## Summary
Activated the `where` field-equality filter (e.g. `category`) and made filtering
on a nonexistent field fail loudly with `KeyError`, while keeping legitimately
sparse items (missing a real field) as simple non-matches. All prior behaviour
and copy-safety preserved; SSOT updated with D7/D8.
