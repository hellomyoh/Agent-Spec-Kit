"""A small in-memory catalog: add items, list them, search, filter, and sort."""


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
        (e.g. 'ap' matches 'Apple').

        where keeps items whose fields all equal the given values, so any
        field can be filtered (e.g. {'category': 'fruit'}). Filtering on a
        field that no item has raises KeyError, since that is a mistake rather
        than an empty result.

        sort_by orders by a field. limit caps the number of results.
        """
        results = self._items

        if query is not None:
            needle = query.lower()
            results = [it for it in results if needle in str(it.get("name", "")).lower()]

        if where:
            known_fields = {field for it in self._items for field in it}
            unknown = [field for field in where if field not in known_fields]
            if unknown:
                raise KeyError(
                    f"Cannot filter on unknown field(s): {', '.join(sorted(unknown))}"
                )
            results = [
                it for it in results
                if all(it.get(field) == value for field, value in where.items())
            ]

        if sort_by is not None:
            results = sorted(results, key=lambda it: it.get(sort_by))

        if limit is not None:
            results = results[:limit]

        return [dict(it) for it in results]
