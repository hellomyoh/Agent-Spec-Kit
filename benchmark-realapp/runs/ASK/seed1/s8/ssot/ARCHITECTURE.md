# ARCHITECTURE

## Module layout
```
work/
  app.py              # single module: Backend class + make_backend / render / seed
  provided/
    opsdb.py          # DB engine (do not edit)
    opscache.py       # TTL cache (do not edit)
    contract.py       # shared surface contract (do not edit)
  ssot/               # living spec docs (update every session)
```

## app.py structure
- `_define_schema(db)` — declares all 4 tables; idempotent.
- `Backend` class — all endpoint handlers as private methods; dispatched in
  `handle(request)`.
- `make_backend(db, cache) -> Backend` — public factory.
- `seed(backend, spec) -> None` — loads `{"projects": [...]}` into DB.
- `render(view, backend, client_state) -> dict` — assembles page dicts by
  calling `backend.handle(...)`.

## Request/Response conventions
- Every handler raises Python built-ins to signal error type:
  - `PermissionError` -> 403
  - `LookupError`     -> 404
  - `ValueError`      -> 409 (state-machine violations, conflicts)
  - anything else     -> 400
- The dispatcher in `handle()` catches these and formats `{"status", "error"}`.
- Success returns `{"status": 200, "data": ...}`.

## Tenant isolation mechanism
- All tables with a per-task or per-project scope carry a denormalised `org_id`
  column.
- Every query filters by `org_id=actor.org_id`.
- Cross-org access is prevented structurally (no global scans except in audit
  by admin — not yet implemented).

## Dependency injection
`make_backend(db, cache)` accepts any DB and Cache objects that match the
`opsdb.Database` / `opscache.Cache` interface. Tests may inject test doubles.
