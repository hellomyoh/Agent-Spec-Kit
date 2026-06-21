import importlib.util, os
_p = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "reference", "app.py"))
_s = importlib.util.spec_from_file_location("_ref_for_nc", _p)
_ref = importlib.util.module_from_spec(_s); _s.loader.exec_module(_ref)
from contract import OK, BAD_REQUEST, FORBIDDEN, NOT_FOUND, CONFLICT
render = _ref.render
seed = _ref.seed

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


def make_backend(db, cache):
    return Backend(db, cache)
