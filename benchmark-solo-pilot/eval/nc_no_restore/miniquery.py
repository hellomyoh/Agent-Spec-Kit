"""NEGATIVE CONTROL: a memoryless agent at S6 that failed to restore the original default
page size — it left the value at S5's 40 (or reverted only one step). The harness MUST mark
`default_limit` FAILED for this app at S6 (expected 7), else the discriminator is broken."""

DEFAULT_PAGE = 40   # NOT restored to the original S1 value (7)


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
