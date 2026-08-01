# THROUGHLINE-QBench — benchmark methodology (v1.0)

🌐 **English** · [한국어](METHODOLOGY.ko.md)

> **Purpose**: to measure, with causal validity, **how much more effective the spec-driven development methodology (THROUGHLINE) is quantitatively** than a baseline.
> **Nature**: this document and everything under `benchmark/` are a **maintainer-side evaluation harness**. The THROUGHLINE runtime kit (`en/`, `ko/`) is prompts only (markdown + git); the benchmark is measurement infrastructure kept separate from it.
> **Principle**: proof of an effect and "no effect" are reported with equal weight. No positive conclusion is drawn without evidence.

---

## 1. Why this is hard to measure, and the rationale for the design

Measuring the effect of a methodology on coding agents commonly falls into the following traps. Each principle below is a control for one of them.

- **Functional ceiling**: a capable model passes nearly 100% of the functional tests on a well-defined task, so functional metrics cannot discriminate between methodologies.
- **Attribution error**: a two-arm "methodology vs. nothing" comparison cannot distinguish whether an improvement came from that methodology's *structure* or merely from *planning ahead, extra reasoning, or sample count*. The apparent gain from a scaffold often shrinks or vanishes once the reasoning budget (compute) is matched.
- **Length confound**: LLM judges and some metrics over-reward longer, more verbose output.
- **Non-independent data**: running a plain t-test on data where seeds are nested within instances causes false positives to spike.
- **Record leakage**: when measuring memory/restoration, if the agent can reach earlier-version code or spec files, even the no-memory arm reads the answer directly and the discrimination disappears.

## 2. Design principles (8)

| | Principle | Trap it controls |
|---|---|---|
| P1 | **Causal isolation** — several arms matched on compute/memory rather than two, separating "structure" from "planning ahead, sample count, presence of memory" | attribution error |
| P2 | **Compute accounting** — record tokens, LLM calls, and LLOC; report the primary comparison as matched or Pareto | attribution error |
| P3 | **Objective metrics first** — code-quality judges are unreliable, so function, regression, restoration, and erosion are measured with deterministic automated metrics; judges are auxiliary, for qualitative dimensions | judging bias |
| P4 | **Ceiling avoidance** — calibrate the baseline pass rate into the 0.3–0.8 band, run strong and weak models in parallel, and **confirm discriminating variance with a pilot first** | functional ceiling |
| P5 | **Length control** — forbid rewarding volume in the judging rubric, plus LLOC normalisation / regression adjustment | length confound |
| P6 | **Hierarchical statistics** — mixed-effects models + cluster bootstrap; repeated measures by step for long-horizon tasks | non-independent data |
| P7 | **Pre-registration and refutation** — fix the primary metric, comparison, and failure conditions before collecting data | post-hoc selection bias |
| P8 | **Filesystem isolation** — when measuring memory/restoration, place only the current code and that arm's memory artifacts in the agent's workspace, and block access to earlier-version code and other specs | record leakage |

## 3. Benchmark items (3)

### B1 — single-shot implementation (5 arms)
- **Question**: given the same requirements, model, and compute, does a spec-first structure produce more correct and robust code than the control arms?
- **Task**: a small library based on a public standard spec (parser, comparator, etc.), a fixed public API, hidden tests (examples + properties + reference comparison).
- **5 arms**: A0 implement directly / A1 think first (unstructured) / A2 best-of-N / **THROUGHLINE** (spec-first) / (THROUGHLINE⁻ — write the spec then discard it; follow-up).
- **Primary comparison**: `THROUGHLINE − max(A0, A1, A2)`. Two conditions: strong and weak model.

### B2 — cumulative feature addition (3 arms)
- **Question**: in development that adds features cumulatively across multiple sessions, does THROUGHLINE's single source of truth (SSOT) reduce regression and structural erosion?
- **Flow**: add a feature at each step. Hidden tests at step N = the new feature (F2P) + everything accumulated from earlier steps (P2P).
- **3 arms**: L0 no memory / L1 unstructured notes / **L-SSOT** structured SSOT.
- **Caution**: if working code is handed over at every step and the scale is small, memory is unnecessary and a ceiling appears. Discriminating requires a sufficiently large codebase.

