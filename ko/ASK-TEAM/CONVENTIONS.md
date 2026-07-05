# CONVENTIONS.md — ASK-Team 구조 규약 (normative)

이 문서는 ASK-Team의 **강제 규약**입니다. 프롬프트(`KICKOFF`·`ADOPT`·`DEVELOP`·`INTEGRATE`·`AUDIT`)는 모두 이 규약을 따릅니다. 규약과 프롬프트가 다르면 이 문서가 우선합니다.

> **이 킷은 markdown + git만 사용합니다.** 추가 런타임(파이썬 등)·실행 바이너리를 요구하지 않습니다.
> 아래의 "검출"·"신원 확인"·"목록 읽기"는 모두 **에이전트가 파일 읽기/쓰기와 `git` 명령으로 직접 수행**합니다.

> 경로 기준: 모든 산출물은 프로젝트 루트의 `AGENTSPECKIT/` 아래에 있습니다(루트 3파일 예외: 프로젝트 `README.md`·`AGENTS.md`·`CLAUDE.md`). 이 문서의 경로는 모두 `AGENTSPECKIT/` 기준입니다.

---

## 1. 파일 등급 (누가 무엇을 쓰는가)

모든 파일은 네 등급 중 하나입니다. 등급이 **누가 single-writer인지**를 결정합니다.

| 등급 | 파일 | 작성 권한 | 동시성 규칙 |
|---|---|---|---|
| **Stable contract** | `ARCHITECTURE.md`, `PLAN.md`, `AGENTS.md`, 프롬프트 | **maintainer만** | 동시편집 금지. 변경은 §6 직렬화 |
| **Coordination** | `workitems/WI-*.md`, `conflicts/CF-*.md`, `team/<handle>.md`, `personas/*.md` | 해당 owner (personas: 생성자) | 공유 브랜치 published (§4.2·§4.5) |
| **Work-scoped** | `features/*.md`, `qa/*.md`, `sessions/*.md`, `notes/*` | 관련 workitem owner | 무관한 workitem은 만지지 않음 |
| **Event (append)** | `history/**`, `assumptions/ASM-*.md`, `adr/ADR-*.md`, `SOURCES/SRC-*.md`, `discussion/*.md` | 생성자 | 새 사건 = 새 파일. 기존 기록은 삭제 대신 supersede |

핵심 원칙: **두 스트림이 같은 파일 영역을 동시에 쓰지 않는다.** 공유 파일에 append하지 말고 새 파일을 만든다. **고정 INDEX 파일은 두지 않는다**(§3).

`personas/*.md`(공유 리뷰 인프라)는 날짜-slug가 아니라 **역할명 파일**(`security.md`)이라, 동시 생성이 충돌할 수 있는 유일한 지점입니다. 인스턴스를 만들기 전에 `git fetch`하여 그 역할의 인스턴스가 이미 없는지 확인하고, 생성/갱신은 **공유 브랜치에서** 합니다(§4.5). 갱신은 생성자 또는 maintainer가 합니다.

---

## 2. 식별 규약

### 2.1 기준점
- 식별의 1차 키는 `git config user.email`(고유). 새 인증 체계를 만들지 않습니다.
- 책임 주체(인간) = commit **author**. 실행자(에이전트) = `Co-Authored-By` 트레일러.

### 2.2 레지스트리 — `team/<handle>.md`
참여자는 per-person 파일로 등록합니다(스키마는 `SCHEMAS.md` §team). `handle`은 안정적 짧은 식별자이며 `owner`/세션 파일명이 이 값을 참조합니다.

- 이탈자는 삭제하지 않고 `active: false`로 둡니다(history가 참조).
- 동명이인은 email 고유키로 구분, `handle`은 별칭.

### 2.3 세션 시작 시 신원 확인 (에이전트가 수행)
에이전트는 세션을 시작할 때 신원을 **스스로 확인**합니다(사용자가 명령을 입력하지 않습니다).

