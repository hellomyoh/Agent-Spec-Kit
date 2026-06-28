"""Minimal in-memory record store.

Implements the pinned `Store` API surface from `provided/contract.py`.
Current behaviour: records can be added and read back as copies; `query`
returns records in insertion order with pagination via `offset`/`limit`.
When `limit` is omitted, a default page size of 7 records applies.
"""

import copy

DEFAULT_PAGE_SIZE = 7


class Store:
    """In-memory store of dict records.

    Records are stored as deep copies on add, and returned as deep copies on
    read, so callers can never mutate internal state.
    """

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
        """Return stored records as copies, in insertion order, paginated.

        `offset` skips that many leading records (default 0). `limit` caps the
        number returned; when omitted, the default page size of 7 applies.
        """
        results = self.all()
        results = results[offset:]
        page_size = DEFAULT_PAGE_SIZE if limit is None else limit
        return results[:page_size]
