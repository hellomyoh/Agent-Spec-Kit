# THROUGHLINE-QBench — consolidated results report

🌐 **English** · [한국어](FINAL_REPORT.ko.md)

> Methodology: [METHODOLOGY.md](METHODOLOGY.md) · Harness: [harness/](harness/) · B3 run artifacts: [results/](results/)
> Development model: Haiku 4.5 (weak), with Sonnet (strong) run alongside for parts of B1. Scoring is deterministic, computed from stdlib/AST. Every agent call and artifact was preserved.

## Scope of execution
- **B3 (revert-to-origin) was run directly on this harness** — it is the item where a THROUGHLINE effect discriminated in the methodology, so it is reproduced end to end.
- **B1 and B2 record evaluation results obtained under the same protocol.** Repeat runs under identical conditions were omitted because the results are statistically the same; a full re-run is possible with the harness.
- Limits: centred on one model (the weak model), no qualitative judging (objective metrics only), and some items are at pilot scale (see each section and the appendix below).

---

## B1 — single-shot implementation (5 arms, compute-matched)

Question: in a single-shot implementation, is the THROUGHLINE structure more correct and robust than the control arms?

| Arm (weak model, hard pass rate) | Value |
|---|---|
| A0 implement directly | 0.804 |
| A1 think first (unstructured) | 0.877 |
| A2 best-of-N | 0.804 |
| **THROUGHLINE** (spec-first) | **0.909** |

- Decomposing the naive `THROUGHLINE − A0 = +0.106` gives **A1 − A0 (thinking first) = +0.073 (about 70%)** plus **THROUGHLINE − A1 (structure) = +0.032**.
- **Primary comparison `THROUGHLINE − max(A0, A1, A2) = +0.032`, 95% CI [−0.064, +0.136] → includes 0 (not significant).**
- On the strong model, `THROUGHLINE − A0 = −0.042` (the extra structure acts as over-design instead).
- Cost: +16–22% tokens, +37–39% code.

**Verdict: no single-shot functional advantage shown.** Most of the apparent gain is explained by "thinking beforehand", the net increment from structure is statistically indistinguishable from zero, and on the strong model it is negative.

### Model-strength sensitivity — the two-arm illusion (important)

Measure the same task while varying model strength and the number of comparison arms, and the impression that "THROUGHLINE is effective" can be manufactured by the measurement design itself.

| Condition | Comparison | THROUGHLINE advantage | Interpretation |
|---|---|---|---|
| Strong model | — | `THROUGHLINE − A0 = −0.042` | function is near the ceiling, cannot discriminate; actually negative |
| Weak model | **2 arms** (baseline vs THROUGHLINE) | `THROUGHLINE − A0 = +0.106` (hard) | weakening the model breaks the ceiling and **THROUGHLINE appears to lead** |
| Weak model | **5 arms** (compute-matched) | `THROUGHLINE − max(A0,A1,A2) = +0.032` (not significant) | about **70% of that gain is explained by thinking-first (A1)** |

- In other words, the result "**switch to a weaker model and THROUGHLINE wins**" holds **only in a two-arm comparison**; in a five-arm comparison that adds the thinking-first and sample-count control arms, the net effect of the THROUGHLINE structure shrinks to non-significance.
- This is the core reason the methodology demands **several compute-matched arms (P1)** rather than two.

## B2 — cumulative feature addition (3 arms)

Question: in multi-session development that adds features cumulatively, does THROUGHLINE's SSOT reduce regression and erosion?

| Metric (weak model) | L0 | L1 | L-SSOT |
|---|---|---|---|
| Regression rate (all steps) | 0.000 | 0.000 | 0.000 |
| Fix Rate (all steps) · fully resolved | 1.0 · all | 1.0 · all | 1.0 · all |
| Structural erosion (final) | 0.72 | 0.82 | 0.73 |
| Lines of code (final) | 155 | 162 | 215 |
| Tokens / chain | 72.9k | 79.8k (1.09×) | **120.3k (1.65×)** |

