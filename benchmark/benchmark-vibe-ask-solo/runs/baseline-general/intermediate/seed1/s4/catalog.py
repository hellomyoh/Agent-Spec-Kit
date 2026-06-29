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

        With no arguments, returns all items in insertion order. When `query`
        is not None, items are kept only when `query` is a case-insensitive
        substring of the item's 'name'. A `query` that is empty or only
        whitespace matches nothing and yields an empty list.

        When `where` is given, it is an equality filter mapping field names to
        required values; an item is kept only when it has every field set to
        the matching value (multiple fields are combined with AND). Each
        `where` field must be present on at least one item in the catalog;
        a field absent from every item raises ValueError.

        When `sort_by` is given, results are ordered by that field in ascending
        order; items that tie on the field keep their insertion order (stable).

        When `limit` is given, it caps the number of results: after filtering and
        sorting, only the first `limit` items are returned. `limit=None` means no
        cap. A `limit` of 0 yields an empty list; a `limit` larger than the number
        of matches returns all of them.
        """
        if where:
            for field in where:
                if not any(field in item for item in self._items):
                    raise ValueError(f"unknown 'where' field: {field!r}")

        items = self._items

        if query is not None:
            needle = query.strip().lower()
            if not needle:
                return []
            items = [item for item in items if needle in item["name"].lower()]

        if where:
            items = [
                item
                for item in items
                if all(field in item and item[field] == value for field, value in where.items())
            ]

        if sort_by is not None:
            items = sorted(items, key=lambda item: item[sort_by])

        if limit is not None:
            items = items[:limit]

        return [dict(item) for item in items]
