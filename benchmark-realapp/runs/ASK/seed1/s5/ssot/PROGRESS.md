# PROGRESS

## S0 — Scaffold (completed 2026-06-21)

### Implemented
- `_define_schema(db)`: declares 4 tables — projects, tasks, comments, audit.
- `seed(backend, spec)`: loads `{"projects": [...]}` into the projects table.
- Endpoints fully implemented (all 13 from contract):
  - **S0 ticket scope**: `list_projects`, `list_tasks`, `create_task`
  - **Stubs for future use (fully working)**: `update_task`, `submit_task`,
    `approve_task`, `reject_task`, `schedule_task`, `get_dashboard`,
    `add_comment`, `list_comments`, `list_audit`, `search_tasks`
- Views: `project_list`, `task_list`, `task_detail`, `dashboard`, `search`
- Multi-tenant isolation: all reads/writes scoped to `actor.org_id`.
- Dashboard cache: key `dashboard:{org_id}`, TTL 60 ticks, invalidated on mutations.

### Self-test result
All assertions passed:
- `list_projects` returns seeded project for correct org.
- `create_task` returns `task_id`.
- `list_tasks` returns the created draft task.
- Org isolation: `list_projects` and `list_tasks` for a different org return `[]`.

## S1 — Create & edit task requests (completed 2026-06-21)

### Implemented
- Added `priority` (nullable int) field to tasks schema; only `project_id`, `org_id`,
  `title`, `status`, `created_by` are required columns now.
- `create_task`: `scope`, `owner`, `priority` are now optional (only `title` required
  per ticket). Fixed contract alignment.
- `update_task`: `priority` added to editable fields (alongside title, scope, owner).
- `get_dashboard`: fixed response shape to `{"total": int, "by_status": dict}` per
  contract (`DASHBOARD_SHAPE`). Previous shape was wrong.

### Self-test result
All assertions passed:
- `create_task` with title-only (no scope/owner) returns task_id.
- `list_tasks` shows the draft task with all expected fields including `priority`.
- `update_task` can edit title, scope, and priority; changes reflected in list_tasks.
- Dashboard returns `{total: 1, by_status: {draft: 1}}`.
- Org isolation: different org sees no tasks.
- `create_task` with all fields (including priority=3) works correctly.

## S2 — Status transitions / approval workflow (completed 2026-06-21)

### Implemented
- `submit_task` (`draft → submitted`): any role; 409 if not draft.
- `approve_task` (`submitted → approved`): privileged only (org_admin|approver); 403 if
  not privileged, 409 if not submitted.
- `reject_task` (`submitted → rejected`): privileged only; same error rules.
- `update_task` CANNOT change status (status not in `allowed_fields`). Confirmed unchanged.
- All illegal transitions (e.g. approve a draft, reject an approved task) return 409 and
  leave the status unchanged.
- `render("task_detail", ...)` now returns `available_actions: list[str]` computed from
  the task's current status and the actor's role:
  - `draft`: `["submit_task"]`
  - `submitted` + privileged: `["approve_task", "reject_task"]`
  - `approved` + privileged: `["schedule_task"]`
  - all other combinations: `[]`

### Self-test result
All assertions passed (13 test cases):
- create/update/submit/approve/reject happy paths.
- Illegal state jumps all return 409.
- Non-privileged approve returns 403.
- `task_detail` available_actions correct for draft/submitted/approved × member/privileged.

## S3 — Permissions / role-based access (completed 2026-06-21)

### Implemented
- Roles updated: `org_admin`, `project_owner`, `member` (replaced `approver`).
- Added `_can_approve(actor, task)` method:
  - `org_admin` → always allowed.
  - `project_owner` → allowed only if `actor.user_id == project.owner_id` for the task's project.
  - `member` → never allowed.
- `approve_task` and `reject_task` now use `_can_approve` with existence-hiding:
  unauthorised actors receive 404 ("task not found"), not 403.
- `task_detail` render: `available_actions` now computed via `backend._can_approve(actor, task)`
  instead of the old role-string check.
- `_is_privileged` updated to `{"org_admin", "project_owner"}` (used by `schedule_task`).

### Self-test result
All 9 assertions passed:
- `member` approve/reject → 404 (existence-hiding).
- `project_owner` of wrong project → 404.
- `project_owner` of correct project → 200 approved.
- `org_admin` → 200 approved.
- `task_detail` available_actions: member → [], correct project_owner → ["approve_task", "reject_task"].

## S4 — Scheduling (completed 2026-06-21)

### Implemented
- `schedule_task` (`approved → scheduled`): takes an integer `slot`.
- Fixed slot validation: `if not isinstance(slot, int)` (was `if not slot`, which broke for slot=0).
- Fixed conflict check: scoped to **project** (not org). Two tasks in the same project cannot share
  a slot. Tasks in different projects CAN share the same slot number.
- `slot` stored as-is (integer) in the tasks table.
- Returns 409 if task is not `approved`; 409 if slot already taken in the same project; 400 if
  slot is missing or not an int.
- Updated D5 in DECISIONS: slot conflict is now project-scoped (not org-scoped).

### Self-test result
All 6 assertions passed:
- approved task schedules into free slot → 200.
- second task in same project+slot → 409 conflict.
- task in different project same slot → 200 (no conflict cross-project).
- non-approved (draft) task schedule → 409.
- missing slot → 400.
- integer slot=0 → 200 (correctly accepted).

## S5 — Dashboard + caching (completed 2026-06-21)

### Implemented
- `get_dashboard`: returns `{"total": int, "by_status": {status: count}}` for the actor's org.
- Result is cached per org using key `dashboard:{org_id}` with TTL=60 ticks.
- Cache is invalidated by all count-affecting mutations: `create_task`, `update_task`,
  `submit_task`, `approve_task`, `reject_task`, `schedule_task`.
- Org isolation: each org has its own cache key; org A and org B never share dashboard data.
- Implementation was already in place from S0 scaffold; verified correct and complete.

### Self-test result
All 8 assertions passed:
- Empty dashboard returns `{total: 0, by_status: {}}`.
- Dashboard updates immediately after create_task (draft counted).
- Dashboard updates after submit_task (submitted counted).
- Dashboard updates after approve_task (approved counted).
- Dashboard updates after schedule_task (scheduled counted).
- Org B sees its own empty dashboard while org A has tasks.
- Org A and org B counts remain independent after each creates their own tasks.
- Cache keys are org-scoped (`dashboard:1`, `dashboard:2` stored separately).
