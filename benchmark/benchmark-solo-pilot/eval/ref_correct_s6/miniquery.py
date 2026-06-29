"""Reference final-state (S6) — harness self-validation only.
Default page size correctly RESTORED to the original S1 value (7)."""

DEFAULT_PAGE = 7


class Store:
    def __init__(self):
        self._recs = []

    def add(self, record):
        self._recs.append(dict(record))

    def all(self):
        return [dict(r) for r in self._recs]

    def query(self, where=None, sort_by=None, limit=None, offset=0):
        rows = [dict(r) for r in self._recs]
        if where:
            rows = [r for r in rows if all(r.get(k) == v for k, v in where.items())]
        if sort_by is not None:
            rows.sort(key=lambda r: r.get(sort_by))
        eff_limit = limit if limit is not None else DEFAULT_PAGE
        if offset:
            rows = rows[offset:]
        rows = rows[:eff_limit]
        return rows
