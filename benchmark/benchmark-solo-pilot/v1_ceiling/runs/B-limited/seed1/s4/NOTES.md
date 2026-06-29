# S4 — Projection (`select`)

Implemented `query(select=[field, ...])`: each returned record keeps ONLY the
selected keys PRESENT on it.

Decisions:
- Applied LAST, on the output copies. Pipeline: where -> sort_by -> paginate ->
  copy out -> select.
- Missing keys are SKIPPED silently (no KeyError, no None filler) — `{k:r[k] for
  k in select if k in r}`. Note: differs from S1 `where`'s hard-error policy;
  select is lenient by ticket ("those present on the record").
- `select=None` => full records (off). `select=[]` => empty dicts.
- S1/S2/S3 policies preserved unchanged. All query params now implemented.
