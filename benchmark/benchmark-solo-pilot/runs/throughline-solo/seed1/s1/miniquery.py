"""miniquery — an in-memory record store.

Implements the `Store` class per provided/contract.py. Records are plain dicts;
the store keeps an internal copy of each and hands back copies so callers cannot
mutate its state.
"""

import copy

DEFAULT_PAGE_SIZE = 7


class Store:
    """In-memory collection of dict records, preserving insertion order."""

    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        """Store a copy of `record`."""
        self._records.append(copy.deepcopy(record))

    def all(self) -> list[dict]:
        """Return copies of all stored records, in insertion order."""
        return [copy.deepcopy(record) for record in self._records]

    def query(
        self,
        where: dict | None = None,
        sort_by: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[dict]:
        """Return stored records (copies) in insertion order, with paging.

        `offset` skips that many leading records. `limit` caps how many are
        returned; when `limit` is omitted, the default page size applies.

        `where` and `sort_by` are part of the pinned contract signature but are
        not yet interpreted.
        """
        results = self.all()
        page_size = DEFAULT_PAGE_SIZE if limit is None else limit
        return results[offset:offset + page_size]
