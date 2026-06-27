"""Generate negative-control apps: each subclasses the reference and breaks
exactly ONE invariant. Stage -1 requires each to FAIL its targeted check —
proving the checker actually detects that violation. Never given to agents.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

HEADER = '''import importlib.util, os
_p = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "reference", "app.py"))
_s = importlib.util.spec_from_file_location("_ref_for_nc", _p)
_ref = importlib.util.module_from_spec(_s); _s.loader.exec_module(_ref)
from contract import OK, BAD_REQUEST, FORBIDDEN, NOT_FOUND, CONFLICT
render = _ref.render
seed = _ref.seed
'''

CONTROLS = {
# name : (target_invariant, class_body)
"nc_cache_no_invalidate": ("cache_dashboard", '''
class Backend(_ref.Backend):
    def _invalidate_dashboard(self, org_id):
        pass  # BREAK: forget to invalidate -> stale dashboard
'''),
"nc_cache_no_org_key": ("cache_dashboard", '''
class Backend(_ref.Backend):
    def _dash_key(self, org_id):
        return "dashboard:global"  # BREAK: key omits org_id -> cross-org bleed
'''),
"nc_perm_bypass": ("permissions", '''
class Backend(_ref.Backend):
    def _can_approve(self, actor, task):
        return True  # BREAK: anyone can approve
'''),
"nc_existence_403": ("existence_hiding", '''
class Backend(_ref.Backend):
    def _transition(self, actor, task_id, target, privileged=False):
        t = self._task_in_org(actor, task_id)
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        if privileged and not self._can_approve(actor, t):
            return {"status": FORBIDDEN, "data": None, "error": "forbidden"}  # BREAK: 403 leaks existence
        if target not in _ref.TRANSITIONS.get(t["status"], set()):
            return {"status": CONFLICT, "data": None, "error": "bad transition"}
        self.db.update("task", task_id, {"status": target})
        self._audit(actor, task_id, "task_status_changed", f"{t['status']}->{target}")
        self._invalidate_dashboard(actor["org_id"])
        return {"status": OK, "data": self.db.get("task", task_id), "error": None}
'''),
"nc_state_machine": ("state_machine", '''
class Backend(_ref.Backend):
    def _transition(self, actor, task_id, target, privileged=False):
        t = self._task_in_org(actor, task_id)
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        if privileged and not self._can_approve(actor, t):
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        self.db.update("task", task_id, {"status": target})  # BREAK: no legality check
        self._audit(actor, task_id, "sc", f"{t['status']}->{target}")  # keep audit (de-confound from audit_trail)
        self._invalidate_dashboard(actor["org_id"])
        return {"status": OK, "data": self.db.get("task", task_id), "error": None}
'''),
"nc_sched_global": ("scheduling", '''
class Backend(_ref.Backend):
    def _h_schedule_task(self, actor, p):
        t = self._task_in_org(actor, p.get("task_id"))
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        if t["status"] != "approved":
            return {"status": CONFLICT, "data": None, "error": "only approved"}
        slot = p.get("slot")
        # BREAK: global slot uniqueness, ignores project_id
        conflict = [r for r in self.db.query("task", org_id=actor["org_id"], status="scheduled") if r["slot"] == slot]
        if conflict:
            return {"status": CONFLICT, "data": None, "error": "slot taken"}
        self.db.update("task", t["id"], {"status": "scheduled", "slot": slot})
        self._audit(actor, t["id"], "task_scheduled", "")
        self._invalidate_dashboard(actor["org_id"])
        return {"status": OK, "data": self.db.get("task", t["id"]), "error": None}
'''),
"nc_comment_leak": ("multi_tenant", '''
class Backend(_ref.Backend):
    def _h_add_comment(self, actor, p):
        t = self.db.get("task", p.get("task_id"))  # BREAK: no org scoping
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        cid = self.db.insert("comment", {"org_id": actor["org_id"], "task_id": t["id"], "author_id": actor["user_id"], "body": p.get("body", "")})
        return {"status": OK, "data": {"comment_id": cid}, "error": None}
    def _h_list_comments(self, actor, p):
        t = self.db.get("task", p.get("task_id"))  # BREAK: no org scoping
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        return {"status": OK, "data": self.db.query("comment", task_id=t["id"]), "error": None}
'''),
"nc_listfilter_leak": ("multi_tenant", '''
class Backend(_ref.Backend):
    def _h_list_tasks(self, actor, p):
        if p.get("project_id") is not None:
            return {"status": OK, "data": self.db.query("task", project_id=p["project_id"]), "error": None}  # BREAK: drops org scope
        return {"status": OK, "data": self.db.query("task", org_id=actor["org_id"]), "error": None}
'''),
"nc_existence_reject_403": ("existence_hiding", '''
class Backend(_ref.Backend):
    def _transition(self, actor, task_id, target, privileged=False):
        t = self._task_in_org(actor, task_id)
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        if privileged and not self._can_approve(actor, t):
            code = FORBIDDEN if target == "rejected" else NOT_FOUND  # BREAK: reject leaks existence via 403
            return {"status": code, "data": None, "error": "no"}
        if target not in _ref.TRANSITIONS.get(t["status"], set()):
            return {"status": CONFLICT, "data": None, "error": "bad transition"}
        self.db.update("task", task_id, {"status": target})
        self._audit(actor, task_id, "sc", f"{t['status']}->{target}")
        self._invalidate_dashboard(actor["org_id"])
        return {"status": OK, "data": self.db.get("task", task_id), "error": None}
'''),
"nc_freeze_title_only": ("post_approval_edit", '''
class Backend(_ref.Backend):
    def _h_update_task(self, actor, p):
        t = self._task_in_org(actor, p.get("task_id"))
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        changes = {k: v for k, v in p.items() if k != "task_id"}
        if "status" in changes:
            return {"status": CONFLICT, "data": None, "error": "use transition endpoint"}
        if t["status"] in _ref.FROZEN_STATES and "title" in changes:  # BREAK: only title frozen, scope/owner free
            return {"status": CONFLICT, "data": None, "error": "title frozen"}
        bad = [k for k in changes if k not in ("title", "scope", "owner", "slot", "priority")]
        if bad:
            return {"status": BAD_REQUEST, "data": None, "error": "unknown"}
        self.db.update("task", t["id"], changes)
        return {"status": OK, "data": self.db.get("task", t["id"]), "error": None}
'''),
"nc_multi_tenant": ("multi_tenant", '''
class Backend(_ref.Backend):
    def _task_in_org(self, actor, task_id):
        return self.db.get("task", task_id)  # BREAK: ignore org scoping on id access
'''),
"nc_post_approval": ("post_approval_edit", '''
class Backend(_ref.Backend):
    def _h_update_task(self, actor, p):
        t = self._task_in_org(actor, p.get("task_id"))
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        changes = {k: v for k, v in p.items() if k not in ("task_id", "status")}
        self.db.update("task", t["id"], changes)  # BREAK: no post-approval freeze
        return {"status": OK, "data": self.db.get("task", t["id"]), "error": None}
'''),
"nc_scheduling": ("scheduling", '''
class Backend(_ref.Backend):
    def _h_schedule_task(self, actor, p):
        t = self._task_in_org(actor, p.get("task_id"))
        if t is None:
            return {"status": NOT_FOUND, "data": None, "error": "task not found"}
        if t["status"] != "approved":
            return {"status": CONFLICT, "data": None, "error": "only approved"}
        self.db.update("task", t["id"], {"status": "scheduled", "slot": p.get("slot")})  # BREAK: no conflict check
        self._audit(actor, t["id"], "task_scheduled", "")
        self._invalidate_dashboard(actor["org_id"])
        return {"status": OK, "data": self.db.get("task", t["id"]), "error": None}
'''),
"nc_audit": ("audit_trail", '''
class Backend(_ref.Backend):
    def _audit(self, actor, task_id, action, detail=""):
        pass  # BREAK: never write audit
'''),
}


def make_backend_src():
    return "\n\ndef make_backend(db, cache):\n    return Backend(db, cache)\n"


if __name__ == "__main__":
    manifest = {}
    for name, (inv, body) in CONTROLS.items():
        d = os.path.join(HERE, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "app.py"), "w", encoding="utf-8") as f:
            f.write(HEADER + body + make_backend_src())
        manifest[name] = inv
    import json
    with open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    print(f"generated {len(CONTROLS)} negative controls")
    for n, i in manifest.items():
        print(f"  {n} -> {i}")
