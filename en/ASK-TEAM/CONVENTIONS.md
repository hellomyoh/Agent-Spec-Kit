# CONVENTIONS.md — ASK-Team structural conventions (normative)

This document is the **enforced convention** for ASK-Team. The prompts (`KICKOFF`·`ADOPT`·`DEVELOP`·`INTEGRATE`·`AUDIT`) all implement these conventions. Where a convention and a prompt disagree, this document wins.

> **This kit uses markdown + git only.** It requires no additional runtime (Python, etc.) or executable binary.
> The "detection"·"identity check"·"reading the listing" below are all **performed directly by the agent using file reads/writes and `git` commands.**

> Path basis: every artifact lives under `AGENTSPECKIT/` at the project root (root 3-file exception: project `README.md`·`AGENTS.md`·`CLAUDE.md`). All paths in this document are relative to `AGENTSPECKIT/`.

---

## 1. File grades (who writes what)

Every file is one of four grades. The grade determines **who is the single-writer**.

| Grade | Files | Write permission | Concurrency rule |
|---|---|---|---|
| **Stable contract** | `ARCHITECTURE.md`, `PLAN.md`, `AGENTS.md`, prompts | **maintainer only** | No concurrent editing. Changes go through §6 serialization |
| **Coordination** | `workitems/WI-*.md`, `conflicts/CF-*.md`, `team/<handle>.md` | the owning owner | published to the shared branch at claim time (§4) |
| **Work-scoped** | `features/*.md`, `qa/*.md`, `sessions/*.md`, `notes/*` | the related workitem owner | don't touch unrelated workitems |
| **Event (append)** | `history/**`, `assumptions/ASM-*.md`, `adr/ADR-*.md`, `SOURCES/SRC-*.md`, `discussion/*.md` | the creator | new event = new file. Supersede existing records instead of deleting |

Core principle: **two streams never write the same file region at the same time.** Don't append to a shared file; create a new file. **We don't keep fixed INDEX files** (§3).

---

## 2. Identity conventions

### 2.1 Anchor point
- The primary key for identity is `git config user.email` (unique). We don't invent a new auth scheme.
- Responsible party (human) = commit **author**. Executor (agent) = `Co-Authored-By` trailer.

### 2.2 Registry — `team/<handle>.md`
Participants register with a per-person file (schema in `SCHEMAS.md` §team). `handle` is a stable short identifier, and `owner`/session filenames reference this value.

- Don't delete departed members; set `active: false` (history references them).
- Distinguish people with the same name by the unique email key; `handle` is an alias.

### 2.3 Identity check at session start (performed by the agent)
At session start the agent confirms identity **on its own** (the user enters no command).

```text
1. run `git config user.email`
2. match against the emails in team/*.md → confirm my handle, role
3. on match failure (unregistered) → register team/<handle>.md first (templates/team-TEMPLATE.md). No work entry before registration.
```

### 2.4 Where identity gets stamped
- workitem `owner:` = a registered handle.
- session file = `sessions/<handle>--<WI-id>.md` (one person may run several workitems concurrently, so `(handle, workitem)` is the unique key).
- commit trailers:
  ```text
  Session-Id: <YYYY-MM-DDThhmm>-<handle>-<WI-id>
  Co-Authored-By: Claude Code <runtime@ask-team>
  ```

### 2.5 Validation points
- **claim:** is `owner` a registered handle with `active: true`.
- **integrate:** feature-branch commit author email ∈ `owner.emails` (or owner is in `Co-Authored-By`). Mismatch → flag "claimer ≠ worker".
- **audit:** commits by unregistered authors / WIs whose owner is missing or inactive / permission violations (a contributor edits a stable contract).

### 2.6 Trust model
Identity validation **catches mistakes and drift, not malicious impersonation** (markdown has no enforcement). If you need to block impersonation, layer on the git platform tier: protected branch, required PR review, signed commits, CODEOWNERS (forcing maintainer approval on `ARCHITECTURE.md`/`PLAN.md`).

---

## 3. Listing·status conventions (no fixed INDEX)

- **The source of truth (SoT) is the frontmatter in each item file.** We don't create a separate INDEX file.
- When the agent needs to understand progress·the work list·history, it **reads the `*.md` frontmatter directly** from the relevant directory (selective loading — only what the current task needs; at detection time, only in-flight workitems).
- If you need a human-readable aggregate table, ask the agent at that point and receive it as markdown. **Don't force-generate·commit the table as a file** (eliminates staleness·concurrent-edit conflicts at the source).
- Thanks to this convention, with no shared INDEX file **concurrent-INDEX-edit conflicts don't exist**, and no additional runtime·build step is needed either.

---

