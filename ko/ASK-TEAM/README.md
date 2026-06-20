# ASK-Team — 팀 개발용 Agent-Spec-Kit

> 여러 개발자와 여러 AI 에이전트가 **동시에** 개발할 때 발생하는
> Git 충돌·의미 충돌·의도 충돌을 markdown + git만으로 줄이는 프레임워크.
> 기존 [Agent-Spec-Kit](../AGENTSPECKIT/)(1인/순차)의 **자매 프레임워크**입니다.

> **이 킷은 markdown 프롬프트로만 구성됩니다.** 별도 런타임(파이썬 등)이나 실행 바이너리를 요구하지 않으며,
> 에이전트가 가진 능력(파일 읽기/쓰기 + `git` 명령)만으로 동작합니다 — Claude Code · Codex · Cursor 어디서나 동일.

---

## 0. 포지셔닝 — solo ASK의 자매

기존 ASK(`AGENTSPECKIT/`)는 **1인/순차·자율 개발**을 위해 `PLAN.md`·`PROGRESS.md`·`HISTORY.md`·`ASSUMPTIONS.md`·`NOTES.md`·`SOURCES/INDEX.md` 같은 **전역 단일 파일**을 중심으로 동작합니다. 단순하지만, N명이 동시에 작업하면 이 파일들이 충돌 핫스팟이 됩니다.

ASK-Team은 이 문제를 **티어로 점진 도입하지 않고**, 처음부터 팀-우선으로 모든 메커니즘을 확정한 별도 프레임워크입니다. 1인 개발이라면 기존 ASK를 쓰는 것이 더 가볍습니다. ASK-Team은 **실제로 N명이 동시에 개발하는 팀**을 위한 것입니다.

**유지하는 철학:** markdown + git, 도구 독립성(Claude Code · Codex · Cursor), 세션 간 기억, 요구사항 추적성, 다중 페르소나 리뷰 하네스.

---

## 1. 핵심 통찰 — git branch 격리

ASK-Team의 모든 설계 결정은 한 가지 사실에서 나옵니다.

> **N명의 기여자는 서로의 *미커밋* 파일을 볼 수 없다.** feature 브랜치는 작업 트리를 격리한다.

따라서 `touches` 기반 충돌 검출이 작동하려면 **조율 메타데이터를 claim 시점에 공유 브랜치로 published**해야 합니다. 그래서 모든 산출물을 두 층으로 가릅니다.

| 층 | 내용 | 사는 곳 |
|---|---|---|
| **조율층(coordination)** | workitem 선언(`touches`), conflicts, 전역 계약(ARCHITECTURE/PLAN) | **공유 브랜치 — claim 시 즉시 published** |
| **작업층(work)** | 코드, feature 명세, qa, notes, assumptions | **feature 브랜치 (격리)** |

조율 메타데이터를 미리 공유하지 않으면 의미 충돌을 **merge 시점에야** 발견합니다. claim-시점 published가 **사전 검출**을 가능하게 합니다.

---

## 2. 역할 모델 (팀엔 필수)

| 역할 | 책임 | single-writer 대상 |
|---|---|---|
| **Maintainer (1+)** | 전역 계약·로드맵 소유, `INTEGRATE` 실행, 의미/의도 충돌 중재, 계약변경 ADR 승인 | `ARCHITECTURE.md`, `PLAN.md`, `AGENTS.md`, `history/` |
| **Contributor (N, 인간/에이전트)** | workitem claim, 브랜치 작업, scoped 파일 작성, PR | 자기 `WI-*.md`, 자기 작업층 파일 |

다중 인간의 **의도 충돌**(서로 다른 사람이 모순되는 요구를 제출)은 파일 구조가 아니라 **거버넌스**로 풉니다 — maintainer가 중재하고 ADR로 기록합니다. 도구는 충돌을 *표면화*할 뿐 합의를 만들지 않습니다.

---

## 3. 디렉토리 구조

프로젝트에 적용하면 모든 산출물은 `AGENTSPECKIT/` 아래에 생성됩니다(루트 3파일 예외: 프로젝트 `README.md`·`AGENTS.md`·`CLAUDE.md`). 기존 ASK와 동일한 루트 규약입니다.

```text
AGENTSPECKIT/
  # 프롬프트 (markdown only)
  KICKOFF.md  ADOPT.md  DEVELOP.md  INTEGRATE.md  AUDIT.md

  # 조율층 (공유 브랜치, maintainer single-writer 영역 포함)
  ARCHITECTURE.md                # 단일·강제로드 — maintainer만 수정
  PLAN.md                        # 안정 로드맵 — maintainer만 수정
  PROGRESS.md                    # 호환 진입점 (정적 스텁 — 항목 파일로 안내)
  workitems/  WI-*.md            # 작업 단위 (frontmatter = 상태의 SoT)
  conflicts/  CF-*.md            # 의미 충돌 기록

  # 식별
  team/       <handle>.md        # 참여자 레지스트리

  # 작업층 (feature 브랜치, 항목별 single-writer)
  sessions/   <handle>--<WI-id>.md   archive/
  history/    YYYY/MM/HIST-*.md       # INTEGRATE가 기록
  assumptions/ ASM-*.md
  notes/      <topic>.md  <topic>/*.md

  # 입력
  SOURCES/
    REQUIREMENTS.md              # 초기 요구사항 (동결 유지)
    SRC-*.md                     # 불변 원본 content
    SRC-*.meta.md                # 가변 triage (per-source single-writer)

  # 명세·리뷰 하네스 (유지 — 논문 핵심 기여)
  features/*.md   personas/*.md   discussion/review-*.md   adr/ADR-*.md   docs/  qa/

  templates/                     # 스키마 복사용 예시
```

