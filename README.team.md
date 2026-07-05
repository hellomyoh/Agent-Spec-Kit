<div align="center">

# ASK-Team — Agent-Spec-Kit for team development

🌐 **English** · [한국어](README.team.ko.md)

**The Team edition of [Agent-Spec-Kit](README.md).** When multiple developers and AI agents build the *same* codebase **concurrently**, ASK-Team uses **markdown + git alone** to surface the Git, semantic, and intent conflicts that a single shared `PROGRESS.md` / `HISTORY.md` would otherwise hide.

Solo guide: [README.md](README.md) · Full team guide & prompts: [en/ASK-TEAM/](en/ASK-TEAM/) · [한국어 키트](ko/ASK-TEAM/)

</div>

---

## Solo or Team?

| | **Solo (ASK)** — [README.md](README.md) | **Team (ASK-Team)** — this guide |
|---|---|---|
| For | 1 developer / sequential, autonomous | multiple developers & AI agents, **concurrent** |
| Progress | single `PROGRESS.md` cursor | `workitems/` + `sessions/<handle>--<WI>` |
| History / assumptions / notes | single files | `history/` · `assumptions/` · `notes/` directories |
| Indexes | hand-updated | none — frontmatter read directly |
| Conflicts | n/a | `touches` + `conflicts/` (agent cross-checks) |
| Identity | not needed | `team/` + git identity (`git config user.email`) |
| Runtime | none | none (markdown + git only) |
| Kit folder | `en/AGENTSPECKIT/` · `ko/AGENTSPECKIT/` | `en/ASK-TEAM/` · `ko/ASK-TEAM/` |

For a single developer, Solo is lighter — use Team only when N people actually develop concurrently.

## Core ideas

- **Git branch isolation is the root fact.** Contributors can't see each other's *uncommitted* files, so a workitem's coordination metadata (its `touches`) is **published to a shared branch at claim time** → conflicts surface early, not at merge.
- **Two artifact layers.** *Coordination* (workitems, conflicts, `ARCHITECTURE.md`/`PLAN.md`) lives on the shared branch; *work* (code, feature specs, qa, notes, assumptions) lives on the isolated feature branch.
- **Roles.** A **Maintainer** owns the global contracts, runs `INTEGRATE`, and arbitrates intent conflicts as ADRs. **Contributors** claim workitems and own their scoped files.
- **No fixed INDEX files.** Each item file's frontmatter is the source of truth and the agent reads directories directly — so concurrent index-edit conflicts simply don't exist.
- **Identity = git identity.** `git config user.email` validated against a `team/<handle>.md` registry — no extra runtime.

## Quick start

