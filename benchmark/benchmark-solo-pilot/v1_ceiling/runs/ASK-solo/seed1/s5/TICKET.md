# S5 — Change unknown-field handling

CHANGE the behaviour for an unknown field in `where`:
- A `where` referencing a field that is not present in any stored record must now yield
  NO match — `query(...)` returns `[]`. It must NOT raise.

Implement only this change this session.
