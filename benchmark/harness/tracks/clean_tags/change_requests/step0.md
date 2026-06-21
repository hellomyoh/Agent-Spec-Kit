# clean_tags library — Initial development

Build `solution.py` (standard library only).

## Public API
```python
def clean_tags(tags: list) -> list:   # list of strings -> cleaned list of strings
```

## Behavior
- For each tag: strip surrounding whitespace, lowercase.
- Drop empty/whitespace-only tags.
- Remove duplicates, **keeping the FIRST occurrence**.
- **Output order: preserve the input order** (of first occurrences).

## Example
- `clean_tags(["Banana","apple","Fig"," apple ","cc",""]) == ["banana","apple","fig","cc"]`
