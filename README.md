# README.md — Usage Guide for Agent-Based Project Initialization / Development Prompts

**English** | [한국어](README.ko.md)

> File references use the canonical names (`AGENTINIT.md`, `KICKOFF.md`, `DEVELOPINIT.md`).

This document is the **framework (template) usage guide** explaining how to use `AGENTINIT.md`, `KICKOFF.md`,
and `DEVELOPINIT.md` with Codex, Claude Code, Cursor Agent, etc. This `README.md` is the README of the agentinit
template repository and is a human-facing reference.

> **How to use it (clone then copy):**
> Clone this template repository, then **copy only the three files `AGENTINIT.md` / `KICKOFF.md` / `DEVELOPINIT.md`
> into your own project repository.**
> Leave this `README.md` (the guide) in the template repository; do not copy it into your project.
> Do not push into the agentinit template repository — you work in your own project repository.
> This way, the **project `README.md`** generated during initialization in your project does not collide with this
> guide (they live in different repositories).

> **Important:** `AGENTINIT.md` must contain your project overview, rough requirements, core features, and constraints.
> The Agent generates the feature specs, the cross-cutting contract document, and the development plan from this content.
>
> If, in the initial setup stage, the project purpose, target users, MVP features, data, external integrations,
> auth/authz, QA criteria, etc. are ambiguous, the Agent must not guess arbitrarily; it must ask the user to clarify.

---

## 0. What's Strengthened in This Version (summary)

To remedy weaknesses in the prior structure, the following were added/changed.

| Strengthening | Detail |
|---|---|
| New `ARCHITECTURE.md` | Collects the **contract applied in common across features** — data model, naming, API contract, auth model — in one place, always loaded in every dev session → cross-feature consistency |
| New `adr/INDEX.md` | An ADR index. Selective-loading sessions can cheaply discover relevant design decisions |
| ADR made mandatory | For specified triggers (architecture/auth/DB/external API/deployment, etc.), writing an ADR is **required**, not discretionary |
| Revised code-spec mismatch rule | Not "always fix the spec" but **first diagnose which side is authority** → prevents retroactive justification of implementation mistakes |
| Provisional PROGRESS record | Write the `first command for next session` **at work start** → continuity preserved even if interrupted |
| Atomic commit | Bundle code changes and corresponding doc changes into **one commit** |
| HISTORY rotation | Compress/archive when history grows long → eases context burden |
| Feature granularity guide | Provides a feature-unit standard and a recommended MVP feature count (3–7) |
| Assumption conflict check | Check conflicts with existing assumptions/ARCHITECTURE before recording a new one |
| Strengthened CLAUDE.md | Carries **core always-on rules** instead of a single-line reference |
| Test evidence | "Test passed" counts only on **actual run + result recorded** |
| Multi-agent audit trace | Leaves a **1–3 line summary** of participating Agents·major risks in the feature document to prevent skipped review |
| AI delegation marker | If the user writes `[AI delegated]` on an unknown item: non-critical proceeds with a default, critical gets a conservative provisional decision + review recommendation in the report |
| Guide/project README separation | Keep the guide `README.md` in the template repo and copy only the 3 prompt files into your project → no collision with the project's generated `README.md` (clone-then-copy workflow) |

---

## 1. Basic File Layout

The agentinit template repository looks like this.

```text
agentinit/  (template repo — what you clone)
├── README.md         # this guide (English). Not copied into your project
├── README.ko.md      # Korean translation of this guide. Not copied into your project
├── AGENTINIT.md      # the project-requirements input document the user writes
├── KICKOFF.md        # the initialization prompt
└── DEVELOPINIT.md    # the development prompt
```

After cloning, **copy only the three files `AGENTINIT.md` / `KICKOFF.md` / `DEVELOPINIT.md` into your own project
repository.** (Do not copy the `README.md` guide.)

```text
my-project/  (your project repo — where you work)
├── AGENTINIT.md      # copied from the template
├── KICKOFF.md        # copied from the template
└── DEVELOPINIT.md    # copied from the template
```

Before running initialization, the user must first fill in the project requirements in `AGENTINIT.md`.

To the extent possible, write the following.

- Project purpose
- Target users
- Core features (granularity guide: one feature = one user value, 3–7 MVP recommended)
- Features that must be in the MVP
- Lower-priority features
- External APIs / external systems
- Data to store or analyze
- Screen / UX requirements
- Auth / authz requirements
- **Cross-cutting (architecture) baseline** (common data model rules, naming, API contract style, auth model)
- Test / QA requirements
- Operations / deployment constraints

The roles of each file are as follows.

