# PRODUCT

## Overview
OpsBoard is a multi-tenant team task-operations app. Teams are organised into
**orgs**. Each org has **projects**; each project has **task requests** that
move through a defined lifecycle before being scheduled and completed.

## Multi-tenancy rule (CRITICAL — never relax)
Every read, write, and list is scoped to the actor's `org_id`. Data MUST
NEVER cross org boundaries. The actor is carried on every request:
`{user_id, org_id, role}`. Users and orgs are NOT stored in the DB; they
come exclusively from the request actor.

## Roles
- `member` — default; can create/submit tasks, add comments, read everything
  within their org.
- `approver` — can approve or reject submitted tasks.
- `org_admin` — can do everything an approver can do, plus administrative
  operations.
- Privileged actions (approve, reject) require role `approver` or `org_admin`.

## Task lifecycle (complete — only draft used in S0)
```
draft -> submitted -> approved -> scheduled -> completed
                  -> rejected   (terminal; may be re-drafted in future)
```

## Sessions implemented
- **S0**: scaffold — projects, tasks (draft only), list/create endpoints,
  project_list and task_list views.
