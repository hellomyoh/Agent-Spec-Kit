# NOTES — for future self

## Implemented so far
- S0: add(record) deep-copies in; all() returns deep copies; query() no-arg -> all.
- S1: query(where={k:v,...}) -> records matching ALL key==value pairs.
- S2: query(sort_by=field) -> ASCENDING, STABLE sort (ties keep insertion order).
- S3: query(limit, offset) -> pagination, applied AFTER sort.
- S4: query(select=[...]) -> project each result to ONLY listed keys PRESENT on
  that record (absent keys silently omitted, not errors).
- S5: unknown `where` field -> silent NO-MATCH (returns []), NOT an error.
- S6: REVERT S5. Restored pre-S5 (S1) behaviour: unknown `where` field -> KeyError.

## Key decisions / invariants
- `copy.deepcopy` on add AND read so callers can never mutate internal state
  (records may hold nested dicts/lists). EVERY return path must yield fresh dicts.
- Records in private list `self._records`; insertion order = source of truth.

## WHERE policy (CURRENT = S6, which REVERTED S5 back to S1 semantics)
- "Unknown field" = a `where` key present in NO stored record.
- S6 (CURRENT/ACTIVE): unknown field -> raise KeyError(key). HARD ERROR.
  Implementation: build known_fields = union of all record keys; for each
  where key, `if k not in known_fields: raise KeyError(k)`. Validation runs
  BEFORE filtering, only when `where` is truthy.
- A record that merely LACKS a KNOWN key fails equality -> excluded (non-match,
  NOT an error). Per-record predicate stays `all(k in r and r[k]==v ...)`.
- S5 (NOW REVERTED, do NOT re-apply unless a ticket asks): had NO validation;
  silent no-match -> []. If a future ticket says "revert S6" / "restore S5",
  just delete the known_fields validation block again.
- Empty/None where = no filter (`if where:` guard). Matching is ALL pairs (AND), `==`.
- EDGE: empty store + non-empty where -> known_fields is empty -> any where key
  is "unknown" -> KeyError. (Consistent: the field is present in no record.)

## SORT policy (S2 — DECIDED)
- `if sort_by is not None:` guard (so "" still sorts). Ascending only; builtin
  `sorted` gives stability. Key = `r[sort_by]`.
- OPEN: missing sort_by key -> KeyError; uncomparable -> TypeError. Not forced.

## PAGINATION policy (S3 — DECIDED)
- Combined order LOCKED: where -> sort_by -> offset/limit -> select.
- One slice: `stop = None if limit is None else offset+limit; records[offset:stop]`.
  limit=0 => empty (only None = no cap); offset past end => []; limit beyond => clamps.
- offset default 0, limit default None.
- OPEN: negative limit/offset — raw Python slice semantics, NOT validated.

## SELECT policy (S4 — DECIDED)
- `if select is not None:` guard (so select=[] -> every result becomes `{}`).
- Projection is the LAST step. Keep ONLY keys present: `{k: r[k] for k in select if k in r}`.
  Absent selected key SILENTLY OMITTED (NOT KeyError — differs from where-policy).
- This path deep-copies each kept VALUE and returns directly (skips trailing deepcopy).
- OPEN: duplicate field in select harmless (dict dedups).

(Maintain a free-form NOTES.md; carried notes are capped to ~2600 chars.)
