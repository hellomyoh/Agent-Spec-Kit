# rank Library — Specification

## Public API

```python
def rank(scores: dict) -> list:
    """
    Rank names by score.
    
    Args:
        scores: Dictionary mapping name (str) to score (int)
    
    Returns:
        List of names sorted by score (descending), then by name (reverse alphabetical, Z→A)
    """
```

## Behavior

- **Primary sort**: Score in descending order (highest first)
- **Tie-break**: When scores are equal, order by name in reverse alphabetical order (Z→A)
- **Completeness**: Every name in the input appears exactly once in the output
- **Empty input**: Returns empty list

## Examples

- `rank({"x":5,"y":9,"z":1})` returns `["y","x","z"]` (by score: 9, 5, 1)
- `rank({"ab":10,"ba":10,"abc":10})` returns `["ba","abc","ab"]` (all tied at 10, reverse alphabetical: ba, abc, ab)
- `rank({})` returns `[]`

## Edge Cases

- Single name: Returns list with that name
- All equal scores: Reverse alphabetical order
- Negative scores: Treated as regular integers, sorted descending
