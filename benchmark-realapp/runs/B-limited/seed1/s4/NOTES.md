# OpsBoard Session Notes

--- S3 ---
Permissions: _can_approve(actor,task) allows org_admin (any task in org) or project_owner (actor.user_id==project.owner_id). approve_task/reject_task use _can_approve with existence-hiding: NOT_FOUND 404 for missing tasks AND unauthorized actors. task_detail available_actions shows approve/reject only when _can_approve passes. (schedule_task currently still uses an org_admin/approver privilege check.)

--- S4 ---
schedule_task: approved->scheduled, slot (integer). Removed privilege gate (no role requirement per ticket). Slot conflict check is per-project (not org-wide): queries tasks by project_id+status=scheduled, compares int(slot). slot stored as str. Non-approved tasks get CONFLICT 409. Same slot in different projects is allowed. Audit-logged and dashboard cache invalidated on success.
