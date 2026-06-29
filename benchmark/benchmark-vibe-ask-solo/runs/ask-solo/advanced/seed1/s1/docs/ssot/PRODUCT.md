# PRODUCT

An in-memory **Catalog** of item dicts. Each item is a dict carrying at least a
string `name`; arbitrary additional fields are allowed.

The public API is pinned by `provided/contract.py` (CONTRACT_VERSION 1.0):

- `add(item: dict) -> None`
- `all() -> list[dict]`
- `search(query=None, where=None, sort_by=None, limit=None) -> list[dict]`

Signatures are FIXED across sessions; behaviour evolves per session and is
recorded in DECISIONS.md.

Invariant (from the contract): callers and the catalog never share mutable
references — items are copied in and out, so external mutation cannot corrupt
internal state.
