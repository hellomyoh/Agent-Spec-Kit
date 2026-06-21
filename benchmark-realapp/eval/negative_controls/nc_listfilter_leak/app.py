import importlib.util, os
_p = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "reference", "app.py"))
_s = importlib.util.spec_from_file_location("_ref_for_nc", _p)
_ref = importlib.util.module_from_spec(_s); _s.loader.exec_module(_ref)
from contract import OK, BAD_REQUEST, FORBIDDEN, NOT_FOUND, CONFLICT
render = _ref.render
seed = _ref.seed

class Backend(_ref.Backend):
    def _h_list_tasks(self, actor, p):
        if p.get("project_id") is not None:
            return {"status": OK, "data": self.db.query("task", project_id=p["project_id"]), "error": None}  # BREAK: drops org scope
        return {"status": OK, "data": self.db.query("task", org_id=actor["org_id"]), "error": None}


def make_backend(db, cache):
    return Backend(db, cache)
