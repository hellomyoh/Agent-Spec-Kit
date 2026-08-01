# ADOPT.md

This is the prompt for **applying (adopting)** this framework to a project that is already under development (brownfield).

Whereas `KICKOFF.md` means "build forward from requirements (greenfield),"
`ADOPT.md` means **"reverse-document existing code into documentation (brownfield)."**

The goal is not actual implementation, but rather to **accurately document the current state of an existing codebase** so that you have the operational documents, cross-cutting contracts, feature specifications, QA, and development plan needed to continue development afterward with `DEVELOPINIT.md`.

> The artifact structure is **completely identical** to `KICKOFF.md` (see Section 1 below). Therefore, once adoption is complete,
> subsequent development uses `DEVELOPINIT.md` exactly as in greenfield.

> **Path baseline:** Except for the three root files (the project `README.md`, `AGENTS.md`, `CLAUDE.md`), all framework artifacts are created
> **inside the `THROUGHLINE/` folder**. Every artifact path in this document is relative to `THROUGHLINE/`.
> This way it does not conflict with same-named folders such as the existing project's `docs/` — **do not try to merge the existing project's folders into the kit's artifacts.**

> **No re-adoption:** A project where the `THROUGHLINE/` folder already exists and contains artifacts is **a project that has already been adopted**.
> Do not run ADOPT again; check `THROUGHLINE/PROGRESS.md` to continue, or confirm with the user.

---

# 0. Relationship with KICKOFF.md (avoiding duplication)

This document specifies **only brownfield-specific behavior**.
For the **detailed rules of writing documents, follow the corresponding sections of `KICKOFF.md` as-is.** (They are not duplicated in two copies.)

| Item | Rule to follow |
|---|---|
| File/folder structure to create | `KICKOFF.md` Section 1 |
| Handling AI-delegation markers (`[AI-delegated]`) | `KICKOFF.md` 2.4 |
| Multi-Agent review method / personas | `KICKOFF.md` Sections 4 & 5 |
| feature document granularity guide / structure | `KICKOFF.md` 6.0 & 6.1 |
| features/README.md / docs/README.md index format | `KICKOFF.md` 6.2 & 7.2 |
| ARCHITECTURE.md contents | `KICKOFF.md` Section 7 |
| Project README.md writing rules | `KICKOFF.md` 7.1 |
| QA document writing rules | `KICKOFF.md` Section 8 |
| AGENTS.md / CLAUDE.md writing rules | `KICKOFF.md` Sections 9 & 11 |
| Git rules | `KICKOFF.md` Section 10 |
| PLAN/PROGRESS/HISTORY/ASSUMPTIONS/NOTES/TODO/ADR format | `KICKOFF.md` Sections 12~16 |
| SOURCES/ management rules / INDEX format | `KICKOFF.md` 15.2 (application procedure in `DEVELOPINIT.md` 4.2) |

What ADOPT.md specifies **additionally/differently**: code analysis first, reverse-extraction, as-built specifications, merging existing files, test baseline, current-state-based PLAN.

---

# 1. Files to create

It produces the **same structure** as `KICKOFF.md` Section 1.

```text
<project root>
├── README.md            # Project README — merge if it already exists (root-fixed)
├── AGENTS.md            # Merge if it already exists (root-fixed — tool auto-recognition convention)
├── CLAUDE.md            # Merge if it already exists (root-fixed — auto-load)
└── THROUGHLINE/         # ★ All framework artifacts (isolated from existing project folders)
    ├── KICKOFF.md / ADOPT.md / DEVELOPINIT.md / AUDIT.md   # Copied prompts
    ├── ARCHITECTURE.md  # Reverse-extracted from existing code
    ├── PLAN.md          # Reflects current state as done / in progress / remaining
    ├── PROGRESS.md
    ├── HISTORY.md
    ├── ASSUMPTIONS.md
    ├── NOTES.md         # Non-trivial facts discovered while reading code closely
    ├── TODO.md          # Backlog (KICKOFF.md 15.3 — empty skeleton at adoption)
    ├── SOURCES/         # User-submitted materials (originals immutable)
    │   ├── INDEX.md
    │   └── REQUIREMENTS.md   # Optional: future goals / unimplemented requirements
    ├── features/        # Implemented features as as-built specifications
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
    ├── personas/        # Persona instances (KICKOFF.md 5.2)
    │   ├── INDEX.md
    │   └── *.md
    ├── discussion/      # Multi-Agent review deliberation logs (KICKOFF.md 4.1)
    │   └── review-*.md
    └── adr/
        ├── INDEX.md
        └── *.md
```

