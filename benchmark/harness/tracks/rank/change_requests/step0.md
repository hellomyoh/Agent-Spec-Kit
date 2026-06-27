# rank library — Initial development

Build `solution.py` (standard library only).

## Public API
```python
def rank(scores: dict) -> list:   # dict {name: score(int)} -> list of names
```

## Behavior
- Return the names ordered by **score descending**.
- **Tie-break (equal scores): alphabetical ascending (A→Z).**
- Every name appears exactly once; empty dict → empty list.

## Examples
- `rank({"x":5,"y":9,"z":1}) == ["y","x","z"]`
- `rank({"ab":10,"ba":10,"abc":10}) == ["ab","abc","ba"]`   # tie -> alphabetical
