"""miniquery — a tiny in-memory record store.

Implements the pinned API contract (see provided/contract.py). Signatures are
FIXED across sessions; only behaviour evolves per the per-session TICKET.md.

S0: scaffold add / all / query() (no-arg -> return all).
S1: query(where={k: v, ...}) -> records matching ALL key==value pairs.
    A `where` field that is present in NO stored record is an ERROR (KeyError):
    `where` keys are validated against the known field set.
S2: query(sort_by=field) -> results sorted ASCENDING by that field's value.
    STABLE sort: records with equal sort keys keep their insertion order.
S3: query(limit=int, offset=int) -> pagination, applied AFTER sorting.
    `offset` skips that many leading results (default 0); `limit` caps the
    number returned (default None -> no cap).
S4: query(select=[field, ...]) -> each returned record contains ONLY the
    selected keys THAT ARE PRESENT on that record (missing keys are skipped,
    not errors). Applied LAST, after offset/limit.
S5: a `where` referencing a field not present in ANY stored record yielded NO
    match (query returned []) instead of raising KeyError.
S6 (this session): REVERT S5. Restore the pre-S5 (S1) behaviour: a `where`
    field that is present in NO stored record is again a hard KeyError — the
    `where` keys are validated against the union of keys across stored records,
    and an unknown field raises. (A record that merely lacks a *known* key
    still fails the equality test and is excluded, not an error.)
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

        POLICY (S6, reverts S5; restores S1): an unknown ``where`` field IS an
        error. A ``where`` key that is present in NO stored record raises
        ``KeyError``. The known field set is the union of keys across all stored
        records; each ``where`` key is validated against it. (A record that
        merely lacks a *known* key still fails that equality and is excluded —
        that is a non-match, not an error.)

        S2: supports ``sort_by`` — when given, results are sorted ASCENDING by
        ``record[sort_by]``. The sort is STABLE: records with equal sort keys
        keep their relative insertion order (contract guarantee).

        S3: supports ``limit`` / ``offset`` pagination, applied AFTER sorting.
        ``offset`` skips that many leading results (default 0); ``limit`` caps
        how many are returned (default None -> no cap).

        S4: supports ``select`` — when given a list of field names, each
        returned record is projected to ONLY those keys that are present on the
        record (keys absent from a record are simply omitted, never an error).
        Applied LAST. Combined order: where -> sort_by -> offset/limit -> select.
        """
        records = self._records

        if where:
            # S6 POLICY (reverts S5, restores S1): validate `where` keys against
            # the union of keys across all stored records. A field present in NO
            # record is an unknown field -> raise KeyError (a hard error, not a
            # silent no-match).
            known_fields = set()
            for r in records:
                known_fields.update(r.keys())
            for k in where:
                if k not in known_fields:
                    raise KeyError(k)
            # Keep records matching ALL key==value pairs. A record that lacks a
            # KNOWN key fails that equality test and is excluded (a non-match,
            # not an error).
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
        # (None is the only value that means no cap).
        stop = None if limit is None else offset + limit
        records = records[offset:stop]

        if select is not None:
            # S4: projection — LAST step. Build a fresh dict per record holding
            # ONLY the selected keys that the record actually has (missing keys
            # are skipped silently, not errors — per ticket: "those present on
            # the record"). Deep-copy each kept value so callers can't mutate
            # internal state (records may hold nested dicts/lists). This both
            # projects AND produces the required fresh copies, so the usual
            # final deepcopy is skipped on this path.
            return [
                {k: copy.deepcopy(r[k]) for k in select if k in r}
                for r in records
            ]

        return [copy.deepcopy(r) for r in records]
