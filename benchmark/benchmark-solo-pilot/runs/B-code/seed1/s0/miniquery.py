"""Minimal in-memory record store."""


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
        """Return copies of all stored records, in insertion order."""
        return self.all()
