#!/usr/bin/env python3
"""M-pilot scorer. Differential vs oracle on two per-op visitors: evaluate, to_rpn.
A solution is a package `exprkit` exposing evaluate(s) and to_rpn(s).
Measures per session: F2P(new ops), P2P(prior ops = cross-module regression),
cross-cutting omissions (op works in one visitor but not the other)."""
import os, sys, importlib, statistics as st
import oracle

NEW_OPS = {0: ["+", "-"], 1: ["*", "/"], 2: ["neg"], 3: ["pow"], 4: ["lt", "gt", "eq"]}
SESSION_OPS = {n: sum((NEW_OPS[k] for k in range(n + 1)), []) for n in range(5)}
MINEX = {"+": "(+ 3 4)", "-": "(- 10 3)", "*": "(* 6 7)", "/": "(/ 7 2)", "neg": "(neg 5)",
         "pow": "(pow 2 5)", "lt": "(lt 3 4)", "gt": "(gt 9 2)", "eq": "(eq 4 4)"}
# nested expressions (op -> a compound expression exercising it together with others)
NESTED = {"-": "(- (+ 1 2) (+ 3 4))", "/": "(/ (* 6 4) (+ 1 2))", "neg": "(neg (- 2 9))",
          "pow": "(pow (+ 1 1) (- 4 1))", "eq": "(eq (* 2 3) (+ 5 1))"}

def _load_pkg(pkg_dir):
    """Import the solution package `exprkit` from pkg_dir; return module or raise."""
    for m in [k for k in list(sys.modules) if k == "exprkit" or k.startswith("exprkit.")]:
        del sys.modules[m]
    sys.path.insert(0, pkg_dir)
    try:
        mod = importlib.import_module("exprkit")
        importlib.reload(mod)
        return mod
    finally:
        sys.path.pop(0)

def _check_op(sol, expr):
    """Return (eval_ok, rpn_ok) comparing solution to oracle on expr."""
    try:
        eo = oracle.evaluate(expr)
        ev_ok = (sol.evaluate(expr) == eo)
    except Exception:
        ev_ok = False
    try:
        ro = oracle.to_rpn(expr)
        rpn_ok = (sol.to_rpn(expr) == ro)
    except Exception:
        rpn_ok = False
    return ev_ok, rpn_ok

def score_session(pkg_dir, step):
    out = {"step": step, "import_error": None}
    try:
        sol = _load_pkg(pkg_dir)
        assert hasattr(sol, "evaluate") and hasattr(sol, "to_rpn")
    except Exception as e:
        return {**out, "import_error": f"{type(e).__name__}: {str(e)[:120]}",
                "f2p": 0.0, "p2p_regression": 1.0, "cross_cut_omissions": None,
                "ops_full": 0, "ops_total": len(SESSION_OPS[step])}
    results = {}  # op -> (ev_ok, rpn_ok)
    for op in SESSION_OPS[step]:
        ev1, rp1 = _check_op(sol, MINEX[op])
        if op in NESTED:  # also require the nested form (regression robustness)
            ev2, rp2 = _check_op(sol, NESTED[op])
            ev1, rp1 = (ev1 and ev2), (rp1 and rp2)
        results[op] = (ev1, rp1)
    full = {op for op, (e, r) in results.items() if e and r}
    new = NEW_OPS[step]
    prior = SESSION_OPS[step - 1] if step > 0 else []
    f2p = sum(1 for op in new if op in full) / len(new)
    p2p_fail = [op for op in prior if op not in full]
    p2p_reg = (len(p2p_fail) / len(prior)) if prior else 0.0
    omissions = [op for op, (e, r) in results.items() if e != r]  # works in one visitor only
    return {**out, "f2p": round(f2p, 3), "p2p_regression": round(p2p_reg, 3),
            "p2p_fail_ops": p2p_fail, "cross_cut_omissions": omissions,
            "ops_full": len(full), "ops_total": len(SESSION_OPS[step]),
            "floor_div_ok": (("/" in full) if step >= 1 else None)}

if __name__ == "__main__":
    # Validation: oracle itself must satisfy every session fully (sanity of test sets).
    print("=== oracle self-check (should be all-pass) ===")
    for step in range(5):
        bad = []
        for op in SESSION_OPS[step]:
            try:
                oracle.evaluate(MINEX[op]); oracle.to_rpn(MINEX[op])
            except Exception as e:
                bad.append(f"{op}:{e}")
        print(f"  S{step}: ops={SESSION_OPS[step]} bad={bad or 'none'}")
    # negative control: a package missing 'neg' in to_rpn should show an omission
    print("oracle.evaluate('(/ 7 2)') =", oracle.evaluate("(/ 7 2)"), "(floor-div decision)")
    print("oracle.to_rpn('(neg (+ 1 2))') =", oracle.to_rpn("(neg (+ 1 2))"))
