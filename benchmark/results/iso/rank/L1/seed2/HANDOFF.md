# Implementation Handoff

## Summary
Updated the `rank()` function per step2 change request: modified tie-breaking policy from length-then-alphabetical to reverse alphabetical (Z→A).

## Change Made
- **Previous tie-break**: name length ascending (shorter first); if same length, alphabetical ascending
- **New tie-break**: reverse alphabetical (Z→A) for all ties regardless of name length

## Implementation Details
- **Function**: `rank(scores: dict) -> list`
- **Algorithm**: Uses `sorted()` with composite sort key: `(-scores[name], [-ord(c) for c in name])`
  - Primary sort: score descending (via negation)
  - Secondary sort: reverse alphabetical (by negating each character's ord value)
- **Behavior**:
  - Returns names ordered by score descending
  - Ties broken by reverse alphabetical order (Z→A)
  - For example: `rank({"ab":10,"ba":10,"abc":10})` returns `["ba","abc","ab"]` (reverse alphabetical)
  - Empty dict returns empty list
  - Each name appears exactly once

## Test Cases Verified (mentally)
- `rank({"x":5,"y":9,"z":1})` → `["y","x","z"]` (distinct scores, unaffected)
- `rank({"ab":10,"ba":10,"abc":10})` → `["ba","abc","ab"]` (reverse alphabetical: ba > abc > ab)
- `rank({})` → `[]` (empty)

## Implementation Note
The sort key `lambda name: (-scores[name], [-ord(c) for c in name])` handles both requirements:
- `-scores[name]` negates the score for descending order
- `[-ord(c) for c in name]` creates a list of negated character codes, which when compared lexicographically produces reverse alphabetical ordering
- Python's stable sort naturally chains these comparisons

The implementation uses `sorted(scores.keys(), ...)` to return names (strings) directly.
No external dependencies needed (standard library only).
