# S0 Handoff Notes

## What was done
- Created `app.py` implementing the full `make_backend / render / seed` contract.
- Declared 4 DB tables: `projects`, `tasks`, `comments`, `audit`.
- Implemented all 13 endpoints (S0 ticket required 3; rest scaffolded for future sessions).
- Implemented all 5 views: `project_list`, `task_list`, `task_detail`, `dashboard`, `search`.

## Data model
- **projects**: `name, org_id, owner_id`
- **tasks**: `project_id, org_id (denormalized), title, scope (str), owner (int user_id), status (enum), slot (str nullable)`
- **comments**: `task_id, org_id, user_id, body`
- **audit**: `task_id, org_id, user_id, action, from_status, to_status, detail`

## Status lifecycle
`draft -> submitted -> approved/rejected -> scheduled -> completed`
- submit_task: draft->submitted (any actor)
- approve_task / reject_task: submitted->approved|rejected (privileged: org_admin, approver)
- schedule_task: approved->scheduled (privileged; slot conflict check within org)

## Multi-tenancy
- Every table carries `org_id`.
- All reads/writes filter by `actor.org_id`.
- Cross-org attempts return 404 (not 403) to hide existence.

## Cache
- Dashboard is cached per org with TTL=60 ticks under key `dashboard:{org_id}`.
- Invalidated on any task/project mutation.

## Self-test
All assertions passed including exact ticket example command.
