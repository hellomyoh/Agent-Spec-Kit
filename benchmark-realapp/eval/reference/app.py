"""OpsBoard REFERENCE implementation (S0-S9) — eval-only, never given to agents.

A correct app that satisfies every oracle invariant. Used in Stage -1 to prove
the hidden tests are passable and to anchor the negative controls. Built strictly
on the provided db/cache primitives and the shared contract.

actor = {"user_id": int, "org_id": int, "role": "org_admin"|"project_owner"|"member"}
"""
from contract import OK, BAD_REQUEST, FORBIDDEN, NOT_FOUND, CONFLICT, validate_request

TRANSITIONS = {
    "draft": {"submitted"}, "submitted": {"approved", "rejected"},
    "approved": {"scheduled"}, "rejected": set(),
    "scheduled": {"completed"}, "completed": set(),
}
FORBIDDEN_AFTER_APPROVAL = {"title", "scope", "owner"}
FROZEN_STATES = {"approved", "scheduled", "completed"}


def _schema(db):
    db.define_table("project", {"org_id": "int", "name": "str", "owner_id": "int"},
                    required=["org_id", "name", "owner_id"])
    db.define_table("task", {
        "org_id": "int", "project_id": "ref:project", "title": "str", "scope": "str",
        "owner": "int", "status": "enum:draft|submitted|approved|rejected|scheduled|completed",
        "slot": "int", "priority": "int",
    }, required=["org_id", "project_id", "title", "status"])
    db.define_table("comment", {"org_id": "int", "task_id": "ref:task",
                                "author_id": "int", "body": "str"},
                    required=["org_id", "task_id", "author_id", "body"])
    db.define_table("audit", {"org_id": "int", "task_id": "int", "action": "str",
                              "actor_id": "int", "detail": "str"},
                    required=["org_id", "task_id", "action", "actor_id"])


class Backend:
    def __init__(self, db, cache):
        self.db, self.cache = db, cache
        _schema(db)

    # ---- helpers ----
    def _audit(self, actor, task_id, action, detail=""):
        self.db.insert("audit", {"org_id": actor["org_id"], "task_id": task_id,
                                  "action": action, "actor_id": actor["user_id"],
                                  "detail": detail})

    def _task_in_org(self, actor, task_id):
        """Return task only if it exists AND belongs to actor's org; else None
        (caller maps None -> 404, hiding existence)."""
        t = self.db.get("task", task_id)
        if t is None or t["org_id"] != actor["org_id"]:
            return None
        return t

    def _can_approve(self, actor, task):
        if actor["role"] == "org_admin":
            return True
        if actor["role"] == "project_owner":
            proj = self.db.get("project", task["project_id"])
            return proj is not None and proj["owner_id"] == actor["user_id"]
        return False

    def _dash_key(self, org_id):
        return f"dashboard:org={org_id}"

    def _invalidate_dashboard(self, org_id):
        self.cache.invalidate(self._dash_key(org_id))

    # ---- dispatch ----
    def handle(self, req):
        try:
            validate_request(req)
        except ValueError as e:
            return {"status": BAD_REQUEST, "data": None, "error": str(e)}
        ep, actor, p = req["endpoint"], req["actor"], req.get("payload") or {}
        return getattr(self, f"_h_{ep}")(actor, p)

    def _h_list_projects(self, actor, p):
        return {"status": OK, "data": self.db.query("project", org_id=actor["org_id"]), "error": None}

    def _h_list_tasks(self, actor, p):
        rows = self.db.query("task", org_id=actor["org_id"])
        if p.get("project_id") is not None:
            rows = [r for r in rows if r["project_id"] == p["project_id"]]
        return {"status": OK, "data": rows, "error": None}

    def _h_create_task(self, actor, p):
        proj = self.db.get("project", p.get("project_id"))
        if proj is None or proj["org_id"] != actor["org_id"]:
            return {"status": NOT_FOUND, "data": None, "error": "project not found"}
        tid = self.db.insert("task", {
            "org_id": actor["org_id"], "project_id": p["project_id"],
            "title": p.get("title", ""), "scope": p.get("scope", ""),
            "owner": p.get("owner", actor["user_id"]), "status": "draft",
            "slot": p.get("slot", 0), "priority": p.get("priority", 0),
        })
        self._audit(actor, tid, "task_created")
        self._invalidate_dashboard(actor["org_id"])
        return {"status": OK, "data": {"task_id": tid}, "error": None}

    def _h_update_task(self, actor, p):
        t = self._task_in_org(actor, p.get("task_id"))
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        changes = {k: v for k, v in p.items() if k != "task_id"}
        # status may only change through dedicated endpoints
        if "status" in changes:
            return {"status": CONFLICT, "data": None, "error": "use transition endpoint"}
        if t["status"] in FROZEN_STATES and (set(changes) & FORBIDDEN_AFTER_APPROVAL):
            return {"status": CONFLICT, "data": None,
                    "error": "core fields frozen after approval"}
        bad = [k for k in changes if k not in ("title", "scope", "owner", "slot", "priority")]
        if bad:
            return {"status": BAD_REQUEST, "data": None, "error": f"unknown field {bad}"}
        self.db.update("task", t["id"], changes)
        return {"status": OK, "data": self.db.get("task", t["id"]), "error": None}

    def _transition(self, actor, task_id, target, privileged=False):
        t = self._task_in_org(actor, task_id)
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        if privileged and not self._can_approve(actor, t):
            # hide existence from non-privileged: 404, not 403
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        if target not in TRANSITIONS.get(t["status"], set()):
            return {"status": CONFLICT, "data": None,
                    "error": f"cannot go {t['status']} -> {target}"}
        self.db.update("task", task_id, {"status": target})
        self._audit(actor, task_id, "task_status_changed", f"{t['status']}->{target}")
        self._invalidate_dashboard(actor["org_id"])
        return {"status": OK, "data": self.db.get("task", task_id), "error": None}

    def _h_submit_task(self, actor, p):
        return self._transition(actor, p.get("task_id"), "submitted")

    def _h_approve_task(self, actor, p):
        return self._transition(actor, p.get("task_id"), "approved", privileged=True)

    def _h_reject_task(self, actor, p):
        return self._transition(actor, p.get("task_id"), "rejected", privileged=True)

    def _h_schedule_task(self, actor, p):
        t = self._task_in_org(actor, p.get("task_id"))
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        if t["status"] != "approved":
            return {"status": CONFLICT, "data": None, "error": "only approved -> scheduled"}
        slot = p.get("slot")
        conflict = [r for r in self.db.query("task", org_id=actor["org_id"],
                                             project_id=t["project_id"], status="scheduled")
                    if r["slot"] == slot]
        if conflict:
            return {"status": CONFLICT, "data": None, "error": "slot taken"}
        self.db.update("task", t["id"], {"status": "scheduled", "slot": slot})
        self._audit(actor, t["id"], "task_scheduled", f"slot={slot}")
        self._invalidate_dashboard(actor["org_id"])
        return {"status": OK, "data": self.db.get("task", t["id"]), "error": None}

    def _h_get_dashboard(self, actor, p):
        key = self._dash_key(actor["org_id"])
        cached = self.cache.get(key)
        if cached is not None:
            return {"status": OK, "data": cached, "error": None}
        tasks = self.db.query("task", org_id=actor["org_id"])
        counts = {}
        for s in TRANSITIONS:
            counts[s] = sum(1 for t in tasks if t["status"] == s)
        data = {"total": len(tasks), "by_status": counts}
        self.cache.set(key, data, ttl=300)
        return {"status": OK, "data": data, "error": None}

    def _h_add_comment(self, actor, p):
        t = self._task_in_org(actor, p.get("task_id"))
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        cid = self.db.insert("comment", {"org_id": actor["org_id"], "task_id": t["id"],
                                         "author_id": actor["user_id"], "body": p.get("body", "")})
        return {"status": OK, "data": {"comment_id": cid}, "error": None}

    def _h_list_comments(self, actor, p):
        t = self._task_in_org(actor, p.get("task_id"))
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        return {"status": OK, "data": self.db.query("comment", org_id=actor["org_id"],
                                                     task_id=t["id"]), "error": None}

    def _h_list_audit(self, actor, p):
        rows = self.db.query("audit", org_id=actor["org_id"])
        if p.get("task_id") is not None:
            rows = [r for r in rows if r["task_id"] == p["task_id"]]
        return {"status": OK, "data": rows, "error": None}

    def _h_search_tasks(self, actor, p):
        rows = self.db.query("task", org_id=actor["org_id"])
        q = (p.get("q") or "").lower()
        if q:
            rows = [r for r in rows if q in (r.get("title", "") or "").lower()]
        if p.get("status"):
            rows = [r for r in rows if r["status"] == p["status"]]
        if p.get("project_id") is not None:
            rows = [r for r in rows if r["project_id"] == p["project_id"]]
        return {"status": OK, "data": rows, "error": None}


