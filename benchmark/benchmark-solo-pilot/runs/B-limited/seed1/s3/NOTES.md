# NOTES

## S3 — Default page size = 25
- DEFAULT_PAGE_SIZE changed 7 -> 25 (applies only when `limit is None`). Explicit `limit` still overrides; `limit=0` -> empty.
- Pipeline ORDER unchanged: `where` (filter) -> `offset` -> `limit`. Sort slots between `where` and `offset` when `sort_by` lands.
- `where`: keeps records matching ALL key==value; absent key fails match (no error). Helper `_matches(record, where)`. Empty/None `where` => no filter.
- deepcopy isolation preserved on add + read.
- NOT yet implemented: `sort_by` (arg present in FIXED signature but inert). Do not pre-build.