> **고정 INDEX 파일을 두지 않습니다.** 각 디렉토리의 목록·상태는 항목 파일의 frontmatter가 진실의 출처이며, 에이전트가 필요할 때 직접 읽습니다(§5). 사람이 읽을 표가 필요하면 그때 에이전트에게 요청합니다.
> `locks/`도 두지 않습니다 — 전역 계약 보호는 **maintainer single-writer + ADR 게이트 + merge 순서**로 대체합니다(§6, CONVENTIONS §6).

---

## 4. 식별 — git identity에 정박

개발자 식별을 새로 발명하지 않습니다. **모든 커밋에 이미 있는 git identity**(email)를 기준으로 삼고, `team/` 레지스트리로 검증합니다. 추가 런타임 없이 **`git` 명령만** 사용합니다.

- **기준 키:** `git config user.email` (고유). `user.name`은 표시용.
- **두 축:** 책임 주체(인간 = commit author) / 실행자(에이전트 = `Co-Authored-By` 트레일러).
- **레지스트리:** `team/<handle>.md` (per-person, single-writer).
- **세션 시작 시 신원 확인:** 에이전트가 `git config user.email`을 읽어 `team/*.md`의 `emails`와 매칭해 `handle`·`role`을 확인합니다. 매칭 실패(미등록)면 `team/<handle>.md`를 먼저 등록한 뒤 진행합니다.
- **신뢰 모델:** 소프트 식별(귀속·충돌회피·검증)은 markdown이 제공, 하드 식별(사칭 차단)은 git 플랫폼(protected branch · signed commit · CODEOWNERS)에 위임.

상세 규약은 [CONVENTIONS.md §2](CONVENTIONS.md)를 참조하세요.

---

## 5. 상태 — 항목 파일이 진실의 출처 (고정 INDEX 없음)

- **SoT = 각 항목 파일의 frontmatter.** 단일 작성자가 자기 파일만 씁니다(`WI-*.md`, `ASM-*.md`, `SRC-*.meta.md`, `HIST-*.md`, `team/*.md`, `CF-*.md`).
- **고정 INDEX 파일을 만들지 않습니다.** 에이전트는 진행 상태·작업 목록을 파악할 때 해당 디렉토리의 `*.md` frontmatter를 **직접 읽습니다**(선택 로딩 — 필요한 것만).
- **사람용 집계 뷰**가 필요하면 그때 에이전트에게 "workitems를 표로 정리해줘"처럼 요청해 markdown으로 받습니다. **파일로 강제 생성·커밋하지 않습니다.**

효과:
- 공유 INDEX 파일이 없으므로 **INDEX 동시수정 충돌 자체가 존재하지 않습니다.**
- 별도 런타임·빌드 스텝이 없습니다 — 순수 프롬프트-only.
- 트레이드오프: 진행 상태를 한눈에 보는 고정 대시보드가 없습니다. 대신 `git`/`grep`/`gh`나 에이전트 요청으로 그때그때 봅니다.

---

## 6. 의미 충돌 검출 & 전역 계약 직렬화

**검출 (claim 직후 · integrate 직전 — 에이전트가 수행):**

```text
공유 브랜치의 workitems/*.md 중 status ∈ {claimed, in_progress}를 읽어
내 touches와 교차한다.
  · contracts 겹침 → STOP. maintainer가 직렬화(아래)
  · modules 겹침   → conflicts/CF-*.md 등재 + 순서 합의
  · 없음           → 진행
```

**전역 계약 직렬화 (locks 대신):**

```text
ARCHITECTURE / 전역 계약 변경 =
  ① touches.contracts 선언한 전용 workitem + ADR(Proposed)
  ② 같은 contract touch하는 in-flight workitem 검출 → STOP 통지
  ③ maintainer가 계약변경 workitem을 먼저 merge, ADR→Accepted, ARCHITECTURE 갱신
     (maintainer가 ARCHITECTURE single-writer → 동시편집 원천 차단)
  ④ 의존 workitem들이 새 계약으로 rebase
```

---

## 7. 개발 흐름

