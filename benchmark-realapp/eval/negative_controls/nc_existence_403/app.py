import importlib.util, os
_p = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "reference", "app.py"))
_s = importlib.util.spec_from_file_location("_ref_for_nc", _p)
_ref = importlib.util.module_from_spec(_s); _s.loader.exec_module(_ref)
from contract import OK, BAD_REQUEST, FORBIDDEN, NOT_FOUND, CONFLICT
render = _ref.render
seed = _ref.seed

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


def make_backend(db, cache):
    return Backend(db, cache)
