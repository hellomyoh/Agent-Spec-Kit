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
        """Add an item to the catalog (stored as an independent deep copy)."""
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

        query:
            None -> no text filter (list mode: every item).
            A blank or whitespace-only string ("" or "   ") -> no match, returns
            [] (an empty search box must not dump the whole catalog).
            Otherwise a case-insensitive substring match on each item's 'name'.
        where:
            None -> no equality filter. A dict selects items whose fields equal
            every given key/value pair (multiple keys are combined with AND).
            Every key must be present on every item in the catalog; a key missing
            from any item raises ValueError.
        sort_by:
            None -> insertion order. Otherwise the field name to order the results
            by, ascending, using a stable sort (items with equal keys keep their
            relative insertion order). The field must be present on every result
            item; a result missing it raises ValueError. Values must be mutually
            comparable (Python raises TypeError otherwise).
        limit:
            None -> no cap (every surviving result). Otherwise a non-negative int
            capping the result to its first N items, applied last (after filtering
            and sorting): the top N. limit=0 returns []; a limit at or above the
            result count returns all results. A negative limit raises ValueError;
            a non-int limit (bool included) raises TypeError.

        Order of operations: filtering (query, then where) runs first, sort_by
        then orders the surviving results, and limit finally caps that ordered
        list to its first N.
        """
        if limit is not None:
            # bool is an int subclass; reject it so limit=True/False is not
            # silently read as 1/0.
            if isinstance(limit, bool) or not isinstance(limit, int):
                raise TypeError(
                    f"limit must be an int or None, not {type(limit).__name__}"
                )
            if limit < 0:
                raise ValueError(f"limit must be non-negative, got {limit}")

        if where is not None:
            for key in where:
                if any(key not in item for item in self._items):
                    raise ValueError(
                        f"where key {key!r} is not present on every item"
                    )

        results = self._items

        # query=None is list mode; a blank/whitespace-only query matches nothing.
        if query is not None:
            if query.strip():
                needle = query.casefold()
                results = [
                    item for item in results
                    if needle in item["name"].casefold()
                ]
            else:
                results = []

        if where is not None:
            results = [
                item for item in results
                if all(item[key] == value for key, value in where.items())
            ]

        if sort_by is not None:
            if any(sort_by not in item for item in results):
                raise ValueError(
                    f"sort_by key {sort_by!r} is not present on every result item"
                )
            # sorted() is stable, so equal keys preserve insertion order.
            results = sorted(results, key=lambda item: item[sort_by])

        # limit caps the ordered results to the first N (the top N). A cap >=
        # len(results) is a no-op; limit=0 yields [].
        if limit is not None:
            results = results[:limit]

        return copy.deepcopy(results)
