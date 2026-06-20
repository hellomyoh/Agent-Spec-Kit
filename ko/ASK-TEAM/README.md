# ASK-Team — 팀 개발용 Agent-Spec-Kit

> 여러 개발자와 여러 AI 에이전트가 **동시에** 개발할 때 발생하는
> Git 충돌·의미 충돌·의도 충돌을 markdown + git만으로 줄이는 프레임워크.
> 기존 [Agent-Spec-Kit](../AGENTSPECKIT/)(1인/순차)의 **자매 프레임워크**입니다.

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
| **Maintainer (1+)** | 전역 계약·로드맵 소유, `INTEGRATE` 실행, 의미/의도 충돌 중재, 계약변경 ADR 승인 | `ARCHITECTURE.md`, `PLAN.md`, `AGENTS.md`, `history/`, 생성 INDEX |
| **Contributor (N, 인간/에이전트)** | workitem claim, 브랜치 작업, scoped 파일 작성, PR | 자기 `WI-*.md`, 자기 작업층 파일 |

다중 인간의 **의도 충돌**(서로 다른 사람이 모순되는 요구를 제출)은 파일 구조가 아니라 **거버넌스**로 풉니다 — maintainer가 중재하고 ADR로 기록합니다. 도구는 충돌을 *표면화*할 뿐 합의를 만들지 않습니다.

---

## 3. 디렉토리 구조

프로젝트에 적용하면 모든 산출물은 `AGENTSPECKIT/` 아래에 생성됩니다(루트 3파일 예외: 프로젝트 `README.md`·`AGENTS.md`·`CLAUDE.md`). 기존 ASK와 동일한 루트 규약입니다.

```text
AGENTSPECKIT/
  # 프롬프트
  KICKOFF.md  ADOPT.md  DEVELOP.md  INTEGRATE.md  AUDIT.md
  askctl.py                      # 조율 도구 (index 생성 · detect · whoami)
  .gitignore                     # 생성 INDEX.md 제외

  # 조율층 (공유 브랜치, maintainer single-writer 영역 포함)
  ARCHITECTURE.md                # 단일·강제로드 — maintainer만 수정
  PLAN.md                        # 안정 로드맵 — maintainer만 수정
  PROGRESS.md                    # 호환 진입점 (정적 스텁 — 인덱스로 안내)
  workitems/  WI-*.md            (INDEX.md = 생성)
  conflicts/  CF-*.md            (INDEX.md = 생성)

  # 식별
  team/       <handle>.md        (INDEX.md = 생성)

  # 작업층 (feature 브랜치, 항목별 single-writer)
  sessions/   <handle>--<WI-id>.md   archive/   (INDEX.md = 생성)
  history/    YYYY/MM/HIST-*.md                  (INDEX.md = 생성, INTEGRATE가 기록)
  assumptions/ ASM-*.md                          (INDEX.md = 생성)
  notes/      <topic>.md  <topic>/*.md           (INDEX.md = 생성)

  # 입력
  SOURCES/
    REQUIREMENTS.md              # 초기 요구사항 (동결 유지)
    SRC-*.md                     # 불변 원본 content
    SRC-*.meta.md                # 가변 triage (per-source single-writer)
    INDEX.md                     # 생성

  # 명세·리뷰 하네스 (유지 — 논문 핵심 기여)
  features/*.md   personas/*.md   discussion/review-*.md   adr/ADR-*.md   docs/  qa/

  templates/                     # 스키마 예시 (askctl이 스캔에서 제외)
```

> `locks/`는 두지 않습니다. advisory lock은 강제수단이 없고 stale-lock에 무방비라, 전역 계약 보호는 **maintainer single-writer + ADR 게이트 + merge 순서**로 대체합니다(§7, CONVENTIONS §6).

---

## 4. 식별 — git identity에 정박

개발자 식별을 새로 발명하지 않습니다. **모든 커밋에 이미 있는 git identity**(email)를 기준으로 삼고, `team/` 레지스트리로 검증합니다.

