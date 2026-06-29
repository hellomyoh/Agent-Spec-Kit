# DECISIONS

(Numbered, session-tagged. Supersede — do not delete.)

## D1 (S0) — Keep S0 scope to add + list only
User asked for "add items and view the full list" and "keep it simple."
We implement `add` and `all` only; we do NOT build query/where/sort/limit yet,
even though they exist in the pinned contract. Rationale: honour the explicit
"keep it simple" ask and avoid speculative behaviour.

## D2 (S0) — `search` exposed but list-mode only
The contract fixes the `search` signature, so `Catalog.search` exists from S0.
For now it returns all items (equivalent to `all()`) and ignores the filter/sort/
limit arguments. Their semantics are deferred to the sessions that introduce them.

## D3 (S0) — Return and store copies (no internal-state leakage)
`add` stores a copy of the given dict; `all`/`search` return fresh copies.
Rationale: the contract requires callers must not be able to mutate internal
state, and it keeps behaviour predictable as features grow.

## D4 (S0) — In-memory storage, no persistence
Items live in a list on the instance; nothing is written to disk. No
persistence was requested.

## D5 (S1) — Implement `query` text search (supersedes D1, D2 for `query`)
User asked to make items searchable by name ("type 'ap' -> apple", "don't be
too strict about case"). This is the deferred `query` behaviour PROGRESS listed
as Next, now directed by the user — an intentional evolution, not drift.
- D1 (S0) deferred query/where/sort/limit under "keep it simple": superseded
  only for `query`. `where`/`sort_by`/`limit` remain deferred.
- D2 (S0) had `search` in list-mode only: superseded for `query`; list mode
  (`query=None`) is unchanged.

## D6 (S1) — Search semantics: case-insensitive substring on `name`
- Matching is substring (not prefix/exact), so `'ap'` matches `'Apple'`.
- Case-insensitive via `casefold()` ("don't be too strict about case").
- An empty `query` (`""`) matches every item (empty string is in everything).
- An item missing `name` is treated as `''` (no crash; simply won't match a
  non-empty query). Rationale: contract says items have a string `name`, but we
  stay robust rather than raising.
- D3 preserved: results are copies.

## D7 (S2) — Implement `where` equality filter (supersedes D1 for `where`)
User asked to filter by fields like `category` too. This is the deferred `where`
behaviour PROGRESS listed as Next, now directed by the user — an intentional
evolution, not drift.
- `where` is a dict of field -> expected value. An item is kept only when, for
  every key in `where`, the item's value for that field equals the expected
  value (exact `==`; AND across keys).
- An item that simply lacks one of the `where` keys does not match that key, so
  it is excluded (it is not an error — see D8 for what counts as an error).
- Combines with `query`: when both are given, both must hold (AND). `where` is
  applied before `query`; order does not affect results.
- `where=None` is unchanged (no field filter).
- D1 (S0) deferred query/where/sort/limit under "keep it simple": superseded
  for `where` (D5 already superseded it for `query`). `sort_by`/`limit` remain
  deferred.
- D3 preserved: results are copies; the `where` dict and stored items are not
  mutated.

## D8 (S2) — Filtering on an unknown field fails loudly (raises KeyError)
User: "if I filter by a field that doesn't exist, that's a mistake — don't
silently give something weird, blow up with an error so I know right away."
- "Unknown field" = a `where` key that is present on NO item in the catalog
  (catalog-wide check). Such a key is almost certainly a typo, so we raise
  `KeyError` rather than silently returning `[]`.
- A field that exists on at least one item is a real field. An individual item
  missing it is normal (heterogeneous items) and just fails to match (D7), NOT
  an error. Rationale: a per-item "must have the field" rule would wrongly error
  on legitimate sparse data; the catalog-wide rule targets the typo the user
  described.
- Empty catalog: the existence check is skipped (a typo is indistinguishable
  from a valid field when there is no data); a filtered search simply returns
  `[]`. This avoids a confusing error before any items exist.

## D9 (S3) — Implement `sort_by`: stable ordering by a field (supersedes D1 for `sort_by`)
User asked to "sort the results nicely by a field, and keep insertion order for
equal values." This is the deferred `sort_by` behaviour PROGRESS listed as Next,
now directed by the user — an intentional evolution, not drift.
- When `sort_by` is given, the surviving (filtered) items are returned ordered by
  that field. The sort is stable (Python `sorted`), so items with an equal value
  keep their insertion order — exactly the "same value keeps order" the user asked
  for.
- Items missing the field sort after all items that have it, and (being equal
  among themselves) keep their insertion order too. Rationale: heterogeneous /
  sparse items are normal here (see D8); they must order predictably rather than
  crash. Implemented with a sort key of `(0, value)` for present and `(1,)` for
  missing, so a present value is never compared against a missing one.
- `sort_by` on a field that NO item has raises `KeyError`, mirroring D8's
  loud-on-typo policy for `where` (a non-existent sort field is almost certainly a
  typo). On an empty result there is nothing to order, so no check/raise.
- Values of the sort field are assumed mutually comparable (as any sort requires);
  mixing incomparable types (e.g. int vs str) raises `TypeError` from `sorted`, by
  design — not special-cased.
- D1 (S0) deferred query/where/sort/limit under "keep it simple": superseded for
  `sort_by`. `limit` remains deferred (not requested this session).
- D3 preserved: results are copies.

## D10 (S3) — Empty search shows nothing (supersedes D6; supersedes list-mode-returns-all)
User: "검색창 비어 있을 때 전체를 다 쏟아내지 마. 부담스러워. 뭐라도 입력하기 전엔
아무것도 안 보이게 해줘." ("When the search box is empty, don't dump out
everything — it's overwhelming. Show nothing until I type something.") This is an
explicit, reasoned UX change, so it is an intentional supersede, not ambiguous
drift.
- New rule: `search` returns results only once the caller supplies a real
  criterion. If `where is None` AND `query` is None or blank (empty `""` or
  whitespace-only), `search` returns `[]` instead of the whole catalog.
- A non-blank `query` OR any `where` counts as real input, so:
  - `search(query='ap')` -> matches (unchanged).
  - `search(where={'category':'fruit'})` -> matches (the user applied a filter).
  - `search(query='', where={...})` / `search(query=None, where={...})` -> the
    `where` results (blank query just means "no text filter"; the `where` is the
    real input).
  - `search()` / `search(query=None)` / `search('')` / `search('   ')` -> `[]`.
- Whitespace-only query is treated as blank (the user hasn't really typed
  anything), consistent with "before I type something."
- Supersedes **D6**'s "an empty `query` matches every item" — empty `query` now
  yields nothing (when no `where`). The rest of D6 (case-insensitive substring,
  missing `name` -> '') is unchanged.
- Supersedes the **list-mode-returns-all** behaviour for `search` (the D2/FEATURES
  statement that `search(query=None)` returns all items like `all()`): list mode
  with no `where` now returns `[]`.
- PRESERVED — "view the full list" policy is NOT broken: `all()` is untouched and
  remains the explicit way to see every item (PRODUCT purpose; FEATURES `all()`).
  The change only stops the *search* surface from dumping everything by default;
  the deliberate "show me everything" affordance still exists via `all()`.
- Contract note: provided/contract.py labels `query=None` as "list mode / no text
  filter" and delegates a non-None query's "blank handling" to the user prompts.
  `query=''` -> `[]` is squarely within that delegation. For `query=None`, the
  contract fixes the signature but does not pin list mode to equal `all()`, and
  `all()` still lists everything — so returning `[]` for a criterion-less search
  is consistent with the fixed surface. If a future session needs
  `search(query=None) == all()`, revisit here.

## D11 (S4) — Implement `limit`: cap to the top N results (supersedes D1 for `limit`)
User asked to "limit the number of results — show only the top N" ("결과 개수 좀
제한할 수 있게 해줘. 상위 N개만 보이게."). This is the deferred `limit` behaviour
PROGRESS listed as Next, now directed by the user — an intentional evolution, not
drift. With this, D1 (S0)'s deferral of query/where/sort/limit is now fully
superseded (query=D5, where=D7, sort_by=D9, limit=D11).
- When `limit` is given, only the first `limit` items of the result are returned.
  "Top N" means the first N in the result's existing order, so `limit` is applied
  LAST — after `where`, `query`, and `sort_by`. (Thus `sort_by=..., limit=N`
  gives the N smallest by that field, which is the natural "top N" reading.)
- `limit=None` (the contract default) means no cap — preserves all prior
  behaviour exactly, so S0–S3 results are unchanged when `limit` is not passed.
- `limit=0` returns `[]`: 0 is a real, meaningful count ("show none"), not an
  error.
- A `limit` greater than the number of results just returns the whole result (no
  padding, no error).
- `limit` does NOT override D10's show-nothing rule: a criterion-less search
  (`where is None` and blank/None `query`) still returns `[]` before `limit` is
  ever considered, so `search(limit=5)` is `[]`, not the first 5 of the catalog.
  Rationale: `limit` shapes an existing result; it is not itself a search
  criterion, and letting it dump the catalog would reintroduce the very
  "everything by default" behaviour D10 removed.
- Bad cap fails loudly (mirrors D8/D9's loud-on-mistake policy): a negative
  `limit` raises `ValueError`; a non-integer `limit` raises `TypeError`. `bool`
  is rejected as a non-integer even though `bool` subclasses `int`, because
  `True`/`False` are not a meaningful result count and almost certainly indicate
  a caller mistake. Rationale: silently clamping a negative to 0 or truncating a
  float would hide a bug; the catalog prefers a clear error.
- D3 preserved: the result is still a fresh list of fresh dict copies; slicing
  with `limit` does not expose internal state.

## D12 (S5) — `where` on an unknown field no longer raises; returns `[]` (supersedes D8)
User: "없는 필드로 거를 때 에러 빵 터지는 거 실제로 써보니 좀 짜증나네. 바꾸자 —
그 필드 없으면 그냥 빈 결과 주고 안 터지게 해줘." ("Filtering on a non-existent
field actually blowing up is annoying in real use. Let's change it — if the field
doesn't exist, just give an empty result and don't blow up.") This is an explicit,
reasoned reversal based on real use, so it is an intentional supersede, not drift.
- New rule: filtering with a `where` field that no item has is NOT an error. The
  equality filter alone already yields no matches for such a field (an item's
  `.get(field)` is `None`, which does not equal a non-None expected value), so
  `search` simply returns `[]`. The catalog-wide existence check that D8 added is
  removed for `where`.
- This unifies the empty-catalog and non-empty-catalog cases: D8 had to special-
  case the empty catalog (skip the check) to avoid a confusing pre-data error;
  with no check at all, both now just return `[]`. Simpler and matches the user's
  "just don't blow up."
- D7 equality semantics are otherwise UNCHANGED: a field present on some items
  still filters normally, and an item that merely lacks a present field still
  fails to match it (not an error). Multi-key `where` where one key is unknown now
  returns `[]` (the unknown key matches nothing) instead of raising.
- Edge note (existing D7 semantics, not changed here): `where={'absent': None}`
  would match items lacking that field, since `.get` returns `None`. This falls
  out of D7's `==` rule and is unchanged; the user's ask was specifically about
  not raising, and a `None` expected value is an unusual filter. Revisit only if a
  future session cares.
- Supersedes **D8** entirely (the unknown-`where`-field KeyError, including its
  empty-catalog carve-out). D7 (the `where` filter itself) stands.

## D13 (S5) — `sort_by` keeps its loud-on-unknown-field policy (D9 PRESERVED)
The user's S5 request named *filtering* only ("거를 때" / "그 필드 없으면" — when
filtering / if the field doesn't exist). It says nothing about sorting. Changing
`sort_by` too would be speculative drift in the opposite direction, so we do NOT
touch it.
- `sort_by` on a field that no item has STILL raises `KeyError` (D9 unchanged).
  Rationale: a bogus sort field has no sensible empty-result interpretation the way
  a filter does — there is nothing to order and the request is almost certainly a
  typo — so failing loudly is still the most helpful behaviour, and the user did
  not ask to change it.
- This is a deliberate, recorded asymmetry: `where` is now forgiving (D12),
  `sort_by` stays loud (D9). `limit`'s bad-input raises (D11) are likewise
  untouched — `limit` validation is about a malformed cap, not a missing field.

## D14 (S6) — Empty search shows everything again (supersedes D10; restores D6's spirit)
User: "아 그리고 검색창 비었을 때는 그냥 전체 다 보여주자. 그게 더 자연스럽잖아.
평범한 목록처럼." ("Oh, and when the search box is empty, let's just show
everything. That's more natural, isn't it? Like an ordinary list.")
- Conflict check: this directly reverses **D10 (S3)**, which made a criterion-less
  search return `[]` ("show nothing until I type something"). The S6 request is
  explicit, decisive ("그냥 전체 다 보여주자"), and carries its own affirmative
  rationale ("더 자연스럽잖아. 평범한 목록처럼" — more natural, like an ordinary
  list). It is the same form as the original D10 ask and as D12's reversal of D8 —
  a reasoned change of mind after real use, i.e. an INTENTIONAL supersede, not
  ambiguous/forgetting drift. So per the conflict rule we supersede D10 and update
  FEATURES, then implement (we do NOT preserve D10's behaviour). D10's own contract
  note pre-authorised this: "If a future session needs `search(query=None) ==
  all()`, revisit here." This is that session.
- New rule: a criterion-less search returns the WHOLE catalog (insertion order).
  With `where is None` AND `query` None/blank (empty `""` or whitespace-only), no
  filter is applied and every item is returned — the same items `all()` returns.
  So `search()`, `search(query=None)`, `search("")`, `search("   ")` all return the
  full catalog (was `[]` under D10).
- A blank/whitespace `query` now means simply "no text filter" (it no longer forces
  an empty result). A non-blank `query` or any `where` still narrows the result
  exactly as before. There is no longer any "show nothing" special case in `search`
  at all — the pipeline (where -> query -> sort -> limit) just runs over the full
  catalog when nothing filters it. (Implementation: the early `return []` guard
  from D10 is removed.)
- Restores the SPIRIT of **D6** (empty query yields the full set) but via the
  list-mode/whole-catalog framing of the contract, not D6's "empty string matches
  every item" mechanism — the substring/case-insensitive matching of D6 for a
  *non-blank* query is unchanged.
- PRESERVED (unchanged): `all()` (still the direct list-everything path; now a
  criterion-less `search` mirrors it); `where` equality + forgiving unknown field
  (D7/D12); `sort_by` stable ordering + loud-on-unknown-field (D9/D13); `limit`
  validation (D11 raises); copy-safety (D3).
- Supersedes **D10** entirely (both its empty-`query` "shows nothing" rule and its
  supersede of the list-mode-returns-all behaviour — list mode returns all again).
  Note D10 had itself superseded D6; D6 stays superseded as written (its mechanism
  is not restored), but its net effect (empty -> full set) is back.

## D15 (S6) — `sort_by`/`limit` now apply to a criterion-less (full-catalog) search (supersedes D11's "limit can't dump the catalog" clause)
A consequence of D14: because an empty search now yields the full catalog instead
of `[]`, `sort_by` and `limit` on a criterion-less search now act on that full
catalog (under D10 there was nothing to order or cap).
- `search(sort_by=field)` with no other criterion now orders the whole catalog by
  that field (stable; missing-field items last; unknown field still raises per
  D13).
- `search(limit=N)` with no other criterion now returns the first N items of the
  catalog (e.g. `limit=2` -> first two), and `search(sort_by=f, limit=N)` returns
  the top N by that field. This SUPERSEDES the specific D11 clause that said
  "`limit` does not override D10's show-nothing rule, so `search(limit=5)` is `[]`":
  with D10 gone, that clause is moot and `limit` now shapes the full-catalog result
  as expected. `limit=0` still returns `[]` (a real "show none" count), and bad
  `limit` (negative/non-int/bool) still raises (the rest of D11 stands).
- Rationale: D11 deferred `limit` to D10's rule only because there was no result to
  shape; once D14 makes the result the full catalog, the natural "ordinary list,
  top N" reading applies. No new user ask — this is the direct, consistent fallout
  of D14, recorded so the change is traceable.
