# AUDIT.md — Team document audit (ASK-Team)

Periodically check the drift that accumulates in concurrent team development and the **integrity of the coordination structure**.
In addition to the general drift checks of the solo kit [AUDIT.md](../AGENTSPECKIT/AUDIT.md) (plan↔actual, assumption lifetime, spec↔code, links, history hygiene), add **team-specific checks**.

> [CONVENTIONS.md](CONVENTIONS.md) takes precedence on conventions. INTEGRATE handles *merge-time consistency*, AUDIT handles *recovery of gradual drift*.

---

# 1. When to run

* Right after Phase completion / before release / on resuming after a while / ~10 sessions accumulated since the last audit / when drift is suspected
* **Regularly while multiple contributors are active concurrently** (the more in-flight workitems, the more often)

---

# 2. Audit principles

1. Don't modify functional code.
2. **Fix mechanical mismatches immediately** (broken links, obvious status typos). Since there are no fixed INDEX files, there is no index-regeneration step.
3. **Only record semantic drift** (code↔spec via DEVELOP authority diagnosis, touches overlap via conflicts/).
4. Record audit results in `history/YYYY/MM/HIST-*.md` as an `audit` event (maintainer).

---

# 3. Audit items

## 3.1 General (inherits solo AUDIT 3.1~3.12)
plan↔actual, assumption lifetime, spec↔code sample, index integrity, links/orphans, history hygiene, README, SOURCES, always-loaded bloat, review logs (sources real), backlog, artifact language consistency.
**Team difference:** "assumptions/history/notes" check the `assumptions/`·`history/`·`notes/` directories, not a single file.

## 3.2 Confirm absence of fixed INDEX
* Has someone created and committed a fixed index file like `INDEX.md` — this kit doesn't keep fixed INDEX (if found, report as a deletion candidate). The listing·status is always read directly from item file frontmatter.

## 3.3 workitem hygiene
* workitems long stuck in `claimed`/`in_progress` (e.g. 14 days+) — ask the owner to re-confirm status.
* Is `owner` a registered active handle in `team/` (unregistered·inactive → flag).
* workitems that are `done` but have no corresponding `history/` event / workitems with broken `feature`·`source_refs` links.
* Orphan workitems (not linked to any PLAN Phase·source).

## 3.4 Undetected touches overlap (core)
* Read the `touches` of all in-flight (`claimed`/`in_progress`) workitems and cross-check pairwise (performed directly by the agent).
  * **contracts overlap with no `conflicts/CF` and no serialization** → report immediately (maintainer serialization needed).
  * **modules overlap with `conflicts/CF` unregistered** → register CF as a follow-up.

## 3.5 Identity / permission integrity
* Are all recent commit author emails registered in `team/` (unregistered author = attribution pollution).
* Does `WI.owner` match the commit author of that feature branch (claimer ≠ worker).
* **single-writer violation:** did a contributor edit `ARCHITECTURE.md`/`PLAN.md` directly (via git history). Is there an ADR for the global-contract change.

## 3.6 conflicts / sessions / SOURCES
* `conflicts/CF-*.md` left in `open` for a long time.
* Is an `active` session in `sessions/` hanging on work that is actually finished (done workitem) → candidate for moving to `archive/`.
* Change requests left in `SRC-*.meta.md` as `not_applied`/`under_review` (user intent unapplied) / has the original (`SRC-*.md`) been modified after `applied` (immutability violation, via git history).

---

# 4. Handling rules

| Finding | Handling |
|---|---|
| broken link / status typo | fix immediately |
| fixed INDEX file committed | report as a deletion candidate (no fixed INDEX) |
| undetected contracts overlap | report immediately → maintainer serialization (INTEGRATE §3) |
| undetected modules overlap | register `conflicts/CF` as a follow-up |
| neglected workitem / unregistered owner | re-confirm with owner·maintainer, state in the report |
| single-writer violation (direct ARCHITECTURE edit) | don't revert; record → retroactive ADR or maintainer review |
| unregistered author commit | request team/ registration, state in the report |
| neglected unapplied SRC / immutability violation | state in PROGRESS·report; for immutability violations confirm with maintainer whether to split into a new SRC |

Register follow-ups in `workitems/` (proposed) or PLAN, and record the whole audit in `history/` as an `audit` event.

---

# 5. Output format

```md
# Team document audit result
## Audit scope / sampling criteria
## Immediate fixes (mechanical)
## Undetected touches overlap (contracts STOP / modules WARN)
## workitem hygiene (neglected / unregistered owner / orphan / broken links)
## Identity·permission integrity (unregistered author / owner≠author / single-writer violation)
## conflicts·sessions·SOURCES status
## General drift (plan↔actual / assumption lifetime / spec↔code sample)
## Items needing user confirmation
## Follow-ups (reflected in workitems/PLAN)
```

---

# 6. Completion conditions

* §3 checks complete (state sampling criteria), pairwise cross-detection of in-flight workitem `touches` performed
* Mechanical mismatches fixed immediately
* Undetected overlaps·single-writer violations·unregistered authors compiled in the report and follow-ups
* `audit` event recorded in `history/`
