# ASK-Team — Agent-Spec-Kit for team development

> A framework that uses markdown + git alone to reduce the Git conflicts, semantic conflicts,
> and intent conflicts that arise when multiple developers and multiple AI agents develop **concurrently**.
> It is the **sister framework** of the existing [Agent-Spec-Kit](../AGENTSPECKIT/) (solo/sequential).

> **This kit is built entirely from markdown prompts.** It requires no separate runtime (Python, etc.) or executable binary,
> and operates solely with the abilities an agent already has (reading/writing files + `git` commands) — identical on Claude Code · Codex · Cursor.

---

## 0. Positioning — the sister of solo ASK

The existing ASK (`AGENTSPECKIT/`) operates around **global single files** like `PLAN.md`·`PROGRESS.md`·`HISTORY.md`·`ASSUMPTIONS.md`·`NOTES.md`·`SOURCES/INDEX.md` for **solo/sequential·autonomous development**. It's simple, but when N people work concurrently these files become conflict hotspots.

ASK-Team is a separate framework that, **rather than introducing tiers gradually**, fixes every mechanism team-first from the start. For solo development, the existing ASK is lighter. ASK-Team is for **teams where N people actually develop concurrently**.

**Philosophy it keeps:** markdown + git, tool independence (Claude Code · Codex · Cursor), cross-session memory, requirements traceability, multi-persona review harness.

---

## 1. Core insight — git branch isolation

Every design decision in ASK-Team flows from one fact.

> **N contributors cannot see each other's *uncommitted* files.** Feature branches isolate the working tree.

So for `touches`-based conflict detection to work, **coordination metadata must be published to a shared branch at claim time**. That's why every artifact is split into two layers.

| Layer | Content | Where it lives |
|---|---|---|
| **Coordination** | workitem declarations (`touches`), conflicts, global contracts (ARCHITECTURE/PLAN) | **shared branch — published immediately at claim** |
| **Work** | code, feature specs, qa, notes, assumptions | **feature branch (isolated)** |

If coordination metadata isn't shared ahead of time, you discover semantic conflicts **only at merge time**. Claim-time publishing enables **early detection**.

---

## 2. Role model (essential for teams)

| Role | Responsibility | single-writer target |
|---|---|---|
| **Maintainer (1+)** | owns global contracts·roadmap, runs `INTEGRATE`, arbitrates semantic/intent conflicts, approves contract-change ADRs | `ARCHITECTURE.md`, `PLAN.md`, `AGENTS.md`, `history/` |
| **Contributor (N, human/agent)** | claims workitems, branch work, writes scoped files, PR | own `WI-*.md`, own work-layer files |

Multi-human **intent conflicts** (different people submit contradicting requirements) are solved not by file structure but by **governance** — the maintainer arbitrates and records it as an ADR. The framework only *surfaces* conflicts; it doesn't create consensus.

---

## 3. Directory structure

When applied to a project, every artifact is created under `AGENTSPECKIT/` (root 3-file exception: project `README.md`·`AGENTS.md`·`CLAUDE.md`). Same root convention as the existing ASK.

```text
AGENTSPECKIT/
  # prompts (markdown only)
  KICKOFF.md  ADOPT.md  DEVELOP.md  INTEGRATE.md  AUDIT.md

  # coordination layer (shared branch, includes maintainer single-writer domains)
  ARCHITECTURE.md                # single·always-loaded — maintainer-only edits
  PLAN.md                        # stable roadmap — maintainer-only edits
  PROGRESS.md                    # compatibility entry point (static stub — points to item files)
  workitems/  WI-*.md            # units of work (frontmatter = SoT for status)
  conflicts/  CF-*.md            # semantic-conflict records

  # identification
  team/       <handle>.md        # participant registry

  # work layer (feature branch, per-item single-writer)
  sessions/   <handle>--<WI-id>.md   archive/
  history/    YYYY/MM/HIST-*.md       # recorded by INTEGRATE
  assumptions/ ASM-*.md
  notes/      <topic>.md  <topic>/*.md

  # inputs
  SOURCES/
    REQUIREMENTS.md              # initial requirements (kept frozen)
    SRC-*.md                     # immutable original content
    SRC-*.meta.md                # mutable triage (per-source single-writer)

  # spec·review harness (kept — the paper's core contribution)
  features/*.md   personas/*.md   discussion/review-*.md   adr/ADR-*.md   docs/  qa/

  templates/                     # schema examples for copying
```