| File | Role |
|---|---|
| `README.md` (template) | The framework usage guide (this document). Kept in the template repo; not copied into your project |
| `AGENTINIT.md` | The project-requirements input document the user writes (copy into your project) |
| `KICKOFF.md` | The project-initialization prompt (copy into your project) |
| `DEVELOPINIT.md` | The prompt for actual development after initialization (copy into your project) |

> Note: the **project `README.md`** generated after initialization in your project shares the name but is a different
> document in a different repository from this guide.
> The guide covers "how to drive the agent"; the project README covers "what this project is and how to run it."

---

## 2. One-Time: Project Initialization Prompt

After completing `AGENTINIT.md`, enter the following prompt into the Agent.

```text
Read AGENTINIT.md and KICKOFF.md, and perform the project initial setup per the instructions in KICKOFF.md.

AGENTINIT.md is the project requirements written by the user.
KICKOFF.md is the initialization work instructions.

Be sure to do the following.

1. Analyze AGENTINIT.md.
2. Confirm whether the core requirements needed for initialization are sufficient.
3. If the project purpose, target users, MVP features, user scenarios, data, external integrations, auth/authz, or QA criteria are ambiguous, ask the user before proceeding with initialization.
4. When asking is needed, write only the core questions, up to 5 at a time.
5. Organize the contract applied in common across features (data model/naming/API/auth) and generate ARCHITECTURE.md.
6. Generate the project structure and documents per the KICKOFF.md procedure.
7. Generate the features/, docs/, qa/, adr/ documents. Include adr/INDEX.md.
8. Generate AGENTS.md, ARCHITECTURE.md, PLAN.md, PROGRESS.md, HISTORY.md, ASSUMPTIONS.md, CLAUDE.md.
8-1. Generate the project README.md (intro·install·run·structure·doc links). It must not contain sensitive info.
9. Write feature documents from Multi-Agent review results — not per-Agent transcripts but final agreed feature specs — and summarize participating Agents and major risks in 1–3 lines.
10. Split QA into per-feature test scenarios and the qa/ folder regression/manual/release checklists. Include the criterion that "test passed" is recognized only on actual run.
11. When initialization is done, report the created file list, ARCHITECTURE summary, feature spec list, QA document list, ADR list, development Phase summary, and the next development start command.
```

This prompt is **for project initial setup only.**
In this stage, it does not start actual implementation; it generates the documents and plan needed to begin development.

> Initialization is a long sequence and may be interrupted. The Agent updates the initialization progress in `PROGRESS.md`
> after each step, so if interrupted you can resume with the same prompt.

---

## 3. When Requirements Are Ambiguous in the Initialization Stage

Requirement quality matters in the initialization stage.
If the following are ambiguous, the Agent must not guess arbitrarily; it must ask the user.

- Project purpose / target users / MVP core features / core user scenarios
- Purpose of external API / external system integration
- Data to store or analyze
- Sensitive info / personal data / security requirements
- Auth / authz / admin features
- The broad direction of the data model·auth model (ARCHITECTURE baseline)
- Test / QA criteria
- Deployment environment / operational constraints
- Distinction between MVP and lower-priority features

Conversely, fine defaults such as file names, folder structure, code style, common testing tools, local dev environment
setup, and **fine naming notation** proceed without asking, recorded in `ASSUMPTIONS.md` (or `ARCHITECTURE.md`).

Example question:

```text
Confirmation needed for project initialization.

After analyzing AGENTINIT.md, I need to confirm the following before creating the initial feature specs and dev plan.

1. What are the 3 features that must be in this project's MVP?
2. Who are the main users — general user, admin, or operator?
3. For external API integration, what is the authentication method and call frequency?

Once you answer, I'll reflect it and continue initialization.
```

### 3.1 Delegating Unknown Items to the AI (`[AI delegated]`)

For items you are unsure about or cannot decide, instead of leaving them blank, write `[AI delegated]`
(aliases `[leave to AI]`, `[unknown]`). The Agent handles them by risk level.

- **Non-critical items** (naming, code style, non-critical UI, log format, etc.): proceed with a reasonable default and record in `ASSUMPTIONS.md`. No question.
- **Critical items** (MVP scope, data model, auth/authz, personal data, external integration, etc.): do not stop initialization; provisionally adopt **the most conservative, easily reversible choice**, record it in `ASSUMPTIONS.md`, and collect it under **"Items Decided by AI Delegation (Review Recommended)"** in the report. You can review/adjust later.

However, two things cannot be delegated. **If both the project purpose and core features are blank or delegated**
(there is no "what this project is"), the Agent does not accept the delegation and asks. Also, items with
**cost·billing·legal impact·hard-to-reverse effects** are never decided silently even when delegated; the Agent picks a
conservative default and requests confirmation.

