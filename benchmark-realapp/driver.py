"""Stage 0 driver — mechanical workspace setup, snapshot, and scoring.

The ORCHESTRATOR (Claude) calls the dev-agent for each session; this script does
the deterministic plumbing around it:
  prepare <group> <session>  -> build runs/<group>/seed1/work/ for the session,
                                print the memory text to inject into the agent prompt
  score   <group> <session>  -> snapshot work/ -> sNN/, run hidden battery, record metrics
  aggregate                  -> per-session trajectory + regression for all groups

Memory regimes (PREREGISTRATION.md):
  B-limited     : only last N=2 sessions' NOTES injected (older dropped); no notes file in work/
  B-continuing  : all prior tickets+notes concatenated (diagnostic ceiling)
  ASK           : 7 SSOT docs live in work/ssot/, carried + updated every session
"""
from __future__ import annotations
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "eval", "harness"))
from run_tests import run_all          # noqa: E402
from score import score_snapshot, INVARIANT_KEYS  # noqa: E402

N_LIMITED = 2
SSOT_DOCS = ["PRODUCT.md", "DATA_MODEL.md", "API_CONTRACTS.md", "CACHE_POLICY.md",
             "ARCHITECTURE.md", "DECISIONS.md", "PROGRESS.md"]

# per-check active-from session (a feature's checks only count once introduced)
ACTIVE_FROM = {
    "list_projects_scoped": 0, "create_task": 0, "task_listed": 0,
    "list_no_cross_org": 0,
    "update_draft": 1, "mutate_cross_org_404": 1,
    "submit": 2, "approve_admin": 2, "no_draft_to_approved": 2,
    "no_submitted_to_scheduled": 2, "no_approved_to_rejected": 2,
    "no_status_via_update": 2, "approve_cross_org_blocked": 2,
    "member_cannot_approve": 3, "wrong_owner_cannot_approve": 3,
    "right_owner_can_approve": 3, "member_approve_404": 3, "perm_fe_api_consistent": 3,
    "schedule": 4, "schedule_approved_ok": 4, "no_slot_conflict": 4, "other_slot_ok": 4,
    "no_stale_after_create": 5, "no_stale_after_status": 5, "org_scoped_key": 5,
    "fe_dashboard_reflects_create": 5,
    "status_changes_audited": 7, "audit_no_cross_org": 7,
    "search_no_cross_org": 8,
    "title_frozen": 9, "noncore_editable": 9, "freeze_fe_api_consistent": 9,
}


def _g(group):  # path-safe
    return os.path.join(ROOT, "runs", group, "seed1")


def _snap(group, n):
    return os.path.join(_g(group), f"s{n}")


def _work(group):
    return os.path.join(_g(group), "work")


def _copy_code(src, dst):
    """copy *.py the agent authored (not provided/, not eval) + ssot/ if present."""
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(src):
        sp = os.path.join(src, f)
        if f.endswith(".py") and os.path.isfile(sp):
            shutil.copy2(sp, os.path.join(dst, f))
        if f == "ssot" and os.path.isdir(sp):
            shutil.copytree(sp, os.path.join(dst, "ssot"), dirs_exist_ok=True)


