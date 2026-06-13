> 🌐 **English** · [한국어](AUDIT.ko.md)

# AUDIT.md

A **document audit prompt** for periodically checking the drift between your project documentation and code.

"Point-of-record checks" such as conflict detection when recording a new assumption already exist in KICKOFF/DEVELOPINIT.
However, the gradual drift that accumulates as sessions pile up — a PLAN that is complete but never updated, active assumptions that should have been dropped,
feature specifications that have slowly diverged from the code, missing index entries, broken document links — is
not caught by point-of-record checks alone. AUDIT recovers these periodically.

> **Path basis:** Except for the three root files (the project's `README.md`, `AGENTS.md`, `CLAUDE.md`), all framework documents
> live inside the `AGENTSPECKIT/` folder. All artifact paths in this document are relative to `AGENTSPECKIT/`.
> During the audit, also check that no artifact has been created outside of AGENTSPECKIT/.

---

# 1. When to Run

Running is recommended if any of the following applies.

* Immediately after a Phase is completed
* Before a release / deployment (together with `qa/release-checklist.md`)
* When resuming a project after a long break
* When roughly 10 or more sessions have accumulated since the last audit
* When you suspect that the documentation and the actual behavior have diverged

---

# 2. Audit Principles

1. **Do not modify feature code in this step.** The audit is a checking and recording step.
2. **Fix mechanical inconsistencies immediately.** Items that require no judgment — such as missing index entries, broken links, or missing status markers —
   are fixed right away in the audit commit.
3. **Record semantic drift instead of fixing it.** Code↔specification inconsistencies are the subject of DEVELOPINIT 3.4 (authority diagnosis),
   so here you only record the findings and separate the handling into a development task.
4. **The audit itself is work.** Record the result in HISTORY.md as an `audit` entry.

---

# 3. Audit Items

## 3.1 Plan vs. Actual (PLAN / PROGRESS)

* Does the Phase status in PLAN.md match HISTORY.md and the actual code?
* For Phases marked complete, is there evidence in HISTORY.md for their completion criteria (including that tests were actually run)?
* Does the "first command for the next session" in PROGRESS.md match the current state?

## 3.2 Assumption Lifecycle (ASSUMPTIONS)

* Among assumptions with `status: active`, those that should already have been confirmed or dropped by a user answer / ADR / implementation
* Assumptions that conflict with each other or diverge from ARCHITECTURE.md

## 3.3 Specification vs. Code (features / ARCHITECTURE) — Sampling

* Pick 1–3 feature documents that have changed the most recently and compare the specification against the actual code
* Spot-check whether the contracts in ARCHITECTURE.md (naming / error format / authentication, etc.) are upheld in recent code
* Do not fix inconsistencies here; only record them (Principle 3)

## 3.4 Index Integrity

* Are all feature documents listed in `features/README.md`, and is their status accurate?
* Are all ADRs in `adr/INDEX.md`, and is their status accurate?
* Does `docs/README.md` match the actual files in the docs/ folder?

## 3.5 Links / Orphan Documents

* Broken relative-path links between documents
* Orphan documents not referenced by any index

## 3.6 History / Notes Hygiene

* Whether HISTORY.md needs rotation (per KICKOFF.md Section 14)
* Whether HISTORY entries follow the fixed-prefix format (`## [YYYY-MM-DD] <type> | <title>`)
* Whether NOTES.md contains conjectures that should have gone into ASSUMPTIONS (fact/assumption distinction)

## 3.7 Project README

* Whether the README's installation / run / structure descriptions match the current code (spot-check)

## 3.8 Submitted Materials (SOURCES)

* Are there items left in `Not applied` / `Under review` status?
  (Especially change requests — a state where the user's intent is sitting dormant, not yet reflected in an artifact)
* Does SOURCES/INDEX.md match the actual file list? (unregistered files / missing files)
* Are the artifact links of `Applied` items valid?
* Has the original not been modified after `Applied`? (immutability-principle violation — verify via git history)

## 3.9 Always-Loaded Document Bloat (Monitoring)

* If the number of completed Phases in PLAN.md **exceeds 4**, or if ARCHITECTURE.md still contains background explanations or deprecated past contracts
  rather than contract declarations, **mark it as a diet candidate in the report**.
* This item is for monitoring. Do not compress or migrate documents here; once a threshold breach is reported,
  decide with the user whether to introduce rotation rules (e.g., archiving completed Phases).

## 3.10 Review Logs (discussion) — Spot-Check

* Does each non-trivial feature document have a review log link? (If not, suspect a missing review)
* Open 1–2 sample logs and check whether the **sourcing obligation** was met — in particular, whether the
  sources the Research Agent cited (URL, SOURCES/ path, document name) **actually exist** (a nonexistent source = a signal of a forged review)
* Does the log follow the structure in KICKOFF.md 4.1 (review per persona / issues / conclusion), and is it not a theatrical log that merely lists generic platitudes?
* Do the participating personas in the log actually exist as instances in `personas/`, and do they match the INDEX?
* Do the persona instances contain only links and checklists, without copying knowledge (the KICKOFF.md 5.2 rule)?
* Are there orphan logs not linked from any feature?

## 3.11 Backlog (TODO)

* Are there items left in `Pending` status for a long time? (e.g., 60+ days — report as candidates for reclassification into promotion/on hold/dropped)
* Are the promotion-target links of `Promoted` items valid?
* Are there items whose promotion-target work is complete but whose TODO status has not been updated to `Done`?
* Does the TODO contain specification-level detail? (Specifications belong in features/ — the KICKOFF.md 15.3 role boundary)

## 3.12 Artifact Language Consistency — Spot-Check

* Is the descriptive prose of sample documents (1–2 each from feature/docs) consistent with the prescribed language (the primary language in SOURCES/REQUIREMENTS.md or the designated "artifact authoring language")?
* Is there no mixing where the prose language changes from section to section within a single document?
  (English in code identifiers, API paths, code blocks, and technical proper nouns is normal — that is not mixing)
* If mixing is found, do not fix it; mark it in the report like a diet candidate, and separate the cleanup into a separate document task

---

# 4. Handling Rules

| Finding type | Handling |
|---|---|
| Missing index entry / broken link / wrong status marker | Fix immediately (include in the audit commit) |
| Assumption that should have been confirmed/dropped | Update status if the evidence is clear; record as "verification needed" if unclear |
| Code↔specification inconsistency | Do not fix; record in the findings list → separate into a task to be handled via DEVELOPINIT 3.4 |
| HISTORY rotation needed | Can be performed immediately (the KICKOFF.md Section 14 rule) |
| Code violating an ARCHITECTURE contract | Record only; the fix becomes a development task |
| Neglected Not-applied / Under-review change request | List it in PROGRESS.md's remaining work and state it in the report |
| Missing review log / nonexistent source / theatrical log | Separate the re-review of that feature into a follow-up task and state it in the report |
| Post-hoc modification of an Applied original (immutability violation) | Do not revert it arbitrarily; confirm with the user whether to separate the modification into a new request document |
| Item that cannot be judged | Summarize under "Items requiring user confirmation" |

Reflect any follow-up work arising from the audit into PROGRESS.md's `remaining work` (and PLAN.md if needed),
and record the entire audit result in HISTORY.md as a `## [YYYY-MM-DD] audit | document audit` entry.
Bundle the mechanical fixes and the audit record into a single commit (use a `docs/...` work branch;
the prohibition on pushing directly to main/master applies the same way).

---

# 5. Output Format

After completing the audit, report in the following format.

```md
# Document Audit Result

## Audit Scope / Sampling Criteria

## Items Fixed Immediately (Mechanical)

## Drift Found (Needs Handling)

- Code↔specification inconsistency:
- Assumption lifecycle issues:
- Plan↔actual inconsistency:

## Index / Link Status

## Submitted Materials (SOURCES) Status

## HISTORY / NOTES Hygiene

## Always-Loaded Document Bloat (PLAN completed-Phase count / whether ARCHITECTURE background remains)

## Review Log Spot-Check Result (including whether sources actually exist)

## Backlog (TODO) Status (neglected / links / completion not reflected)

## Artifact Language Consistency (sample result)

## Items Requiring User Confirmation

## Follow-up Work Proposal (content reflected into PROGRESS.md)
```

---

# 6. Completion Criteria

* Checking of the Section 3 items is complete (for sampling items, the selection criteria are stated)
* Mechanical inconsistencies are fixed immediately and committed
* Semantic drift is organized into a findings list and reflected into PROGRESS.md
* An `audit` entry is recorded in HISTORY.md
* Reported in the Section 5 format