The same applies in the development stage. If you delegate with "just decide this" in a prompt, the Agent's autonomy for
that item broadens, but critical items are decided conservatively and left in `ASSUMPTIONS.md` and the completion report.

---

## 4. Documents Generated After Initialization

After initialization, the following structure is typically generated.

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

The roles of each document are as follows.

| File / Folder | Role |
|---|---|
| `README.md` | The **project README** (deliverable). Project intro·install·run·structure·doc links. Updated per push |
| `AGENTS.md` | The work instructions the Agent references on every run |
| `CLAUDE.md` | Claude Code auto-load file. References AGENTS.md + core always-on rules |
| `ARCHITECTURE.md` | The **cross-cutting contract** (data model/naming/API/auth). Always loaded in every dev session |
| `PLAN.md` | The full development Phases and completion criteria |
| `PROGRESS.md` | Current progress and the first command for the next session |
| `HISTORY.md` | Work history (archived when long) |
| `ASSUMPTIONS.md` | What the Agent decided autonomously (incl. status/conflict management) |
| `features/*.md` | Per-feature final feature specs (incl. review summary) |
| `docs/*.md` | User / operator documentation |
| `qa/*.md` | QA operations, regression tests, manual QA, release checklist |
| `adr/INDEX.md` | ADR index |
| `adr/*.md` | Records of important design decisions |

---

## 5. Development Start Prompt

When starting actual development after initialization, enter the following prompt.

```text
Read AGENTS.md and DEVELOPINIT.md, and start actual development based on the current project documents.

Proceed strictly in this order.

1. Read AGENTS.md.
2. Read ARCHITECTURE.md. (cross-cutting contract — always loaded)
3. Read PLAN.md.
4. Read PROGRESS.md and check the "first command for the next session".
5. Check HISTORY.md as needed to detect duplicate implementation.
6. Check features/README.md and adr/INDEX.md.
7. Selectively read only the feature documents and related ADRs for the current Phase.
8. Read qa/README.md and selectively check only the QA documents the current work needs.
9. Implement the current Phase per the DEVELOPINIT.md procedure.

Cautions:

- Do not re-initialize the project based on AGENTINIT.md.
- Always load ARCHITECTURE.md, PLAN.md, PROGRESS.md. Read only the feature/QA docs the current Phase needs.
- Follow ARCHITECTURE.md for common decisions (data model/naming/API/auth).
- Do not implement by guessing without a spec.
- When code and spec differ, diagnose which side is authority first, then handle. Do not disguise an implementation mistake as the spec.
- Actually run tests and record results in HISTORY.md. Do not claim passing without running.
- At work start, provisionally record the progress and the first command for the next session in PROGRESS.md.
- When a meaningful unit of work is done, bundle code+docs into one commit and commit/push.
- Direct push to main/master is forbidden.
- After completing work, update ARCHITECTURE.md (if changed), PLAN.md, PROGRESS.md, HISTORY.md.
- On push, if there is user/install/run/architecture impact, update the project README.md in the same commit.
```

This prompt is **for starting actual development.**

---

## 6. Criteria for Asking the User During Development

In the development stage, the Agent does not ask the user for every minor implementation decision.
It proceeds autonomously based on the already-created `AGENTS.md`, `ARCHITECTURE.md`, `PLAN.md`, `PROGRESS.md`,
`features/*.md`, `qa/*.md`.

Asking the user is limited to **when a decision entirely different from the existing design intent is needed.**

- Changing the existing MVP scope
- Changing a feature in a direction different from its purpose
- A major change to a core UX flow
- A fundamental data-model change
- Changing auth / authz / security policy
- Changing how personal / sensitive data is handled
- Replacing an external API / external-system integration approach
- A major change to deployment structure / operating method
- **A change to the cross-cutting contract in ARCHITECTURE.md**
- Possible cost / billing / legal impact
- Hard-to-reverse data deletion / destructive change

Otherwise — internal function names, file placement, test data, mock data, non-critical UI layout, small refactors,
QA checklist improvements, etc. — proceed without asking and record in `ASSUMPTIONS.md` if needed (incl. conflict check
with existing assumptions).

---

## 7. Prompt to Resume Work the Next Day or After a Session Break

```text
Read AGENTS.md and DEVELOPINIT.md, and resume the previous work based on the "first command for the next session" in PROGRESS.md.

Read ARCHITECTURE.md and PLAN.md together to re-align the cross-cutting contract.
Do not redo already-completed work. Check HISTORY.md (and the archive) to prevent duplicate implementation.
Read only the feature documents and related ADRs for the current Phase, and continue development.
Check only the QA documents the current work needs.

At work start, provisionally update the progress in PROGRESS.md,
and when work is done, update PLAN.md, PROGRESS.md, HISTORY.md, ASSUMPTIONS.md, then bundle code+docs and commit/push.
```

