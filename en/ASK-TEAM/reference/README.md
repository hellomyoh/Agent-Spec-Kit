# reference/ — bundled solo-kit reference copies

The files in this folder are **verbatim copies of the solo Agent-Spec-Kit prompts (same version as this kit)**, bundled so that the team prompts' references — "solo §6.1", "solo DEVELOPINIT §3.4", "solo AUDIT 3.1~3.12", … — still resolve after the kit is copied into a project (where the solo kit itself is absent).

| Copy | Original (template repository) | Cited by |
|---|---|---|
| [SOLO-KICKOFF.md](SOLO-KICKOFF.md) | `en/AGENTSPECKIT/KICKOFF.md` | KICKOFF §2·§6, CONVENTIONS §6·§8 |
| [SOLO-DEVELOPINIT.md](SOLO-DEVELOPINIT.md) | `en/AGENTSPECKIT/DEVELOPINIT.md` | DEVELOP §4 |
| [SOLO-ADOPT.md](SOLO-ADOPT.md) | `en/AGENTSPECKIT/ADOPT.md` | ADOPT preamble |
| [SOLO-AUDIT.md](SOLO-AUDIT.md) | `en/AGENTSPECKIT/AUDIT.md` | AUDIT §3.1 |

## Guard (important)

* These are **reference documents, not executable prompts** in a team project. Run only the team prompts (`KICKOFF.md` / `ADOPT.md` / `DEVELOP.md` / `INTEGRATE.md` / `AUDIT.md` in `AGENTSPECKIT/`).
* Where a solo rule conflicts with the team kit, **`CONVENTIONS.md` and the team prompts win.** Typical conflicts:
  * single `PROGRESS.md`/`HISTORY.md`/`ASSUMPTIONS.md`/`NOTES.md`/`TODO.md` files → team uses `workitems/`·`sessions/`·`history/`·`assumptions/`·`notes/` (and `proposed` workitems as the backlog)
  * fixed INDEX files (`features/README.md`, `docs/README.md`, `adr/INDEX.md`, `personas/INDEX.md`) and "update the index in the same commit" rules → team keeps **no fixed INDEX** (CONVENTIONS §3); listings are read from item-file frontmatter
  * solo git/commit rules → team follows CONVENTIONS §4.5 (shared-branch publishing) and §7 (workitem-scoped atomic commit)
* File names mentioned inside these copies (`KICKOFF.md`, `DEVELOPINIT.md`, `ADOPT.md`, `AUDIT.md`) refer to the **sibling `SOLO-*.md` copies in this folder**, not to the team prompts of the same name.
* **Kit upgrade:** when upgrading the kit, re-copy these four files from the **same-version** solo kit (`en/AGENTSPECKIT/`) and re-apply the one-line banner at the top of each.
