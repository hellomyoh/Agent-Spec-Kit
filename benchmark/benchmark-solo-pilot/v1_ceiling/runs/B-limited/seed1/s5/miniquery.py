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
  S2 — sorting (`sort_by`):
    - query(sort_by=field): sort results ASCENDING by that field's value.
    - POLICY: ties (records with EQUAL sort keys) keep their INSERTION ORDER
      (stable sort). Python's `sorted` is stable, so this falls out naturally.
  S3 — pagination (`limit`, `offset`):
    - query(limit=int, offset=int): applied AFTER sorting.
    - `offset` skips that many leading results (default 0).
    - `limit` caps the number returned (default None => no cap).
  S4 — projection (`select`):
    - query(select=[field, ...]): each returned record contains ONLY the
      selected keys that are PRESENT on that record. Missing keys are skipped
      (no KeyError, no None filler). All other query behaviour is unchanged.
  S5 — unknown-field handling in `where` (CHANGES S1 policy):
    - A `where` key not present in ANY stored record now yields NO match
      (query returns []). It must NOT raise. This supersedes the old S1
      KeyError-on-unknown-field policy. A record simply fails the match when
      it lacks a `where` key, so a field absent everywhere matches nothing.

Query pipeline order: where -> sort_by -> paginate -> copy out -> select.
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

        where: equality match on ALL key==value pairs. A record that lacks a
            `where` key fails the match, so a field absent from every record
            yields no results ([]) — an unknown field is NOT an error (S5).

        sort_by: sort results ASCENDING by that field's value. Ties (equal sort
            keys) keep their insertion order (stable sort).

        limit/offset: pagination, applied AFTER sorting. `offset` skips that many
            leading results (default 0); `limit` caps the number returned
            (default None => no cap).

        select: project each returned record to ONLY the listed keys that are
            PRESENT on that record. Keys absent from a record are simply omitted
            (no error, no None placeholder). select=None => full records.
        """
        records = self._records

        if where:
            # S5: no unknown-field check. A record lacking a `where` key fails
            # the match, so a field present in NO record matches nothing (=> []),
            # rather than raising KeyError as the old S1 policy did.
            records = [
                r for r in records
                if all(k in r and r[k] == v for k, v in where.items())
            ]

        if sort_by is not None:
            # POLICY (S2): ascending, stable (ties keep insertion order). `sorted`
            # is stable, so equal keys preserve their current relative order.
            records = sorted(records, key=lambda r: r[sort_by])

        # S3: pagination, applied AFTER sorting. offset skips leading results;
        # limit caps the count. Slicing handles out-of-range values gracefully
        # (offset beyond the end => empty; limit larger than remaining => all).
        if offset or limit is not None:
            stop = None if limit is None else offset + limit
            records = records[offset:stop]

        result = [copy.deepcopy(r) for r in records]

        # S4: projection, applied LAST on the output copies. Each record keeps
        # only the selected keys that are present on it; missing keys are skipped.
        if select is not None:
            result = [
                {k: r[k] for k in select if k in r}
                for r in result
            ]

        return result
