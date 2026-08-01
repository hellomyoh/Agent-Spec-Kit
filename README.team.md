<div align="center">

# THROUGHLINE — Team edition

**Spec-Driven Development when several developers and AI agents share one codebase**

Every workitem declares what it touches, published to a shared branch at claim
time — so Git, semantic, and intent conflicts surface early instead of at merge.

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Claude Code · Codex · Cursor](https://img.shields.io/badge/agents-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor-blue)](#quick-start)

🌐 **English** · [한국어](README.team.ko.md)

[Quick start](#quick-start) · [Solo edition](README.md) · [Full team guide & prompts](en/THROUGHLINE-TEAM/) · [한국어 키트](ko/THROUGHLINE-TEAM/)

</div>

---

## Solo or Team?

| | **Solo (THROUGHLINE)** — [README.md](README.md) | **Team (THROUGHLINE Team)** — this guide |
|---|---|---|
| For | 1 developer / sequential, autonomous | multiple developers & AI agents, **concurrent** |
| Progress | single `PROGRESS.md` cursor | `workitems/` + `sessions/<handle>--<WI>` |
| History / assumptions / notes | single files | `history/` · `assumptions/` · `notes/` directories |
| Indexes | hand-updated | none — frontmatter read directly |
| Conflicts | n/a | `touches` + `conflicts/` (agent cross-checks) |
| Identity | not needed | `team/` + git identity (`git config user.email`) |
| Runtime | none | none (markdown + git only) |
| Kit folder | `en/THROUGHLINE/` · `ko/THROUGHLINE/` | `en/THROUGHLINE-TEAM/` · `ko/THROUGHLINE-TEAM/` |

For a single developer, Solo is lighter — use Team only when N people actually develop concurrently.

## Core ideas

- **Git branch isolation is the root fact.** Contributors can't see each other's *uncommitted* files, so a workitem's coordination metadata (its `touches`) is **published to a shared branch at claim time** → conflicts surface early, not at merge.
- **Two artifact layers.** *Coordination* (workitems, conflicts, `ARCHITECTURE.md`/`PLAN.md`) lives on the shared branch; *work* (code, feature specs, qa, notes, assumptions) lives on the isolated feature branch.
- **Roles.** A **Maintainer** owns the global contracts, runs `INTEGRATE`, and arbitrates intent conflicts as ADRs. **Contributors** claim workitems and own their scoped files.
- **No fixed INDEX files.** Each item file's frontmatter is the source of truth and the agent reads directories directly — so concurrent index-edit conflicts simply don't exist.
- **Identity = git identity.** `git config user.email` validated against a `team/<handle>.md` registry — no extra runtime.

## Quick start

1. Clone this repo and copy the contents of [`en/THROUGHLINE-TEAM/`](en/THROUGHLINE-TEAM/) (or [`ko/THROUGHLINE-TEAM/`](ko/THROUGHLINE-TEAM/)) into your project root's `THROUGHLINE/`.
2. For a **new project**, write the initial requirements in `THROUGHLINE/SOURCES/REQUIREMENTS.md` (reuse the solo kit's [REQUIREMENTS template](en/THROUGHLINE/SOURCES/REQUIREMENTS.md)); for an existing codebase (ADOPT) it is optional.
3. The **maintainer** registers `team/<handle>.md` with `role: maintainer` (copy `templates/team-TEMPLATE.md`); each **contributor** registers their own.
4. Contributors run the [`DEVELOP.md`](en/THROUGHLINE-TEAM/DEVELOP.md) prompt; the maintainer runs [`INTEGRATE.md`](en/THROUGHLINE-TEAM/INTEGRATE.md). Use [`KICKOFF.md`](en/THROUGHLINE-TEAM/KICKOFF.md) (new) / [`ADOPT.md`](en/THROUGHLINE-TEAM/ADOPT.md) (existing code) to initialize, and [`AUDIT.md`](en/THROUGHLINE-TEAM/AUDIT.md) for periodic checks.

## Development prompt — claim → detect → implement → PR (DEVELOP · contributor)

Once initialization (or adoption) has been committed to the shared branch, each contributor uses this prompt to **perform one workitem**. Before running, your own `team/<handle>.md` must be registered (if not, the prompt registers it first). Only the contributor runs it; the maintainer merges via [`INTEGRATE.md`](en/THROUGHLINE-TEAM/INTEGRATE.md).

```text
Read AGENTS.md and THROUGHLINE/DEVELOP.md, and following the DEVELOP.md procedure, claim one workitem and develop it.
Conventions in THROUGHLINE/CONVENTIONS.md take precedence. This kit uses markdown + git only.

Proceed strictly in the following order.

0. Identity check: match git config user.email against the emails in team/*.md to confirm my handle·role.
   If unregistered, register team/<handle>.md first (templates/team-TEMPLATE.md), then proceed.
   Then git fetch, and read the latest shared branch's workitems/*.md frontmatter to see in-flight (claimed/in_progress) work and its touches.
1. Always load: AGENTS.md (root), THROUGHLINE/ARCHITECTURE.md (cross-cutting contracts), THROUGHLINE/PLAN.md, in-flight workitems frontmatter.
   Read the features/*.md·ADR·qa·notes needed for my work optionally. For common rules always follow ARCHITECTURE.md as the baseline.
2. Claim a workitem:
   - Existing item: pick a WI with status: proposed|ready, set owner to my handle, status to claimed, branch to feat/<WI-id>, and
     commit only this change on the shared branch and push (before code work — publishing).
   - New item: copy templates/WI-TEMPLATE.md to workitems/WI-<YYYYMMDD>-<slug>.md, fill touches (contracts/modules) without fail, then
     commit·push on the shared branch.
3. Conflict detection (mandatory right after claim): git fetch, then read the latest shared branch's workitems/*.md with status ∈ {claimed, in_progress} and cross-check against my touches.
   - contracts overlap = STOP: do not proceed; ask the maintainer to serialize (see 7 below). If it's a contract change, go via ADR.
   - modules overlap = WARN: register conflicts/CF-*.md (templates/CF-TEMPLATE.md) and agree on order with the other owner.
   - independent = OK: proceed.
4. Development (feature branch): git checkout -b feat/<WI-id>. Create sessions/<handle>--<WI-id>.md and update "Next first command".
   - Set WI status to in_progress and commit·push on the shared branch (WI files are edited only on the shared branch).
   - Check the features/*.md spec and ARCHITECTURE.md contracts (if absent, start from the spec; review non-trivial features via personas/+discussion/) and implement.
   - Write automated tests and actually run them (capture commands·results). Don't claim passing without running.
   - Handle code↔spec mismatch with an authority diagnosis (decide which side is authoritative first; don't arbitrarily edit the spec to erase the mismatch).
   - Record autonomous judgments as new assumptions/ASM-*.md files, and facts you learned in notes/<topic>.md (guesses go to assumptions).
   - If a global contract (ARCHITECTURE.md) must change, don't edit it directly — treat it as a STOP cause and follow step 7.
5. Atomic commit: bundle code + that workitem's work-layer files (features/qa/assumptions/notes/sessions) only into one commit.
   Exclude ARCHITECTURE/PLAN (maintainer)·history (INTEGRATE)·workitems/WI-* (coordination layer).
   Add Session-Id: <YYYY-MM-DDThhmm>-<handle>-<WI-id> and Co-Authored-By: <agent runtime> trailers to the commit message.
   Do not push code directly to main/master/the shared branch (PR only). But coordination-layer files are pushed directly on the shared branch. No committing .env·secrets.
6. Submit for review: set WI status to review and commit·push on the shared branch, push feat/<WI-id>, then create a PR.
   In the PR body state the WI-id, change summary, test results, touches, and unresolved conflicts/. The merge is done by the maintainer in INTEGRATE.
7. If STOP/serialization is needed: write a dedicated workitem declaring the contract-change intent via touches.contracts + adr/ADR-*.md (Proposed) and
   ask the maintainer to serialize. After the maintainer merges the contract first and updates ARCHITECTURE, rebase my workitem onto the new contract.

When done, report in the format below.
# Development result (WI-<id>)
## Work done / changed files
## Test results (commands run / pass·fail)
## touches (contracts / modules) and detection result
## Registered conflicts / assumptions / notes
## Git (branch / commit / PR)
## Next first command (= the update to sessions/<handle>--<WI-id>.md)
```

> To continue the same workitem in a later session, run the same prompt — the agent reads the "Next first command" in `sessions/<handle>--<WI-id>.md` and resumes from where it left off.

## Kit upgrade (applying a new version to an already-initialized team project)

Use this to reflect template-repository updates into a project that already ran KICKOFF/ADOPT. **Don't re-run KICKOFF or ADOPT** — the re-initialization/re-adoption guard blocks them, and bypassing it overwrites coordination-layer content. **Only `role: maintainer` runs this** (it rewrites kit-owned files and the root rule files — both maintainer-only domains).

| Category | Target | Processing |
|---|---|---|
| Kit-owned (no project content) | `KICKOFF.md`·`ADOPT.md`·`DEVELOP.md`·`INTEGRATE.md`·`AUDIT.md`·`CONVENTIONS.md`·`SCHEMAS.md`·`README.md`·`templates/`·`reference/` | **Overwrite-copy** from the same-version, same-language kit folder |
| Coordination/work artifacts (project content) | `ARCHITECTURE.md`, `PLAN.md`, `workitems/`, `conflicts/`, `team/`, `sessions/`, `history/`, `assumptions/`, `notes/`, `SOURCES/` originals, `features/`, `personas/`, `discussion/`, `adr/`, `docs/`, `qa/` | **Preserve content** — do not touch |
| Root rule files | `AGENTS.md` | **Merge-update** — add only missing team-convention blocks |
| | `CLAUDE.md` | **Replace** with the new KICKOFF.md template (malfunction-prevention only) — lossless gate |
| New structure (absent in the old version) | e.g. `workitems/archive/` | **Newly create** (`.gitkeep` if empty) and **migrate qualifying existing data** into it |

**Step 1 (human, maintainer):** pull the template repository and overwrite-copy the kit-owned files above **from the same language folder you originally used** (`en/THROUGHLINE-TEAM/` or `ko/THROUGHLINE-TEAM/`) into the project's `THROUGHLINE/`. Since these are coordination-layer files, do this directly on the shared branch (or a work branch + PR first if the shared branch is push-protected — merge before any contributor resumes claiming).

**Step 2 (Agent):**

```text
The THROUGHLINE Team kit has been updated and its kit-owned files have been replaced with the new version.
Upgrade this project's artifact structure to the new-version standard.
Do not re-run KICKOFF or ADOPT (re-initialization/re-adoption forbidden). Preserve the content of existing coordination/work artifacts.
Only role: maintainer runs this prompt.

0. Identity check: match git config user.email against team/*.md. If role is not maintainer, stop and delegate to a maintainer.
   git fetch and read the latest shared branch before comparing structure.
1. Compare the structure in the new KICKOFF.md §1 against the current THROUGHLINE/ and list missing files/folders.
2. Create missing empty structure (.gitkeep per KICKOFF §1) — e.g. workitems/archive/ if this project predates it.
3. One-time archive sweep (meaningful only if workitems/archive/ is new): for every workitems/WI-*.md at the root with
   status: done, confirm a matching history/ event exists, then move it to workitems/archive/ in this same commit
   (CONVENTIONS §9). List any done item with no matching history/ event instead of moving it — flag it for AUDIT,
   don't archive it blind.
4. Merge-update root AGENTS.md against the new KICKOFF.md §4 (team conventions) — preserve existing project-specific
   content, add only missing principle blocks (identity/shared branch/conflict detection/atomic commit/etc.). If the
   existing content is in a different language, translate-merge without mixing languages.
5. Replace root CLAUDE.md with the new KICKOFF.md template (malfunction-prevention only). Lossless gate: before removing
   a rule, confirm it exists in AGENTS.md (add it there first if not); preserve project-specific custom rules by
   translating them into the prescribed language.
6. Do not modify the content of existing artifacts (ARCHITECTURE/PLAN/workitems/features/etc.). Conform format only
   where a schema changed, preserving content (e.g. a new optional SCHEMAS.md field is not force-added to existing files).
7. Record history/YYYY/MM/HIST-<YYYYMMDD-hhmm>-kit-upgrade.md as a `chore | Framework upgrade` event — list files
   updated/created and workitems archived by the sweep.
8. Commit the whole change as coordination-layer files directly on the shared branch (or the work branch used in Step 1).
   Do not bundle code changes into this commit.
9. Report the list of files updated/created/migrated, workitems archived by the sweep, and any conflicts needing manual
   confirmation.
```

**Step 3 (verification):** run the `AUDIT.md` prompt right after the upgrade — it catches migration omissions (a stray `done`-but-unarchived workitem, a fixed INDEX file someone committed, broken links) against the new standard.

## Prompts & reference (in [`en/THROUGHLINE-TEAM/`](en/THROUGHLINE-TEAM/))

| File | Role |
|---|---|
| [README.md](en/THROUGHLINE-TEAM/README.md) | full framework overview & spec |
| [KICKOFF.md](en/THROUGHLINE-TEAM/KICKOFF.md) · [ADOPT.md](en/THROUGHLINE-TEAM/ADOPT.md) | initialize a new / existing team project |
| [DEVELOP.md](en/THROUGHLINE-TEAM/DEVELOP.md) · [INTEGRATE.md](en/THROUGHLINE-TEAM/INTEGRATE.md) | contributor / maintainer prompts |
| [AUDIT.md](en/THROUGHLINE-TEAM/AUDIT.md) | team document audit (drift + coordination integrity) |
| [CONVENTIONS.md](en/THROUGHLINE-TEAM/CONVENTIONS.md) · [SCHEMAS.md](en/THROUGHLINE-TEAM/SCHEMAS.md) | structural conventions & frontmatter schemas |
| [reference/](en/THROUGHLINE-TEAM/reference/README.md) | bundled solo-kit reference copies cited by the team prompts |

> THROUGHLINE Team keeps the Solo philosophy — markdown + git, tool independence (Claude Code · Codex · Cursor), cross-session memory, traceability, the multi-persona review harness. See the **[full guide](en/THROUGHLINE-TEAM/README.md)** for the conflict-detection model, the development flow, and the honest limitations (detection ≠ enforcement; governance ≠ tooling).