- **기준 키:** `git config user.email` (고유). `user.name`은 표시용.
- **두 축:** 책임 주체(인간 = commit author) / 실행자(에이전트 = `Co-Authored-By` 트레일러).
- **레지스트리:** `team/<handle>.md` (per-person, single-writer) + 생성 `team/INDEX.md`.
- **자동 해소:** `python askctl.py whoami` → git email을 레지스트리와 매칭해 `handle`·`role` 반환. 미등록이면 진입 차단.
- **신뢰 모델:** 소프트 식별(귀속·충돌회피·검증)은 markdown이 제공, 하드 식별(사칭 차단)은 git 플랫폼(protected branch · signed commit · CODEOWNERS)에 위임.

상세 규약은 [CONVENTIONS.md §2](CONVENTIONS.md)를 참조하세요.

---

## 5. 상태 & 인덱스 — 생성물로 통일

직전 설계 논의가 수렴한 키스톤 결정입니다. **단일 메커니즘을 모든 디렉토리에 균일 적용합니다.**

```text
- 진실의 출처(SoT) = 각 항목 파일의 frontmatter (단일 작성자가 자기 파일만 씀)
- INDEX.md = askctl이 frontmatter를 스캔해 만든 생성물
    · .gitignore 처리 → git에 커밋하지 않음 → 충돌 0, stale 0
    · 세션 시작 필수 스텝: `python askctl.py index` 실행 후 읽기
    · 손으로 INDEX.md를 수정하지 않는다 (덮어쓰여짐)
```

효과:
- **INDEX 동시수정 충돌이 구조적으로 불가능**(아무도 손으로 안 씀).
- status table에 `merge=union`을 걸 때의 행-중복 silent corruption 문제 **소멸**(INDEX가 git에 없음).
- 결정적 스크립트라 인덱스 생성에 **LLM 토큰 0**.
- 트레이드오프: GitHub 웹에선 INDEX가 안 보임 → `askctl.py index`로 생성. 에이전트-우선 프레임워크라 수용.

---

## 6. 의미 충돌 검출 & 전역 계약 직렬화

**검출 트리거 (claim · integrate 두 지점에서 자동 실행):**

```text
python askctl.py detect <WI-id>
  내 touches vs status ∈ {claimed, in_progress} 인 다른 workitem 전수 교차
    · contracts 겹침 → STOP. maintainer가 직렬화(아래)
    · modules 겹침   → WARN. conflicts/CF-*.md 등재 + 순서 합의
    · 없음           → OK. 진행
```

**전역 계약 직렬화 (locks 대신):**

```text
ARCHITECTURE / 전역 계약 변경 =
  ① touches.contracts 선언한 전용 workitem + ADR(Proposed)
  ② askctl detect → 같은 contract touch하는 in-flight workitem에 STOP 통지
  ③ maintainer가 계약변경 workitem을 먼저 merge, ADR→Accepted, ARCHITECTURE 갱신
     (maintainer가 ARCHITECTURE single-writer → 동시편집 원천 차단)
  ④ 의존 workitem들이 새 계약으로 rebase
```

---

## 7. 개발 흐름

```text
1. 요구 수집      SOURCES/SRC-*.md (불변 원본) + SRC-*.meta.md (triage)
2. 분해 / claim   workitems/WI-*.md 작성(touches) → 공유 브랜치 커밋 → askctl detect
3. 개발           feat/WI-* 브랜치: 코드 + feature/qa/notes/assumptions (작업층)
                  비자명 기능은 personas/discussion 리뷰
4. review         WI status=review, PR
5. INTEGRATE      maintainer: touches 재교차 → merge → history 기록
                  → SRC-*.meta status=applied → PLAN 갱신 → askctl index → 전체 회귀
6. audit          주기적: 고아 WI / 미검출 touches / 방치 SRC / 링크 무결성
```

**원자 커밋(재정의):** feature 브랜치의 원자 커밋 = **코드 + 그 workitem의 작업층 파일**. 생성 INDEX, ARCHITECTURE/PLAN(maintainer), history(INTEGRATE)는 **포함하지 않습니다**. "코드와 대응 문서를 한 커밋에"라는 원칙은 *workitem 스코프 내에서* 유지됩니다.

