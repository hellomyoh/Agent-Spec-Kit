"""In-memory item catalog.

Implements the pinned API contract (see provided/contract.py). Items are dicts,
each with a string 'name'. Methods that return items return copies so callers
cannot mutate the catalog's internal state.

Current behaviour:
- add(item): append an item dict to the catalog.
- all(): return all items as copies, in insertion order.
- search(): filter items by an optional text query, returning copies.
    - query=None (or blank/whitespace-only): list mode, no text filter.
    - non-blank query: case-insensitive substring match on item 'name'.
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
        """
        results = self._items

        if query is not None and query.strip():
            needle = query.lower()
            results = [item for item in results if needle in item["name"].lower()]

        return [dict(item) for item in results]
