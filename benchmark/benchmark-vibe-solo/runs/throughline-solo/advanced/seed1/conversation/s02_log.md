# CONVERSATION — S2 (advanced, seed1)

## Request
Add a `where={k: v}` equality filter to `search()` (multiple keys = AND).
Policy: if a `where` key is not present on every item, raise `ValueError`.
Add tests for the matching, multi-key, and ValueError cases.

## Conflict check (vs recorded decisions)
- D2 (S0) made every out-of-scope `search()` argument — including `where` —
  raise `NotImplementedError` until a session specifies it. This session
  specifies `where`, so this is an **intentional, user-directed supersede**, not
  forgetting/drift. Resolution: supersede D2 for `where` (mirroring how D4
  superseded it for `query` in S1), then implement.
- The missing-key `ValueError` policy is a new, user-requested rule; it conflicts
  with nothing recorded. It also aligns with D2's spirit (don't silently drop a
  filter the caller asked for) — a missing key surfaces as an error instead of
  silently matching nothing.
- `sort_by` and `limit` stay unspecified → preserved under D2; they still raise
  `NotImplementedError`, including when combined with `where`.

No forbidden silent compliance: prior behaviour (copy in/out D1, insertion order
D3, query semantics D4) is preserved unchanged.

## Plan
1. In `search()`, replace the blanket `where` rejection with: validate every
   `where` key exists on every catalog item (else `ValueError`), then filter by
   AND equality. Keep `sort_by`/`limit` raising `NotImplementedError`.
2. Validate `where` keys over the full catalog (not just query-matched items) so
   the error is independent of any co-supplied `query`.
3. Preserve copy-on-read and insertion order.
4. Add behavioural tests; update SSOT.

## SSOT updates
- DECISIONS.md: added **D5** (`where` = AND equality, keys must exist on every
  item else `ValueError`, composes with `query`); updated **D2** status header
  and body to note it is superseded for `where` (S2).
- FEATURES.md: `where` moved [planned] -> [done] with policy; narrowed the
  "still unspecified" note to `sort_by`/`limit` only.
- PROGRESS.md: added S2 entry; trimmed the Next list to `sort_by`/`limit`.

## Test run
- `python -c "import catalog"` -> import ok.
- `python test_catalog.py` -> 14 tests passed: single-key match, multi-key AND
  (incl. tightened value dropping a non-match), no-match empty, where+query
  composition, copy-on-read isolation, ValueError when a key is missing on all
  items and on some items, where+sort_by still NotImplementedError; plus
  preserved prior tests (insertion order, copy-on-add/read, query case-insensitive
  substring + blank list mode, sort_by/limit NotImplementedError).

## Summary
`where` equality filtering is implemented with AND semantics and the requested
missing-key `ValueError` policy, composing with `query` and preserving copy/order
invariants. `sort_by`/`limit` remain unspecified and still raise. SSOT and tests
updated; all checks green.
