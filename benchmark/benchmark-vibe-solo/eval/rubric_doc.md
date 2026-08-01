# Doc-quality rubric (plan §5.2)

Scored per run (per mode/level/seed), judging the FINAL docs (`runs/.../docs/`): for throughline-solo the
`docs/ssot/*`; for baseline-general the `docs/NOTES.md` (often sparse — that is a valid low score, not a bug).
Each dimension 0–3. Output one JSON row per dimension-set into `scores/doc_scores.jsonl` (schema:
`eval/schemas/doc_scores.schema.json`).

Anti-gaming (plan §6): do NOT reward length or plausible-looking prose. Reward only what would help the
NEXT session's agent do the right thing. A short correct note beats a long vague one.

| dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `ssot_completeness` | no usable record | goals OR features only | most of goals/features/decisions/progress | goals, features, the key policies (unknown-field, blank-query), decisions, progress all present and current |
| `authority_clarity` | no notion of authority | implicit only | states decisions but not their precedence vs latest chat | clearly: recorded decisions are authority; latest chat is checked against them; supersede chain visible |
| `update_correctness` | docs contradict code | stale in places | mostly matches code | docs match the final code behaviour (incl. S5 supersede, S6 resolution) |
| `no_fake_certainty` | asserts unverified things as fact | some | mostly grounded | no invented certainty; unconfirmed items marked as assumption/needs-confirmation |
| `reuse_value` | useless next session | minimal | usable with effort | a next-session agent could resolve the S6 conflict correctly using these docs alone |

Total doc score = sum (0–15). Record the per-dimension scores and a 1–2 line justification each.
Baseline-general typically scores low on completeness/authority by design — that is the measured contrast,
not a penalty to invent.
