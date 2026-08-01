# Measuring the THROUGHLINE effect — consolidated results

🌐 **English** · [한국어](RESULTS_SUMMARY.ko.md)

> Methodology: [METHODOLOGY.md](METHODOLOGY.md) · Single-shot / cumulative / restoration detail: [FINAL_REPORT.md](FINAL_REPORT.md) · Mid-scale design: [REALWORLD_DESIGN.md](REALWORLD_DESIGN.md) *(Korean)* · Mid-scale pilot (B7 Stage 0) detail: `benchmark-realapp/` was superseded by a later benchmark and removed from the repository (commit f6c8cc9) — for the summary see §1 below and [FINAL_REPORT.md](FINAL_REPORT.md)
> This document gathers the results of every benchmark item in one place and gives an honest verdict — neither inflated nor deflated — on **"does THROUGHLINE work?"** Principle: proof of an effect and "no effect" are reported with equal weight.

## 1. At a glance

| Item | What it measured | Result | Cost (THROUGHLINE) |
|---|---|---|---|
| **B1** single-shot implementation (5 arms, compute-matched) | does the structure produce more correct/robust code? | **No advantage shown.** `THROUGHLINE − max(A0,A1,A2) = +0.032` (CI includes 0). About 70% of the apparent gain is "thinking beforehand"; on the strong model it is −0.042 | +16–22% tokens |
| **B2** cumulative feature addition (3 arms) | does the SSOT reduce regression/erosion? | **No advantage shown (ceiling).** Zero regressions in every arm | +65% tokens |
| **B3** revert-to-origin (3 arms, isolated) | does memory of a past decision enable faithful restoration? | **Memory effect proven.** No-memory 0/2 failed; the memory-bearing arms (notes · SSOT) 2/2 succeeded. *But structure vs. plain notes was not separated* | (n/a) |
| **M-pilot** mid-scale synthetic (exprkit) | cross-cutting consistency across multi-module increments | **No advantage shown (ceiling).** 9/9 in every arm, zero regressions. Generic dispatch made the contract self-evident | +60% tokens |
| **B7 Stage 0** mid-scale real app (OpsBoard) | consistency advantage of a structured SSOT over lossy memory | **Failed to discriminate (ceiling).** Both arms held all 8 invariants with zero regressions across every session. THROUGHLINE actually scored lower because of a one-off coding bug | +29% tokens |

## 2. The core verdict — does this mean "THROUGHLINE does not work"?

**No — but "it works" has not been proven either.** The precise current state:

1. **At the scales tested (small to lower-mid), no consistency or functional benefit was shown, and a cost of +29–65% was confirmed consistently.** Taken at face value that is unfavourable to THROUGHLINE. The legitimate skeptical reading: *"a capable model + the existing code + a simple memo is enough, and a structured SSOT is pure overhead."*

2. **But we have not yet reached the territory where THROUGHLINE claims its strength.** Every mid-scale pilot hit a ceiling *for identifiable reasons* — the code was small enough to re-read in full every session, the lossy-memory simulation was too weak (a rolling note amounted to a full summary), a single seed, insufficient scale. That is not "we tested the target territory and it lost" but **"we have not yet tested the target territory"** (absence of evidence ≠ evidence of absence).

3. **There is one clear positive signal — B3 (revert-to-origin).** When the past decision was lost, restoration failed (no-memory 0/2); when the record (history / decisions) was preserved, it succeeded (2/2). A narrow but real case where THROUGHLINE's DECISIONS/HISTORY mechanism earns its keep.

4. **There is a great deal this benchmark does not measure.** What it measured = *the consistency and correctness of automated incremental coding*. What it did **not** measure = the value a human gets from writing and reviewing a spec (requirement clarification, design agreement, communication, onboarding, intent alignment). A substantial part of the value of spec-driven development lives there, and it is neither proven nor refuted. Also, B7 Stage 0 observed an **SSOT that the agent maintains by itself**, which cannot be equated with human-in-the-loop THROUGHLINE.

## 3. An honest risk warning (not moving the goalposts indefinitely)

Continually changing the conditions while blaming the ceiling can become post-hoc rationalisation. If **B7 Stage 1** (designed so that lossy memory actually hits its limit — §5 below) also yields no benefit, that becomes **fairly strong cumulative evidence** for *"THROUGHLINE-as-agent-memory has weak practical effect in automated coding."* We must be prepared to accept that outcome with equal weight.

## 4. One-line conclusion

> **In small to lower-mid-scale automated coding, THROUGHLINE is pure cost (+29–65%) with no benefit shown. Benefits in the large-scale, long-horizon territory are untested (not refuted). For memory/restoration there is a proven benefit (B3). The value of a human-centred spec process is outside the measured scope.**

This is consistent with the author's starting premise (**not recommended at small scale; recommended for intermediate and above**). The crux is that the "benefit at intermediate and above" has not yet been shown *with data*, and settling that is the next task.

## 5. The next experiment that will settle it (B7 Stage 1 — pre-registered revisions)

Remove the causes that put B7 Stage 0 on the ceiling, and create the conditions where structured memory is actually needed:

1. **Make lossy memory actually lossy**: put a K-token cap on the B-limited notes (a 2-session window alone is defeated by a rolling full summary) and **increase scale** (sessions, modules, and code volume to the point where re-reading the whole codebase is impractical).
2. **Specify the `render()` output shape in the shared contract** (removes the cause of Stage 0's cross-layer non-attachment).
3. **Force one feature per session** (prevents cramming everything into S0 → lets consistency cost accumulate).
4. **Multiple seeds (≥3)** to average out one-off coding noise (e.g. Stage 0's slot bug).

For detailed results and reproduction, see each report. Statistical assertions only at multi-app, multi-seed scale (Stage 3+).