1. Clone this repo and copy the contents of [`en/ASK-TEAM/`](en/ASK-TEAM/) (or [`ko/ASK-TEAM/`](ko/ASK-TEAM/)) into your project root's `AGENTSPECKIT/`.
2. For a **new project**, write the initial requirements in `AGENTSPECKIT/SOURCES/REQUIREMENTS.md` (reuse the solo kit's [REQUIREMENTS template](en/AGENTSPECKIT/SOURCES/REQUIREMENTS.md)); for an existing codebase (ADOPT) it is optional.
3. The **maintainer** registers `team/<handle>.md` with `role: maintainer` (copy `templates/team-TEMPLATE.md`); each **contributor** registers their own.
4. Contributors run the [`DEVELOP.md`](en/ASK-TEAM/DEVELOP.md) prompt; the maintainer runs [`INTEGRATE.md`](en/ASK-TEAM/INTEGRATE.md). Use [`KICKOFF.md`](en/ASK-TEAM/KICKOFF.md) (new) / [`ADOPT.md`](en/ASK-TEAM/ADOPT.md) (existing code) to initialize, and [`AUDIT.md`](en/ASK-TEAM/AUDIT.md) for periodic checks.

## Kit upgrade (applying a new version to an already-initialized team project)

Use this to reflect template-repository updates into a project that already ran KICKOFF/ADOPT. **Don't re-run KICKOFF or ADOPT** — the re-initialization/re-adoption guard blocks them, and bypassing it overwrites coordination-layer content. **Only `role: maintainer` runs this** (it rewrites kit-owned files and the root rule files — both maintainer-only domains).

| Category | Target | Processing |
|---|---|---|
| Kit-owned (no project content) | `KICKOFF.md`·`ADOPT.md`·`DEVELOP.md`·`INTEGRATE.md`·`AUDIT.md`·`CONVENTIONS.md`·`SCHEMAS.md`·`README.md`·`templates/`·`reference/` | **Overwrite-copy** from the same-version, same-language kit folder |
| Coordination/work artifacts (project content) | `ARCHITECTURE.md`, `PLAN.md`, `workitems/`, `conflicts/`, `team/`, `sessions/`, `history/`, `assumptions/`, `notes/`, `SOURCES/` originals, `features/`, `personas/`, `discussion/`, `adr/`, `docs/`, `qa/` | **Preserve content** — do not touch |
| Root rule files | `AGENTS.md` | **Merge-update** — add only missing team-convention blocks |
| | `CLAUDE.md` | **Replace** with the new KICKOFF.md template (malfunction-prevention only) — lossless gate |
| New structure (absent in the old version) | e.g. `workitems/archive/` | **Newly create** (`.gitkeep` if empty) and **migrate qualifying existing data** into it |

**Step 1 (human, maintainer):** pull the template repository and overwrite-copy the kit-owned files above **from the same language folder you originally used** (`en/ASK-TEAM/` or `ko/ASK-TEAM/`) into the project's `AGENTSPECKIT/`. Since these are coordination-layer files, do this directly on the shared branch (or a work branch + PR first if the shared branch is push-protected — merge before any contributor resumes claiming).

**Step 2 (Agent):**

```text
The ASK-Team kit has been updated and its kit-owned files have been replaced with the new version.
Upgrade this project's artifact structure to the new-version standard.
Do not re-run KICKOFF or ADOPT (re-initialization/re-adoption forbidden). Preserve the content of existing coordination/work artifacts.
Only role: maintainer runs this prompt.

0. Identity check: match git config user.email against team/*.md. If role is not maintainer, stop and delegate to a maintainer.
   git fetch and read the latest shared branch before comparing structure.
1. Compare the structure in the new KICKOFF.md §1 against the current AGENTSPECKIT/ and list missing files/folders.
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

## Prompts & reference (in [`en/ASK-TEAM/`](en/ASK-TEAM/))

| File | Role |
|---|---|
| [README.md](en/ASK-TEAM/README.md) | full framework overview & spec |
| [KICKOFF.md](en/ASK-TEAM/KICKOFF.md) · [ADOPT.md](en/ASK-TEAM/ADOPT.md) | initialize a new / existing team project |
| [DEVELOP.md](en/ASK-TEAM/DEVELOP.md) · [INTEGRATE.md](en/ASK-TEAM/INTEGRATE.md) | contributor / maintainer prompts |
| [AUDIT.md](en/ASK-TEAM/AUDIT.md) | team document audit (drift + coordination integrity) |
| [CONVENTIONS.md](en/ASK-TEAM/CONVENTIONS.md) · [SCHEMAS.md](en/ASK-TEAM/SCHEMAS.md) | structural conventions & frontmatter schemas |
| [reference/](en/ASK-TEAM/reference/README.md) | bundled solo-kit reference copies cited by the team prompts |

> ASK-Team keeps the Solo philosophy — markdown + git, tool independence (Claude Code · Codex · Cursor), cross-session memory, traceability, the multi-persona review harness. See the **[full guide](en/ASK-TEAM/README.md)** for the conflict-detection model, the development flow, and the honest limitations (detection ≠ enforcement; governance ≠ tooling).
