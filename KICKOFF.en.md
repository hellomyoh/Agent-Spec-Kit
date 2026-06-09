# KICKOFF.md

> English version of the KICKOFF initialization prompt. File references use canonical names.

Using the `AGENTINIT.md` file, perform the project initial setup.

The goal of this stage is **not** actual development, but to generate the project operations documents,
the cross-cutting contract document, feature specifications, user documentation, QA documents, and the
development plan so that development can begin.

---

# 1. Files to Create

Create the following files and folders.

```text
/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── ARCHITECTURE.md
├── PLAN.md
├── PROGRESS.md
├── HISTORY.md
├── ASSUMPTIONS.md
├── features/
│   ├── README.md
│   └── *.md
├── docs/
│   ├── README.md
│   └── *.md
├── qa/
│   ├── README.md
│   ├── regression-checklist.md
│   ├── manual-test-cases.md
│   └── release-checklist.md
└── adr/
    ├── INDEX.md
    └── *.md
```

* The top-level `README.md` is the **project README** (a deliverable): what this project is and how to install/run it.
* `ARCHITECTURE.md` collects the cross-cutting contract applied in common across features; **always create it.**
* `adr/INDEX.md` is the ADR index; **always create it** (it may be empty initially).
* `adr/*.md` are written when there is a decision matching an ADR trigger (Section 16).

---

# 2. Requirement Clarification Rules for the Initial Setup

In the KICKOFF stage, after analyzing the user requirements in `AGENTINIT.md`, first confirm whether they are
sufficient to produce the initial project documents and feature specifications.

In this stage, if requirements are ambiguous, the Agent must not guess arbitrarily; it must ask the user to
clarify the project direction.

## 2.1 When to Ask the User

If the following are blank or ambiguous, ask the user before continuing initialization.

* The project purpose is unclear
* The target users are unclear
* The features that must be in the MVP are unclear
* The core user scenarios are unclear
* The purpose of external API / external system integration is unclear
* The data to store or the data to analyze is unclear
* Sensitive info, personal data, or security requirements are unclear
* Authentication / authorization / admin-feature presence is unclear
* Test / QA criteria are unclear
* The deployment environment or operational constraints are important but unspecified
* The feature scope is too broad to separate MVP from lower priority

## 2.2 When You May Proceed with Defaults Without Asking

For the following, pick a reasonable default without asking, record it in `ASSUMPTIONS.md`, and proceed.

* File / folder naming
* Document fine structure
* Default code style
* Common testing tools
* Common local development environment setup
* Log format
* Non-critical UI presentation
* Implementation details of lower-priority features
* Fine defaults in `ARCHITECTURE.md` (when Section 10 of AGENTINIT is empty)

> However, among cross-cutting decisions recorded in `ARCHITECTURE.md`, the **broad direction of the auth model,
> personal data handling, and data model** should be asked if they fall under 2.1. Only fine notational rules
> proceed with defaults.

## 2.3 How to Ask

Don't ask too much at once; bundle only the questions truly needed to proceed, up to 5.

Format:

```md
# Confirmation needed for project initialization

After analyzing AGENTINIT.md, I need to confirm the following before creating the initial feature specs and dev plan.

1. <question>
2. <question>
3. <question>

Once you answer, I'll reflect it and continue the AGENTINIT.md-based project initialization.
```

## 2.4 AI Delegation Marker Handling Rules

When the user writes `[AI delegated]` (aliases `[leave to AI]`, `[unknown]`) on an item, interpret it as
"the user has delegated this decision to the Agent." For delegated items, the 2.1 "must ask" rule is adjusted
as follows.

* **Non-critical delegated items** (the 2.2 kind):
  Pick a reasonable default, proceed, and record it in `ASSUMPTIONS.md`. Do not ask.