> **We don't keep fixed INDEX files.** The listing·status of each directory has the item file's frontmatter as its source of truth, and the agent reads it directly when needed (§5). If you want a human-readable table, ask the agent for one at that point.
> We don't keep `locks/` either — global-contract protection is replaced by **maintainer single-writer + ADR gate + merge order** (§6, CONVENTIONS §6).

---

## 4. Identity — anchored to git identity

We don't reinvent developer identity. We use the **git identity already on every commit** (email) as the basis, validated by the `team/` registry. It uses **`git` commands only**, with no additional runtime.

- **Anchor key:** `git config user.email` (unique). `user.name` is for display.
- **Two axes:** responsible party (human = commit author) / executor (agent = `Co-Authored-By` trailer).
- **Registry:** `team/<handle>.md` (per-person, single-writer).
- **Identity check at session start:** the agent runs `git config user.email` and matches it against the `emails` in `team/*.md` to confirm `handle`·`role`. On a match failure (unregistered), it registers `team/<handle>.md` first, then proceeds.
- **Trust model:** soft identity (attribution·conflict avoidance·validation) is provided by markdown; hard identity (blocking impersonation) is delegated to the git platform (protected branch · signed commit · CODEOWNERS).

For detailed conventions see [CONVENTIONS.md §2](CONVENTIONS.md).

---

## 5. Status — the item file is the source of truth (no fixed INDEX)

- **SoT = the frontmatter in each item file.** A single writer writes only their own file (`WI-*.md`, `ASM-*.md`, `SRC-*.meta.md`, `HIST-*.md`, `team/*.md`, `CF-*.md`).
- **We don't create fixed INDEX files.** When the agent needs to understand progress·the work list, it **reads the `*.md` frontmatter directly** from the relevant directory (selective loading — only what's needed).
- If you need a **human-readable aggregate view**, ask the agent at that point — e.g. "summarize the workitems as a table" — and receive it as markdown. **We don't force-generate·commit it as a file.**

Effects:
- With no shared INDEX file, **concurrent-INDEX-edit conflicts simply don't exist.**
- No separate runtime·build step — pure prompt-only.
- Trade-off: there's no fixed dashboard for seeing progress at a glance. Instead, you check ad hoc via `git`/`grep`/`gh` or by asking the agent.

---

## 6. Semantic-conflict detection & global-contract serialization

**Detection (right after claim · right before integrate — performed by the agent):**

```text
read the shared branch's workitems/*.md with status ∈ {claimed, in_progress}
and cross-check against my touches.
  · contracts overlap → STOP. maintainer serializes (below)
  · modules overlap   → register conflicts/CF-*.md + agree on order
  · none              → proceed
```

**Global-contract serialization (instead of locks):**

```text
ARCHITECTURE / global-contract change =
  ① a dedicated workitem declaring touches.contracts + an ADR(Proposed)
  ② detect in-flight workitems touching the same contract → STOP notice
  ③ maintainer merges the contract-change workitem first, ADR→Accepted, updates ARCHITECTURE
     (maintainer is ARCHITECTURE single-writer → concurrent editing blocked at the source)
  ④ dependent workitems rebase onto the new contract
```

---

## 7. Development flow

```text
1. Gather requirements   SOURCES/SRC-*.md (immutable original) + SRC-*.meta.md (triage)
2. Decompose / claim     write workitems/WI-*.md (touches) → commit to shared branch → detect (§6)
3. Develop               feat/WI-* branch: code + feature/qa/notes/assumptions (work layer)
                         review non-trivial features via personas/discussion
4. review                WI status=review, PR
5. INTEGRATE             maintainer: re-cross touches → merge → record history
                         → SRC-*.meta status=applied → update PLAN → full regression
6. audit                 periodic: orphan WIs / undetected touches / neglected SRC / link integrity
```

