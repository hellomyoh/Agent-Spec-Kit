# S2 — Status transitions (approval workflow)

Implement the request workflow with dedicated endpoints:
- `submit_task`: `draft → submitted`
- `approve_task`: `submitted → approved`
- `reject_task`: `submitted → rejected`

Rules:
- **Status may change ONLY through these dedicated transition endpoints — never via
  `update_task`.**
- **Only the transitions defined in the lifecycle are allowed; any other transition must
  be refused** (e.g. you cannot approve a `draft`, cannot schedule yet, cannot reject an
  already-approved task). Lifecycle: `draft → submitted → approved/rejected → scheduled →
  completed`.

The task detail view should offer the actions valid for the current status.

Acceptance: a draft can be submitted then approved or rejected; illegal jumps are refused
and leave the status unchanged.

<!-- tags: explicit(state_machine, status-only-via-transitions) -->
