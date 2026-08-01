"""PINNED API CONTRACT for the `catalog` task (given to the agent every session).

Implement `catalog.py` exposing exactly this surface. Signatures are FIXED across sessions;
only BEHAVIOUR evolves as the per-session user prompt directs. The exact semantics of each
feature/policy are NOT specified here — they are introduced by the user prompts over the
sessions, and (for throughline-solo) recorded in your SSOT docs.

    class Catalog:
        def add(self, item: dict) -> None: ...
        def all(self) -> list[dict]: ...
        def search(self,
                   query: str | None = None,   # text filter on item 'name'
                   where: dict | None = None,   # equality filter on item fields
                   sort_by: str | None = None,  # ordering field
                   limit: int | None = None,    # max results
                   ) -> list[dict]: ...

Notes the contract DOES fix (so tests are stable):
- Items are dicts; every item has a string 'name'.
- `search` returns a list of item dicts (copies; callers must not mutate internal state).
- `query=None` means "no text filter" (list mode). A non-None `query` is a text search whose
  precise behaviour (matching, blank handling) is defined by the user prompts.
"""
CONTRACT_VERSION = "1.0"