def prepare(group, n):
    n = int(n)
    work = _work(group)
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work)
    # provided/ copy so the agent can import + self-test
    shutil.copytree(os.path.join(ROOT, "provided"), os.path.join(work, "provided"))
    # carry forward code from previous snapshot
    if n > 0:
        _copy_code(_snap(group, n - 1), work)
    # current ticket
    shutil.copy2(os.path.join(ROOT, "tickets", f"s{n:02d}.md"), os.path.join(work, "TICKET.md"))

    memory = ""
    if group == "ASK":
        ssot = os.path.join(work, "ssot")
        os.makedirs(ssot, exist_ok=True)
        for d in SSOT_DOCS:
            p = os.path.join(ssot, d)
            if not os.path.exists(p):
                open(p, "w", encoding="utf-8").write(f"# {d[:-3]}\n\n(maintain this across sessions)\n")
        memory = f"Your SSOT docs are in ssot/ ({', '.join(SSOT_DOCS)}). Read them, then UPDATE them this session."
    elif group == "B-limited":
        notes = []
        for k in range(max(0, n - N_LIMITED), n):
            p = os.path.join(_snap(group, k), "NOTES.md")
            if os.path.exists(p):
                notes.append(f"--- notes from session S{k} ---\n" + open(p, encoding="utf-8").read())
        memory = ("\n\n".join(notes) if notes else "(no earlier notes available)")
    elif group == "B-continuing":
        chunks = []
        for k in range(0, n):
            tk = os.path.join(ROOT, "tickets", f"s{k:02d}.md")
            chunks.append(f"=== S{k} TICKET ===\n" + open(tk, encoding="utf-8").read())
            p = os.path.join(_snap(group, k), "NOTES.md")
            if os.path.exists(p):
                chunks.append(f"=== S{k} NOTES ===\n" + open(p, encoding="utf-8").read())
        memory = "\n\n".join(chunks) if chunks else "(this is the first session)"

    open(os.path.join(work, "_MEMORY_FOR_PROMPT.txt"), "w", encoding="utf-8").write(memory)
    print(f"PREPARED {group} S{n} at {work}")
    print(f"---MEMORY-BEGIN---\n{memory}\n---MEMORY-END---")


def score(group, n):
    n = int(n)
    work = _work(group)
    snap = _snap(group, n)
    if os.path.isdir(snap):
        shutil.rmtree(snap)
    os.makedirs(snap)
    # snapshot agent-authored code + memory (exclude provided/)
    for f in os.listdir(work):
        sp = os.path.join(work, f)
        if f == "provided":
            continue
        if os.path.isfile(sp):
            shutil.copy2(sp, os.path.join(snap, f))
        elif os.path.isdir(sp):
            shutil.copytree(sp, os.path.join(snap, f), dirs_exist_ok=True)

    if not os.path.exists(os.path.join(snap, "app.py")):
        rec = {"group": group, "session": n, "chain_dead": True, "reason": "no app.py"}
        _append(group, rec)
        print(json.dumps(rec)); return

    res = run_all(snap)
    active = [c for c in res["checks"] if ACTIVE_FROM.get(c["name"], 99) <= n]
    sc = score_snapshot(active)
    crashed = bool(res["errors"])
    rec = {"group": group, "session": n, "chain_dead": False,
           "n_active": len(active), "n_active_pass": sum(1 for c in active if c["passed"]),
           "functional": sc["functional"], "invariants": sc["invariants"],
           "cross_layer": sc["cross_layer"], "invariant_violations": sc["invariant_violations"],
           "per_invariant": sc["per_invariant"], "errors": res["errors"],
           "checks": {c["name"]: c["passed"] for c in active}}
    _append(group, rec)
    print(f"SCORED {group} S{n}: active {rec['n_active_pass']}/{rec['n_active']} "
          f"func={sc['functional']} inv={sc['invariants']} xlayer={sc['cross_layer']} "
          f"viol={sc['invariant_violations']} crashed={crashed}")


def _append(group, rec):
    p = os.path.join(_g(group), "scores.jsonl")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def aggregate():
    groups = [d for d in os.listdir(os.path.join(ROOT, "runs"))
              if os.path.isdir(os.path.join(ROOT, "runs", d))] if os.path.isdir(os.path.join(ROOT, "runs")) else []
    out = {}
    for g in sorted(groups):
        p = os.path.join(_g(g), "scores.jsonl")
        if not os.path.exists(p):
            continue
        recs = [json.loads(l) for l in open(p, encoding="utf-8")]
        recs = {r["session"]: r for r in recs}  # last wins
        rows, seen_pass = [], {}
        for n in sorted(recs):
            r = recs[n]
            if r.get("chain_dead"):
                rows.append({"S": n, "dead": True}); continue
            regr = sum(1 for name, ok in r["checks"].items() if seen_pass.get(name) and not ok)
            for name, ok in r["checks"].items():
                if ok:
                    seen_pass[name] = True
            rows.append({"S": n, "func": r["functional"], "inv": r["invariants"],
                         "xlayer": r["cross_layer"], "viol": r["invariant_violations"],
                         "regressions": regr})
        out[g] = rows
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prepare":
        prepare(sys.argv[2], sys.argv[3])
    elif cmd == "score":
        score(sys.argv[2], sys.argv[3])
    elif cmd == "aggregate":
        aggregate()
