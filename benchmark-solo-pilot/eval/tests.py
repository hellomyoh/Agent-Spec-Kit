"""Hidden battery for the miniquery task (v2 — value-restoration discriminator).

NEVER copied into an agent workspace.

The decisive memory check is `default_limit`: the default page size is an ARBITRARY
product value set once at S1 (=7), changed at S3 (->25) and again at S5 (->40), and at S6
the ticket asks to restore the ORIGINAL S1 value. Because the original is overwritten twice,
it is no longer present in the current code at S6 — only durable memory holds "7".
Each check takes (module, session_n); most ignore n.
"""
from __future__ import annotations
import importlib.util, os, sys

INVARIANT_CHECKS = {"default_limit", "sort_stable"}

# expected default page size (limit omitted) per session — the drift target
DEFAULT_BY_SESSION = {1: 7, 2: 7, 3: 25, 4: 25, 5: 40, 6: 7}


def _load(snap):
    path = os.path.join(snap, "miniquery.py")
    spec = importlib.util.spec_from_file_location("miniquery_snap", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["miniquery_snap"] = mod
    spec.loader.exec_module(mod)
    return mod


def c_add_all(m, n):
    s = m.Store(); s.add({"id": 1, "v": "a"}); s.add({"id": 2, "v": "b"})
    a = s.all()
    return len(a) == 2 and {r["id"] for r in a} == {1, 2}


def c_query_all(m, n):
    # small dataset (under any default page size) -> query() returns everything
    s = m.Store(); s.add({"id": 1}); s.add({"id": 2})
    return len(s.query()) == 2


def c_explicit_page(m, n):
    # explicit limit/offset overrides the default page size
    s = m.Store()
    for i in range(5):
        s.add({"id": i})
    return [x["id"] for x in s.query(sort_by="id", limit=2, offset=1)] == [1, 2]


def c_default_limit(m, n):
    # DECISIVE: query() with no limit returns at most the session's default page size
    exp = DEFAULT_BY_SESSION.get(n)
    if exp is None:
        return False
    s = m.Store()
    for i in range(80):
        s.add({"id": i})
    return len(s.query()) == exp


def c_where_eq(m, n):
    s = m.Store()
    for i, g in [(1, "x"), (2, "y"), (3, "x")]:
        s.add({"id": i, "g": g})
    return {x["id"] for x in s.query(where={"g": "x"})} == {1, 3}


def c_sort_stable(m, n):
    s = m.Store()
    for i, k in [(1, 5), (2, 5), (3, 1), (4, 5)]:
        s.add({"id": i, "k": k})
    return [x["id"] for x in s.query(sort_by="k")] == [3, 1, 2, 4]


CHECKS = [
    ("add_all", c_add_all), ("query_all", c_query_all), ("explicit_page", c_explicit_page),
    ("default_limit", c_default_limit), ("where_eq", c_where_eq), ("sort_stable", c_sort_stable),
]


def active_in(name, n):
    table = {
        "add_all": n >= 0,
        "query_all": n >= 0,
        "explicit_page": n >= 1,
        "default_limit": n >= 1,     # value differs by session (DEFAULT_BY_SESSION)
        "where_eq": n >= 2,
        "sort_stable": n >= 4,
    }
    return bool(table.get(name, False))


def run_all(snap, n):
    out = {"checks": [], "import_error": None}
    try:
        mod = _load(snap)
    except Exception as e:
        out["import_error"] = f"{type(e).__name__}: {e}"
        return out
    for name, fn in CHECKS:
        try:
            ok, err = bool(fn(mod, n)), None
        except Exception as e:
            ok, err = False, f"{type(e).__name__}: {e}"
        out["checks"].append({"name": name, "passed": ok, "error": err})
    return out
