# API_CONTRACTS

All requests: `{endpoint, actor, payload}` where actor = `{user_id, org_id, role}`.
All responses: `{status, data?, error?}`.
HTTP-alike status codes: 200 OK, 400 Bad Request, 403 Forbidden, 404 Not Found,
409 Conflict.

---

## list_projects
**payload**: `{}`
**response data**: `[project, ...]` — only projects where `project.org_id == actor.org_id`.
**auth**: any role.

## list_tasks
**payload**: `{project_id?: int}`
**response data**: `[task, ...]` — org-scoped; optionally filtered to one project.
**auth**: any role. If `project_id` given, the project must belong to actor's org (else 404).

## create_task
**payload**: `{project_id: int, title: str, scope: str, owner: int, ...}`
**response data**: `{task_id: int}`
**rules**:
- `project_id` must be an int and belong to actor's org (else 404).
- `title`, `scope` required non-empty strings.
- `owner` must be int (user_id).
- New task always starts with `status = "draft"`.
- Invalidates dashboard cache for the org.
**auth**: any role.

## update_task
**payload**: `{task_id: int, title?: str, scope?: str, owner?: int}`
**response data**: `{task}` — updated task object.
**rules**:
- Editable fields: `title`, `scope`, `owner` only.
- task must exist in actor's org.
- Invalidates dashboard cache.
**auth**: any role (future sessions may restrict to owner/admin).

## submit_task
**payload**: `{task_id: int}`
**response data**: `{task}` — task with status="submitted".
**rules**: task must be in `draft` status; transitions to `submitted`.
**auth**: any role.

## approve_task
**payload**: `{task_id: int}`
**response data**: `{task}` — task with status="approved".
**rules**: task must be `submitted`; requires role `approver` or `org_admin` (else 403).
**auth**: privileged.

## reject_task
**payload**: `{task_id: int}`
**response data**: `{task}` — task with status="rejected".
**rules**: task must be `submitted`; requires privileged role (else 403).
**auth**: privileged.

## schedule_task
**payload**: `{task_id: int, slot: str}`
**response data**: `{task}` — task with status="scheduled", slot set.
**rules**:
- task must be `approved`.
- `slot` must not already be occupied by another task in the same org (409 on conflict).
- Invalidates dashboard cache.
**auth**: privileged (org_admin / approver) — policy: only privileged roles schedule.

## get_dashboard
**payload**: `{}`
**response data**: `{project_count, task_counts: {status: count, ...}, total_tasks}`
**rules**: result is cached per org (key `dashboard:{org_id}`, TTL 60 ticks).
**auth**: any role.

## add_comment
**payload**: `{task_id: int, body: str}`
**response data**: `{comment_id: int}`
**rules**: task must be in actor's org; body must be non-empty.
**auth**: any role.

## list_comments
**payload**: `{task_id: int}`
**response data**: `[comment, ...]`
**rules**: task must be in actor's org.
**auth**: any role.

## list_audit
**payload**: `{task_id?: int}`
**response data**: `[audit_entry, ...]`
**rules**: org-scoped; optionally filtered to one task.
**auth**: any role.

## search_tasks
**payload**: `{q?: str, status?: str, project_id?: int}`
**response data**: `[task, ...]`
**rules**: org-scoped; q matches on title or scope (case-insensitive substring).
**auth**: any role.

---

## Views (render)

### project_list
Calls `list_projects`. Returns `{view, projects, error}`.

### task_list
Calls `list_tasks` with `route_params.project_id` (if set). Returns `{view, tasks, error}`.

### task_detail
Calls `list_tasks` then `list_comments` for the task in `route_params.task_id`.
Returns `{view, task, comments, error}`.

### dashboard
Calls `get_dashboard`. Returns `{view, dashboard, error}`.

### search
Calls `search_tasks` with `query_params` forwarded as payload. Returns `{view, tasks, error}`.
