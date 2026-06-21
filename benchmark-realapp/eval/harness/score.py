"""Score an OpsBoard implementation from the hidden E2E check results.

Maps raw checks (run_tests.run_all) to the pre-registered headline metrics
(REALWORLD_DESIGN.md §6): functional / invariants / cross-layer / regression / rework.
Regression and rework are computed across sessions by the Stage-0 driver; this
module scores a single implementation snapshot.
"""
from __future__ import annotations

INVARIANT_KEYS = ["state_machine", "permissions", "existence_hiding", "multi_tenant",
                  "scheduling", "cache_dashboard", "post_approval_edit", "audit_trail"]
WEIGHTS = {"functional": 30, "invariants": 30, "cross_layer": 20}  # regression/rework added by driver


def score_snapshot(checks):
    """checks: list of {invariant, name, passed}. Returns per-group metrics in [0,1]
    plus a weighted snapshot score (functional+invariants+cross_layer only = /80)."""
    by_inv = {}
    for c in checks:
        by_inv.setdefault(c["invariant"], []).append(bool(c["passed"]))

    def rate(keys):
        items = [p for k in keys for p in by_inv.get(k, [])]
        return (sum(items) / len(items)) if items else None

    functional = rate(["functional"])
    invariants = rate(INVARIANT_KEYS)
    cross_layer = rate(["cross_layer"])
    # per-invariant pass rates (diagnostic)
    per_inv = {k: (sum(by_inv.get(k, [])) / len(by_inv[k]) if by_inv.get(k) else None)
               for k in INVARIANT_KEYS}
    inv_violations = sum(1 for k in INVARIANT_KEYS for p in by_inv.get(k, []) if not p)

    weighted = 0.0
    for name, val in (("functional", functional), ("invariants", invariants),
                      ("cross_layer", cross_layer)):
        if val is not None:
            weighted += WEIGHTS[name] * val
    return {
        "functional": functional,
        "invariants": invariants,
        "cross_layer": cross_layer,
        "invariant_violations": inv_violations,
        "per_invariant": per_inv,
        "weighted_80": round(weighted, 2),
        "n_checks": len(checks),
        "n_passed": sum(1 for c in checks if c["passed"]),
    }


def passed_invariant(checks, invariant):
    """True iff every check tagged `invariant` passed (used by the validation gate)."""
    items = [c for c in checks if c["invariant"] == invariant]
    return bool(items) and all(c["passed"] for c in items)
