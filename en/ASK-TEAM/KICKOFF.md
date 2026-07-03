# KICKOFF.md — Team project initialization (ASK-Team)

Initialize a project into a **state ready for concurrent team development**, based on `SOURCES/REQUIREMENTS.md` (initial requirements).
The goal of this stage is not actual development, but to build the **coordination structure + initial artifacts** so that multiple contributors can claim·progress work without conflict.

> [CONVENTIONS.md](CONVENTIONS.md) takes precedence on conventions, [SCHEMAS.md](SCHEMAS.md) on schemas.
> For the **detailed format** of feature-spec/persona/QA documents, follow §6·§8 of the solo kit KICKOFF.md as-is ([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md) — bundled reference copy; on conflict the team kit wins) — here we specify **only the team-structure differences**.
> This kit uses markdown + git only (no additional runtime). The "identity check"·"reading the listing" are performed directly by the agent using `git` and file reads.

> **No re-initialization:** if REQUIREMENTS' status (`SOURCES/REQUIREMENTS.meta.md`) is already `applied`, do not run KICKOFF again.
> **This prompt is run by the maintainer** (initialization = fixing global contracts·structure).

---

# 1. Structure to create

Except for the root 3 files (project `README.md`·`AGENTS.md`·`CLAUDE.md`), create everything under `AGENTSPECKIT/`.

```text
AGENTSPECKIT/
  KICKOFF.md ADOPT.md DEVELOP.md INTEGRATE.md AUDIT.md   # copied prompts (markdown only)
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
  reference/                                             # bundled solo-kit reference copies (not executable prompts)
```

* **Don't create fixed INDEX files.** Each directory's listing·status has the item file's frontmatter as its SoT, and the agent reads it directly (§7).
* Don't create the solo kit's single files (`HISTORY.md`/`ASSUMPTIONS.md`/`NOTES.md`/`TODO.md`). Each is replaced by `history/`·`assumptions/`·`notes/`·workitem `proposed` respectively.
* Git does not track empty directories — put a `.gitkeep` (empty file) in directories that start empty (`conflicts/`, `sessions/archive/`, `history/`, `notes/`, `discussion/`) so the structure survives commit/clone.

---

# 2. Requirements clarification / AI delegation

Follow §2 of the solo kit KICKOFF.md ([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md)) (question criteria·defaults·`[AI delegation]` handling) as-is.
**Team difference:** decisions adopted via autonomous judgment are recorded not in a single `ASSUMPTIONS.md` but as **individual files** `assumptions/ASM-*.md` (including the `scope` field — for conflict checking).

---

# 3. Initialization work order

Update progress at the end of each step. If initialization is interrupted, the next session takes over by reading `workitems/` and the `PROGRESS.md` stub.

1. **Register maintainer** — register the initializer as `team/<handle>.md` (`role: maintainer`). Confirm that `git config user.email` is in that file's `emails` (identity matching).
2. Analyze `SOURCES/REQUIREMENTS.md` — create `SOURCES/REQUIREMENTS.meta.md` (`id: REQUIREMENTS` — SCHEMAS §source) and set its status to `under_review`. If there are other submitted materials, register them too (`SRC-*.md` + `SRC-*.meta.md`).
3. Confirm whether mandatory requirements are met / ask if ambiguous (§2).
4. Organize project purpose·scope.
5. **Cross-cutting contracts → `ARCHITECTURE.md`** draft (maintainer single-writer domain).
6. Separate MVP/later priorities.
7. Decompose into feature units → `features/*.md` (skeleton in §6.1; details solo 6.1) + review non-trivial features via `personas/`+`discussion/` (solo §4·§5 — see §6).
8. **Work breakdown → `workitems/WI-*.md`** (status: `proposed`). Fill each WI's `touches` (contracts/modules)·`feature`·`source_refs`. The initial backlog is the workitem list.
9. Write QA documents (`qa/`) (format per solo §8).
10. Write user docs (`docs/`).
11. Important design decisions → `adr/ADR-<YYYYMMDD>-<slug>.md`.
12. Finalize `ARCHITECTURE.md`.
13. Draft the project `README.md` (root).
14. **Write `AGENTS.md`** (root) — including the team conventions (§4 below).
15. Write `PLAN.md` (stable roadmap — Phase level only; work status is held by workitems).
16. Write the `PROGRESS.md` compat stub (§5).
17. Initial autonomous judgments → `assumptions/ASM-*.md`.
18. Set the status in `SOURCES/REQUIREMENTS.meta.md` to `applied` (**freeze point**), link applied artifacts.
19. Write `CLAUDE.md` (root — solo §11 malfunction-prevention ([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md)) + team items: "global contracts are maintainer-only, progress state is in the workitems frontmatter").
20. Commit the initialization artifacts (§3.1).
21. Report initialization completion (§8).

## 3.1 Branch·commit rules for initialization

* Initialization is performed by the maintainer **on the shared branch** (CONVENTIONS §4.5 — for a new repository, the default branch; if the shared branch is push-protected, initialize the designated `coordination` branch instead and record it in AGENTS.md).
* Initialization ends with **a commit** bundling all generated artifacts (the three root files + AGENTSPECKIT/), pushed if a remote exists — contributors can only see the coordination layer once it is on the shared branch, so **claims cannot start before this commit**.
* If initialization spans multiple sessions, interim milestone commits are allowed (e.g., after ARCHITECTURE/features are complete).

