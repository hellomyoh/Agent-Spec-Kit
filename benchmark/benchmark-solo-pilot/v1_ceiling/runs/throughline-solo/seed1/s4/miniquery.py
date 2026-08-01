"""miniquery — a tiny in-memory record store.

Implements the pinned API contract in provided/contract.py. The public surface
(method names and signatures) is FIXED across sessions; only behaviour evolves
as per-session tickets direct.

Implemented so far:
  - Store.add(record)   : store a defensive copy of the record.
  - Store.all()         : return all stored records (copies, insertion order).
  - Store.query()       : return matching records (copies).
      * where={k: v, ...} : keep records matching ALL key==value pairs (S1).
      * sort_by=field     : stable ascending sort by that field (S2).
      * offset / limit    : paginate the (filtered, sorted) results (S3).
      * select=[field,..] : project each row to only the selected keys (S4).

The query() signature carries the full pinned parameter set so the API surface
stays stable.
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
        """Query stored records, returning copies.

        ``where`` (S1): a mapping of field -> value. Only records that match
        ALL key==value pairs are returned. Matching uses ``==`` on the stored
        value. A record that lacks one of the ``where`` keys does not match.
        Policy (S1/D6): if a ``where`` key is not present in ANY stored record,
        raise ``KeyError(key)`` — an unknown field is a hard error, not a
        silent no-match.

        ``sort_by`` (S2): a field name. Results are sorted ASCENDING by that
        field's value. The sort is STABLE: records with equal sort keys keep
        their relative insertion order. Sorting is applied AFTER ``where``
        filtering, over the records that survived the filter.
        Policy (S2/D7): consistent with the ``where`` unknown-field rule, if
        ``sort_by`` names a field not present in ANY stored record, raise
        ``KeyError(sort_by)``. A record that lacks the key (while other records
        have it) raises ``KeyError(sort_by)`` as well, since its sort position
        is undefined.

        ``offset`` / ``limit`` (S3): pagination applied AFTER ``where`` and
        ``sort_by``. ``offset`` (default 0) skips that many leading results;
        ``limit`` (default ``None`` = no cap) caps how many are returned. Both
        are applied with list slicing, so out-of-range values clamp rather than
        error (e.g. an ``offset`` past the end yields an empty list).

        ``select`` (S4): a list of field names. Each returned record is
        projected to ONLY the selected keys, preserving the order they appear in
        ``select``. A selected key that a given record lacks is silently
        omitted from that record (NOT an error and NOT inserted as None) — so a
        projected record may have fewer keys than ``select``, or even be empty.
        Projection is applied LAST, after ``where``, ``sort_by``, and
        pagination: it changes the SHAPE of the returned rows, not which rows
        are returned or their order. ``select=None`` (default) returns full
        records, and ``select=[]`` projects every row to an empty dict.
        Note (S4): unlike ``where``/``sort_by``, ``select`` does NOT validate
        field names — projection describes the desired output shape and a
        field absent everywhere simply yields nothing for that key. The
        defensive output copy is produced BY the projection (a fresh dict per
        row), so callers still cannot mutate internal state.
        """
        results = self._records

        if where:
            known_keys = self._known_keys()
            for key in where:
                if key not in known_keys:
                    raise KeyError(key)
            results = [
                r
                for r in results
                if all(k in r and r[k] == v for k, v in where.items())
            ]

        if sort_by is not None:
            # Unknown-field policy (D7), consistent with `where` (D6): the
            # field must exist somewhere in the store, else it is a hard error.
            if sort_by not in self._known_keys():
                raise KeyError(sort_by)
            # Python's sorted() is stable, so equal keys preserve the order of
            # `results` (which is insertion order after filtering). A record
            # missing the key has no defined sort position -> KeyError.
            results = sorted(results, key=lambda r: r[sort_by])

        # Pagination (S3): applied AFTER where-filtering and sorting.
        # Slicing clamps gracefully: offset past the end -> empty list; a limit
        # larger than what remains just returns the remainder. offset=0 and
        # limit=None (the defaults) leave the result unchanged.
        if offset:
            results = results[offset:]
        if limit is not None:
            results = results[:limit]

        # Projection (S4): applied LAST. Each row becomes a fresh dict with only
        # the selected keys that the row actually has (missing keys are dropped,
        # not errors). When select is None we still copy out (defensive copy);
        # when select is given the projection IS the copy.
        if select is not None:
            return [{k: r[k] for k in select if k in r} for r in results]

        return [dict(r) for r in results]

    def _known_keys(self) -> set:
        """Union of keys across all stored records (empty if the store is empty)."""
        if not self._records:
            return set()
        return set().union(*(r.keys() for r in self._records))
