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

        if query is not None:
            # query=None means "no text filter"; a non-None query is a text search.
            # A blank query (empty or all-whitespace) matches nothing.
            if query.strip() == "":
                results = []
            else:
                needle = query.casefold()
                results = [
                    item for item in results if needle in item["name"].casefold()
                ]

        if where is not None:
            for field in where:
                if any(field not in item for item in results):
                    raise ValueError(f"unknown where field: {field!r}")
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
            results = results[:limit]

        return [dict(item) for item in results]
