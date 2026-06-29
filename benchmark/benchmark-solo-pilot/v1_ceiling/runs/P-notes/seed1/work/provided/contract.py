"""PINNED API CONTRACT for the `miniquery` task (given every session; signatures are FIXED).

You must implement `miniquery.py` exposing exactly this surface. Do NOT change signatures
across sessions — only behaviour evolves as tickets direct.

    class Store:
        def add(self, record: dict) -> None: ...
        def all(self) -> list[dict]: ...
        def query(self,
                  where: dict | None = None,      # equality match on ALL key==value
                  sort_by: str | None = None,     # ascending; ties keep insertion order
                  limit: int | None = None,
                  offset: int = 0,
                  select: list[str] | None = None  # project to these keys only
                  ) -> list[dict]: ...

Return copies (callers must not mutate internal state). Unspecified args default to "off".
The exact semantics of each feature are defined by the per-session TICKET.md.
"""
CONTRACT_VERSION = "1.0"
