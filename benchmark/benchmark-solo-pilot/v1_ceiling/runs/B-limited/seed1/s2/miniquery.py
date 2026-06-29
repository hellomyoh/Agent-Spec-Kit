"""miniquery — a tiny in-memory record store.

Implements `class Store` per provided/contract.py. Signatures are FIXED across
sessions; only behaviour evolves as tickets direct.

Implemented so far:
  S0 — scaffold:
    - add(record): store a (deep) copy of the record.
    - all(): return all stored records (copies), insertion order.
    - query(): with no arguments, return all records (copies), insertion order.
  S1 — equality filter (`where`):
    - query(where={k: v, ...}): return records matching ALL key==value pairs.
    - POLICY: a `where` key not present in ANY stored record raises KeyError(key)
      (an unknown field is a hard error, not a silent no-match).
  S2 — sorting (`sort_by`):
    - query(sort_by=field): sort results ASCENDING by that field's value.
    - POLICY: ties (records with EQUAL sort keys) keep their INSERTION ORDER
      (stable sort). Python's `sorted` is stable, so this falls out naturally.

The remaining query() parameters (limit/offset/select) are present to honour the
pinned signature but are not yet implemented.
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
        """Return matching records as copies.

        where: equality match on ALL key==value pairs. A key not present in ANY
            stored record raises KeyError(key) (unknown field is a hard error).

        sort_by: sort results ASCENDING by that field's value. Ties (equal sort
            keys) keep their insertion order (stable sort).

        Other parameters (limit/offset/select) are part of the pinned contract
        signature but are not implemented in this session's ticket.
        """
        records = self._records

        if where:
            for key in where:
                # POLICY (S1): unknown field — absent from every record — is a hard error.
                if not any(key in r for r in records):
                    raise KeyError(key)
            records = [
                r for r in records
                if all(k in r and r[k] == v for k, v in where.items())
            ]

        if sort_by is not None:
            # POLICY (S2): ascending, stable (ties keep insertion order). `sorted`
            # is stable, so equal keys preserve their current relative order.
            records = sorted(records, key=lambda r: r[sort_by])

        return [copy.deepcopy(r) for r in records]
