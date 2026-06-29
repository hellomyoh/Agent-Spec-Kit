"""miniquery — a tiny in-memory record store.

Implements `class Store` per `provided/contract.py`. Behaviour evolves per
ticket. Implemented so far:
  - Store.add(record)  : store a copy of the record
  - Store.all()        : return all stored records (copies)
  - Store.query()      : return records (copies); supports:
      * where   : equality match on ALL key==value pairs (S1)
      * sort_by : sort results ASCENDING by that field's value (S2)

`where` policy (decided in S1, applies to all future `where` handling):
  - If a `where` key is not present in ANY stored record, raise KeyError(key).
    An unknown field is a hard error, not a silent no-match.

`sort_by` policy (decided in S2):
  - Sort ascending by the given field's value.
  - Records with EQUAL sort keys keep their INSERTION ORDER (stable sort).
    Python's `sorted` is guaranteed stable, so this falls out naturally.
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
        """Return matching records as copies.

        With no arguments, return all records. `where` filters to records
        matching ALL key==value pairs. A `where` key absent from every stored
        record raises KeyError(key).

        `sort_by` orders the (already filtered) results ascending by that
        field's value; records with equal keys keep their insertion order
        (stable sort).

        limit/offset/select are introduced by later tickets and are not yet
        implemented.
        """
        records = self._records

        if where:
            # Policy: an unknown field (absent from ALL records) is a hard error.
            for key in where:
                if not any(key in record for record in records):
                    raise KeyError(key)
            records = [
                record for record in records
                if all(key in record and record[key] == value
                       for key, value in where.items())
            ]

        if sort_by is not None:
            # sorted() is stable, so records with equal sort keys retain their
            # relative (insertion) order.
            records = sorted(records, key=lambda record: record[sort_by])

        return [copy.deepcopy(record) for record in records]
