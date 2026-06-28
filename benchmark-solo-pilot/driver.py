"""ASK-solo DriftBench — Stage-1 M-only pilot driver (compact `miniquery` task).

Orchestrator model (same as benchmark-realapp): the ORCHESTRATOR (Claude) calls a
fresh dev-agent per session; this script does the deterministic plumbing:

  prepare <group> <session>  -> build runs/<group>/seed<seed>/work/ for the session,
                                inject the group's memory artifact, print it
  score   <group> <session>  -> snapshot work/ -> sNN/, run hidden battery (active checks),
                                record metrics to scores.jsonl
  aggregate                  -> per-session trajectory + cumulative regression per group

Groups (review §6.2 / §6.2.1):
  B-code      : fresh agent, current code + ticket ONLY (no memory).  [floor / B-code pre-check]
  B-limited   : last N=2 sessions' NOTES, each capped to K_B chars (lossy memory).
  P-notes     : ALL prior NOTES concatenated, capped to K_P chars (~ASK SSOT budget) (record control).
  ASK-solo    : SSOT docs in work/ssot/, carried + updated every session (structured SSOT).

Single manipulated variable = the memory regime. SEED via env SEED (default seed1).
"""
from __future__ import annotations
import json, os, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "eval"))
from tests import run_all, active_in, INVARIANT_CHECKS  # noqa: E402

SEED = os.environ.get("SEED", "seed1")
N_LIMITED = 2
K_B = 600     # B-limited: hard char cap per carried session note (lossy)
K_P = 2600    # P-notes: total carried-notes char cap (~matched to ASK SSOT size; logged each session)
SSOT_DOCS = ["PRODUCT.md", "DECISIONS.md", "DATA_MODEL.md", "PROGRESS.md"]
MODULE = "miniquery.py"
NSESSIONS = 7  # s0..s6


def _g(group):
    return os.path.join(ROOT, "runs", group, SEED)


def _snap(group, n):
    return os.path.join(_g(group), f"s{n}")


def _work(group):
    return os.path.join(_g(group), "work")


def _copy_code(src, dst):
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(src):
        sp = os.path.join(src, f)
        if f.endswith(".py") and os.path.isfile(sp):
            shutil.copy2(sp, os.path.join(dst, f))
        if f == "ssot" and os.path.isdir(sp):
            shutil.copytree(sp, os.path.join(dst, "ssot"), dirs_exist_ok=True)


def _ssot_chars(group, n):
    """total chars of ASK SSOT at the previous snapshot (for P-notes budget matching/logging)."""
    d = os.path.join(_snap("ASK-solo", n - 1), "ssot") if n > 0 else None
    if not d or not os.path.isdir(d):
        return None
    return sum(len(open(os.path.join(d, f), encoding="utf-8").read())
               for f in os.listdir(d) if f.endswith(".md"))