```text
1. `git config user.email` 실행
2. team/*.md 의 emails 와 매칭 → 내 handle, role 확인
3. 매칭 실패(미등록) → team/<handle>.md 등록 먼저 (templates/team-TEMPLATE.md). 등록 전 작업 진입 금지.
```

### 2.4 식별이 박히는 곳
- workitem `owner:` = 등록된 handle.
- 세션 파일 = `sessions/<handle>--<WI-id>.md` (한 사람이 동시에 여러 workitem을 돌릴 수 있으므로 `(handle, workitem)`이 고유키).
- commit 트레일러:
  ```text
  Session-Id: <YYYY-MM-DDThhmm>-<handle>-<WI-id>
  Co-Authored-By: Claude Code <runtime@ask-team>
  ```

### 2.5 검증 시점
- **claim:** `owner`가 `active: true` 등록 handle인가.
- **integrate:** feature 브랜치 commit author email ∈ `owner.emails` (또는 owner가 `Co-Authored-By`에). 불일치 → "claim한 사람 ≠ 작업한 사람" flag.
- **audit:** 미등록 author commit / owner 없거나 inactive한 WI / 권한 위반(contributor가 stable contract 수정).

### 2.6 신뢰 모델
신원 검증은 **실수·드리프트를 잡지 악의적 사칭은 막지 못합니다**(markdown엔 강제수단 없음). 사칭 차단이 필요하면 git 플랫폼 계층을 얹습니다: protected branch, required PR review, signed commits, CODEOWNERS(`ARCHITECTURE.md`/`PLAN.md`에 maintainer 승인 강제).

---

## 3. 목록·상태 규약 (고정 INDEX 없음)

- **진실의 출처(SoT)는 각 항목 파일의 frontmatter입니다.** 별도 INDEX 파일을 만들지 않습니다.
- 에이전트는 진행 상태·작업 목록·이력 등을 파악할 때 해당 디렉토리의 `*.md` frontmatter를 **직접 읽습니다**(선택 로딩 — 현재 작업에 필요한 것만, 검출 시에는 in-flight workitem만).
- 사람이 읽을 집계 표가 필요하면 그때 에이전트에게 요청해 markdown으로 받습니다. **표를 파일로 강제 생성·커밋하지 않습니다**(staleness·동시수정 충돌 원천 차단).
- 이 규약 덕분에 공유 INDEX 파일이 없어 **INDEX 동시수정 충돌이 존재하지 않으며**, 추가 런타임·빌드 스텝도 필요 없습니다.

---

## 4. workitem 규약

### 4.1 상태 머신
```text
proposed → ready → claimed → in_progress → review → done
                          ↘ blocked ↗
```
- `proposed`/`ready`가 백로그 역할을 합니다(solo ASK의 `TODO.md`를 흡수).
- `done`은 INTEGRATE에서 merge·history 기록이 끝났을 때만 부여합니다 (status→`done` 기록은 INTEGRATE 중 maintainer가 수행 — WI single-writer 규칙의 공인된 예외).
- `done`이 되면 INTEGRATE가 status 기록과 같은 커밋에서 파일을 `workitems/archive/`로 이동합니다(§9) — 이로써 claim 직후·integrate 직전 검출(§5.1)이 프로젝트 누적 workitem 수가 아니라 활성 백로그로 범위가 제한됩니다.

### 4.2 claim = 조율층 published (핵심)
workitem을 claim하면 `WI-*.md`(`touches` 포함)를 **공유 브랜치에 먼저 커밋하고 즉시 push**합니다(파일 추가만 → 저충돌; 발행 절차 §4.5). 이로써 모든 기여자가 in-flight 작업과 그 `touches`를 볼 수 있습니다. 코드 작업은 그 다음 `feat/WI-*` 브랜치에서 시작합니다.

### 4.3 필수 필드
`id`·`title`·`owner`·`status`·`branch`·`feature`·`touches`(`contracts`·`modules`). 스키마는 `SCHEMAS.md` §workitem.

