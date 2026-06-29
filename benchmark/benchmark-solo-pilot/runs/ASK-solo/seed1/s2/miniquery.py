"""miniquery — an in-memory record store.

Implements the `Store` class per provided/contract.py. Records are plain dicts;
the store keeps an internal copy of each and hands back copies so callers cannot
mutate its state.
"""

import copy

DEFAULT_PAGE_SIZE = 7


class Store:
    """In-memory collection of dict records, preserving insertion order."""

    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        """Store a copy of `record`."""
        self._records.append(copy.deepcopy(record))

    def all(self) -> list[dict]:
        """Return copies of all stored records, in insertion order."""
        return [copy.deepcopy(record) for record in self._records]

    def query(
        self,
        where: dict | None = None,
        sort_by: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[dict]:
        """Return stored records (copies) in insertion order, with filter and paging.

        `where` keeps only records that match every `key == value` pair; a key
        absent from a record fails the match for that record. Filtering is applied
        first, then paging: `offset` skips that many leading matches and `limit`
        caps how many are returned (the default page size applies when `limit` is
        omitted).

        `sort_by` is part of the pinned contract signature but is not yet
        interpreted.
        """
        results = self.all()
        if where is not None:
            results = [r for r in results if self._matches(r, where)]
        page_size = DEFAULT_PAGE_SIZE if limit is None else limit
        return results[offset:offset + page_size]

    @staticmethod
    def _matches(record: dict, where: dict) -> bool:
        """True when `record` contains every `where` key with an equal value."""
        return all(key in record and record[key] == value for key, value in where.items())
