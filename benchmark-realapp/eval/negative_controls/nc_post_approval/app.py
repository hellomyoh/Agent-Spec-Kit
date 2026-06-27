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
        changes = {k: v for k, v in p.items() if k not in ("task_id", "status")}
        self.db.update("task", t["id"], changes)  # BREAK: no post-approval freeze
        return {"status": OK, "data": self.db.get("task", t["id"]), "error": None}


def make_backend(db, cache):
    return Backend(db, cache)
