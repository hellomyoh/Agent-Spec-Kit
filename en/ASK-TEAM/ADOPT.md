# ADOPT.md — Adopting an existing project (ASK-Team)

Apply ASK-Team to a project that already has code. Rather than from requirements, **analyze the existing code to reverse-document the current state** and set up a concurrent team-development structure.
The artifact structure is identical to [KICKOFF.md](KICKOFF.md), so once adoption is done, continue straight into development with [DEVELOP.md](DEVELOP.md).

> [CONVENTIONS.md](CONVENTIONS.md) takes precedence on conventions, [SCHEMAS.md](SCHEMAS.md) on schemas.
> For the **detailed method** of code reverse-documentation (state the range read·as-built spec·mark estimates), follow the solo kit [ADOPT.md](../AGENTSPECKIT/ADOPT.md) — here we specify **only the team-structure differences**.
> **This prompt is run by the maintainer.** At this stage, **do not modify code.**

---

# 1. Prerequisites check

1. If there are existing artifacts in `AGENTSPECKIT/`, it's **already adopted** → don't re-adopt, just report.
2. Inventory whether root `README`/`AGENTS.md`/`CLAUDE.md`/`.gitignore` exist. Don't overwrite existing files; merge or confirm before proceeding.
3. **Register maintainer** — register the runner as `team/<handle>.md` (`role: maintainer`). Confirm with `python askctl.py whoami`.

---

# 2. Adoption work order

1. **Code scan** — stack·build/run/test commands·structure·entry points·dependencies·environment variable **names** (don't collect values/secrets).
2. **Trace actual behavior** — read the core paths directly from the entry points. Don't guess from filenames·structure alone. State the range read/not read; leave unread areas as workitems (`status: proposed`, `title: "unread area ..."`).
3. **Reverse-extract cross-cutting contracts → `ARCHITECTURE.md`** (maintainer single-writer). For items not determinable from code, use `assumptions/ASM-*.md` (active, needs verification).
4. **As-built spec → `features/*.md`** — base each behavior claim on a code location (file/function). Don't assert behavior you didn't read directly; mark it "estimate (needs verification)". Separately mark code↔intent gap points.
5. **Actually run existing tests → record baseline (pass/fail/absent) in `history/YYYY/MM/HIST-*.md`**.
6. **Remaining/unimplemented work → decompose into `workitems/WI-*.md` (proposed)**, fill `touches`. Already-implemented things go as feature as-built; future things go as workitems.
7. If `SOURCES/REQUIREMENTS.md` exists, use it as future goals/unimplemented requirements. If it conflicts with as-built, ask. On adoption completion, register in `SRC-*.meta.md` and freeze as `applied`.
8. Reflect the current state in `PLAN.md` (stable roadmap) as done/in-progress/remaining. Write the `PROGRESS.md` compat stub ([KICKOFF.md](KICKOFF.md) §5).
9. Write/merge `AGENTS.md` (team conventions — KICKOFF §4)·`CLAUDE.md`. Exclude INDEX via `.gitignore`.
10. Run `python askctl.py index`.
11. Report adoption completion (below).

---

# 3. Completion conditions / report

* maintainer registered in `team/`, `askctl whoami` succeeds
* `ARCHITECTURE.md` (reverse-extracted)·as-built `features/*.md` (code-based)·test baseline (`history/`) created
* Unimplemented/unread work registered in `workitems/` (proposed, including `touches`)
* code↔intent gap list compiled
* `.gitignore`·`askctl index` applied

Report format:

```md
# Team adoption result
## Registered maintainer
## Range read / not read (→ workitem)
## Reverse-extracted ARCHITECTURE summary
## as-built feature list (code-based)
## code↔intent gap list
## Test baseline (commands run / results)
## Created initial workitems (touches) / PLAN reflection
## Next steps (DEVELOP.md guidance)
```

> Adoption is also multi-stage, so it can be interrupted. On interruption, take over from the index that `workitems/` and `history/`, and the `PROGRESS` stub point to.
