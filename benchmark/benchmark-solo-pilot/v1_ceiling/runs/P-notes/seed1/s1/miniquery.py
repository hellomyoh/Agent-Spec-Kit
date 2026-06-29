"""miniquery — a tiny in-memory record store.

Implements the pinned API contract (see provided/contract.py). Signatures are
FIXED across sessions; only behaviour evolves per the per-session TICKET.md.

S0: scaffold add / all / query() (no-arg -> return all).
S1 (this session): query(where={k: v, ...}) -> records matching ALL key==value
    pairs. A `where` key absent from EVERY stored record raises KeyError(key).
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

        The remaining parameters (sort_by, limit, offset, select) are part of the
        fixed contract signature and gain behaviour in later sessions.
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

        return [copy.deepcopy(r) for r in records]
