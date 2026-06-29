"""miniquery — a tiny in-memory record store.

Implements `class Store` per `provided/contract.py`. Behaviour evolves per
ticket. Implemented so far:
  - Store.add(record)  : store a copy of the record
  - Store.all()        : return all stored records (copies)
  - Store.query()      : return records (copies); supports:
      * where          : equality match on ALL key==value pairs (S1)
      * sort_by        : sort results ASCENDING by that field's value (S2)
      * limit / offset : paginate results AFTER sorting (S3)
      * select         : project each record to ONLY the selected keys (S4)

`where` policy (S1; S5 change REVERTED in S6):
  - A record matches only if it contains EVERY `where` key with an equal value.
  - Unknown-field handling (S6 reverts to the original S1 rule): a `where` key
    that is not present in ANY stored record is a hard error — `query(...)`
    raises KeyError(key).
    (S5 had replaced this hard error with a silent no-match returning []; S6
    reverts that, restoring the pre-S5 KeyError behaviour.)
  - A `where` key that is present in some records but absent from a particular
    record simply means that record does not match (it is not an error), as
    long as the field appears in at least one stored record.

`sort_by` policy (decided in S2):
  - Sort ascending by the given field's value.
  - Records with EQUAL sort keys keep their INSERTION ORDER (stable sort).
    Python's `sorted` is guaranteed stable, so this falls out naturally.

`limit`/`offset` policy (decided in S3):
  - Pagination is applied AFTER filtering and sorting.
  - `offset` (default 0) skips that many leading results.
  - `limit` (default None) caps the number returned; None means no cap.

`select` policy (decided in S4):
  - Each returned record contains ONLY the selected keys, and only those that
    are actually present on that record. A selected key absent from a given
    record is simply omitted from that record's output (NOT an error, unlike
    `where`'s unknown-field rule) — projection is best-effort per record.
  - Projection runs LAST, after filtering, sorting, and pagination, so it never
    affects which records match, their order, or the page selected.
  - Selected-key order is preserved in each projected record.
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
        matching ALL key==value pairs. A `where` key absent from a particular
        record means that record does not match; a `where` key absent from
        EVERY stored record raises KeyError(key) (S6 reverts the S5 silent
        no-match back to this original S1 hard error).

        `sort_by` orders the (already filtered) results ascending by that
        field's value; records with equal keys keep their insertion order
        (stable sort).

        `limit`/`offset` paginate the (already filtered and sorted) results:
        `offset` skips that many leading results (default 0); `limit` caps the
        number returned (default None means no cap).

        `select` projects each returned record to ONLY the selected keys that
        are present on that record (missing selected keys are omitted, not an
        error). Projection is applied last and does not affect matching, order,
        or pagination.
        """
        records = self._records

        if where:
            # Unknown-field check (S1 behaviour, restored in S6): a `where` key
            # absent from EVERY stored record is a hard error.
            for key in where:
                if not any(key in record for record in records):
                    raise KeyError(key)

            # A record matches only when it contains every `where` key with an
            # equal value.
            records = [
                record for record in records
                if all(key in record and record[key] == value
                       for key, value in where.items())
            ]

        if sort_by is not None:
            # sorted() is stable, so records with equal sort keys retain their
            # relative (insertion) order.
            records = sorted(records, key=lambda record: record[sort_by])

        # Pagination (S3): applied AFTER filtering and sorting.
        # offset skips leading results; limit caps the count (None = no cap).
        if offset or limit is not None:
            stop = None if limit is None else offset + limit
            records = records[offset:stop]

        result = [copy.deepcopy(record) for record in records]

        # Projection (S4): applied LAST, after filtering/sorting/pagination.
        # Keep only the selected keys that are present on each record; preserve
        # the order in which keys were selected. A selected key missing from a
        # record is simply omitted (not an error).
        if select is not None:
            result = [
                {key: record[key] for key in select if key in record}
                for record in result
            ]

        return result