---

## 8. How QA Is Run

QA is managed in two layers.

```text
features/*.md
→ per-feature test scenarios

qa/*.md
→ overall regression tests / manual QA / release checklist
```

During development, check the following.

1. Check the current feature document's test scenarios
2. Write automated tests
3. **Actually run** automated tests (capture run command·results)
4. Fix failing tests
5. Review regression-test impact
6. Decide whether manual QA is needed
7. Update `qa/manual-test-cases.md` if needed
8. Record test-run results / QA results in `HISTORY.md` and `PROGRESS.md`

> "Test passed" counts only when the test is actually run and the result is recorded. If deployment/release work is involved, check `qa/release-checklist.md`.

### 8.1 Project README.md Update (per push)

The project `README.md` is a deliverable that covers "what this project is and how to install/run it" (separate from the
the guide).

- **Generation**: at initialization, KICKOFF drafts it from `ARCHITECTURE.md` / `features/` / `PLAN.md`.
- **When to update**: not on every commit, but **check whether it needs updating per push.** If the following changed, include the README change in the same atomic commit.
  - Project intro / feature list (e.g., a new feature completed)
  - Install / run / build instructions, dependencies, environment variable **names** (never write values/secrets)
  - Project structure, links to key documents (docs/, etc.)
  - User-facing items from `ARCHITECTURE.md` (e.g., supported environments)
- **No update needed**: internal refactors, test-only changes, non-critical UI fine adjustments — anything with no user/install/run impact does not touch the README.
- The README is a **derived deliverable**, not an always-loaded reference. The source of truth is `ARCHITECTURE.md`/`features/`; the README summarizes and links to them.

---

## 9. Consistency Mechanisms (the core of this version)

To keep the development direction steady as features and sessions grow, the following are used.

```text
ARCHITECTURE.md       → All cross-feature contracts in one place. Always loaded every session.
adr/INDEX.md          → A list of important decisions. Selective-loading sessions discover relevant ones cheaply.
PROGRESS (provisional) → Even if a session breaks, the next session picks up exactly.
Atomic commit          → Code and docs always remain in the same state.
Authority-diagnosis rule → Don't arbitrarily erase code-spec mismatch. Prevents drift.
HISTORY rotation       → Manages context burden without losing history.
```

Core principle: **common decisions in ARCHITECTURE.md, important decisions in ADRs, progress in PROGRESS, history in HISTORY.**
Feature documents hold only that feature's own spec.

---

## 10. Usage Flow Summary

```text
1. Write AGENTINIT.md (incl. cross-cutting baseline)
2. Run the initialization prompt with KICKOFF.md
3. If requirements are ambiguous, the Agent asks the user
4. Generate AGENTS / ARCHITECTURE / features / docs / qa / adr / PLAN / PROGRESS, etc.
5. Run the development prompt with DEVELOPINIT.md (ARCHITECTURE/PLAN/PROGRESS always loaded)
6. Thereafter, continue development based on PROGRESS.md
```

---

## 11. Choosing the Right Prompt

| Situation | Prompt to use |
|---|---|
| Starting a project for the first time | Initialization prompt (Section 2) |
| Starting development after specs and docs are generated | Development start prompt (Section 5) |
| Resuming previous work | Resume prompt (Section 7) |

---

## 12. Core Principles

- `AGENTINIT.md` is the initialization input document; you must write the project requirements in it.
- If core requirements are ambiguous in the initialization stage, the Agent asks the user.
- After initialization, the references for actual development are `AGENTS.md`, `ARCHITECTURE.md`, `PLAN.md`, `PROGRESS.md`, `features/*.md`, `qa/*.md`.
- **Decisions common across features go in `ARCHITECTURE.md` and are loaded every session.** They are not scattered across feature documents.
- In the development stage, do not ask for every minor implementation decision; ask only when a decision entirely different from the design intent is needed.
- `features/*.md` are final agreed feature specs, not per-Agent transcripts, and include a review summary (participating Agents·major risks).
- Important design decisions are split into `adr/*.md` and `adr/INDEX.md` is updated (specified triggers are mandatory).
- Do not arbitrarily fix the spec to erase a code-spec mismatch; diagnose authority first.
- "Test passed" counts only on actual run + result recorded.
- The first command for the next session in PROGRESS is provisionally recorded at work start and finalized at the end.
- When a meaningful unit of work is done, bundle code+docs into one commit and commit/push.
- Keep the guide `README.md` in the agentinit template repo only; do not copy it into your project. Your project's `README.md` is a separate deliverable generated at initialization, updated per push when there is user/install/run/architecture impact.
- Direct push to `main` / `master` is forbidden, and files containing secrets/certificates/private keys/tokens are not committed.
