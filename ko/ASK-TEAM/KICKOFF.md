# KICKOFF.md — 팀 프로젝트 초기화 (ASK-Team)

`SOURCES/REQUIREMENTS.md`(초기 요구사항)를 기준으로 **팀 동시 개발이 가능한 상태**로 프로젝트를 초기화합니다.
이 단계의 목적은 실제 개발이 아니라, 여러 기여자가 충돌 없이 작업을 claim·진행할 수 있도록 **조율 구조 + 초기 산출물**을 만드는 것입니다.

> 규약은 [CONVENTIONS.md](CONVENTIONS.md), 스키마는 [SCHEMAS.md](SCHEMAS.md)가 우선합니다.
> 기능명세/페르소나/QA 문서의 **세부 형식**은 solo 킷 KICKOFF.md 6·8절을 그대로 따릅니다([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md) — 동봉된 참조 사본, 충돌 시 팀 킷 우선) — 여기서는 **팀 구조 차이만** 규정합니다.
> 이 킷은 markdown + git만 씁니다(추가 런타임 없음). "신원 확인"·"목록 읽기"는 에이전트가 `git`·파일 읽기로 직접 수행합니다.

> **재초기화 금지:** REQUIREMENTS의 상태(`SOURCES/REQUIREMENTS.meta.md`)가 이미 `applied`면 KICKOFF를 다시 실행하지 않습니다.
> **이 프롬프트는 maintainer가 실행**합니다(초기화 = 전역 계약·구조 확정).

---

# 1. 생성할 구조

루트 3파일(프로젝트 `README.md`·`AGENTS.md`·`CLAUDE.md`)을 제외하고 모두 `AGENTSPECKIT/` 아래에 만듭니다.

```text
AGENTSPECKIT/
  KICKOFF.md ADOPT.md DEVELOP.md INTEGRATE.md AUDIT.md   # 복사된 프롬프트 (markdown only)
  ARCHITECTURE.md  PLAN.md  PROGRESS.md(호환 스텁)
  team/        <maintainer-handle>.md                    # ★ 최소 1명(초기화 실행자) 등록
  workitems/   WI-*.md    archive/                       # 초기 작업 분해 (status: proposed); archive/ = done 항목, INTEGRATE가 이동 (§9)
  conflicts/                                             # 빈 폴더
  sessions/    archive/                                  # 빈 폴더
  history/                                               # 빈 폴더
  assumptions/ ASM-*.md                                  # 초기 자율 판단
  notes/                                                 # 빈 골격
  SOURCES/     REQUIREMENTS.md  SRC-*.md  SRC-*.meta.md
  features/*.md  personas/*.md  discussion/  adr/ADR-*.md  docs/  qa/
  templates/
  reference/                                             # 동봉된 솔로 킷 참조 사본 (실행 프롬프트 아님)
```

* **고정 INDEX 파일을 만들지 않습니다.** 디렉토리별 목록·상태는 항목 파일의 frontmatter가 SoT이며 에이전트가 직접 읽습니다(§7).
* solo 킷의 단일 파일(`HISTORY.md`/`ASSUMPTIONS.md`/`NOTES.md`/`TODO.md`)은 **만들지 않습니다.** 각각 `history/`·`assumptions/`·`notes/`·workitem `proposed`로 대체됩니다.
* git은 빈 디렉토리를 추적하지 않습니다 — 비어 있는 채로 시작하는 디렉토리(`conflicts/`, `sessions/archive/`, `workitems/archive/`, `history/`, `notes/`, `discussion/`)에는 `.gitkeep`(빈 파일)을 넣어 commit/clone 후에도 구조가 남게 합니다.

---

# 2. 요구사항 명확화 / AI 위임

solo 킷 KICKOFF.md 2절([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md))(질문 기준·기본값·`[AI 위임]` 처리)을 그대로 따릅니다.
**팀 차이:** 자율 판단으로 채택한 결정은 단일 `ASSUMPTIONS.md`가 아니라 `assumptions/ASM-*.md` **개별 파일**로 기록합니다(`scope` 필드 포함 — 충돌 점검용).

---

# 3. 초기화 작업 순서

각 단계가 끝날 때마다 진행 상태를 갱신합니다. 초기화가 중단되면 다음 세션이 `workitems/`와 `PROGRESS.md` 스텁을 읽고 이어받습니다.

