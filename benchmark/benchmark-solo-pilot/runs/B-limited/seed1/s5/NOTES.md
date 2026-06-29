# NOTES

## S5 — Default page size = 40
- DEFAULT_PAGE_SIZE changed 25 -> 40 (applies only when `limit is None`). Explicit `limit` still overrides; `limit=0` -> empty.
- Pipeline ORDER (final): `where` (filter) -> `sort` (sort_by) -> `offset` -> `limit`.
- `sort_by`: stable ascending `sorted(..., key=lambda r: r[field])`; equal keys keep insertion order; `None` => no sort.
- `where`: keeps records matching ALL key==value; absent key fails match (no error). Helper `_matches`. Empty/None => no filter.
- deepcopy isolation preserved on add + read.
