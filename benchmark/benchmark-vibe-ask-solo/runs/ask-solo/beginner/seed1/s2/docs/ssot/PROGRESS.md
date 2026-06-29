# PROGRESS

## S0 (seed1) — initial catalog
- Created `catalog.py` with `Catalog`.
- Implemented: `add(item)`, `all()`.
- `search(...)` exposed per contract; list-mode only (other args inert).
- Verified: `python -c "import catalog"` + add/all/copy-safety/list-mode checks pass.
- Decisions recorded: D1-D4.

## S1 (seed1) — name search
- Implemented `search(query=...)`: case-insensitive substring match on `name`
  (`'ap'` matches `'Apple'`); empty query matches all; missing `name` -> `''`.
- List mode (`query=None`) and copy-safety (D3) unchanged.
- Verified: `python -c "import catalog"` + substring/case-insensitive/list-mode/
  empty-query/no-match/copy-safety/missing-name checks pass.
- Decisions recorded: D5 (supersedes D1, D2 for `query`), D6.

## S2 (seed1) — field equality filter (`where`)
- Implemented `search(where=...)`: equality filter on item fields, e.g.
  `where={'category': 'fruit'}`; multiple keys AND together; combines with
  `query` (both must hold).
- Loud-on-mistake: a `where` key present on no item in a non-empty catalog
  raises `KeyError` (catches typos) instead of silently returning nothing; an
  item that merely lacks the key just doesn't match. Empty catalog skips the
  check and returns `[]`.
- List mode, prior `query` behaviour (D5/D6), and copy-safety (D3) unchanged.
- Verified: `python -c "import catalog"` + where-equality / sparse-field /
  unknown-field-raises / query+where AND / multi-key / list-mode / copy-safety /
  empty-catalog checks pass.
- Decisions recorded: D7 (supersedes D1 for `where`), D8.

### Next / deferred
- Define `sort_by` ordering, `limit` cap.
- Persistence (only if a future session asks).
