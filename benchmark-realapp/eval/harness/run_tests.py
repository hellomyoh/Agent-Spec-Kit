"""OpsBoard hidden E2E test battery (eval-only, never in agent workspace).

Behaviourally verifies every oracle invariant through the public surface
(handle/render) of ANY app implementing the shared contract. Implementation
internals are never inspected. Each check is tagged with its invariant.

Hardened after independent adversarial review (C1-C4, I1-I5): scheduling is
tested cross-project; audit is checked semantically (grows per transition, none
for refused); caching is required + exact staleness; existence-hiding and
multi-tenant are parametrised across endpoints; exact status codes asserted.

Usage: from run_tests import run_all; res = run_all("/path/to/app_dir")
"""
from __future__ import annotations
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROVIDED = os.path.normpath(os.path.join(HERE, "..", "..", "provided"))

SEED_SPEC = {"projects": [
    {"name": "Alpha", "org_id": 1, "owner_id": 20},
    {"name": "Beta",  "org_id": 1, "owner_id": 21},
    {"name": "Gamma", "org_id": 2, "owner_id": 40},
]}
ADMIN1 = {"user_id": 10, "org_id": 1, "role": "org_admin"}
OWNER_A = {"user_id": 20, "org_id": 1, "role": "project_owner"}
OWNER_B = {"user_id": 21, "org_id": 1, "role": "project_owner"}
MEMBER1 = {"user_id": 11, "org_id": 1, "role": "member"}
ADMIN2 = {"user_id": 30, "org_id": 2, "role": "org_admin"}

_counter = [0]


