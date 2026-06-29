# S6 — Revert S5

Reverted S5's unknown-field handling in `where`; restored the pre-S5 (S1) policy.

Decisions:
- Re-added the hard unknown-field check before filtering: any `where` key
  present in NO stored record now raises `KeyError(key)` again (S5 had made it
  return [] silently).
- Filter logic itself unchanged: a record lacking a (known) key is still a
  non-match; `where=None`/`{}` still returns all.
- S2 sort / S3 paginate / S4 select policies untouched.
