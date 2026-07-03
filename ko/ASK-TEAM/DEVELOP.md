# DEVELOP.md — 기여자(Contributor) 개발 프롬프트

ASK-Team 팀 개발에서 **한 명의 기여자(인간/AI 에이전트)가 하나의 workitem을 수행**하는 절차입니다.
규약은 [CONVENTIONS.md](CONVENTIONS.md)가 우선합니다. 전역 계약 변경·통합은 maintainer의 [INTEGRATE.md](INTEGRATE.md)가 담당합니다.

> 이 킷은 markdown + git만 씁니다. 아래 "신원 확인"·"검출"·"목록 읽기"는 모두 **에이전트가 파일 읽기와 `git` 명령으로 직접 수행**합니다(별도 도구·명령 입력 없음).
> 경로 기준: 산출물은 모두 `AGENTSPECKIT/` 아래에 있습니다(루트 3파일 예외).

---

## 0. 세션 시작 (에이전트가 자동 수행)

1. **신원 확인** — `git config user.email`을 읽어 `team/*.md`의 `emails`와 매칭해 내 `handle`·`role`을 확인합니다. 매칭 실패(미등록)면 `team/<handle>.md`를 먼저 등록(`templates/team-TEMPLATE.md`)한 뒤 진행합니다.
2. **현황 파악** — 먼저 `git fetch`한 뒤, **최신** 공유 브랜치의 `workitems/*.md` frontmatter(`origin/<공유 브랜치>` — CONVENTIONS §4.5)를 읽어 in-flight 작업(특히 `claimed`/`in_progress`)과 그 `touches`를 확인합니다(고정 INDEX 파일 없음 — 항목 파일이 SoT).

---

## 1. 항상 로드하는 문서

1. `AGENTS.md` (프로젝트 루트)
2. `AGENTSPECKIT/ARCHITECTURE.md` (횡단 계약 — 항상 로드)
3. `AGENTSPECKIT/PLAN.md` (로드맵)
4. `AGENTSPECKIT/workitems/*.md` 중 **in-flight 항목의 frontmatter** (현황 + 다른 사람의 `touches`)

내 작업에 필요한 `features/*.md`·ADR·qa·notes는 선택적으로 읽습니다. 공통 규칙(데이터 모델/네이밍/API/인증)은 항상 `ARCHITECTURE.md`를 기준으로 따릅니다.

---

## 2. workitem 선택 또는 생성 (claim)

### 2.1 기존 workitem을 claim
`workitems/*.md` 중 `status: proposed|ready`인 항목을 고릅니다.

1. 해당 `WI-*.md`의 `owner`를 내 handle로, `status`를 `claimed`로 바꿉니다.
2. `branch`를 `feat/<WI-id>`로 기록합니다.
3. **공유 브랜치에 이 변경만 커밋하고 즉시 push**합니다 (코드 작업 전 — 발행, CONVENTIONS §4.5).

### 2.2 새 workitem 생성
`templates/WI-TEMPLATE.md`를 복사해 `workitems/WI-<YYYYMMDD>-<slug>.md`로 만듭니다.

* `touches`를 **반드시 채웁니다** — 이 작업이 건드릴 횡단 계약(`contracts`)과 모듈(`modules`). 충돌 검출의 핵심이므로 정확히 선언합니다.
* `feature`에 대응 명세 파일을 링크하고, `source_refs`에 근거 SRC를 링크합니다.
* 공유 브랜치에 커밋하고 즉시 push합니다 (발행 — CONVENTIONS §4.5).

---

## 3. 충돌 검출 (claim 직후 — 필수, 에이전트가 수행)

먼저 `git fetch`한 뒤, 최신 공유 브랜치의 `workitems/*.md` 중 `status ∈ {claimed, in_progress}`인 것을 읽어(CONVENTIONS §4.5), 내 `touches`와 교차합니다.

| 결과 | 의미 | 해야 할 일 |
|---|---|---|
| **STOP** | 다른 in-flight workitem과 `contracts` 겹침 | 진행하지 말 것. maintainer에게 직렬화 요청(§7). 계약 변경이면 ADR 경유 |
| **WARN** | `modules` 겹침 (잠재 의미 충돌) | `conflicts/CF-*.md` 등재(`templates/CF-TEMPLATE.md`), 상대 owner와 순서 합의 |
| **OK** | 독립 | `feat/<WI-id>` 브랜치 생성 후 개발 시작 |

---

## 4. 개발 (작업층 — feature 브랜치)

브랜치 생성: `git checkout -b feat/<WI-id>`. 세션 파일을 만듭니다: `sessions/<handle>--<WI-id>.md`(`templates/session-TEMPLATE.md`). 진행하며 "다음 첫 명령"을 갱신합니다.