### B3 — revert-to-origin cycle (3 arms)
- **Question**: after modifying several times, when **reverting to the first revision (R1)**, does memory that preserved the past decision (particularly a structured SSOT / change history) enable faithful restoration?
- **Flow**: develop (Base) → **R1** (policy change) → **R2** (policy changed again) → **Revert (restore R1)** → verify R1 restoration.
- **Key design**: each modification is a behavioural change that *overwrites* the policy. The current code at the moment of reverting is in the R2 state, so **the R1 behaviour is no longer present in the code.** Restoring it therefore requires *memory* of the past decision. (This creates the "memory is mandatory" condition that B2 failed to create.)
- **3 arms**: L0 no memory / L1 free notes / **L-SSOT** (spec + append-only change history + progress record).
- **Mandatory controls**:
  1. **Filesystem isolation (P8)**: put only the current R2 code and that arm's memory files in the revert workspace. Earlier-step code and change requests (especially the R1 spec) must be unreachable.
  2. **R1 must be a non-default policy.** It has to differ from the model's natural guess, otherwise the no-memory arm hits it by chance.
  3. The revert request states only R2 and **does not describe the content of R1** ("consult your records").
- **Primary comparison**: on restoration fidelity (R1 policy pass rate), `{L1, L-SSOT} − L0` (memory effect) and `L-SSOT − L1` (structure effect).

### B4–B6 — mid-scale and beyond (separate design)
That THROUGHLINE has no effect at small scale (B1, B2) is a settled premise, and the author's recommendation is for **intermediate and larger** projects. Multi-module evolution (B4), decision-conflict traps (B5), and the cost-vs-scale threshold curve (B6) are designed to *prove or refute* a THROUGHLINE effect at that scale. Detail: [MIDSCALE_DESIGN.md](MIDSCALE_DESIGN.md) *(Korean)*.

> **B7 (recommended — reproducing reality)**: B4's synthetic "cross-cutting contract" became self-evident under a good design (generic dispatch) and failed to discriminate (M-pilot). Replace it with a real-world app where **multi-layer (DB · cache · backend · frontend) integration consistency** naturally breaks down as scale grows. Do not invent rules for THROUGHLINE's benefit; score only on the *app's actual end-to-end behaviour*. Detail: [REALWORLD_DESIGN.md](REALWORLD_DESIGN.md) *(Korean)*.

## 4. Metrics (objective metrics first)

| Area | Metric | Definition |
|---|---|---|
| Function | Fix Rate | pass rate of the new feature (F2P), but only when everything accumulated earlier (P2P) also passes; otherwise 0 |
| Regression | regression rate / regression-free rate | share of previously passing tests that broke / share of runs with zero regressions |
| Restoration (B3) | restoration fidelity | R1 policy pass rate after reverting + R2 residue (if R2 behaviour remains, it is not restored) |
| Structure | erosion · max complexity · LLOC growth | share of complexity mass concentrated in high-complexity functions (AST) |
| Change | churn · API breakage | lines added + deleted between steps / number of changed signatures among previously public functions (AST) |
| Cost | tokens · call count · time | agent telemetry |
| Qualitative (optional) | design quality | 3 judges from different families, position counterbalancing, length control, agreement (κ) reported; withheld if κ < 0.40 |

## 5. Statistics
Mixed-effects model `metric ~ arm (+ step) + (1 | instance)`, cluster bootstrap, standardised effect sizes. For long-horizon tasks, compare the **trajectory (slope)** across steps between arms. When the number of instances (clusters) is small, report only effect size and direction and avoid statistical assertions (explicitly labelled a pilot).

## 6. Pre-registration and interpretation criteria
- **Effect proven**: the primary comparison is significant against the control arms, holds after compute and length controls, is not concentrated in a single task, and (if qualitative judging is used) judge agreement κ ≥ 0.60.
- **No effect claimed**: any one of — a control arm (A1/L1) is statistically equal to THROUGHLINE (attribution failure), the difference disappears after controls, the result is concentrated in a single task, judge reliability falls short, or a ceiling prevents discrimination.

## 7. Execution protocol
1. Confirm that the reference passes 100% of the hidden tests, and that a deliberately wrong solution is caught by them (negative control).
2. **Confirm discriminating variance with a pilot.** If the variance of the primary metric is 0 (ceiling), adjust difficulty and isolation before the main run.
3. Main run: arm × instance × seed (× step). Handoffs are passed as files on disk, and **B3 is performed in an isolated workspace**.
4. Compute the objective metrics automatically, analyse with mixed effects / bootstrap, and judge against the pre-registered criteria.
5. Preserve every agent call (task, arm, seed, step, tokens, call count) and artifact to secure reproducibility.

## 8. Folder structure
```
benchmark/
  METHODOLOGY.md     # (this document)
  FINAL_REPORT.md    # consolidated B1 · B2 · B3 results and conclusions
  harness/
    tracks/rank/     # B3 verification track (non-default R1 policy): reference, tests, change requests
    tracks/clean_tags/  # reference track (R1 is the default policy, so unfit for B3 discrimination)
    score.py         # cumulative / restoration scorer
    README.md        # how to run
  results/           # B3 run artifacts and scores
```
