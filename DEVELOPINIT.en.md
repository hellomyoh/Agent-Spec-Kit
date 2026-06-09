# DEVELOPINIT.md

> English version of the DEVELOPINIT development prompt. File references use canonical names.

Proceed with actual development based on the current project documents.

In this stage, do not re-analyze the project from scratch or re-initialize it.

Develop the current Phase based on the documents already created.

---

# 1. Documents to Check Before Starting Development

## 1.1 Always-Loaded Documents (Required)

Read the following **always** at the start of every session. They are not subject to selective loading.

1. AGENTS.md
2. ARCHITECTURE.md  (cross-cutting contract: data model · naming · API contract · auth model, etc.)
3. PLAN.md
4. PROGRESS.md

Check the `first command for the next session` in `PROGRESS.md` first.

## 1.2 Selectively-Loaded Documents

Read only the following that the current work needs.

5. HISTORY.md (check recent history to prevent duplicate implementation)
6. features/README.md
7. `features/*.md` related to the current Phase
8. adr/INDEX.md (check for related ADRs → if any, read the relevant `adr/*.md`)
9. qa/README.md
10. Relevant `qa/*.md` if needed
11. Relevant `docs/*.md` if needed

Important:

* Do not bulk-load all feature documents. Read only those related to the current work.
* Do not always bulk-load all QA documents. Read only what is needed.
* **Before selecting feature documents, check `adr/INDEX.md`** to see whether there is a decision affecting the current work.
* **Always follow `ARCHITECTURE.md` for common rules (data model/naming/API contract/auth).** They are not duplicated in feature documents.
* AGENTINIT.md is the initialization input document; do not use it as a reference for the development stage.
* The project `README.md` is a **deliverable (derived document)**. It is not the source of truth, so do not always load it; only check whether it needs updating per push (see 4.1).
* The reference documents for the development stage are AGENTS.md, ARCHITECTURE.md, PLAN.md, PROGRESS.md, features/*.md, qa/*.md.

---

# 2. Development Principles

* Do not re-initialize the project.
* Do not implement by guessing without a spec.
* Before implementing, check whether the relevant feature documents and ARCHITECTURE.md items exist.
* **When code and spec differ, do not immediately fix one side. First diagnose which side is the authority.** (see 3.4)
* Record and follow common decisions (data model/naming/API/auth) in ARCHITECTURE.md. Do not scatter them across feature documents.
* When feature scope changes, re-run a Multi-Agent review with the needed Agent personas.
* Leave ADRs for important design decisions and update `adr/INDEX.md`.
* Reflect changes the user needs to understand in the docs documents.
* Treat tests and QA as part of the implementation. Actually run the tests.
* Record work progress in PROGRESS.md.
* Record work history in HISTORY.md.
* Record autonomous decisions in ASSUMPTIONS.md, after first checking for conflicts with existing assumptions/ARCHITECTURE.

---

# 3. User-Confirmation Rules During Development

In the DEVELOPINIT stage, perform actual development based on the already-created `AGENTS.md`, `ARCHITECTURE.md`,
`PLAN.md`, `PROGRESS.md`, `features/*.md`, `qa/*.md`.

In the development stage, do not stop frequently for minor ambiguities or routine implementation decisions.

The Agent decides as autonomously as possible based on the existing design intent and specs, and records those
decisions in `ASSUMPTIONS.md`, `HISTORY.md`, `PROGRESS.md` as it proceeds.

## 3.1 When to Ask the User

Ask the user only when a decision entirely different from the existing design intent is needed, such as:

* The existing MVP scope must change
* A feature must change in a direction different from the feature document's purpose
* The user-experience flow changes significantly
* The data model must change fundamentally
* The authentication / authorization / security policy must change
* The way personal or sensitive data is handled changes
* The external API or external-system integration approach must be replaced
* The deployment structure or operating method changes significantly
* Cost, billing, or legal impact may arise
* The cross-cutting contract in `ARCHITECTURE.md` must change
* Existing specs clearly conflict and the Agent cannot reasonably choose
* A hard-to-reverse data deletion or destructive change is needed

## 3.2 When You May Proceed Without Asking

Proceed on the following without asking. Record in `ASSUMPTIONS.md` if needed.

* Internal function/class/file names (but follow ARCHITECTURE.md naming conventions)
* Folder placement
* Generic error messages
* Test data names
* Mock data for local development
* Non-critical UI layout adjustments
* Code-style tidying
* Small refactors
* Test-case improvements
* Documentation wording improvements
* API implementation details that don't deviate from the feature document's intent and the ARCHITECTURE.md contract
* QA checklist improvements
* Minor adjustments to log messages or event names

## 3.3 How to Ask

When user confirmation is truly needed, minimize the questions and present the reason a decision is needed along
with the options.

Format:

```md
# User confirmation needed during development

To continue the current implementation, a decision different from the existing design intent is needed.

## Why confirmation is needed

<explain why the existing specs alone cannot decide>

## Options

1. <Option A>
2. <Option B>
3. <Option C>

## Agent's recommendation

<recommendation and reason>

After confirmation, I'll update ARCHITECTURE.md / feature docs / QA docs / implementation accordingly.
```

## 3.4 Handling Code–Spec Mismatch (Important)

When code and spec (feature/ARCHITECTURE) differ, do not immediately fix the spec to erase the mismatch.
This prevents retroactively disguising an implementation mistake "as if it were the spec."

Order:

1. Diagnose which side is the authority.
2. If the spec accurately captures the intent and the code is wrong → **fix the code.**
3. If the spec is confirmed to diverge from reality/intent → **update the spec first and align the code.**
4. If you cannot reasonably judge which is right → ask the user per 3.1.
5. Record the reasoning and the resolution in HISTORY.md (and ASSUMPTIONS.md if needed).

## 3.5 When the User Delegates a Decision ("just decide")

When the user explicitly delegates a particular decision during development (e.g., "just decide this", `[AI delegated]`),
the Agent's autonomy for that item broadens. However, handle by risk level.

* **Non-critical items**: decide reasonably, record in `ASSUMPTIONS.md`, and proceed.
* **Critical items** (the 3.1 kind): even when delegated, adopt **the most conservative, easily reversible choice**,
  record the decision/rationale in `ASSUMPTIONS.md` (`status: active`), and state it under `Autonomous Decisions` in the
  completion report. If it is a cross-cutting contract, also update `ARCHITECTURE.md`/ADR.
* **Cost/legal/destructive items** are never executed silently even when delegated; confirm per 3.3.

---

# 4. Development Procedure

For the current Phase, work in the following order.

1. Confirm the `first command for the next session` and the current Phase in PROGRESS.md
2. Check the relevant cross-cutting contract in ARCHITECTURE.md
3. Check that Phase's completion criteria and QA completion criteria in PLAN.md
4. Check related specs/decisions in features/README.md and adr/INDEX.md
5. Read only the needed feature documents and related ADRs
6. Check the feature document's test scenarios
7. Check the QA operating criteria in qa/README.md (check regression/manual if needed)
8. Analyze the affected code areas
9. Form an implementation plan
10. **Provisionally update `in-progress work` and `first command for the next session` in PROGRESS.md** (record at work start → if interrupted, the next session picks it up)
11. Implement
12. Write automated tests
13. **Actually run** the automated tests (capture the run command and results)
14. Fix failing tests
15. Review related regression-test impact
16. Decide whether manual QA is needed → if so, add/update entries in qa/manual-test-cases.md
17. Check code ↔ feature/ARCHITECTURE consistency (apply 3.4 on mismatch)
18. If common decisions changed, update ARCHITECTURE.md; for important decisions, write an ADR + update INDEX
19. Update docs documents
20. **Check whether the project README.md needs updating** (update if there is user/install/run/architecture impact — see 4.1)
21. Update the PLAN.md check status
22. Finalize PROGRESS.md (completed work / remaining work / first command for the next session)
23. Record implementation results, test-run results, and QA results in HISTORY.md
24. Record in ASSUMPTIONS.md if needed (check for conflicts with existing assumptions)
25. **Bundle code changes and corresponding doc changes (including README) into one atomic commit, and commit / push**

> Key: For continuity, PROGRESS is **provisionally recorded at work start (step 10)** and **finalized at the end (step 22)**.
> Bundle docs and code into the same commit so that, even if interrupted mid-way, the code and the record don't diverge.

## 4.1 Project README.md Update Rule (Per Push)

The project `README.md` is a deliverable (derived document). Do not touch it on every commit; **check whether it needs
updating per push.**

If the following changed, **include the README change in the same atomic commit.**

* Project intro / feature list (e.g., a new feature completed)
* Install / run / build instructions, dependencies
* Environment variable **names and purposes** (never write values/secrets)
* Project structure, links to key documents
* User-facing items from `ARCHITECTURE.md` (e.g., supported environments, public API summary)

The following do not touch the README.

* Internal refactors, test-only changes
* Non-critical UI fine adjustments
* Changes with no user/install/run impact

Notes:

* The README is a summary/link document, not the source of truth. Do not duplicate detailed specs in the README.
* Never put sensitive info — secrets, tokens, passwords, internal URLs — in the README.

---

# 5. QA Procedure Rules

Conduct QA during development by the following criteria.

## 5.1 Per-Feature QA

Per-feature QA is performed against the test scenarios in the relevant `features/*.md`.

Items to check:

* Whether functional requirements are met
* Normal-case behavior
* Exception-case behavior
* Input validation
* Authorization / authentication requirements (including compliance with the auth model in ARCHITECTURE.md)
* Data create / read / update / delete behavior
* Whether log / analytics events are recorded

## 5.2 Automated Tests

Write automated tests for everything feasible.

Targets: unit tests / API tests / service·business-logic tests / DB·Repository tests / screen-component tests / E2E tests

> "Test passed" counts only when the test is **actually run** and its result (run command + pass·fail summary) is recorded in HISTORY.md.
> Do not claim passing without running.

## 5.3 Regression Tests

If there is any chance of affecting existing features, check `qa/regression-checklist.md`.
For affected items, verify directly or add tests, and record results in PROGRESS.md or HISTORY.md.

## 5.4 Manual QA

Record items that are hard to automate or that a human must check directly in `qa/manual-test-cases.md`.

Targets: screen usability / design·responsive / accessibility / actual external-system integration / data validation requiring operator judgment / operational scenarios

## 5.5 Release QA

When performing deployment- or release-related work, check `qa/release-checklist.md`.

Items: all tests pass (incl. run results) / regression checklist verified / manual QA complete / environment variables·secrets check / DB migration check / log·monitoring check / rollback method confirmed / known issues documented

---

# 6. When a Multi-Agent Review Is Needed During Development

If the following arise, select the needed Agent personas and review again.

* The existing feature spec is insufficient
* The feature scope changed
* A DB structure change is needed
* The API contract changes (affects ARCHITECTURE.md)
* The UX flow changes
* A security risk is found
* Test scenarios are insufficient
* There is major impact on performance or operations

Review method:

1. Select only the needed Agent personas
2. Review risks and alternatives from each perspective
3. Reconcile conflicting opinions
4. Derive the final agreed plan
5. Reflect only the final spec + minimal review summary (participating Agents·major risks) in the feature document
6. If the common contract changes, update ARCHITECTURE.md
7. If QA changes, update the qa/ documents too
8. Record important decisions in an ADR and update adr/INDEX.md

Notes:

* Do not add long per-Agent transcripts to the feature document.
* Keep the feature document as the final feature spec.

---

# 7. Simple Git Rules

* Do not work directly on `main` / `master`.
* Use work branches named `feat/...`, `fix/...`, `docs/...`, `chore/...`.
* When a meaningful unit of work is done, commit without asking the user.
* **Bundle code changes and corresponding doc changes (features/ARCHITECTURE/PROGRESS/HISTORY, plus README if needed) into one atomic commit.**
* Use Conventional Commits for commit messages.
* After committing, push to the work branch.
* Direct push to `main` / `master` is forbidden.
* Force push and PR merge are performed only after user approval.
* Never commit files containing `.env`, secrets, certificates, private keys, or tokens.

---

# 8. Completion Criteria

Development work is complete when the following are satisfied.

* Current Phase implementation complete
* Related automated tests written
* Related automated tests **actually run and passing** (green), with run results recorded in HISTORY.md
* Related feature test scenarios satisfied
* Regression-test impact reviewed
* Whether manual QA is needed recorded
* qa/manual-test-cases.md updated if needed
* For deployment-related work, qa/release-checklist.md checked
* Code ↔ feature/ARCHITECTURE consistent (handle via authority diagnosis on mismatch)
* ARCHITECTURE.md updated when common decisions change
* docs documents updated when there is user impact
* Project README.md updated if there is user/install/run/architecture impact
* ADR written + adr/INDEX.md updated when there are important design decisions
* PLAN.md updated
* PROGRESS.md updated (includes first command for next session)
* Test-run results / QA results recorded in HISTORY.md
* ASSUMPTIONS.md updated if needed (includes conflict check)
* Per-unit commit / push complete (atomic bundle of code+docs)

---

# 9. Post-Completion Report Format

After completing work, report in the following format.

```md
# Development Result Report

## Work Done

## Changed Files

## Test Results

- Run command:
- Pass / Fail:

## QA Results

- Per-feature QA:
- Automated tests:
- Regression impact:
- Manual QA needed?:
- Release check needed?:

## Documents Updated

- ARCHITECTURE.md changed?:
- Project README.md changed?:
- ADR added?:

## Git Status

- Branch:
- Commit:
- Push:
- PR:

## Autonomous Decisions (reflected in ASSUMPTIONS)

## Remaining Work

## Suggested Next Work (= PROGRESS.md first command for next session)
```

---

# 10. Resuming a Session

If work was interrupted in a previous session, check the `first command for the next session` in `PROGRESS.md`
first and resume from there.

* Always read `ARCHITECTURE.md` and `PLAN.md` together to re-align the cross-cutting contract.
* Check `HISTORY.md` (and the archive if needed) to prevent duplicate implementation.
* Do not redo an already-completed Phase.
* If PROGRESS was provisionally updated at work start (procedure step 10), trust that record but cross-check it against the actual code state.

---

# 11. When User Confirmation Is Needed

In the following cases, stop work and ask the user.

However, user confirmation during development is minimized.
Ask only when a decision entirely different from the existing design intent is needed.

* Changing the existing MVP scope
* Changing a feature's purpose
* Changing a core UX flow
* A fundamental data-model change
* Changing authentication / authorization / security policy
* Changing how personal / sensitive data is handled
* Replacing an external API / external system
* A major change to deployment structure / operating method
* A change to the cross-cutting contract in ARCHITECTURE.md
* Possible cost / billing / legal impact
* Hard-to-reverse data deletion or destructive change
* Adding/changing a remote repository
* force push
* PR merge
* `git reset --hard`
