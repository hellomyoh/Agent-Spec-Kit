"""A simple in-memory catalog of item dicts.

Each item is a dict with a string 'name'. The catalog stores items in
insertion order and hands back copies so callers cannot mutate internal state.
"""


class Catalog:
    def __init__(self) -> None:
        self._items: list[dict] = []

    def add(self, item: dict) -> None:
        """Append an item to the catalog."""
        self._items.append(item)

    def all(self) -> list[dict]:
        """Return all items, in insertion order, as copies."""
        return [dict(item) for item in self._items]

    def search(
        self,
        query: str | None = None,
        where: dict | None = None,
        sort_by: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Return matching items as copies.

        With no arguments, returns all items in insertion order.
        """
        return [dict(item) for item in self._items]