def prepare(group, n):
    n = int(n)
    work = _work(group)
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work)
    shutil.copytree(os.path.join(ROOT, "provided"), os.path.join(work, "provided"))
    if n > 0:
        _copy_code(_snap(group, n - 1), work)
    shutil.copy2(os.path.join(ROOT, "tickets", f"s{n:02d}.md"), os.path.join(work, "TICKET.md"))

    memory, budget_note = "", ""
    if group == "ASK-solo":
        ssot = os.path.join(work, "ssot")
        os.makedirs(ssot, exist_ok=True)
        for d in SSOT_DOCS:
            p = os.path.join(ssot, d)
            if not os.path.exists(p):
                open(p, "w", encoding="utf-8").write(f"# {d[:-3]}\n\n(maintain this SSOT doc across sessions)\n")
        memory = (f"Your SSOT docs live in ssot/ ({', '.join(SSOT_DOCS)}). "
                  "READ them first, then UPDATE them this session (record durable decisions in DECISIONS.md).")
    elif group == "B-limited":
        notes = []
        for k in range(max(0, n - N_LIMITED), n):
            p = os.path.join(_snap(group, k), "NOTES.md")
            if os.path.exists(p):
                txt = open(p, encoding="utf-8").read()[:K_B]
                notes.append(f"--- notes from session S{k} (capped {K_B} chars) ---\n{txt}")
        memory = "\n\n".join(notes) if notes else "(no earlier notes available)"
        memory += "\n\n(Write a short NOTES.md this session; only the last 2 sessions' notes survive, capped.)"
    elif group == "P-notes":
        chunks = []
        for k in range(0, n):
            p = os.path.join(_snap(group, k), "NOTES.md")
            if os.path.exists(p):
                chunks.append(f"=== S{k} NOTES ===\n" + open(p, encoding="utf-8").read())
        full = "\n\n".join(chunks)
        capped = full[-K_P:] if len(full) > K_P else full   # keep most recent within budget
        ask_chars = _ssot_chars(group, n)
        budget_note = f"[budget] P-notes carried chars={len(capped)} (cap {K_P}); ASK SSOT chars(prev)={ask_chars}"
        memory = (capped if capped else "(this is the first session)")
        memory += f"\n\n(Maintain a free-form NOTES.md; carried notes are capped to ~{K_P} chars.)"
    # B-code: no memory

    open(os.path.join(work, "_MEMORY_FOR_PROMPT.txt"), "w", encoding="utf-8").write(memory)
    print(f"PREPARED {group} {SEED} S{n} at {work}")
    if budget_note:
        print(budget_note)
    print(f"---MEMORY-BEGIN---\n{memory}\n---MEMORY-END---")


def score(group, n):
    n = int(n)
    work = _work(group)
    snap = _snap(group, n)
    if os.path.isdir(snap):
        shutil.rmtree(snap)
    os.makedirs(snap)
    for f in os.listdir(work):
        sp = os.path.join(work, f)
        if f == "provided":
            continue
        if os.path.isfile(sp):
            shutil.copy2(sp, os.path.join(snap, f))
        elif os.path.isdir(sp):
            shutil.copytree(sp, os.path.join(snap, f), dirs_exist_ok=True)

    if not os.path.exists(os.path.join(snap, MODULE)):
        rec = {"group": group, "seed": SEED, "session": n, "chain_dead": True, "reason": f"no {MODULE}"}
        _append(group, rec); print(json.dumps(rec)); return

    res = run_all(snap, n)                     # {checks:[{name,passed,error}], import_error}
    active = [c for c in res["checks"] if active_in(c["name"], n)]
    n_pass = sum(1 for c in active if c["passed"])
    inv_active = [c for c in active if c["name"] in INVARIANT_CHECKS]
    inv_viol = sum(1 for c in inv_active if not c["passed"])
    rec = {"group": group, "seed": SEED, "session": n, "chain_dead": False,
           "import_error": res["import_error"],
           "n_active": len(active), "n_active_pass": n_pass,
           "functional": round(n_pass / len(active), 3) if active else 0.0,
           "invariant_violations": inv_viol,
           "checks": {c["name"]: c["passed"] for c in active}}
    _append(group, rec)
    print(f"SCORED {group} {SEED} S{n}: active {n_pass}/{len(active)} "
          f"func={rec['functional']} inv_viol={inv_viol} import_err={bool(res['import_error'])}")


def _append(group, rec):
    p = os.path.join(_g(group), "scores.jsonl")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def aggregate():
    base = os.path.join(ROOT, "runs")
    groups = sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))) if os.path.isdir(base) else []
    out = {}
    for g in groups:
        p = os.path.join(_g(g), "scores.jsonl")
        if not os.path.exists(p):
            continue
        recs = {r["session"]: r for r in (json.loads(l) for l in open(p, encoding="utf-8"))}
        rows, seen_pass = [], {}
        for n in sorted(recs):
            r = recs[n]
            if r.get("chain_dead"):
                rows.append({"S": n, "dead": True}); continue
            regr = sum(1 for nm, ok in r["checks"].items() if seen_pass.get(nm) and not ok)
            for nm, ok in r["checks"].items():
                if ok:
                    seen_pass[nm] = True
            rows.append({"S": n, "func": r["functional"], "inv_viol": r["invariant_violations"],
                         "regr": regr, "default_ok": r["checks"].get("default_limit")})
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