* **Critical delegated items** (the 2.1 kind: MVP scope, data model, auth/authz, personal data, external integration, etc.):
  Do not stop initialization. Instead:
  1. Adopt **the most conservative, easily reversible choice** as a provisional decision.
     (e.g., personal data → avoid collecting sensitive data / MVP → smallest reasonable scope / auth → a standard, safe default)
  2. Record the decision and rationale in `ASSUMPTIONS.md` with `status: active`.
  3. If it is a cross-cutting contract, reflect it in `ARCHITECTURE.md` too; if important, leave an ADR.
  4. Collect it under **"Items Decided by AI Delegation (Review Recommended)"** in the report so the user can review/adjust.

* **Non-delegable exception:**
  If both the project purpose and core features are delegated/blank, do not accept the delegation; ask using the
  2.3 format. "What the project is" is not delegable.

* **Cost/legal/destructive exception:**
  Items with cost, billing, legal impact, or hard-to-reverse effects are never decided silently even when delegated.
  Pick a conservative, no-cost/no-risk default, then explicitly request confirmation in the report.

* **The `[unknown]` case:**
  If a critical item is marked `[unknown]` and the choice depends heavily on user judgment, you may, instead of
  adopting a provisional decision, ask using the 2.3 format **with concrete options and a recommendation**.
  (More appropriate when the signal is "I need help" rather than "I delegate.")

---

# 3. Initialization Work Order

Because initialization is a long sequence, **update the initialization progress in `PROGRESS.md` after each step.**
If initialization is interrupted, the next session reads `PROGRESS.md` and resumes from where it stopped.

1. Analyze AGENTINIT.md
2. Confirm whether the essential requirements for initialization are met
3. Identify ambiguous or missing core requirements
4. If items need user confirmation, ask and pause initialization
5. Record items you can proceed on with defaults (no question) in `ASSUMPTIONS.md`
6. Organize project purpose and scope
7. **Organize the cross-cutting contract → draft `ARCHITECTURE.md`**
8. Separate MVP scope from lower-priority scope
9. Decompose into feature units (granularity guide: see 6.0)
10. Perform Multi-Agent review per feature
11. Consolidate review results into the final feature specs
12. Write per-feature test scenarios
13. Write all QA documents
14. Write user-facing docs documents
15. If there are important design decisions, write ADRs and update `adr/INDEX.md`
16. Finalize `ARCHITECTURE.md` based on ADR/feature-spec results
17. **Draft the project `README.md`** (based on ARCHITECTURE/features/PLAN)
18. Write the Agent work instructions AGENTS.md
19. Write PLAN.md
20. Write PROGRESS.md
21. Write HISTORY.md
22. Write ASSUMPTIONS.md
23. Write CLAUDE.md
24. Report initialization completion (Section 18 format)

---

# 4. Multi-Agent Feature-Spec Authoring Method

Feature documents are not written from a single perspective.

When writing each feature spec, assemble the needed Agent personas, review requirements, risks, and design
considerations from each Agent's perspective, then consolidate the results into one final feature spec.

Key principles:

* A feature document is not a transcript of each Agent.
* A feature document is the final feature spec for implementers to reference.
* Each Agent's input is reflected in the feature requirements, data design, API design, UI/UX design, security
  requirements, logging requirements, and test scenarios.
* Don't force unrelated Agents to participate.

## 4.1 Auditability of the Review Process (Important)

Keep the principle of "not listing long per-Agent transcripts," but **leave the minimum trace needed to verify
that a review actually happened.**

* For non-trivial features (those affecting data model / API contract / auth / external integration / performance),
  leave in feature item 4 a **list of participating Agent personas and a 1–3 line summary of the major risks/tradeoffs
  found during review.**
* Important conflicts or decisions needing long-term tracking are split into `adr/*.md`, and referenced from feature
  item 14.
* Trivial features like simple CRUD or static screens may omit the summary and be marked "Simple feature — no further review needed."

This summary is not for reproducing a transcript; it is a minimal audit trace to prevent "skipping the review and
writing only a plausible conclusion."

