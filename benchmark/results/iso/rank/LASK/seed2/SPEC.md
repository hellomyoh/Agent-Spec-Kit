# rank library — API Specification

## Public API

```python
def rank(scores: dict) -> list:
```

Maps a dictionary of names to scores into an ordered list of names.

## Behavior

- **Input**: A dictionary where keys are names (strings) and values are scores (integers).
- **Output**: A list of names (strings) ordered by score in descending order.
- **Tie-breaking**: When scores are equal, names are ordered by reverse alphabetical descending (Z→A).
- **Coverage**: Every name appears exactly once in the output.
- **Edge case**: Empty dictionary returns empty list.

## Examples

| Input | Output | Reason |
|-------|--------|--------|
| `{"x":5,"y":9,"z":1}` | `["y","x","z"]` | Ordered by score: 9 > 5 > 1 |
| `{"ab":10,"ba":10,"abc":10}` | `["ba","abc","ab"]` | All tied at 10; reverse alphabetical: "ba" > "abc" > "ab" |
| `{}` | `[]` | Empty input |
