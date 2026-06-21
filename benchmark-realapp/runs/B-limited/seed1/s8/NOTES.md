--- S7 ---
list_audit: org-scoped, optional task_id filter (404 if cross-org task). Audit entries on every status transition. audit table: task_id/org_id/user_id/action/from_status/to_status/detail. General rule across the app: every read/write is scoped to actor.org_id; cross-org access is hidden as 404.
--- S8 ---
search_tasks: org-scoped (queries tasks with org_id=actor.org_id first), then filters by optional q (case-insensitive substring of title/scope), status, and project_id. The search view wires query_params.q/status/project_id to the endpoint. No cross-org leakage possible because the base DB query is always tenant-scoped.
