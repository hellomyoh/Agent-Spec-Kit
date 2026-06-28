"""miniquery — a tiny in-memory record store.

Implements the pinned `Store` API from `provided/contract.py`.
"""

import copy

# Page size applied when `query()` is called without an explicit `limit`.
DEFAULT_PAGE_SIZE = 7


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
        """Return stored records (copies), filtered, sorted, then paginated.

        `where` keeps only records matching ALL key==value pairs (AND
        semantics); a key absent from a record fails the match for that record.

        `sort_by` sorts the filtered records ascending by that field's value.
        The sort is stable, so records with equal sort keys keep their
        insertion order.

        `offset` skips that many leading records of the filtered/sorted set
        (default 0). `limit` caps the number returned; when omitted, the
        DEFAULT_PAGE_SIZE applies.

        The pipeline is: filter -> sort -> offset -> limit.
        """
        results = self._records

        if where:
            results = [r for r in results
                       if all(k in r and r[k] == v for k, v in where.items())]

        if sort_by is not None:
            results = sorted(results, key=lambda r: r[sort_by])

        results = results[offset:]

        page_size = DEFAULT_PAGE_SIZE if limit is None else limit
        results = results[:page_size]

        return [copy.deepcopy(r) for r in results]
