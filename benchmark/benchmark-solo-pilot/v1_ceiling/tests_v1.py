"""Hidden battery for the miniquery task. NEVER copied into an agent workspace.

Each check is behavioural (drives the public API only). active_in() gates a check to
the sessions where it should hold. The decisive memory check is `where_unknown_raises`,
which is set once at S1, retired at S5 (policy flip), and REACTIVATED at S6 (revert):
a memoryless agent at S6 cannot know the pre-S5 behaviour was "raise".
"""
from __future__ import annotations
import importlib.util, os, sys

INVARIANT_CHECKS = {"where_unknown_raises", "where_unknown_empty", "sort_stable"}


def _load(snap):
    path = os.path.join(snap, "miniquery.py")
    spec = importlib.util.spec_from_file_location("miniquery_snap", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["miniquery_snap"] = mod
    spec.loader.exec_module(mod)
    return mod


def c_add_all(m):
    s = m.Store(); s.add({"id": 1, "v": "a"}); s.add({"id": 2, "v": "b"})
    a = s.all()
    return len(a) == 2 and {r["id"] for r in a} == {1, 2}


def c_query_all(m):
    s = m.Store(); s.add({"id": 1}); s.add({"id": 2})
    return len(s.query()) == 2


def c_where_eq(m):
    s = m.Store()
    for i, g in [(1, "x"), (2, "y"), (3, "x")]:
        s.add({"id": i, "g": g})
    return {x["id"] for x in s.query(where={"g": "x"})} == {1, 3}


def c_where_unknown_raises(m):
    s = m.Store(); s.add({"id": 1, "g": "x"})
    try:
        s.query(where={"nope": 1}); return False
    except KeyError:
        return True
    except Exception:
        return False


def c_where_unknown_empty(m):
    s = m.Store(); s.add({"id": 1, "g": "x"})
    try:
        return s.query(where={"nope": 1}) == []
    except Exception:
        return False


def c_sort_stable(m):
    s = m.Store()
    for i, k in [(1, 5), (2, 5), (3, 1), (4, 5)]:
        s.add({"id": i, "k": k})
    return [x["id"] for x in s.query(sort_by="k")] == [3, 1, 2, 4]


def c_limit_offset(m):
    s = m.Store()
    for i in range(5):
        s.add({"id": i, "k": i})
    return [x["id"] for x in s.query(sort_by="k", limit=2, offset=1)] == [1, 2]


def c_select_proj(m):
    s = m.Store(); s.add({"id": 1, "a": 10, "b": 20})
    r = s.query(where={"id": 1}, select=["a"])
    return len(r) == 1 and set(r[0].keys()) == {"a"} and r[0]["a"] == 10


CHECKS = [
    ("add_all", c_add_all), ("query_all", c_query_all), ("where_eq", c_where_eq),
    ("where_unknown_raises", c_where_unknown_raises), ("where_unknown_empty", c_where_unknown_empty),
    ("sort_stable", c_sort_stable), ("limit_offset", c_limit_offset), ("select_proj", c_select_proj),
]


def active_in(name, n):
    table = {
        "add_all": n >= 0,
        "query_all": n >= 0,
        "where_eq": n >= 1,
        "sort_stable": n >= 2,
        "limit_offset": n >= 3,
        "select_proj": n >= 4,
        "where_unknown_raises": (1 <= n <= 4) or (n >= 6),   # decided S1, retired S5, restored S6
        "where_unknown_empty": (n == 5),                     # temporary policy only at S5
    }
    return bool(table.get(name, False))


def run_all(snap):
    out = {"checks": [], "import_error": None}
    try:
        mod = _load(snap)
    except Exception as e:
        out["import_error"] = f"{type(e).__name__}: {e}"
        return out
    for name, fn in CHECKS:
        try:
            ok, err = bool(fn(mod)), None
        except Exception as e:
            ok, err = False, f"{type(e).__name__}: {e}"
        out["checks"].append({"name": name, "passed": ok, "error": err})
    return out
