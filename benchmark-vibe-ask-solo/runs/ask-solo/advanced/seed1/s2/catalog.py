"""Catalog: an in-memory store of item dicts.

Public API is pinned by provided/contract.py (CONTRACT_VERSION 1.0).
Every item is a dict with a string 'name'. Callers never share references with
internal state: items are copied on the way in and on the way out.
"""

import copy


class Catalog:
    def __init__(self):
        self._items = []

    def add(self, item: dict) -> None:
        """Add an item to the catalog."""
        self._items.append(copy.deepcopy(item))

    def all(self) -> list:
        """Return all items as independent copies, in insertion order."""
        return copy.deepcopy(self._items)

    def search(self,
               query: str | None = None,
               where: dict | None = None,
               sort_by: str | None = None,
               limit: int | None = None,
               ) -> list:
        """Return matching items as independent copies, in insertion order.

        query:
            None or blank/whitespace-only -> list mode (every item).
            Otherwise a case-insensitive substring match on each item's 'name'.
        where:
            None -> no equality filter. A dict selects items whose fields equal
            every given key/value pair (multiple keys are combined with AND).
            Every key must be present on every item in the catalog; a key missing
            from any item raises ValueError.
        sort_by, limit:
            Not specified yet; passing either raises NotImplementedError.
        """
        if sort_by is not None or limit is not None:
            raise NotImplementedError(
                "search sort_by/limit is not available yet; "
                "only query text filtering, where equality filtering, and the "
                "no-argument list mode are supported"
            )

        if where is not None:
            for key in where:
                if any(key not in item for item in self._items):
                    raise ValueError(
                        f"where key {key!r} is not present on every item"
                    )

        results = self._items
        if query is not None and query.strip():
            needle = query.casefold()
            results = [item for item in results if needle in item["name"].casefold()]

        if where is not None:
            results = [
                item for item in results
                if all(item[key] == value for key, value in where.items())
            ]

        return copy.deepcopy(results)
