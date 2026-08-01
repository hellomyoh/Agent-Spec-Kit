# CONVERSATION — S1 (seed1, throughline-solo)

## Request
User (Korean): "이제 이름으로 검색되게 해줘. 'ap' 치면 apple 나오게. 대소문자는 너무 따지지 말고."
Translation: make items searchable by name; typing `ap` should return `apple`;
don't be too strict about case.

Interpretation: implement the `query` text filter on `name` as a
case-insensitive substring match.

## Conflict check vs recorded decisions
- D1 (S0, "keep it simple", defer query/where/sort/limit) and D2 (S0, `search`
  list-mode only): the user is now explicitly directing the `query` behaviour
  that PROGRESS already listed under "Next". This is the anticipated intentional
  evolution, not forgetting/drift that breaks a policy. Resolution: SUPERSEDE
  D1/D2 for the `query` part only (recorded as D5) and implement.
- D3 (return/store copies, no state leakage): PRESERVED — `search` still returns
  fresh dict copies.
- D4 (in-memory, no persistence): unaffected.
- `where`/`sort_by`/`limit`: NOT requested this session; remain deferred.
No policy-breaking conflict requiring "needs user confirmation".

## Plan
1. Implement `search(query=...)` as case-insensitive (`casefold`) substring
   match on `name`; keep `query=None` as list mode; keep copy-safety.
2. Leave `where`/`sort_by`/`limit` inert.
3. Update SSOT (FEATURES, DECISIONS D5/D6, PROGRESS); write this file.
4. Verify via `python -c "import catalog"` + behaviour checks.

## SSOT updates
- FEATURES.md: rewrote the Search section to describe active `query` semantics.
- DECISIONS.md: added D5 (supersedes D1, D2 for `query`) and D6 (semantics:
  case-insensitive substring; empty query matches all; missing `name` -> '').
- PROGRESS.md: added S1 entry; trimmed the `query` item from Next.

## Test run
`python -c "import catalog"` plus checks:
- 'ap' / 'AP' match Apple, apricot, apple (substring + case-insensitive)
- list mode (`search()`), `all()` unchanged
- empty query matches all; 'zzz' matches none
- mutating a result does not change internal state (D3)
- item without `name` does not crash search
Result: ALL CHECKS PASS.

## Summary
Added case-insensitive substring name search via `search(query=...)`, the
deferred behaviour the user requested. Superseded D1/D2 for `query` only;
preserved copy-safety (D3) and list mode. `where`/`sort_by`/`limit` still
deferred.
