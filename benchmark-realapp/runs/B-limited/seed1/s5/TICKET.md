# S5 — Dashboard + caching

Add a dashboard and make the hot path fast.

- `get_dashboard`: returns the actor's org task counts — total and a breakdown by status.
- The dashboard/list path is hit often, so **cache** the dashboard result using the
  provided `cache`.
- **The dashboard must never serve stale numbers.** After any change that affects the
  counts — a new task, a status change (submit/approve/reject), or a scheduling — the next
  `get_dashboard` for that org must reflect it.
- Different orgs must see their own numbers (the cache must not let one org's dashboard
  show another org's data).

Acceptance: dashboard counts are correct immediately after creating/transitioning/
scheduling tasks; org A and org B never see each other's counts.

<!-- tags: explicit(no stale, invalidate on count-affecting changes), latent(cache key must include org) -->
