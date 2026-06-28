# PRODUCT

A small in-memory **Catalog** library: a `Catalog` class holding a collection
of item dicts. Items each have a string `name`. Callers add items and retrieve
them, with `search` evolving over sessions into a filter/sort/limit query API.

The public surface is pinned by `provided/contract.py` (signatures FIXED across
sessions; only behaviour evolves per the per-session user prompts).