def _load(app_dir):
    for p in (PROVIDED, app_dir):
        if p not in sys.path:
            sys.path.insert(0, p)
    _counter[0] += 1
    name = f"_app_{_counter[0]}"
    spec = importlib.util.spec_from_file_location(name, os.path.join(app_dir, "app.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fresh(app):
    from opsdb import Database
    from opscache import Cache, Clock
    db, cache = Database(), Cache(Clock())
    be = app.make_backend(db, cache)
    app.seed(be, SEED_SPEC)
    return be, db, cache


def _proj_id(be, actor, name):
    r = be.handle({"endpoint": "list_projects", "actor": actor, "payload": {}})
    for p in (r.get("data") or []):
        if p.get("name") == name:
            return p["id"]
    return None


def _create(be, actor, pid, title="t", scope="s", owner=None):
    r = be.handle({"endpoint": "create_task", "actor": actor,
                   "payload": {"project_id": pid, "title": title, "scope": scope,
                               "owner": owner or actor["user_id"]}})
    return (r.get("data") or {}).get("task_id"), r


def _status(be, actor, tid):
    r = be.handle({"endpoint": "list_tasks", "actor": actor, "payload": {}})
    t = next((x for x in (r.get("data") or []) if x.get("id") == tid), None)
    return t.get("status") if t else None


def _approved(be, actor, pid):
    t, _ = _create(be, actor, pid)
    be.handle({"endpoint": "submit_task", "actor": actor, "payload": {"task_id": t}})
    be.handle({"endpoint": "approve_task", "actor": actor, "payload": {"task_id": t}})
    return t


def _audit_count(be, actor, tid):
    r = be.handle({"endpoint": "list_audit", "actor": actor, "payload": {"task_id": tid}})
    return len(r.get("data") or [])


class Checks:
    def __init__(self, app):
        self.app = app
        self.results = []

    def ok(self, inv, name, cond, detail=""):
        self.results.append({"invariant": inv, "name": name,
                             "passed": bool(cond), "detail": detail})

    # ---------- functional happy path ----------
    def functional(self):
        be, _db, _c = _fresh(self.app)
        pid = _proj_id(be, ADMIN1, "Alpha")
        self.ok("functional", "list_projects_scoped", pid is not None)
        tid, r = _create(be, MEMBER1, pid, title="hello")
        self.ok("functional", "create_task", r["status"] == 200 and tid is not None)
        lst = be.handle({"endpoint": "list_tasks", "actor": MEMBER1, "payload": {}})
        self.ok("functional", "task_listed", any(t["id"] == tid for t in (lst.get("data") or [])))
        up = be.handle({"endpoint": "update_task", "actor": MEMBER1,
                        "payload": {"task_id": tid, "title": "hello2"}})
        self.ok("functional", "update_draft", up["status"] == 200)
        sub = be.handle({"endpoint": "submit_task", "actor": MEMBER1, "payload": {"task_id": tid}})
        self.ok("functional", "submit", sub["status"] == 200 and _status(be, ADMIN1, tid) == "submitted")
        ap = be.handle({"endpoint": "approve_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        self.ok("functional", "approve_admin", ap["status"] == 200 and _status(be, ADMIN1, tid) == "approved")
        sc = be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": tid, "slot": 1}})
        self.ok("functional", "schedule", sc["status"] == 200 and _status(be, ADMIN1, tid) == "scheduled")

    # ---------- state machine (full graph, exact 409) ----------
    def state_machine(self):
        be, _db, _c = _fresh(self.app)
        pid = _proj_id(be, ADMIN1, "Alpha")
        tid, _ = _create(be, ADMIN1, pid)
        r = be.handle({"endpoint": "approve_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        self.ok("state_machine", "no_draft_to_approved", r["status"] == 409 and _status(be, ADMIN1, tid) == "draft")
        be.handle({"endpoint": "submit_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        r = be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": tid, "slot": 1}})
        self.ok("state_machine", "no_submitted_to_scheduled", r["status"] == 409 and _status(be, ADMIN1, tid) == "submitted")
        be.handle({"endpoint": "approve_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        r = be.handle({"endpoint": "reject_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        self.ok("state_machine", "no_approved_to_rejected", r["status"] == 409 and _status(be, ADMIN1, tid) == "approved")
        r = be.handle({"endpoint": "update_task", "actor": ADMIN1, "payload": {"task_id": tid, "status": "completed"}})
        self.ok("state_machine", "no_status_via_update", _status(be, ADMIN1, tid) == "approved")
        # rejected is terminal: cannot approve a rejected task
        tr, _ = _create(be, ADMIN1, pid)
        be.handle({"endpoint": "submit_task", "actor": ADMIN1, "payload": {"task_id": tr}})
        be.handle({"endpoint": "reject_task", "actor": ADMIN1, "payload": {"task_id": tr}})
        r = be.handle({"endpoint": "approve_task", "actor": ADMIN1, "payload": {"task_id": tr}})
        self.ok("state_machine", "rejected_terminal", r["status"] == 409 and _status(be, ADMIN1, tr) == "rejected")
        # scheduled cannot go back to submitted
        ts = _approved(be, ADMIN1, pid)
        be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": ts, "slot": 77}})
        r = be.handle({"endpoint": "submit_task", "actor": ADMIN1, "payload": {"task_id": ts}})
        self.ok("state_machine", "scheduled_no_resubmit", r["status"] == 409 and _status(be, ADMIN1, ts) == "scheduled")

    # ---------- permissions + existence hiding (parametrised, exact 404) ----------
    def permissions(self):
        be, _db, _c = _fresh(self.app)
        pid = _proj_id(be, ADMIN1, "Alpha")
        tid, _ = _create(be, MEMBER1, pid)
        be.handle({"endpoint": "submit_task", "actor": MEMBER1, "payload": {"task_id": tid}})
        r = be.handle({"endpoint": "approve_task", "actor": MEMBER1, "payload": {"task_id": tid}})
        self.ok("permissions", "member_cannot_approve", r["status"] != 200 and _status(be, ADMIN1, tid) == "submitted")
        self.ok("existence_hiding", "member_approve_404", r["status"] == 404)
        rr = be.handle({"endpoint": "reject_task", "actor": MEMBER1, "payload": {"task_id": tid}})
        self.ok("existence_hiding", "member_reject_404", rr["status"] == 404 and _status(be, ADMIN1, tid) == "submitted")
        r = be.handle({"endpoint": "approve_task", "actor": OWNER_B, "payload": {"task_id": tid}})
        self.ok("permissions", "wrong_owner_cannot_approve", r["status"] != 200 and _status(be, ADMIN1, tid) == "submitted")
        r = be.handle({"endpoint": "approve_task", "actor": OWNER_A, "payload": {"task_id": tid}})
        self.ok("permissions", "right_owner_can_approve", r["status"] == 200 and _status(be, ADMIN1, tid) == "approved")

    # ---------- multi-tenant isolation (parametrised across endpoints) ----------
    def multi_tenant(self):
        be, _db, _c = _fresh(self.app)
        pid1 = _proj_id(be, ADMIN1, "Alpha")
        tid, _ = _create(be, ADMIN1, pid1, title="secret1")
        # list_projects must not leak org2's Gamma to org1
        pl = be.handle({"endpoint": "list_projects", "actor": ADMIN1, "payload": {}})
        self.ok("multi_tenant", "list_projects_no_cross_org",
                all(p.get("name") != "Gamma" for p in (pl.get("data") or [])))
        lst2 = be.handle({"endpoint": "list_tasks", "actor": ADMIN2, "payload": {}})
        self.ok("multi_tenant", "list_no_cross_org", all(t["id"] != tid for t in (lst2.get("data") or [])))
        # org2 listing org1's project id must not leak that project's tasks
        flt = be.handle({"endpoint": "list_tasks", "actor": ADMIN2, "payload": {"project_id": pid1}})
        self.ok("multi_tenant", "list_foreign_project_no_leak", all(t["id"] != tid for t in (flt.get("data") or [])))
        r = be.handle({"endpoint": "update_task", "actor": ADMIN2, "payload": {"task_id": tid, "title": "x"}})
        title_now = next((t["title"] for t in be.handle({"endpoint": "list_tasks", "actor": ADMIN1, "payload": {}}).get("data") if t["id"] == tid), None)
        self.ok("multi_tenant", "mutate_cross_org_404", r["status"] == 404 and title_now == "secret1",
                f"status={r['status']} title={title_now}")
        r = be.handle({"endpoint": "approve_task", "actor": ADMIN2, "payload": {"task_id": tid}})
        self.ok("multi_tenant", "approve_cross_org_blocked", r["status"] != 200)
        # comments must be org-scoped (read + write)
        cw = be.handle({"endpoint": "add_comment", "actor": ADMIN2, "payload": {"task_id": tid, "body": "leak"}})
        self.ok("existence_hiding", "crossorg_comment_404", cw["status"] == 404)
        cr = be.handle({"endpoint": "list_comments", "actor": ADMIN2, "payload": {"task_id": tid}})
        leaked = cr["status"] == 200 and (cr.get("data") or [])
        self.ok("multi_tenant", "comments_no_cross_org", cr["status"] == 404 or not leaked)
        sr = be.handle({"endpoint": "search_tasks", "actor": ADMIN2, "payload": {"q": "secret1"}})
        self.ok("multi_tenant", "search_no_cross_org", all(t["id"] != tid for t in (sr.get("data") or [])))
        be.handle({"endpoint": "submit_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        au = be.handle({"endpoint": "list_audit", "actor": ADMIN2, "payload": {}})
        self.ok("multi_tenant", "audit_no_cross_org", all(a.get("task_id") != tid for a in (au.get("data") or [])))

    # ---------- scheduling (cross-project slot scoping) ----------
    def scheduling(self):
        be, _db, _c = _fresh(self.app)
        pid_a = _proj_id(be, ADMIN1, "Alpha")
        pid_b = _proj_id(be, ADMIN1, "Beta")
        t1 = _approved(be, ADMIN1, pid_a)
        r = be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": t1, "slot": 5}})
        self.ok("scheduling", "schedule_approved_ok", r["status"] == 200)
        t2 = _approved(be, ADMIN1, pid_a)
        r = be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": t2, "slot": 5}})
        self.ok("scheduling", "no_slot_conflict_same_project", r["status"] == 409 and _status(be, ADMIN1, t2) == "approved")
        r = be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": t2, "slot": 6}})
        self.ok("scheduling", "other_slot_ok", r["status"] == 200)
        # CROSS-PROJECT: same slot number in a different project must be allowed
        t3 = _approved(be, ADMIN1, pid_b)
        r = be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": t3, "slot": 5}})
        self.ok("scheduling", "crossproject_same_slot_ok", r["status"] == 200 and _status(be, ADMIN1, t3) == "scheduled")
        # non-approved cannot schedule
        td, _ = _create(be, ADMIN1, pid_a)
        r = be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": td, "slot": 9}})
        self.ok("scheduling", "non_approved_no_schedule", r["status"] == 409)

    # ---------- cache correctness (must cache; exact staleness) ----------
    def cache(self):
        be, _db, cache = _fresh(self.app)
        pid = _proj_id(be, ADMIN1, "Alpha")

        def dash(actor):
            d = be.handle({"endpoint": "get_dashboard", "actor": actor, "payload": {}}).get("data")
            return d if isinstance(d, dict) else {}

        def sub_count(d):
            return (d.get("by_status") or {}).get("submitted", 0)

        _create(be, ADMIN1, pid)
        d0 = dash(ADMIN1)
        self.ok("cache_dashboard", "dashboard_is_cached", cache.stats["sets"] >= 1,
                f"cache sets={cache.stats['sets']}")
        base = d0.get("total")
        _create(be, ADMIN1, pid)
        d1 = dash(ADMIN1)
        self.ok("cache_dashboard", "no_stale_after_create",
                base is not None and d1.get("total") == base + 1, f"{base}->{d1.get('total')}")
        tid, _ = _create(be, ADMIN1, pid)
        before = sub_count(dash(ADMIN1))
        be.handle({"endpoint": "submit_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        after = sub_count(dash(ADMIN1))
        self.ok("cache_dashboard", "no_stale_after_status", after == before + 1, f"{before}->{after}")
        d_org2 = dash(ADMIN2)
        self.ok("cache_dashboard", "org_scoped_key", d_org2.get("total") == 0, f"org2 total={d_org2.get('total')}")

    # ---------- post-approval edit freeze (all core fields, all frozen states) ----------
    def post_approval(self):
        be, _db, _c = _fresh(self.app)
        pid = _proj_id(be, ADMIN1, "Alpha")

        def field_of(tid, field):
            for t in (be.handle({"endpoint": "list_tasks", "actor": ADMIN1, "payload": {}}).get("data") or []):
                if t.get("id") == tid:
                    return t.get(field)
            return None

        def frozen_check(state_label, make_state):
            for field, val in (("title", "hacked"), ("scope", "hackedscope"), ("owner", 999)):
                tid = make_state()
                orig = field_of(tid, field)
                r = be.handle({"endpoint": "update_task", "actor": ADMIN1, "payload": {"task_id": tid, field: val}})
                cur = field_of(tid, field)
                self.ok("post_approval_edit", f"{field}_frozen_{state_label}",
                        r["status"] != 200 and cur == orig, f"status={r['status']} {orig!r}->{cur!r}")

        frozen_check("approved", lambda: _approved(be, ADMIN1, pid))

        def make_scheduled():
            t = _approved(be, ADMIN1, pid)
            ntasks = len(be.handle({"endpoint": "list_tasks", "actor": ADMIN1, "payload": {}}).get("data") or [])
            be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": t, "slot": 200 + ntasks}})
            return t
        frozen_check("scheduled", make_scheduled)
        # non-core field still editable after approval
        tid = _approved(be, ADMIN1, pid)
        r2 = be.handle({"endpoint": "update_task", "actor": ADMIN1, "payload": {"task_id": tid, "priority": 9}})
        self.ok("post_approval_edit", "noncore_editable", r2["status"] == 200)

    # ---------- audit trail (semantic: grows per transition, none for refused) ----------
    def audit(self):
        be, _db, _c = _fresh(self.app)
        pid = _proj_id(be, ADMIN1, "Alpha")
        tid, _ = _create(be, ADMIN1, pid)
        be.handle({"endpoint": "submit_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        c_sub = _audit_count(be, ADMIN1, tid)
        self.ok("audit_trail", "status_change_audited", c_sub >= 1, f"after submit={c_sub}")
        be.handle({"endpoint": "approve_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        c_app = _audit_count(be, ADMIN1, tid)
        self.ok("audit_trail", "audit_grows_per_transition", c_app > c_sub, f"{c_sub}->{c_app}")
        be.handle({"endpoint": "schedule_task", "actor": ADMIN1, "payload": {"task_id": tid, "slot": 3}})
        c_sch = _audit_count(be, ADMIN1, tid)
        self.ok("audit_trail", "schedule_audited", c_sch > c_app, f"{c_app}->{c_sch}")
        # acting on a NON-EXISTENT task is refused (404) and must add no audit anywhere
        # (refusal-by-absence is independent of every other invariant -> de-confounded)
        org_before = len(be.handle({"endpoint": "list_audit", "actor": ADMIN1, "payload": {}}).get("data") or [])
        be.handle({"endpoint": "approve_task", "actor": ADMIN1, "payload": {"task_id": 999999}})
        org_after = len(be.handle({"endpoint": "list_audit", "actor": ADMIN1, "payload": {}}).get("data") or [])
        self.ok("audit_trail", "no_audit_for_refused", org_after == org_before, f"{org_before}->{org_after}")

    # ---------- cross-layer completeness (E2E through FE render) ----------
    def cross_layer(self):
        be, _db, _c = _fresh(self.app)
        from contract import new_client_state
        pid = _proj_id(be, ADMIN1, "Alpha")
        cs = new_client_state(ADMIN1)
        cs["route_params"] = {"project_id": pid}
        d0 = (self.app.render("dashboard", be, cs).get("data") or {}).get("total")
        _create(be, ADMIN1, pid)
        d1 = (self.app.render("dashboard", be, cs).get("data") or {}).get("total")
        self.ok("cross_layer", "fe_dashboard_reflects_create", d0 is not None and d1 == d0 + 1, f"{d0}->{d1}")
        tid, _ = _create(be, MEMBER1, pid)
        be.handle({"endpoint": "submit_task", "actor": MEMBER1, "payload": {"task_id": tid}})
        cs_m = new_client_state(MEMBER1)
        cs_m["route_params"] = {"task_id": tid}
        view = self.app.render("task_detail", be, cs_m)
        fe_hides = "approve" not in view.get("available_actions", [])
        api_blocks = be.handle({"endpoint": "approve_task", "actor": MEMBER1,
                                "payload": {"task_id": tid}})["status"] != 200
        self.ok("cross_layer", "perm_fe_api_consistent", fe_hides and api_blocks,
                f"fe_hides={fe_hides} api_blocks={api_blocks}")
        be.handle({"endpoint": "approve_task", "actor": ADMIN1, "payload": {"task_id": tid}})
        cs_a = new_client_state(ADMIN1); cs_a["route_params"] = {"task_id": tid}
        view2 = self.app.render("task_detail", be, cs_a)
        fe_disabled = "title" in view2.get("disabled_fields", [])
        api_freezes = be.handle({"endpoint": "update_task", "actor": ADMIN1,
                                 "payload": {"task_id": tid, "title": "z"}})["status"] != 200
        self.ok("cross_layer", "freeze_fe_api_consistent", fe_disabled and api_freezes,
                f"fe_disabled={fe_disabled} api_freezes={api_freezes}")


SUITES = ["functional", "state_machine", "permissions", "multi_tenant",
          "scheduling", "cache", "post_approval", "audit", "cross_layer"]


def run_all(app_dir):
    app = _load(app_dir)
    c = Checks(app)
    errors = []
    for s in SUITES:
        try:
            getattr(c, s)()
        except Exception as e:
            errors.append({"suite": s, "error": f"{type(e).__name__}: {e}"})
            c.ok(s, f"{s}_suite_crash", False, f"{type(e).__name__}: {e}")
    return {"checks": c.results, "errors": errors}


if __name__ == "__main__":
    import json
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "reference")
    res = run_all(os.path.abspath(d))
    npass = sum(1 for r in res["checks"] if r["passed"])
    for r in res["checks"]:
        if not r["passed"]:
            print("FAIL", r["invariant"], r["name"], r["detail"])
    print(f"\n{npass}/{len(res['checks'])} checks passed; errors={len(res['errors'])}")
