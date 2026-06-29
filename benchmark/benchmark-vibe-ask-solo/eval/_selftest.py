"""Stage -1 gate: validate the hidden battery + the LEVEL-AWARE S6 oracle before any agent runs.

Confirms:
  - reference (S5+ canonical) passes all active checks at S5 and at beginner S6
  - the SAME preserve-reference FAILS blank_query at advanced S6 (aware override expected) -> level-aware oracle works
  - nc_blank_dumps (drift) FAILS blank_query at beginner S6 but PASSES at advanced S6
  - nc_unknown_no_supersede FAILS unknown_where_ignored at S5 (must adopt explicit change)
"""
import os
from tests import run_all, active_in

HERE = os.path.dirname(os.path.abspath(__file__))


def checks(folder, level, n):
    res = run_all(os.path.join(HERE, folder), level, n)
    assert res["import_error"] is None, f"{folder}: import_error {res['import_error']}"
    return {c["name"]: c["passed"] for c in res["checks"] if active_in(c["name"], n)}


def all_pass(d):
    return all(d.values())


def main():
    # reference at S5 (any level) — full canonical behaviour
    r5 = checks("ref_correct", "beginner", 5)
    assert all_pass(r5), ("ref S5 should pass all", r5)

    # reference at beginner S6: P-BLANK preserved is CORRECT
    rb6 = checks("ref_correct", "beginner", 6)
    assert all_pass(rb6), ("ref beginner S6 should pass all", rb6)

    # SAME reference at advanced S6: advanced expects aware override (blank->all) -> must FAIL
    ra6 = checks("ref_correct", "advanced", 6)
    assert ra6["blank_query"] is False, ("ref advanced S6 blank_query should FAIL (level-aware)", ra6)

    # nc_blank_dumps: drift caught at beginner S6, but correct at advanced S6
    nb6 = checks("negative_controls/nc_blank_dumps", "beginner", 6)
    assert nb6["blank_query"] is False, ("nc_blank_dumps beginner S6 should FAIL", nb6)
    na6 = checks("negative_controls/nc_blank_dumps", "advanced", 6)
    assert na6["blank_query"] is True, ("nc_blank_dumps advanced S6 should PASS", na6)

    # nc_unknown_no_supersede: failed to adopt explicit S5 change
    nu5 = checks("negative_controls/nc_unknown_no_supersede", "beginner", 5)
    assert nu5["unknown_where_ignored"] is False, ("nc_unknown_no_supersede S5 should FAIL", nu5)

    print("SELFTEST OK - hidden battery + level-aware S6 oracle validated.")
    print("  ref S5            :", r5)
    print("  ref beginner  S6  :", rb6)
    print("  ref advanced  S6  : blank_query =", ra6["blank_query"], "(expected False)")
    print("  nc_dumps  beg S6  : blank_query =", nb6["blank_query"], "(expected False)")
    print("  nc_dumps  adv S6  : blank_query =", na6["blank_query"], "(expected True)")
    print("  nc_no_supersede S5: unknown_where_ignored =", nu5["unknown_where_ignored"], "(expected False)")


if __name__ == "__main__":
    main()
