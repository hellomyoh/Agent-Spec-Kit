# CONVERSATION

## Request
Add an equality filter `search(where={field: value})`. Multiple keys are combined
with AND. If a `where` field is present on no item at all, raise `ValueError`.

## Plan
- Keep existing `query` (case-insensitive substring on `name`) and copy-on-return behaviour.
- Validate `where` first: for each field, if it is absent from every stored item, raise
  `ValueError`. This guards against typo'd / unknown filter fields.
- Then keep items where all `field == value` pairs match (AND). An item missing a queried
  field is excluded (not an error, as long as the field exists on some other item).
- `where=None` and `where={}` mean "no filter".
- `where` composes with `query` (both must match).

## Test run
`python -c "import catalog"` -> IMPORT OK.
Behavioural checks (all PASSED):
1. single-key where filters correctly.
2. multi-key where = AND.
3. field absent from every item -> ValueError.
4. existing field with non-matching value -> empty list (no error).
5. query + where applied together (AND).
6. field present on only some items is valid; items lacking it are excluded.
7. `where=None` / `where={}` -> no filter (all items).
8. results are copies; mutating them does not change internal state.
9. one valid + one unknown field -> ValueError (validated before filtering).

## Summary
`where` equality filtering added with AND semantics and an unknown-field `ValueError`
guard. Prior `query`, list mode, ordering, and copy-on-return behaviour preserved.
`sort_by` / `limit` remain accepted but unused (not requested this session).
