# OpsBoard Session Notes (last 2 sessions)

--- S4 ---
schedule_task: approved->scheduled, slot (integer). No privilege gate. Slot conflict per-project (queries tasks by project_id+status=scheduled, compares int(slot)). slot stored as str (coerced). Non-approved -> CONFLICT 409. Same slot in different projects allowed. Audit-logged, dashboard cache invalidated on success. Data model reminder: tasks have org_id (multi-tenant: all reads/writes filter actor.org_id, cross-org 404). Dashboard cached per org key dashboard:{org_id}, invalidate on mutation.

--- S5 ---
get_dashboard: returns {total, by_status, project_count, task_count} for actor's org. Cache key dashboard:{org_id} (org-isolated). Cache invalidated after every mutation: create_task, update_task, submit_task, approve_task, reject_task, schedule_task. Cache TTL=60. Implementation was already present from prior sessions; self-tested org isolation (org A and org B never share counts) and staleness (dashboard reflects state immediately after any mutation).
