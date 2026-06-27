# rank library — 1st revision (R1): change the tie-break policy

CHANGE the tie-break rule. Everything else (score-descending ordering, API) stays the same.

## New tie-break (replaces the previous one)
- Equal scores are now broken by **name LENGTH ascending (shorter first); if same length, alphabetical ascending.**

## Examples
- `rank({"ab":10,"ba":10,"abc":10}) == ["ab","ba","abc"]`   # len2 (ab,ba), then len3 (abc)
- `rank({"x":5,"y":9,"z":1}) == ["y","x","z"]`              # distinct scores unaffected

Write the FULL updated `solution.py`.
