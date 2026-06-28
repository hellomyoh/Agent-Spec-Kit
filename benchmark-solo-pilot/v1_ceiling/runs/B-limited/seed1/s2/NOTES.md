# S2 — Sorting (`sort_by`)

Implemented `query(sort_by=field)`: ascending sort by that field's value.

Decisions:
- POLICY (applies to ALL future `sort_by`): STABLE sort — ties (equal sort keys)
  keep INSERTION ORDER. Used Python `sorted(key=lambda r: r[sort_by])`, which is
  stable, so this falls out for free.
- Applied AFTER `where` filtering, on the filtered set, BEFORE copying out.
- `sort_by=None` => no sorting (unchanged). `where` policy from S1 preserved.
- limit/offset/select still unimplemented (future tickets).
