# NOTES

## S2 — `where` equality filter
- `query(where=...)`: keeps records matching ALL key==value pairs. Absent key on a record => that record fails the match (no error). Empty/None `where` => no filtering.
- Pipeline ORDER: `where` (filter) -> `offset` -> `limit`. Sort would slot between where and offset when it lands.
- Helper `_matches(record, where)` does the per-record check (`k in record and record[k]==v`).
- DEFAULT_PAGE_SIZE=7 when `limit is None`; `limit=0` -> empty. deepcopy isolation preserved.
- NOT yet implemented: `sort_by` (arg present in FIXED signature but inert). Do not pre-build; apply BEFORE offset/limit when ticketed.
