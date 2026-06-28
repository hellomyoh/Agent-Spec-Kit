"""NEGATIVE CONTROL: blank query DUMPS the whole catalog (P-BLANK violated / S6 drift).
Harness must mark blank_query FAILED at beginner/intermediate S6, but PASSED at advanced S6
(aware override). Unknown where-field ignored (S5 adopted)."""


class Catalog:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(dict(item))

    def all(self):
        return [dict(it) for it in self._items]

    def search(self, query=None, where=None, sort_by=None, limit=None):
        rows = [dict(it) for it in self._items]
        if where:
            for k in where:
                if not any(k in it for it in self._items):
                    return []
            rows = [r for r in rows if all(r.get(k) == v for k, v in where.items())]
        if query is not None:
            q = query.strip().lower()
            if q != "":
                rows = [r for r in rows if q in str(r.get("name", "")).lower()]
            # blank query -> NO filter -> dumps everything (the drift)
        if sort_by is not None:
            rows.sort(key=lambda r: r.get(sort_by))
        if limit is not None:
            rows = rows[:limit]
        return rows
