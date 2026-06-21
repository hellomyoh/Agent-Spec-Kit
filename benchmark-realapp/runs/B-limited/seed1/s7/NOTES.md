# Session Notes (last 2 sessions)

--- S6 ---
add_comment/list_comments: org-isolated via _get_task check (404 if cross-org); comments table task_id/org_id/user_id/body. Already implemented from schema setup.

--- S7 ---
list_audit: org-scoped, optional task_id filter (404 if cross-org task). Audit entries written on every status transition: submit (draft_to_submitted), approve (submitted_to_approved), reject (submitted_to_rejected), schedule (scheduled). audit table: task_id/org_id/user_id/action/from_status/to_status/detail. No new code needed — already fully implemented in app.py from prior sessions.
