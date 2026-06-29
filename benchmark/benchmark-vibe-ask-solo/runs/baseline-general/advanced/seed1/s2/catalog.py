"""In-memory item catalog.

Implements the pinned API contract (see provided/contract.py). Items are dicts,
each with a string 'name'. Methods that return items return copies so callers
cannot mutate the catalog's internal state.

Current behaviour:
- add(item): append an item dict to the catalog.
- all(): return all items as copies, in insertion order.
- search(): filter items by optional text query and field equality, returning copies.
    - query=None (or blank/whitespace-only): list mode, no text filter.
    - non-blank query: case-insensitive substring match on item 'name'.
    - where=None: no equality filter.
    - where={k: v, ...}: keep items whose field k equals v for every key (AND).
      Every where key must be present on every item; otherwise ValueError is raised.
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
        """Return matching items as copies, in insertion order.

        query=None, or a query that is blank/whitespace-only, is list mode:
        no text filter is applied. A non-blank query is a case-insensitive
        substring match against each item's 'name'.

        where=None applies no equality filter. where={k: v, ...} keeps items
        whose field k equals v for every key (AND). Every where key must exist
        on every item in the catalog; if any key is missing from any item,
        ValueError is raised.
        """
        results = self._items

        if where:
            for key in where:
                if any(key not in item for item in self._items):
                    raise ValueError(f"where key {key!r} is missing from some items")
            results = [
                item for item in results
                if all(item[key] == value for key, value in where.items())
            ]

        if query is not None and query.strip():
            needle = query.lower()
            results = [item for item in results if needle in item["name"].lower()]

        return [dict(item) for item in results]
