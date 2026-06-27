# CACHE_POLICY

The app uses `opscache.Cache` (injected TTL cache). Agents choose keys, TTLs,
and invalidation points. Missing an invalidation = stale read (observable).

## Dashboard cache
- **Key**: `dashboard:{org_id}` (one entry per tenant org)
- **TTL**: 60 ticks
- **Set on**: `get_dashboard` — on miss, compute from DB and cache.
- **Invalidated on**: any write that can change dashboard counts:
  - `create_task`
  - `update_task`
  - `submit_task`
  - `approve_task`
  - `reject_task`
  - `schedule_task`
- **NOT invalidated on**: `add_comment`, `list_*`, `search_tasks` (read-only).

## Rules for future sessions
- Any new endpoint that changes task counts or project counts MUST call
  `_invalidate_dashboard(org_id)`.
- Do NOT cache `list_projects` or `list_tasks` individually (not yet required;
  add only if a performance ticket demands it and document here).
- New cache keys must be documented in this file with key pattern, TTL,
  set-on, and invalidated-on.
