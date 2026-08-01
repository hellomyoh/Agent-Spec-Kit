# PRODUCT

`miniquery` is a small in-memory record store (the `Store` class in `miniquery.py`)
with a pinned public API defined in `provided/contract.py` (CONTRACT_VERSION 2.0).

## Purpose
Store dict records and retrieve them. Over successive sessions the `query()` method
gains filtering (`where`), sorting (`sort_by`), and paging (`limit`, `offset`)
behaviour. Signatures are FIXED by the contract; only behaviour evolves per ticket.

## Public API (pinned)
- `Store.add(record: dict) -> None` — store a copy of the record.
- `Store.all() -> list[dict]` — return copies of all records, insertion order.
- `Store.query(where=None, sort_by=None, limit=None, offset=0) -> list[dict]`
  — retrieval with optional equality filter, ascending sort (ties keep insertion
  order), and paging. An omitted `limit` is governed by the current default page
  size set by tickets.

## Invariants
- The store never returns references to its internal state; callers receive copies
  and cannot mutate stored records.

## Implemented so far
- S0: scaffold — `add`, `all`, and no-argument `query` (returns all records).
- S1: paging — `offset`/`limit` with a default page size for omitted `limit`.
- S2: `where` — conjunctive equality filter, applied before paging.
- S3: default page size set to `DEFAULT_PAGE_SIZE = 25` (was 7).
