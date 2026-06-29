"""Harness self-validation (Stage -1 gate) for v2: the battery must (a) pass the reference at
S6 (default page size restored to 7), and (b) catch the negative control that left it at 40."""
import os
from tests import run_all

HERE = os.path.dirname(os.path.abspath(__file__))


def _checks(folder, n):
    res = run_all(os.path.join(HERE, folder), n)
    assert res["import_error"] is None, f"{folder}: {res['import_error']}"
    return {c["name"]: c["passed"] for c in res["checks"]}


def main():
    ref = _checks("ref_correct_s6", 6)
    nc = _checks("nc_no_restore", 6)
    assert ref["default_limit"] is True, ref          # restored 7 -> passes at S6
    for k in ("add_all", "query_all", "explicit_page", "where_eq", "sort_stable"):
        assert ref[k] is True, (k, ref)
    assert nc["default_limit"] is False, nc           # left at 40 -> decisive check fails
    for k in ("add_all", "query_all", "explicit_page", "where_eq", "sort_stable"):
        assert nc[k] is True, (k, nc)                 # capability identical; only the decision differs
    print("SELFTEST OK - battery passes reference S6 (default restored=7) and catches no-restore (40).")
    print("  ref:", ref)
    print("  nc :", nc)


if __name__ == "__main__":
    main()
