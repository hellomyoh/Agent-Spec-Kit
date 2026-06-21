# S6 — Comments

Let users discuss a task.

- `add_comment`: attach a comment `{task_id, body}` to a task.
- `list_comments`: list a task's comments.
- Comments follow the same rules as the rest of the app: org-scoped, and you cannot
  comment on / list comments for a task you are not allowed to see (respond as if not found).

Acceptance: a user can comment on a task in their org and read it back; another org cannot
see or reach it.

<!-- tags: latent(reuse multi_tenant + existence-hiding for comments) -->
