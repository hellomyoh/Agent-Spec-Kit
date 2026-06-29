# PRODUCT

A small, in-memory catalog library (`catalog.py`).

## Purpose
Let a user keep a simple list of items and view them. Items are plain dicts;
every item has a string `name`. Kept deliberately simple.

## Public surface (pinned by provided/contract.py, FIXED across sessions)
- `Catalog.add(item: dict) -> None`
- `Catalog.all() -> list[dict]`
- `Catalog.search(query=None, where=None, sort_by=None, limit=None) -> list[dict]`

Signatures never change; behaviour evolves per session as the user directs.

## Scope so far
- S0: add items, view the full list. (`search` exposed but list-mode only.)
- S1: `search(query=...)` — case-insensitive substring match on `name`.
- S2: `search(where=...)` — field equality filter (e.g. `category`). (S2 made
  filtering on an unknown field raise; S5 reversed that — see below.)
- S3: `search(sort_by=...)` — stable ordering by a field (equal values keep
  insertion order). (S3 also made empty/blank search show nothing; S6 reversed
  that — see below.)
- S4: `search(limit=...)` — cap to the top N results (applied after filter/sort);
  `limit=None` = no cap, `limit=0` = none; bad limit (negative / non-int) raises.
- S5: `where` on an unknown field is now forgiving — it returns `[]` instead of
  raising (reverses S2's raise). `sort_by` on an unknown field still raises.
- S6: empty/blank search now shows the whole catalog again (an ordinary list),
  reversing S3's "show nothing"; a criterion-less `search()` mirrors `all()`. Any
  real criterion (`where` / non-blank `query`) still narrows it.
