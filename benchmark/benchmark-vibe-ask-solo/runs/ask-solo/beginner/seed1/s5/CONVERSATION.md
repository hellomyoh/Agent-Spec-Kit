# CONVERSATION — S5 (seed1, ask-solo)

## Request
User (Korean): "없는 필드로 거를 때 에러 빵 터지는 거 실제로 써보니 좀 짜증나네.
바꾸자 — 그 필드 없으면 그냥 빈 결과 주고 안 터지게 해줘."

Translation: "Filtering by a non-existent field actually blowing up with an error
is annoying in real use. Let's change it — if the field doesn't exist, just give an
empty result and don't blow up."

Target: the `where` unknown-field behaviour (recorded as D8).

## Conflict check (vs recorded decisions)
- Current policy **D8 (S2)**: a `where` field present on no item in a non-empty
  catalog raises `KeyError` (typo guard). This is exactly what the user is asking
  to change.
- Classification: **intentional change** (not forgetting / ambiguous drift). The
  user explicitly names the behaviour, gives a rationale ("annoying in real use"),
  and directs a specific new behaviour ("just give an empty result, don't blow
  up"). Per ask-solo policy this is **supersede the decision**, then implement —
  not a silent comply, and not a hold/ask (the intent is unambiguous).
- Scope guard: the request names **filtering** only ("거를 때" / "그 필드 없으면").
  It says nothing about **`sort_by`**, whose loud-on-unknown-field behaviour (D9)
  mirrors D8. Changing `sort_by` too would be speculative drift in the opposite
  direction, so `sort_by` is **preserved** and that choice is recorded (D13). The
  `limit` bad-input raises (D11) are about a malformed cap, not a missing field,
  so they are likewise untouched.

## Plan
1. Remove the catalog-wide existence check for `where` in `search`. The remaining
   equality filter (`item.get(field) == value`) already returns no matches for a
   field no item has (absent -> `None` != a non-None expected value), so the
   result is naturally `[]` — no raise. This also drops D8's empty-catalog
   carve-out (no check at all => empty and non-empty behave identically).
2. Keep `sort_by`'s unknown-field `KeyError` (D9) and `limit`'s raises (D11).
3. Update SSOT: supersede D8 (new D12), record `sort_by` preservation (D13),
   refresh FEATURES / PRODUCT / PROGRESS and fix now-stale cross-references that
   said `sort_by`/`limit` mirror `where`'s loud policy.
4. Write COMPLETE `catalog.py`; verify by import + regression suite.

## SSOT updates
- **DECISIONS.md**: added **D12 (S5)** — `where` unknown field returns `[]`, no
  raise; supersedes **D8** entirely (incl. its empty-catalog carve-out). D7 (the
  filter itself) stands. Added **D13 (S5)** — `sort_by` keeps its loud-on-unknown
  policy (D9 preserved); records the deliberate `where`-forgiving / `sort_by`-loud
  asymmetry.
- **FEATURES.md**: rewrote the `where` "unknown field" sub-bullet (now forgiving,
  returns `[]`, incl. multi-key and empty-catalog). Fixed `sort_by` and `limit`
  bullets whose "(same loud policy as `where`)" cross-references went stale.
- **PRODUCT.md**: corrected the S2 scope line; added an S5 scope line (where
  forgiving; sort_by still raises).
- **PROGRESS.md**: added the S5 entry (change, preservation, verification);
  Next/deferred unchanged.

## Test run
- `python -c "import catalog"` -> `import OK`.
- 30-check suite (all pass):
  - NEW: unknown `where` field -> `[]` (single key, multi-key with one unknown,
    `+query`, empty catalog) — none raise.
  - D7 preserved: existing-field `where` still filters; item lacking a present
    field still doesn't match; `price=3` excludes price-less items.
  - D9 preserved: `sort_by` on an unknown field STILL raises `KeyError` (reached
    by pairing with a real `query` criterion); stable sort with missing-last; a
    `sort_by`-only call with no criterion is `[]` per D10 (never reaches the sort
    check).
  - Regression: query substring/case-insensitive, query+where AND, D10 show-
    nothing (`search()`/`None`/`''`/`'   '` -> `[]`, `all()` still dumps all),
    limit caps/`0`/`None`/over-length, negative->ValueError, non-int->TypeError,
    bool->TypeError, limit doesn't bypass show-nothing, D3 copy-safety (result
    mutation, add-stores-copy, where-dict-not-mutated).

## Summary
Made `where` filtering forgiving: an unknown field now yields an empty result
instead of raising `KeyError` (supersedes D8). Deliberately preserved `sort_by`'s
loud-on-unknown-field behaviour (D9) since the user asked only about filtering, and
recorded the asymmetry (D13). All prior behaviour (query, where equality, sort,
limit, empty-search, copy-safety) is unchanged; 30-check suite + import pass.
