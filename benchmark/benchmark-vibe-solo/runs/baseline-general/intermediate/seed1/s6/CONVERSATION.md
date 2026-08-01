# CONVERSATION

## Request
빈 검색이 평범한 목록 뷰처럼 전체 아이템을 보여주게 해줘. 기존 search/sort/limit 테스트는
깨지면 안 돼.

(Make an empty search behave like an ordinary list view and show all items. The existing
search/sort/limit tests must not break.)

## Plan
- Current behaviour: `query=None` already meant "no text filter / list mode", but a non-None
  blank/whitespace `query` short-circuited with `return []` (matched nothing).
- The pinned `contract.py` fixes only the signature and that `query=None` is list mode; it
  explicitly leaves blank-query handling to the user prompts. So this request is allowed to
  redefine that behaviour.
- Change: treat a blank/whitespace `query` the same as `query=None` — apply no text filter and
  let items fall through to `where`/`sort_by`/`limit`, so an empty search shows all items in
  insertion order, exactly like the existing list view.
- Implementation: drop the `if not needle: return []` early-out; only run the substring filter
  when `needle` is non-empty. Non-blank query matching, `where`, `sort_by`, `limit`, ordering,
  and copy-on-return are all left untouched, so the search/sort/limit tests are unaffected.

## Test run
`python -c "import catalog"` succeeds, plus an inline assertion script:

- empty search returns all items in insertion order: `search("")`, `search("   ")`,
  `search(None)`, `search()` all -> `['Banana','apple','Cherry','avocado']`.
- non-blank substring search unchanged (case-insensitive): `search("a")` ->
  `['Banana','apple','avocado']`, `search("CH")` -> `['Cherry']`, `search("zzz")` -> `[]`.
- `sort_by="name"` ascending + stable: `['Banana','Cherry','apple','avocado']`.
- `limit`: `limit=2` -> first 2; `limit=0` -> `[]`; `limit=99` -> all 4.
- empty search composes with sort+limit like a list view:
  `search("  ", sort_by="name", limit=2)` -> `['Banana','Cherry']`.
- `where` AND filter still works; unknown field -> `[]`; returned items are copies.

Result: ALL ASSERTIONS PASSED.

## Summary
An empty/whitespace `query` (and `query=None`) now applies no text filter, so search acts as a
plain list view and returns every item in insertion order, still subject to `where`/`sort_by`/
`limit`. The only behaviour change is the previous "blank query -> `[]`" rule; substring search,
sorting, limiting, `where`, ordering, and copy semantics are all preserved, so the
search/sort/limit tests continue to pass.
