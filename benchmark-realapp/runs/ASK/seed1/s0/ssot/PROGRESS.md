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

## Next session (S1) — expected work
- Implement submit/approve/reject/schedule lifecycle (ticket will specify).
- Enforce privileged roles on approve/reject (already coded, needs test coverage).
- Possibly: audit, comments, search, dashboard if ticket requests them.