---

# 4. Team conventions to include in AGENTS.md

In addition to the solo kit §9·§10 content, **you must** include:

```text
- No runtime: this kit uses markdown + git only. It requires no additional tool·binary.
- Roles: maintainer (global contracts·INTEGRATE·arbitration) / contributor (workitem claim·work). Confirm identity at session start.
- Identity: anchored to git identity. The agent matches `git config user.email` against the emails in team/<handle>.md. owner is the handle. Session-Id / Co-Authored-By trailers on commits.
- Progress: not PROGRESS.md but the workitems/WI-*.md frontmatter (no fixed INDEX — read directly). The session cursor is sessions/<handle>--<WI-id>.md.
- Shared branch: <name decided at KICKOFF — default branch or 'coordination'> (CONVENTIONS §4.5). Coordination files (workitems/conflicts/team/personas) are committed·pushed directly on it; code arrives only via PR. WI files are edited only on the shared branch.
- Conflicts: right after claim·right before integrate, git fetch first, then read the latest shared branch's workitems/*.md (claimed/in_progress) and cross-check touches. contracts overlap=STOP, modules overlap=register conflicts/CF.
- Global contracts (ARCHITECTURE/PLAN): maintainer single-writer. Changes via ADR + detection notice + merge-first (serialization).
- Read the listing directly from frontmatter. Don't create fixed INDEX files. If a human-readable table is needed, generate one then to show but don't commit it as a file.
- Atomic commit: only code + that workitem's work-layer files. Exclude ARCHITECTURE/PLAN/history.
- New event = new file: don't append to history/assumptions/conflicts, create a file.
- Integration is done by the maintainer via INTEGRATE.md. Contributors go up to PR.
```

---

# 5. PROGRESS.md compat stub

```md
# Progress (multi-worker mode)

The truth of progress is not this file but the frontmatter in each item file. Don't record work directly in this file.
We don't keep fixed INDEX files — the agent reads the *.md frontmatter of the directories below directly.

- workitems/*.md   — work status (SoT)
- sessions/*.md    — per-session resume cursor
- history/**       — completion history

Session start: the agent confirms identity via `git config user.email` and reads the item files it needs for the current task directly.
```

---

# 6. Multi-Agent review / personas / feature specs

Follow solo kit §4·§5·§6 as-is ([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md)) — `personas/` instances, `discussion/` logs, feature document structure·review summary·source obligations. These artifacts are file-level on a team too, so they're concurrency-safe.

**Exception (no fixed INDEX — CONVENTIONS §3):** do **not** create the listing-index files those solo sections mandate — `personas/INDEX.md` (solo 5.2), `features/README.md` (solo 6.2), `docs/README.md` (solo 7.2), `adr/INDEX.md` (solo §16) — nor apply their "update the index in the same commit" rules. The listing is read directly from the files; work status lives in the workitem frontmatter. (`qa/README.md` — QA operating standards, not a listing — is still written.)

In a subagent-capable environment, review core features via **actual parallel subagents** (execution mode·per-subagent evidence per solo 4.1). New persona instances are created **on the shared branch** — `git fetch` first and check the role doesn't already have an instance (CONVENTIONS §1·§4.5).

## 6.1 Feature-document skeleton (inline)

```md
# Feature: <name>
## 1. Purpose        ## 2. Scope (In / Out of scope)        ## 3. User scenarios
## 4. Final agreed proposal (+ review summary: participating personas · key issues · 3–4-line conclusion · discussion log link)
## 5. Functional requirements        ## 6. Non-functional requirements
## 7. Data design    ## 8. API design    ## 9. UI/UX design    (each: `Not applicable` if none; common rules → reference ARCHITECTURE.md)
## 10. Security requirements         ## 11. Log / analytics requirements
## 12. Test scenarios (automated / manual QA / exception cases / regression impact)
## 13. Completion criteria (must include "the relevant automated tests actually ran and passed")
## 14. Referenced ADRs               ## 15. Open issues
```

(Full per-section guidance: solo 6.1 in the reference copy.)

---

# 7. Reading the listing·status (no fixed INDEX)

We don't keep a separate INDEX file for progress·the work list. The agent **reads the `*.md` frontmatter directly** from directories like `workitems/`·`assumptions/`·`history/`·`SOURCES/`·`team/` to understand them (selective loading — only what's needed). If you need a human-readable aggregate table, ask the agent at that point and receive it as markdown (don't force-generate·commit it as a file — eliminates staleness·concurrent-edit conflicts at the source).

---

# 8. Completion conditions / report

* At least 1 maintainer registered in `team/`, `git config user.email` matches that file
* `ARCHITECTURE.md`·`PLAN.md`·project `README.md`·`AGENTS.md`·`CLAUDE.md` created
* `features/*.md` (+ `discussion/` logs for non-trivial features)·`qa/`·`docs/`·`adr/` created
* **Initial `workitems/WI-*.md` (status: proposed) created, each `touches` filled**
* REQUIREMENTS in `SOURCES/` frozen as `applied` (`SOURCES/REQUIREMENTS.meta.md` written)
* No fixed listing-INDEX files created (personas/features/docs/adr — §6 exception)
* Initialization committed on the shared branch (§3.1), `.gitkeep` in empty directories

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
