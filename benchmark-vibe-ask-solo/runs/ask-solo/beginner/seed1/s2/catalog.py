"""A small in-memory catalog: add items, list them, and search them.

Implements the pinned API contract (provided/contract.py). `search` supports a
case-insensitive substring text filter on an item's 'name' (`query=...`) and an
equality filter on arbitrary item fields (`where=...`). Filtering on a field that
no item has raises KeyError, so a typo'd field name fails loudly instead of
silently returning nothing. The `sort_by` and `limit` arguments are part of the
fixed contract but are not active yet.
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
        """Return items, optionally filtered by name text and/or field equality.

        With `query=None` no text filter is applied (list mode). With a non-None
        `query`, items are kept when the query appears anywhere in their 'name',
        compared case-insensitively (so 'ap' matches 'Apple'). An empty query
        matches every item.

        With a non-None `where`, items are kept only when every field in `where`
        equals the item's value for that field. A `where` key that is present on
        no item in a non-empty catalog is treated as a mistake (e.g. a typo) and
        raises KeyError, rather than silently matching nothing. (An empty catalog
        skips this check and simply returns no items.) When both `query` and
        `where` are given, both must hold.

        `sort_by` and `limit` are part of the fixed contract but are not active
        yet.
        """
        items = self._items

        if where is not None and items:
            for field in where:
                if not any(field in item for item in items):
                    raise KeyError(
                        f"cannot filter on unknown field {field!r}: "
                        f"no item has it"
                    )
            items = [
                item
                for item in items
                if all(item.get(field) == value for field, value in where.items())
            ]

        if query is not None:
            needle = query.casefold()
            items = [
                item
                for item in items
                if needle in str(item.get("name", "")).casefold()
            ]

        return [dict(item) for item in items]
