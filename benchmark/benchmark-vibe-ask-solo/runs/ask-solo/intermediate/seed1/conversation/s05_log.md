# CONVERSATION — S5 (seed1, ask-solo)

## Request
> 없는 where 필드 동작을 바꾸자: raise 하지 말고 그냥 빈 결과를 반환하도록 변경해줘.

Change the missing-`where`-field behaviour: don't raise — return an empty result instead.

## Conflict check
- This targets **D7 (S2)**, which decided a `where` field missing from any item under
  test raises `ValueError`.
- The S5 prompt **intentionally** reverses that consequence (raise → empty result).
  This is a deliberate change to a recorded decision, not forgetting/ambiguous drift.
- Resolution: **supersede** D7's raise-clause with a new **D11 (S5)**, update FEATURES,
  then implement. D7's equality-match (`item[field] == value`), multi-key AND, and the
  precedence (query → where → sort_by → limit) are **preserved** — only the missing-field
  consequence changes.

## Plan
1. In `search`, keep the missing-field detection identical to D7 (the `where` field is
   absent from at least one item remaining after the `query` stage), but on that
   condition set `results = []` instead of raising.
2. Leave the present-field equality filter, and the `sort_by`/`limit` stages, unchanged
   (both are no-ops on an empty list).
3. Preserve all other policies: D2 copy-safety, D3 no-arg search / `query=None` = off,
   D5 case-insensitive substring, D8 blank-query → [], D9 sort ascending+stable,
   D10 limit cap.

## SSOT updates
- **DECISIONS.md** — added **D11 (S5)**: missing `where` field → empty result (matches
  nothing), not `ValueError`. Marked the relevant clause of **D7** superseded-in-part by
  D11 (D7 match/AND/precedence remain in force).
- **FEATURES.md** — `where` bullet now reads: a missing `where` field returns an empty
  list (matches nothing) *(S5; supersedes the S2 raise rule)*.
- **PROGRESS.md** — added the S5 entry (request, conflict→supersede D7, verification).
- PRODUCT.md — unchanged (public surface and product description are stable).

## Test run
`python -c "import catalog"` → OK. Smoke test (all PASS):
- **S5 new behaviour:** `where={"qty": 3}` with an item lacking `qty` → `[]` (no raise);
  missing field surfacing only after a `query` survivor lacks it → `[]`; `query`+`where`
  where all survivors have the field → normal equality filter.
- **Preserved:** present-field equality (single + multi-key AND) and present-field
  no-match → `[]`; `query`+`where` AND; no-arg search == `all()`; `query=None` → all;
  blank `query` (`""`/whitespace) → `[]`; case-insensitive substring; `sort_by` ascending
  with stable ties; `limit` cap / `0` / negative → `[]` / `None` → all; copy-safety.

## Summary
A missing `where` field now returns an empty result instead of raising `ValueError`
(D11 supersedes D7's raise-clause); D7's equality-match, multi-key AND, precedence and
all other prior policies are preserved. SSOT (FEATURES, DECISIONS, PROGRESS) updated and
the import + smoke test pass.
