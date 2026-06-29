"""Minimal in-memory record store.

Implements the pinned `Store` API surface from `provided/contract.py`.
Current behaviour: records can be added and read back as copies. `query`
filters records by an optional `where` equality match, optionally sorts the
survivors ascending by a `sort_by` field, then returns them with pagination
via `offset`/`limit`. When `limit` is omitted, a default page size of 40
records applies.
"""

import copy

DEFAULT_PAGE_SIZE = 40


class Store:
    """In-memory store of dict records.

    Records are stored as deep copies on add, and returned as deep copies on
    read, so callers can never mutate internal state.
    """

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
        """Return matching records as copies, paginated.

        `where` keeps only records that match ALL key==value pairs; a key
        absent from a record fails the match for that record (no error). The
        filter is applied first. When `sort_by` is given, the survivors are
        then sorted ascending by that field's value; the sort is stable, so
        records with equal sort keys keep their insertion order. `offset`
        then skips that many leading records (default 0), and `limit` caps the
        number returned; when `limit` is omitted, the default page size of 40
        applies.
        """
        results = self.all()
        if where:
            results = [r for r in results if _matches(r, where)]
        if sort_by is not None:
            results = sorted(results, key=lambda r: r[sort_by])
        results = results[offset:]
        page_size = DEFAULT_PAGE_SIZE if limit is None else limit
        return results[:page_size]


def _matches(record: dict, where: dict) -> bool:
    """True when `record` contains every key in `where` with an equal value."""
    return all(k in record and record[k] == v for k, v in where.items())
