# clean_tags library — 1st revision (R1): change the output ordering policy

CHANGE the output ordering. All cleaning rules (strip, lowercase, drop-empty, dedup keep-first) stay the same.

## New ordering (replaces input-order)
- The output list is now **sorted ALPHABETICALLY ascending**.

## Example
- `clean_tags(["Banana","apple","Fig"," apple ","cc",""]) == ["apple","banana","cc","fig"]`

Write the FULL updated `solution.py`.
