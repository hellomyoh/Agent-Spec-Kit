# HISTORY — rank Library

## [2026-06-21] v1.0.0 — Initial Implementation

**Decision**: Implemented `rank(scores: dict) -> list` with stable two-key sorting:
1. Primary: Score in descending order (highest to lowest)
2. Tie-break: Name alphabetically (A→Z, ascending)

**Key Implementation Details**:
- Uses Python's built-in `sorted()` with a custom sort key
- Sort key: tuple of `(-score, name)` for reverse score and forward name order
- Handles empty input naturally (returns empty list)
- All names from input appear exactly once in output

**Rationale**:
- Two-key tuple sort is Pythonic and efficient (O(n log n))
- Negative score for descending order avoids reverse parameter complexity
- Alphabetical tie-break matches common ranking conventions
- No external dependencies required (standard library only)

## [2026-06-21] v1.1.0 — Tie-break Policy Revision (R1)

**Change**: Modified tie-break rule for equal scores.

**Previous Behavior**: When scores were equal, names were ordered alphabetically (A→Z).

**New Behavior**: When scores are equal, names are now ordered by:
1. Length ascending (shorter names first)
2. Alphabetical ascending (within same length)

**Examples of Changed Behavior**:
- `rank({"ab":10,"ba":10,"abc":10})` previously returned `["ab","abc","ba"]` (pure alphabetical)
- Now returns `["ab","ba","abc"]` (length 2 first alphabetically, then length 3)

**Key Implementation Details**:
- Sort key updated to: `(-score, len(name), name)`
- Three-level tuple sort: score (descending), length (ascending), name (ascending)
- Maintains O(n log n) efficiency and standard library only approach
- Empty input and single names still handled naturally

**Rationale**:
- Length-based tie-break may reflect domain requirements where name brevity is valued
- Preserves secondary alphabetical order for consistency and predictability within length groups

## [2026-06-21] v1.2.0 — Tie-break Policy Revision (R2)

**Change**: Modified tie-break rule for equal scores again.

**Previous Behavior**: When scores were equal, names were ordered by length (ascending) then alphabetically (A→Z).

**New Behavior**: When scores are equal, names are now ordered by reverse alphabetical order (Z→A).

**Examples of Changed Behavior**:
- `rank({"ab":10,"ba":10,"abc":10})` previously returned `["ab","ba","abc"]` (length-based with alphabetical within length)
- Now returns `["ba","abc","ab"]` (pure reverse alphabetical)

**Key Implementation Details**:
- Sort key simplified to: `(-score, name)` with reverse=False on sorted()
- Two-level tuple sort: score (descending), name (reverse alphabetical)
- Returns to O(n log n) efficiency with standard library only
- Empty input and single names still handled naturally

**Rationale**:
- Reverse alphabetical tie-break provides simpler, more direct ordering when scores are equal
- Removes complexity of length-based sorting in favor of pure reverse alphabetical consistency
