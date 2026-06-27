import importlib.util, os
_p = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "reference", "app.py"))
_s = importlib.util.spec_from_file_location("_ref_for_nc", _p)
_ref = importlib.util.module_from_spec(_s); _s.loader.exec_module(_ref)
from contract import OK, BAD_REQUEST, FORBIDDEN, NOT_FOUND, CONFLICT
render = _ref.render
seed = _ref.seed

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


def make_backend(db, cache):
    return Backend(db, cache)