**Atomic commit (redefined):** a feature-branch atomic commit = **code + that workitem's work-layer files**. It does **not** include ARCHITECTURE/PLAN (maintainer) or history (INTEGRATE). The "code and corresponding docs in one commit" principle is kept *within the workitem scope*.

---

## 8. Quick start

1. Clone this repository and copy the contents of `en/ASK-TEAM/` into the project root's `AGENTSPECKIT/`.
2. **The maintainer** registers their own `team/<handle>.md` first with `role: maintainer` (copy `templates/team-TEMPLATE.md`). Each contributor also registers their own `team/<handle>.md`.
3. Contributors work with the `DEVELOP.md` prompt, the maintainer with `INTEGRATE.md`. At session start the agent confirms identity (§4) and reads the item files it needs directly — there is no separate command to enter.

> Use `KICKOFF.md` (new) / `ADOPT.md` (existing code) for initialization, and `AUDIT.md` for periodic checks.

---

## 9. Differences from solo ASK

| Item | solo ASK | ASK-Team |
|---|---|---|
| progress state | `PROGRESS.md` single cursor | `workitems/` + `sessions/<handle>--<WI>` |
| history | `HISTORY.md` append | `history/YYYY/MM/HIST-*.md` (recorded by INTEGRATE) |
| assumptions | `ASSUMPTIONS.md` single | `assumptions/ASM-*.md` |
| notes | `NOTES.md` single | `notes/<topic>.md` |
| requirement state | `SOURCES/INDEX.md` rows (mutable) | `SRC-*.meta.md` (per-source) |
| listing/index | a single file updated by hand | **no fixed INDEX — read frontmatter directly** |
| identity | not needed | `team/` + git identity (`git config`) |
| semantic conflict | n/a | `touches` + detection (§6) + `conflicts/` |
| global contract | ADR | ADR + **maintainer single-writer + merge order** |
| runtime | none | none (markdown + git only) |

---

## 10. Honest limitations (no unfounded positivity)

1. **Governance ≠ tooling.** Multi-human intent conflicts are solved only by maintainer arbitration. The framework only surfaces conflicts; it can't create consensus.
2. **Detection ≠ enforcement.** If `touches` is undeclared/misdeclared, detection fails. It relies on the agent following the convention (a prompt is not enforcement — see the residual limitations in [README.md](../../README.md)), and INTEGRATE's re-detection is the last net but it's after the fact. If you need real *enforcement*, layer on the git platform tier (protected branch / CI) as an option.
3. **The cost is an intended trade-off.** It accepts per-session overhead (reading in-flight workitem frontmatter at detection time) and the maintainer's INTEGRATE burden. For solo, solo ASK is cheaper.
4. **Single point of failure.** The maintainer can become a bottleneck → multiple maintainers are possible, but the ARCHITECTURE single-writer discipline is kept by domain partitioning.
5. **No at-a-glance dashboard.** Since there is no fixed INDEX, you check progress ad hoc via `git`/`grep`/`gh` or by asking the agent.

---

## 11. Files that make up this kit

| File | Role |
|---|---|
| `README.md` | this document — framework overview·spec |
| `CONVENTIONS.md` | structural conventions (file grades·identity·status·conflicts·contracts·atomic commits·SOURCES) |
| `SCHEMAS.md` | frontmatter schemas (workitem·source·assumption·session·team·conflict) |
| `KICKOFF.md` | initialize a new team project |
| `ADOPT.md` | adopt an existing codebase (as-built reverse-documentation) |
| `DEVELOP.md` | contributor development prompt (claim → detect → work) |
| `INTEGRATE.md` | maintainer integration prompt (re-detect → merge → history) |
| `AUDIT.md` | team document audit (drift + coordination integrity) |
| `templates/` | example files for copying schemas |