## 4. workitem conventions

### 4.1 State machine
```text
proposed → ready → claimed → in_progress → review → done
                          ↘ blocked ↗
```
- `proposed`/`ready` serve as the backlog (absorbing solo ASK's `TODO.md`).
- `done` is granted only when merge and history recording have completed in INTEGRATE.

### 4.2 claim = coordination-layer published (core)
When you claim a workitem, you **commit `WI-*.md` (including `touches`) to the shared branch first** (add-only → low conflict). This lets every contributor see in-flight work and its `touches`. Code work then begins on the `feat/WI-*` branch afterward.

### 4.3 Required fields
`id`·`title`·`owner`·`status`·`branch`·`feature`·`touches` (`contracts`·`modules`). Schema in `SCHEMAS.md` §workitem.

### 4.4 ID convention
`WI-<YYYYMMDD>-<slug>` (e.g. `WI-20260620-admin-role`). No sequential numbers, to avoid concurrent-allocation collisions. `ADR-*` is the same: `ADR-<YYYYMMDD>-<slug>`.

---

## 5. Conflict conventions

### 5.1 Detection (performed by the agent)
**Right after claim** and **right before integrate**, read the shared branch's `workitems/*.md` with `status ∈ {claimed, in_progress}` and exhaustively cross-check against my `touches`.

| Overlap | Meaning | Handling |
|---|---|---|
| `contracts` | global contract edited concurrently — highest risk | **STOP.** maintainer serializes per §6 |
| `modules` | same module changed concurrently — potential conflict | register `conflicts/CF-*.md` + agree on order |
| none | independent | proceed |

### 5.2 conflicts/CF-*.md
Records one semantic conflict (no git conflict but a contradiction) and its resolution decision (immutable, append-only). It records which workitem rebases/yields and the rationale for the agreement. Schema in `SCHEMAS.md` §conflict.

Example targets: two workitems assume the same API contract differently / change the same data model in different directions / source requirements conflict / an unagreed architecture change.

---

## 6. Global-contract serialization conventions

`ARCHITECTURE.md`·`PLAN.md` are **maintainer single-writer**. Contributors don't edit them directly.

```text
Contract-change procedure:
  ① a dedicated workitem declaring touches.contracts + an ADR(Proposed)
  ② detect in-flight workitems touching the same contract (§5) → STOP notice
  ③ maintainer: merge the contract-change workitem first → ADR Accepted → update ARCHITECTURE
  ④ dependent workitems rebase onto the new contract, then proceed
```

ADR triggers (architecture, auth, DB structure, external API, deployment, test strategy, etc.) follow solo ASK [KICKOFF §16](../AGENTSPECKIT/KICKOFF.md). No lock files (maintainer + merge order is the serialization device).

---

## 7. Atomic-commit conventions

One feature-branch commit = **code + that workitem's work-scoped files** (feature spec, qa, notes, assumptions, own `WI-*.md` status).

What it does not include:
- `ARCHITECTURE.md`/`PLAN.md` (maintainer domain)
- `history/**` (recorded by INTEGRATE)

This keeps the "code and its corresponding docs in one commit" principle within the workitem scope, while preventing stable files from conflicting across cross-branch merges. (Since there is no fixed INDEX, INDEX is never a commit target in the first place.)

---

## 8. SOURCES conventions

- `SOURCES/REQUIREMENTS.md` — initial requirements. **Frozen** (immutable) once fully applied. Keeps the KICKOFF freeze contract as-is.
- `SOURCES/SRC-<YYYYMMDD-hhmm>-<slug>.md` — submitted original. **Immutable content.**
- `SOURCES/SRC-*.meta.md` — the **mutable triage** of that original (status·owner·linked workitems). Per-source single-writer, so triaging different sources concurrently does not conflict. **Only one person triages a given source.**
- Read the source listing·status directly from `SRC-*.meta.md` frontmatter (no fixed INDEX).
- Authority rule: a change request has no authority until `applied`. Read current intent from the artifacts (ARCHITECTURE/features/PLAN). (Inherits solo ASK [KICKOFF §15.2](../AGENTSPECKIT/KICKOFF.md) authority·immutability·supersede-chain rules.)

---

## 9. Lifecycle / rotation

- `sessions/`: move completed sessions to `sessions/archive/`. Keep only active sessions at the root.
- `history/`: naturally partitioned by `YYYY/MM`, so no separate rotation is needed. Compress-archive old years if needed.
- `notes/`: when a topic grows, split `notes/<topic>.md` → `notes/<topic>/*.md`.

---

## 10. Schemas

All frontmatter schemas and examples are in [SCHEMAS.md](SCHEMAS.md). Start by copying the example files in `templates/`.
