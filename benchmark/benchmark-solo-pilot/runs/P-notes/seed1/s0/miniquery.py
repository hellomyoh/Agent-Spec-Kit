"""miniquery — a tiny in-memory record store.

Implements the pinned `Store` API from `provided/contract.py`.
"""

import copy


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
        """Return stored records (copies).

        With no arguments, return all records in insertion order.
        """
        return [copy.deepcopy(r) for r in self._records]
