# NOTES

## S4 — `sort_by` (now implemented)
- `query(sort_by=field)`: stable ascending sort by `record[field]`. Uses `sorted(..., key=lambda r: r[field])`; Python's stable sort keeps insertion order for equal keys. `sort_by is None` => no sorting.
- Pipeline ORDER (final): `where` (filter) -> `sort` (sort_by) -> `offset` -> `limit`. Sort applied BEFORE pagination, as ticket requires.
- `where`: keeps records matching ALL key==value; absent key fails match (no error). Helper `_matches`. Empty/None `where` => no filter.
- DEFAULT_PAGE_SIZE=25 when `limit is None`; explicit `limit` overrides; `limit=0` -> empty. deepcopy isolation preserved on add + read.
