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
        """Return matching items as independent copies.

        With no arguments, return every item (copies), in insertion order.
        """
        if query is not None or where is not None or sort_by is not None or limit is not None:
            raise NotImplementedError(
                "search filtering/sorting/limiting is not available yet; "
                "only the no-argument list mode is supported"
            )
        return copy.deepcopy(self._items)
