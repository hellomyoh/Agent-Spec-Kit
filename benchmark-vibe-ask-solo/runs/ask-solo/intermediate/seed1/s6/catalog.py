"""Catalog: an in-memory collection of item dicts.

Implements the pinned API contract (see provided/contract.py). Item dicts each
carry a string 'name'. Reads return copies so callers cannot mutate internal state.
"""


class Catalog:
    def __init__(self) -> None:
        self._items: list[dict] = []

    def add(self, item: dict) -> None:
        self._items.append(dict(item))

    def all(self) -> list[dict]:
        return [dict(item) for item in self._items]

    def search(
        self,
        query: str | None = None,
        where: dict | None = None,
        sort_by: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        results = self._items

        if query is None:
            # No text filter: an empty search (no search term given) is the plain
            # list view and lets every item through. `search()` / query=None == all().
            pass
        elif query.strip() == "":
            # A non-None but blank query (empty "" or all-whitespace) is a real but
            # unusable search term and matches nothing.
            results = []
        else:
            # Non-blank query: case-insensitive substring match on item 'name'.
            needle = query.casefold()
            results = [item for item in results if needle in item["name"].casefold()]

        if where is not None:
            # Equality filter; multiple keys combine with AND. A where field
            # missing from any item under test yields an empty result (matches
            # nothing) rather than raising.
            if any(field not in item for field in where for item in results):
                results = []
            else:
                results = [
                    item
                    for item in results
                    if all(item[field] == value for field, value in where.items())
                ]

        if sort_by is not None:
            # Ascending by the field value; ties keep insertion order
            # (Python's sorted is stable).
            results = sorted(results, key=lambda item: item.get(sort_by))

        if limit is not None:
            # Cap to the first `limit` results, applied last (after filtering and
            # sorting). A non-positive limit caps to nothing (empty list).
            results = results[:limit] if limit > 0 else []

        return [dict(item) for item in results]