---

# 5. Available Agent Personas

Pick only the Agents needed for the feature's nature.

* Product Manager Agent — reviews requirements, user value, scope, priority, completion criteria
* Research Agent — reviews similar cases, external APIs, tech choices, best practices
* UX/UI Designer Agent — reviews user flow, screen structure, usability, accessibility, error states
* System Architect Agent — reviews system structure, module separation, scalability, maintainability
* Database Engineer Agent — reviews data model, tables, indexes, migrations, integrity
* Backend Engineer Agent — reviews APIs, business logic, external integration, error handling, testability
* Frontend Engineer Agent — reviews screen implementation, state management, component structure, API integration
* Security Agent — reviews auth, authz, personal data, secrets, input validation, vulnerabilities
* QA Agent — reviews test strategy, normal/exception scenarios, regression scope, release acceptance criteria
* Data Analyst Agent — reviews logs, KPIs, analytics events, reporting requirements

---

# 6. Feature Document Authoring Rules

Write each feature document in `/features/*.md`.

A feature document is the final agreed implementation spec.

## 6.0 Feature Decomposition Granularity Guide

* Write one feature document as **one user-value unit.**
* Recommend **3–7** MVP feature documents; if it exceeds 7, reconsider splitting to lower priority or merging.
* If a feature is so large that the spec would become shallow, split it into sub-features.
* Rules applied in common across features (data model, naming, common error format, etc.) should not be duplicated
  in feature documents; **reference `ARCHITECTURE.md`.**

## 6.1 Feature Document Structure

```md
# Feature: <feature name>

## 1. Purpose

## 2. Scope

### In Scope

### Out of Scope

## 3. User Scenarios

## 4. Final Agreed Plan

Summarize the implementation direction confirmed through Multi-Agent review.
Do not list per-Agent opinions verbatim; record only the final decided direction.

### Review Summary (for audit)

- Participating Agents:
- Major risks / tradeoffs (1–3 lines):
- (If trivial, "Simple feature — no further review needed")

## 5. Functional Requirements

## 6. Non-Functional Requirements

## 7. Data Design

Write `N/A` if not applicable.
Reference ARCHITECTURE.md for common data rules; write only what is unique to this feature.

## 8. API Design

Write `N/A` if not applicable.
Reference ARCHITECTURE.md for the common API contract (error format, pagination, etc.).

## 9. UI/UX Design

Write `N/A` if not applicable.

## 10. Security Requirements

## 11. Logging / Analytics Requirements

## 12. Test Scenarios

### Automated Tests

### Manual QA

### Exception Cases

### Regression Test Impact

## 13. Completion Criteria

(Completion criteria must include "the related automated tests were actually run and passed (green)".)

## 14. Referenced ADRs

Write `None` if none.

## 15. Undecided Items

### Needs User Confirmation

### Items Proceeded with Defaults

### Items for Lower-Priority Review
```

---

# 7. ARCHITECTURE.md Authoring Rules

`ARCHITECTURE.md` is the **cross-cutting contract** document applied in common across features.

This document is always loaded in every development session.
Feature documents reference it and do not duplicate the same content.

Contents:

* System overview / module structure
* Confirmed tech stack
* Common data model rules (ID strategy, timestamps, soft delete, integrity rules, etc.)
* Naming conventions (DB column / variable / file / API path casing)
* API contract (protocol, common error response format, pagination, versioning strategy)
* Authentication / session model (token approach, storage location, expiry/refresh, authorization scheme)
* Common log / monitoring format
* Environment / deployment structure overview
* Change rule: changing an item here requires writing an ADR and updating INDEX

> When the cross-cutting contract changes, update `ARCHITECTURE.md` and the affected feature documents together,
> and leave an ADR for important changes.

## 7.1 README.md (Project) Authoring Rules

The top-level `README.md` is **a deliverable that introduces the project itself.**

