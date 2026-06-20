# CONVENTIONS.md — ASK-Team 구조 규약 (normative)

이 문서는 ASK-Team의 **강제 규약**입니다. 프롬프트(`DEVELOP.md`·`INTEGRATE.md`)와 도구(`askctl.py`)는 모두 이 규약을 구현합니다. 규약과 프롬프트가 다르면 이 문서가 우선합니다.

> 경로 기준: 모든 산출물은 프로젝트 루트의 `AGENTSPECKIT/` 아래에 있습니다(루트 3파일 예외: 프로젝트 `README.md`·`AGENTS.md`·`CLAUDE.md`). 이 문서의 경로는 모두 `AGENTSPECKIT/` 기준입니다.

---

## 1. 파일 등급 (누가 무엇을 쓰는가)

모든 파일은 네 등급 중 하나입니다. 등급이 **누가 single-writer인지**를 결정합니다.

| 등급 | 파일 | 작성 권한 | 동시성 규칙 |
|---|---|---|---|
| **Stable contract** | `ARCHITECTURE.md`, `PLAN.md`, `AGENTS.md`, 프롬프트 | **maintainer만** | 동시편집 금지. 변경은 §6 직렬화 |
| **Coordination** | `workitems/WI-*.md`, `conflicts/CF-*.md`, `team/<handle>.md` | 해당 owner | claim 시 공유 브랜치 published (§4) |
| **Work-scoped** | `features/*.md`, `qa/*.md`, `sessions/*.md`, `notes/*` | 관련 workitem owner | 무관한 workitem은 만지지 않음 |
| **Event (append)** | `history/**`, `assumptions/ASM-*.md`, `adr/ADR-*.md`, `SOURCES/SRC-*.md`, `discussion/*.md` | 생성자 | 새 사건 = 새 파일. 기존 기록은 삭제 대신 supersede |
| **Generated** | 모든 `INDEX.md`, (선택) `PROGRESS.md` 다이제스트 | `askctl`만 | 손으로 수정 금지. git 미추적 (§3) |

핵심 원칙: **두 스트림이 같은 파일 영역을 동시에 쓰지 않는다.** 공유 파일에 append하지 말고 새 파일을 만든다.

---

## 2. 식별 규약

### 2.1 기준점
- 식별의 1차 키는 `git config user.email`(고유). 새 인증 체계를 만들지 않습니다.
- 책임 주체(인간) = commit **author**. 실행자(에이전트) = `Co-Authored-By` 트레일러.

### 2.2 레지스트리 — `team/<handle>.md`
참여자는 per-person 파일로 등록합니다(스키마는 `SCHEMAS.md` §team). `handle`은 안정적 짧은 식별자이며 `owner`/세션 파일명이 이 값을 참조합니다. `team/INDEX.md`는 생성물입니다.

- 이탈자는 삭제하지 않고 `active: false`로 둡니다(history가 참조).
- 동명이인은 email 고유키로 구분, `handle`은 별칭.

### 2.3 자동 해소 — `askctl whoami`
세션 시작 시 식별을 **추론**합니다(입력하지 않음).

```bash
python AGENTSPECKIT/askctl.py whoami
# git config user.email → team/*.md 의 emails[] 매칭 → handle, role 출력
# 미등록 → 비정상 종료. 작업 진입 차단(귀속 오염 방지).
```

### 2.4 식별이 박히는 곳
- workitem `owner:` = 등록된 handle (askctl이 검증).
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
askctl 검증은 **실수·드리프트를 잡지 악의적 사칭은 막지 못합니다**(markdown엔 강제수단 없음). 사칭 차단이 필요하면 git 플랫폼 계층을 얹습니다: protected branch, required PR review, signed commits, CODEOWNERS(`ARCHITECTURE.md`/`PLAN.md`에 maintainer 승인 강제).

---

## 3. INDEX 규약 (생성물)

- 모든 `INDEX.md`는 **askctl이 frontmatter를 스캔해 만든 생성물**입니다.
- **git 미추적**입니다(`.gitignore`). 절대 손으로 수정하지 않습니다 — 다음 `index` 실행에 덮어쓰여집니다.
- 세션을 시작할 때 **반드시** `python askctl.py index`를 먼저 실행해 최신 인덱스를 만든 뒤 읽습니다. 신선하지 않은 인덱스는 in-flight 작업을 누락해 충돌 검출을 실패시킵니다.
- `INDEX.md`는 **읽기 편의를 위한 집계 뷰일 뿐 진실의 출처가 아닙니다.** SoT는 각 항목 파일의 frontmatter입니다.

---

## 4. workitem 규약

### 4.1 상태 머신
```text
proposed → ready → claimed → in_progress → review → done
                          ↘ blocked ↗
```
- `proposed`/`ready`가 백로그 역할을 합니다(solo ASK의 `TODO.md`를 흡수).
- `done`은 INTEGRATE에서 merge·history 기록이 끝났을 때만 부여합니다.

### 4.2 claim = 조율층 published (핵심)
workitem을 claim하면 `WI-*.md`(`touches` 포함)를 **공유 브랜치에 먼저 커밋**합니다(파일 추가만 → 저충돌). 이로써 모든 기여자가 in-flight 작업과 그 `touches`를 볼 수 있습니다. 코드 작업은 그 다음 `feat/WI-*` 브랜치에서 시작합니다.

