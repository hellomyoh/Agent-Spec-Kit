# runs/ — produced per run (plan §7)

`driver.py` creates this layout. Pilot uses `seed1`; other seeds are structure-only (set `SEED=...`).

```
runs/<mode>/<level>/<seed>/
  prompts/        s00_user_prompt.md ...        # the user prompt shown each session (copied by driver prepare)
  conversation/   s00_log.md ...                # the dev-agent's CONVERSATION.md per session (copied by score)
  work/           catalog.py, docs/, provided/  # the LIVE session workspace (rebuilt each prepare)
  <sNN>/          per-session snapshot           # catalog.py + docs/ frozen after score (the audit trail)
  docs/           latest docs/ (ssot/* or NOTES.md)
  scores/
    code_scores.jsonl       # automated (driver.py score)
    cost.jsonl              # edit_churn automated; tokens/turns/tool_calls/wall_time filled by orchestrator
    doc_scores.jsonl        # judge step (eval/rubric_doc.md)      — created during judging
    process_scores.jsonl    # judge step (eval/rubric_process.md)  — created during judging
  final_report.md           # optional per-run human summary
```

- `mode` ∈ {baseline-general, throughline-solo}; `level` ∈ {beginner, intermediate, advanced}.
- Seed1 pilot = 2×3×7 = 42 dev-agent sessions. Each session: `prepare` → fresh dev-agent edits `work/` → `score`.
- The dev-agent is sandboxed to `work/`. `eval/` is never copied here (oracle isolation).
- This directory is run output; safe to delete and regenerate. (Consider git-ignoring `runs/**/work/`.)
