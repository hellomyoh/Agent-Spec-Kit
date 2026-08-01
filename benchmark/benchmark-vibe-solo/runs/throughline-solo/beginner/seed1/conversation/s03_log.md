# CONVERSATION — S3 (seed1, throughline-solo)

## Request (user, Korean)
> 결과를 필드 기준으로 보기 좋게 정렬해줘. 같은 값은 넣은 순서 유지하고. 그리고
> 검색창 비어 있을 때 전체를 다 쏟아내지 마. 부담스러워. 뭐라도 입력하기 전엔
> 아무것도 안 보이게 해줘.

Two asks:
1. **Sort** search results by a field, and for **equal values keep insertion
   order** (i.e. a stable sort) → implement `sort_by`.
2. When the **search box is empty, don't dump the whole list** ("it's
   overwhelming"); **show nothing until I type something** → empty/blank search
   should return nothing instead of everything.

## Conflict-check vs recorded decisions

**Ask 1 — `sort_by`:** No conflict. `sort_by` was explicitly deferred (D1) and
listed under PROGRESS "Next / deferred". The user is now directing it → the
intended-evolution path. Recorded as **D9** (supersedes D1 for `sort_by`).
- Edge policy chosen to match the existing codebase character: unknown sort field
  raises `KeyError` (mirrors D8's loud-on-typo rule for `where`); items missing
  the field sort last and keep their order; sort values assumed comparable.

**Ask 2 — empty search shows nothing:** This is the interesting one. It directly
contradicts **D6** ("an empty `query` matches every item") and the
**list-mode-returns-all** behaviour (D2 / FEATURES: `search(query=None)` == `all()`).
Classified as an **intentional supersede**, not ambiguous drift: the request is
explicit, reasoned ("부담스러워" / overwhelming), and aimed precisely at the
behaviour D6 specifies. So: supersede + update FEATURES + implement (not
preserve-and-flag). Recorded as **D10**.
- **Preserved policy (did NOT silently break):** the "view the full list" purpose
  (PRODUCT) / FEATURES `all()` still hold — `all()` is left untouched as the
  explicit "show me everything" affordance. Only the *search* surface stops
  dumping everything by default. This keeps a deliberate way to see all items, so
  no recorded policy is silently lost.
- **Scope decision:** "empty search" = no real criterion supplied → `search`
  returns `[]` when `where is None` AND `query` is None/blank/whitespace. A
  `where` filter or a non-blank `query` counts as real input and returns matches
  (so `where`-only search still works; blank-query-with-where returns the where
  results).
- **Contract check (provided/contract.py):** the contract delegates a non-None
  query's "blank handling" to the user prompts, so `query=""` → `[]` is in-bounds.
  For `query=None` ("list mode"), the contract fixes the signature but does not
  pin list mode to equal `all()`; `all()` still lists everything, so a
  criterion-less search returning `[]` is consistent with the fixed surface.
  Noted in D10 for a future session to revisit if needed.

## Plan
1. Add empty-search short-circuit: `where is None` and blank/None/whitespace
   `query` → return `[]`.
2. Treat blank query as "no text filter" (so `where`-only still filters).
3. Implement `sort_by`: stable `sorted` with key `(0, value)` present / `(1,)`
   missing (missing sorts last; present never compared to missing); `KeyError`
   when the sort field exists on no item.
4. Keep `add`, `all`, `where` equality + KeyError (D8), copy-safety (D3), and
   substring/case-insensitive `query` matching (D6) unchanged. Leave `limit`
   deferred (not requested).
5. Update SSOT (PRODUCT, FEATURES, DECISIONS D9/D10, PROGRESS) and this file.

## SSOT updates
- **DECISIONS.md:** added **D9** (sort_by; supersedes D1 for sort_by) and **D10**
  (empty search shows nothing; supersedes D6 and the list-mode-returns-all
  behaviour for `search`).
- **FEATURES.md:** rewrote the Search section — empty/blank/whitespace search →
  `[]`, `where`-only counts as input, `sort_by` now active (stable, missing-last,
  KeyError on unknown field); `all()` still lists everything; only `limit` left.
- **PROGRESS.md:** added the S3 entry and refreshed Next/deferred (`limit`,
  persistence, possible D10 revisit).
- **PRODUCT.md:** added the S3 scope line.

## Test run
`python -c "import catalog"` → OK (Python 3.10.11).
Ran a 22-check suite (in-session) covering:
- empty/None/blank/whitespace search → `[]`;
- non-blank query, where-only, and blank-query+where all return correct matches;
- `all()` still returns all items in insertion order (regression);
- unknown `where` field raises `KeyError`; sparse field doesn't; empty-catalog
  where → `[]` (D8 regression);
- `sort_by` stable with ties keeping insertion order and missing-field-last;
  `sort_by` + `where`; unknown `sort_by` field raises `KeyError`; `sort_by` with
  no criterion → `[]`;
- copy-safety: mutating results / the added dict / the `where` dict does not leak
  into internal state (D3 regression).

Result: **PASS 22 / FAIL 0.**

## Summary
Implemented stable `sort_by` (equal values keep insertion order; missing field
sorts last; unknown field raises `KeyError`) and changed search so an empty/blank
query with no `where` returns nothing instead of the whole catalog — superseding
D6 and the list-mode-returns-all behaviour (D9, D10). `all()` is preserved as the
explicit "view everything" path, so no recorded policy was silently dropped. All
prior behaviour (query/where matching, D8 KeyError, D3 copy-safety) intact; 22/22
checks pass.