```text
1. 요구 수집      SOURCES/SRC-*.md (불변 원본) + SRC-*.meta.md (triage)
2. 분해 / claim   workitems/WI-*.md 작성(touches) → 공유 브랜치 커밋 → 검출(§6)
3. 개발           feat/WI-* 브랜치: 코드 + feature/qa/notes/assumptions (작업층)
                  비자명 기능은 personas/discussion 리뷰
4. review         WI status=review, PR
5. INTEGRATE      maintainer: touches 재검출 → merge → history 기록
                  → SRC-*.meta status=applied → PLAN 갱신 → 전체 회귀
6. audit          주기적: 고아 WI / 미검출 touches / 방치 SRC / 링크 무결성
```

**원자 커밋(재정의):** feature 브랜치의 원자 커밋 = **코드 + 그 workitem의 작업층 파일**. ARCHITECTURE/PLAN(maintainer), history(INTEGRATE)는 **포함하지 않습니다**. "코드와 대응 문서를 한 커밋에"라는 원칙은 *workitem 스코프 내에서* 유지됩니다.

---

## 8. 빠른 시작

1. 이 저장소를 clone하고 `ko/ASK-TEAM/`의 내용을 프로젝트 루트의 `AGENTSPECKIT/`로 복사합니다.
2. **Maintainer가** `team/<handle>.md`를 본인 것부터 등록하고 `role: maintainer`로 둡니다(`templates/team-TEMPLATE.md` 복사). 각 기여자도 자기 `team/<handle>.md`를 등록합니다.
3. 기여자는 `DEVELOP.md`, maintainer는 `INTEGRATE.md` 프롬프트로 작업합니다. 세션 시작 시 에이전트가 신원(§4)을 확인하고 필요한 항목 파일을 직접 읽습니다 — 별도 명령 입력이 없습니다.

> 초기화는 `KICKOFF.md`(신규)·`ADOPT.md`(기존 코드), 주기 점검은 `AUDIT.md`를 사용합니다.

---

## 9. solo ASK와의 차이

| 항목 | solo ASK | ASK-Team |
|---|---|---|
| 진행 상태 | `PROGRESS.md` 단일 커서 | `workitems/` + `sessions/<handle>--<WI>` |
| 이력 | `HISTORY.md` append | `history/YYYY/MM/HIST-*.md` (INTEGRATE 기록) |
| 가정 | `ASSUMPTIONS.md` 단일 | `assumptions/ASM-*.md` |
| 노트 | `NOTES.md` 단일 | `notes/<topic>.md` |
| 요구 상태 | `SOURCES/INDEX.md` 행(가변) | `SRC-*.meta.md` (per-source) |
| 목록/인덱스 | 손으로 갱신하는 단일 파일 | **고정 INDEX 없음 — frontmatter 직접 읽기** |
| 식별 | 불필요 | `team/` + git identity (`git config`) |
| 의미 충돌 | 해당 없음 | `touches` + 검출(§6) + `conflicts/` |
| 전역 계약 | ADR | ADR + **maintainer single-writer + merge 순서** |
| 런타임 | 없음 | 없음 (markdown + git만) |

---

## 10. 솔직한 한계 (근거 없는 긍정 금지)

1. **거버넌스 ≠ 도구.** 다중 인간 의도 충돌은 maintainer 중재로만 풀립니다. 프레임워크는 충돌을 표면화할 뿐 합의를 만들지 못합니다.
2. **검출 ≠ 강제.** `touches` 미선언/오선언이면 검출이 실패합니다. 에이전트가 규약을 따른다는 보장에 의존하며(프롬프트는 강제가 아님 — [README.md](../../README.md) 잔여 한계), INTEGRATE 재검출이 마지막 그물이지만 사후입니다. 진짜 *강제*가 필요하면 git 플랫폼 계층(protected branch / CI)을 옵션으로 얹습니다.
3. **비용은 의도된 대가.** 세션당 오버헤드(검출 시 in-flight workitem frontmatter 읽기)와 maintainer의 INTEGRATE 부담을 수용합니다. 1인이라면 solo ASK가 더 쌉니다.
4. **단일 실패점.** maintainer가 병목이 될 수 있습니다 → maintainer 복수화는 가능하되 ARCHITECTURE single-writer 규율은 영역 분할로 유지합니다.
5. **한눈 대시보드 없음.** 고정 INDEX를 두지 않으므로 진행 상태는 `git`/`grep`/`gh`나 에이전트 요청으로 그때그때 확인합니다.

---

## 11. 이 킷의 구성 파일

| 파일 | 역할 |
|---|---|
| `README.md` | 이 문서 — 프레임워크 개요·사양 |
| `CONVENTIONS.md` | 구조 규약 (파일 등급·식별·상태·충돌·계약·원자커밋·SOURCES) |
| `SCHEMAS.md` | frontmatter 스키마 (workitem·source·assumption·session·team·conflict) |
| `KICKOFF.md` | 신규 팀 프로젝트 초기화 |
| `ADOPT.md` | 기존 코드 채택 (as-built 역문서화) |
| `DEVELOP.md` | 기여자 개발 프롬프트 (claim → 검출 → 작업) |
| `INTEGRATE.md` | maintainer 통합 프롬프트 (재검출 → merge → history) |
| `AUDIT.md` | 팀 문서 감사 (표류 + 조율 무결성) |
| `templates/` | 스키마 복사용 예시 파일 |
