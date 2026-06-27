#!/usr/bin/env python3
"""Revert/restoration-cycle scorer (benchmark item B3).
Steps: 0=Base, 1=R1, 2=R2, 3=Revert->R1. Expected policy per step below.
core = invariants (P2P, all policies). policy = step-specific behavior.
Restoration fidelity = policy pass-rate at step 3 (must recall R1, not visible in current R2 code)."""
import os, json, importlib.util
STEP_POLICY = {0: "base", 1: "R1", 2: "R2", 3: "R1"}

def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def _run(checks, sol):
    p, fails = 0, []
    for nm, fn in checks:
        try:
            fn(sol); p += 1
        except Exception as e:
            fails.append(f"{nm}: {type(e).__name__}: {str(e)[:80]}")
    return p, len(checks), fails

def score_revert(track_dir, sol_path, step):
    T = _load(f"{track_dir}/tests.py", "tests_" + os.path.basename(track_dir))
    base = {"step": step, "policy_expected": STEP_POLICY[step]}
    if not os.path.exists(sol_path):
        return {**base, "import_error": "missing", "core_pass": 0, "core_total": 0,
                "policy_pass": 0, "policy_total": 0, "r2_residue": None, "fails": ["missing"]}
    try:
        sol = _load(sol_path, "solution")
    except Exception as e:
        return {**base, "import_error": f"{type(e).__name__}: {str(e)[:120]}", "core_pass": 0,
                "core_total": 0, "policy_pass": 0, "policy_total": 0, "r2_residue": None, "fails": []}
    cp, ct, cf = _run(T.get_core(), sol)
    pp, pt, pf = _run(T.get_policy(STEP_POLICY[step]), sol)
    r2_residue = None
    if step == 3:
        # after reverting to R1, the R2 policy must NOT hold. If R2 still passes -> R2 not removed (residue).
        r2p, r2t, _ = _run(T.get_policy("R2"), sol)
        r2_residue = (r2p == r2t)
    return {**base, "import_error": None, "core_pass": cp, "core_total": ct,
            "policy_pass": pp, "policy_total": pt,
            "policy_fidelity": round(pp / pt, 4) if pt else 0.0,
            "core_regression": round((ct - cp) / ct, 4) if ct else 0.0,
            "r2_residue": r2_residue, "fails": (cf + pf)[:4]}

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    ok = True
    for tr in ("rank", "clean_tags"):
        td = f"{root}/tracks/{tr}"
        T = _load(f"{td}/tests.py", "t")
        for refpol in ("base", "R1", "R2"):
            sol = _load(f"{td}/ref_{refpol}.py", f"ref_{tr}_{refpol}")
            cp, ct, cf = _run(T.get_core(), sol)
            own_p, own_t, _ = _run(T.get_policy(refpol), sol)
            others = {o: _run(T.get_policy(o), sol)[0] for o in ("base", "R1", "R2") if o != refpol}
            # valid iff: core all pass, own policy all pass, OTHER policies do NOT fully pass (discriminating)
            disc = all(v < own_t for v in others.values())
            status = "OK" if (cp == ct and own_p == own_t and disc) else "FAIL"
            if status != "OK":
                ok = False
            print(f"{tr:11s} ref={refpol:4s}: {status}  core {cp}/{ct}  own {own_p}/{own_t}  others_pass {others}")
            if cf: print("   core fails:", cf)
    print("ALL REFERENCES VALID & POLICIES DISCRIMINATE" if ok else "VALIDATION FAILED")
