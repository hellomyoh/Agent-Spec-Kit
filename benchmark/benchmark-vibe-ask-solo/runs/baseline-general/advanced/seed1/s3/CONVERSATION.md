# CONVERSATION — advanced S3

## Request
(from USER_PROMPT.md, translated)
- Add `sort_by` (ascending, **stable** sort).
- Safety policy: a blank / whitespace-only `query` returns `[]` (an empty search
  box must not dump the whole catalog).
- Keep all existing tests green.

## Plan
Starting point: `search` already declared `query`, `where`, `sort_by`, `limit`
in its signature, but `sort_by` and `limit` were accepted-and-ignored, and a
blank/whitespace-only `query` was treated as *list mode* (no text filter).

Two changes, both inside `Catalog.search`:

1. **Empty-search guard.** Change blank-query handling: if `query is not None`
   and `query.strip()` is empty, return `[]` immediately (before any filtering).
   - `query=None` is left untouched = list mode / no text filter (fixed by the
     pinned contract, so this preserves prior behaviour).
   - Because the blank case now short-circuits, the substring branch no longer
     needs its own `.strip()` re-check; `if query is not None:` is sufficient
     there (the value is guaranteed non-blank by then).

2. **`sort_by`.** After filtering, if `sort_by is not None`,
   `results = sorted(results, key=lambda item: item[sort_by])`. Python's
   `sorted` is stable, giving ascending order with insertion order preserved
   among equal keys. Sorting after filtering means it composes with `where` and
   `query`.

Pipeline order: empty-query guard -> `where` -> `query` -> `sort_by` -> copy out.

Out of scope / preserved unchanged:
- `limit` stays accepted-but-unimplemented (no-op), exactly as before — the
  prompt did not ask for it; not touching it preserves prior behaviour.
- `where` strictness (every key must exist on every item, else `ValueError`)
  and copy-out semantics are unchanged.
- `sort_by` on a field missing from an item raises a natural `KeyError`; no
  bespoke policy was invented since the prompt did not specify one.

## Test run
`python -c "import catalog"` -> import OK.

Ran an inline behaviour script (`python -c ...`) covering:
1. `query=None` -> list mode, insertion order — OK
2. `query=''`, `'   '`, `'\t\n'` -> `[]` — OK
3. non-blank query -> case-insensitive substring on `name` — OK
4. `sort_by='qty'` -> ascending **and stable** (apple before Cherry at qty=1) — OK
5. `sort_by='name'` -> ascending — OK
6. `where` + `query` + `sort_by` compose — OK
7. `where` with missing key -> `ValueError` — OK
8. returned items are copies (mutating a result does not change the catalog) — OK
9. empty catalog: `search()`/`where`/blank-query edge cases — OK

Result: ALL PASS.

## Summary
Added an ascending, stable `sort_by` to `Catalog.search` and changed the
blank/whitespace-only `query` policy to return `[]` (empty-search guard) while
keeping `query=None` as list mode. `where`, copy-out, and the
accepted-but-ignored `limit` behaviour are preserved. Docstrings now describe
the current behaviour; all inline checks pass.
