# NOTES

(optional free-form notes; not an authority doc)

- `search(where={k: v})`: equality filter, multiple keys AND-ed together.
- Policy: every `where` key must exist on every catalog item, else `ValueError`.
  (Empty catalog: vacuously valid -> no error, empty result.)
- `where` is applied before the `query` substring filter so they compose.
