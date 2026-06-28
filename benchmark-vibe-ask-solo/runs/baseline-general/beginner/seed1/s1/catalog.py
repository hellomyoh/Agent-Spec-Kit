"""A small in-memory catalog: add items, list them, and search by name."""


class Catalog:
    """Holds a list of item dicts. Each item has a string 'name'."""

    def __init__(self) -> None:
        self._items: list[dict] = []

    def add(self, item: dict) -> None:
        """Add an item to the catalog."""
        self._items.append(dict(item))

    def all(self) -> list[dict]:
        """Return every item, in insertion order, as copies."""
        return [dict(item) for item in self._items]

    def search(
        self,
        query: str | None = None,
        where: dict | None = None,
        sort_by: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Return items, optionally filtered, sorted, and limited.

        query=None lists items. A non-None query keeps items whose 'name'
        contains the query text as a substring, matched case-insensitively
        (e.g. 'ap' matches 'Apple'). where keeps items whose fields all equal
        the given values. sort_by orders by a field. limit caps the number of
        results.
        """
        results = self._items

        if query is not None:
            needle = query.lower()
            results = [it for it in results if needle in str(it.get("name", "")).lower()]

        if where:
            results = [
                it for it in results
                if all(it.get(field) == value for field, value in where.items())
            ]

        if sort_by is not None:
            results = sorted(results, key=lambda it: it.get(sort_by))

        if limit is not None:
            results = results[:limit]

        return [dict(it) for it in results]
