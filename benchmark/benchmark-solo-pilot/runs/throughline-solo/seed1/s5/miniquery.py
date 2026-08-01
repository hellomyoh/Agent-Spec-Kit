"""miniquery — an in-memory record store.

Implements the `Store` class per provided/contract.py. Records are plain dicts;
the store keeps an internal copy of each and hands back copies so callers cannot
mutate its state.
"""

import copy

DEFAULT_PAGE_SIZE = 40


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
        """Return stored records (copies) with filter, sort, and paging.

        The pipeline is filter, then sort, then page:

        - `where` keeps only records that match every `key == value` pair; a key
          absent from a record fails the match for that record.
        - `sort_by` sorts the surviving records ascending by that field's value.
          The sort is stable, so records with equal sort keys keep their
          insertion order. Records that have the field are ordered by value
          first; records missing the field are grouped together after them, in
          insertion order (the missing case is segregated so it never has to be
          compared against a present value).
        - `offset` then skips that many leading records and `limit` caps how many
          are returned (the default page size applies when `limit` is omitted).
        """
        results = self.all()
        if where is not None:
            results = [r for r in results if self._matches(r, where)]
        if sort_by is not None:
            results.sort(key=lambda r: (sort_by not in r, r.get(sort_by)))
        page_size = DEFAULT_PAGE_SIZE if limit is None else limit
        return results[offset:offset + page_size]

    @staticmethod
    def _matches(record: dict, where: dict) -> bool:
        """True when `record` contains every `where` key with an equal value."""
        return all(key in record and record[key] == value for key, value in where.items())
