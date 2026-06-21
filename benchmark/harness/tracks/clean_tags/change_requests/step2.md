# clean_tags library — 2nd revision (R2): change the output ordering again

CHANGE the output ordering again. All cleaning rules stay the same.

## New ordering (replaces the 1st-revision ordering)
- The output is now **sorted by LENGTH ascending (shortest first); ties by alphabetical ascending**.

## Example
- `clean_tags(["Banana","apple","Fig"," apple ","cc",""]) == ["cc","fig","apple","banana"]`

Write the FULL updated `solution.py`.
