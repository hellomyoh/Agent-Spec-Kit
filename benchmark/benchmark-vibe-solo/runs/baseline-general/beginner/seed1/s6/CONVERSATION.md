# CONVERSATION — S6

## Request
User (Korean): "아 그리고 검색창 비었을 때는 그냥 전체 다 보여주자. 그게 더 자연스럽잖아. 평범한 목록처럼."

Translation: "Oh, and when the search box is empty, let's just show everything. That's
more natural — like a normal list."

So: an empty search box should now show all items (a plain list), instead of showing
nothing. This reverses the S3 blank-search policy.

## Plan
- The contract leaves blank-query handling to the user prompts, so changing it is allowed.
- In `search`, a non-None `query` is still stripped and lowercased. Previously a blank
  result (`needle == ""`) returned `[]`; now a blank query simply applies no name filter,
  so every item flows through (then any `where` / `sort_by` / `limit` still apply).
- Keep everything else exactly as before:
  - `query=None` stays list mode (contract-fixed "no text filter").
  - Non-blank `query` keeps case-insensitive substring matching on `name`.
  - `where` (incl. unknown-field => `[]` from S5), `sort_by` (stable), and `limit`
    (`limit=0` => `[]`, `limit<0` => `ValueError`) are untouched.
- Implementation: replace the early `return []` on a blank needle with an `if needle:`
  guard around the name-filter step, so a blank box falls through showing all.

## Test run
`python -c "import catalog"` + assertions (all passed):
- `search(query='')` and `search(query='   ')` => all 3 items (NEW S6 behaviour).
- `search(query=None)` / `search()` => all 3 (list mode unchanged).
- `search(query='ap')` => `['Apple']`; `search(query='a')` => all 3 (case-insensitive
  substring); `search(query='rr')` => `['Carrot']`.
- `where={'category':'fruit'}` => 2; `where={'nope':1}` => `[]` (S5 unknown field).
- `search(query='', where={'category':'veg'})` => 1 (blank box + where still filters).
- `sort_by='name'` => alphabetical; `limit=2` => 2; `limit=0` => `[]`;
  `limit=-1` => `ValueError`; `search(query='  ', limit=1)` => 1 (blank box composes
  with limit).
- Results are copies: mutating a returned dict does not change internal state.

## Summary
Changed the empty/whitespace-only search box to show everything (like a plain list)
instead of returning nothing, reversing the S3 blank-search policy as the user asked.
A blank `query` now just skips the name filter; `query=None` list mode, non-blank name
search, `where`, `sort_by`, and `limit` are all unchanged.
