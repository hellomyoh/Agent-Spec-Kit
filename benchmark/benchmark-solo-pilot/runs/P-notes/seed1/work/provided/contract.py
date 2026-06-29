"""PINNED API CONTRACT for the `miniquery` task (given every session; signatures are FIXED).

Implement `miniquery.py` exposing exactly this surface. Do NOT change signatures across
sessions — only behaviour evolves as the per-session TICKET.md directs.

    class Store:
        def add(self, record: dict) -> None: ...
        def all(self) -> list[dict]: ...
        def query(self,
                  where: dict | None = None,     # equality match on ALL key==value
                  sort_by: str | None = None,    # ascending; ties keep insertion order
                  limit: int | None = None,      # explicit cap; if omitted, a DEFAULT page size applies (see tickets)
                  offset: int = 0
                  ) -> list[dict]: ...

Return copies (callers must not mutate internal state). Unspecified args default to "off",
except that an omitted `limit` is governed by the current default page size set by tickets.
"""
CONTRACT_VERSION = "2.0"
