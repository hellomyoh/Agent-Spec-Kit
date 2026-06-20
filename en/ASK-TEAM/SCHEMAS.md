# SCHEMAS.md — frontmatter schemas

Every coordination-layer / event item file starts with YAML frontmatter (a block fenced by `---`). `askctl.py` scans this frontmatter to generate INDEX files and detect conflicts.

> **Tool parser constraint (important):** `askctl.py` uses a dependency-free lightweight parser. It supports only —
> ① `key: value` (scalar), ② `key: [a, b]` (**inline list**), ③ one level of nested map (`contracts: [..]` indented under `touches:`).
> Write lists **as inline (`[...]`)**. Block lists (multiple `- item` lines) parse too, but inline is recommended.
> If a value contains `:` or `#`, wrap it in quotes.

---

## §workitem — `workitems/WI-<YYYYMMDD>-<slug>.md`

```yaml
---
id: WI-20260620-admin-role
title: Add admin role model
owner: munyeong                 # handle from team/<handle>.md (validated by askctl)
status: claimed                 # proposed | ready | claimed | in_progress | review | done | blocked
branch: feat/WI-20260620-admin-role
feature: features/feature-admin.md
source_refs: [SOURCES/SRC-20260620-0930-user-request.md]
depends_on: []                  # [WI-id, ...]
touches:
  contracts: [auth, data_model] # ARCHITECTURE section keys. [] if none
  modules: [admin, auth]        # code modules/domains. [] if none
created: 2026-06-20
---

## Progress notes
- Next first command: ...
```

If `contracts` overlaps another in-flight workitem, `detect` raises **STOP**; if `modules` overlaps, it raises **WARN**.

---

## §source — `SOURCES/SRC-*.md` (immutable) + `SOURCES/SRC-*.meta.md` (mutable)

**Original (immutable content):** frontmatter is the bare minimum for identification. The body is the submitted text as-is.

```yaml
---
id: SRC-20260620-0930-user-request
kind: change_request            # change_request | reference | initial_requirements
submitted: 2026-06-20
---

(submitted text — not modified)
```

**Meta (mutable triage, per-source single-writer):**

```yaml
---
id: SRC-20260620-0930-user-request
status: under_review            # not_applied | under_review | applied | rejected | superseded
triage_owner: munyeong
related_workitems: [WI-20260620-admin-role]
applied_artifacts: []           # [features/..., ARCHITECTURE.md, ...]
supersedes: []
summary: Request to add an admin role model
---
```

---

## §assumption — `assumptions/ASM-<YYYYMMDD>-<slug>.md`

```yaml
---
id: ASM-20260620-token-expiry
status: active                  # active | confirmed | superseded
scope: auth                     # area key for conflict checking
owner: munyeong
related_workitems: [WI-20260620-auth-login]
conflicts_with: []              # [ASM-id, ...]
created: 2026-06-20
---

Decision: ... / Rationale: ...
```

---

## §note — `notes/<topic>.md` or `notes/<topic>/<YYYYMMDD>-<slug>.md`

Frontmatter is optional; if present, `topic` is recommended.

```yaml
---
topic: auth
created: 2026-06-20
---

## refresh token
- [2026-06-20] ... (basis: verified with an actual call)
```

---

## §conflict — `conflicts/CF-<YYYYMMDD>-<slug>.md`

```yaml
---
id: CF-20260620-token-expiry-policy
status: open                    # open | resolved
kind: modules                   # contracts | modules | source | architecture
between: [WI-20260620-admin-role, WI-20260620-auth-login]
owner: munyeong                 # coordination lead
created: 2026-06-20
---

## What conflicts
## Resolution decision (who rebases/yields, rationale)
```

---

## §session — `sessions/<handle>--<WI-id>.md`

```yaml
---
handle: munyeong
workitem: WI-20260620-admin-role
status: active                  # active | done
started: 2026-06-20
---

## Where I left off
## Next first command
```

---

## §team — `team/<handle>.md`

```yaml
---
handle: munyeong                # stable short identifier (referenced by owner/session filenames)
name: Munyeong Oh
emails: [munyeong.oh@nhn.com]   # key matched against git config user.email (multiple allowed)
role: maintainer                # maintainer | contributor
agents: [claude-code, codex]    # agent runtimes you operate
active: true
joined: 2026-06-20
---
```