### 4.4 ID 규약
`WI-<YYYYMMDD>-<slug>` (예: `WI-20260620-admin-role`). 순차번호를 쓰지 않아 동시 할당 충돌을 회피합니다. `ADR-*`도 동일하게 `ADR-<YYYYMMDD>-<slug>`.

### 4.5 공유 브랜치와 발행(publishing) 절차 (normative)

* **공유 브랜치**는 저장소의 기본 통합 브랜치입니다(`main`/`master`, 또는 팀이 지정한 trunk). KICKOFF가 선택한 이름을 `AGENTS.md`에 기록합니다. 플랫폼이 직접 push를 막으면(브랜치 보호) 별도의 `coordination` 브랜치를 공유 브랜치로 지정하고 그것을 기록합니다.
* **발행 = 공유 브랜치에 커밋 + 즉시 push.** claim, `WI-*.md` 상태 변경, `conflicts/CF-*.md`, `team/<handle>.md` 등록, `personas/*.md` 인스턴스 생성/갱신은 모두 이 방식으로 발행합니다. 공유 브랜치에 직접 push할 수 있는 것은 이 조율층 파일들**뿐**이고 — 코드/작업층 변경은 PR(INTEGRATE)로만 도달합니다.
* **`WI-*.md`는 공유 브랜치에서만 편집합니다**(단일 거처). WI 상태 변경을 feature 브랜치에 싣지 마세요 — feature 브랜치 원자 커밋은 `WI-*.md`를 제외합니다(§7).
* **읽기 전 fetch:** 공유 브랜치의 조율 상태를 읽는 모든 단계(검출 §5.1, INTEGRATE, AUDIT)는 먼저 `git fetch`를 실행하고 **최신** 공유 브랜치(`origin/<공유 브랜치>`)를 읽습니다. 낡았을 수 있는 로컬 사본을 읽지 않습니다.
* 동시에 발행이 겹쳐 push가 거부되면 공유 브랜치를 `git pull --rebase`한 뒤 다시 push합니다 — 조율 파일은 owner별 새 파일/추가 전용이라 내용 충돌은 구조적으로 드뭅니다.

---

## 5. 충돌 규약

### 5.1 검출 (에이전트가 수행)
**claim 직후**와 **integrate 직전**에, 먼저 `git fetch`(§4.5)한 뒤 최신 공유 브랜치의 `workitems/*.md` 중 `status ∈ {claimed, in_progress}`인 것을 읽어 내 `touches`와 전수 교차합니다.

| 겹침 | 의미 | 처리 |
|---|---|---|
| `contracts` | 전역 계약 동시 편집 — 최고 위험 | **STOP.** maintainer가 §6으로 직렬화 |
| `modules` | 같은 모듈 동시 변경 — 잠재 충돌 | `conflicts/CF-*.md` 등재 + 순서 합의 |
| 없음 | 독립 | 진행 |

### 5.2 conflicts/CF-*.md
의미 충돌(git 충돌은 없지만 모순) 1건과 해소 결정을 기록합니다(불변·추가전용). 어느 workitem이 rebase/양보하는지, 합의 근거를 남깁니다. 스키마는 `SCHEMAS.md` §conflict.

대상 예: 두 workitem이 같은 API 계약을 다르게 가정 / 같은 데이터 모델을 다른 방향으로 변경 / source 요구 간 충돌 / 합의되지 않은 architecture 변경.

---

## 6. 전역 계약 직렬화 규약

`ARCHITECTURE.md`·`PLAN.md`는 **maintainer single-writer**입니다. contributor는 직접 수정하지 않습니다.

```text
계약 변경 절차:
  ① touches.contracts 선언한 전용 workitem + ADR(Proposed)
  ② 같은 contract를 touch하는 in-flight workitem 검출(§5) → STOP 통지
  ③ maintainer: 계약변경 workitem을 먼저 merge → ADR Accepted → ARCHITECTURE 갱신
  ④ 의존 workitem들이 새 계약으로 rebase 후 진행
```

