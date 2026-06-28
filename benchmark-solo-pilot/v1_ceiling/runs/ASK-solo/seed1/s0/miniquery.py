"""miniquery — a tiny in-memory record store.

Implements the pinned API contract in provided/contract.py. The public surface
(method names and signatures) is FIXED across sessions; only behaviour evolves
as per-session tickets direct.

Session S0 (scaffold) implements:
  - Store.add(record)   : store a defensive copy of the record.
  - Store.all()         : return all stored records (copies, insertion order).
  - Store.query()       : with no arguments, return all records (copies).

The query() signature carries the full pinned parameter set so the API surface
stays stable, but only the no-argument behaviour is implemented this session.
The remaining parameters (where/sort_by/limit/offset/select) are reserved for
future tickets and are not yet honoured.
"""


class Store:
    """An ordered, in-memory collection of dict records.

    Records are stored and returned as shallow copies so callers cannot mutate
    the store's internal state by holding on to a reference.
    """

    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        """Store a copy of ``record``.

        A shallow copy is taken on insertion so later mutation of the caller's
        dict does not affect what is stored.
        """
        self._records.append(dict(record))

    def all(self) -> list[dict]:
        """Return all stored records as copies, in insertion order."""
        return [dict(r) for r in self._records]

    def query(
        self,
        where: dict | None = None,
        sort_by: str | None = None,
        limit: int | None = None,
        offset: int = 0,
        select: list[str] | None = None,
    ) -> list[dict]:
        """Query stored records.

        Session S0 scope: with no arguments, return all records (copies), in
        insertion order. The where/sort_by/limit/offset/select parameters are
        part of the fixed contract but are reserved for future tickets and are
        not implemented yet.
        """
        return self.all()