### 4.3 필수 필드
`id`·`title`·`owner`·`status`·`branch`·`feature`·`touches`(`contracts`·`modules`). 스키마는 `SCHEMAS.md` §workitem.

### 4.4 ID 규약
`WI-<YYYYMMDD>-<slug>` (예: `WI-20260620-admin-role`). 순차번호를 쓰지 않아 동시 할당 충돌을 회피합니다. `ADR-*`도 동일하게 `ADR-<YYYYMMDD>-<slug>`.

---

## 5. 충돌 규약

### 5.1 검출 트리거
`python askctl.py detect <WI-id>`를 **claim 직후**와 **integrate 직전**에 실행합니다. 내 `touches`를 `status ∈ {claimed, in_progress}`인 다른 workitem들과 전수 교차합니다.

| 겹침 | 의미 | 처리 | askctl 종료코드 |
|---|---|---|---|
| `contracts` | 전역 계약 동시 편집 — 최고 위험 | **STOP.** maintainer가 §6으로 직렬화 | 2 |
| `modules` | 같은 모듈 동시 변경 — 잠재 충돌 | `conflicts/CF-*.md` 등재 + 순서 합의 | 1 |
| 없음 | 독립 | 진행 | 0 |

### 5.2 conflicts/CF-*.md
의미 충돌(git 충돌은 없지만 모순) 1건과 해소 결정을 기록합니다(불변·추가전용). 어느 workitem이 rebase/양보하는지, 합의 근거를 남깁니다. 스키마는 `SCHEMAS.md` §conflict.

대상 예: 두 workitem이 같은 API 계약을 다르게 가정 / 같은 데이터 모델을 다른 방향으로 변경 / source 요구 간 충돌 / 합의되지 않은 architecture 변경.

---

## 6. 전역 계약 직렬화 규약

`ARCHITECTURE.md`·`PLAN.md`는 **maintainer single-writer**입니다. contributor는 직접 수정하지 않습니다.

```text
계약 변경 절차:
  ① touches.contracts 선언한 전용 workitem + ADR(Proposed)
  ② askctl detect → 같은 contract를 touch하는 in-flight workitem에 STOP 통지
  ③ maintainer: 계약변경 workitem을 먼저 merge → ADR Accepted → ARCHITECTURE 갱신
  ④ 의존 workitem들이 새 계약으로 rebase 후 진행
```

ADR 작성 트리거(아키텍처·인증·DB 구조·외부 API·배포·테스트 전략 등)는 solo ASK [KICKOFF §16](../AGENTSPECKIT/KICKOFF.md)을 따릅니다. lock 파일은 두지 않습니다(maintainer + merge 순서가 직렬화 장치).

---

## 7. 원자 커밋 규약

feature 브랜치의 한 커밋 = **코드 + 그 workitem의 작업층 파일**(feature 명세, qa, notes, assumptions, 자기 `WI-*.md` status).

포함하지 않는 것:
- 생성 `INDEX.md` (git 미추적)
- `ARCHITECTURE.md`/`PLAN.md` (maintainer 영역)
- `history/**` (INTEGRATE가 기록)

이로써 "코드와 대응 문서를 한 커밋에"라는 원칙을 workitem 스코프 내에서 유지하면서, 브랜치 간 merge에서 stable/generated 파일이 충돌하지 않게 합니다.

---

## 8. SOURCES 규약

- `SOURCES/REQUIREMENTS.md` — 초기 요구사항. 반영 완료 시 **동결**(불변). KICKOFF freeze 계약을 그대로 유지합니다.
- `SOURCES/SRC-<YYYYMMDD-hhmm>-<slug>.md` — 제출 원본. **불변 content.**
- `SOURCES/SRC-*.meta.md` — 해당 원본의 **가변 triage**(status·owner·연결 workitem). per-source single-writer라 서로 다른 source를 동시에 triage해도 충돌하지 않습니다. **같은 source는 한 명만 triage**합니다.
- `SOURCES/INDEX.md` — 생성물.
- 권위 규칙: 변경요청은 `applied` 전까지 권위가 없습니다. 현재 의도는 산출물(ARCHITECTURE/features/PLAN)에서 읽습니다. (solo ASK [KICKOFF §15.2](../AGENTSPECKIT/KICKOFF.md) 권위·불변·대체 체인 규칙을 계승.)

---

## 9. 수명 / 회전

- `sessions/`: 완료된 세션은 `sessions/archive/`로 이동합니다. 활성 세션만 루트에 둡니다.
- `history/`: `YYYY/MM`로 자연 분할되므로 별도 회전이 불필요합니다. 오래된 연도는 필요 시 압축 아카이브.
- `notes/`: 주제가 커지면 `notes/<topic>.md` → `notes/<topic>/*.md`로 분할합니다.

---

## 10. 스키마

모든 frontmatter 스키마와 예시는 [SCHEMAS.md](SCHEMAS.md)에 있습니다. `templates/`의 예시 파일을 복사해 시작하세요(이 디렉토리는 `askctl`이 스캔에서 제외합니다).
