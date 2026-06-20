# SCHEMAS.md — frontmatter 스키마

모든 조율층/이벤트 항목 파일은 YAML frontmatter(`---`로 감싼 블록)로 시작합니다. `askctl.py`가 이 frontmatter를 스캔해 INDEX를 생성하고 충돌을 검출합니다.

> **도구 파서 제약 (중요):** `askctl.py`는 의존성 없는 경량 파서를 씁니다. 다음만 지원합니다 —
> ① `key: value`(스칼라), ② `key: [a, b]`(**인라인 리스트**), ③ 한 단계 중첩 맵(`touches:` 아래 들여쓴 `contracts: [..]`).
> 리스트는 **반드시 인라인(`[...]`)** 으로 적으세요. 블록 리스트(`- item` 여러 줄)도 파싱되지만, 인라인을 권장합니다.
> 값에 `:`나 `#`가 들어가면 따옴표로 감싸세요.

---

## §workitem — `workitems/WI-<YYYYMMDD>-<slug>.md`

```yaml
---
id: WI-20260620-admin-role
title: Add admin role model
owner: munyeong                 # team/<handle>.md 의 handle (askctl이 검증)
status: claimed                 # proposed | ready | claimed | in_progress | review | done | blocked
branch: feat/WI-20260620-admin-role
feature: features/feature-admin.md
source_refs: [SOURCES/SRC-20260620-0930-user-request.md]
depends_on: []                  # [WI-id, ...]
touches:
  contracts: [auth, data_model] # ARCHITECTURE 절 키. 비면 []
  modules: [admin, auth]        # 코드 모듈/도메인. 비면 []
created: 2026-06-20
---

## 진행 메모
- 다음 첫 명령: ...
```

`contracts`가 다른 in-flight workitem과 겹치면 `detect`가 **STOP**, `modules`가 겹치면 **WARN**을 냅니다.

---

## §source — `SOURCES/SRC-*.md` (불변) + `SOURCES/SRC-*.meta.md` (가변)

**원본 (불변 content):** frontmatter는 식별 최소한만. 본문은 제출된 원문 그대로.

```yaml
---
id: SRC-20260620-0930-user-request
kind: change_request            # change_request | reference | initial_requirements
submitted: 2026-06-20
---

(제출 원문 — 수정하지 않음)
```

**메타 (가변 triage, per-source single-writer):**

```yaml
---
id: SRC-20260620-0930-user-request
status: under_review            # not_applied | under_review | applied | rejected | superseded
triage_owner: munyeong
related_workitems: [WI-20260620-admin-role]
applied_artifacts: []           # [features/..., ARCHITECTURE.md, ...]
supersedes: []
summary: 관리자 역할 모델 추가 요청
---
```

---

## §assumption — `assumptions/ASM-<YYYYMMDD>-<slug>.md`

```yaml
---
id: ASM-20260620-token-expiry
status: active                  # active | confirmed | superseded
scope: auth                     # 충돌 점검용 영역 키
owner: munyeong
related_workitems: [WI-20260620-auth-login]
conflicts_with: []              # [ASM-id, ...]
created: 2026-06-20
---

결정: ... / 이유: ...
```

---

## §note — `notes/<topic>.md` 또는 `notes/<topic>/<YYYYMMDD>-<slug>.md`

frontmatter는 선택이며, 있으면 `topic`을 권장합니다.

```yaml
---
topic: auth
created: 2026-06-20
---

## refresh token
- [2026-06-20] ... (근거: 실제 호출로 확인)
```

---

## §conflict — `conflicts/CF-<YYYYMMDD>-<slug>.md`

```yaml
---
id: CF-20260620-token-expiry-policy
status: open                    # open | resolved
kind: modules                   # contracts | modules | source | architecture
between: [WI-20260620-admin-role, WI-20260620-auth-login]
owner: munyeong                 # 조정 담당
created: 2026-06-20
---

## 무엇이 충돌하는가
## 해소 결정 (누가 rebase/양보, 근거)
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

## 어디까지
## 다음 첫 명령
```

---

## §team — `team/<handle>.md`

```yaml
---
handle: munyeong                # 안정적 짧은 식별자 (owner/세션 파일명이 참조)
name: 오문영
emails: [munyeong.oh@nhn.com]   # git config user.email 매칭 키 (복수 허용)
role: maintainer                # maintainer | contributor
agents: [claude-code, codex]    # 운용하는 에이전트 런타임
active: true
joined: 2026-06-20
---
```
