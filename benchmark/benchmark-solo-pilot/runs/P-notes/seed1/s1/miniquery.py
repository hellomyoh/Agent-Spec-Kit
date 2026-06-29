"""miniquery — a tiny in-memory record store.

Implements the pinned `Store` API from `provided/contract.py`.
"""

import copy

# Page size applied when `query()` is called without an explicit `limit`.
DEFAULT_PAGE_SIZE = 7


class Store:
    """In-memory store of dict records. Returns copies so callers cannot
    mutate internal state."""

    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        """Store a copy of `record`."""
        self._records.append(copy.deepcopy(record))

    def all(self) -> list[dict]:
        """Return copies of all stored records, in insertion order."""
        return [copy.deepcopy(r) for r in self._records]

    def query(self,
              where: dict | None = None,
              sort_by: str | None = None,
              limit: int | None = None,
              offset: int = 0
              ) -> list[dict]:
        """Return stored records (copies) in insertion order, paginated.

        `offset` skips that many leading records (default 0). `limit` caps the
        number returned; when omitted, the DEFAULT_PAGE_SIZE applies.

        `where` and `sort_by` are accepted for API compatibility but not yet
        honoured.
        """
        results = self._records[offset:]

        page_size = DEFAULT_PAGE_SIZE if limit is None else limit
        results = results[:page_size]

        return [copy.deepcopy(r) for r in results]