ADR 작성 트리거(아키텍처·인증·DB 구조·외부 API·배포·테스트 전략 등)는 solo ASK KICKOFF §16([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md))을 따르되, 거기서 의무화하는 `adr/INDEX.md` 등재는 **예외**입니다(고정 INDEX 없음, §3; ADR ID는 순차번호가 아니라 §4.4의 `ADR-<YYYYMMDD>-<slug>`). lock 파일은 두지 않습니다(maintainer + merge 순서가 직렬화 장치).

---

## 7. 원자 커밋 규약

feature 브랜치의 한 커밋 = **코드 + 그 workitem의 작업층 파일**(feature 명세, qa, notes, assumptions, 자기 세션 파일).

포함하지 않는 것:
- `ARCHITECTURE.md`/`PLAN.md` (maintainer 영역)
- `history/**` (INTEGRATE가 기록)
- `workitems/WI-*.md` (조율 등급 — 상태 변경은 공유 브랜치에서 커밋·push, §4.5)

이로써 "코드와 대응 문서를 한 커밋에"라는 원칙을 workitem 스코프 내에서 유지하면서, 브랜치 간 merge에서 stable 파일이 충돌하지 않게 합니다. (고정 INDEX가 없으므로 INDEX는 애초에 커밋 대상이 아닙니다.)

---

## 8. SOURCES 규약

- `SOURCES/REQUIREMENTS.md` — 초기 요구사항. 반영 완료 시 **동결**(불변). KICKOFF freeze 계약을 그대로 유지합니다.
- `SOURCES/SRC-<YYYYMMDD-hhmm>-<slug>.md` — 제출 원본. **불변 content.**
- `SOURCES/SRC-*.meta.md` — 해당 원본의 **가변 triage**(status·owner·연결 workitem). per-source single-writer라 서로 다른 source를 동시에 triage해도 충돌하지 않습니다. **같은 source는 한 명만 triage**합니다.
- source 목록·상태는 `SRC-*.meta.md` frontmatter를 직접 읽어 파악합니다(고정 INDEX 없음).
- `SOURCES/REQUIREMENTS.meta.md` — `REQUIREMENTS.md`의 triage meta. `SRC-*` 명명을 따르지 않는 유일한 source입니다(`id: REQUIREMENTS`, 나머지 필드는 동일 — SCHEMAS §source). KICKOFF가 생성하고 초기화 완료 시 status를 `applied`로 동결합니다.
- 권위 규칙: 변경요청은 `applied` 전까지 권위가 없습니다. 현재 의도는 산출물(ARCHITECTURE/features/PLAN)에서 읽습니다. (solo ASK KICKOFF §15.2([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md)) 권위·불변·대체 체인 규칙을 계승.)

---

## 9. 수명 / 회전

- `workitems/`: workitem이 `done`이 되면 INTEGRATE가 status 기록과 같은 커밋에서 파일을 `workitems/archive/`로 옮깁니다(§4.1). 루트에는 `proposed`/`ready`/`claimed`/`in_progress`/`review`/`blocked` 항목만 남으므로, 세션마다 도는 검출 스캔(§5.1, INTEGRATE §2, AUDIT §3.4)이 프로젝트 누적 workitem 수가 아니라 활성 백로그 크기로 제한됩니다. 상호참조(`depends_on`/`related_workitems`/`between`)는 경로가 아니라 `WI-id`를 저장하므로 아카이브해도 링크가 깨지지 않습니다 — id를 찾을 때는 `workitems/`를 먼저, 없으면 `workitems/archive/`를 확인합니다.
- `sessions/`: 완료된 세션은 `sessions/archive/`로 이동합니다. 활성 세션만 루트에 둡니다.
- `history/`: `YYYY/MM`로 자연 분할되므로 별도 회전이 불필요합니다. 오래된 연도는 필요 시 압축 아카이브.
- `notes/`: 주제가 커지면 `notes/<topic>.md` → `notes/<topic>/*.md`로 분할합니다.

---

## 10. 스키마

모든 frontmatter 스키마와 예시는 [SCHEMAS.md](SCHEMAS.md)에 있습니다. `templates/`의 예시 파일을 복사해 시작하세요.
