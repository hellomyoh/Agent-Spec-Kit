# KICKOFF.md — Team project initialization (ASK-Team)

Initialize a project into a **state ready for concurrent team development**, based on `SOURCES/REQUIREMENTS.md` (initial requirements).
The goal of this stage is not actual development, but to build the **coordination structure + initial artifacts** so that multiple contributors can claim·progress work without conflict.

> [CONVENTIONS.md](CONVENTIONS.md) takes precedence on conventions, [SCHEMAS.md](SCHEMAS.md) on schemas.
> For the **detailed format** of feature-spec/persona/QA documents, follow §6·§8 of the solo kit [KICKOFF.md](../AGENTSPECKIT/KICKOFF.md) as-is — here we specify **only the team-structure differences**.

> **No re-initialization:** if REQUIREMENTS' status in `SOURCES/INDEX.md` is already `applied`, do not run KICKOFF again.
> **This prompt is run by the maintainer** (initialization = fixing global contracts·structure).

---

# 1. Structure to create

Except for the root 3 files (project `README.md`·`AGENTS.md`·`CLAUDE.md`), create everything under `AGENTSPECKIT/`.

```text
AGENTSPECKIT/
  KICKOFF.md ADOPT.md DEVELOP.md INTEGRATE.md AUDIT.md   # copied prompts
  askctl.py  .gitignore
  ARCHITECTURE.md  PLAN.md  PROGRESS.md(compat stub)
  team/        <maintainer-handle>.md                    # ★ at least 1 (the initializer) registered
  workitems/   WI-*.md                                   # initial work breakdown (status: proposed)
  conflicts/                                             # empty folder
  sessions/    archive/                                  # empty folder
  history/                                               # empty folder
  assumptions/ ASM-*.md                                  # initial autonomous judgments
  notes/                                                 # empty skeleton
  SOURCES/     REQUIREMENTS.md  SRC-*.md  SRC-*.meta.md
  features/*.md  personas/*.md  discussion/  adr/ADR-*.md  docs/  qa/
  templates/
```

* Don't create any `INDEX.md` by hand — `python askctl.py index` generates them (§7).
* Don't create the solo kit's single files (`HISTORY.md`/`ASSUMPTIONS.md`/`NOTES.md`/`TODO.md`). Each is replaced by `history/`·`assumptions/`·`notes/`·workitem `proposed` respectively.

---

# 2. Requirements clarification / AI delegation

Follow §2 of the solo kit [KICKOFF.md](../AGENTSPECKIT/KICKOFF.md) (question criteria·defaults·`[AI delegation]` handling) as-is.
**Team difference:** decisions adopted via autonomous judgment are recorded not in a single `ASSUMPTIONS.md` but as **individual files** `assumptions/ASM-*.md` (including the `scope` field — for conflict checking).

---

# 3. Initialization work order

Update progress at the end of each step. If initialization is interrupted, the next session takes over (state is read from the index that `workitems/` and the `PROGRESS.md` stub point to).

1. **Register maintainer** — register the initializer as `team/<handle>.md` (`role: maintainer`). Confirm git identity matching with `python askctl.py whoami`.
2. Analyze `SOURCES/REQUIREMENTS.md` — set the `SRC-*.meta.md` status to `under_review`. If there are other submitted materials, register them too.
3. Confirm whether mandatory requirements are met / ask if ambiguous (§2).
4. Organize project purpose·scope.
5. **Cross-cutting contracts → `ARCHITECTURE.md`** draft (maintainer single-writer domain).
6. Separate MVP/later priorities.
7. Decompose into feature units → `features/*.md` (format per solo 6.1) + review non-trivial features via `personas/`+`discussion/` (solo §4·§5).
8. **Work breakdown → `workitems/WI-*.md`** (status: `proposed`). Fill each WI's `touches` (contracts/modules)·`feature`·`source_refs`. The initial backlog is the workitem list.
9. Write QA documents (`qa/`) (format per solo §8).
10. Write user docs (`docs/`).
11. Important design decisions → `adr/ADR-<YYYYMMDD>-<slug>.md` + INDEX (generated).
12. Finalize `ARCHITECTURE.md`.
13. Draft the project `README.md` (root).
14. **Write `AGENTS.md`** (root) — including the team conventions (§4 below).
15. Write `PLAN.md` (stable roadmap — Phase level only; work status is held by workitems).
16. Write the `PROGRESS.md` compat stub (§5).
17. Initial autonomous judgments → `assumptions/ASM-*.md`.
18. Set the REQUIREMENTS status in `SOURCES/SRC-*.meta.md` to `applied` (**freeze point**), link applied artifacts.
19. Write `CLAUDE.md` (root — solo §11 malfunction-prevention + team items: "global contracts are maintainer-only, don't touch INDEX").
20. **Check `.gitignore`** — exclude every `INDEX.md`.
21. Run `python askctl.py index` → generate the index.
22. Report initialization completion (§8).

