# DEVELOP.md — Contributor development prompt

The procedure for **a single contributor (human/AI agent) performing one workitem** in THROUGHLINE Team team development.
[CONVENTIONS.md](CONVENTIONS.md) takes precedence on conventions. Global-contract changes and integration are handled by the maintainer's [INTEGRATE.md](INTEGRATE.md).

> This kit uses markdown + git only. The "identity check"·"detection"·"reading the listing" below are all **performed directly by the agent using file reads and `git` commands** (no separate tool or command to enter).
> Path basis: all artifacts live under `THROUGHLINE/` (root 3-file exception).

---

## 0. Session start (performed automatically by the agent)

1. **Identity check** — read `git config user.email` and match it against the `emails` in `team/*.md` to confirm my `handle`·`role`. On a match failure (unregistered), register `team/<handle>.md` first (`templates/team-TEMPLATE.md`), then proceed.
2. **Survey the state** — `git fetch` first, then read the frontmatter of the **latest** shared branch's `workitems/*.md` (`origin/<shared branch>` — CONVENTIONS §4.5) to see in-flight work (especially `claimed`/`in_progress`) and its `touches` (no fixed INDEX file — the item file is the SoT).

---

## 1. Always-loaded documents

1. `AGENTS.md` (project root)
2. `THROUGHLINE/ARCHITECTURE.md` (cross-cutting contracts — always loaded)
3. `THROUGHLINE/PLAN.md` (roadmap)
4. The **frontmatter of in-flight items** among `THROUGHLINE/workitems/*.md` (the current state + others' `touches`)

Read the `features/*.md`·ADR·qa·notes needed for my work optionally. For common rules (data model/naming/API/auth) always follow `ARCHITECTURE.md` as the baseline.

---

## 2. Select or create a workitem (claim)

### 2.1 Claim an existing workitem
Pick an item with `status: proposed|ready` from `workitems/*.md`.

1. Change that `WI-*.md`'s `owner` to my handle and `status` to `claimed`.
2. Record `branch` as `feat/<WI-id>`.
3. **Commit only this change on the shared branch and push immediately** (before code work — publishing, CONVENTIONS §4.5).

### 2.2 Create a new workitem
Copy `templates/WI-TEMPLATE.md` to `workitems/WI-<YYYYMMDD>-<slug>.md`.

* **You must fill in `touches`** — the cross-cutting contracts (`contracts`) and modules (`modules`) this work will touch. This is the core of conflict detection, so declare it accurately.
* Link the corresponding spec file in `feature`, and link the supporting SRC in `source_refs`.
* Commit on the shared branch and push immediately (publishing — CONVENTIONS §4.5).

---

## 3. Conflict detection (right after claim — mandatory, performed by the agent)

`git fetch` first, then read the latest shared branch's `workitems/*.md` with `status ∈ {claimed, in_progress}` (CONVENTIONS §4.5) and cross-check against my `touches`.

| Result | Meaning | What to do |
|---|---|---|
| **STOP** | `contracts` overlap with another in-flight workitem | Do not proceed. Ask the maintainer to serialize (§7). If it's a contract change, go via ADR |
| **WARN** | `modules` overlap (potential semantic conflict) | Register `conflicts/CF-*.md` (`templates/CF-TEMPLATE.md`), agree on order with the other owner |
| **OK** | independent | Create the `feat/<WI-id>` branch and start development |

---

## 4. Development (work layer — feature branch)

Create the branch: `git checkout -b feat/<WI-id>`. Create the session file: `sessions/<handle>--<WI-id>.md` (`templates/session-TEMPLATE.md`). Update "Next first command" as you progress.

Work order:

1. Set `WI-*.md` status to `in_progress` — **commit·push on the shared branch** (WI files are edited only on the shared branch; CONVENTIONS §4.5).
2. Check the spec in `features/*.md` and the contracts in `ARCHITECTURE.md` (if absent, start from the spec; review non-trivial features via `personas/`+`discussion/` — the the Solo edition DEVELOPINIT §6 way, [reference/SOLO-DEVELOPINIT.md](reference/SOLO-DEVELOPINIT.md)).
3. Implement + write automated tests → **actually run them** (capture commands·results). Don't claim passing without running.
4. On code ↔ spec mismatch, do an **authority diagnosis** before handling: ① diagnose which side is authoritative → ② if the spec captures the intent and the code is wrong, fix the code → ③ if the spec is confirmed stale, update the spec first and then conform the code → ④ if you cannot judge, ask (maintainer/user) — and record the basis in `assumptions/`·`notes/`. Don't arbitrarily edit the spec to erase the mismatch (details: solo DEVELOPINIT §3.4, [reference/SOLO-DEVELOPINIT.md](reference/SOLO-DEVELOPINIT.md)).
5. Record autonomous judgments as a **new file** `assumptions/ASM-*.md` (don't append to a shared single file). If it conflicts with an existing assumption, record it in `conflicts/`.
6. Record non-trivial facts you learned in `notes/<topic>.md` (guesses go to assumptions).

**If you decide a global contract needs to change, do not edit `ARCHITECTURE.md` directly.** Treat it as a STOP cause and follow the §7 procedure.

---

## 5. Atomic commit (workitem scope)

For each meaningful unit, bundle **code + that workitem's work-layer files** into one commit.

* Include: code, `features/*.md`, `qa/*.md`, `assumptions/ASM-*.md`, `notes/*`, `sessions/<handle>--<WI-id>.md`.
* **Exclude**: `ARCHITECTURE.md`/`PLAN.md` (maintainer), `history/**` (INTEGRATE), `workitems/WI-*.md` (coordination — status updates go on the shared branch, CONVENTIONS §4.5).
* commit message: Conventional Commits + trailers
  ```text
  feat: <summary>

  Session-Id: <YYYY-MM-DDThhmm>-<handle>-<WI-id>
  Co-Authored-By: <agent runtime>
  ```
* Code/work-layer changes are never pushed directly to `main`/`master`/the shared branch — they arrive there only via PR (INTEGRATE). **Exception:** coordination-layer files (`workitems/`·`conflicts/`·`team/`·`personas/`) are committed·pushed directly on the shared branch — that *is* the publishing mechanism (CONVENTIONS §4.5). No committing `.env`·secrets·key files.

---

## 6. Submit for review

1. Set `WI-*.md` status to `review` (commit·push on the shared branch — CONVENTIONS §4.5).
2. Push `feat/<WI-id>` and create a PR (merge is done by the maintainer in INTEGRATE).
3. In the PR body, state the WI-id, change summary, test results, `touches`, and unresolved `conflicts/`.

---

## 7. When STOP/serialization is needed (global-contract impact)

If detection returns STOP or a global contract change is needed:

1. Write a **dedicated workitem** declaring the contract-change intent via `touches.contracts` + an `adr/ADR-*.md` (Proposed).
2. Ask the maintainer to serialize (INTEGRATE §3).
3. After the maintainer merges the contract change first and updates `ARCHITECTURE.md`/the ADR, **rebase** my workitem onto the new contract and resume §4.

---

## 8. Completion report format

```md
# Development result (WI-<id>)
## Work done / changed files
## Test results (commands run / pass·fail)
## touches (contracts / modules) and detection result
## Registered conflicts / assumptions / notes
## Git (branch / commit / PR)
## Next first command (= the update to sessions/<handle>--<WI-id>.md)
```
