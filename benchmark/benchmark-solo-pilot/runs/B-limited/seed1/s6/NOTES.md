# NOTES

## S6 — Restore original default page size
- DEFAULT_PAGE_SIZE restored to 25 (the S1 original). History: S1 introduced 25; S5 changed 25 -> 40; S6 reverts to 25.
- Applies only when `limit is None`; explicit `limit` still overrides; `limit=0` -> empty.
- Pipeline ORDER (unchanged): `where` (filter) -> `sort` (sort_by) -> `offset` -> `limit`.
- `sort_by`: stable ascending `sorted(..., key=lambda r: r[field])`; equal keys keep insertion order; `None` => no sort.
- `where`: keeps records matching ALL key==value; absent key fails match (no error). Helper `_matches`. Empty/None => no filter.
- deepcopy isolation preserved on add + read.
