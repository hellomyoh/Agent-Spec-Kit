# Vibe ASK-Solo Benchmark

Implements `BENCHMARK-PLAN-VIBE-ASK-SOLO.md` (repo root) as a runnable file structure.

**Hypothesis.** In vibe-coding, users give incomplete/inconsistent instructions and forget their own
past intent. ASK-solo (feature spec + SSOT docs + a conflict-handling discipline) should beat plain
"general" progress on goal attainment, code quality, drift suppression, and rework — **most at
beginner/intermediate prompt levels, least at advanced** (where the user already states everything).

We measure four axes together: **code tests, doc quality, conversation process, cost** (plan §1, §5).

## Design (fixed before running — see PREREGISTRATION.md)

- **One task**: `catalog` (a tiny in-memory product search lib; `add/all/search`). Same hidden oracle for all levels.
- **3 prompt levels** × **2 modes** × **7 sessions (s0–s6)**.
  - Levels (`tasks/catalog/prompts/{beginner,intermediate,advanced}/sNN.md`) differ only in how explicit
    the user is — they drive toward the SAME canonical behavior (`eval/oracle/policies.md`).
  - Modes: `baseline-general` (no SSOT, just build the request) vs `ask-solo` (maintain SSOT + run a
    conflict check). Mode behavior is defined by `agents/dev_<mode>.md`.
- **The two conflicts** (plan §4.5):
  - **S5 — real intentional change** (explicit in all levels): unknown `where` field: *raise* → *ignore*.
    Correct = adopt (both modes). Tests that ask-solo doesn't *stubbornly* keep an old decision.
  - **S6 — forgetting / ambiguous drift** (the discriminator): "show everything when the search box is
    empty" — conflicts with the S3 safety policy (blank query → `[]`). Level-aware correct answer:
    beginner/intermediate → **preserve** `[]` (the user forgot; silent compliance = drift); advanced →
    **adopt** blank→all (the user explicitly, knowingly overrides). ask-solo's SSOT records the S3
    decision so it can resist the drift; baseline-general has no such record.

## Layout

```
benchmark-vibe-ask-solo/
  README.md  PREREGISTRATION.md  RESULTS_TEMPLATE.md
  driver.py                       # prepare / score / aggregate / init
  agents/                         # dev-agent prompt templates per mode + judge instructions
    dev_baseline-general.md  dev_ask-solo.md  judge_instructions.md
  tasks/catalog/
    provided/contract.py          # pinned API (given to the agent each session)
    prompts/{beginner,intermediate,advanced}/s00..s06.md
  eval/
    oracle/policies.md            # HIDDEN ground truth (never given to dev-agent)
    tests.py                      # hidden battery (level/session aware; no oracle leak)
    rubric_doc.md  rubric_process.md
    schemas/{code,doc,process,cost}_scores.schema.json
    judge.py                      # validate score JSONL + aggregate composite
    ref_correct/ negative_controls/ _selftest.py   # Stage -1 harness gate
  runs/<mode>/<level>/<seed>/      # produced per run (see runs/README.md)
```

## How to run (orchestrator loop — seed1 pilot)

The driver does plumbing + automated code scoring; the ORCHESTRATOR runs a fresh dev-agent per session.

```
cd benchmark-vibe-ask-solo
PYTHONIOENCODING=utf-8 python eval/_selftest.py          # Stage -1 gate (must pass)

# for each mode in {baseline-general, ask-solo}, level in {beginner,intermediate,advanced}, n in 0..6:
PYTHONIOENCODING=utf-8 python driver.py prepare <mode> <level> <n>
#   -> run a FRESH dev-agent whose prompt is agents/dev_<mode>.md, sandboxed to
#      runs/<mode>/<level>/seed1/work/  (it edits catalog.py, docs/, writes CONVERSATION.md)
PYTHONIOENCODING=utf-8 python driver.py score   <mode> <level> <n>

# after all sessions: judge docs/process (agents/judge_instructions.md) -> doc_scores.jsonl, process_scores.jsonl
PYTHONIOENCODING=utf-8 python eval/judge.py validate
PYTHONIOENCODING=utf-8 python driver.py aggregate        # per-session code trajectory
PYTHONIOENCODING=utf-8 python eval/judge.py aggregate     # end-state weighted composite
```

That is `2 modes × 3 levels × 7 sessions = 42 dev-agent sessions` for the seed1 pilot.

**Oracle isolation:** the dev-agent is sandboxed to its `work/` dir; `eval/` (oracle, tests, scorer) is
never copied in. Test failures surface only failing check NAMES (`public_qa`), never expected values.

**Seeds:** pilot = `seed1` (default). Seed expansion is structure-only: set `SEED=seed2` (etc.) and re-run
the same loop; analysis stays the same. Do NOT scale seeds before the seed1 dry-run validates discrimination.

## Scoring (plan §6 weights)

| axis | weight | source |
|---|---:|---|
| code tests / hidden invariant | 45 | automated (`driver.py score` → `code_scores.jsonl`) |
| goal / product-intent maintained | 20 | automated (decisive invariant checks at final session) |
| doc quality / SSOT usefulness | 15 | judge (`rubric_doc.md` → `doc_scores.jsonl`) |
| conversation process / question quality | 10 | judge (`rubric_process.md` → `process_scores.jsonl`) |
| cost efficiency | 10 | `cost.jsonl` (edit_churn automated; tokens/turns from orchestrator) |

`eval/judge.py aggregate` combines whatever exists and marks the rest PENDING.

## What this can / cannot show
Can: whether ask-solo helps on sparse/ambiguous prompts, whether it curbs intent-drift, at which user
level it pays off, whether its doc cost is offset. Cannot: that ASK wins on all tasks, Team/multi-agent
effects, whole-model performance, or guaranteed product quality (plan §12).
