import os, json, glob, difflib, statistics as st
from score_M import score_session, SESSION_OPS
ROOT = os.path.dirname(os.path.abspath(__file__))
GROUPS = ["B", "P", "ASK"]; SEEDS = [1, 2]; SESSIONS = [0, 1, 2, 3, 4]

# tokens from run_log
tok = {}
for ln in open(f"{ROOT}/logs/run_log.jsonl", encoding="utf-8"):
    r = json.loads(ln); tok[(r["group"], r["seed"], r["session"])] = r.get("tokens")

def pkg_churn(prev_dir, cur_dir):
    """added+deleted lines across exprkit/*.py between two session snapshots."""
    def files(d):
        out = {}
        for f in glob.glob(f"{d}/exprkit/*.py"):
            out[os.path.basename(f)] = open(f, encoding="utf-8").read().splitlines()
        return out
    a, b = files(prev_dir), files(cur_dir)
    ch = 0
    for fn in set(a) | set(b):
        for line in difflib.ndiff(a.get(fn, []), b.get(fn, [])):
            if line[:2] in ("+ ", "- "): ch += 1
    return ch

rows = []
for g in GROUPS:
    for k in SEEDS:
        for s in SESSIONS:
            d = f"{ROOT}/runs/{g}/seed{k}/s{s}"
            sc = score_session(d, s)
            churn = pkg_churn(f"{ROOT}/runs/{g}/seed{k}/s{s-1}", d) if s > 0 else 0
            rows.append({"group": g, "seed": k, "session": s, "f2p": sc["f2p"],
                         "p2p_reg": sc["p2p_regression"], "omissions": sc["cross_cut_omissions"],
                         "ops_full": sc["ops_full"], "ops_total": sc["ops_total"],
                         "import_error": sc["import_error"], "floor_div_ok": sc.get("floor_div_ok"),
                         "churn": churn, "tokens": tok.get((g, k, s))})
json.dump(rows, open(f"{ROOT}/logs/results_M.json", "w"), ensure_ascii=False, indent=1)

def sub(g, s=None):
    return [r for r in rows if r["group"] == g and (s is None or r["session"] == s)]

print("############ M-pilot (exprkit, 3 groups x 2 seeds x 5 sessions) ############")
print("\n=== end-state (S4): cross-cutting completeness & regression ===")
for g in GROUPS:
    s4 = sub(g, 4)
    print(f"  {g}: ops_full={st.mean(r['ops_full'] for r in s4):.1f}/9  "
          f"p2p_reg(S4)={st.mean(r['p2p_reg'] for r in s4):.2f}  "
          f"import_err={sum(1 for r in s4 if r['import_error'])}/2  "
          f"floor_div_ok={[r['floor_div_ok'] for r in s4]}")

print("\n=== regression & omissions across sessions 1-4 (per group, summed over chains) ===")
for g in GROUPS:
    rs = [r for r in sub(g) if r["session"] >= 1]
    total_om = sum(len(r["omissions"]) for r in rs if r["omissions"])
    mean_reg = st.mean(r["p2p_reg"] for r in rs)
    ie = sum(1 for r in rs if r["import_error"])
    print(f"  {g}: mean_regression={mean_reg:.3f}  total_cross_cut_omissions={total_om}  import_errors={ie}")

print("\n=== F2P (new ops) by session ===")
print(f"{'grp':4s} " + " ".join(f"S{s}" for s in SESSIONS))
for g in GROUPS:
    print(f"{g:4s} " + " ".join(f"{st.mean(r['f2p'] for r in sub(g,s)):.2f}" for s in SESSIONS))

print("\n=== cost & churn (per chain, mean over seeds) ===")
for g in GROUPS:
    toks = [sum(r["tokens"] for r in rows if r["group"] == g and r["seed"] == k) for k in SEEDS]
    chn = [sum(r["churn"] for r in rows if r["group"] == g and r["seed"] == k) for k in SEEDS]
    base = st.mean([sum(r["tokens"] for r in rows if r["group"] == "B" and r["seed"] == k) for k in SEEDS])
    print(f"  {g}: tokens/chain={st.mean(toks):.0f} ({st.mean(toks)/base:.2f}x B)  churn/chain={st.mean(chn):.0f}")

# any nonzero regression / import errors / omissions anywhere
print("\n=== notable failures (any chain/session) ===")
bad = [r for r in rows if r["import_error"] or (r["omissions"]) or r["p2p_reg"] > 0]
if not bad: print("  none — all sessions: import OK, no cross-cutting omissions, no regression")
for r in bad[:12]:
    print(f"  {r['group']}/s{r['seed']}/S{r['session']}: import={r['import_error']} omissions={r['omissions']} p2p_reg={r['p2p_reg']}")
