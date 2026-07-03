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
