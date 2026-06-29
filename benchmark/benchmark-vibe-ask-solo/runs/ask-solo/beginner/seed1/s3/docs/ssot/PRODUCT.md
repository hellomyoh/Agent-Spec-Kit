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
- S2: `search(where=...)` — field equality filter (e.g. `category`); filtering on
  an unknown field raises instead of silently matching nothing.
- S3: `search(sort_by=...)` — stable ordering by a field (equal values keep
  insertion order). Empty/blank search now shows nothing (no criterion -> `[]`);
  use `all()` to view the full list.