1. **maintainer 등록** — 초기화 실행자를 `team/<handle>.md`(`role: maintainer`)로 등록. `git config user.email`이 그 파일의 `emails`에 들어가는지 확인(신원 매칭).
2. `SOURCES/REQUIREMENTS.md` 분석 — `SOURCES/REQUIREMENTS.meta.md`를 생성(`id: REQUIREMENTS` — SCHEMAS §source)하고 상태를 `under_review`로. 다른 제출 자료가 있으면 함께 등록(`SRC-*.md` + `SRC-*.meta.md`).
3. 필수 요구 충족 여부 확인 / 모호하면 질문(2절).
4. 프로젝트 목적·범위 정리.
5. **횡단 계약 → `ARCHITECTURE.md`** 초안 (maintainer single-writer 영역).
6. MVP/후순위 분리.
7. 기능 단위 분해 → `features/*.md` (골격은 §6.1, 상세는 solo 6.1) + 비자명 기능은 `personas/`+`discussion/` 리뷰(solo 4·5절 — 6절 참조).
8. **작업 분해 → `workitems/WI-*.md`** (status: `proposed`). 각 WI에 `touches`(contracts/modules)·`feature`·`source_refs`를 채웁니다. 초기 백로그가 곧 workitem 목록입니다.
9. QA 문서(`qa/`) 작성(형식은 solo 8절).
10. 사용자 문서(`docs/`) 작성.
11. 중요한 설계 결정 → `adr/ADR-<YYYYMMDD>-<slug>.md`.
12. `ARCHITECTURE.md` 확정.
13. 프로젝트 `README.md` 초안(루트).
14. **`AGENTS.md` 작성**(루트) — 팀 규약 포함(아래 4절).
15. `PLAN.md` 작성(안정 로드맵 — Phase 수준만, 작업 상태는 workitems가 가짐).
16. `PROGRESS.md` 호환 스텁 작성(5절).
17. 초기 자율 판단 → `assumptions/ASM-*.md`.
18. `SOURCES/REQUIREMENTS.meta.md`의 상태를 `applied`로(**동결 시점**), 반영 산출물 링크.
19. `CLAUDE.md` 작성(루트 — solo 11절 오작동 방지([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md)) + 팀 항목: "전역 계약은 maintainer만, 진행 상태는 workitems frontmatter").
20. 초기화 산출물 commit(§3.1).
21. 초기화 완료 보고(8절).

## 3.1 초기화의 브랜치·commit 규칙

* 초기화는 maintainer가 **공유 브랜치에서** 수행합니다(CONVENTIONS §4.5 — 신규 저장소면 기본 브랜치; 공유 브랜치가 push 보호 중이면 지정한 `coordination` 브랜치에서 초기화하고 AGENTS.md에 기록).
* 초기화는 생성한 산출물 전체(루트 3파일 + AGENTSPECKIT/)를 묶는 **commit으로 끝나며**, 원격이 있으면 push합니다 — 조율층이 공유 브랜치에 올라가야 기여자가 볼 수 있으므로, **이 commit 전에는 claim을 시작할 수 없습니다.**
* 초기화가 여러 세션에 걸치면 의미 있는 중간 지점 commit을 해도 됩니다(예: ARCHITECTURE/features 완성 후).

---

# 4. AGENTS.md에 포함할 팀 규약

solo 킷 9·10절 내용에 더해 **반드시** 포함:

```text
- 런타임 없음: 이 킷은 markdown + git만 사용한다. 추가 도구·바이너리를 요구하지 않는다.
- 역할: maintainer(전역 계약·INTEGRATE·중재) / contributor(workitem claim·작업). 세션 시작 시 신원 확인.
- 식별: git identity 정박. 에이전트가 `git config user.email`을 team/<handle>.md의 emails와 매칭. owner는 handle. commit에 Session-Id / Co-Authored-By 트레일러.
- 진행 상태: PROGRESS.md가 아니라 workitems/WI-*.md frontmatter(고정 INDEX 없음 — 직접 읽음). 세션 커서는 sessions/<handle>--<WI-id>.md.
- 공유 브랜치: <KICKOFF에서 결정한 이름 — 기본 브랜치 또는 'coordination'> (CONVENTIONS §4.5). 조율 파일(workitems/conflicts/team/personas)은 여기에 직접 커밋·push하고, 코드는 PR로만 도달한다. WI 파일은 공유 브랜치에서만 편집한다.
- 충돌: claim 직후·integrate 직전, 먼저 git fetch한 뒤 최신 공유 브랜치의 workitems/*.md(claimed/in_progress)를 읽어 touches 교차. contracts 겹침=STOP, modules 겹침=conflicts/CF 등재.
- 전역 계약(ARCHITECTURE/PLAN): maintainer single-writer. 변경은 ADR + 검출 통지 + merge 우선(직렬화).
- 목록은 frontmatter에서 직접 읽는다. 고정 INDEX 파일을 만들지 않는다. 사람용 표가 필요하면 그때 생성해 보여주되 파일로 커밋하지 않는다.
- 원자 커밋: 코드 + 그 workitem 작업층 파일만. ARCHITECTURE/PLAN/history는 제외.
- 새 사건은 새 파일: history/assumptions/conflicts에 append하지 말고 파일 생성.
- 통합은 maintainer가 INTEGRATE.md로. 기여자는 PR까지.
```

---

# 5. PROGRESS.md 호환 스텁

