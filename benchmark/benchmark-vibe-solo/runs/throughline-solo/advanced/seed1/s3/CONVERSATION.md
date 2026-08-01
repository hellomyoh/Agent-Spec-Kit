# CONVERSATION — S3 (advanced, seed1), MODE throughline-solo

## Request (USER_PROMPT.md)
Add `sort_by` (ascending, stable sort). Safety policy: a blank/whitespace-only
`query` returns `[]` (an empty search box must not dump the whole catalog). Keep
all existing tests green.

## Conflict check (vs recorded decisions)
Two parts, handled separately:

1. **`sort_by`** — currently `[planned]` and raising `NotImplementedError` under
   D2 (out-of-scope args raise). Specifying it is exactly what D2 anticipated
   ("future sessions supersede this per-argument"). **No policy conflict** →
   implement and supersede D2 for `sort_by` only.

2. **Blank `query` → `[]`** — **conflicts with D4**, which deliberately decided a
   blank/whitespace-only `query` is *list mode* (return all items). This is not
   forgetting or ambiguous drift: the user states the new behaviour and its
   safety rationale explicitly. Per throughline-solo, an **intentional change** →
   **supersede** the conflicting decision and update FEATURES, then implement
   (do not silently comply, do not refuse). So D4's blank half is recorded as
   superseded by **D6**.
   - **Scope guard:** the contract (CONTRACT_VERSION 1.0) fixes `query=None` as
     "no text filter" (list mode), and the prompt named only blank/whitespace-only
     *strings*. So `query=None` is preserved as list mode; only an
     actually-supplied empty/blank string now returns `[]`. Changing `None` too
     would have broken the pinned contract — avoided.

## Plan
- `catalog.py` (complete rewrite of `search` body):
  - Blank/whitespace-only `query` string → `[]`; `query=None` → list mode;
    non-blank `query` → existing case-insensitive substring match.
  - `sort_by`: order the post-filter results ascending via `sorted()` (stable, so
    equal keys keep insertion order). Missing field on any result item →
    `ValueError` (mirrors D5 `where` policy); incomparable types → `TypeError`
    (natural Python behaviour, let propagate).
  - Pipeline: filter by `query` then `where`, then `sort_by`.
  - `limit` still unspecified → still raises `NotImplementedError` (D2), incl.
    combined with `sort_by`.
- SSOT updates (below).
- Tests: refresh `test_catalog.py` (blank query now `[]`, `None` still list mode;
  add sort_by cases; preserve all still-valid prior coverage).

## SSOT updates
- **DECISIONS.md**
  - D2 header/status: superseded for `sort_by` (S3); only `limit` still raises.
  - D4 header/body: blank handling marked SUPERSEDED by D6; substring rule kept.
  - D5 footer: note `sort_by` now specified by D7.
  - **D6** (new): blank/whitespace-only `query` → `[]`; explicit `query=None`
    scope guard; reasoning + supersede note.
  - **D7** (new): `sort_by` ascending + stable; pipeline order; missing-key
    `ValueError`; incomparable-type `TypeError`; `limit` still raises.
- **FEATURES.md**: `query` line rewritten (None=list mode, blank string=`[]`);
  `sort_by` moved to `[done]`; footer now lists only `limit` as unspecified.
- **PROGRESS.md**: added S3 entry (work, conflict check, decisions, tests,
  verification); refreshed "Next" (limit semantics; possible sort direction).
- **PRODUCT.md**: unchanged (describes the pinned contract surface only; still
  accurate).

## Test run
- `python -c "import catalog"` → import OK.
- `python test_catalog.py` → **28 tests passed**.
- Coverage: copy in/out isolation (D1), insertion order (D3), query substring +
  insertion order + no-match (D4), `query=None` list mode (contract), blank/empty
  string → `[]` (D6), where single/multi-key AND + no-match + empty `{}` + missing
  key on all/some → `ValueError` + where∘query (D5), sort_by ascending +
  stability + after-query + after-where + missing-key `ValueError` +
  incomparable-type `TypeError` + internal-order-unchanged (D7), limit
  `NotImplementedError` alone / with query / with sort_by (D2).
- One self-inflicted test bug found and fixed during the run: an early
  query-filter case used `query="ap"` with a "grape" item (which contains "ap"),
  so the expected set was wrong; replaced with non-overlapping names.

## Summary
Implemented `sort_by` (ascending, stable, filter-then-sort, missing-key
`ValueError`) and the user's blank-query safety policy (blank/whitespace-only
string → `[]`). The blank-query change conflicted with D4 and was an explicit,
intentional change, so D4's blank half was superseded by D6 (with `query=None`
preserved as contract list mode); `sort_by` superseded D2 for that argument only.
SSOT updated; full suite green (28 tests).
