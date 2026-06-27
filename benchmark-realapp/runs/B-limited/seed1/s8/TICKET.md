# S8 — Search & filter

Add task search.

- `search_tasks` with optional filters: `q` (case-insensitive substring of title),
  `status`, `project_id`.
- The `search` view drives it from the client query params.
- **Search must respect every existing rule: results are scoped to the actor's org (never
  return another org's tasks) and follow the same visibility rules as the rest of the app.**

Acceptance: filtering by title/status/project returns the right tasks; a search never
returns or reveals tasks from another org.

<!-- tags: explicit(filters), explicit(must keep org scoping — common place to reintroduce a leak) -->
