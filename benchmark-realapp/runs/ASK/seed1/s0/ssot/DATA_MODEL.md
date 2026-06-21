# DATA_MODEL

All tables are declared via `opsdb.Database.define_table()`. The `id` column
is an auto-incremented integer PK added implicitly by the DB engine.

## Table: projects
| Column    | Type | Required | Notes                        |
|-----------|------|----------|------------------------------|
| id        | int  | auto     | PK                           |
| name      | str  | yes      | project display name         |
| org_id    | int  | yes      | tenant scoping key           |
| owner_id  | int  | yes      | user_id of project owner     |

## Table: tasks
| Column     | Type                                              | Required | Notes                                |
|------------|---------------------------------------------------|----------|--------------------------------------|
| id         | int                                               | auto     | PK                                   |
| project_id | ref:projects                                      | yes      | FK to projects                       |
| org_id     | int                                               | yes      | denormalised; enables org-only scans |
| title      | str                                               | yes      |                                      |
| scope      | str                                               | yes      | free-text scope description          |
| owner      | int                                               | yes      | user_id responsible                  |
| status     | enum:draft\|submitted\|approved\|rejected\|scheduled\|completed | yes | lifecycle state |
| slot       | str                                               | no       | scheduled time slot; None until scheduled |
| created_by | int                                               | yes      | user_id who created the task         |

## Table: comments
| Column  | Type      | Required | Notes                    |
|---------|-----------|----------|--------------------------|
| id      | int       | auto     | PK                       |
| task_id | ref:tasks | yes      | FK to tasks              |
| org_id  | int       | yes      | denormalised tenant key  |
| author  | int       | yes      | user_id                  |
| body    | str       | yes      | comment text             |

## Table: audit
| Column   | Type      | Required | Notes                                   |
|----------|-----------|----------|-----------------------------------------|
| id       | int       | auto     | PK                                      |
| task_id  | ref:tasks | yes      | FK to tasks                             |
| org_id   | int       | yes      | denormalised tenant key                 |
| actor_id | int       | yes      | user_id who performed the action        |
| action   | str       | yes      | e.g. create, update, submit, approve    |
| detail   | str       | yes      | human-readable detail (may be empty "")  |

## Denormalisation rule
`org_id` is stored on tasks, comments, and audit rows so that all org-scoped
queries can be satisfied with a single `db.query(table, org_id=X)` call
without joining to projects. Future sessions MUST populate `org_id` on every
insert to these tables.

## Schema initialisation
`_define_schema(db)` in app.py declares all tables and is idempotent (guards
on `"projects" in db.tables()`). It is called automatically by `make_backend`.
