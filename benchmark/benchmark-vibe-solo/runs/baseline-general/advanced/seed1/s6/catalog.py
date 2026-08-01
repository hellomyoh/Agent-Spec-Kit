"""In-memory item catalog.

Implements the pinned API contract (see provided/contract.py). Items are dicts,
each with a string 'name'. Methods that return items return copies so callers
cannot mutate the catalog's internal state.

Current behaviour:
- add(item): append an item dict to the catalog.
- all(): return all items as copies, in insertion order.
- search(): filter items by optional text query and field equality, optionally
  ordered by a field and capped to a maximum count, returning copies.
    - query=None: list mode, no text filter (per contract).
    - query is blank/whitespace-only: also no text filter, so it returns every
      item (subject to where/sort/limit). This is the list-view behaviour: an
      empty search box shows the whole catalog.
    - non-blank query: case-insensitive substring match on item 'name'.
    - where=None: no equality filter.
    - where={k: v, ...}: keep items whose field k equals v for every key (AND).
      An item missing a where key simply does not match (it is filtered out); a
      missing key is never an error, so a where key absent from every item just
      yields [].
    - sort_by=None: results stay in insertion order.
    - sort_by=field: stable ascending sort by that field, applied after filtering.
    - limit=None: no cap; all matching items are returned.
    - limit=N (N >= 0): return at most the first N items, applied last (after
      sorting), so it caps to the top N. limit=0 returns []. A negative limit is
      invalid and raises ValueError.
"""


class Catalog:
    def __init__(self) -> None:
        self._items: list[dict] = []

    def add(self, item: dict) -> None:
        """Add an item dict to the catalog."""
        self._items.append(item)

    def all(self) -> list[dict]:
        """Return all items as copies, in insertion order."""
        return [dict(item) for item in self._items]

    def search(self,
               query: str | None = None,
               where: dict | None = None,
               sort_by: str | None = None,
               limit: int | None = None,
               ) -> list[dict]:
        """Return matching items as copies.

        query=None is list mode: no text filter is applied (per contract). A
        query that is blank or whitespace-only is treated the same way (no text
        filter), so it returns every item subject to where/sort/limit -- the
        list-view behaviour where an empty search box shows the whole catalog.
        A non-blank query is a case-insensitive substring match against each
        item's 'name'.

        where=None applies no equality filter. where={k: v, ...} keeps items
        whose field k equals v for every key (AND). An item that is missing a
        where key does not match and is filtered out; a missing key is never an
        error, so a where key that is absent from every item yields [].

        sort_by=None leaves results in insertion order. sort_by=field returns
        results sorted by that field in ascending order; the sort is stable, so
        items that compare equal keep their insertion order. Sorting is applied
        after filtering.

        limit=None returns every matching item. limit=N (N >= 0) caps the result
        to the first N items, applied last (after sorting), yielding the top N;
        limit=0 returns []. A negative limit raises ValueError.
        """
        if limit is not None and limit < 0:
            raise ValueError(f"limit must be non-negative, got {limit!r}")

        results = self._items

        if where:
            results = [
                item for item in results
                if all(key in item and item[key] == value
                       for key, value in where.items())
            ]

        if query is not None and query.strip():
            needle = query.lower()
            results = [item for item in results if needle in item["name"].lower()]

        if sort_by is not None:
            results = sorted(results, key=lambda item: item[sort_by])

        if limit is not None:
            results = results[:limit]

        return [dict(item) for item in results]
