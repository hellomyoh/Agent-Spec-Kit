"""Minimal in-memory record store."""

DEFAULT_PAGE_SIZE = 7


class Store:
    """An in-memory store of dict records."""

    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        """Store a copy of the record."""
        self._records.append(dict(record))

    def all(self) -> list[dict]:
        """Return copies of all stored records, in insertion order."""
        return [dict(record) for record in self._records]

    def query(self,
              where: dict | None = None,
              sort_by: str | None = None,
              limit: int | None = None,
              offset: int = 0
              ) -> list[dict]:
        """Return a page of stored records, in insertion order.

        ``where`` keeps only records that match ALL given ``key == value``
        pairs; a key absent from a record fails the match for that record.
        Filtering is applied before pagination.

        ``offset`` skips that many leading records. ``limit`` caps how many
        records are returned; when omitted, a default page size of 7 applies.
        """
        results = self.all()

        if where:
            results = [
                record for record in results
                if all(key in record and record[key] == value
                       for key, value in where.items())
            ]

        results = results[offset:]

        page_size = DEFAULT_PAGE_SIZE if limit is None else limit
        return results[:page_size]
