# S0 — Scaffold OpsBoard

Stand up the skeleton of **OpsBoard**, a team task-operations app.

Domain: a team has **projects**; a project has **task requests**.

Implement the `app` module on top of the provided `db` and `cache` (see `provided/`),
exposing exactly the shared contract entry points: `make_backend(db, cache)`,
`render(view, backend, client_state)`, `seed(backend, spec)`.

This session:
- Define your data model (declare tables via the provided db) and `seed()` to load
  the public seed spec `{"projects": [{"name", "org_id", "owner_id"}, ...]}`.
- Endpoints: `list_projects`, `list_tasks`, `create_task` (a new task starts as `draft`).
- Views: `project_list`, `task_list`.
- A task carries at least: `project_id, title, scope, owner, status`.
- Status lifecycle for the whole product (only `draft` is used now, the rest come later):
  `draft → submitted → approved/rejected → scheduled → completed`.
- **Everything is multi-tenant: every read/write/list is scoped to the actor's
  `org_id`. Data must never cross orgs.** Each request carries
  `actor = {user_id, org_id, role}`.

Acceptance: a user can list their org's projects and tasks and create a draft task;
nothing from another org is ever visible.

<!-- tags: explicit(scaffold, multi_tenant, status enum), latent(schema decomposition) -->
