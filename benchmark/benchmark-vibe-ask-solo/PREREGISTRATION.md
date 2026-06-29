# PREREGISTRATION — Vibe ASK-Solo Benchmark (seed1 pilot)

Fixed BEFORE running. Prompt levels are assigned in advance and never reclassified from results (plan §3).

## Hypotheses (plan §8)
- **H1** Beginner prompts: ask-solo ≥ baseline-general on goal attainment / fewer invariant violations.
- **H2** Intermediate: ask-solo retains some advantage.
- **H3** Advanced: advantage shrinks; ask-solo's doc cost may not pay off (acceptable).
- **H4** Higher ambiguity ⇒ more baseline drift. **H5** ask-solo dampens that drift.
- **H6** ask-solo's extra questions (if any) reduce rework/regression rather than just adding burden.
- **H7** Better SSOT doc quality ⇒ fewer late-session invariant violations.

## Fixed factors
- Task: `catalog` (one task). Hidden oracle: `eval/oracle/policies.md` (same for all levels).
- Factors: mode {baseline-general, ask-solo} × level {beginner, intermediate, advanced} × session s0..s6.
- Mode behavior fixed by `agents/dev_{mode}.md`. Prompts fixed in `tasks/catalog/prompts/`.
- Conflicts: S5 = intentional change (adopt; level-independent). S6 = forgetting-drift, level-aware oracle:
  beginner/intermediate expect blank→`[]` (preserve); advanced expects blank→all (aware override).
- Decisive automated metric: `blank_query` at S6, plus `invariant_violations` and cumulative `regression`.

## Primary (pre-registered) comparisons
1. **S6 conflict (the headline):** at **beginner & intermediate**, `ask-solo` keeps `blank_query` correct
   (preserve `[]`) while `baseline-general` is expected to drift (blank→all → `blank_query` fail + regression).
   At **advanced**, both should adopt blank→all (no ask-solo advantage expected).
2. **Late-session invariant/regression:** at beginner/intermediate, `ask-solo` invariant_violations and
   regression at s6 ≤ baseline-general.
3. **S5 control:** both modes adopt the explicit change (`unknown_where_ignored` passes at s5+ for both);
   ask-solo must NOT stubbornly keep raising. (Guards against "ask-solo just always keeps old behavior".)
4. **Cost:** ask-solo token/turn cost is recorded; the claim requires its quality gain to offset added cost.

## Seed1 pilot = go/no-go, not inference
Single seed; we read DIRECTION + harness soundness, not p-values (plan §9). Interpretation:
- **Go**: at beginner/intermediate, ask-solo preserves the S6 policy / fewer violations while baseline
  drifts, and cost overhead is not extreme.
- **Revise prompts**: all modes/levels succeed easily ⇒ prompts too explicit / task too easy.
- **Revise task**: all fail ⇒ task too hard / scaffold too heavy.
- **Revise ASK docs**: ask-solo writes docs but still drifts at s6 ⇒ SSOT structure/authority unclear.
- **Stop or narrow claim**: difference only absent at advanced but present at beginner/intermediate ⇒
  narrow ASK's claimed value to "beginner/intermediate user correction" (plan §10 Stop/narrow).

## Analysis questions (answer in RESULTS)
Plan §8 Q1–Q7. Minimum: does ambiguity (level) modulate the ask-solo − baseline gap, concentrated at S6?

## Threats / notes
- Single seed ⇒ one coding accident can dominate; ≥3 seeds before any quantitative claim.
- Code can carry behavior (a prior session's code/comments may encode a decision) — the S6 discriminator is
  designed so the *original* (S3 blank policy) is only restated for advanced; beginner/intermediate rely on
  memory. The uniform "no inline changelog" coding norm (agents/dev_*.md) keeps decisions out of code comments.
- Doc/process scores are judge-produced; judge must not see the oracle (agents/judge_instructions.md).
