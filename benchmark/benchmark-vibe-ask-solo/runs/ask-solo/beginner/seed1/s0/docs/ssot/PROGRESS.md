# PROGRESS

## S0 (seed1) — initial catalog
- Created `catalog.py` with `Catalog`.
- Implemented: `add(item)`, `all()`.
- `search(...)` exposed per contract; list-mode only (other args inert).
- Verified: `python -c "import catalog"` + add/all/copy-safety/list-mode checks pass.
- Decisions recorded: D1-D4.

### Next / deferred
- Define `search` text matching (`query`): matching rules, blank handling.
- Define `where` equality filter, `sort_by` ordering, `limit` cap.
- Persistence (only if a future session asks).