```md
# Progress (multi-worker mode)

진행 상태의 진실은 이 파일이 아니라 각 항목 파일의 frontmatter입니다. 이 파일에 작업을 직접 기록하지 마세요.
고정 INDEX 파일은 두지 않습니다 — 에이전트가 아래 디렉토리의 *.md frontmatter를 직접 읽습니다.

- workitems/*.md   — 작업 상태 (SoT)
- sessions/*.md    — 세션별 재개 커서
- history/**       — 완료 이력

세션 시작: 에이전트가 `git config user.email`로 신원을 확인하고, 현재 작업에 필요한 항목 파일을 직접 읽습니다.
```

---

# 6. Multi-Agent 리뷰 / 페르소나 / 기능명세

solo 킷 4·5·6절을 그대로 따릅니다([reference/SOLO-KICKOFF.md](reference/SOLO-KICKOFF.md)) — `personas/` 인스턴스, `discussion/` 로그, feature 문서 구조·검토 요약·출처 의무. 팀에서도 이 산출물들은 파일 단위라 동시성 안전합니다.

**예외(고정 INDEX 없음 — CONVENTIONS §3):** 해당 solo 절이 의무화하는 목록 인덱스 파일은 만들지 **않습니다** — `personas/INDEX.md`(solo 5.2), `features/README.md`(solo 6.2), `docs/README.md`(solo 7.2), `adr/INDEX.md`(solo 16절) — "같은 commit에서 인덱스 갱신" 규칙도 적용하지 않습니다. 목록은 파일에서 직접 읽고, 작업 상태는 workitem frontmatter가 가집니다. (`qa/README.md`는 목록이 아니라 QA 운영 기준 문서이므로 그대로 작성합니다.)

서브에이전트 도구가 가능한 환경이면 핵심 기능은 **실제 병렬 서브에이전트**로 검토합니다(실행 방식·서브에이전트별 증거는 solo 4.1). 새 페르소나 인스턴스는 **공유 브랜치에서** 생성합니다 — 먼저 `git fetch`하여 그 역할의 인스턴스가 이미 없는지 확인합니다(CONVENTIONS §1·§4.5).

## 6.1 feature 문서 골격 (인라인)

```md
# Feature: <기능명>
## 1. 목적        ## 2. 범위 (In / Out of scope)        ## 3. 사용자 시나리오
## 4. 최종 합의안 (+ 검토 요약: 참여 페르소나 · 주요 쟁점 · 결론 3–4줄 · discussion 로그 링크)
## 5. 기능 요구사항        ## 6. 비기능 요구사항
## 7. 데이터 설계   ## 8. API 설계   ## 9. UI/UX 설계   (각: 해당 없으면 `해당 없음`; 공통 규칙 → ARCHITECTURE.md 참조)
## 10. 보안 요구사항         ## 11. 로그 / 분석 요구사항
## 12. 테스트 시나리오 (자동 / 수동 QA / 예외 케이스 / 회귀 영향)
## 13. 완료 조건 ("관련 자동 테스트가 실제 실행되어 통과" 포함 필수)
## 14. 참조 ADR               ## 15. 미결 사항
```

(절별 상세 가이드: 참조 사본의 solo 6.1.)

---

# 7. 목록·상태 파악 (고정 INDEX 없음)

진행 상태·작업 목록은 별도 INDEX 파일을 두지 않습니다. 에이전트가 `workitems/`·`assumptions/`·`history/`·`SOURCES/`·`team/` 등의 `*.md` frontmatter를 **직접 읽어** 파악합니다(선택 로딩 — 필요한 것만). 사람이 읽을 집계 표가 필요하면 그때 에이전트에게 요청해 markdown으로 받습니다(파일로 강제 생성·커밋하지 않습니다 — staleness·동시수정 충돌 원천 차단).

---

# 8. 완료 조건 / 보고

* `team/`에 maintainer 1명 이상 등록, `git config user.email`이 그 파일과 매칭
* `ARCHITECTURE.md`·`PLAN.md`·프로젝트 `README.md`·`AGENTS.md`·`CLAUDE.md` 생성
* `features/*.md`(+ 비자명 기능 `discussion/` 로그)·`qa/`·`docs/`·`adr/` 생성
* **초기 `workitems/WI-*.md`(status: proposed) 생성, 각 `touches` 채움**
* `SOURCES/`의 REQUIREMENTS가 `applied`로 동결(`SOURCES/REQUIREMENTS.meta.md` 작성)
* 고정 목록-INDEX 파일을 만들지 않음(personas/features/docs/adr — 6절 예외)
* 초기화가 공유 브랜치에 commit됨(§3.1), 빈 디렉토리에 `.gitkeep`

보고 형식:

```md
# 팀 프로젝트 초기화 결과
## 등록한 team 멤버 / 역할
## 생성한 구조 / 횡단 계약(ARCHITECTURE) 요약
## 기능명세 목록 / 초기 workitem 목록(touches 포함)
## ADR / QA / docs 목록
## AI 위임으로 결정한 항목 (검토 권장)
## 다음 단계 (첫 claim 후보 / DEVELOP.md 안내)
```
