"""A small in-memory catalog: add items, list them, and search them.

Implements the pinned API contract (provided/contract.py). `search` supports a
case-insensitive substring text filter on an item's 'name' (`query=...`), an
equality filter on arbitrary item fields (`where=...`), stable ordering of the
results by a field (`sort_by=...`), and a cap on how many results to return
(`limit=...`).

Two "fail loudly / show less" policies keep behaviour predictable:
- Filtering or sorting on a field that no item has raises KeyError, so a typo'd
  field name fails loudly instead of doing something surprising.
- `search` only returns items once the caller supplies a real search criterion.
  With no `where` and a blank or omitted `query` it returns nothing (an empty
  list) rather than the whole catalog. To deliberately view everything, call
  `all()`.

`limit` caps the result to the top N items (after filtering and sorting); a
negative or non-integer limit is rejected as a mistake (raises).
"""


class Catalog:
    """Holds a list of item dicts. Each item has a string 'name'."""

    def __init__(self) -> None:
        self._items: list[dict] = []

    def add(self, item: dict) -> None:
        """Add one item to the catalog."""
        self._items.append(dict(item))

    def all(self) -> list[dict]:
        """Return every item, in insertion order (copies).

        This is the explicit "view the full list" affordance. Unlike `search`,
        it always returns the whole catalog.
        """
        return [dict(item) for item in self._items]

    def search(
        self,
        query: str | None = None,
        where: dict | None = None,
        sort_by: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Return items matching the given criteria, optionally sorted and capped.

        Showing nothing by default: a search shows results only once the caller
        provides a real criterion. If `where` is None and `query` is None or
        blank (empty or whitespace only), this returns an empty list instead of
        the full catalog. Call `all()` to deliberately view everything.

        `query` (text filter): with a non-blank `query`, items are kept when the
        query appears anywhere in their 'name', compared case-insensitively (so
        'ap' matches 'Apple'). A blank `query` applies no text filter (and, on
        its own, yields nothing per the rule above).

        `where` (field equality filter): items are kept only when every field in
        `where` equals the item's value for that field. A `where` key that is
        present on no item in a non-empty catalog is treated as a mistake (e.g. a
        typo) and raises KeyError, rather than silently matching nothing. (An
        empty catalog skips this check and simply returns no items.) When both
        `query` and `where` are given, both must hold.

        `sort_by` (ordering field): when given, the surviving items are returned
        ordered by that field. The sort is stable, so items with an equal value
        keep their insertion order. Items missing the field sort after those
        that have it. `sort_by` referencing a field that no item has raises
        KeyError (same loud-on-typo policy as `where`); on an empty result there
        is nothing to order.

        `limit` (max results): when given, only the first `limit` items of the
        result are returned (the "top N" in the result's order, i.e. after any
        filtering and sorting). `limit=None` means no cap. `limit=0` returns an
        empty list. A negative or non-integer `limit` is treated as a mistake and
        raises (ValueError / TypeError), consistent with the catalog's
        fail-loudly-on-bad-input policy. A `limit` larger than the result simply
        returns all of it.
        """
        # Show nothing until the caller supplies a real criterion.
        query_is_blank = query is None or query.strip() == ""
        if where is None and query_is_blank:
            return []

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

        if not query_is_blank:
            needle = query.casefold()
            items = [
                item
                for item in items
                if needle in str(item.get("name", "")).casefold()
            ]

        if sort_by is not None and items:
            if not any(sort_by in item for item in items):
                raise KeyError(
                    f"cannot sort on unknown field {sort_by!r}: no item has it"
                )
            # Stable sort: equal values keep insertion order. Items lacking the
            # field sort last (and only ever compare equal among themselves, so
            # their relative order is preserved too).
            items = sorted(
                items,
                key=lambda item: (0, item[sort_by]) if sort_by in item else (1,),
            )

        if limit is not None:
            # A bad cap is a caller mistake: reject it loudly rather than guess.
            # (bool is an int subclass but is not a meaningful count, so reject.)
            if isinstance(limit, bool) or not isinstance(limit, int):
                raise TypeError(
                    f"limit must be an int or None, got {type(limit).__name__}"
                )
            if limit < 0:
                raise ValueError(f"limit must be >= 0, got {limit}")
            items = items[:limit]

        return [dict(item) for item in items]
