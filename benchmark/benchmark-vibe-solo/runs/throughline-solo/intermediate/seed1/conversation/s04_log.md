# CONVERSATION — S4 (seed1, throughline-solo)

## Request
> search(limit=n)으로 결과 개수를 제한해줘. 정렬과 필터링은 기존처럼 유지하고.

Limit the number of results with `search(limit=n)`. Keep sorting and filtering
as before.

## Conflict check (vs recorded decisions)
No conflict.
- `limit` is a FIXED contract parameter (provided/contract.py) and was already
  implemented as "cap count" (D4, S0) applied last in the precedence
  query → where → sort_by → limit (D6, S1). FEATURES already said
  "`limit` → caps the number of results".
- The S4 prompt asks for exactly that, and explicitly says to keep sort/filter
  unchanged. So the requested behaviour is already in force — this is an
  affirm-and-pin, not a behaviour change for the common (positive) case.
- The only loose edge was a **non-positive** `limit`: the old `results[:limit]`
  slice let a negative `n` fall through to Python's negative-index slicing
  (e.g. `[:-1]` drops the last item), which is a misleading reading of "limit
  the result count". Pinned this edge (D10) the same way D9 clarified `sort_by`.

## Plan
1. Pin `limit` semantics: `limit=n` keeps the first `n` items, applied last
   (after query/where/sort_by); `limit=None` → no cap; non-positive `limit`
   (`0`/negative) → empty list.
2. Implement the non-positive clamp; leave positive-limit, sort, and filter
   code untouched (preserve prior behaviour).
3. Update SSOT (DECISIONS D10, FEATURES, PROGRESS) and write the complete
   catalog.py.

## SSOT updates
- DECISIONS: added **D10 (S4)** — `limit` count-cap semantics, incl. the
  non-positive → empty-list edge; clarifies D4's "cap count" (no change to
  positive-limit behaviour). D6 precedence preserved.
- FEATURES: `limit` bullet now states first-`n` cap, applied last, `None` = no
  cap, non-positive → empty list *(S4)*.
- PROGRESS: added S4 entry (done); Open/deferred remains none.

## Test run
`python -c "import catalog"` → OK.
Smoke test (all assertions passed):
- limit: cap to first n; `=0` → []; `<0` → [] (clamped); `=None` → all;
  `>len` → all.
- precedence: limit applied after `sort_by`, after `query`, and with
  query+sort+limit combined.
- preserved: no-arg search == all; `query=None` → all; blank query (`""` /
  whitespace) → []; case-insensitive substring match; `where` equality AND;
  missing `where` field → ValueError; `sort_by` ascending + stable ties;
  read copy-safety.

## Summary
S4 pins `search`'s `limit` as a first-`n` count cap applied after sort/filter,
with non-positive limits returning an empty list. Sorting and filtering are
unchanged; the only real effect is making the previously-undefined non-positive
edge well-defined. SSOT updated (D10) and catalog.py rewritten in full;
import + smoke tests green.
