# Judge step — produce doc_scores.jsonl & process_scores.jsonl

Code scoring is automated (`driver.py score`). Doc-quality and process-quality are judged separately —
by an independent LLM-judge agent (or a human), NOT by the dev-agent that produced the work, and NOT
with knowledge of the hidden oracle (judge from the run artifacts only).

## Inputs per run `runs/<mode>/<level>/<seed>/`
- `docs/` (ask-solo: `docs/ssot/*`; baseline-general: `docs/NOTES.md`)
- `conversation/sNN_log.md`
- `prompts/sNN_user_prompt.md`
- `scores/code_scores.jsonl` (for context: what actually passed/failed)

Do NOT read `eval/oracle/` or `eval/tests.py` (no oracle leakage into the judge).

## Produce
- One `doc_scores.jsonl` row per run, scoring the FINAL docs against `eval/rubric_doc.md`
  (5 dims, 0–3 each; include `total` and a 1–2 line `justification` per dim; set `judge`).
- One `process_scores.jsonl` row per session against `eval/rubric_process.md`
  (5 dims, 0–3 each; `total`; `note`; `judge`). Focus rigor on S5 (real change) and S6 (forgetting-drift).

Write rows with `driver`-compatible keys (see `eval/schemas/*.schema.json`). Then run
`python eval/judge.py validate` to confirm the rows are well-formed, and
`python eval/judge.py aggregate` to see the composite.

## Judging rules (plan §6)
- Reward usefulness to the NEXT session, not length or plausible prose.
- A necessary clarifying question is positive (process), an unnecessary one is negative (`over_questioning`).
- Silent compliance that broke a recorded policy (e.g. beginner/intermediate S6 blank→all) → `conflict_detection`=0.
- Correctly adopting the explicit S5 change is NOT a conflict-handling failure; stubbornly keeping the old
  raise behavior IS (it shows the agent can't tell intentional change from drift).
- Score baseline-general honestly: sparse NOTES and no conflict handling are the measured contrast.