At initialization, draft it based on `ARCHITECTURE.md` / `features/` / `PLAN.md`.

Contents:

* Project name / one-line description
* Summary of main features (based on features)
* Tech stack (based on ARCHITECTURE)
* Prerequisites (runtime, versions, etc.)
* Install / run / build instructions
* Environment variable **names and purposes** (never write values/secrets)
* How to run tests
* Project structure overview
* Links to key documents (docs/, ARCHITECTURE.md, PLAN.md, etc.)

Rules:

* The README is not the source of truth; it is a **derived deliverable.** Keep detailed specs in `ARCHITECTURE.md`/`features/`; the README summarizes and links.
* The README is not an always-loaded reference document. During development, only check whether it needs updating per push (see DEVELOPINIT.md for dev rules).
* Never put sensitive info — secrets, tokens, passwords, internal URLs — in the README.

---

# 8. QA Document Authoring Rules

At initialization, create the `qa/` folder and write the following documents.

## qa/README.md

The QA operating-method document.

Contents:

* QA principles
* Distinction between automated tests and manual QA
* Relationship between per-feature tests and regression tests
* Where QA results are recorded (HISTORY.md / PROGRESS.md)
* Definition of "test passed": only counts as passed if the test was actually run and the result (output/summary) is recorded
* Pre-release QA procedure

## qa/regression-checklist.md

A regression checklist of things to repeatedly verify across the whole service.

Contents:

* Core user flows
* Auth / authz flows
* Correct behavior of major APIs
* Correct behavior of major screens
* Data create / read / update / delete flows
* Behavior on external-integration failure
* Items to verify that existing features didn't break

## qa/manual-test-cases.md

A list of tests that are hard to automate or that a human must check directly.

Contents:

* Screen usability
* Design / responsive
* Accessibility
* Admin screens
* Data validation requiring operator judgment
* Verifying external-system integration results

## qa/release-checklist.md

The final pre-deployment acceptance checklist.

Contents:

* Whether all automated tests pass (include run-result capture)
* Whether major regression tests were checked
* Whether manual QA is complete
* Environment variables / secrets check
* DB migration check
* Log / monitoring check
* Rollback method confirmed
* Known issues documented

---

# 9. AGENTS.md Authoring Rules

AGENTS.md is the work-instruction document the Agent references on every run.

Must include:

* Project overview
* Document priority
* Work-start procedure
* **Always-load document list** (AGENTS.md, ARCHITECTURE.md, PLAN.md, PROGRESS.md)
* Feature-document reference rules (selective load)
* Multi-Agent review rules
* QA procedure rules
* Criteria for user confirmation during development
* PLAN / PROGRESS / HISTORY / ASSUMPTIONS management rules
* ADR authoring criteria and INDEX update rules
* Git workflow rules
* Spec-check-before-implementation rule
* Test rules
* Project README.md update rule (update per push when there is user/install/run/architecture impact)
* Work-completion criteria

AGENTS.md must include the following principle.

```text
The Agent reads AGENTS.md first at work start,
always reads ARCHITECTURE.md, PLAN.md, and PROGRESS.md together,
then selectively reads only the feature documents needed for the current work.
When selecting feature documents, check adr/INDEX.md for related ADRs.
```

It must also include this principle.

```text
Decisions applied in common across features (data model, naming, API contract, auth model)
are recorded in ARCHITECTURE.md, not in feature documents.
Feature documents are written from Multi-Agent review results, but do not list per-Agent transcripts;
keep only a minimal review summary (participating Agents and major risks).
Important design decisions are split into ADRs, and adr/INDEX.md is updated.
```

For code-spec mismatch, it must include this principle.

```text
When code and spec (feature/ARCHITECTURE) differ, do not immediately fix one side.
First diagnose which side is the authority.
- If the spec accurately captures the intent and the code is wrong, fix the code.
- If the spec is confirmed to diverge from reality/intent, update the spec first and align the code.
Do not retroactively justify an implementation mistake as if it were the spec.
```

