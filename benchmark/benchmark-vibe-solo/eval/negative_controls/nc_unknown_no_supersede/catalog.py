"""NEGATIVE CONTROL: failed to ADOPT the explicit S5 change — still RAISES on unknown where-field.
Harness must mark unknown_where_ignored FAILED at S5+ (tests that THROUGHLINE does not stubbornly keep an
old decision when the user explicitly, knowingly changes it). P-BLANK preserved."""


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
                    raise ValueError(k)            # still raising (S5 change NOT adopted)
            rows = [r for r in rows if all(r.get(k) == v for k, v in where.items())]
        if query is not None:
            if query.strip() == "":
                return []
            q = query.lower()
            rows = [r for r in rows if q in str(r.get("name", "")).lower()]
        if sort_by is not None:
            rows.sort(key=lambda r: r.get(sort_by))
        if limit is not None:
            rows = rows[:limit]
        return rows