> **Do not overwrite files that already exist.** Follow Section 5 (existing-file merge rules).

---

# 2. Brownfield core principles

1. **Code is the current fact (authority for as-built).**
   The specification first accurately describes the code's actual behavior, then separately flags "the gap from intent."
   It neither disguises implementation mistakes as the specification, nor arbitrarily declares the code "correct."
2. **Read the code for real (do not stop at a metadata scan).**
   Do not skim only the file list, folder structure, and names to guess behavior; starting from the entry points, **directly read and trace the behavior** of each feature's actual implementation and core paths
   before writing the specification. The as-built specification must be grounded in "code that was read."
3. **No guessing (no-hallucination).** Assert only what you have directly read and confirmed.
   Do not write the behavior of code you have not read into the specification by guessing from file names or structure.
   Conventions, contracts, or intents that remained mere inference or that could not be confirmed from the code are recorded in `ASSUMPTIONS.md` with `status: active` (needs verification)
   and collected in the adoption report's "review recommended."
4. **Non-destructive to existing files.** Existing `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `docs/`, etc.
   are not overwritten; instead, merge them or present a diff and get confirmation (Section 5).
5. **Do not modify code in this step.** ADOPT is a documentation / planning step.
   Bugs, smells, and gaps you find are only recorded; the actual fixes are handed off to the `DEVELOPINIT.md` step.
6. **Tests are actually run to create a baseline.** Record the run result (pass/fail/absent), not a "claim of passing."

---

# 3. Inputs

* **Existing codebase (required).** This is the primary input for adoption.
* **`SOURCES/REQUIREMENTS.md` (optional, recommended).** If present, use it as "future goals / constraints / unimplemented requirements"
  and cross-check it against the as-built. If absent or empty, build the current-state document from the code and ask only as much as needed about future direction.
  (In brownfield, the type of this document is likewise `Initial requirements`, and it is frozen as `Applied` when adoption is complete.)
* **Existing documents (if any).** Absorb existing `README.md`/wiki/comments, etc. as auxiliary input for understanding intent.

---

# 4. Adoption work sequence

Adoption has many steps and can be interrupted. **Each time a step finishes, update the adoption progress state in `PROGRESS.md`.**
If interrupted, the next session reads `PROGRESS.md` and continues from where it left off.

1. **Inventory existing artifacts.** First, check whether existing artifacts are present in `THROUGHLINE/`
   (if so, no re-adoption — see the preamble). Next, identify which of the root README.md / AGENTS.md / CLAUDE.md / .gitignore
   already exist, and make a preservation/merge plan (Section 5).
   Same-named folders such as the existing project's docs/ are unrelated to the kit's artifacts, so do not touch them.
2. **Codebase scan (outer map).** Identify the language/runtime/framework, the build/run/test commands, directory structure, entry points,
   dependencies, and environment-variable **names** (never collect or record values/secrets).
   (This step is a **metadata map**. Do not stop here; actually read the code in step 3.)
3. **Read existing code closely (review).** Starting from the entry points, **directly read and trace the behavior** of the major features' actual implementations and core paths.
   Read first the **code that determines behavior**, such as routing/handlers/services/data access/external integrations/authentication paths.
   * Later steps (4 conventions, 5 specification, 9 ADR) must be **grounded in the code read here**.
   * Do not guess behavior from file names/folders/names alone (Section 2, principles 2 & 3).
   * If the code is vast, do not look at an arbitrary subset and claim "I saw it all"; instead, **explicitly state the range read and the range not read.**
     Leave the unread areas in `PROGRESS.md` so the next session continues reading them.
4. **Reverse-extract cross-cutting conventions → `ARCHITECTURE.md` draft.** From the code you read, detect and record the
   naming actually used (DB/variables/files/API paths), the API contract style and error format, the authentication/session method, and common data-model rules.
   Items that cannot be confirmed from the code are left in `ASSUMPTIONS.md` (active).
   (The contents follow `KICKOFF.md` Section 7, but interpret "decide" as "detect/confirm.")
5. **Identify implemented features and write as-built specifications.** From the code you read, decompose into feature units (granularity guide `KICKOFF.md` 6.0), and
   write each feature **exactly as it currently behaves** into `features/*.md` (structure `KICKOFF.md` 6.1).
   * **Cite the supporting code (accuracy check):** Each behavior claim in the specification must be able to cite the code location (file/function) it is based on.
     Do not assert behavior you have not directly read; mark it as "estimated (needs verification)" (Section 2, principle 3).
     Where possible, **cross-check** by actually running that path or with a test.
   * Code↔intent gaps, dead code, unfinished features, and suspect spots are recorded in that feature document's **Section 15 (open issues)** and
     `ASSUMPTIONS.md`; if you cannot judge, ask per Section 6.
   * For non-trivial features, leave a minimal review summary (participating Agents · major risks) per `KICKOFF.md` 4.1.
6. **Identify unimplemented/planned items.** If `SOURCES/REQUIREMENTS.md` is present, classify the requirements listed there that are not yet in the code
   as "remaining work." Requirements that conflict with the as-built are asked per Section 6.
7. **Test baseline.** **Actually run** the existing automated tests and record the result (run command + pass/fail/absent).
   Reflect failed/absent items into `HISTORY.md`/`PROGRESS.md` and the `qa/` documents as the current coverage.
8. **Write QA documents** (`KICKOFF.md` Section 8). However, reflect the **current coverage reality** first rather than an ideal standard,
   and mark the lacking parts as "needs reinforcement."
9. **Retroactive ADRs (optional).** For important design decisions already reflected in the current code (architecture/auth/DB/external API/deployment, etc.),
   record only the essential core as retroactive ADRs and create `adr/INDEX.md`. Do not create them excessively.
10. **Finalize `ARCHITECTURE.md`**, **write/merge the project `README.md`** (`KICKOFF.md` 7.1; if it already exists, Section 5).
11. **Write/merge `AGENTS.md` / `CLAUDE.md`** (`KICKOFF.md` Sections 9 & 11; if they already exist, Section 5).
12. **Write `PLAN.md`:** reflect the current state by marking Phases as **done (existing implementation) / in progress / remaining**.
13. **Write `PROGRESS.md`:** seed the current state and record the **first command for the next session**.
14. **Write `HISTORY.md`:** set the first entry as "Framework adoption (ADOPT)" and record the test baseline and the gap list.
15. **Write `ASSUMPTIONS.md`:** record reverse-extracted estimates and items needing verification.
16. **Write `NOTES.md`** (`KICKOFF.md` 15.1): record, by topic, the non-trivial facts **confirmed** while reading code closely
    (undocumented external-API behavior, environment pitfalls, performance characteristics).
    Unconfirmed guesses go in ASSUMPTIONS, not NOTES.
17. **Create/update `SOURCES/INDEX.md`** (`KICKOFF.md` 15.2).
    If `SOURCES/REQUIREMENTS.md` is present, register it with type `Initial requirements` and freeze it as `Applied` when adoption is complete.
    Whether to move and register existing scattered requirements/spec documents into SOURCES/ is done only after user confirmation
    (the non-destructive principle of Section 5 applies — do not move them arbitrarily).
18. **Commit the adoption artifacts.** Perform adoption on a work branch (e.g., `docs/agentspeckit-adopt`) — the project already has working code, so do not work directly on main/master. Bundle the generated/merged documents into a single commit (interim milestone commits are allowed if adoption spans multiple sessions). This commit contains documents only — no code changes (Section 2, principle 5). Push follows the push policy (default: commit only).
19. **Report adoption completion** (Section 7 format).

---

# 5. Existing-file merge rules (important)

Since the kit's artifacts are isolated inside THROUGHLINE/, the merge targets are effectively just the **four root files**
(`README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`). If these already exist, **do not overwrite them.**
Same-named folders such as the existing project's `docs/` are separate from the kit's artifacts (THROUGHLINE/docs/), so do not merge or modify them.

* Prioritize **preserving** the existing content. The object of preservation is not the exact wording but the **meaning (rules/information)**.
* If an item the framework requires is missing, **add (merge)** it.
* **The descriptive prose of the merge result also follows the language baseline (KICKOFF.md preamble).**
  If the existing content is written in another language, preserve the meaning and translate it into the prescribed language before merging —
  appending content with mixed languages turns that file (especially CLAUDE.md, which is auto-loaded every session) into an ignition signal for English drift.
  (Code identifiers, proper nouns, and `.gitignore` are not subject to translation.)
* If existing content conflicts with a framework rule, do not change it arbitrarily; **present a diff/alternative and then get confirmation.**
* If a large change is unavoidable, preserve the pre-change state (e.g., a backup or tracked via git) before proceeding.
* For `.gitignore`, keep existing entries and add only the missing ones.

---

# 6. When to ask the user during adoption

These are brownfield-specific criteria. (For other general criteria, follow `KICKOFF.md` 2.1.)

* When the code and the intent conflict and you **cannot reasonably judge which one is authoritative**
* When you must **overwrite or significantly change an existing artifact file** (always confirm)
* When a requirement in `SOURCES/REQUIREMENTS.md` **clearly conflicts with the current implementation**
* When a code modification seems necessary but is outside the scope of this step (documentation) → do not modify; record and confirm as remaining work
* When a structure is found that could affect sensitive information/personal data/security

Handling of `[AI-delegated]` markers is identical to `KICKOFF.md` 2.4.

---

# 7. Output format

After adoption is complete, report in the following format.

```md
# Project adoption (ADOPT) result

## Files created / files merged
(Distinguish what was newly created from what was merged into existing files)

## Codebase summary
- Stack / build·run·test commands / structure overview

## Code-reading range
- Areas directly read and whose behavior was confirmed:
- Areas not yet read (continue reading next session):

## Cross-cutting contracts (ARCHITECTURE.md) — reverse-extraction summary
(Distinguish what was confirmed by detection / what was left as estimated (needs verification))

## as-built feature specification list
(Supporting code location for each feature; mark behavior left as estimated)

## Code ↔ intent gap / suspect-spot list
(Candidates to address in the future DEVELOPINIT step)

## Test baseline
- Run command:
- Pass / fail / nonexistent:

## QA documents / current coverage

## ADR list (INDEX, including retroactive)

## Development Phase summary (done / in progress / remaining)

## AI-delegated / estimated items (review recommended)

## Items requiring user confirmation

## Next steps
(Subsequent development uses DEVELOPINIT.md. Point to PROGRESS.md's "first command for the next session")
```

---

# 8. Completion criteria

Satisfy the completion criteria of `KICKOFF.md` Section 17, while additionally satisfying the following brownfield criteria.

* Implemented features are documented as **as-built specifications**
* The as-built specifications are **grounded in code that was actually read**, and each behavior claim can cite the supporting code location
  (behavior not directly read is not asserted but marked as "estimated (needs verification)")
* The **range read / range not read** is stated, and unread areas are left in PROGRESS.md
* The **code ↔ intent gap list** is organized and recorded in HISTORY/ASSUMPTIONS/feature Section 15
* The **run baseline** of existing tests is recorded in HISTORY.md
* Existing artifact files have been **merged without overwriting**, or, where overwriting was needed, user confirmation was obtained
* `ARCHITECTURE.md` was **reverse-extracted** from the code, and estimated items are stated in ASSUMPTIONS
* `PLAN.md` reflects the **current state (done / in progress / remaining)**
* **No code was modified** in this step (documentation/planning only)
* The adoption artifacts are **committed on a work branch** (documentation-only commit — no code changes; interim commits allowed for a multi-session adoption)
