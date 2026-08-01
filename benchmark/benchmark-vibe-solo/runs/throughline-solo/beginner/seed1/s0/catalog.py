"""A small in-memory catalog: add items and list them.

Implements the pinned API contract (provided/contract.py). This session covers
adding items and viewing the full list; `search` is part of the fixed contract
and is provided in a minimal form (list mode only) for now.
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
        """Return items. With no arguments this lists everything (list mode).

        Only list mode (query=None) is defined this session; richer filtering,
        sorting, and limiting evolve in later sessions.
        """
        return self.all()
