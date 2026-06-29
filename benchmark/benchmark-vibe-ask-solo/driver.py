"""Vibe ASK-Solo Benchmark — driver (orchestrator-driven, like benchmark-realapp).

The ORCHESTRATOR (Claude/Codex) runs a fresh dev-agent per (mode, level, session); this script
does the deterministic plumbing and the AUTOMATED code scoring. Doc/process scoring is done by a
separate judge step (eval/judge.py) against the rubrics.

Commands:
  prepare <mode> <level> <n>   build runs/<mode>/<level>/<seed>/work/ for session n; inject memory; print it
  score   <mode> <level> <n>   snapshot work/ -> sNN/, run hidden battery, write scores/code_scores.jsonl + cost.jsonl
  aggregate                    per-(mode,level) trajectory + cumulative regression
  init                         create the empty runs/ skeleton for seed1

modes  = baseline-general | ask-solo
levels = beginner | intermediate | advanced
SEED   = env SEED (default seed1). Pilot runs seed1; seed2+ is structure-only (set SEED=seed2 ... to extend).
"""
from __future__ import annotations
import difflib, json, os, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "eval"))
from tests import run_all, active_in, INVARIANT_CHECKS, public_summary  # noqa: E402

SEED = os.environ.get("SEED", "seed1")
MODES = ("baseline-general", "ask-solo")
LEVELS = ("beginner", "intermediate", "advanced")
MODULE = "catalog.py"
NSESSIONS = 7  # s0..s6
TASK = "catalog"
SSOT_DOCS = ["PRODUCT.md", "FEATURES.md", "DECISIONS.md", "PROGRESS.md"]

TASKDIR = os.path.join(ROOT, "tasks", TASK)
PROVIDED = os.path.join(TASKDIR, "provided")


def _run(mode, level):
    return os.path.join(ROOT, "runs", mode, level, SEED)


def _snap(mode, level, n):
    return os.path.join(_run(mode, level), f"s{n}")


def _work(mode, level):
    return os.path.join(_run(mode, level), "work")


def _carry_code_and_docs(src, dst):
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(src):
        sp = os.path.join(src, f)
        if f == MODULE and os.path.isfile(sp):
            shutil.copy2(sp, os.path.join(dst, f))
        if f == "docs" and os.path.isdir(sp):
            shutil.copytree(sp, os.path.join(dst, "docs"), dirs_exist_ok=True)


def prepare(mode, level, n):
    n = int(n)
    assert mode in MODES and level in LEVELS, "bad mode/level"
    run = _run(mode, level)
    work = _work(mode, level)
    for sub in ("prompts", "conversation", "docs", "scores"):
        os.makedirs(os.path.join(run, sub), exist_ok=True)
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work)
    shutil.copytree(PROVIDED, os.path.join(work, "provided"))
    if n > 0:
        _carry_code_and_docs(_snap(mode, level, n - 1), work)

    # user prompt for this session/level
    src_prompt = os.path.join(TASKDIR, "prompts", level, f"s{n:02d}.md")
    prompt_txt = open(src_prompt, encoding="utf-8").read()
    open(os.path.join(work, "USER_PROMPT.md"), "w", encoding="utf-8").write(prompt_txt)
    shutil.copy2(src_prompt, os.path.join(run, "prompts", f"s{n:02d}_user_prompt.md"))

    # memory artifact + mode instruction
    docs = os.path.join(work, "docs")
    os.makedirs(docs, exist_ok=True)
    if mode == "ask-solo":
        ssot = os.path.join(docs, "ssot")
        os.makedirs(ssot, exist_ok=True)
        for d in SSOT_DOCS:
            p = os.path.join(ssot, d)
            if not os.path.exists(p):
                open(p, "w", encoding="utf-8").write(f"# {d[:-3]}\n\n(maintain this SSOT doc across sessions)\n")
        mem = (f"MODE=ask-solo. Your SSOT docs are in docs/ssot/ ({', '.join(SSOT_DOCS)}). "
               "READ them before coding; UPDATE them after. Follow agents/dev_ask-solo.md: if the user's "
               "latest request conflicts with a recorded decision, do NOT blindly implement — choose "
               "hold / ask / supersede-the-decision / implement, and record the conflict.")
    else:
        notes = os.path.join(docs, "NOTES.md")
        if not os.path.exists(notes):
            open(notes, "w", encoding="utf-8").write("# NOTES\n\n(optional free-form notes; not an authority doc)\n")
        mem = ("MODE=baseline-general. You may keep a short docs/NOTES.md if you like, but it is not an "
               "authority document. Follow agents/dev_baseline-general.md: implement the user's current "
               "request against the current code. No required spec/SSOT structure.")

    open(os.path.join(work, "_MEMORY_FOR_PROMPT.txt"), "w", encoding="utf-8").write(mem)
    print(f"PREPARED {mode}/{level}/{SEED} S{n} at {work}")
    print(f"---USER PROMPT---\n{prompt_txt}\n---MEMORY---\n{mem}")


