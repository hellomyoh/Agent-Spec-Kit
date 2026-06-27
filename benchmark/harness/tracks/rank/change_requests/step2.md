# rank library — 2nd revision (R2): change the tie-break policy again

CHANGE the tie-break rule again. Score-descending ordering and API stay the same.

## New tie-break (replaces the 1st-revision rule)
- Equal scores are now broken by **REVERSE alphabetical (Z→A)**.

## Examples
- `rank({"ab":10,"ba":10,"abc":10}) == ["ba","abc","ab"]`   # reverse alphabetical
- `rank({"x":5,"y":9,"z":1}) == ["y","x","z"]`              # distinct scores unaffected

Write the FULL updated `solution.py`.
