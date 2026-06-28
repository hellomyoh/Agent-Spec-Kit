"""miniquery — a tiny in-memory record store.

Implements `class Store` per `provided/contract.py`. Behaviour evolves per
ticket; this session (S0 — Scaffold) implements only:
  - Store.add(record)  : store a copy of the record
  - Store.all()        : return all stored records (copies)
  - Store.query()      : with no arguments, return all records (copies)
"""

import copy


class Store:
    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        """Store a copy of the record so later caller mutations don't leak in."""
        self._records.append(copy.deepcopy(record))

    def all(self) -> list[dict]:
        """Return all stored records as a list of copies."""
        return [copy.deepcopy(record) for record in self._records]

    def query(self,
              where: dict | None = None,
              sort_by: str | None = None,
              limit: int | None = None,
              offset: int = 0,
              select: list[str] | None = None
              ) -> list[dict]:
        """With no arguments, return all records (copies).

        The full filtering/sorting/projection semantics are introduced by
        later tickets; this scaffold only supports the no-argument form.
        """
        return self.all()
