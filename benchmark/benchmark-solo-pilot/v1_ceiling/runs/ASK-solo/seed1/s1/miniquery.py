"""miniquery — a tiny in-memory record store.

Implements the pinned API contract in provided/contract.py. The public surface
(method names and signatures) is FIXED across sessions; only behaviour evolves
as per-session tickets direct.

Implemented so far:
  - Store.add(record)   : store a defensive copy of the record.
  - Store.all()         : return all stored records (copies, insertion order).
  - Store.query()       : return matching records (copies, insertion order).
      * where={k: v, ...} : keep records matching ALL key==value pairs (S1).

The query() signature carries the full pinned parameter set so the API surface
stays stable. The sort_by/limit/offset/select parameters are part of the fixed
contract but are reserved for future tickets and are not yet honoured.
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
        """Query stored records, returning copies in insertion order.

        ``where`` (S1): a mapping of field -> value. Only records that match
        ALL key==value pairs are returned. Matching uses ``==`` on the stored
        value. A record that lacks one of the ``where`` keys does not match.

        Policy (S1): if a ``where`` key is not present in ANY stored record,
        raise ``KeyError(key)`` — an unknown field is a hard error, not a
        silent no-match.

        The sort_by/limit/offset/select parameters are part of the fixed
        contract but are reserved for future tickets and are not yet honoured.
        """
        results = self._records

        if where:
            known_keys = set().union(*(r.keys() for r in self._records)) if self._records else set()
            for key in where:
                if key not in known_keys:
                    raise KeyError(key)
            results = [
                r
                for r in results
                if all(k in r and r[k] == v for k, v in where.items())
            ]

        return [dict(r) for r in results]
