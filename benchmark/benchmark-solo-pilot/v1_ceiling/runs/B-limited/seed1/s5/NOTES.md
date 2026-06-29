# S5 — Unknown-field in `where` => no match (was KeyError)

CHANGED S1 policy: a `where` field absent from EVERY record now yields `[]`,
no raise.

Decisions:
- Removed the explicit unknown-field check loop that raised KeyError(key).
- No new code needed: the existing match `all(k in r and r[k] == v ...)`
  already drops records lacking the key, so a field present nowhere matches
  nothing => []. Records that have the key on some rows still filter normally.
- S2 sort / S3 paginate / S4 select policies preserved unchanged.
- `where=None` or `{}` still returns all (falsy guard untouched).
