# INTEGRATE.md — Maintainer integration prompt

The **maintainer-only** procedure for merging multiple contributors' feature branches into the shared branch.
It covers semantic-conflict re-detection, global-contract serialization, history recording, and full regression.
[CONVENTIONS.md](CONVENTIONS.md) takes precedence on conventions.

> This kit uses markdown + git only. The "identity check"·"detection" are performed directly by the agent using `git` and file reads.
> Only `role: maintainer` runs this prompt.

---

## 0. Session start (mandatory)

1. **Identity check** — match `git config user.email` against `team/*.md`. If `role` is not `maintainer`, stop and delegate to a maintainer.
2. **Survey the state** — `git fetch` first, then gather the workitems with `status: review` and their PRs/branches from the latest shared branch (CONVENTIONS §4.5).

---

## 1. Collect integration targets

* Gather the workitems with `status: review` and their PRs/branches from `workitems/*.md`.
* Check each workitem's `touches` (contracts/modules) and `depends_on`.

---

## 2. Re-detect conflicts (before merge — mandatory, performed by the agent)

After `git fetch` (CONVENTIONS §4.5), exhaustively cross-check the `touches` of the integration candidates + all other in-flight (`claimed`/`in_progress`) workitems.

* **contracts overlap (STOP):** two or more touch the same global contract → handle via §3 serialization. Do not merge them concurrently.
* **modules overlap (WARN):** check whether `conflicts/CF-*.md` has a resolution decision. If not, register it and proceed after agreeing on order with the owners.
* **Identity validation:** verify each candidate's feature-branch commit author email matches `WI.owner`'s registered email (mismatch = "claimer ≠ worker" → report).

---

## 3. Global-contract serialization (contract-change workitem first)

If there's a workitem with `touches.contracts`, handle **it first**.

1. Confirm the corresponding ADR is `Accepted` (if not, review·approve).
2. Merge the contract-change workitem.
3. **The maintainer** updates `ARCHITECTURE.md` (and `PLAN.md` if needed) — this is the maintainer single-writer domain.
4. Notify the owners of the remaining workitems that were `touch`ing the same contract to **rebase onto the new contract** (don't merge before they rebase).

---

## 4. Merge

Merge the PRs in serialization order (contract change → dependent workitems → independent workitems).

* Resolve git conflicts via the normal procedure.
* Since there are no fixed INDEX files, INDEX merge conflicts don't occur.
* After merge, change each `WI-*.md` status to `done` (the maintainer commits this on the shared branch — the sanctioned exception to the WI single-writer rule, CONVENTIONS §4.1).

---

## 5. History recording (maintainer single-writer)

For each merged workitem, create `history/YYYY/MM/HIST-<YYYYMMDD-hhmm>-<slug>.md` as a **new file** (`templates/` format). Include: the completed workitem, related commits, test results run, related sources, QA, impact scope, follow-up.

> Only INTEGRATE records into `history/`. Contributors don't write to `history` (eliminates append contention).

---

## 6. Update SOURCES status

For a source whose requirement is fully applied via merge, change `status` in `SOURCES/SRC-*.meta.md` to `applied` and link the applied artifacts. Use `applied` only when every item is reflected (partial reflection stays `under_review`).

---

## 7. Full regression & PROGRESS

* **Actually run the full regression tests** — individual contributors only saw their own part, so verify the whole at integration time. Record the results in history.
* Sample-check that `ARCHITECTURE.md` contracts are upheld in recent code (if violated, `conflicts/` or a follow-up workitem).
* Keep `PROGRESS.md` (compatibility stub) pointing at the item files — state that the truth of progress is the `workitems/*.md` frontmatter (no fixed INDEX).

---

## 8. Completion report format

```md
# Integration result (INTEGRATE)
## Merged workitems (order and rationale)
## Global-contract changes (ARCHITECTURE/ADR)
## Re-detection results (STOP/WARN and resolution)
## Identity validation (owner ↔ commit author mismatch?)
## Recorded history events
## SOURCES status changes (applied processing)
## Full regression results (commands run / pass·fail)
## Remaining review/blocked workitems
```

---

## 9. Relationship to periodic audit

INTEGRATE handles *merge-time consistency*; AUDIT handles *recovery of gradual drift*. Before a Phase completion/release, run AUDIT separately to check orphan workitems, undetected `touches` overlaps, neglected `SRC-*.meta` (unapplied), broken links, and stale sessions.