For QA, it must include this principle.

```text
QA is performed against the feature documents' test scenarios and the qa/ folder checklists.
Per-feature tests are recorded in features/*.md;
overall regression tests and release acceptance are managed in the qa/ folder.
"Test passed" counts only when the test was actually run and the result was recorded in HISTORY.md.
Before completing development, check related automated tests, whether manual QA is needed, and regression impact.
```

For user-confirmation criteria during development, it must include this principle.

```text
During development, do not ask the user for every minor implementation decision.
Items resolvable within the design intent of the existing AGENTS.md, ARCHITECTURE.md, PLAN.md, PROGRESS.md,
features/*.md, qa/*.md are decided autonomously by the Agent and recorded in ASSUMPTIONS.md.
Ask the user only when a decision is needed that is entirely different from the existing design intent —
MVP scope, user experience, data model, auth/authz, security/personal data, external integration, deployment
structure, cost/legal impact, etc.
```

For ASSUMPTIONS management, it must include this principle.

```text
Before recording a new assumption, check whether it conflicts with existing entries in ASSUMPTIONS.md and with ARCHITECTURE.md.
If it conflicts, do not overwrite arbitrarily; record the conflict and the resolution direction together.
When a user answer or an ADR confirms/retires an assumption, update that assumption's status.
```

---

# 10. Simple Git Rules to Include in AGENTS.md

Include the Git rules below in AGENTS.md.

```md
## Git Workflow Rules

- Check the current branch at work start.
- Do not work directly on `main` or `master`.
- When needed, create a work branch named `feat/...`, `fix/...`, `docs/...`, or `chore/...`.
- When a meaningful unit of work is done, commit without asking the user.
- Bundle code changes and their corresponding doc changes (features/ARCHITECTURE/PROGRESS/HISTORY, etc.) into one atomic commit.
- Use Conventional Commits for commit messages.
- After committing, push to the work branch.
- Direct push to `main` / `master` is forbidden.
- Force push only when the user explicitly requests it.
- Never commit files containing `.env`, secrets, certificates, private keys, or tokens.
- PRs may be created when needed, but merge is performed after user approval.
- Adding/changing remotes, `git reset --hard`, and adding large files are done after user confirmation.
```

---

# 11. CLAUDE.md Authoring Rules

CLAUDE.md is the file Claude Code auto-loads every session.
A single-line reference wastes the auto-load slot, so **include the core always-on rules as well.**

Write the following in CLAUDE.md.

```md
# CLAUDE.md

For detailed work instructions, follow AGENTS.md.

## Core Always-On Rules (summary)

- In every session, read AGENTS.md, ARCHITECTURE.md, PLAN.md, PROGRESS.md first.
- Read feature/QA docs selectively, only what the current work needs. Check related ADRs via adr/INDEX.md.
- Record and follow common decisions (data model/naming/API contract/auth) in ARCHITECTURE.md.
- Do not implement by guessing without a spec. For code-spec mismatch, diagnose authority first, then handle.
- Actually run tests and record results in HISTORY.md. Do not claim passing without running.
- Commit/push code+docs atomically per meaningful unit. No direct push to main/master.
- On push, if there is user/install/run/architecture impact, update the project README.md in the same commit.
- Record autonomous decisions in ASSUMPTIONS.md, after first checking for conflicts with existing assumptions/ARCHITECTURE.
- Ask the user only when a decision entirely different from the design intent is needed.
```

---

# 12. PLAN.md Authoring Rules

Write the project development Phases in PLAN.md.

Each Phase must include:

* Phase name
* Purpose
* Deliverables
* Completion criteria (include related automated tests actually run/passed)
* QA completion criteria
* Dependencies
* Related feature documents
* Related ARCHITECTURE items / ADRs
* Status

---

# 13. PROGRESS.md Authoring Rules

Record the current progress in PROGRESS.md.

