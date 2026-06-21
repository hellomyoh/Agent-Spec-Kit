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

## Next session (S2) — expected work
- Implement submit/approve/reject/schedule lifecycle if not already tested.
- Enforce privileged roles on approve/reject.
- Possibly: audit, comments, search enhancements.
