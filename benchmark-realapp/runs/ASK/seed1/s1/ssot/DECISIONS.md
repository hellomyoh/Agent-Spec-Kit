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

### D3: privileged roles = org_admin | approver
The set `{"org_admin", "approver"}` is what `_is_privileged(actor)` checks.
Add new roles here if the product definition expands. Do NOT hard-code
role strings anywhere else.

### D4: single Backend class, no sub-routers
All endpoints live as private methods on `Backend`. This is simple enough for
the current scale. If the module grows past ~600 lines, split into
`backend_tasks.py`, `backend_projects.py`, etc. and re-export from `app.py`.

### D5: slot conflict check is org-scoped
Two tasks in the same org cannot share a `slot`. Tasks across orgs CAN share
a slot (multi-tenant isolation). This rule is enforced in `_schedule_task`.

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
