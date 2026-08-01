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

> Paste-ready prompts for each step are in the [Prompts](#prompts-paste-ready) section below. Every prompt writes paths relative to the `THROUGHLINE/` folder copied into your project root (the three root files `README.md` · `AGENTS.md` · `CLAUDE.md` excepted).

---

## Prompts (paste-ready)

Exactly as in the solo kit ([README.md](README.md) §2 · 5 · 7 · 9.1), paste the prompts below into your Agent (Claude Code · Codex · Cursor). Each is an entry point that makes the agent read the corresponding kit file (`THROUGHLINE/KICKOFF.md`, etc.) and follow its instructions, and each has a **designated runner (maintainer / contributor)**.

This kit uses **markdown + git only** — "identity check", "conflict detection", and "reading the list" are not a separate runtime; the agent performs them directly with `git` commands and file reads. **No fixed INDEX file is ever created**: the truth of progress is the frontmatter of each item file (`workitems/WI-*.md`, etc.).

> **What is the shared branch?** The branch where coordination-layer files (`workitems/` · `conflicts/` · `team/` · `personas/`) are published the moment a workitem is claimed — your default branch, or a separate `coordination` branch if the default is push-protected ([CONVENTIONS.md §4.5](en/THROUGHLINE-TEAM/CONVENTIONS.md)). Coordination metadata has to reach this branch for other contributors to see it, so **nobody can start claiming before the initialization commit lands there**. Code never reaches this branch by direct push — only through a PR.

### A. Initialization prompt — new team project (KICKOFF · maintainer)

Write `THROUGHLINE/SOURCES/REQUIREMENTS.md` (initial requirements), register yourself as `team/<handle>.md` with `role: maintainer`, then paste the prompt below. This step does not implement anything — it builds **the coordination structure plus an initial backlog of workitems that several contributors can claim and progress without colliding**.

```text
Read THROUGHLINE/SOURCES/REQUIREMENTS.md and THROUGHLINE/KICKOFF.md, and following KICKOFF.md's instructions,
initialize this team project into a state where several contributors can concurrently claim and progress work without conflict.
Conventions in THROUGHLINE/CONVENTIONS.md and schemas in THROUGHLINE/SCHEMAS.md take precedence.

This kit uses markdown + git only (no extra runtime). Perform "identity check" and "reading the list" directly with git commands and file reads.
Generate every artifact under THROUGHLINE/, except the three root files (project README.md · AGENTS.md · CLAUDE.md).

First check these guards.
- No re-initialization: if SOURCES/REQUIREMENTS.meta.md is already applied, do not re-run KICKOFF — just report.
- This prompt is run by the maintainer (initialization = fixing the global contracts and structure).

Proceed strictly in the following order (update progress after each step — if interrupted, resume from workitems/ and the PROGRESS.md stub).

1. Register the maintainer: register whoever runs the initialization as team/<handle>.md (role: maintainer) by copying templates/team-TEMPLATE.md.
   Confirm git config user.email is among that file's emails (identity match).
2. Analyze SOURCES/REQUIREMENTS.md and create SOURCES/REQUIREMENTS.meta.md (id: REQUIREMENTS) with status under_review.
   If other materials were submitted, register them too as SRC-*.md (immutable original) + SRC-*.meta.md (triage).
3. Check whether the core requirements are sufficient to initialize; if anything is ambiguous (purpose · target users · MVP · data ·
   external integrations · authn/authz · cross-cutting baseline · QA), ask the user before proceeding (max 5 questions at once, essentials only).
   Handle [AI-delegated] items per the KICKOFF §2 rules.
4. Settle the project purpose and scope.
5. Settle the cross-cutting contracts that apply across features (data model / naming / API / authentication) and write ARCHITECTURE.md
   (maintainer single-writer domain).
6. Separate MVP from lower-priority work.
7. Decompose into features and write features/*.md (skeleton: KICKOFF §6.1). Review non-trivial features via personas/ + discussion/;
   write the feature document as the final agreed spec rather than a transcript, but leave 3–4 lines on the participating personas,
   the key contentions, and the conclusion, plus a link to the log.
8. Work breakdown: create workitems/WI-*.md with status: proposed, filling in touches (contracts/modules), feature, and source_refs for each.
   This initial backlog is the workitem list.
9. Write the QA documents (qa/), including the rule that "tests pass" counts only when they were actually executed.
10. Write the user documents (docs/).
11. Record significant design decisions as adr/ADR-<YYYYMMDD>-<slug>.md.
12. Finalize ARCHITECTURE.md.
13. Draft the project README.md (root) — no sensitive information.
14. Write AGENTS.md (root) — it MUST include the [AGENTS.md team conventions] below.
15. Write PLAN.md (a stable roadmap — Phase level only; task state lives in workitems).
16. Write a PROGRESS.md compatibility stub (the truth of progress is item-file frontmatter; do not record it directly here).
17. Record initial autonomous judgments as individual assumptions/ASM-*.md files (with a scope field — do not create a single ASSUMPTIONS.md).
18. Set SOURCES/REQUIREMENTS.meta.md to applied (the freeze point) and link the artifacts that reflect it.
    From then on REQUIREMENTS.md is immutable; further requests arrive as new SRC-* change requests.
19. Write CLAUDE.md (root) — malfunction-prevention only, plus the team entries: "global contracts are maintainer-only; progress lives in
    workitems frontmatter".
20. Put .gitkeep in the directories that start empty (conflicts/, sessions/archive/, workitems/archive/, history/, notes/, discussion/).
21. Per KICKOFF §3.1, bundle every initialization artifact (the three root files + THROUGHLINE/) into a single commit on the shared branch,
    and push if a remote exists. ★ No contributor can start claiming before this commit.
    (If the shared branch is push-protected, initialize on the designated coordination branch and record that in AGENTS.md.)

Do not create fixed INDEX files — personas/INDEX.md · features/README.md · docs/README.md · adr/INDEX.md are NOT generated
(lists are read straight from each directory's frontmatter). qa/README.md is the exception: it is a QA operating-standard document, so write it.

[AGENTS.md team conventions — must be included]
- No runtime: markdown + git only.
- Roles: maintainer (global contracts · INTEGRATE · arbitration) / contributor (claim a workitem · do the work). Check identity at session start.
- Identity: anchored to git identity — match git config user.email against the emails in team/<handle>.md. Session-Id / Co-Authored-By trailers on commits.
- Progress: workitems/WI-*.md frontmatter, not PROGRESS.md (no fixed INDEX). The session cursor is sessions/<handle>--<WI-id>.md.
- Shared branch: <the name decided at initialization — the default branch or coordination>. Coordination files (workitems/conflicts/team/personas)
  are committed and pushed directly there; code arrives only by PR. WI files are edited only on the shared branch.
- Conflicts: right after a claim and right before integrating, git fetch first, then read workitems/*.md (claimed/in_progress) on the latest
  shared branch and cross-check touches. contracts overlap = STOP; modules overlap = register conflicts/CF.
- Global contracts (ARCHITECTURE/PLAN): maintainer single-writer. Changes go via ADR + a detection notice + merge-first (serialization).
- Atomic commits: code + that workitem's work-layer files only. Exclude ARCHITECTURE/PLAN/history.
- A new event is a new file: never append to history/assumptions/conflicts — create a file.
- Integration is the maintainer's, via INTEGRATE.md. Contributors stop at the PR. No direct push to main/master.

When initialization is complete, report in the format below.
# Team project initialization result
## Registered team members / roles
## Structure created / cross-cutting contract (ARCHITECTURE) summary
## Feature spec list / initial workitem list (with touches)
## ADR / QA / docs list
## Items decided by AI delegation (review recommended)
## Next steps (first claim candidates / DEVELOP.md guidance)
```

> Initialization has many steps and can be interrupted. Progress is left in the item files after each step, so if it breaks off, just run the same prompt again to resume.

### B. Adoption prompt — a project already under development (ADOPT · maintainer)

For a project that **already has code** rather than a new one, use `ADOPT.md` instead of `KICKOFF.md`. It reverse-documents the current state **by analyzing the existing code** rather than requirements, and stands up the concurrent-team structure. The artifact structure is identical to KICKOFF, so once adoption finishes you continue straight into DEVELOP.

```text
Read THROUGHLINE/ADOPT.md and, following its instructions, adopt (apply) THROUGHLINE Team into this project that is already under development.
Conventions in THROUGHLINE/CONVENTIONS.md and schemas in THROUGHLINE/SCHEMAS.md take precedence.

Generate every artifact under THROUGHLINE/, except the three root files (project README.md · AGENTS.md · CLAUDE.md).
Do not touch same-named folders of the existing project (docs/, etc.). This prompt is run by the maintainer.

Observe the following without fail.

1. Do not modify code at this stage. This step documents the current state and stands up the team-development structure.
2. Precondition check: if THROUGHLINE/ already holds artifacts, it is already adopted → do not re-adopt, just report.
   Inventory the root README/AGENTS/CLAUDE/.gitignore; do not overwrite existing files — merge them or get confirmation.
   Register the runner as team/<handle>.md (role: maintainer) and confirm the git config user.email match.
3. Code scan: identify the stack, the build/run/test commands, the structure, entry points, dependencies, and the *names* of
   environment variables (do not collect values or secrets).
4. Trace actual behaviour: read the core paths yourself starting from the entry point. Do not infer from filenames or structure alone.
   State explicitly what you read and what you did not, and leave the unread areas as workitems/WI-*.md
   (status: proposed, title: "Unread area ...").
5. Reverse-extract the cross-cutting contracts → ARCHITECTURE.md (maintainer single-writer). For anything the code cannot settle,
   do not invent it — leave it in assumptions/ASM-*.md (active, needs verification).
6. As-built specs → features/*.md. Back every behavioural claim with the evidence location in code (file/function).
   Mark behaviour you did not read directly as "presumed (needs verification)", and flag code↔intent divergences separately.
7. Actually run the existing tests and record the baseline (pass/fail/absent) in history/YYYY/MM/HIST-*.md.
8. Decompose the remaining/unimplemented work into workitems/WI-*.md (proposed) and fill in touches (contracts/modules).
9. If SOURCES/REQUIREMENTS.md exists, treat it as future goals / unimplemented requirements, and ask when it conflicts with as-built.
   On completing adoption, register it in SOURCES/REQUIREMENTS.meta.md (id: REQUIREMENTS) and freeze it to applied.
10. Reflect the current state in PLAN.md as done/in-progress/remaining, and write a PROGRESS.md compatibility stub.
11. Write/merge AGENTS.md (team conventions — the KICKOFF §4 items) and CLAUDE.md. (No fixed INDEX files, no extra runtime.)
12. Commit the adoption artifacts (documents only — no code changes). If the maintainer can push to the shared branch, work directly there;
    otherwise work on a docs/throughline-adopt branch and merge it by PR before any contributor starts claiming.
    Put .gitkeep in directories that start empty.
13. When adoption is complete, report in the format below.
# Team adoption result
## Registered maintainer
## What was read / what was not (→ workitem)
## Reverse-extracted ARCHITECTURE summary
## As-built feature list (with code evidence)
## Code↔intent divergence list
## Test baseline (commands run / results)
## Initial workitems created (touches) / PLAN reflection
## Next steps (DEVELOP.md guidance)
```

> Adoption is multi-step too and can be interrupted. On resuming, read the frontmatter of the item files under workitems/ and history/ to pick up where it stopped.

### C. Contributor development prompt — claim → detect → implement → PR (DEVELOP · contributor)

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

### D. Resume prompt — continuing in a later session (DEVELOP · contributor)

Use this to continue the same workitem in a later session. The session cursor (`sessions/<handle>--<WI-id>.md`) and its "Next first command" is the reference point.

```text
Read AGENTS.md and THROUGHLINE/DEVELOP.md, and continue developing the workitem I already had in progress.

1. Confirm identity with git config user.email, then git fetch.
2. Read the "Next first command" in sessions/<handle>--<WI-id>.md to find where I left off.
3. Re-read the touches of workitems/*.md (claimed/in_progress) on the latest shared branch and re-detect conflicts that
   appeared while I was away (contracts overlap = STOP; modules overlap = check/register conflicts/CF).
4. Re-align with the cross-cutting contracts in ARCHITECTURE.md / PLAN.md, and do not redo work that is already finished.
5. Continue implementing from DEVELOP.md §4 on the feat/<WI-id> branch (actually run the tests, atomic commit, update the session cursor).
6. When the work reaches a stopping point, report in the DEVELOP.md §8 format and update sessions/<handle>--<WI-id>.md.
```

### E. Integration prompt — merging review-complete work (INTEGRATE · maintainer)

Use this after contributors have opened PRs, when the maintainer merges the feature branches into the shared branch. Only `role: maintainer` runs it.

```text
Read AGENTS.md and THROUGHLINE/INTEGRATE.md, and following the INTEGRATE.md procedure, integrate the review-complete workitems.
Conventions in THROUGHLINE/CONVENTIONS.md take precedence. Only role: maintainer runs this prompt.

Proceed strictly in the following order.

0. Identity check: match git config user.email against team/*.md. If the role is not maintainer, stop and delegate to a maintainer.
   git fetch, then collect the workitems/*.md with status: review on the latest shared branch, along with their PRs/branches.
1. Collect the integration set: check each workitem's touches (contracts/modules) and depends_on.
2. Re-detect conflicts (mandatory before merging): exhaustively cross-check the touches of the candidates against every other
   in-flight (claimed/in_progress) workitem.
   - contracts overlap = STOP: do not merge them together; handle via the serialization in step 3.
   - modules overlap = WARN: check whether conflicts/CF-*.md records a resolution; if not, register one and agree the order with the owners.
   - Identity verification: confirm each candidate feature branch's commit author email matches the registered email of WI.owner
     (a mismatch = the claimer ≠ the worker → report it).
3. Serialize global contracts: handle workitems that carry touches.contracts first.
   Confirm the relevant ADR is Accepted → merge the contract-changing workitem first → the maintainer updates ARCHITECTURE.md
   (and PLAN.md if needed) → notify the owners of the remaining workitems touching the same contract to rebase onto the new
   contract (no merging before they rebase).
4. Merge: merge the PRs in serialization order (contract changes → dependents → independents). Resolve git conflicts the usual way.
   After merging, set each WI status to done and, in the same commit, move the file into workitems/archive/ and commit on the shared
   branch (the sanctioned exception to WI single-writer — CONVENTIONS §9).
5. Record history: for every merged workitem create a new file history/YYYY/MM/HIST-<YYYYMMDD-hhmm>-<slug>.md
   (completed workitem, commit, test results, source, QA, impact scope, follow-ups). Only INTEGRATE writes history.
6. Update SOURCES status: for sources fully reflected by the merge, set SRC-*.meta.md status to applied and link the resulting artifacts
   (applied only when every item is reflected; partial reflection stays under_review).
7. Full regression & PROGRESS: actually run the full regression suite and record the results in history.
   Spot-check that the ARCHITECTURE contracts still hold in the recent code (if they don't, open conflicts/ or a follow-up workitem).
   Keep the PROGRESS.md stub pointing at the item files (the truth of progress is workitems frontmatter).

When done, report in the format below.
# Integration result (INTEGRATE)
## Workitems merged (order and rationale)
## Global contract changes (ARCHITECTURE/ADR)
## Re-detection results (STOP/WARN and how resolved)
## Identity verification (owner ↔ commit author mismatches)
## History events recorded
## SOURCES status changes (marked applied)
## Full regression results (commands run / pass·fail)
## Remaining review/blocked workitems
```

### F. Document-audit prompt — drift + coordination integrity (AUDIT · maintainer)

Run this periodically: right after a Phase completes, before a release, when resuming after a long gap, once roughly 10 sessions have accumulated since the last audit, or while several contributors are active concurrently.

```text
Read THROUGHLINE/AUDIT.md and, following its instructions, audit the team documents and code for drift and the coordination
structure for integrity.
Conventions in THROUGHLINE/CONVENTIONS.md take precedence. INTEGRATE handles merge-time consistency; AUDIT recovers gradual drift.

Observe the following without fail.

1. Do not modify feature code. This is an inspection-and-record step.
2. Fix mechanical inconsistencies (broken links, obviously wrong status values) immediately and include them in the audit commit.
   There is no index-regeneration step because there are no fixed INDEX files.
3. Do not fix semantic drift — record it only (code↔spec goes through the DEVELOP authority diagnosis; touches overlaps go to conflicts/).
4. Confirm the absence of fixed INDEXes: if someone created and committed a fixed index file such as INDEX.md, report it as a deletion candidate.
5. Workitem hygiene: items left claimed/in_progress for a long time (e.g. 14+ days); whether each owner is an active handle registered in team/;
   items marked done with no history/ event (including archive/); items marked done but not moved into workitems/archive/;
   items with broken feature/source_refs links; orphaned workitems.
6. Undetected touches overlap (the core check): git fetch, then pairwise cross-check the touches of every in-flight (claimed/in_progress)
   workitem on the latest shared branch.
   - a contracts-overlapping pair with no conflicts/CF and no serialization → report immediately (the maintainer must serialize).
   - a modules-overlapping pair with no conflicts/CF registered → queue CF registration as a follow-up.
7. Identity/authority integrity: are all recent commit author emails registered in team/; does WI.owner match the feature branch's commit
   author; did a contributor edit ARCHITECTURE.md/PLAN.md directly (single-writer violation, per git history); does every global contract
   change have an ADR.
8. conflicts/sessions/SOURCES: CFs left open for a long time; sessions still active though done (→ archive/ candidates);
   SRC-*.meta left not_applied/under_review (user intent not reflected); originals modified after applied (immutability violation).
9. Register follow-ups in workitems/ (proposed) or PLAN, and record the whole audit as an audit event in history/YYYY/MM/HIST-*.md.

When done, report in the format below.
# Team document audit result
## Audit scope / sampling basis
## Immediate fixes (mechanical)
## Undetected touches overlap (contracts STOP / modules WARN)
## Workitem hygiene (stale / unregistered owner / orphaned / broken links)
## Identity & authority integrity (unregistered author / owner≠author / single-writer violations)
## conflicts · sessions · SOURCES status
## General drift (plan↔actual / assumption lifetime / spec↔code sample)
## Items needing user confirmation
## Follow-up work (reflected in workitems/PLAN)
```

### G. Kit-upgrade prompt — applying a new version (maintainer)

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

When done, report in the format below.
# Kit upgrade result
## Files updated / created
## Workitem archive sweep result (number moved / exceptions not moved)
## AGENTS.md merge content / whether CLAUDE.md was replaced
## Newly created structure
## History event recorded
## Conflicts needing manual confirmation
```

**Step 3 (verification):** run the **F. Document-audit prompt (AUDIT)** right after the upgrade — it catches migration omissions (a stray `done`-but-unarchived workitem, a fixed INDEX file someone committed, broken links) against the new standard.

### Criteria for choosing a prompt

| Situation | Prompt to use | Runner |
|---|---|---|
| Starting a brand-new team project | A. Initialization (KICKOFF) | maintainer |
| Applying it to a project already under development | B. Adoption (ADOPT) | maintainer |
| Claiming a workitem and starting development | C. Contributor development (DEVELOP) | contributor |
| Continuing a workitem already in progress | D. Resume | contributor |
| Merging review-complete workitems | E. Integration (INTEGRATE) | maintainer |
| Phase completion / before a release / drift suspected | F. Document audit (AUDIT) | maintainer |
| Upgrading the kit to a new version (already-initialized project) | G. Kit upgrade | maintainer |

> The authoritative sources for the rule details (file grades · identity · conflicts · shared branch · commits) and the frontmatter formats are [CONVENTIONS.md](en/THROUGHLINE-TEAM/CONVENTIONS.md) and [SCHEMAS.md](en/THROUGHLINE-TEAM/SCHEMAS.md) respectively.

---

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
