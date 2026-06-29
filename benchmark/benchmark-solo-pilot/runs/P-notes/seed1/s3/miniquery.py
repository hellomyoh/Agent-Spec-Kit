"""miniquery — a tiny in-memory record store.

Implements the pinned `Store` API from `provided/contract.py`.
"""

import copy

# Page size applied when `query()` is called without an explicit `limit`.
DEFAULT_PAGE_SIZE = 25


class Store:
    """In-memory store of dict records. Returns copies so callers cannot
    mutate internal state."""

    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        """Store a copy of `record`."""
        self._records.append(copy.deepcopy(record))

    def all(self) -> list[dict]:
        """Return copies of all stored records, in insertion order."""
        return [copy.deepcopy(r) for r in self._records]

    def query(self,
              where: dict | None = None,
              sort_by: str | None = None,
              limit: int | None = None,
              offset: int = 0
              ) -> list[dict]:
        """Return stored records (copies), filtered then paginated.

        `where` keeps only records matching ALL key==value pairs (AND
        semantics); a key absent from a record fails the match for that record.
        Filtering is applied before pagination.

        `offset` skips that many leading records of the filtered set (default
        0). `limit` caps the number returned; when omitted, the
        DEFAULT_PAGE_SIZE applies.

        `sort_by` is accepted for API compatibility but not yet honoured.
        """
        results = self._records

        if where:
            results = [r for r in results
                       if all(k in r and r[k] == v for k, v in where.items())]

        results = results[offset:]

        page_size = DEFAULT_PAGE_SIZE if limit is None else limit
        results = results[:page_size]

        return [copy.deepcopy(r) for r in results]
