"""OpsBoard — shared public interface contract (given to EVERY group).

This is the minimal external API the harness binds tests to. It fixes ONLY the
surface (endpoint names, request/response shape, view names, client_state keys,
and the two entry points the app must expose). It deliberately says NOTHING about
deep policy — data model decomposition, cache keys/TTL, permission placement,
state-machine internals, tenant scoping. Those are the agent's design space and
the substance the hidden oracle measures.

The agent must provide a module `app` exposing:

    make_backend(db, cache) -> backend         # backend.handle(request) -> response
    render(view, backend, client_state) -> dict
    seed(backend, spec) -> None                # load initial state from public spec

Nothing else about internal structure is prescribed.

SEED spec (public format): the harness sets up initial state implementation-agnostically.
    {"projects": [{"name": str, "org_id": int, "owner_id": int}, ...]}
The app's seed() must create those projects so that list_projects (scoped by the
actor's org) returns them. The harness then discovers each project's real id via
list_projects (matching on name) and drives everything else through the endpoints.
Users/orgs are NOT stored — every request carries the actor {user_id, org_id, role}.
"""

# ---- endpoints (names are part of the shared contract; behaviour is not) ----
ENDPOINTS = {
    "list_projects",   # payload: {} -> data: [project,...] scoped to actor.org
    "list_tasks",      # payload: {project_id?} -> data: [task,...]
    "create_task",     # payload: {project_id, title, scope, owner, ...} -> data: {task_id}
    "update_task",     # payload: {task_id, **fields} -> data: {task}
    "submit_task",     # payload: {task_id} -> moves draft->submitted
    "approve_task",    # payload: {task_id} -> submitted->approved (privileged)
    "reject_task",     # payload: {task_id} -> submitted->rejected (privileged)
    "schedule_task",   # payload: {task_id, slot} -> approved->scheduled (no conflict)
    "get_dashboard",   # payload: {} -> data: {counts,...} (cached)
    "add_comment",     # payload: {task_id, body}
    "list_comments",   # payload: {task_id}
    "list_audit",      # payload: {task_id?} -> data: [audit_entry,...]
    "search_tasks",    # payload: {q?, status?, project_id?} -> data: [task,...]
}

# ---- response data shapes (the shared API contract; deep policy stays private) ----
# These fix only the *shape* the frontend/tests consume, not the behaviour:
#   list_projects -> data: [ {"id": int, "name": str, ...}, ... ]
#   list_tasks / search_tasks -> data: [ task, ... ]
#   create_task -> data: {"task_id": int}
#   task object (as returned in lists): at least
#       {"id": int, "project_id": int, "title": str, "scope": str,
#        "owner": int, "status": str, "slot": int, "priority": int}
#   get_dashboard -> data: {"total": int, "by_status": {<status>: int}}
#   list_comments -> data: [ {"id", "task_id", "body", ...}, ... ]
#   list_audit -> data: [ {"task_id": int, ...}, ... ]
TASK_FIELDS = ("id", "project_id", "title", "scope", "owner", "status", "slot", "priority")
DASHBOARD_SHAPE = {"total": int, "by_status": dict}

# ---- views (frontend entry points) ----
VIEWS = {"project_list", "task_list", "task_detail", "dashboard", "search"}

# ---- client state the frontend mock must carry ----
CLIENT_STATE_KEYS = {
    "actor",                    # current user {user_id, org_id, role}
    "route_params",             # e.g. {"task_id": 3}
    "query_params",             # e.g. {"q": "x", "status": "approved"}
    "form_state",               # in-progress form fields
    "view_cache",               # last rendered data per view (client-side staleness)
    "pending_optimistic_actions",
    "last_error",
}

# ---- response status conventions ----
OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403       # actor lacks permission (NOTE: 404 may be required to hide existence)
NOT_FOUND = 404
CONFLICT = 409        # e.g. schedule slot conflict, illegal state transition


def new_client_state(actor):
    return {
        "actor": actor,
        "route_params": {},
        "query_params": {},
        "form_state": {},
        "view_cache": {},
        "pending_optimistic_actions": [],
        "last_error": None,
    }


def validate_request(req: dict):
    if not isinstance(req, dict):
        raise ValueError("request must be a dict")
    if req.get("endpoint") not in ENDPOINTS:
        raise ValueError(f"unknown endpoint {req.get('endpoint')!r}")
    if "actor" not in req or "payload" not in req:
        raise ValueError("request needs 'actor' and 'payload'")
    return True


def validate_response(resp: dict):
    if not isinstance(resp, dict):
        raise ValueError("response must be a dict")
    if "status" not in resp:
        raise ValueError("response needs 'status'")
    return True