---

## 8. 빠른 시작

1. 이 저장소를 clone하고 `ko/ASK-TEAM/`의 내용을 프로젝트 루트의 `AGENTSPECKIT/`로 복사합니다.
2. **Maintainer가** `team/<handle>.md`를 본인 것부터 등록하고 `role: maintainer`로 둡니다. 각 기여자도 자기 `team/<handle>.md`를 등록합니다.
3. 세션 시작 시 항상:
   ```bash
   python AGENTSPECKIT/askctl.py whoami     # 내 handle/role 확인
   python AGENTSPECKIT/askctl.py index      # 인덱스 재생성 후 읽기
   ```
4. 기여자는 `DEVELOP.md`, maintainer는 `INTEGRATE.md` 프롬프트로 작업합니다.

> 초기화(KICKOFF)·채택(ADOPT)·감사(AUDIT) 프롬프트는 solo ASK의 것을 팀 규약에 맞게 확장해 쓰며, 본 릴리스에서는 핵심 3종(`DEVELOP`·`INTEGRATE` + `askctl`)을 먼저 확정합니다.

---

## 9. solo ASK와의 차이

| 항목 | solo ASK | ASK-Team |
|---|---|---|
| 진행 상태 | `PROGRESS.md` 단일 커서 | `workitems/` + `sessions/<handle>--<WI>` |
| 이력 | `HISTORY.md` append | `history/YYYY/MM/HIST-*.md` (INTEGRATE 기록) |
| 가정 | `ASSUMPTIONS.md` 단일 | `assumptions/ASM-*.md` |
| 노트 | `NOTES.md` 단일 | `notes/<topic>.md` |
| 요구 상태 | `SOURCES/INDEX.md` 행(가변) | `SRC-*.meta.md` (per-source) + 생성 INDEX |
| 인덱스 | 손으로 갱신 | **생성물 (gitignore)** |
| 식별 | 불필요 | `team/` + git identity + `askctl whoami` |
| 의미 충돌 | 해당 없음 | `touches` + `askctl detect` + `conflicts/` |
| 전역 계약 | ADR | ADR + **maintainer single-writer + merge 순서** |

---

## 10. 솔직한 한계 (근거 없는 긍정 금지)

1. **거버넌스 ≠ 도구.** 다중 인간 의도 충돌은 maintainer 중재로만 풀립니다. 프레임워크는 충돌을 표면화할 뿐 합의를 만들지 못합니다.
2. **검출 ≠ 강제.** `touches` 미선언/오선언이면 검출이 실패합니다. INTEGRATE의 전수교차가 마지막 그물이지만 사후입니다.
3. **비용은 의도된 대가.** 세션당 오버헤드(고정로드 증가)와 maintainer의 INTEGRATE 부담을 수용합니다. 1인이라면 solo ASK가 더 쌉니다.
4. **단일 실패점.** maintainer가 병목이 될 수 있습니다 → maintainer 복수화는 가능하되 ARCHITECTURE single-writer 규율은 영역 분할로 유지합니다.
5. **INDEX 비가시성.** gitignore 대가로 웹 브라우징 시 인덱스가 없습니다 → `askctl.py index`로 생성합니다.

---

## 11. 이 킷의 구성 파일

| 파일 | 역할 |
|---|---|
| `README.md` | 이 문서 — 프레임워크 개요·사양 |
| `CONVENTIONS.md` | 구조 규약 (파일 등급·식별·INDEX·충돌·계약·원자커밋·SOURCES) |
| `SCHEMAS.md` | frontmatter 스키마 (workitem·source·assumption·session·team·conflict) |
| `DEVELOP.md` | 기여자 개발 프롬프트 (claim → detect → 작업) |
| `INTEGRATE.md` | maintainer 통합 프롬프트 (재교차 → merge → history → index) |
| `askctl.py` | 조율 도구 (`index` · `detect` · `whoami`) |
| `.gitignore` | 생성 INDEX.md 제외 규칙 |
| `templates/` | 스키마 복사용 예시 파일 |
