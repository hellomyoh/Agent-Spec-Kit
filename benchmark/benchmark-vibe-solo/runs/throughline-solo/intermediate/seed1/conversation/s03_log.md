# CONVERSATION — S3 (seed1, throughline-solo)

## Request
(From USER_PROMPT.md, Korean.) Two changes to `search`:
1. Support `search(sort_by=field)` — ascending order, with stable tie-breaking
   (items with equal keys keep insertion order).
2. If `query` is whitespace/empty, return an empty list instead of all items.

## Conflict check (vs recorded decisions)
- **Part 1 (sort_by ascending + stable):** No conflict. `sort_by` already existed
  (D4/D6) as "order-by-field", implemented with Python's `sorted`, which is already
  ascending and stable. S3 only pins the order/tie semantics that were loosely
  specified. Recorded as **D9** (clarification, no behaviour change).
- **Part 2 (blank query → empty list):** **Conflicts with D6 (S1)**, which stated
  `query=""` matches every item (and FEATURES echoed this). The S3 prompt requests
  this change *intentionally and explicitly* ("return empty list instead of all"),
  so per throughline-solo policy this is a **supersede**, not a drift to preserve. D6's
  empty-string clause is superseded by **D8**; D6's precedence + query/where-AND
  parts stay in force.
  - `query=None` remains "no text filter" (D3 preserved). `None` and a blank string
    are now distinct: `None` passes all items through; a blank/whitespace string
    filters everything out.
  - "Blank" defined as `query.strip() == ""`, covering `""` and any all-whitespace
    string (folds the "whitespace" case into the same rule).

## Plan
1. In `search`, split the `query is not None` branch: if `query.strip() == ""` →
   `results = []`; else the existing D5 case-insensitive substring match.
2. Keep `sort_by` as stable `sorted(key=item.get(sort_by))`; add a current-behaviour
   comment noting ascending + stable ties.
3. Update SSOT: FEATURES (query blank rule, sort_by ascending/stable), DECISIONS
   (D8, D9; mark D6 empty-string clause superseded), PROGRESS (S3 entry).
4. `import catalog` + smoke test.

## SSOT updates
- **FEATURES.md:** rewrote the `query=""` line (now blank → empty list, S3); noted
  `sort_by` is ascending + stable (S3).
- **DECISIONS.md:** added **D8** (blank query → empty list; supersedes D6 empty-string
  clause; D3/D5 preserved) and **D9** (sort_by ascending + stable). Annotated D6 as
  superseded-in-part.
- **PROGRESS.md:** added S3 (DONE) entry recording the conflict + supersede.

## Test run
`python -c "import catalog"` → OK. Smoke test (all assertions passed):
- sort ascending + stable ties: `['apple','avocado','Banana','Cherry']` (Banana/Cherry
  both qty=3, insertion order kept).
- `query=""` / `"   "` / `"\t\n "` → `[]`.
- `query=None` and no-arg `search()` → all 4 items (D3 preserved).
- non-blank substring `query='a'` → `['Banana','apple','avocado']` (case-insensitive,
  insertion order); `query='CHERRY'` → `['Cherry']`.
- blank query + `where={missing}` → `[]` (no ValueError; empty set can't be field-tested).
- `where={'qty':3}` → `['Banana','Cherry']`; `where={missing}` on non-empty set → ValueError (D7).
- `query='a'` + `where={'qty':3}` → `['Banana']` (AND).
- `sort_by='qty', limit=2` → `['apple','avocado']`.
- copy-safety: mutating a returned dict does not affect internal state (D2).

## Summary
Implemented S3: `sort_by` documented as ascending + stable (D9, no behaviour change),
and blank/whitespace `query` now returns `[]` (D8), which intentionally supersedes
D6's old `query=""`-matches-all rule. All prior policies (D2 copy-safety, D3 `query=None`
= no filter, D5 substring, D6 precedence/AND, D7 `where`) preserved. SSOT and
`catalog.py` updated; import + smoke tests green.