---

# 4. Team conventions to include in AGENTS.md

In addition to the solo kit §9·§10 content, **you must** include:

```text
- Roles: maintainer (global contracts·INTEGRATE·arbitration) / contributor (workitem claim·work). Confirm role with `askctl whoami` at session start.
- Identity: anchored to git identity. owner is the handle in team/<handle>.md. Session-Id / Co-Authored-By trailers on commits.
- Progress: not PROGRESS.md but workitems/WI-*.md (+generated INDEX). The session cursor is sessions/<handle>--<WI-id>.md.
- Conflicts: `askctl detect <WI-id>` right after claim·right before integrate. contracts overlap=STOP, modules overlap=register conflicts/CF.
- Global contracts (ARCHITECTURE/PLAN): maintainer single-writer. Changes via ADR + detect notice + merge-first (serialization).
- INDEX.md: generated, untracked by git. Don't touch. Run `askctl index` first at session start.
- Atomic commit: only code + that workitem's work-scoped files. Exclude ARCHITECTURE/PLAN/history/INDEX.
- New event = new file: don't append to history/assumptions/conflicts, create a file.
- Integration is done by the maintainer via INTEGRATE.md. Contributors go up to PR.
```

---

# 5. PROGRESS.md compat stub

```md
# Progress (multi-worker mode)

The truth of progress is not this file but the indexes below. Don't record work directly in this file.

- workitems/INDEX.md  — work status (generated by `askctl index`)
- sessions/INDEX.md   — per-session resume cursor
- history/INDEX.md     — completion history

Session start: `python AGENTSPECKIT/askctl.py whoami && python AGENTSPECKIT/askctl.py index`
```

---

# 6. Multi-Agent review / personas / feature specs

Follow solo kit §4·§5·§6 as-is (`personas/` instances, `discussion/` logs, feature document structure·review summary·source obligations). These artifacts are file-level on a team too, so they're concurrency-safe.

---

# 7. Index generation

`python askctl.py index` generates the INDEX.md of `workitems`·`conflicts`·`team`·`sessions`·`history`·`assumptions`·`notes`·`SOURCES` from frontmatter. Don't create or edit them by hand (they get overwritten). They are not committed to git (`.gitignore`).

---

# 8. Completion conditions / report

* At least 1 maintainer registered in `team/`, `askctl whoami` succeeds
* `ARCHITECTURE.md`·`PLAN.md`·project `README.md`·`AGENTS.md`·`CLAUDE.md` created
* `features/*.md` (+ `discussion/` logs for non-trivial features)·`qa/`·`docs/`·`adr/` created
* **Initial `workitems/WI-*.md` (status: proposed) created, each `touches` filled**
* REQUIREMENTS in `SOURCES/` frozen as `applied`, `SRC-*.meta.md` written
* INDEX excluded via `.gitignore`, `askctl index` run once successfully

Report format:

```md
# Team project initialization result
## Registered team members / roles
## Created structure / cross-cutting contracts (ARCHITECTURE) summary
## Feature-spec list / initial workitem list (including touches)
## ADR / QA / docs list
## Items decided via AI delegation (review recommended)
## Next steps (first claim candidates / DEVELOP.md guidance)
```
