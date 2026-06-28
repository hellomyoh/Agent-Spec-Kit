# PROGRESS

## S0 (seed1) — DONE
- Created `catalog.py` with the full pinned contract surface: `Catalog.add`,
  `.all`, `.search(query, where, sort_by, limit)`.
- This session's behaviour: `search()` with no arguments returns all items.
- Verified via `python -c "import catalog"` plus a smoke test (no-arg search == all,
  copy-safety).
- SSOT updated: PRODUCT, FEATURES, DECISIONS (D1–D4).

## Open / deferred
- Precise `query` text-search semantics (matching rules, blank handling) — to be
  defined by a future user prompt.
