# CONVERSATION — S1 (advanced, seed1), ASK-solo

## Request
Add `query` to `search()`: a non-None, non-blank `query` does case-insensitive
substring matching on `name`. `query=None` keeps list mode (all items).

## Conflict check (vs recorded decisions)
- **D2** (out-of-scope search args raise `NotImplementedError`): D2 explicitly
  planned to be superseded per-argument as behaviour is defined. Defining `query`
  is an intentional, in-scope change -> **supersede D2 for `query`** and update
  FEATURES. `where`/`sort_by`/`limit` stay unspecified and keep raising.
- **D1** (copy in/out): preserved — filtered results are still deep-copied on read.
- **D3** (insertion order): preserved — matches are returned in insertion order.
- No drift that would silently break a recorded policy. The anti-silent-ignore
  spirit of D2 is upheld: `query` combined with an unspecified arg still raises.

## Plan
1. In `search()`, drop `query` from the raise guard; keep `where`/`sort_by`/`limit`
   raising.
2. If `query` is not None and not blank (after `strip()`), filter items whose
   `name` contains the query as a case-insensitive substring (`str.casefold()`).
   Otherwise list mode.
3. Deep-copy results on the way out (D1).
4. SSOT: supersede D2 for `query`, add D4 (query semantics + blank handling),
   refresh FEATURES and PROGRESS.

## Ambiguity resolved (D4)
Prompt fixed `query=None` as list mode but left blank/whitespace-only `query`
implicit. Chosen: treat blank/whitespace-only as list mode too (no meaningful
needle; a blank substring would match everything anyway). Recorded in D4. This is
a deliberate choice on an unspecified input, not a silent drop of a real filter.

## SSOT updates
- `DECISIONS.md`: D2 annotated as superseded-for-`query` by D4; added D4.
- `FEATURES.md`: `query` moved to [done] (S1); `where`/`sort_by`/`limit` remain
  [planned] and still raise.
- `PROGRESS.md`: added S1 entry; refreshed "Next".

## Test run
`python -c "import catalog"` -> OK.
Behavioural smoke tests -> ALL SMOKE TESTS PASSED:
- case-insensitive substring match on `name`;
- insertion order preserved among matches;
- `query=None` and blank/whitespace-only (`""`, `"   "`, `"\t"`) -> all items;
- no-argument `search()` -> all items;
- no match -> empty list;
- copy-on-read isolation (mutating a result does not change stored items);
- `where` / `sort_by` / `limit` each raise `NotImplementedError`;
- `query` + `limit` still raises (no silent ignore).

## Summary
`search(query=...)` now performs case-insensitive substring matching on `name`,
with None/blank meaning list mode; insertion order and copy-on-read are preserved;
`where`/`sort_by`/`limit` remain unspecified and still raise. SSOT updated (D4
added, D2 superseded for `query`).
