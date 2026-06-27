# S9 — Lock core fields after approval

New policy from the product team:

- **Once a task is `approved` (or any later status — `scheduled`, `completed`), its core
  fields `title`, `scope`, `owner` must no longer be editable.** An `update_task` that tries
  to change any of these on an approved-or-later task must be refused and must not persist
  the change.
- Non-core fields (e.g. `priority`) may still be updated.
- This changes the earlier free-editing behaviour from S1: `update_task` must now check the
  task's status before allowing edits to core fields. The detail view should show those
  fields as locked once the task is approved.

Acceptance: editing `title`/`scope`/`owner` on a `draft` still works; the same edit on an
`approved` task is refused and the stored value is unchanged; `priority` can still change.

<!-- tags: explicit(post_approval_edit: forbidden_fields = title/scope/owner — seeded for conformance) -->
