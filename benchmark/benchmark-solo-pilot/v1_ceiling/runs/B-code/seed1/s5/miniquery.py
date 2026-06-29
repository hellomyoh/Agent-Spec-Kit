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

`where` policy (S1, REVISED in S5):
  - A record matches only if it contains EVERY `where` key with an equal value.
  - S5 change: a `where` key that is not present in ANY stored record now yields
    NO match — `query(...)` returns `[]`. It is NO LONGER a hard error.
    (S1 originally raised KeyError(key) for such an unknown field; S5 replaces
    that with silent no-match.) Because a record only matches when it actually
    contains each `where` key, an absent-everywhere field naturally matches
    nothing, so no special-case check is needed.

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
    record is simply omitted from that record's output (NOT an error, like
    `where`'s S5 behaviour) — projection is best-effort per record.
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
        matching ALL key==value pairs. A `where` key absent from a record means
        that record does not match; a `where` key absent from EVERY stored
        record yields no matches (returns []) — it does NOT raise (S5 change).

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
            # A record matches only when it contains every `where` key with an
            # equal value. S5: an unknown field (absent from all records) is no
            # longer a hard error — it simply matches nothing, yielding [].
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
