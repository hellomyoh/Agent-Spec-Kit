# DECISIONS

Numbered, session-tagged. Supersede (do not delete) when a decision changes.

- **D1 (S0)** — `Catalog` is in-memory: items live in a list, in insertion order.
- **D2 (S0)** — `add(item)` stores a copy of the item dict; `all()` and `search()`
  return copies. Rationale: contract requires reads not to expose mutable internal
  state.
- **D3 (S0)** — `search()` with no arguments returns all items. Implemented as
  `query=None` meaning "no text filter" (list mode), per the contract note.
- **D4 (S0)** — Contract parameters `where` / `sort_by` / `limit` are implemented
  with their plain meaning (equality filter / order-by-field / cap count) so the
  pinned surface is complete and correct. Precise text-search (`query`) semantics
  are deferred to a future session that defines them.
  - *Superseded by D5 (S1):* the deferred `query` semantics are now defined.
    The `where` / `sort_by` / `limit` portion of D4 remains in force.
  - *Refined by D7 (S2):* the `where` equality-filter behaviour is now fully
    defined (missing-field handling). `sort_by` / `limit` portion of D4 remains
    in force.
- **D5 (S1)** — Non-None `query` is a **case-insensitive substring match on the
  item `name`**: an item matches when `query.casefold()` is contained in
  `item["name"].casefold()`. Matching items keep insertion order (no implicit
  sort). Resolves the D4 deferral. `query=None` still means "no text filter"
  (D3 preserved).
- **D6 (S1)** — Filter precedence in `search`: `query` first, then `where`, then
  `sort_by`, then `limit`. `query` and `where` are independent filters (AND); a
  result must satisfy both. `query=""` matches every item (empty string is a
  substring of any name), consistent with treating `query` as a plain substring
  test. Rationale: `None` is the documented "off" signal (D3), so an explicit
  empty string is a real, all-matching query rather than a second "off" value.
  - *Superseded in part by D8 (S3):* a blank `query` (empty/whitespace) now
    returns an empty list, not every item. The precedence ordering and the
    `query`/`where` AND independence in D6 remain in force.
- **D7 (S2)** — `where={field: value}` is an equality filter: an item matches when,
  for every key, `item[field] == value` (multiple keys AND, per D6; precedence
  query → where → sort_by → limit unchanged). A `where` field that is **missing
  from any item under test** raises `ValueError`. Refines D4/D6, which had left
  missing-field handling unspecified (the prior `item.get(field)` treated a missing
  field as `None`, silently non-matching). Rationale: the S2 prompt requires an
  explicit error when a `where` field is absent, so an unknown field is a caller
  mistake to surface, not a silent no-match. The check runs against the items
  remaining after the `query` stage; an empty result set after `query` cannot be
  tested for fields, so an unknown `where` field on an empty set does not raise.
  - *Superseded in part by D11 (S5):* a missing `where` field no longer raises
    `ValueError`; it now returns an empty result. The equality-match semantics,
    multi-key AND, and precedence in D7 remain in force.
