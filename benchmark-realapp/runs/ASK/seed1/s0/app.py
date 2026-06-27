"""OpsBoard — app module (Session S0: scaffold).

Exposes:
    make_backend(db, cache) -> backend
    render(view, backend, client_state) -> dict
    seed(backend, spec) -> None
"""
from __future__ import annotations
import sys, os

# ---------------------------------------------------------------------------
# Schema definitions
# ---------------------------------------------------------------------------
TASK_STATUS_ENUM = "draft|submitted|approved|rejected|scheduled|completed"

def _define_schema(db):
    """Declare all tables. Safe to call multiple times (idempotent via guard)."""
    if "projects" in db.tables():
        return  # already initialised

    db.define_table(
        "projects",
        {
            "name":     "str",
            "org_id":   "int",
            "owner_id": "int",
        },
        required=["name", "org_id", "owner_id"],
    )

    db.define_table(
        "tasks",
        {
            "project_id": "ref:projects",
            "org_id":     "int",          # denormalised for fast org-scoped queries
            "title":      "str",
            "scope":      "str",
            "owner":      "int",          # user_id
            "status":     f"enum:{TASK_STATUS_ENUM}",
            "slot":       "str",          # scheduled time slot (nullable)
            "created_by": "int",          # user_id
        },
        required=["project_id", "org_id", "title", "scope", "owner", "status", "created_by"],
    )

    db.define_table(
        "comments",
        {
            "task_id": "ref:tasks",
            "org_id":  "int",
            "author":  "int",   # user_id
            "body":    "str",
        },
        required=["task_id", "org_id", "author", "body"],
    )

    db.define_table(
        "audit",
        {
            "task_id":    "ref:tasks",
            "org_id":     "int",
            "actor_id":   "int",
            "action":     "str",
            "detail":     "str",
        },
        required=["task_id", "org_id", "actor_id", "action", "detail"],
    )


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
DASHBOARD_TTL = 60   # ticks

def _dashboard_key(org_id: int) -> str:
    return f"dashboard:{org_id}"


