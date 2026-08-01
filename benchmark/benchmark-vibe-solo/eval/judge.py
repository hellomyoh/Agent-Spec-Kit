"""Validate the score JSONL files and aggregate the weighted composite (plan §6).

Dependency-free (no jsonschema). Two commands:
  python eval/judge.py validate          # structural check of all *_scores.jsonl + cost.jsonl under runs/
  python eval/judge.py aggregate         # per-(mode,level) composite from whatever scores exist

Composite weights (plan §6): code/invariant 45, goal/product-intent 20, doc 15, process 10, cost 10.
Sub-scores are 0..1 then weighted. Missing inputs (doc/process not yet judged, cost tokens null) are
reported as PENDING rather than silently zeroed.
"""
from __future__ import annotations
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "runs")
MODES = ("baseline-general", "throughline-solo")
LEVELS = ("beginner", "intermediate", "advanced")
WEIGHTS = {"code": 45, "goal": 20, "doc": 15, "process": 10, "cost": 10}
INVARIANT = {"unknown_where_raises", "unknown_where_ignored", "blank_query", "sort_stable"}


def _load(p):
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def _scores_dir(mode, level, seed):
    return os.path.join(RUNS, mode, level, seed, "scores")


def validate(seed="seed1"):
    problems, counts = [], {}
    checks = {
        "code_scores.jsonl": (["mode", "level", "seed", "session", "chain_dead"], None),
        "doc_scores.jsonl": (["mode", "level", "seed", "dims"], ("dims", 0, 3)),
        "process_scores.jsonl": (["mode", "level", "seed", "session", "dims"], ("dims", 0, 3)),
        "cost.jsonl": (["mode", "level", "seed", "session"], None),
    }
    for mode in MODES:
        for level in LEVELS:
            for fname, (req, rng) in checks.items():
                p = os.path.join(_scores_dir(mode, level, seed), fname)
                rows = _load(p)
                counts[f"{mode}/{level}/{fname}"] = len(rows)
                for i, r in enumerate(rows):
                    for k in req:
                        if k not in r:
                            problems.append(f"{p}[{i}] missing '{k}'")
                    if rng:
                        key, lo, hi = rng
                        for dk, dv in (r.get(key) or {}).items():
                            if not (isinstance(dv, int) and lo <= dv <= hi):
                                problems.append(f"{p}[{i}] {key}.{dk}={dv} out of [{lo},{hi}]")
    print("=== row counts ===")
    for k, v in sorted(counts.items()):
        if v:
            print(f"  {k}: {v}")
    print("=== problems ===")
    print("  none" if not problems else "\n".join("  " + x for x in problems))
    return not problems


def _final_code(mode, level, seed):
    rows = {r["session"]: r for r in _load(os.path.join(_scores_dir(mode, level, seed), "code_scores.jsonl"))}
    if not rows:
        return None
    n = max(rows)
    return rows[n], n, rows


def aggregate(seed="seed1"):
    print(f"=== composite (seed={seed}) -- PENDING = inputs not yet produced ===\n")
    for mode in MODES:
        for level in LEVELS:
            fc = _final_code(mode, level, seed)
            if not fc:
                continue
            final, n, allrows = fc
            # code sub-score (0..1): functional minus invariant penalty, plus no-regression
            if final.get("chain_dead"):
                code_sub, goal_sub = 0.0, 0.0
            else:
                code_sub = final.get("functional", 0.0)
                # goal/product-intent: did the decisive policy checks hold at the final session?
                checks = final.get("checks", {})
                decisive = [checks[k] for k in INVARIANT if k in checks]
                goal_sub = (sum(1 for x in decisive if x) / len(decisive)) if decisive else 0.0
            doc_rows = _load(os.path.join(_scores_dir(mode, level, seed), "doc_scores.jsonl"))
            proc_rows = _load(os.path.join(_scores_dir(mode, level, seed), "process_scores.jsonl"))
            doc_sub = (doc_rows[-1]["total"] / 15) if doc_rows and "total" in doc_rows[-1] else None
            proc_sub = (sum(r.get("total", 0) for r in proc_rows) / (15 * len(proc_rows))) if proc_rows else None
            cost_rows = _load(os.path.join(_scores_dir(mode, level, seed), "cost.jsonl"))
            cost_known = cost_rows and all(r.get("total_tokens") is not None for r in cost_rows)

            parts = []
            parts.append(f"code {WEIGHTS['code']*code_sub:.1f}/{WEIGHTS['code']}")
            parts.append(f"goal {WEIGHTS['goal']*goal_sub:.1f}/{WEIGHTS['goal']}")
            parts.append(f"doc {WEIGHTS['doc']*doc_sub:.1f}/{WEIGHTS['doc']}" if doc_sub is not None else "doc PENDING/15")
            parts.append(f"proc {WEIGHTS['process']*proc_sub:.1f}/{WEIGHTS['process']}" if proc_sub is not None else "proc PENDING/10")
            parts.append("cost READY" if cost_known else "cost PENDING/10")
            print(f"{mode}/{level} (final S{n}): " + " | ".join(parts))
    print("\n(Use driver.py aggregate for the per-session trajectory; this is the end-state composite.)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "validate"
    seed = sys.argv[2] if len(sys.argv) > 2 else "seed1"
    if cmd == "validate":
        ok = validate(seed)
        sys.exit(0 if ok else 1)
    elif cmd == "aggregate":
        aggregate(seed)
