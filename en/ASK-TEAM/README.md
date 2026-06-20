# ASK-Team — Agent-Spec-Kit for team development

> A framework that uses markdown + git alone to reduce the Git conflicts, semantic conflicts,
> and intent conflicts that arise when multiple developers and multiple AI agents develop **concurrently**.
> It is the **sister framework** of the existing [Agent-Spec-Kit](../AGENTSPECKIT/) (solo/sequential).

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
| **Maintainer (1+)** | owns global contracts·roadmap, runs `INTEGRATE`, arbitrates semantic/intent conflicts, approves contract-change ADRs | `ARCHITECTURE.md`, `PLAN.md`, `AGENTS.md`, `history/`, generated INDEX |
| **Contributor (N, human/agent)** | claims workitems, branch work, writes scoped files, PR | own `WI-*.md`, own work-layer files |

Multi-human **intent conflicts** (different people submit contradicting requirements) are solved not by file structure but by **governance** — the maintainer arbitrates and records it as an ADR. The tool only *surfaces* conflicts; it doesn't create consensus.

---

## 3. Directory structure

When applied to a project, every artifact is created under `AGENTSPECKIT/` (root 3-file exception: project `README.md`·`AGENTS.md`·`CLAUDE.md`). Same root convention as the existing ASK.

```text
AGENTSPECKIT/
  # prompts
  KICKOFF.md  ADOPT.md  DEVELOP.md  INTEGRATE.md  AUDIT.md
  askctl.py                      # coordination tool (index generation · detect · whoami)
  .gitignore                     # excludes generated INDEX.md

  # coordination layer (shared branch, includes maintainer single-writer domains)
  ARCHITECTURE.md                # single·always-loaded — maintainer-only edits
  PLAN.md                        # stable roadmap — maintainer-only edits
  PROGRESS.md                    # compatibility entry point (static stub — points to the index)
  workitems/  WI-*.md            (INDEX.md = generated)
  conflicts/  CF-*.md            (INDEX.md = generated)

  # identification
  team/       <handle>.md        (INDEX.md = generated)

  # work layer (feature branch, per-item single-writer)
  sessions/   <handle>--<WI-id>.md   archive/   (INDEX.md = generated)
  history/    YYYY/MM/HIST-*.md                  (INDEX.md = generated, recorded by INTEGRATE)
  assumptions/ ASM-*.md                          (INDEX.md = generated)
  notes/      <topic>.md  <topic>/*.md           (INDEX.md = generated)

  # inputs
  SOURCES/
    REQUIREMENTS.md              # initial requirements (kept frozen)
    SRC-*.md                     # immutable original content
    SRC-*.meta.md                # mutable triage (per-source single-writer)
    INDEX.md                     # generated

  # spec·review harness (kept — the paper's core contribution)
  features/*.md   personas/*.md   discussion/review-*.md   adr/ADR-*.md   docs/  qa/

  templates/                     # schema examples (askctl excludes from scanning)
```

> We don't keep `locks/`. Advisory locks have no enforcement and are defenseless against stale locks, so global-contract protection is replaced by **maintainer single-writer + ADR gate + merge order** (§7, CONVENTIONS §6).

---

## 4. Identity — anchored to git identity

We don't reinvent developer identity. We use the **git identity already on every commit** (email) as the basis, validated by the `team/` registry.

- **Anchor key:** `git config user.email` (unique). `user.name` is for display.
- **Two axes:** responsible party (human = commit author) / executor (agent = `Co-Authored-By` trailer).
- **Registry:** `team/<handle>.md` (per-person, single-writer) + generated `team/INDEX.md`.
- **Auto-resolution:** `python askctl.py whoami` → matches the git email against the registry and returns `handle`·`role`. Unregistered → entry blocked.
- **Trust model:** soft identity (attribution·conflict avoidance·validation) is provided by markdown; hard identity (blocking impersonation) is delegated to the git platform (protected branch · signed commit · CODEOWNERS).

For detailed conventions see [CONVENTIONS.md §2](CONVENTIONS.md).

---

## 5. Status & index — unified as generated artifacts

The keystone decision the recent design discussion converged on. **A single mechanism applied uniformly across every directory.**

```text
- Source of truth (SoT) = the frontmatter in each item file (a single writer writes only their own file)
- INDEX.md = a generated artifact produced by askctl scanning frontmatter
    · .gitignore'd → not committed to git → zero conflicts, zero stale
    · mandatory session-start step: run `python askctl.py index`, then read
    · never edit INDEX.md by hand (it gets overwritten)
```