# ---------------------------------------------------------------------------
# Backend
# ---------------------------------------------------------------------------
class Backend:
    def __init__(self, db, cache):
        self._db = db
        self._cache = cache
        _define_schema(db)

    # ---- public entry point -----------------------------------------------
    def handle(self, request: dict) -> dict:
        endpoint = request.get("endpoint")
        actor    = request.get("actor", {})
        payload  = request.get("payload", {})

        handler = {
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
        }.get(endpoint)

        if handler is None:
            return {"status": 400, "error": f"unknown endpoint {endpoint!r}"}

        try:
            return handler(actor, payload)
        except PermissionError as e:
            return {"status": 403, "error": str(e)}
        except LookupError as e:
            return {"status": 404, "error": str(e)}
        except ValueError as e:
            return {"status": 409, "error": str(e)}
        except Exception as e:
            return {"status": 400, "error": str(e)}

    # ---- helpers -------------------------------------------------------------
    def _require_org(self, actor):
        org_id = actor.get("org_id")
        if not isinstance(org_id, int):
            raise RuntimeError("actor.org_id missing or invalid")
        return org_id

    def _get_task_in_org(self, task_id, org_id):
        task = self._db.get("tasks", task_id)
        if task is None or task["org_id"] != org_id:
            raise LookupError(f"task {task_id} not found")
        return task

    def _get_project_in_org(self, project_id, org_id):
        proj = self._db.get("projects", project_id)
        if proj is None or proj["org_id"] != org_id:
            raise LookupError(f"project {project_id} not found")
        return proj

    def _is_privileged(self, actor):
        return actor.get("role") in ("org_admin", "approver")

    def _audit(self, task_id, org_id, actor_id, action, detail=""):
        self._db.insert("audit", {
            "task_id":  task_id,
            "org_id":   org_id,
            "actor_id": actor_id,
            "action":   action,
            "detail":   detail,
        })

    def _invalidate_dashboard(self, org_id):
        self._cache.invalidate(_dashboard_key(org_id))

    # ---- endpoint handlers ---------------------------------------------------

    def _list_projects(self, actor, payload):
        org_id = self._require_org(actor)
        projects = self._db.query("projects", org_id=org_id)
        return {"status": 200, "data": projects}

    def _list_tasks(self, actor, payload):
        org_id = self._require_org(actor)
        project_id = payload.get("project_id")
        if project_id is not None:
            # validate project belongs to org
            self._get_project_in_org(project_id, org_id)
            tasks = self._db.query("tasks", project_id=project_id, org_id=org_id)
        else:
            tasks = self._db.query("tasks", org_id=org_id)
        return {"status": 200, "data": tasks}

    def _create_task(self, actor, payload):
        org_id = self._require_org(actor)
        project_id = payload.get("project_id")
        title      = payload.get("title")
        scope      = payload.get("scope")
        owner      = payload.get("owner")

        if not isinstance(project_id, int):
            raise RuntimeError("project_id (int) required")
        if not title:
            raise RuntimeError("title required")
        if not scope:
            raise RuntimeError("scope required")
        if not isinstance(owner, int):
            raise RuntimeError("owner (int user_id) required")

        # ensure project is in the same org
        self._get_project_in_org(project_id, org_id)

        task_id = self._db.insert("tasks", {
            "project_id": project_id,
            "org_id":     org_id,
            "title":      title,
            "scope":      scope,
            "owner":      owner,
            "status":     "draft",
            "slot":       None,
            "created_by": actor.get("user_id", 0),
        })

        self._audit(task_id, org_id, actor.get("user_id", 0), "create", f"title={title}")
        self._invalidate_dashboard(org_id)

        return {"status": 200, "data": {"task_id": task_id}}

    def _update_task(self, actor, payload):
        org_id  = self._require_org(actor)
        task_id = payload.get("task_id")
        if not isinstance(task_id, int):
            raise RuntimeError("task_id (int) required")
        task = self._get_task_in_org(task_id, org_id)

        allowed_fields = {"title", "scope", "owner"}
        changes = {k: v for k, v in payload.items() if k in allowed_fields}
        if not changes:
            return {"status": 200, "data": task}

        updated = self._db.update("tasks", task_id, changes)
        self._audit(task_id, org_id, actor.get("user_id", 0), "update", str(changes))
        self._invalidate_dashboard(org_id)
        return {"status": 200, "data": updated}

    def _transition(self, actor, payload, from_status, to_status, action, privileged=False):
        org_id  = self._require_org(actor)
        task_id = payload.get("task_id")
        if not isinstance(task_id, int):
            raise RuntimeError("task_id (int) required")
        if privileged and not self._is_privileged(actor):
            raise PermissionError(f"role {actor.get('role')!r} cannot {action}")
        task = self._get_task_in_org(task_id, org_id)
        if task["status"] != from_status:
            raise ValueError(f"task must be {from_status!r} to {action}, is {task['status']!r}")
        updated = self._db.update("tasks", task_id, {"status": to_status})
        self._audit(task_id, org_id, actor.get("user_id", 0), action)
        self._invalidate_dashboard(org_id)
        return {"status": 200, "data": updated}

    def _submit_task(self, actor, payload):
        return self._transition(actor, payload, "draft", "submitted", "submit")

    def _approve_task(self, actor, payload):
        return self._transition(actor, payload, "submitted", "approved", "approve", privileged=True)

    def _reject_task(self, actor, payload):
        return self._transition(actor, payload, "submitted", "rejected", "reject", privileged=True)

    def _schedule_task(self, actor, payload):
        org_id  = self._require_org(actor)
        task_id = payload.get("task_id")
        slot    = payload.get("slot")
        if not isinstance(task_id, int):
            raise RuntimeError("task_id (int) required")
        if not slot:
            raise RuntimeError("slot required")
        task = self._get_task_in_org(task_id, org_id)
        if task["status"] != "approved":
            raise ValueError(f"task must be approved to schedule, is {task['status']!r}")
        # conflict check: no two tasks in the same org may share a slot
        existing = self._db.query("tasks", org_id=org_id, slot=slot)
        if existing:
            raise ValueError(f"slot {slot!r} already taken")
        updated = self._db.update("tasks", task_id, {"status": "scheduled", "slot": slot})
        self._audit(task_id, org_id, actor.get("user_id", 0), "schedule", f"slot={slot}")
        self._invalidate_dashboard(org_id)
        return {"status": 200, "data": updated}

    def _get_dashboard(self, actor, payload):
        org_id = self._require_org(actor)
        key    = _dashboard_key(org_id)
        cached = self._cache.get(key)
        if cached is not None:
            return {"status": 200, "data": cached}

        tasks = self._db.query("tasks", org_id=org_id)
        counts = {}
        for t in tasks:
            counts[t["status"]] = counts.get(t["status"], 0) + 1

        projects = self._db.query("projects", org_id=org_id)
        data = {
            "project_count": len(projects),
            "task_counts":   counts,
            "total_tasks":   len(tasks),
        }
        self._cache.set(key, data, ttl=DASHBOARD_TTL)
        return {"status": 200, "data": data}

    def _add_comment(self, actor, payload):
        org_id  = self._require_org(actor)
        task_id = payload.get("task_id")
        body    = payload.get("body", "").strip()
        if not isinstance(task_id, int):
            raise RuntimeError("task_id (int) required")
        if not body:
            raise RuntimeError("body required")
        self._get_task_in_org(task_id, org_id)  # verify access
        comment_id = self._db.insert("comments", {
            "task_id": task_id,
            "org_id":  org_id,
            "author":  actor.get("user_id", 0),
            "body":    body,
        })
        return {"status": 200, "data": {"comment_id": comment_id}}

    def _list_comments(self, actor, payload):
        org_id  = self._require_org(actor)
        task_id = payload.get("task_id")
        if not isinstance(task_id, int):
            raise RuntimeError("task_id (int) required")
        self._get_task_in_org(task_id, org_id)
        comments = self._db.query("comments", task_id=task_id, org_id=org_id)
        return {"status": 200, "data": comments}

    def _list_audit(self, actor, payload):
        org_id  = self._require_org(actor)
        task_id = payload.get("task_id")
        if task_id is not None:
            if not isinstance(task_id, int):
                raise RuntimeError("task_id must be int")
            self._get_task_in_org(task_id, org_id)
            entries = self._db.query("audit", task_id=task_id, org_id=org_id)
        else:
            entries = self._db.query("audit", org_id=org_id)
        return {"status": 200, "data": entries}

    def _search_tasks(self, actor, payload):
        org_id     = self._require_org(actor)
        q          = payload.get("q", "").lower().strip()
        status     = payload.get("status")
        project_id = payload.get("project_id")

        tasks = self._db.query("tasks", org_id=org_id)

        if project_id is not None:
            tasks = [t for t in tasks if t["project_id"] == project_id]
        if status is not None:
            tasks = [t for t in tasks if t["status"] == status]
        if q:
            tasks = [t for t in tasks
                     if q in t["title"].lower() or q in t["scope"].lower()]

        return {"status": 200, "data": tasks}


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------