def _churn(mode, level, n):
    cur = os.path.join(_work(mode, level), MODULE)
    prev = os.path.join(_snap(mode, level, n - 1), MODULE) if n > 0 else None
    if not os.path.exists(cur):
        return None
    cur_lines = open(cur, encoding="utf-8").read().splitlines()
    prev_lines = open(prev, encoding="utf-8").read().splitlines() if prev and os.path.exists(prev) else []
    diff = list(difflib.unified_diff(prev_lines, cur_lines, n=0))
    changed = sum(1 for l in diff if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---")))
    return {"changed_lines": changed, "total_lines": len(cur_lines)}


def score(mode, level, n):
    n = int(n)
    run = _run(mode, level)
    work = _work(mode, level)
    snap = _snap(mode, level, n)
    if os.path.isdir(snap):
        shutil.rmtree(snap)
    os.makedirs(snap)
    for f in os.listdir(work):
        sp = os.path.join(work, f)
        if f == "provided":
            continue
        if os.path.isfile(sp):
            shutil.copy2(sp, os.path.join(snap, f))
        else:
            shutil.copytree(sp, os.path.join(snap, f), dirs_exist_ok=True)
    # mirror prompt / conversation / docs into the run's stable folders
    for fname, sub, newname in [("CONVERSATION.md", "conversation", f"s{n:02d}_log.md")]:
        fp = os.path.join(work, fname)
        if os.path.exists(fp):
            shutil.copy2(fp, os.path.join(run, sub, newname))
    if os.path.isdir(os.path.join(work, "docs")):
        shutil.copytree(os.path.join(work, "docs"), os.path.join(run, "docs"), dirs_exist_ok=True)

    code = {"mode": mode, "level": level, "seed": SEED, "session": n}
    if not os.path.exists(os.path.join(snap, MODULE)):
        code.update({"chain_dead": True, "reason": f"no {MODULE}"})
        _append(run, "code_scores.jsonl", code)
        _append(run, "cost.jsonl", _cost_row(mode, level, n, None))
        print(json.dumps(code)); return

    res = run_all(snap, level, n)
    active = [c for c in res["checks"] if active_in(c["name"], n)]
    n_pass = sum(1 for c in active if c["passed"])
    inv = [c for c in active if c["name"] in INVARIANT_CHECKS]
    code.update({
        "chain_dead": False, "import_error": res["import_error"],
        "n_active": len(active), "n_active_pass": n_pass,
        "functional": round(n_pass / len(active), 3) if active else 0.0,
        "invariant_violations": sum(1 for c in inv if not c["passed"]),
        "checks": {c["name"]: c["passed"] for c in active},
        "public_qa": public_summary(res, n, level),     # safe: failing names only
    })
    _append(run, "code_scores.jsonl", code)
    _append(run, "cost.jsonl", _cost_row(mode, level, n, _churn(mode, level, n)))
    print(f"SCORED {mode}/{level}/{SEED} S{n}: active {n_pass}/{len(active)} "
          f"func={code['functional']} inv_viol={code['invariant_violations']} "
          f"failing={code['public_qa']['failing']}")


def _cost_row(mode, level, n, churn):
    # edit_churn computed deterministically; token/turn/tool/wall fields are filled by the orchestrator
    return {"mode": mode, "level": level, "seed": SEED, "session": n,
            "edit_churn": churn, "total_tokens": None, "conversation_turns": None,
            "tool_calls": None, "wall_time_s": None, "rework_count": None}


def _append(run, fname, rec):
    p = os.path.join(run, "scores", fname)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def aggregate():
    base = os.path.join(ROOT, "runs")
    out = {}
    if not os.path.isdir(base):
        print("{}"); return {}
    for mode in MODES:
        for level in LEVELS:
            p = os.path.join(base, mode, level, SEED, "scores", "code_scores.jsonl")
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
                             "regr": regr, "blank_ok": r["checks"].get("blank_query")})
            out[f"{mode}/{level}"] = rows
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out


def init():
    for mode in MODES:
        for level in LEVELS:
            for sub in ("prompts", "conversation", "work", "docs", "scores"):
                os.makedirs(os.path.join(_run(mode, level), sub), exist_ok=True)
    print(f"initialised runs/ skeleton for {SEED}: {len(MODES)} modes x {len(LEVELS)} levels")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prepare":
        prepare(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "score":
        score(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "aggregate":
        aggregate()
    elif cmd == "init":
        init()
