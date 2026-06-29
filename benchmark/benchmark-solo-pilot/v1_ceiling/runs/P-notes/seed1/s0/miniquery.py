"""miniquery — a tiny in-memory record store.

Implements the pinned API contract (see provided/contract.py). Signatures are
FIXED across sessions; only behaviour evolves per the per-session TICKET.md.

S0 (this session): scaffold add / all / query() (no-arg -> return all).
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

        S0: only the no-argument form is implemented — it returns all records
        (as copies). The remaining parameters are part of the fixed contract
        signature and will gain behaviour in later sessions.
        """
        return self.all()