def make_backend(db, cache):
    return Backend(db, cache)


def seed(backend: Backend, spec: dict):
    """Load initial state from public seed spec.
    spec = {"projects": [{"name": str, "org_id": int, "owner_id": int}, ...]}
    """
    for proj in spec.get("projects", []):
        backend._db.insert("projects", {
            "name":     proj["name"],
            "org_id":   proj["org_id"],
            "owner_id": proj["owner_id"],
        })


def render(view: str, backend: Backend, client_state: dict) -> dict:
    """Render a frontend view by calling backend endpoints and assembling the page dict."""
    actor        = client_state.get("actor", {})
    route_params = client_state.get("route_params", {})
    query_params = client_state.get("query_params", {})

    if view == "project_list":
        resp = backend.handle({"endpoint": "list_projects", "actor": actor, "payload": {}})
        return {
            "view":     "project_list",
            "projects": resp.get("data", []),
            "error":    resp.get("error"),
        }

    if view == "task_list":
        project_id = route_params.get("project_id")
        payload = {"project_id": project_id} if project_id is not None else {}
        resp = backend.handle({"endpoint": "list_tasks", "actor": actor, "payload": payload})
        return {
            "view":     "task_list",
            "tasks":    resp.get("data", []),
            "error":    resp.get("error"),
        }

    if view == "task_detail":
        task_id = route_params.get("task_id")
        # list tasks filtered by project, then find the task
        task_resp = backend.handle({
            "endpoint": "list_tasks",
            "actor":    actor,
            "payload":  {},
        })
        tasks   = task_resp.get("data", [])
        task    = next((t for t in tasks if t["id"] == task_id), None)
        comment_resp = backend.handle({
            "endpoint": "list_comments",
            "actor":    actor,
            "payload":  {"task_id": task_id},
        }) if task_id is not None else {"data": []}
        return {
            "view":     "task_detail",
            "task":     task,
            "comments": comment_resp.get("data", []),
            "error":    comment_resp.get("error") or task_resp.get("error"),
        }

    if view == "dashboard":
        resp = backend.handle({"endpoint": "get_dashboard", "actor": actor, "payload": {}})
        return {
            "view":      "dashboard",
            "dashboard": resp.get("data", {}),
            "error":     resp.get("error"),
        }

    if view == "search":
        resp = backend.handle({
            "endpoint": "search_tasks",
            "actor":    actor,
            "payload":  dict(query_params),
        })
        return {
            "view":   "search",
            "tasks":  resp.get("data", []),
            "error":  resp.get("error"),
        }

    return {"view": view, "error": f"unknown view {view!r}"}
