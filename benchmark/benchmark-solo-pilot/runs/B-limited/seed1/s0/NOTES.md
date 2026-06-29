# NOTES

## S0 — Scaffold
- `Store` class in `miniquery.py` per contract v2.0.
- `query` signature is FIXED: `(where, sort_by, limit, offset=0)`. Keep it stable.
- Implemented this session: `add` (stores deepcopy), `all` (returns deepcopies, insertion order), `query()` returns all (delegates to `all`).
- Isolation: deepcopy on BOTH add and read so nested values can't leak/mutate internal state.
- NOT yet implemented (future tickets): where-filter, sort_by, limit/offset, default page size. Do not pre-build.
