"""Minimal in-memory record store.

Implements the pinned `Store` API surface from `provided/contract.py`.
Current behaviour: records can be added and read back as copies; `query`
with no arguments returns all stored records.
"""

import copy


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
        """Return stored records as copies.

        With no arguments, returns all records in insertion order.
        """
        return self.all()
