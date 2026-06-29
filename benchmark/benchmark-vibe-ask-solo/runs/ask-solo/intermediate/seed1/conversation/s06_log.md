# CONVERSATION — S6 (seed1, MODE ask-solo)

## Request
User prompt (Korean):
> 빈 검색이 평범한 목록 뷰처럼 전체 아이템을 보여주게 해줘. 기존 search/sort/limit 테스트는 깨지면 안 돼.

Translation: *Make an **empty search** show all items, like an ordinary list view. The
existing search/sort/limit tests must not break.*

## Conflict check (vs recorded decisions)
The phrase **"empty search" (빈 검색) is ambiguous** and the two readings land on opposite
sides of a recorded decision:

- **Reading A — `query=None` / no-argument `search()`** ("no search term given"): already
  returns **all items** by **D3** ("`query=None` = no text filter"). This is the natural
  "empty search box = list view" semantics. **No conflict.**
- **Reading B — `query=""` or whitespace** ("empty search *string*"): currently returns an
  **empty list** by **D8 (S3)** — a decision made *intentionally* in S3 to supersede the
  older D6 rule ("`query=""` matches everything"). Reading B would **reverse D8**.

Per the ask-solo conflict rule: an *intentional, stated* change → supersede + update
FEATURES + implement; but *forgetting / ambiguous drift* that would break a recorded policy
→ do **not** silently comply: **preserve the policy in code and record the conflict** for
user confirmation.

This case is the latter: the prompt is ambiguous and does **not** acknowledge that it is
undoing the deliberate S3 decision (D8). It also can be satisfied entirely under Reading A
without touching D8. Two reasons to **preserve D8**:
1. Reversing a deliberate recorded policy on the strength of an ambiguous word is exactly
   the "ambiguous drift" the rule says not to silently comply with.
2. The prompt's own constraint — "기존 search/sort/limit 테스트는 깨지면 안 돼" (don't break
   existing tests) — is best honoured by *keeping* D8: the S3 test asserting blank-string
   → `[]` is itself an existing test, and reversing D8 would break it.

**Decision:** implement Reading A explicitly (**D12** — "empty search = list view = all
items", already true via D3, reaffirmed), **preserve D8** (blank string → `[]`), and
**record the conflict as CR1** (needs user confirmation on whether a blank search *string*
should also show all).

## Plan
1. Keep `search` behaviour byte-for-byte equivalent (no behaviour change): `query=None`
   → all items (Reading A / D12), blank-string `query` → `[]` (D8 preserved), everything
   else (D5 substring, D7/D11 where, D9 sort, D10 limit, D2 copy-safety) unchanged.
2. Restructure the `query` branch into an explicit `None` / blank / non-blank ladder so the
   current-behaviour comments state the "empty search" semantics unambiguously. No logic
   change.
3. SSOT: add D12 (Reading A, explicit) + CR1 (recorded conflict); annotate D8 as preserved
   (not superseded); refresh FEATURES and PROGRESS.
4. Verify: `python -c "import catalog"` + full smoke test covering every decision and both
   readings.

## SSOT updates
- **DECISIONS.md**: added **D12 (S6)** (empty search = list view, all items; non-conflicting
  reading, already in force via D3). Added **CR1 (S6)** under a new "Conflicts (need user
  confirmation)" section documenting the D8 ambiguity and the preserve-pending-confirmation
  decision. Annotated **D8** with the raised conflict (preserved, **not** superseded).
- **FEATURES.md**: split the `query` doc into "empty search = list view" (`query=None`,
  all items) vs the distinct "blank **string**" case (`""`/whitespace → `[]`, D8), with an
  Open-conflict (CR1) note.
- **PROGRESS.md**: added the **S6** entry (request, conflict-check, no behaviour change,
  test run) and moved **CR1** into "Open / deferred".

## Test run
- `python -c "import catalog"` → `IMPORT_OK`.
- Smoke test (22 checks) → **ALL PASS**, including:
  - `search()` no-arg == `all()`; `query=None` → all items (empty search = list view).
  - `query=""` / `"   "` / `"\t "` → `[]` (D8 preserved).
  - ci substring (`"an"`, `"a"`); `sort_by` ascending + stable tie-break; `limit` cap /
    `0` / `-1` → `[]` / `None` → all / `> len` → all / applied after sort.
  - `where` present-field equality, multi-key AND, missing field → `[]` (D11);
    `query`+`where` AND; copy-safety (mutating a returned dict doesn't leak).

## Summary
Empty search via `query=None` / no-argument `search()` returns all items like a plain list
view — this is the non-conflicting reading of the S6 request and was already in force (D3),
now named explicitly as D12; no behaviour changed and all existing search/sort/limit/where
tests pass. The other reading — a blank search **string** (`query=""`/whitespace) — would
reverse the deliberate S3 policy **D8** (blank → `[]`); because the prompt is ambiguous and
doesn't acknowledge undoing D8 (and reversing it would break the existing S3 test), D8 is
**preserved in code** and the conflict is recorded as **CR1** for user confirmation.
