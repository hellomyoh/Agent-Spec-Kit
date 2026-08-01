# THROUGHLINE-QBench harness (B3 Revert-to-Origin)

🌐 **English** · [한국어](README.ko.md)

A maintainer-side evaluation tool, kept separate from the THROUGHLINE runtime kit (`en/`, `ko/`). Methodology: [../METHODOLOGY.md](../METHODOLOGY.md).

## Layout
- `tracks/rank/` — **the B3 verification track**. A library whose tie-break policy changes.
  - `ref_base.py` (alphabetical) `ref_R1.py` (length) `ref_R2.py` (reverse alphabetical) — one oracle per policy.
  - `tests.py` — `get_core()` (invariants across all policies = P2P), `get_policy(name)` (per-policy behaviour).
  - `change_requests/step{0..3}.md` — the agent's input. step0 = Base, step1 = R1, step2 = R2, **step3 = Revert** (R1 not described).
- `tracks/clean_tags/` — the same pattern, but **R1 = alphabetical sort (the model's default guess) → unfit for B3 discrimination** (kept for reference).
- `score.py` — the scorer. `score_revert(track_dir, solution.py, step)` → restoration fidelity / regression / core.

## Verification (confirming tests and policy discrimination)
```
PYTHONIOENCODING=utf-8 python score.py
# -> "ALL REFERENCES VALID & POLICIES DISCRIMINATE"
```

## B3 run procedure (summary)
1. **Build the Base→R1→R2 chain**: each arm (L0 / L1 / L-SSOT) develops step0→1→2 in sequence (handed the previous step's code plus that arm's memory). L-SSOT maintains SPEC + HISTORY (append-only) + PROGRESS.
2. **Set up the isolated workspace (mandatory, P8)**: copy only each chain's step2 output (current = R2 code + that arm's memory files) into an empty directory. Block access to earlier steps and to the change requests.
3. **Run the revert**: tell the agent "use only this directory; roll back R2 and restore R1" (without providing the content of R1). The no-memory arm must have no way to know R1.
4. **Score**: `score.get_policy("R1")` pass rate = restoration fidelity. `get_policy("R2")` residue = not restored.

Latest run results: [../results/B3_results.json](../results/B3_results.json) (L0 0/2, L1 2/2, L-SSOT 2/2).

## Leakage warning (critical)
Without filesystem isolation, a no-memory agent will search for and open `change_requests/step1.md` (the R1 spec) or the earlier step's code and **read R1 directly, at which point the discrimination disappears**. The revert (step3) workspace must be isolated as self-contained, with external access forbidden (methodology P8).