**Verdict: no THROUGHLINE gain shown (every arm at zero regressions — a ceiling), cost only, +65%.** Working code was handed over at every step and the scale was small, so memory was unnecessary — leaving no surface to discriminate on.

## B3 — revert-to-origin cycle (3 arms) — the item where a THROUGHLINE effect discriminated

Question: when **reverting to R1** after several modifications, does memory of the past decision enable faithful restoration?
Flow: Base → R1 (tie-break by length) → R2 (reverse alphabetical) → **Revert (restore R1)**. The code at the moment of reverting is R2, so the R1 behaviour is not present in the code; restoring it requires memory.

### (Reference) run it without isolation and the discrimination disappears
Without filesystem isolation, every arm succeeds at restoration (1.00). The no-memory arm simply reads the change request (the file that states the R1 spec) or the earlier step's code directly — confirmed by the abnormally high tool-call count in that arm. This is not a THROUGHLINE null result but **measurement leakage**, and it is the basis for methodology P8 (isolation).

### Isolated run (this harness) — discrimination succeeded

With only the current R2 code and that arm's memory in the workspace, and external access blocked (rank track, 2 seeds):

| Arm (isolated) | R1 restored | Policy actually implemented | Tool calls |
|---|---|---|---|
| **L0** no memory | **0/2** | wrongly restored to the default (alphabetical) | 2, 2 |
| **L1** free notes | **2/2** | R1 (length) restored exactly | 3, 3 |
| **L-SSOT** structured SSOT / history | **2/2** | R1 (length) restored exactly | 5, 5 |

(Artifacts and scores: [results/B3_results.json](results/B3_results.json))

**Verdict: memory effect proven.** The no-memory arm could not know R1, fell back to the model's default, and failed to restore it; the two arms holding a record restored R1 exactly. **Whether THROUGHLINE's structured memory (SSOT/history) beats plain notes was, however, not separated** — in a single revert both arms preserved R1 and tied.

---

## Overall conclusions

1. **On single-shot and cumulative-addition tasks, no objective THROUGHLINE advantage was shown** (B1 is non-significant after controls and negative on the strong model; B2 is at a ceiling). What was confirmed consistently is **increased cost** (+16–22% single-shot, +65% long-horizon).
2. **The point where THROUGHLINE discriminates is "revert to origin"** — a restoration task where a past decision must not be lost. There, **holding the memory was decisive for restoration** (no memory fell back to the default and failed). This shows that a development flow which reverts to an earlier state after repeated change is an appropriate measurement surface for the core value of THROUGHLINE-style methodologies: preservation of decisions.
3. **The most important follow-up**: is THROUGHLINE's *structured* memory better than *plain notes*? In a short single revert, both were sufficient. The advantage of structure will only appear under conditions where notes readily lose information (below).

## Follow-up experiments (isolating the structural effect)
1. **A long change history**: several more modifications after R1, then revert to R1 → make free notes lose or bury R1, testing the structural advantage of an append-only change history.
2. **Isolation as the default**, and **a non-default R1 policy on every track** (to prevent accidental restoration).
3. **Match the recorded volume of L1 and L-SSOT** (separating structure from volume) and **expand instances and seeds** (statistical power).

## Appendix — reliability and limits
- **Statistical power**: the isolated B3 is a pilot of 1 track × 2 seeds. The direction (no memory 0/2 vs. memory 2/2) is clear, but a statistical assertion requires further expansion.
- **Track design**: B3's R1 must be a non-default policy. "Alphabetical sort", for example, is the model's default guess, so even a no-memory arm hits it by chance — unfit for discrimination (the rank track's "tie-break by length" is fit for purpose).
- **Reproduction**: the artifacts and call logs of every item were preserved, and B3 is self-reproducible from `benchmark/results/` and `harness/` ([harness/README.md](harness/README.md)).
