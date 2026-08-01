# CONVERSATION

## Request
Add a `where={k: v}` equality filter to `Catalog.search` (multiple keys = AND).
Policy: if a `where` key does not exist on every item, raise `ValueError`.
Add tests for the matching, multi-key, and ValueError cases.

## Plan
- The `where` parameter already exists in the pinned contract signature but was
  unimplemented. Implement it in `search`:
  - `where=None` (or empty) -> no equality filter (preserve list/query behaviour).
  - Validate first: every key in `where` must be present on every item in the
    catalog; if any key is missing from any item, raise `ValueError`.
  - Then keep items where `item[k] == v` for all keys (AND).
  - Keep returning copies; preserve insertion order.
- Order of operations: validate + apply `where`, then apply the existing `query`
  substring filter, so the two compose and the ValueError is deterministic.
- Add stdlib `unittest` tests (pytest is not installed in this environment).

## Test run
`python -m unittest test_catalog -v` -> 8 tests, all OK.
Covered: single-key match, no-match -> empty, multi-key AND (incl. conflicting
pair -> empty), where+query combination, ValueError when a key is absent from all
items, ValueError when a key is absent from some items, `where=None` no-op, and
copy semantics. `python -c "import catalog"` succeeds.

## Summary
Implemented the `where` equality filter with AND semantics across keys and the
missing-key -> `ValueError` policy. Existing `add`/`all`/`query` behaviour is
unchanged. Added a self-contained unittest suite; full pass.