Effects:
- **Concurrent INDEX-edit conflicts are structurally impossible** (nobody writes it by hand).
- The row-duplication silent-corruption problem of applying `merge=union` to a status table **disappears** (INDEX isn't in git).
- A deterministic script means **zero LLM tokens** for index generation.
- Trade-off: the INDEX isn't visible on GitHub web → generate with `askctl.py index`. Acceptable for an agent-first framework.

---

## 6. Semantic-conflict detection & global-contract serialization

**Detection trigger (auto-run at two points: claim · integrate):**

```text
python askctl.py detect <WI-id>
  cross-check my touches against every other workitem with status ∈ {claimed, in_progress}
    · contracts overlap → STOP. maintainer serializes (below)
    · modules overlap   → WARN. register in conflicts/CF-*.md + agree on order
    · none              → OK. proceed
```

**Global-contract serialization (instead of locks):**

```text
ARCHITECTURE / global-contract change =
  ① a dedicated workitem declaring touches.contracts + an ADR(Proposed)
  ② askctl detect → STOP notice to in-flight workitems touching the same contract
  ③ maintainer merges the contract-change workitem first, ADR→Accepted, updates ARCHITECTURE
     (maintainer is ARCHITECTURE single-writer → concurrent editing blocked at the source)
  ④ dependent workitems rebase onto the new contract
```

---

## 7. Development flow

```text
1. Gather requirements   SOURCES/SRC-*.md (immutable original) + SRC-*.meta.md (triage)
2. Decompose / claim     write workitems/WI-*.md (touches) → commit to shared branch → askctl detect
3. Develop               feat/WI-* branch: code + feature/qa/notes/assumptions (work layer)
                         review non-trivial features via personas/discussion
4. review                WI status=review, PR
5. INTEGRATE             maintainer: re-cross touches → merge → record history
                         → SRC-*.meta status=applied → update PLAN → askctl index → full regression
6. audit                 periodic: orphan WIs / undetected touches / neglected SRC / link integrity
```

**Atomic commit (redefined):** a feature-branch atomic commit = **code + that workitem's work-layer files**. It does **not** include generated INDEX, ARCHITECTURE/PLAN (maintainer), or history (INTEGRATE). The "code and corresponding docs in one commit" principle is kept *within the workitem scope*.

---

## 8. Quick start

1. Clone this repository and copy the contents of `en/ASK-TEAM/` into the project root's `AGENTSPECKIT/`.
2. **The maintainer** registers their own `team/<handle>.md` first with `role: maintainer`. Each contributor also registers their own `team/<handle>.md`.
3. Always, at session start:
   ```bash
   python AGENTSPECKIT/askctl.py whoami     # confirm my handle/role
   python AGENTSPECKIT/askctl.py index      # regenerate the index, then read
   ```
4. Contributors work with the `DEVELOP.md` prompt, the maintainer with `INTEGRATE.md`.

> The initialization (KICKOFF)·adoption (ADOPT)·audit (AUDIT) prompts extend the solo ASK ones to fit team conventions; this release fixes the core three (`DEVELOP`·`INTEGRATE` + `askctl`) first.

---

## 9. Differences from solo ASK

| Item | solo ASK | ASK-Team |
|---|---|---|
| progress state | `PROGRESS.md` single cursor | `workitems/` + `sessions/<handle>--<WI>` |
| history | `HISTORY.md` append | `history/YYYY/MM/HIST-*.md` (recorded by INTEGRATE) |
| assumptions | `ASSUMPTIONS.md` single | `assumptions/ASM-*.md` |
| notes | `NOTES.md` single | `notes/<topic>.md` |
| requirement state | `SOURCES/INDEX.md` rows (mutable) | `SRC-*.meta.md` (per-source) + generated INDEX |
| index | hand-updated | **generated (gitignore)** |
| identity | not needed | `team/` + git identity + `askctl whoami` |
| semantic conflict | n/a | `touches` + `askctl detect` + `conflicts/` |
| global contract | ADR | ADR + **maintainer single-writer + merge order** |

---

## 10. Honest limitations (no unfounded positivity)

1. **Governance ≠ tooling.** Multi-human intent conflicts are solved only by maintainer arbitration. The framework only surfaces conflicts; it can't create consensus.
2. **Detection ≠ enforcement.** If `touches` is undeclared/misdeclared, detection fails. INTEGRATE's full cross-check is the last net, but it's after the fact.
3. **The cost is an intended trade-off.** It accepts per-session overhead (more always-loaded context) and the maintainer's INTEGRATE burden. For solo, solo ASK is cheaper.
4. **Single point of failure.** The maintainer can become a bottleneck → multiple maintainers are possible, but the ARCHITECTURE single-writer discipline is kept by domain partitioning.
5. **INDEX invisibility.** The cost of gitignore is that there's no index when browsing on the web → generate with `askctl.py index`.

---

## 11. Files that make up this kit

| File | Role |
|---|---|
| `README.md` | this document — framework overview·spec |
| `CONVENTIONS.md` | structural conventions (file grades·identity·INDEX·conflicts·contracts·atomic commits·SOURCES) |
| `SCHEMAS.md` | frontmatter schemas (workitem·source·assumption·session·team·conflict) |
| `DEVELOP.md` | contributor development prompt (claim → detect → work) |
| `INTEGRATE.md` | maintainer integration prompt (re-cross → merge → history → index) |
| `askctl.py` | coordination tool (`index` · `detect` · `whoami`) |
| `.gitignore` | rules excluding generated INDEX.md |
| `templates/` | example files for copying schemas |
