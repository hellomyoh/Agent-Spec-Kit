# OpsBoard Session Notes

## S7
list_audit: org-scoped. Audit on every status transition. General rule across the app: every read/write is scoped to actor.org_id; cross-org access hidden as 404.

## S8
search_tasks: org-scoped base query then filters q (substring title/scope)/status/project_id. update_task currently allows editing title/scope/owner/priority on tasks; non-privileged can only edit drafts. Status changes only via transition endpoints (not update_task).

## S9
Lock core fields after approval: update_task now refuses changes to title/scope/owner when task status is approved, scheduled, or completed (returns CONFLICT 409). Non-core fields (priority) remain editable. Draft editing is unchanged. The task_detail render view returns locked_fields=["title","scope","owner"] when the task is in an approved-or-later status (empty list otherwise).
