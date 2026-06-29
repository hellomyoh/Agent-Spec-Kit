# CONVERSATION — advanced S6

## Request
For a new list view, a **blank** `query` (empty string or whitespace-only) must
now return **all** items instead of `[]`. This intentionally supersedes the S3
empty-search guard. Keep `where`, `sort_by`, `limit`, and unknown-field
behaviour unchanged. Update docs/tests to match.

## Plan
- The S3 guard returned `[]` early for a blank/whitespace-only query
  (`if query is not None and not query.strip(): return []`). Remove that guard.
- A blank query must mean "no text filter" — the same as `query=None`. Simply
  deleting the guard is not enough: the substring filter `needle in name` would
  then run with `needle=""` (matches all, fine) but `needle="  "` would match
  only names containing those spaces, which is wrong. So gate the substring
  filter on a **non-blank** query: apply it only when `query is not None and
  query.strip()`. Blank/None both fall through to no text filter.
- Leave the pipeline order and every other branch untouched: `limit < 0`
  validation up front, then `where` (AND equality, missing key filtered out, not
  an error), then the text filter, then `sort_by` (stable ascending), then
  `limit` (top-N, applied last; `0` -> `[]`).

## Test run
`python -c "import catalog"` succeeds. Ran an inline assertion suite covering:
- NEW: `query=''` and `query='   '` return all items in insertion order.
- `query=None` still list mode (unchanged); non-blank query still
  case-insensitive substring on `name`.
- Blank query composes with `where` / `sort_by` / `limit` (e.g.
  `query='', where={'cat':'fruit'}`; `query='  ', sort_by='price'`;
  `query='', limit=2`; `query='', limit=0` -> `[]`).
- `where`: AND of keys; a key missing from an item is not an error and filters
  the item out; a key absent from all items -> `[]`.
- Unknown field in `where` -> `[]` (no error).
- `limit=-1` -> `ValueError` (unchanged); `sort_by` + `limit` yields top-N.
- Returned dicts are copies (mutating a result does not change the catalog).

Result: `ALL PASS`.

## Summary
Blank/whitespace-only `query` now behaves as list mode (no text filter) and
returns the whole catalog, subject to `where`/`sort`/`limit`. The S3
empty-search guard is removed. All other behaviour — `query=None`, non-blank
substring matching, `where` semantics, unknown-field handling, `sort_by`,
`limit`, the negative-limit `ValueError`, and copy-on-return — is preserved.
Docstrings and `docs/NOTES.md` updated to describe the new blank-query rule.
