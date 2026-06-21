# S7 — Audit log

Make changes traceable.

- `list_audit`: returns a trace of changes, optionally filtered by `task_id`, scoped to the
  actor's org.
- **Every status change (submit/approve/reject) and every scheduling must be recorded** in
  the audit trail.
- Audit entries are org-scoped like everything else.

Acceptance: after submitting/approving/scheduling a task, its audit trail lists those
events; another org cannot see them.

<!-- tags: explicit(audit_trail: record status changes + scheduling, org-scoped) -->
