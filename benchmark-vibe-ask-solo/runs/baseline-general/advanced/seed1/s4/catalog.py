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
    - query is blank/whitespace-only: returns [] (empty-search guard, so an
      empty search box does not dump the whole catalog).
    - non-blank query: case-insensitive substring match on item 'name'.
    - where=None: no equality filter.
    - where={k: v, ...}: keep items whose field k equals v for every key (AND).
      Every where key must be present on every item; otherwise ValueError is raised.
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
        query that is blank or whitespace-only returns [] (empty-search guard:
        an empty search box must not return the whole catalog). A non-blank
        query is a case-insensitive substring match against each item's 'name'.

        where=None applies no equality filter. where={k: v, ...} keeps items
        whose field k equals v for every key (AND). Every where key must exist
        on every item in the catalog; if any key is missing from any item,
        ValueError is raised.

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

        if query is not None and not query.strip():
            return []

        results = self._items

        if where:
            for key in where:
                if any(key not in item for item in self._items):
                    raise ValueError(f"where key {key!r} is missing from some items")
            results = [
                item for item in results
                if all(item[key] == value for key, value in where.items())
            ]

        if query is not None:
            needle = query.lower()
            results = [item for item in results if needle in item["name"].lower()]

        if sort_by is not None:
            results = sorted(results, key=lambda item: item[sort_by])

        if limit is not None:
            results = results[:limit]

        return [dict(item) for item in results]
