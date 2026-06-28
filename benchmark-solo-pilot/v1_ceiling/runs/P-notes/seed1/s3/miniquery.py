"""miniquery — a tiny in-memory record store.

Implements the pinned API contract (see provided/contract.py). Signatures are
FIXED across sessions; only behaviour evolves per the per-session TICKET.md.

S0: scaffold add / all / query() (no-arg -> return all).
S1: query(where={k: v, ...}) -> records matching ALL key==value pairs. A
    `where` key absent from EVERY stored record raises KeyError(key).
S2: query(sort_by=field) -> results sorted ASCENDING by that field's value.
    STABLE sort: records with equal sort keys keep their insertion order.
S3 (this session): query(limit=int, offset=int) -> pagination, applied AFTER
    sorting. `offset` skips that many leading results (default 0); `limit`
    caps the number returned (default None -> no cap).
"""

import copy


class Store:
    """In-memory store of dict records.

    Records are stored as deep copies on insertion and returned as deep copies,
    so callers can never mutate the store's internal state.
    """

    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        """Store a (deep) copy of ``record``."""
        self._records.append(copy.deepcopy(record))

    def all(self) -> list[dict]:
        """Return all stored records as a list of (deep) copies."""
        return [copy.deepcopy(r) for r in self._records]

    def query(self,
              where: dict | None = None,       # equality match on ALL key==value
              sort_by: str | None = None,      # ascending; ties keep insertion order
              limit: int | None = None,
              offset: int = 0,
              select: list[str] | None = None  # project to these keys only
              ) -> list[dict]:
        """Query stored records.

        S1: supports ``where`` — an equality filter. ``query(where={k: v, ...})``
        returns records matching ALL key==value pairs (as deep copies).

        POLICY (fixed for all future ``where`` handling): if a ``where`` key is
        not present in ANY stored record, raise ``KeyError(key)`` — an unknown
        field is a hard error, not a silent no-match.

        S2: supports ``sort_by`` — when given, results are sorted ASCENDING by
        ``record[sort_by]``. The sort is STABLE: records with equal sort keys
        keep their relative insertion order (contract guarantee).

        S3: supports ``limit`` / ``offset`` pagination, applied AFTER sorting.
        ``offset`` skips that many leading results (default 0); ``limit`` caps
        how many are returned (default None -> no cap). Combined order is
        where -> sort_by -> offset/limit.

        The remaining parameter (select) is part of the fixed contract
        signature and gains behaviour in a later session.
        """
        records = self._records

        if where:
            # Validate every filter key exists in at least one stored record.
            # Unknown field -> hard error (KeyError), per pinned POLICY.
            for key in where:
                if not any(key in r for r in records):
                    raise KeyError(key)
            # Keep records matching ALL key==value pairs. A record missing a key
            # simply fails that equality test (it cannot match), but is not an
            # error because the key exists in *some* record (checked above).
            records = [
                r for r in records
                if all(k in r and r[k] == v for k, v in where.items())
            ]

        if sort_by is not None:
            # Ascending, STABLE sort. Python's `sorted` is stable, so records
            # with equal sort keys keep their insertion order automatically.
            # Applied AFTER `where` filtering (combined order: where -> sort_by).
            records = sorted(records, key=lambda r: r[sort_by])

        # S3: pagination — applied AFTER sorting (where -> sort_by -> offset/limit).
        # `offset` skips leading results; `limit` caps the count. Compute an
        # explicit slice so `limit=0` means "return nothing" rather than "no cap"
        # (None is the only value that means no cap). `sorted`/`where` above
        # already produced a fresh list, but slicing self._records directly when
        # neither ran is also safe because the final deepcopy returns copies.
        stop = None if limit is None else offset + limit
        records = records[offset:stop]

        return [copy.deepcopy(r) for r in records]
