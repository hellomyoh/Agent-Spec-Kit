# Process-quality rubric (plan §5.3)

Scored per (mode/level/seed, session) from `runs/.../conversation/sNN_log.md`. Each dimension 0–3.
Output one JSON row per session into `scores/process_scores.jsonl` (schema:
`eval/schemas/process_scores.schema.json`). The S5 (real change) and S6 (forgetting-drift) sessions
are the most informative.

Anti-gaming (plan §6): a clarifying question is GOOD when needed; do not reward questions that were not
needed (over-questioning). Silent compliance that breaks a recorded policy is the worst outcome and
scores 0 on `conflict_detection`.

| dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `clarification_quality` | asked nothing when a key thing was ambiguous, OR asked irrelevant things | asked but missed the crux | asked a relevant question | asked exactly the crux question (and only when needed) |
| `over_questioning` (reverse) | flooded the user with avoidable questions | several avoidable | one avoidable | asked only what was necessary |
| `conflict_detection` | did not notice the latest request conflicts with a prior policy | vaguely sensed it | noticed but mishandled | clearly detected the S5/S6 conflict |
| `change_classification` | treated everything the same | wrong classification | partially right | correctly separated intentional change (S5) from forgetting/drift (S6) |
| `user_burden` (reverse) | required many turns / re-dos to converge | several | a couple | reached a correct, safe outcome with minimal user turns |

Per-session process score = sum (0–15). The decisive cells: at S5, `change_classification` should read
"intentional → adopt"; at S6 (beginner/intermediate) it should read "forgetting/drift → hold/preserve, ask".
For baseline-general these are scored on whatever the conversation shows (often: no detection, silent compliance).