def make_backend(db, cache):
    return Backend(db, cache)


def seed(backend, spec):
    for pr in spec.get("projects", []):
        backend.db.insert("project", {"org_id": pr["org_id"], "name": pr["name"],
                                      "owner_id": pr["owner_id"]})


def render(view, backend, client_state):
    actor = client_state["actor"]
    out = {"view": view, "data": None, "available_actions": [], "disabled_fields": [],
           "error": None}
    if view == "project_list":
        r = backend.handle({"endpoint": "list_projects", "actor": actor, "payload": {}})
        out["data"] = r["data"]
    elif view == "task_list":
        r = backend.handle({"endpoint": "list_tasks", "actor": actor,
                            "payload": {"project_id": client_state["route_params"].get("project_id")}})
        out["data"] = r["data"]
        client_state["view_cache"]["task_list"] = r["data"]
    elif view == "search":
        r = backend.handle({"endpoint": "search_tasks", "actor": actor,
                            "payload": client_state["query_params"]})
        out["data"] = r["data"]
    elif view == "dashboard":
        r = backend.handle({"endpoint": "get_dashboard", "actor": actor, "payload": {}})
        out["data"] = r["data"]
        client_state["view_cache"]["dashboard"] = r["data"]
    elif view == "task_detail":
        tid = client_state["route_params"].get("task_id")
        r = backend.handle({"endpoint": "list_tasks", "actor": actor, "payload": {}})
        task = next((t for t in (r["data"] or []) if t["id"] == tid), None)
        if task is None:
            out["error"] = "not_found"
            out["data"] = None
            return out
        out["data"] = task
        # action visibility must match what the API will actually allow
        st = task["status"]
        can_priv = actor["role"] == "org_admin" or actor["role"] == "project_owner"
        if st == "draft":
            out["available_actions"].append("submit")
        if st == "submitted" and can_priv:
            out["available_actions"] += ["approve", "reject"]
        if st == "approved":
            out["available_actions"].append("schedule")
        if st in FROZEN_STATES:
            out["disabled_fields"] = sorted(FORBIDDEN_AFTER_APPROVAL)
    else:
        out["error"] = f"unknown view {view}"
    out["last_error"] = client_state.get("last_error")
    return out
