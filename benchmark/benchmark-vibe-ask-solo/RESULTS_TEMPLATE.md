# RESULTS — Vibe ASK-Solo Benchmark (seed1 pilot)  [TEMPLATE — fill after running]

Run date: ____ · dev-agent model: ____ · judge: ____ · seed: seed1
Scope run: ___ / 42 dev-agent sessions (2 modes × 3 levels × 7 sessions).

## 1. Harness status
- Stage -1 gate (`eval/_selftest.py`): PASS / FAIL
- `eval/judge.py validate`: clean / issues: ____

## 2. Code trajectory (from `driver.py aggregate`)
Per (mode/level), `func` / `inv_viol` / `regr` / `blank_ok` by session. Paste the aggregate JSON or table.

| mode/level | S0 | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|---|
| baseline-general/beginner | | | | | | | |
| ask-solo/beginner | | | | | | | |
| baseline-general/intermediate | | | | | | | |
| ask-solo/intermediate | | | | | | | |
| baseline-general/advanced | | | | | | | |
| ask-solo/advanced | | | | | | | |

## 3. The decisive S6 conflict (headline)
For each level, what did each mode do with a blank query at S6, and was it correct (oracle: preserve `[]`
for beginner/intermediate, blank→all for advanced)?

| level | baseline-general S6 | ask-solo S6 | oracle-correct? | ask-solo detected conflict? |
|---|---|---|---|---|
| beginner | | | | |
| intermediate | | | | |
| advanced | | | | |

## 4. S5 control (adopt the explicit change)
Did BOTH modes adopt unknown-field→ignore at s5+? (ask-solo must not stubbornly keep raising.) ____

## 5. Doc & process scores (judge)
- Doc totals (0–15) per mode/level: ____
- Process totals (esp. S5/S6) per mode/level: ____
- Did ask-solo's SSOT actually carry the S3 blank policy into S6? ____

## 6. Cost
- tokens / turns / tool calls / edit_churn per mode (esp. ask-solo overhead vs baseline): ____
- Composite (`eval/judge.py aggregate`): paste table.

## 7. Answers to plan §8 questions
Q1 beginner ASK gain? Q2 intermediate? Q3 advanced cost vs gain? Q4 ambiguity→drift?
Q5 ASK dampens drift? Q6 questions reduced rework? Q7 doc quality→fewer late violations?

## 8. Go / No-Go verdict (PREREGISTRATION §)
[ ] Go  [ ] Revise prompts  [ ] Revise task  [ ] Revise ASK docs  [ ] Stop/narrow claim — because: ____

## 9. Honest limitations
Single seed; one task; judge subjectivity; any oracle/discrimination caveats observed.

## 10. Next
Seed expansion (`SEED=seed2 ...`), second task, or task/prompt revisions per the verdict.
