# KICKOFF.md — 팀 프로젝트 초기화 (ASK-Team)

`SOURCES/REQUIREMENTS.md`(초기 요구사항)를 기준으로 **팀 동시 개발이 가능한 상태**로 프로젝트를 초기화합니다.
이 단계의 목적은 실제 개발이 아니라, 여러 기여자가 충돌 없이 작업을 claim·진행할 수 있도록 **조율 구조 + 초기 산출물**을 만드는 것입니다.

> 규약은 [CONVENTIONS.md](CONVENTIONS.md), 스키마는 [SCHEMAS.md](SCHEMAS.md)가 우선합니다.
> 기능명세/페르소나/QA 문서의 **세부 형식**은 solo 킷 [KICKOFF.md](../AGENTSPECKIT/KICKOFF.md) 6·8절을 그대로 따릅니다 — 여기서는 **팀 구조 차이만** 규정합니다.

> **재초기화 금지:** `SOURCES/INDEX.md`에서 REQUIREMENTS의 상태가 이미 `applied`면 KICKOFF를 다시 실행하지 않습니다.
> **이 프롬프트는 maintainer가 실행**합니다(초기화 = 전역 계약·구조 확정).

---

# 1. 생성할 구조

루트 3파일(프로젝트 `README.md`·`AGENTS.md`·`CLAUDE.md`)을 제외하고 모두 `AGENTSPECKIT/` 아래에 만듭니다.

```text
AGENTSPECKIT/
  KICKOFF.md ADOPT.md DEVELOP.md INTEGRATE.md AUDIT.md   # 복사된 프롬프트
  askctl.py  .gitignore
  ARCHITECTURE.md  PLAN.md  PROGRESS.md(호환 스텁)
  team/        <maintainer-handle>.md                    # ★ 최소 1명(초기화 실행자) 등록
  workitems/   WI-*.md                                   # 초기 작업 분해 (status: proposed)
  conflicts/                                             # 빈 폴더
  sessions/    archive/                                  # 빈 폴더
  history/                                               # 빈 폴더
  assumptions/ ASM-*.md                                  # 초기 자율 판단
  notes/                                                 # 빈 골격
  SOURCES/     REQUIREMENTS.md  SRC-*.md  SRC-*.meta.md
  features/*.md  personas/*.md  discussion/  adr/ADR-*.md  docs/  qa/
  templates/
```

* 모든 `INDEX.md`는 손으로 만들지 않습니다 — `python askctl.py index`가 생성합니다(§7).
* solo 킷의 단일 파일(`HISTORY.md`/`ASSUMPTIONS.md`/`NOTES.md`/`TODO.md`)은 **만들지 않습니다.** 각각 `history/`·`assumptions/`·`notes/`·workitem `proposed`로 대체됩니다.

---

# 2. 요구사항 명확화 / AI 위임

solo 킷 [KICKOFF.md](../AGENTSPECKIT/KICKOFF.md) 2절(질문 기준·기본값·`[AI 위임]` 처리)을 그대로 따릅니다.
**팀 차이:** 자율 판단으로 채택한 결정은 단일 `ASSUMPTIONS.md`가 아니라 `assumptions/ASM-*.md` **개별 파일**로 기록합니다(`scope` 필드 포함 — 충돌 점검용).

---

# 3. 초기화 작업 순서

각 단계가 끝날 때마다 진행 상태를 갱신합니다. 초기화가 중단되면 다음 세션이 이어받습니다(상태는 `workitems/`와 `PROGRESS.md` 스텁이 가리키는 인덱스로 파악).