Items:

* Current Phase
* (If initializing) initialization progress step
* Completed work
* In-progress work
* Remaining work
* QA status
* **First command for the next session** (most important; look at this first when a session starts)

---

# 14. HISTORY.md Authoring Rules

Record the Agent's work history chronologically in HISTORY.md.

Items:

* Date
* Work done
* Changed files
* Test results (run command / pass·fail summary)
* QA results
* Git commit
* Notes

Rotation / summary rule:

```text
When HISTORY.md grows long (e.g., 30+ entries or a certain size), compress and summarize old entries
into HISTORY-archive.md (or similar), keeping only recent history and a link to the summary in HISTORY.md.
Perform this rotation without losing information needed to prevent duplicate implementation (completed Phases/features).
```

---

# 15. ASSUMPTIONS.md Authoring Rules

Record in ASSUMPTIONS.md what the Agent decided without asking the user.

Format:

```text
YYYY-MM-DD | area | decision | reason | status(active/confirmed/superseded)
```

Rules:

* Before adding a new assumption, check for conflicts with existing assumptions and `ARCHITECTURE.md`.
* If it conflicts, do not overwrite arbitrarily; record the conflict and the resolution direction together.
* When a user answer or an ADR confirms/retires an assumption, update its `status`.

---

# 16. ADR Authoring Rules

Decisions matching an ADR trigger (below) must be written in `/adr/*.md` **as a requirement, not at discretion**,
and an entry added to `adr/INDEX.md`.

ADR targets (required):

* Architecture choice
* Authentication method choice
* A decision with major impact on DB structure
* External API choice
* State-management approach choice
* Deployment structure choice
* A decision with major impact on test strategy
* A decision affecting long-term maintainability
* A decision that changes the cross-cutting contract in `ARCHITECTURE.md`

ADR format:

```md
# ADR-000: <decision title>

## Status

Proposed / Accepted / Deprecated / Superseded

## Context

## Options

## Decision

## Rationale

## Consequences

## Related feature / ARCHITECTURE items
```

adr/INDEX.md format:

```md
# ADR Index

| No. | Title | Status | Area | Related feature |
|---|---|---|---|---|
| ADR-001 | ... | Accepted | Auth | feature-auth.md |
```

> Keep INDEX always up to date so selective-loading sessions can cheaply discover relevant decisions.

---

# 17. Completion Criteria

Initialization is complete only when all of the following are satisfied.

* AGENTS.md created
* CLAUDE.md created (includes core rules)
* ARCHITECTURE.md created
* Project README.md created (no sensitive info)
* PLAN.md created
* PROGRESS.md created (includes first command for next session)
* HISTORY.md created
* ASSUMPTIONS.md created
* features/README.md created
* Per-feature documents created (follow the granularity guide)
* docs/README.md created
* User documentation created
* qa/README.md created
* qa/regression-checklist.md created
* qa/manual-test-cases.md created
* qa/release-checklist.md created
* adr/INDEX.md created
* If needed, ADRs created and INDEX updated
* Each feature document is in final-agreed-spec form and includes the review summary
* Each feature document has test scenarios and completion criteria including "tests actually pass"
* Common decisions are organized in ARCHITECTURE.md, not in feature documents
* A Phase plan that lets development begin
* The first development command is written in PROGRESS.md

---

# 18. Output Format

After completing initialization, report in the following format.

```md
# Project Initialization Result

## Files Created

## Cross-Cutting Contract (ARCHITECTURE.md) Summary

## Feature Spec List

## User Documentation List

## QA Document List

## ADR List (INDEX)

## Development Phase Summary

## Items Decided by AI Delegation (Review Recommended)

(Collect the provisional decisions and rationale the Agent adopted for critical items the user delegated via
`[AI delegated]`, etc. For cost/legal/destructive items, explicitly request confirmation here.)

## Items Needing User Confirmation

## Next Steps
```
