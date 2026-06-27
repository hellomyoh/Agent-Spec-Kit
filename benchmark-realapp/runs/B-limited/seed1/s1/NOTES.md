# S1 Handoff Notes

## What was done
- Added `priority` (int, default 0) field to the tasks table schema; required for the contract's TASK_FIELDS.
- `create_task` now accepts optional `priority` in payload (defaults to 0).
- `update_task` now allows editing `priority` in addition to `title`, `scope`, `owner`. Coerces to int. Only draft tasks editable by non-privileged actors; admins can update any status.
- Dashboard response now includes `total` key (alongside `task_count` and `project_count`) to match contract DASHBOARD_SHAPE: `{"total": int, "by_status": dict}`.

## Contract notes
- TASK_FIELDS: id, project_id, title, scope, owner, status, slot, priority — all present.
- DASHBOARD_SHAPE: must have `total` (int) and `by_status` (dict).
- `create_task` returns `{"task_id": int, "task": {...}}` — task_id key satisfies contract.
- All 13 endpoints remain wired; handlers from S0 unchanged except the above.

## Data model
- projects: name, org_id, owner_id
- tasks: project_id, org_id (denorm), title, scope, owner (user_id), priority (int), status (enum), slot (str nullable)
- comments: task_id, org_id, user_id, body
- audit: task_id, org_id, user_id, action, from_status, to_status, detail

## Status lifecycle
draft -> submitted -> approved/rejected -> scheduled -> completed
- submit_task: draft->submitted (any actor)
- approve_task / reject_task: submitted->approved|rejected (privileged: org_admin, approver)
- schedule_task: approved->scheduled (privileged; slot conflict check within org)

## Multi-tenancy
- Every table carries org_id. All reads/writes filter by actor.org_id. Cross-org attempts return 404.

## Cache
- Dashboard cached per org with TTL=60 ticks under key `dashboard:{org_id}`. Invalidated on any task/project mutation.
