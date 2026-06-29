# PROGRESS

(maintain this SSOT doc across sessions)

## Done
### S0 — Scaffold
- Created `miniquery.py` with `class Store` per `provided/contract.py` (v1.0).
- Implemented:
  - `add(record)` — stores a shallow copy.
  - `all()` — returns all records as copies, in insertion order.
  - `query()` — no-argument: returns all records as copies.
- `query()` declared with full pinned signature; extra params inert (not implemented).
- Sanity-checked: `import miniquery` OK; verified copy-in / copy-out isolation
  and insertion order via a throwaway `python -c` check.
- SSOT docs initialised: PRODUCT, DATA_MODEL, DECISIONS (D1–D5), PROGRESS.

### S1 — Equality filter (`where`)
- Implemented `query(where={k: v, ...})`: keep records matching ALL key==value
  pairs (AND), `==` comparison, insertion order, returned as copies.
- Empty/None `where` is a no-op (returns all) — S0 behaviour preserved.
- Unknown-field policy (D6): a `where` key absent from EVERY stored record raises
  `KeyError(key)`. A record merely lacking the key is filtered out, not an error.
- Sanity-checked via `python -c`: single/multi-key AND, no-match, KeyError on
  unknown key, copy-out isolation, and missing-key-in-some-records all OK.
- SSOT updated: DECISIONS D6 (+ note on D5), PRODUCT status, this entry.

### S2 — Sorting (`sort_by`)
- Implemented `query(sort_by=field)`: STABLE ascending sort by `field`'s value;
  equal keys keep insertion order. Applied AFTER `where` filtering. Returns copies.
- `sort_by=None` is a no-op — S0/S1 insertion-order behaviour preserved.
- Missing-field policy (D7, mirrors D6): `sort_by` field absent from EVERY record
  raises `KeyError(sort_by)`; a surviving record lacking the key also raises
  `KeyError(sort_by)`.
- Sanity-checked via `python -c`: numeric + string ascending sort, tie-stability,
  `where`+`sort_by` combination, no-arg insertion order, copy-out isolation,
  KeyError on unknown sort field and on a record missing the key, and D6 `where`
  KeyError still intact — all OK.
- SSOT updated: DECISIONS D7, PRODUCT status, this entry.

### S3 — Pagination (`limit`, `offset`)
- Implemented `query(offset=int, limit=int)`: applied LAST, after `where`
  filtering and `sort_by` ordering. `offset` skips leading results (default 0);
  `limit` caps the count (default `None` = no cap). Returns copies.
- Slice-based with clamping (D8): offset past the end -> empty; limit beyond the
  remainder -> the remainder; `limit=0` -> empty. No error on out-of-range.
- Defaults (`offset=0`, `limit=None`) leave results unchanged — S0–S2 preserved.
- Sanity-checked via `python -c`: offset-only, limit-only, offset+limit,
  defaults, offset-past-end, limit>remainder, limit=0, pagination AFTER sort,
  pagination AFTER where (stable), copy-out isolation, and D6 `where` KeyError
  still intact — all OK.
- SSOT updated: DECISIONS D8, PRODUCT status, this entry.

### S4 — Projection (`select`)
- Implemented `query(select=[field, ...])`: each returned row is projected to
  ONLY the selected keys that the row actually has. Applied LAST — after `where`,
  `sort_by`, and pagination.
- Present-keys-only (D9): a selected key a record lacks is silently dropped (not
  an error, not None). `select=[]` -> empty dict per row; `select=None` -> full
  records (S0–S3 preserved). Unlike `where`/`sort_by`, `select` does NOT validate
  field names (a globally-absent field just projects to nothing). Projected key
  order follows the `select` list. Projection doubles as the defensive copy.
- Sanity-checked via `python -c`: basic projection, select key-order, missing-key
  dropped, unknown field -> empty (no KeyError), `select=[]`, `select=None`
  default, copy-out isolation, where+sort+page+select combo, select-after-
  pagination, and regressions (S1/S2 KeyError intact, S3 clamping intact, where
  validation independent of select) — all OK.
- SSOT updated: DECISIONS D9, PRODUCT status, this entry.

### S5 — Change unknown-field handling (`where`)
- CHANGED `where`'s unknown-field policy: a `where` field present in NO stored
  record now yields NO match (`query()` returns `[]`) and MUST NOT raise. This
  reverses the S1/D6 `KeyError` rule. On an empty store, a non-empty `where` now
  returns `[]` too (was: raised).
- Implementation: removed the unknown-field pre-validation loop from the `where`
  branch; the existing match predicate already returns no rows for an absent key,
  so no new code path was needed. (`_known_keys()` is retained — still used by the
  `sort_by` D7 check.)
- SCOPE: only `where` changed. `sort_by`'s `KeyError` on an unknown/absent-on-row
  field (D7) is deliberately LEFT INTACT; `select` still does not validate (D9).
- Sanity-checked via `python -c`: unknown `where` field -> `[]`, unknown+known
  combined -> `[]`, empty store + non-empty `where` -> `[]` (all no-raise);
  regressions — known-field match, record-lacking-a-present-key filtered out,
  where+sort+offset+limit+select composition, `sort_by` unknown-field KeyError
  STILL raised, `sort_by` missing-on-surviving-row KeyError STILL raised, and
  copy-out isolation — all OK.
- SSOT updated: DECISIONS D10 (+ marked D6 superseded), PRODUCT status, this entry.

## Next (future tickets, NOT yet implemented)
- Full pinned signature (where, sort_by, limit, offset, select) is now all
  implemented; no reserved params remain. Future tickets would extend/refine
  behaviour (e.g. richer `where` operators, multi-key/desc sort) — none specified.

## Invariants to preserve
- Single self-contained file; no deps.
- Pinned signatures unchanged (contract v1.0).
- Copy-in / copy-out; default insertion order.
