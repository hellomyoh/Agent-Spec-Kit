# S3 — Permissions

Add role-based access to the approval workflow. Roles (on `actor.role`):
`org_admin`, `project_owner`, `member`.

- **Only an `org_admin`, or the `project_owner` of the task's project, may `approve_task`
  or `reject_task`.** A `member` must not be able to.
- **A user who is not allowed to act on a task must not be able to learn whether it even
  exists** — respond as if the task is not found rather than revealing that it exists but
  is forbidden. (This applies to acting on tasks the user may not see, including across orgs.)
- The detail view must only offer the approve/reject actions to users who are actually
  allowed to perform them.

Acceptance: a member's approve attempt is refused and indistinguishable from a missing
task; an org admin or the owning project's owner succeeds.

<!-- tags: explicit(permissions roles), explicit(existence-hiding: "as if not found") -->
