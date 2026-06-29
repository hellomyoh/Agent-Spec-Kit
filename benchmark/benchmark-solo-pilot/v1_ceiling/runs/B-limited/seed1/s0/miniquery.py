"""miniquery — a tiny in-memory record store.

Implements `class Store` per provided/contract.py. Signatures are FIXED across
sessions; only behaviour evolves as tickets direct.

S0 (this session): scaffold only —
  - add(record): store a copy of the record.
  - all(): return all stored records (copies).
  - query(): with no arguments, return all records (copies).
The remaining query() parameters (where/sort_by/limit/offset/select) are present
to honour the pinned signature but are not yet implemented.
"""

import copy


class Store:
    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        """Store a (deep) copy of the record so later caller mutations don't leak in."""
        self._records.append(copy.deepcopy(record))

    def all(self) -> list[dict]:
        """Return all stored records as copies, in insertion order."""
        return [copy.deepcopy(r) for r in self._records]

    def query(self,
              where: dict | None = None,
              sort_by: str | None = None,
              limit: int | None = None,
              offset: int = 0,
              select: list[str] | None = None
              ) -> list[dict]:
        """With no arguments, return all records (copies), in insertion order.

        Other parameters are part of the pinned contract signature but are not
        implemented in this session's ticket.
        """
        return [copy.deepcopy(r) for r in self._records]
