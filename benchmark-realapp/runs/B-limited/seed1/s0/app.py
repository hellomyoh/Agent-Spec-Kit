"""OpsBoard — app module (Session S0: Scaffold).

Exposes:
    make_backend(db, cache) -> backend
    render(view, backend, client_state) -> dict
    seed(backend, spec) -> None
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "provided"))

from contract import OK, BAD_REQUEST, FORBIDDEN, NOT_FOUND, CONFLICT

# ---------------------------------------------------------------------------
# Schema definition helpers
# ---------------------------------------------------------------------------

def _define_schema(db):
    """Declare all tables once on first backend creation."""
    if "projects" in db.tables():
        return  # already defined

    db.define_table(
        "projects",
        {
            "name":     "str",
            "org_id":   "int",
            "owner_id": "int",
        },
        required=["name", "org_id", "owner_id"],
    )

    # Status lifecycle: draft -> submitted -> approved/rejected -> scheduled -> completed
    db.define_table(
        "tasks",
        {
            "project_id": "ref:projects",
            "org_id":     "int",          # denormalized for fast tenant-scoped queries
            "title":      "str",
            "scope":      "str",
            "owner":      "int",          # user_id of task owner
            "status":     "enum:draft|submitted|approved|rejected|scheduled|completed",
            "slot":       "str",          # scheduled time slot (used later)
        },
        required=["project_id", "org_id", "title", "scope", "owner", "status"],
    )

    db.define_table(
        "comments",
        {
            "task_id": "ref:tasks",
            "org_id":  "int",
            "user_id": "int",
            "body":    "str",
        },
        required=["task_id", "org_id", "user_id", "body"],
    )

    db.define_table(
        "audit",
        {
            "task_id":    "ref:tasks",
            "org_id":     "int",
            "user_id":    "int",
            "action":     "str",
            "from_status":"str",
            "to_status":  "str",
            "detail":     "str",
        },
        required=["task_id", "org_id", "user_id", "action"],
    )


# ---------------------------------------------------------------------------
# Backend
# ---------------------------------------------------------------------------

class Backend:
    def __init__(self, db, cache):
        self._db = db
        self._cache = cache
        _define_schema(db)

    # ---- routing ----

    def handle(self, request: dict) -> dict:
        endpoint = request.get("endpoint")
        actor    = request.get("actor", {})
        payload  = request.get("payload", {})

        handlers = {
            "list_projects": self._list_projects,
            "list_tasks":    self._list_tasks,
            "create_task":   self._create_task,
            "update_task":   self._update_task,
            "submit_task":   self._submit_task,
            "approve_task":  self._approve_task,
            "reject_task":   self._reject_task,
            "schedule_task": self._schedule_task,
            "get_dashboard": self._get_dashboard,
            "add_comment":   self._add_comment,
            "list_comments": self._list_comments,
            "list_audit":    self._list_audit,
            "search_tasks":  self._search_tasks,
        }

        handler = handlers.get(endpoint)
        if handler is None:
            return {"status": BAD_REQUEST, "data": None, "error": f"unknown endpoint: {endpoint}"}

        try:
            return handler(actor, payload)
        except Exception as exc:
            return {"status": BAD_REQUEST, "data": None, "error": str(exc)}

    # ---- helpers ----

    def _ok(self, data):
        return {"status": OK, "data": data, "error": None}

    def _err(self, status, msg):
        return {"status": status, "data": None, "error": msg}

    def _get_project(self, project_id, org_id):
        """Fetch project ensuring it belongs to org_id."""
        p = self._db.get("projects", project_id)
        if p is None or p["org_id"] != org_id:
            return None
        return p

    def _get_task(self, task_id, org_id):
        """Fetch task ensuring it belongs to org_id."""
        t = self._db.get("tasks", task_id)
        if t is None or t["org_id"] != org_id:
            return None
        return t

    def _invalidate_dashboard(self, org_id):
        self._cache.invalidate(f"dashboard:{org_id}")

    def _is_privileged(self, actor):
        return actor.get("role") in ("org_admin", "approver")

    # ---- endpoint handlers ----

    def _list_projects(self, actor, payload):
        org_id = actor.get("org_id")
        if org_id is None:
            return self._err(BAD_REQUEST, "actor missing org_id")
        projects = self._db.query("projects", org_id=org_id)
        return self._ok(projects)

    def _list_tasks(self, actor, payload):
        org_id = actor.get("org_id")
        if org_id is None:
            return self._err(BAD_REQUEST, "actor missing org_id")
        project_id = payload.get("project_id")
        if project_id is not None:
            # Verify project belongs to actor's org
            p = self._get_project(project_id, org_id)
            if p is None:
                return self._err(NOT_FOUND, "project not found")
            tasks = self._db.query("tasks", project_id=project_id, org_id=org_id)
        else:
            tasks = self._db.query("tasks", org_id=org_id)
        return self._ok(tasks)

    def _create_task(self, actor, payload):
        org_id = actor.get("org_id")
        if org_id is None:
            return self._err(BAD_REQUEST, "actor missing org_id")
        project_id = payload.get("project_id")
        if project_id is None:
            return self._err(BAD_REQUEST, "project_id required")
        title = payload.get("title")
        if not title:
            return self._err(BAD_REQUEST, "title required")
        scope = payload.get("scope")
        if scope is None:
            return self._err(BAD_REQUEST, "scope required")
        owner = payload.get("owner", actor.get("user_id"))

        # Verify project belongs to actor's org
        p = self._get_project(project_id, org_id)
        if p is None:
            return self._err(NOT_FOUND, "project not found")

        task_id = self._db.insert("tasks", {
            "project_id": project_id,
            "org_id":     org_id,
            "title":      title,
            "scope":      str(scope),
            "owner":      int(owner),
            "status":     "draft",
            "slot":       None,
        })
        self._invalidate_dashboard(org_id)
        task = self._db.get("tasks", task_id)
        return self._ok({"task_id": task_id, "task": task})

    def _update_task(self, actor, payload):
        org_id = actor.get("org_id")
        task_id = payload.get("task_id")
        if task_id is None:
            return self._err(BAD_REQUEST, "task_id required")
        task = self._get_task(task_id, org_id)
        if task is None:
            return self._err(NOT_FOUND, "task not found")

        # Only draft tasks can be freely updated by owner; admins can update anytime
        if task["status"] != "draft" and not self._is_privileged(actor):
            return self._err(CONFLICT, "only draft tasks can be updated by non-privileged users")

        allowed_fields = {"title", "scope", "owner"}
        changes = {k: v for k, v in payload.items() if k in allowed_fields}
        if not changes:
            return self._err(BAD_REQUEST, "no updatable fields provided")

        # coerce types
        if "owner" in changes:
            changes["owner"] = int(changes["owner"])
        if "scope" in changes:
            changes["scope"] = str(changes["scope"])

        updated = self._db.update("tasks", task_id, changes)
        self._invalidate_dashboard(org_id)
        return self._ok({"task": updated})

    def _transition_task(self, actor, payload, from_status, to_status, privileged=False):
        org_id = actor.get("org_id")
        task_id = payload.get("task_id")
        if task_id is None:
            return self._err(BAD_REQUEST, "task_id required")
        task = self._get_task(task_id, org_id)
        if task is None:
            return self._err(NOT_FOUND, "task not found")
        if privileged and not self._is_privileged(actor):
            return self._err(FORBIDDEN, "insufficient permissions")
        if task["status"] != from_status:
            return self._err(CONFLICT, f"task must be '{from_status}' to perform this action (current: {task['status']})")
        updated = self._db.update("tasks", task_id, {"status": to_status})
        # Audit log
        self._db.insert("audit", {
            "task_id":     task_id,
            "org_id":      org_id,
            "user_id":     actor.get("user_id", 0),
            "action":      f"{from_status}_to_{to_status}",
            "from_status": from_status,
            "to_status":   to_status,
            "detail":      "",
        })
        self._invalidate_dashboard(org_id)
        return self._ok({"task": updated})

    def _submit_task(self, actor, payload):
        return self._transition_task(actor, payload, "draft", "submitted")

    def _approve_task(self, actor, payload):
        return self._transition_task(actor, payload, "submitted", "approved", privileged=True)

    def _reject_task(self, actor, payload):
        return self._transition_task(actor, payload, "submitted", "rejected", privileged=True)

    def _schedule_task(self, actor, payload):
        org_id = actor.get("org_id")
        task_id = payload.get("task_id")
        slot = payload.get("slot")
        if task_id is None:
            return self._err(BAD_REQUEST, "task_id required")
        if not slot:
            return self._err(BAD_REQUEST, "slot required")
        task = self._get_task(task_id, org_id)
        if task is None:
            return self._err(NOT_FOUND, "task not found")
        if not self._is_privileged(actor):
            return self._err(FORBIDDEN, "insufficient permissions")
        if task["status"] != "approved":
            return self._err(CONFLICT, f"task must be 'approved' to schedule (current: {task['status']})")
        # Check slot conflict within this org
        existing = self._db.query("tasks", org_id=org_id, slot=slot, status="scheduled")
        if existing:
            return self._err(CONFLICT, f"slot '{slot}' already taken")
        updated = self._db.update("tasks", task_id, {"status": "scheduled", "slot": str(slot)})
        self._db.insert("audit", {
            "task_id":     task_id,
            "org_id":      org_id,
            "user_id":     actor.get("user_id", 0),
            "action":      "scheduled",
            "from_status": "approved",
            "to_status":   "scheduled",
            "detail":      str(slot),
        })
        self._invalidate_dashboard(org_id)
        return self._ok({"task": updated})

    def _get_dashboard(self, actor, payload):
        org_id = actor.get("org_id")
        if org_id is None:
            return self._err(BAD_REQUEST, "actor missing org_id")
        cache_key = f"dashboard:{org_id}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return self._ok(cached)

        tasks = self._db.query("tasks", org_id=org_id)
        counts = {}
        for t in tasks:
            s = t["status"]
            counts[s] = counts.get(s, 0) + 1

        projects = self._db.query("projects", org_id=org_id)
        data = {
            "project_count": len(projects),
            "task_count":    len(tasks),
            "by_status":     counts,
        }
        self._cache.set(cache_key, data, ttl=60)
        return self._ok(data)

    def _add_comment(self, actor, payload):
        org_id = actor.get("org_id")
        task_id = payload.get("task_id")
        body = payload.get("body")
        if task_id is None:
            return self._err(BAD_REQUEST, "task_id required")
        if not body:
            return self._err(BAD_REQUEST, "body required")
        task = self._get_task(task_id, org_id)
        if task is None:
            return self._err(NOT_FOUND, "task not found")
        comment_id = self._db.insert("comments", {
            "task_id": task_id,
            "org_id":  org_id,
            "user_id": actor.get("user_id", 0),
            "body":    body,
        })
        comment = self._db.get("comments", comment_id)
        return self._ok({"comment_id": comment_id, "comment": comment})

    def _list_comments(self, actor, payload):
        org_id = actor.get("org_id")
        task_id = payload.get("task_id")
        if task_id is None:
            return self._err(BAD_REQUEST, "task_id required")
        task = self._get_task(task_id, org_id)
        if task is None:
            return self._err(NOT_FOUND, "task not found")
        comments = self._db.query("comments", task_id=task_id, org_id=org_id)
        return self._ok(comments)

    def _list_audit(self, actor, payload):
        org_id = actor.get("org_id")
        task_id = payload.get("task_id") if payload else None
        if task_id is not None:
            task = self._get_task(task_id, org_id)
            if task is None:
                return self._err(NOT_FOUND, "task not found")
            entries = self._db.query("audit", task_id=task_id, org_id=org_id)
        else:
            entries = self._db.query("audit", org_id=org_id)
        return self._ok(entries)

    def _search_tasks(self, actor, payload):
        org_id = actor.get("org_id")
        q          = payload.get("q", "").lower() if payload.get("q") else ""
        status     = payload.get("status")
        project_id = payload.get("project_id")

        tasks = self._db.query("tasks", org_id=org_id)
        results = []
        for t in tasks:
            if status and t["status"] != status:
                continue
            if project_id is not None and t["project_id"] != project_id:
                continue
            if q and q not in t["title"].lower() and q not in t["scope"].lower():
                continue
            results.append(t)
        return self._ok(results)


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------

def make_backend(db, cache):
    return Backend(db, cache)


def render(view, backend, client_state):
    """Render a view by calling the appropriate backend endpoints and returning
    a dict suitable for the frontend to display."""
    actor        = client_state.get("actor", {})
    route_params = client_state.get("route_params", {})
    query_params = client_state.get("query_params", {})

    if view == "project_list":
        resp = backend.handle({"endpoint": "list_projects", "actor": actor, "payload": {}})
        return {
            "view":     "project_list",
            "projects": resp.get("data") or [],
            "error":    resp.get("error"),
        }

    elif view == "task_list":
        project_id = route_params.get("project_id")
        payload = {}
        if project_id is not None:
            payload["project_id"] = project_id
        resp = backend.handle({"endpoint": "list_tasks", "actor": actor, "payload": payload})
        return {
            "view":       "task_list",
            "project_id": project_id,
            "tasks":      resp.get("data") or [],
            "error":      resp.get("error"),
        }

    elif view == "task_detail":
        task_id = route_params.get("task_id")
        # list_tasks for the project, find the one task; or search
        resp = backend.handle({
            "endpoint": "search_tasks",
            "actor":    actor,
            "payload":  {},
        })
        tasks = resp.get("data") or []
        task = next((t for t in tasks if t["id"] == task_id), None)

        comments_resp = backend.handle({
            "endpoint": "list_comments",
            "actor":    actor,
            "payload":  {"task_id": task_id},
        }) if task_id is not None else {"data": []}

        return {
            "view":     "task_detail",
            "task":     task,
            "comments": comments_resp.get("data") or [],
            "error":    resp.get("error"),
        }

    elif view == "dashboard":
        resp = backend.handle({"endpoint": "get_dashboard", "actor": actor, "payload": {}})
        return {
            "view":      "dashboard",
            "dashboard": resp.get("data") or {},
            "error":     resp.get("error"),
        }

    elif view == "search":
        resp = backend.handle({
            "endpoint": "search_tasks",
            "actor":    actor,
            "payload":  {
                "q":         query_params.get("q"),
                "status":    query_params.get("status"),
                "project_id": query_params.get("project_id"),
            },
        })
        return {
            "view":   "search",
            "tasks":  resp.get("data") or [],
            "query":  query_params,
            "error":  resp.get("error"),
        }

    else:
        return {"view": view, "error": f"unknown view: {view}"}


def seed(backend, spec):
    """Load initial state from the public seed spec.

    spec format: {"projects": [{"name": str, "org_id": int, "owner_id": int}, ...]}
    """
    for p in spec.get("projects", []):
        backend._db.insert("projects", {
            "name":     p["name"],
            "org_id":   p["org_id"],
            "owner_id": p["owner_id"],
        })
