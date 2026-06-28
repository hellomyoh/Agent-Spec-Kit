# miniquery — notes to future self

## Implemented so far
- S0: add(record) deep-copies in; all() returns deep copies; query() no-arg -> all.
- S1: query(where={k:v,...}) -> records matching ALL key==value pairs.
- S2: query(sort_by=field) -> ASCENDING, STABLE sort (ties keep insertion order).
- S3: query(limit, offset) -> pagination, applied AFTER sort.
- S4: query(select=[...]) -> project each result to ONLY listed keys PRESENT on
  that record (absent keys silently omitted, not errors).
- S5: unknown `where` field -> NO match (returns []), NOT an error. DONE.

## Key decisions / invariants
- `copy.deepcopy` on add AND read so callers can never mutate internal state
  (records may hold nested dicts/lists). EVERY return path must yield fresh dicts.
- Records in private list `self._records`; insertion order = source of truth.

## WHERE policy (S5 SUPERSEDES S1 — DECIDED, applies to ALL future where handling)
- Unknown field (key in NO stored record) = SILENT NO-MATCH -> query returns [].
  MUST NOT raise. (S1's old "hard KeyError on unknown field" is REVERSED — do
  not re-add validation.)
- Implementation: NO validation step. The predicate
  `all(k in r and r[k] == v ...)` already excludes any record lacking the key,
  so if the key is absent everywhere, all records fail -> []. Clean & correct.
- A record that merely LACKS a present key also fails equality (excluded).
- Empty/None where = no filter (`if where:` guard). Matching is ALL pairs (AND), `==`.

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
  Absent selected key SILENTLY OMITTED (NOT KeyError — differs from old where-policy).
- This path deep-copies each kept VALUE and returns directly (skips trailing deepcopy).
- OPEN: duplicate field in select harmless (dict dedups).

(Maintain a free-form NOTES.md; carried notes are capped to ~2600 chars.)
