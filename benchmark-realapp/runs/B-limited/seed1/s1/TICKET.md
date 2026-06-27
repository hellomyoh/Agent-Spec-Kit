# S1 — Create & edit task requests

Flesh out task authoring.

- `create_task` (already started) takes `project_id, title, scope, owner` and creates a
  `draft` task in the actor's org. `title` is required.
- `update_task` lets a user edit a task's fields (e.g. `title, scope, owner, priority`)
  while it is being worked on.
- The task list / detail views should reflect edits.

Acceptance: create a draft, edit its title/scope, see the change in `list_tasks`.

<!-- tags: explicit(create/edit fields), latent(which fields editable) -->