1. **maintainer 등록** — 초기화 실행자를 `team/<handle>.md`(`role: maintainer`)로 등록. `python askctl.py whoami`로 git identity 매칭 확인.
2. `SOURCES/REQUIREMENTS.md` 분석 — `SRC-*.meta.md` 상태를 `under_review`로. 다른 제출 자료가 있으면 함께 등록.
3. 필수 요구 충족 여부 확인 / 모호하면 질문(2절).
4. 프로젝트 목적·범위 정리.
5. **횡단 계약 → `ARCHITECTURE.md`** 초안 (maintainer single-writer 영역).
6. MVP/후순위 분리.
7. 기능 단위 분해 → `features/*.md` (형식은 solo 6.1) + 비자명 기능은 `personas/`+`discussion/` 리뷰(solo 4·5절).
8. **작업 분해 → `workitems/WI-*.md`** (status: `proposed`). 각 WI에 `touches`(contracts/modules)·`feature`·`source_refs`를 채웁니다. 초기 백로그가 곧 workitem 목록입니다.
9. QA 문서(`qa/`) 작성(형식은 solo 8절).
10. 사용자 문서(`docs/`) 작성.
11. 중요한 설계 결정 → `adr/ADR-<YYYYMMDD>-<slug>.md` + INDEX(생성).
12. `ARCHITECTURE.md` 확정.
13. 프로젝트 `README.md` 초안(루트).
14. **`AGENTS.md` 작성**(루트) — 팀 규약 포함(아래 4절).
15. `PLAN.md` 작성(안정 로드맵 — Phase 수준만, 작업 상태는 workitems가 가짐).
16. `PROGRESS.md` 호환 스텁 작성(5절).
17. 초기 자율 판단 → `assumptions/ASM-*.md`.
18. `SOURCES/SRC-*.meta.md`의 REQUIREMENTS 상태를 `applied`로(**동결 시점**), 반영 산출물 링크.
19. `CLAUDE.md` 작성(루트 — solo 11절 오작동 방지 + 팀 항목: "전역 계약은 maintainer만, INDEX는 손대지 않음").
20. **`.gitignore` 확인** — 모든 `INDEX.md` 제외.
21. `python askctl.py index` 실행 → 인덱스 생성.
22. 초기화 완료 보고(8절).

---

# 4. AGENTS.md에 포함할 팀 규약

solo 킷 9·10절 내용에 더해 **반드시** 포함:

```text
- 역할: maintainer(전역 계약·INTEGRATE·중재) / contributor(workitem claim·작업). 세션 시작 시 `askctl whoami`로 역할 확인.
- 식별: git identity 정박. owner는 team/<handle>.md의 handle. commit에 Session-Id / Co-Authored-By 트레일러.
- 진행 상태: PROGRESS.md가 아니라 workitems/WI-*.md(+생성 INDEX). 세션 커서는 sessions/<handle>--<WI-id>.md.
- 충돌: claim 직후·integrate 직전 `askctl detect <WI-id>`. contracts 겹침=STOP, modules 겹침=conflicts/CF 등재.
- 전역 계약(ARCHITECTURE/PLAN): maintainer single-writer. 변경은 ADR + detect 통지 + merge 우선(직렬화).
- INDEX.md: 생성물, git 미추적. 손대지 않음. 세션 시작 시 `askctl index` 먼저 실행.
- 원자 커밋: 코드 + 그 workitem 작업층 파일만. ARCHITECTURE/PLAN/history/INDEX는 제외.
- 새 사건은 새 파일: history/assumptions/conflicts에 append하지 말고 파일 생성.
- 통합은 maintainer가 INTEGRATE.md로. 기여자는 PR까지.
```

---

# 5. PROGRESS.md 호환 스텁

```md
# Progress (multi-worker mode)

진행 상태의 진실은 이 파일이 아니라 아래 인덱스입니다. 이 파일에 작업을 직접 기록하지 마세요.

- workitems/INDEX.md  — 작업 상태 (`askctl index`로 생성)
- sessions/INDEX.md   — 세션별 재개 커서
- history/INDEX.md    — 완료 이력

세션 시작: `python AGENTSPECKIT/askctl.py whoami && python AGENTSPECKIT/askctl.py index`
```

---

# 6. Multi-Agent 리뷰 / 페르소나 / 기능명세

solo 킷 4·5·6절을 그대로 따릅니다(`personas/` 인스턴스, `discussion/` 로그, feature 문서 구조·검토 요약·출처 의무). 팀에서도 이 산출물들은 파일 단위라 동시성 안전합니다.

---

# 7. 인덱스 생성

`python askctl.py index`는 `workitems`·`conflicts`·`team`·`sessions`·`history`·`assumptions`·`notes`·`SOURCES`의 INDEX.md를 frontmatter에서 생성합니다. 손으로 만들거나 수정하지 마세요(덮어쓰여짐). git에 커밋하지 않습니다(`.gitignore`).

---

# 8. 완료 조건 / 보고

* `team/`에 maintainer 1명 이상 등록, `askctl whoami` 성공
* `ARCHITECTURE.md`·`PLAN.md`·프로젝트 `README.md`·`AGENTS.md`·`CLAUDE.md` 생성
* `features/*.md`(+ 비자명 기능 `discussion/` 로그)·`qa/`·`docs/`·`adr/` 생성
* **초기 `workitems/WI-*.md`(status: proposed) 생성, 각 `touches` 채움**
* `SOURCES/`의 REQUIREMENTS가 `applied`로 동결, `SRC-*.meta.md` 작성
* `.gitignore`로 INDEX 제외, `askctl index` 1회 실행 성공

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
