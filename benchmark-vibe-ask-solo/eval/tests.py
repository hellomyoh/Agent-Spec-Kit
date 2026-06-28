"""Hidden battery for the `catalog` task. NEVER copied into an agent workspace (oracle isolation).

Behavioural checks driven through the public API only. Each check takes (module, level, session_n).
The only level-aware check is `blank_query` at S6 (the forgetting-drift conflict — see
eval/oracle/policies.md).

ORACLE NON-LEAKAGE: checks return only pass/fail; on exception we keep the exception TYPE name only,
never the expected value. `public_summary()` exposes failing check NAMES only — safe to surface.
"""
from __future__ import annotations
import importlib.util, os, sys

INVARIANT_CHECKS = {"unknown_where_raises", "unknown_where_ignored", "blank_query", "sort_stable"}
LEVELS = ("beginner", "intermediate", "advanced")


def _load(snap):
    path = os.path.join(snap, "catalog.py")
    spec = importlib.util.spec_from_file_location("catalog_snap", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["catalog_snap"] = mod
    spec.loader.exec_module(mod)
    return mod


def _cat(m, items):
    c = m.Catalog()
    for it in items:
        c.add(it)
    return c


FRUITS = [{"name": "Apple", "cat": "fruit"}, {"name": "Banana", "cat": "fruit"}, {"name": "Grape", "cat": "fruit"}]


def expected_blank(level, n):
    """'empty' (P-BLANK holds) or 'all' (aware override at advanced S6)."""
    if n == 6 and level == "advanced":
        return "all"
    return "empty"


def c_add_all(m, level, n):
    c = _cat(m, [{"name": "A"}, {"name": "B"}])
    a = c.all()
    return len(a) == 2 and {r["name"] for r in a} == {"A", "B"}


def c_search_none_all(m, level, n):
    c = _cat(m, FRUITS)                       # query=None => list mode => all
    return len(c.search()) == 3


def c_query_substring(m, level, n):
    c = _cat(m, FRUITS)                        # case-insensitive substring on name
    return [r["name"] for r in c.search(query="an")] == ["Banana"]


def c_where_eq(m, level, n):
    c = _cat(m, FRUITS + [{"name": "Bolt", "cat": "tool"}])
    return {r["name"] for r in c.search(where={"cat": "tool"})} == {"Bolt"}


def c_unknown_where_raises(m, level, n):
    c = _cat(m, FRUITS)
    try:
        c.search(where={"nope": 1}); return False
    except ValueError:
        return True
    except Exception:
        return False


def c_unknown_where_ignored(m, level, n):
    c = _cat(m, FRUITS)
    try:
        return c.search(where={"nope": 1}) == []
    except Exception:
        return False


def c_sort_stable(m, level, n):
    items = [{"name": "x", "k": 5}, {"name": "y", "k": 5}, {"name": "z", "k": 1}, {"name": "w", "k": 5}]
    c = _cat(m, items)
    return [r["name"] for r in c.search(sort_by="k")] == ["z", "x", "y", "w"]


def c_blank_query(m, level, n):
    c = _cat(m, FRUITS)
    exp = expected_blank(level, n)
    try:
        r1, r2 = c.search(query=""), c.search(query="   ")
    except Exception:
        return False
    if exp == "empty":
        return r1 == [] and r2 == []
    return len(r1) == 3 and len(r2) == 3       # advanced S6 aware override: blank -> all


def c_limit_caps(m, level, n):
    c = _cat(m, [{"name": n_} for n_ in "abcde"])
    return len(c.search(limit=2)) == 2


CHECKS = [
    ("add_all", c_add_all), ("search_none_all", c_search_none_all), ("query_substring", c_query_substring),
    ("where_eq", c_where_eq), ("unknown_where_raises", c_unknown_where_raises),
    ("unknown_where_ignored", c_unknown_where_ignored), ("sort_stable", c_sort_stable),
    ("blank_query", c_blank_query), ("limit_caps", c_limit_caps),
]


def active_in(name, n):
    table = {
        "add_all": n >= 0, "search_none_all": n >= 0,
        "query_substring": n >= 1,
        "where_eq": n >= 2,
        "unknown_where_raises": 2 <= n <= 4,
        "unknown_where_ignored": n >= 5,
        "sort_stable": n >= 3,
        "blank_query": n >= 3,
        "limit_caps": n >= 4,
    }
    return bool(table.get(name, False))


def run_all(snap, level, n):
    out = {"checks": [], "import_error": None}
    try:
        mod = _load(snap)
    except Exception as e:
        out["import_error"] = type(e).__name__           # type only, no message (no oracle leak)
        return out
    for name, fn in CHECKS:
        try:
            ok, err = bool(fn(mod, level, n)), None
        except Exception as e:
            ok, err = False, type(e).__name__             # type only
        out["checks"].append({"name": name, "passed": ok, "error": err})
    return out


def public_summary(run_result, n, level):
    """Safe-to-surface QA summary: names of FAILING active checks only (no expected values)."""
    if run_result["import_error"]:
        return {"import_error": True, "failing": []}
    failing = [c["name"] for c in run_result["checks"] if active_in(c["name"], n) and not c["passed"]]
    return {"import_error": False, "failing": failing}
