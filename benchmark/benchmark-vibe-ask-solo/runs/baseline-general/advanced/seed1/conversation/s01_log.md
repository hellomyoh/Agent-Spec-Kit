# Conversation — advanced S1

## Request
Add `query` support to `Catalog.search`:
- A `query` that is not None and not blank/whitespace does a case-insensitive
  substring match against each item's `name`.
- `query=None` keeps list mode (returns all items).

## Plan
- Read contract (FIXED API) and current `catalog.py`. Signature already includes
  `query`, so only behaviour changes inside `search`.
- In `search`: if `query is not None and query.strip()`, filter `_items` to those
  whose `name` (lowercased) contains the query (lowercased). Otherwise no text
  filter (list mode) — this covers `query=None` and blank/whitespace-only queries,
  matching the prompt's "not None and not blank" wording.
- Preserve insertion order and continue returning copies of item dicts.
- Leave `where`, `sort_by`, `limit` untouched (not in scope this session).

## Test run
`python -c "..."` smoke test covering:
- list mode for `search()`, `query=None`;
- case-insensitive substring (`'apple'`, `'APP'`, `'rry'`) and no-match (`'xyz'`);
- blank `''` and whitespace `'   '` -> list mode;
- returned dicts are copies (mutating a result does not affect internal state);
- insertion order preserved.

Result: ALL TESTS PASSED.

## Summary
`search` now applies a case-insensitive substring filter on `name` for a non-blank
`query`, and stays in list mode for `query=None` or a blank/whitespace query.
Results remain insertion-ordered copies. No other API surface changed.