- **D8 (S3)** — A **blank** `query` returns an empty list (matches nothing). "Blank"
  means a non-None `query` whose `str.strip()` is empty — i.e. `""` or any
  all-whitespace string. Supersedes the D6 clause that `query=""` matched every
  item. `query=None` still means "no text filter" (D3 preserved); `None` and a
  blank string are now distinct — `None` lets all items through, a blank string
  filters them all out. A non-blank `query` is still the D5 case-insensitive
  substring match (preserved). Rationale: the S3 prompt intentionally changes the
  empty-query semantics, and folds whitespace-only input into the same "no usable
  search term" case. A blank `query` yields the empty set in the `query` stage and
  flows through the remaining stages unchanged; because no items survive, a later
  `where` field cannot be tested and so does not raise (consistent with D7).
  - *Conflict raised in S6 (see CR1):* the S6 prompt ("empty search → show all
    items, like a list view") may be read as `query=""` → all, which would
    reverse D8. Because that reading is ambiguous and breaks this deliberate
    recorded policy, D8 is **preserved in code pending user confirmation** and
    the conflict is recorded as CR1. Not superseded.
- **D9 (S3)** — `sort_by` orders results in **ascending** order by the field value,
  and ties preserve insertion order (stable sort), implemented via Python's stable
  `sorted`. Makes explicit the order/tie-breaking that D4/D6 left loose ("order-by
  -field"); the existing `sorted(..., key=item.get(sort_by))` already satisfied
  this, so it is a clarification with no behaviour change. Precedence
  (query → where → sort_by → limit) unchanged.
- **D10 (S4)** — `limit=n` caps the result to the **first `n`** items, applied
  **last** (after `query`/`where`/`sort_by`, per the D6 precedence — preserved).
  `limit=None` means "no cap" (return all). A **non-positive** `limit` (`0` or any
  negative) caps to **nothing** (empty list). Makes explicit the count-cap that D4
  ("cap count") / FEATURES left loose: a positive `limit` already worked via the
  `results[:limit]` slice (no behaviour change there), but a negative `limit` would
  have fallen through to Python's negative-index slice (e.g. `[:-1]` drops the last
  item) — a misleading reading of "limit the number of results". Clamping
  non-positive to the empty list gives "limit ≤ 0 → keep nothing", which is the
  well-defined meaning of a count cap. Rationale: the S4 prompt asks to limit the
  result count while keeping sort/filter as-is; this pins the cap semantics
  (incl. the previously-undefined non-positive edge) without changing the positive
  `limit`, sort, or filter behaviour.
- **D11 (S5)** — A `where` field **missing from any item under test** now yields an
  **empty result** (matches nothing) instead of raising `ValueError`. Supersedes
  the D7 clause that raised on a missing field; D7's equality-match (`item[field]
  == value`), multi-key AND, and precedence (query → where → sort_by → limit) are
  all preserved. The missing-field condition is detected exactly as before (the
  field is absent from at least one item remaining after the `query` stage); only
  the consequence changes from raise → return `[]`. The empty result then flows
  through the remaining `sort_by`/`limit` stages unchanged (both are no-ops on an
  empty list). As under D7, the check runs against the post-`query` items, so a
  `where` field on an already-empty set is moot (the result is empty regardless).
  Rationale: the S5 prompt intentionally changes the missing-field behaviour from
  an error to a silent empty result, so an unknown `where` field is no longer
  surfaced as a caller mistake but simply matches no items.
- **D12 (S6)** — An **empty search** — meaning a search with **no text term
  supplied** (`query=None`, including the no-argument `search()`) — is the plain
  **list view** and returns **all items** (in insertion order, subject to any
  `where`/`sort_by`/`limit` also passed). This is the non-conflicting reading of
  the S6 prompt ("빈 검색이 평범한 목록 뷰처럼 전체 아이템을 보여주게 해줘" / "make
  an empty search show all items like an ordinary list view"). It is **already in
  force** via D3 (`query=None` = "no text filter") — D12 only names it explicitly
  as the intended "empty search = list view" behaviour and reaffirms it. No
  behaviour change. The distinct case of a **blank search string** (`query=""` or
  whitespace) is NOT covered here: it remains D8 (→ empty list), preserved pending
  user confirmation (see CR1). Rationale: the natural "empty search box shows
  everything" semantics is satisfied by the documented off-signal (`query=None`)
  without disturbing the deliberately-chosen blank-string policy (D8).

## Conflicts (need user confirmation)

- **CR1 (S6)** — *Possible conflict between the S6 prompt and D8.* The S6 prompt
  asks that an "empty search" (빈 검색) show all items like a list view. "Empty
  search" is **ambiguous**:
  - Reading A — `query=None` / no-argument `search()` ("no search term"): already
    returns all items (D3). Implemented and reaffirmed as **D12**. No conflict.
  - Reading B — `query=""` / whitespace ("empty search *string*"): currently
    returns an **empty list** by **D8 (S3)**, a decision made *intentionally* in
    S3 to supersede the older "`query=""` matches everything" rule. Reading B
    would **reverse D8**.
  Decision this session: **preserve D8** (blank string → `[]`) in code and **do
  not silently reverse it**, because (a) the prompt is ambiguous and does not
  acknowledge that it is undoing a deliberate prior decision (this is
  forgetting/ambiguous drift, not a stated intentional supersede), and (b) the
  prompt's own constraint "기존 search/sort/limit 테스트는 깨지면 안 돼" ("existing
  search/sort/limit tests must not break") is best honoured by *keeping* D8 — the
  S3 test asserting blank-string → `[]` is itself an existing test that reversing
  D8 would break. The natural "list view shows all" intent is fully met by Reading
  A (D12) without touching D8.
  **Needs user confirmation:** if the user actually wants a blank search *string*
  (`query=""`/whitespace) to also return all items, confirm and D8 will be
  superseded in a follow-up; until then blank-string → `[]` stands.
