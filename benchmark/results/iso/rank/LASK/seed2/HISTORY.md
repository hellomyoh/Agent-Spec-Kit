# HISTORY

## v0.1.0 — Initial Implementation

**Date**: 2026-06-21
**Seed**: seed2

### Key Behavioral Decisions

1. **Primary Sort Key**: Score in descending order (highest first)
2. **Tie-Break Rule**: When two names have equal scores, sort alphabetically ascending (A→Z)
3. **Return Type**: List of name strings only (not tuples or objects)
4. **Completeness**: Every input name appears exactly once in output
5. **Empty Input**: Returns empty list for empty dictionary

### Implementation Approach

- Use Python's `sorted()` built-in with a stable sorting algorithm
- Apply a two-level sort key: `(-score, name)` to achieve descending score with alphabetical tie-break
- This leverages tuple comparison: tuples compare element-by-element left-to-right

### Rationale

The two-level sort key approach is simple, readable, and leverages Python's built-in sorting efficiency without external dependencies. The negation of score achieves descending order naturally within ascending tuple comparison logic.

## v0.2.0 — Revised Tie-Break Policy (R1)

**Date**: 2026-06-21
**Change**: Replaced alphabetical-only tie-break with length-first then alphabetical tie-break

### What Changed

**Prior behavior** (v0.1.0): When scores are equal, names were sorted alphabetically (A→Z).
- Example: `rank({"ab":10,"ba":10,"abc":10})` returned `["ab","abc","ba"]`

**New behavior** (v0.2.0): When scores are equal, names are sorted by length ascending (shorter first); if same length, then alphabetically ascending.
- Example: `rank({"ab":10,"ba":10,"abc":10})` now returns `["ab","ba","abc"]`

### Implementation Approach

- Updated sort key from `(-score, name)` to `(-score, len(name), name)`
- This adds a second tie-break level: length comparison before alphabetical comparison
- Tuple comparison chains these naturally: first score (descending), then length (ascending), then alphabetical (ascending)

### Rationale

The three-level sort key maintains simplicity and readability while accommodating the new tie-break policy. Standard library `sorted()` continues to handle all logic efficiently.

## v0.3.0 — Second Revision Tie-Break Policy (R2)

**Date**: 2026-06-21
**Change**: Replaced length-first then alphabetical tie-break with reverse alphabetical tie-break

### What Changed

**Prior behavior** (v0.2.0): When scores are equal, names were sorted by length ascending (shorter first); if same length, then alphabetically ascending.
- Example: `rank({"ab":10,"ba":10,"abc":10})` returned `["ab","ba","abc"]`

**New behavior** (v0.3.0): When scores are equal, names are sorted in reverse alphabetical order (Z→A).
- Example: `rank({"ab":10,"ba":10,"abc":10})` now returns `["ba","abc","ab"]`

### Implementation Approach

- Updated sort key from `(-score, len(name), name)` to `(-score, name)` with `reverse=True` parameter
- Using `reverse=True` on the entire sort inverts the secondary comparisons while maintaining descending score order through negation
- This naturally produces reverse alphabetical ordering for the tie-break without explicit string reversal

### Rationale

The `reverse=True` approach is simpler than the previous three-level key and more directly expresses the intent: primary descending score order with secondary reverse alphabetical order. The negated score combined with reverse flag produces the correct behavior across all cases.
