"""A small in-memory catalog: add items, list them, and search by name.

Implements the pinned API contract (provided/contract.py). This session adds
case-insensitive substring search on an item's 'name' via `search(query=...)`.
The `where`, `sort_by`, and `limit` arguments are part of the fixed contract but
are not active yet.
"""


class Catalog:
    """Holds a list of item dicts. Each item has a string 'name'."""

    def __init__(self) -> None:
        self._items: list[dict] = []

    def add(self, item: dict) -> None:
        """Add one item to the catalog."""
        self._items.append(dict(item))

    def all(self) -> list[dict]:
        """Return every item, in insertion order (copies)."""
        return [dict(item) for item in self._items]

    def search(
        self,
        query: str | None = None,
        where: dict | None = None,
        sort_by: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Return items, optionally filtered by a name text search.

        With `query=None` this lists everything (list mode). With a non-None
        `query`, items are kept when the query appears anywhere in their 'name',
        compared case-insensitively (so 'ap' matches 'Apple'). An empty query
        matches every item.

        `where`, `sort_by`, and `limit` are part of the fixed contract but are
        not active yet.
        """
        items = self._items
        if query is not None:
            needle = query.casefold()
            items = [
                item
                for item in items
                if needle in str(item.get("name", "")).casefold()
            ]
        return [dict(item) for item in items]
