"""In-memory item catalog.

Implements the pinned API contract (see provided/contract.py). Items are dicts,
each with a string 'name'. Methods that return items return copies so callers
cannot mutate the catalog's internal state.

Current behaviour:
- add(item): append an item dict to the catalog.
- all(): return all items as copies, in insertion order.
- search(): with no arguments, returns all items as copies (list mode).
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

        With no arguments (query=None), this is list mode: it returns all items
        as copies, in insertion order.
        """
        return self.all()
