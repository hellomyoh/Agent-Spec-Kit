# DECISIONS

## S0 — 2026-06-21

### D1: org_id denormalised on tasks, comments, audit
Storing `org_id` directly on every child row avoids joining through `projects`
for every tenant-scoped query. Trade-off: write-time must always populate it.
This is the blessed approach — do not remove it.

### D2: users/orgs not stored in DB
Per contract: every request carries `actor = {user_id, org_id, role}`. There
is no users or orgs table. All permission and scoping decisions are derived
from the actor dict on each request.

### D3: privileged roles = org_admin | project_owner
S3 replaced `approver` with `project_owner`. The three valid roles are
`org_admin`, `project_owner`, `member`. `_is_privileged(actor)` checks
`{"org_admin", "project_owner"}` (used by schedule_task). For approve/reject
use `_can_approve(actor, task)` which additionally verifies that a
`project_owner` owns the task's specific project (see D14).

### D4: single Backend class, no sub-routers
All endpoints live as private methods on `Backend`. This is simple enough for
the current scale. If the module grows past ~600 lines, split into
`backend_tasks.py`, `backend_projects.py`, etc. and re-export from `app.py`.

### D5: slot conflict check is project-scoped (updated S4)
Two tasks in the same **project** cannot share a `slot`. Tasks across projects
(even within the same org) CAN share the same slot number. Multi-tenant
isolation still applies — org_id is always verified before checking project.
This rule is enforced in `_schedule_task` via `query("tasks", project_id=..., slot=...)`.

### D6: update_task editable fields are title, scope, owner only
`project_id`, `status`, `org_id`, `created_by` are immutable via `update_task`.
Status changes go through the dedicated transition endpoints.

### D7: dashboard cache TTL = 60 ticks
Chosen as a reasonable staleness window for aggregate counts. The harness
controls the clock; if a test needs fresh data it will tick past TTL or
the mutation path will invalidate the key.

## S1 — 2026-06-21

### D8: create_task only requires title (scope/owner/priority optional)
Per ticket: "title is required". scope defaults to None, owner defaults to None,
priority defaults to None. The DB schema reflects this — only project_id, org_id,
title, status, created_by are required columns. Do NOT revert to treating scope/owner
as required.

### D9: update_task editable fields = title, scope, owner, priority
`priority` added in S1 to match contract TASK_FIELDS. Other immutable fields
(project_id, status, org_id, created_by) are unchanged.

### D10: dashboard response shape = {total, by_status}
Contract specifies `DASHBOARD_SHAPE = {"total": int, "by_status": dict}`.
The old shape (project_count, task_counts, total_tasks) was wrong and corrected in S1.
Future sessions must use `total` and `by_status` keys only.

## S2 — 2026-06-21

### D11: status changes ONLY via dedicated transition endpoints
`update_task.allowed_fields` must NEVER include `status`. Status transitions are
exclusively: `submit_task`, `approve_task`, `reject_task`, `schedule_task`. Any
attempt to sneak status through `update_task` is silently ignored (field not in
`allowed_fields`). Do NOT relax this rule.

### D12: task_detail view exposes available_actions
`render("task_detail", ...)` returns an `available_actions: list[str]` key that
enumerates the endpoint names the actor can legally invoke on the task right now.
The list is derived from `task.status` and `actor.role` on every render call — it is
NOT cached. Rules:
- `draft` → `["submit_task"]` (any role)
- `submitted` + can_approve → `["approve_task", "reject_task"]`
- `approved` + can_approve → `["schedule_task"]`
- everything else → `[]`
`can_approve` uses `backend._can_approve(actor, task)` (see D14).

### D13: lifecycle order is draft→submitted→approved/rejected→scheduled→completed
No skipping steps. Any transition from a status not listed as the `from_status`
for that action returns 409 Conflict. The `_transition` helper enforces this by
checking `task["status"] != from_status`.

## S3 — 2026-06-21

### D14: approve/reject permission = org_admin OR owning project_owner; denied = 404
S3 introduced existence-hiding: a `member` (or any actor without approve rights)
who calls `approve_task` or `reject_task` gets a 404 response identical to "task
not found" — they cannot learn whether the task exists.

Permission logic (`_can_approve(actor, task)`):
- `org_admin` → always allowed (within org).
- `project_owner` → allowed only if `actor.user_id == project.owner_id` where
  `project` is the task's own project.
- `member` → never allowed.

`approve_task` and `reject_task` are implemented as standalone methods (not via
`_transition`) because they need access to the task before deciding permission, so
the existence-hiding LookupError can be raised after the task is fetched.

### D15: member role cannot learn task existence via approve/reject
When `_can_approve` returns False, `LookupError` is raised (not `PermissionError`).
The exception handler maps `LookupError` → 404. This is the canonical existence-hiding
pattern. Do NOT switch this to 403 even if it seems more "correct" — the ticket
explicitly requires it.

## S4 — 2026-06-21

### D16: slot is an integer; validation uses isinstance(slot, int)
The ticket specifies slot as "an integer time slot". Validation uses
`isinstance(slot, int)` (not `if not slot`) so that slot=0 is accepted.
Non-integer or missing slot raises RuntimeError → 400.

### D17: slot conflict is project-scoped (replaces org-scoped D5)
The ticket says "two scheduled tasks in the same **project** must not occupy the
same slot". The conflict check queries `tasks` filtered by `project_id` and `slot`.
Tasks in different projects within the same org may share slot numbers.
