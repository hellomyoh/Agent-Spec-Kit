# AGENTINIT.md

> This is the English version of the AGENTINIT input document. References to other files
> use their canonical names (`AGENTINIT.md`, `KICKOFF.md`, `DEVELOPINIT.md`).

This document is the user input file for Agent-based project initialization.

You must fill in the project overview, rough requirements, core features, and constraints here,
then hand this file to the Agent together with the `KICKOFF.md` prompt.

Based on this document, the Agent analyzes the project and generates the feature specifications,
user documentation, QA documents, the development plan, the cross-cutting contract document
(`ARCHITECTURE.md`), and the Agent work instructions.

> Important: If this document is too empty or the core requirements are ambiguous,
> the Agent must not continue initialization and must instead ask you questions to clarify the requirements.

> Tip: You do not have to fill in every item perfectly.
> However, write **Section 2 (Project Description)**, **Section 3 (Core Features)**,
> **Section 4 (User Scenarios)**, and — if there are external integrations — **Section 5**
> as concretely as possible. If these are empty, the Agent will pause initialization and ask.

---

# 0. Delegating Unknown Items to the AI

For items you are unsure about or cannot decide, instead of leaving them blank, write the marker
below and the Agent will decide for you.

* `[AI delegated]`  (aliases: `[leave to AI]`, `[unknown]`)

How it is handled depends on the item's risk level.

* **Non-critical items** (naming, code style, non-critical UI, low-priority feature details, log format, etc.):
  The Agent picks a reasonable default, proceeds, and records it in `ASSUMPTIONS.md`. It does not ask.
* **Critical items** (MVP scope, data model, authentication/authorization, personal data handling,
  external integration approach, etc.):
  The Agent does not stop initialization. It adopts **the most conservative, easily reversible choice**
  as a provisional decision. This provisional decision is recorded in `ASSUMPTIONS.md` and collected under
  **"Items Decided by AI Delegation (Review Recommended)"** in the initialization report, so you can review
  and adjust it later.

Notes:

* **If both the project purpose and the core features are delegated/blank**, the Agent does not accept the
  delegation and asks instead. "What this project is" cannot be delegated.
* Items with **cost, billing, legal impact, or hard-to-reverse effects** are never decided silently even when
  delegated. The Agent picks a conservative, no-cost/no-risk default and requests confirmation in the report.

Example:

```text
## Authentication / Session Model (Shared)

[AI delegated]   ← Agent provisionally adopts a conservative default (e.g., standard token-based + secure storage) and flags it in the report

## Design Tone

[unknown]        ← Non-critical, so the Agent picks a default and records it only in ASSUMPTIONS.md
```

---

# 1. Project Basics

## Project Name

<!-- e.g., Stability Metrics Collection & Analysis Application -->

## Project Purpose

<!-- Describe the problem this project aims to solve. -->

## Target Users

<!-- Describe the actual users, organizations, operators, administrators, etc. -->

## Core Value

<!-- Describe the value users gain from this project. -->

---

# 2. Project Description

<!-- Free-form. A rough description is fine. -->

Example:

Stability Metrics Collection & Analysis Application

* Collects data via the l&cs API.
* The API spec is at the following URL:

  * https://docs.nhncloud.com/en/Data%20&%20Analytics/Log%20&%20Crash%20Search/en/api-guide/
* Collected data is stored locally.
* Analyzes the characteristics and fields of the locally stored data.
* Produces graphs based on the analysis results.
* Provides a screen where users can easily review the metrics.

---

# 3. Core Features

> Granularity guide: write one "feature" as **an independent unit that delivers one user value**.
> Split things like "data collection", "data analysis", "metrics view screen",
> and avoid lumping too much together like "the whole system" or "all screens".
> If features exceed 7–8, actively split off what can be deferred to a later priority.

## Features That Must Be in the MVP

* Feature 1:
* Feature 2:
* Feature 3:

## Lower-Priority Features

* Feature 1:
* Feature 2:
* Feature 3:

---

# 4. User Scenarios

<!-- Describe the flow in which users use the service. -->

1.
2.
3.

---

# 5. External Integrations

## External API

* Name:
* URL:
* Authentication method:
* API documentation:
* Call frequency:
* Limitations:

## External System

* System name:
* Integration purpose:
* Data send/receive direction:
* Behavior on failure:

---

# 6. Data Requirements

## Data to Store

* Data name:
* Key fields:
* Storage location:
* Retention period:
* Contains sensitive info?:

## Data to Analyze

* Analysis target:
* Analysis purpose:
* Aggregation basis:
* Visualization needed?:

---

# 7. Screen / UX Requirements

## Main Screens

* Screen 1:
* Screen 2:
* Screen 3:

## User Flow

* Main entry path:
* Main task flow:
* Exception/edge-case flow:

## Design Requirements

* Design tone:
* Mobile support?:
* Accessibility requirements:
* Internationalization (i18n) support?:

---

# 8. Technical Conditions

## Preferred Tech Stack

* Frontend:
* Backend:
* Database:
* Infra:
* Batch / Scheduler:
* Other:

## Constraints That Must Be Respected

* Security:
* Performance:
* Operations:
* Deployment:
* Internal policy:
* Browser / OS support range:

---

# 9. Authentication / Authorization

## User Types

* General user:
* Administrator:
* Operator:
* External system:

## Authorization Rules

* Login required?:
* Admin features:
* Data access restrictions:
* Audit log required?:

---

# 10. Cross-Cutting (Architecture) Baseline

> This section is the "contract" applied in common across multiple features.
> The Agent generates `ARCHITECTURE.md` based on this section and always loads that document
> in every development session.
> If left blank, the Agent picks reasonable defaults and records them in `ARCHITECTURE.md` and `ASSUMPTIONS.md`.
> For anything you are unsure about, write `[AI delegated]`. It is handled per Section 0.

## Common Data Model Rules

<!-- e.g., created_at/updated_at on all tables, whether to use soft delete, ID strategy (UUID/auto-increment), etc. -->

## Naming Conventions

<!-- e.g., snake_case DB columns, camelCase JS variables, API path casing, etc. Leave blank if undecided. -->

## API Contract Style

<!-- e.g., REST/GraphQL, error response format, pagination approach, versioning strategy, etc. -->

## Authentication / Session Model (Shared)

<!-- e.g., token-based/session-based, token storage location, expiry/refresh policy, etc. -->

---

# 11. Test / QA Requirements

## Core Scenarios That Must Be Verified

* Scenario 1:
* Scenario 2:
* Scenario 3:

## Areas Needing Automated Tests

* API:
* Screens:
* Data processing:
* Batch / scheduler:
* External integrations:

## Areas Needing Manual QA

* Screen usability:
* Admin features:
* Data validation:
* Operational scenarios:
* Edge cases:

## Features Where Regression Testing Matters

* Feature 1:
* Feature 2:
* Feature 3:

## Failure Situations

* API failure:
* DB failure:
* Network failure:
* Data errors:
* Authentication errors:
* Authorization errors:

## Quality Criteria

* Performance criteria:
* Stability criteria:
* Log / monitoring items needed:
* Alerts needed?:

---

# 12. Operations / Deployment

## Runtime Environments

* Local:
* Development:
* Staging:
* Production:

## Deployment Method

* Manual deployment:
* CI/CD:
* Docker used?:
* Cloud / on-premise?:

---

# 13. Additional Requests

<!-- Write freely. -->