작업 순서:

1. `WI-*.md` status를 `in_progress`로 — **공유 브랜치에서 커밋·push**합니다 (WI 파일은 공유 브랜치에서만 편집 — CONVENTIONS §4.5).
2. `features/*.md`의 명세와 `ARCHITECTURE.md` 계약을 확인합니다(없으면 명세부터, 비자명 기능은 `personas/`+`discussion/` 리뷰 — solo ASK DEVELOPINIT §6 방식, [reference/SOLO-DEVELOPINIT.md](reference/SOLO-DEVELOPINIT.md)).
3. 구현 + 자동 테스트 작성 → **실제 실행**(명령·결과 캡처). 실행 없이 통과를 주장하지 않습니다.
4. 코드 ↔ 명세 불일치 시 **권위 진단** 후 처리합니다: ① 어느 쪽이 권위인지 진단 → ② 명세가 의도를 담고 코드가 틀렸으면 코드 수정 → ③ 명세의 낡음이 확인되면 명세를 먼저 갱신한 뒤 코드를 맞춤 → ④ 판단 불가면 질문(maintainer/사용자) — 근거는 `assumptions/`·`notes/`에 기록. 임의로 명세를 고쳐 불일치를 지우지 않습니다(상세: solo DEVELOPINIT §3.4, [reference/SOLO-DEVELOPINIT.md](reference/SOLO-DEVELOPINIT.md)).
5. 자율 판단은 `assumptions/ASM-*.md`로 **새 파일** 생성(공유 단일 파일에 append하지 않음). 기존 가정과 충돌하면 `conflicts/`에 기록.
6. 학습한 비자명한 사실은 `notes/<topic>.md`에 기록(추측은 assumptions로).

**전역 계약을 바꿔야 한다고 판단되면 직접 `ARCHITECTURE.md`를 고치지 마세요.** STOP 사유로 보고 §7 절차를 따릅니다.

---

## 5. 원자 커밋 (workitem 스코프)

의미 있는 단위마다 **코드 + 그 workitem의 작업층 파일**을 하나의 커밋으로 묶습니다.

* 포함: 코드, `features/*.md`, `qa/*.md`, `assumptions/ASM-*.md`, `notes/*`, `sessions/<handle>--<WI-id>.md`.
* **제외**: `ARCHITECTURE.md`/`PLAN.md`(maintainer), `history/**`(INTEGRATE), `workitems/WI-*.md`(조율층 — 상태 변경은 공유 브랜치에서, CONVENTIONS §4.5).
* commit 메시지: Conventional Commits + 트레일러
  ```text
  feat: <요약>

  Session-Id: <YYYY-MM-DDThhmm>-<handle>-<WI-id>
  Co-Authored-By: <에이전트 런타임>
  ```
* 코드/작업층 변경은 `main`/`master`·공유 브랜치에 직접 push하지 않습니다 — PR(INTEGRATE)로만 도달합니다. **예외:** 조율층 파일(`workitems/`·`conflicts/`·`team/`·`personas/`)은 공유 브랜치에 직접 커밋·push합니다 — 그것이 곧 발행 메커니즘입니다(CONVENTIONS §4.5). `.env`·Secret·키 파일 commit 금지.

---

## 6. review 제출

1. `WI-*.md` status를 `review`로 (공유 브랜치에서 커밋·push — CONVENTIONS §4.5).
2. `feat/<WI-id>` push 후 PR 생성(merge는 maintainer가 INTEGRATE에서).
3. PR 본문에 WI-id, 변경 요약, 테스트 결과, `touches`, 미해소 `conflicts/`를 명시합니다.

---

## 7. STOP/직렬화가 필요할 때 (전역 계약 영향)

검출이 STOP이거나 전역 계약 변경이 필요하면:

1. 계약 변경 의도를 `touches.contracts`로 선언한 **전용 workitem** + `adr/ADR-*.md`(Proposed)를 작성합니다.
2. maintainer에게 직렬화를 요청합니다(INTEGRATE §3).
3. maintainer가 계약 변경을 먼저 merge하고 `ARCHITECTURE.md`/ADR을 갱신한 뒤, 내 workitem을 새 계약으로 **rebase**하고 §4를 재개합니다.

---

## 8. 완료 보고 형식

```md
# 개발 결과 (WI-<id>)
## 수행한 작업 / 변경 파일
## 테스트 결과 (실행 명령 / 통과·실패)
## touches (contracts / modules) 와 검출 결과
## 등재한 conflicts / assumptions / notes
## Git (브랜치 / commit / PR)
## 다음 첫 명령 (= sessions/<handle>--<WI-id>.md 갱신 내용)
```
