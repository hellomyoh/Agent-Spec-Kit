# miniquery — NOTES to future self

## State after S2 (Equality filter `where`)
`Store` in `miniquery.py`. Contract v2.0 (`provided/contract.py`) pins the API
surface — signatures are FIXED across sessions; only BEHAVIOUR evolves per ticket.

### Implemented so far
- `__init__`: `self._records: list[dict]` (insertion order = append order).
- `add(record)`: stores a **deep copy** (callers may mutate their source after).
- `all()`: returns deep copies of all records, insertion order.
- `query(where=None, sort_by=None, limit=None, offset=0)` pipeline so far:
  filter(where) -> offset -> limit. (sort still pending — see below.)
  - **`where` IS implemented (S2):** keeps records matching ALL key==value
    pairs (AND). A key ABSENT from a record FAILS the match (no error). Test is
    `all(k in r and r[k]==v ...)`. Empty/None `where` = no filtering.
    Value-equality (`==`), not identity.
  - **Pagination (S1):** `offset` skips N leading records of the FILTERED set;
    `limit` caps count. **DEFAULT_PAGE_SIZE = 7** when `limit is None`.
    `limit=0` returns []. Distinguish `limit is None` (->7) from `limit=0`.
    Default-7 applies to the POST-filter result set (filter runs first).
  - `sort_by` still ACCEPTED but NOT honoured yet (next ticket).

### Key invariants (keep these!)
- **Always return copies** (`copy.deepcopy`) on add and read so internal state
  can't be mutated via inputs or outputs. Records can be nested dicts.
- **Insertion order** is the baseline ordering; `sort_by` ties must keep it.
- Keep the FIXED signature; never change it across sessions.

## Contract reminders for FUTURE tickets (NOT yet implemented)
- `sort_by`: ascending; ties keep insertion order (use STABLE `sorted`).
- Full intended pipeline once all built:
  filter(where) -> sort(sort_by) -> offset -> limit.
  Insert `sort` AFTER filter and BEFORE the offset/limit slicing so default-7
  page size applies to the filtered+sorted result set.

## Process notes
- Sandbox = this work dir only. Write COMPLETE module to `miniquery.py` each session.
- No change-history comments in code; comments describe CURRENT behaviour only.
  History lives HERE in NOTES.md.
- Only implement the CURRENT ticket; don't pre-build future features.
- Verified S2 with `python -c "import miniquery"` + manual checks: AND match,
  single-key multi-match, missing key -> no match, empty where, where+offset+limit
  (filter-first), limit=0, output-copy isolation, no-where unchanged (default 7).
  All passed. (S0/S1 checks also previously passed.)

(Maintain a free-form NOTES.md; carried notes are capped to ~2600 chars.)
