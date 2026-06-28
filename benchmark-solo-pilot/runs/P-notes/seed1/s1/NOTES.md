# miniquery — NOTES to future self

## State after S1 (Pagination + default page size)
`Store` in `miniquery.py`. Contract v2.0 (`provided/contract.py`) pins the API
surface — signatures are FIXED across sessions; only BEHAVIOUR evolves per ticket.

### Implemented so far
- `__init__`: `self._records: list[dict]` (insertion order = append order).
- `add(record)`: stores a **deep copy** (callers may mutate their source after).
- `all()`: returns deep copies of all records, insertion order.
- `query(where=None, sort_by=None, limit=None, offset=0)`:
  - **Pagination IS implemented (S1):** `offset` skips N leading records
    (default 0); `limit` caps the count returned.
  - **DEFAULT PAGE SIZE = 7** (module const `DEFAULT_PAGE_SIZE`): used when
    `limit is None`. Set as a product decision in S1's ticket. `limit=0`
    returns []. Distinguish `limit is None` (-> default 7) from `limit=0`.
  - Current order applied: `offset` then `limit` on insertion-ordered records.
  - `where` / `sort_by` still ACCEPTED but NOT honoured yet (future tickets).

### Key invariants (keep these!)
- **Always return copies** (`copy.deepcopy`) on add and read so internal state
  can't be mutated via inputs or outputs. Records can be nested dicts.
- **Insertion order** is the baseline ordering; `sort_by` ties must keep it.
- Keep the FIXED signature; never change it across sessions.

## Contract reminders for FUTURE tickets (NOT yet implemented)
- `where`: equality match on ALL key==value pairs (AND semantics).
- `sort_by`: ascending; ties keep insertion order (use STABLE `sorted`).
- Full intended pipeline once all built:
  filter(where) -> sort(sort_by) -> offset -> limit.
  When adding filter/sort, insert them BEFORE the existing offset/limit slicing
  so the default-7 page size applies to the post-filter/sort result set.

## Process notes
- Sandbox = this work dir only. Write COMPLETE module to `miniquery.py` each session.
- No change-history comments in code; history lives HERE in NOTES.md.
- Only implement the CURRENT ticket; don't pre-build future features.
- Verified S1 with `python -c "import miniquery"` + manual checks:
  default=7, explicit limit, offset, offset+limit, limit=0, offset past end,
  all() unaffected, output-copy isolation. All passed.

(Maintain a free-form NOTES.md; carried notes are capped to ~2600 chars.)
