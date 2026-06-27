"""Stage -1 validation gate (REALWORLD_DESIGN.md §11).

PASS requires ALL of:
  (1) reference passes every hidden check (0 invariant violations);
  (2) each negative control FAILS its targeted invariant (checker detects the break);
  (3) every targeted invariant is observable through the public surface
      (i.e., the break manifests as a behavioural check failure, not a structural one);
  (4) isolation structural check: eval-only artifacts live outside the agent workspace.

If this gate fails, Stage 0 is forbidden.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from run_tests import run_all          # noqa: E402
from score import passed_invariant, score_snapshot, INVARIANT_KEYS  # noqa: E402

REF = os.path.join(ROOT, "eval", "reference")
NC_DIR = os.path.join(ROOT, "eval", "negative_controls")


def main():
    fails = []

    # (1) reference passes all
    ref = run_all(REF)
    ref_score = score_snapshot(ref["checks"])
    ref_ok = ref_score["invariant_violations"] == 0 and not ref["errors"] \
        and ref_score["functional"] == 1.0 and ref_score["cross_layer"] == 1.0
    print(f"[1] reference: {ref_score['n_passed']}/{ref_score['n_checks']} checks, "
          f"violations={ref_score['invariant_violations']}, errors={len(ref['errors'])} "
          f"-> {'OK' if ref_ok else 'FAIL'}")
    if not ref_ok:
        fails.append("reference did not pass all checks")
        for e in ref["errors"]:
            print("    ref error:", e)
        for c in ref["checks"]:
            if not c["passed"]:
                print("    ref FAIL:", c["invariant"], c["name"], c["detail"])

    # (2)+(3) each negative control fails its target invariant (behaviourally);
    #         also report which invariants each NC breaks (I5 confinement) and which
    #         invariants are caught by exactly one NC (independent checker validation).
    manifest = json.load(open(os.path.join(NC_DIR, "manifest.json")))
    print(f"\n[2] negative controls ({len(manifest)}):")
    broke_by_invariant = {}
    for name, target in sorted(manifest.items()):
        res = run_all(os.path.join(NC_DIR, name))
        broken = sorted({c["invariant"] for c in res["checks"] if not c["passed"]})
        caught = target in broken
        for inv in broken:
            broke_by_invariant.setdefault(inv, []).append(name)
        status = "OK" if caught else "FAIL (slipped)"
        extra = [b for b in broken if b not in (target, "cross_layer")]
        print(f"    {name:24s} target={target:18s} breaks={broken} -> {status}"
              + (f"   (collateral: {extra})" if extra else ""))
        if not caught:
            fails.append(f"{name}: break in {target} NOT detected by checker")

    # (3b) every oracle invariant must be broken by >=1 control (checker is validated)
    print("\n[2b] per-invariant checker validation:")
    for inv in INVARIANT_KEYS:
        controls = broke_by_invariant.get(inv, [])
        print(f"    {inv:18s} broken by: {controls or 'NONE'}")
        if not controls:
            fails.append(f"invariant {inv} has no negative control that breaks it")

    # (4) isolation structural check
    print("\n[3] isolation structural check:")
    agent_visible = []
    for sub in ("provided", "tickets"):
        d = os.path.join(ROOT, sub)
        if os.path.isdir(d):
            agent_visible += [os.path.join(sub, f) for f in os.listdir(d)]
    leak_terms = ("oracle", "negative_control", "reference", "run_tests", "score", "invariants")
    leaks = [f for f in agent_visible if any(t in f.lower() for t in leak_terms)]
    eval_outside = os.path.isdir(os.path.join(ROOT, "eval"))
    iso_ok = not leaks and eval_outside
    print(f"    agent-visible dirs = provided/, tickets/ ; eval-only under eval/ = {eval_outside}")
    print(f"    leak terms found in agent-visible files: {leaks or 'none'} -> {'OK' if iso_ok else 'FAIL'}")
    if not iso_ok:
        fails.append("isolation structural check failed")

    print("\n" + "=" * 60)
    if fails:
        print("STAGE -1 GATE: FAIL")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("STAGE -1 GATE: PASS — Stage 0 permitted.")


if __name__ == "__main__":
    main()
