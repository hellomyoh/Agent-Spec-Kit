<div align="center">

# THROUGHLINE — Team 에디션

**여러 개발자와 AI 에이전트가 한 코드베이스를 공유할 때의 명세 주도 개발**

모든 워크아이템이 자기가 건드리는 범위를 claim 시점에 공유 브랜치로 게시합니다 —
그래서 Git 충돌·의미 충돌·의도 충돌이 머지 때가 아니라 조기에 드러납니다.

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Claude Code · Codex · Cursor](https://img.shields.io/badge/agents-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor-blue)](#빠른-시작)

🌐 [English](README.team.md) · **한국어**

[빠른 시작](#빠른-시작) · [Solo 에디션](README.ko.md) · [팀 전체 가이드·프롬프트](ko/THROUGHLINE-TEAM/) · [English kit](en/THROUGHLINE-TEAM/)

</div>

---

## Solo와 Team 중 무엇을?

| | **Solo (THROUGHLINE)** — [README.ko.md](README.ko.md) | **Team (THROUGHLINE Team)** — 이 문서 |
|---|---|---|
| 대상 | 1인 / 순차·자율 개발 | 다수 개발자·AI 에이전트 **동시** 개발 |
| 진행 상태 | 단일 `PROGRESS.md` 커서 | `workitems/` + `sessions/<handle>--<WI>` |
| 이력 / 가정 / 노트 | 단일 파일 | `history/` · `assumptions/` · `notes/` 디렉토리 |
| 인덱스 | 손으로 갱신 | 없음 — frontmatter 직접 읽기 |
| 충돌 | 해당 없음 | `touches` + `conflicts/` (에이전트가 교차 점검) |
| 식별 | 불필요 | `team/` + git identity (`git config user.email`) |
| 런타임 | 없음 | 없음 (markdown + git만) |
| 키트 폴더 | `ko/THROUGHLINE/` · `en/THROUGHLINE/` | `ko/THROUGHLINE-TEAM/` · `en/THROUGHLINE-TEAM/` |

1인 개발이면 Solo가 더 가볍습니다 — 실제로 N명이 동시에 개발할 때만 Team을 쓰세요.

## 핵심 아이디어

- **git 브랜치 격리가 근본 사실.** 기여자는 서로의 *커밋되지 않은* 파일을 볼 수 없으므로, 워크아이템의 조정 메타데이터(`touches`)를 **claim 시점에 공유 브랜치로 게시**합니다 → 충돌이 머지 때가 아니라 조기에 드러납니다.
- **산출물 2계층.** *Coordination*(workitems·conflicts·`ARCHITECTURE.md`/`PLAN.md`)은 공유 브랜치에, *Work*(코드·기능명세·qa·노트·가정)는 격리된 피처 브랜치에 둡니다.
- **역할.** **Maintainer**가 전역 계약을 소유하고 `INTEGRATE`를 수행하며 의도 충돌을 ADR로 중재합니다. **Contributor**는 워크아이템을 claim하고 자기 범위 파일만 씁니다.
- **고정 INDEX 파일 없음.** 각 항목 파일의 frontmatter가 진실의 출처이고 에이전트가 디렉토리를 직접 읽으므로, 인덱스 동시 편집 충돌이 아예 없습니다.
- **식별 = git identity.** `git config user.email`을 `team/<handle>.md` 레지스트리로 검증 — 추가 런타임 없음.

## 빠른 시작

**설치할 것 없음** — 마크다운 파일과 git뿐입니다. 런타임·CLI·의존성 없음.

1. 이 저장소를 클론하고 [`ko/THROUGHLINE-TEAM/`](ko/THROUGHLINE-TEAM/)(또는 [`en/THROUGHLINE-TEAM/`](en/THROUGHLINE-TEAM/))의 내용을 프로젝트 루트의 `THROUGHLINE/`로 복사합니다.
2. **신규 프로젝트**면 `THROUGHLINE/SOURCES/REQUIREMENTS.md`에 초기 요구사항을 작성합니다(솔로 킷의 [REQUIREMENTS 템플릿](ko/THROUGHLINE/SOURCES/REQUIREMENTS.md) 재사용 가능); 기존 코드베이스(ADOPT)면 선택 사항입니다.
3. **maintainer**가 `role: maintainer`로 자기 `team/<handle>.md`를 먼저 등록하고(`templates/team-TEMPLATE.md` 복사), 각 **contributor**도 자기 것을 등록합니다.
4. Contributor는 [`DEVELOP.md`](ko/THROUGHLINE-TEAM/DEVELOP.md) 프롬프트로, maintainer는 [`INTEGRATE.md`](ko/THROUGHLINE-TEAM/INTEGRATE.md)로 작업합니다. 초기화는 [`KICKOFF.md`](ko/THROUGHLINE-TEAM/KICKOFF.md)(신규) / [`ADOPT.md`](ko/THROUGHLINE-TEAM/ADOPT.md)(기존 코드), 주기 점검은 [`AUDIT.md`](ko/THROUGHLINE-TEAM/AUDIT.md)를 사용합니다.

초기화가 올라간 뒤에는 `AGENTS.md`가 매 실행마다 로드되므로, claim한 workitem 안에서의 일상 작업은 붙여넣기 없이도 됩니다 → [프롬프트 없이 쓰기](#프롬프트-없이-쓰기).

> 각 단계에서 그대로 붙여넣어 쓸 수 있는 프롬프트는 아래 [프롬프트](#프롬프트-그대로-붙여넣어-사용) 절에 있습니다. 모든 프롬프트는 프로젝트 루트에 복사된 `THROUGHLINE/`를 기준으로 경로를 씁니다(루트 3파일 `README.md`·`AGENTS.md`·`CLAUDE.md` 예외).

---


## 프롬프트 (그대로 붙여넣어 사용)

솔로 킷([README.ko.md](README.ko.md) 2·5·7·9.1절)과 같은 방식으로, 아래 프롬프트를 Agent(Claude Code · Codex · Cursor)에 붙여넣어 사용합니다. 각 프롬프트는 해당 킷 파일(`THROUGHLINE/KICKOFF.md` 등)을 읽고 그 지시를 따르게 하는 진입점이며, **실행 주체(maintainer / contributor)**가 정해져 있습니다.

이 킷은 **markdown + git만** 씁니다 — "신원 확인"·"충돌 검출"·"목록 읽기"는 별도 런타임이 아니라 에이전트가 `git` 명령과 파일 읽기로 직접 수행합니다. **고정 INDEX 파일을 만들지 않으며**, 진행 상태의 진실은 각 항목 파일(`workitems/WI-*.md` 등)의 frontmatter입니다.

> **공유 브랜치란?** 조율층 파일(`workitems/`·`conflicts/`·`team/`·`personas/`)을 claim 시점에 즉시 published하는 브랜치입니다(기본 브랜치, 또는 push 보호 시 별도 `coordination` 브랜치 — [CONVENTIONS.md §4.5](ko/THROUGHLINE-TEAM/CONVENTIONS.md)). 이 브랜치에 조율 메타데이터가 올라가야 다른 기여자가 볼 수 있으므로, 초기화 커밋 전에는 누구도 claim을 시작할 수 없습니다. 코드는 이 브랜치에 직접 push하지 않고 **PR로만** 도달합니다.

### A. 초기화 프롬프트 — 신규 팀 프로젝트 (KICKOFF · maintainer)

`THROUGHLINE/SOURCES/REQUIREMENTS.md`(초기 요구사항)를 작성하고, maintainer 본인을 `team/<handle>.md`(`role: maintainer`)로 등록한 뒤 아래 프롬프트를 입력합니다. 실제 구현이 아니라 **여러 기여자가 충돌 없이 claim·진행할 수 있는 조율 구조 + 초기 workitem**을 만드는 단계입니다.

```text
THROUGHLINE/SOURCES/REQUIREMENTS.md 와 THROUGHLINE/KICKOFF.md 를 읽고,
KICKOFF.md의 지시에 따라 이 팀 프로젝트를 "여러 기여자가 충돌 없이 동시에 작업을 claim·진행할 수 있는 상태"로 초기화하세요.
규약은 THROUGHLINE/CONVENTIONS.md, 스키마는 THROUGHLINE/SCHEMAS.md 가 우선합니다.

이 킷은 markdown + git만 사용합니다(추가 런타임 없음). "신원 확인"·"목록 읽기"는 git 명령과 파일 읽기로 직접 수행하세요.
산출물은 루트 3파일(프로젝트 README.md · AGENTS.md · CLAUDE.md)을 제외하고 모두 THROUGHLINE/ 아래에 생성하세요.

먼저 다음 가드를 확인하세요.
- 재초기화 금지: SOURCES/REQUIREMENTS.meta.md 의 상태가 이미 applied 이면 KICKOFF를 다시 실행하지 말고 보고만 하세요.
- 이 프롬프트는 maintainer가 실행합니다(초기화 = 전역 계약·구조 확정).

반드시 다음 순서로 수행하세요 (각 단계 후 진행 상태를 갱신 — 중단되면 workitems/ 와 PROGRESS.md 스텁으로 이어받습니다).

1. maintainer 등록: 초기화 실행자를 team/<handle>.md (role: maintainer)로 등록하세요(templates/team-TEMPLATE.md 복사).
   git config user.email 이 그 파일의 emails 에 들어가는지 확인(신원 매칭).
2. SOURCES/REQUIREMENTS.md 를 분석하고 SOURCES/REQUIREMENTS.meta.md 를 생성(id: REQUIREMENTS)해 상태를 under_review 로 두세요.
   다른 제출 자료가 있으면 SRC-*.md(불변 원본) + SRC-*.meta.md(triage)로 함께 등록하세요.
3. 초기화에 필요한 핵심 요구사항이 충분한지 확인하고, 모호하면(목적·대상 사용자·MVP·데이터·외부 연동·인증/권한·횡단 기준선·QA)
   진행 전에 사용자에게 질문하세요(한 번에 최대 5개, 핵심만). [AI 위임] 항목은 KICKOFF 2절 규칙대로 처리하세요.
4. 프로젝트 목적·범위를 정리하세요.
5. 여러 기능에 공통 적용되는 횡단 계약(데이터 모델/네이밍/API/인증)을 정리해 ARCHITECTURE.md 를 작성하세요(maintainer single-writer 영역).
6. MVP / 후순위를 분리하세요.
7. 기능 단위로 분해해 features/*.md 를 작성하세요(골격 KICKOFF 6.1). 비자명 기능은 personas/ + discussion/ 로 검토하고,
   feature 문서는 발언록이 아니라 최종 합의 명세로 작성하되 참여 페르소나·핵심 쟁점·결론 3~4줄 + 로그 링크를 남기세요.
8. 작업 분해: workitems/WI-*.md 를 status: proposed 로 생성하고, 각 WI에 touches(contracts/modules)·feature·source_refs 를 채우세요.
   이 초기 백로그가 곧 workitem 목록입니다.
9. QA 문서(qa/)를 작성하세요("테스트 통과"는 실제 실행 시에만 인정하는 기준 포함).
10. 사용자 문서(docs/)를 작성하세요.
11. 중요한 설계 결정은 adr/ADR-<YYYYMMDD>-<slug>.md 로 남기세요.
12. ARCHITECTURE.md 를 확정하세요.
13. 프로젝트 README.md(루트) 초안을 작성하세요(민감 정보 금지).
14. AGENTS.md(루트)를 작성하세요 — 아래 [AGENTS.md 팀 규약]을 반드시 포함하세요.
15. PLAN.md(안정 로드맵 — Phase 수준만, 작업 상태는 workitems가 가짐)를 작성하세요.
16. PROGRESS.md 호환 스텁을 작성하세요(진행 상태의 진실은 항목 파일 frontmatter, 여기 직접 기록 금지).
17. 초기 자율 판단을 assumptions/ASM-*.md 개별 파일로 기록하세요(scope 필드 포함 — 단일 ASSUMPTIONS.md 만들지 않음).
18. SOURCES/REQUIREMENTS.meta.md 의 상태를 applied 로 바꾸고(동결 시점) 반영 산출물을 링크하세요.
    이후 REQUIREMENTS.md 원본은 불변이며, 추가 요구는 새 SRC-* 변경요청으로 받습니다.
19. CLAUDE.md(루트)를 작성하세요(오작동 방지 전용 + 팀 항목: "전역 계약은 maintainer만, 진행 상태는 workitems frontmatter").
20. 빈 채로 시작하는 디렉토리(conflicts/, sessions/archive/, workitems/archive/, history/, notes/, discussion/)에 .gitkeep 을 넣으세요.
21. KICKOFF 3.1절에 따라 초기화 산출물 전체(루트 3파일 + THROUGHLINE/)를 공유 브랜치에서 하나의 commit으로 묶고,
    원격이 있으면 push하세요. ★ 이 commit 전에는 어떤 기여자도 claim을 시작할 수 없습니다.
    (공유 브랜치가 push 보호 중이면 지정한 coordination 브랜치에서 초기화하고 AGENTS.md에 기록.)

고정 INDEX 파일을 만들지 마세요 — personas/INDEX.md · features/README.md · docs/README.md · adr/INDEX.md 는 생성하지 않습니다
(목록은 각 디렉토리 frontmatter에서 직접 읽음). 단 qa/README.md 는 QA 운영 기준 문서이므로 작성합니다.

[AGENTS.md 팀 규약 — 반드시 포함]
- 런타임 없음: markdown + git만 사용.
- 역할: maintainer(전역 계약·INTEGRATE·중재) / contributor(workitem claim·작업). 세션 시작 시 신원 확인.
- 식별: git identity 정박 — git config user.email 을 team/<handle>.md 의 emails 와 매칭. commit에 Session-Id / Co-Authored-By 트레일러.
- 진행 상태: PROGRESS.md가 아니라 workitems/WI-*.md frontmatter(고정 INDEX 없음). 세션 커서는 sessions/<handle>--<WI-id>.md.
- 공유 브랜치: <초기화에서 결정한 이름 — 기본 브랜치 또는 coordination>. 조율 파일(workitems/conflicts/team/personas)은 여기에 직접 커밋·push, 코드는 PR로만. WI 파일은 공유 브랜치에서만 편집.
- 충돌: claim 직후·integrate 직전, 먼저 git fetch 후 최신 공유 브랜치의 workitems/*.md(claimed/in_progress)를 읽어 touches 교차. contracts 겹침=STOP, modules 겹침=conflicts/CF 등재.
- 전역 계약(ARCHITECTURE/PLAN): maintainer single-writer. 변경은 ADR + 검출 통지 + merge 우선(직렬화).
- 원자 커밋: 코드 + 그 workitem 작업층 파일만. ARCHITECTURE/PLAN/history는 제외.
- 새 사건은 새 파일: history/assumptions/conflicts 에 append 금지, 파일 생성.
- 통합은 maintainer가 INTEGRATE.md로. 기여자는 PR까지. main/master 직접 push 금지.

초기화가 끝나면 아래 형식으로 보고하세요.
# 팀 프로젝트 초기화 결과
## 등록한 team 멤버 / 역할
## 생성한 구조 / 횡단 계약(ARCHITECTURE) 요약
## 기능명세 목록 / 초기 workitem 목록(touches 포함)
## ADR / QA / docs 목록
## AI 위임으로 결정한 항목 (검토 권장)
## 다음 단계 (첫 claim 후보 / DEVELOP.md 안내)
```

> 초기화는 단계가 길어 중간에 끊길 수 있습니다. 각 단계 후 진행 상태가 항목 파일에 남으므로, 끊기면 같은 프롬프트로 이어서 진행하면 됩니다.

### B. 채택 프롬프트 — 이미 개발 중인 프로젝트 (ADOPT · maintainer)

신규가 아니라 **이미 코드가 있는 프로젝트**라면 `KICKOFF.md` 대신 `ADOPT.md`를 씁니다. 요구사항이 아니라 **기존 코드를 분석해 현재 상태를 역문서화**하고 팀 동시 개발 구조를 세웁니다. 산출물 구조는 KICKOFF와 동일하므로, 채택이 끝나면 그대로 DEVELOP으로 잇습니다.

```text
THROUGHLINE/ADOPT.md 를 읽고, 그 지시에 따라 이미 개발 중인 이 프로젝트에 THROUGHLINE Team을 채택(적용)하세요.
규약은 THROUGHLINE/CONVENTIONS.md, 스키마는 THROUGHLINE/SCHEMAS.md 가 우선합니다.

산출물은 루트 3파일(프로젝트 README.md · AGENTS.md · CLAUDE.md)을 제외하고 모두 THROUGHLINE/ 아래에 생성하세요.
기존 프로젝트의 docs/ 등 동명 폴더는 건드리지 마세요. 이 프롬프트는 maintainer가 실행합니다.

반드시 다음을 지키세요.

1. 이 단계에서는 코드를 수정하지 않습니다. 현재 상태를 문서화하고 팀 개발 구조를 세우는 단계입니다.
2. 선행 확인: THROUGHLINE/ 에 기존 산출물이 있으면 이미 채택됨 → 재채택하지 말고 보고만 하세요.
   루트 README/AGENTS/CLAUDE/.gitignore 를 인벤토리하고, 이미 있는 파일은 덮어쓰지 말고 병합하거나 확인을 받으세요.
   실행자를 team/<handle>.md (role: maintainer)로 등록하고 git config user.email 매칭을 확인하세요.
3. 코드 스캔: 스택·빌드/실행/테스트 명령·구조·진입점·의존성·환경변수 '이름'을 파악하세요(값/Secret 수집 금지).
4. 실제 동작 추적: 진입점부터 핵심 경로를 직접 읽으세요. 파일명·구조만으로 추측하지 마세요.
   읽은 범위/안 읽은 범위를 명시하고, 안 읽은 영역은 workitems/WI-*.md(status: proposed, title: "미독파 영역 ...")로 남기세요.
5. 횡단 계약 역추출 → ARCHITECTURE.md (maintainer single-writer). 코드에서 못 정하는 항목은 지어내지 말고
   assumptions/ASM-*.md(active, 검증 필요)에 남기세요.
6. as-built 명세 → features/*.md. 각 동작 주장은 근거 코드 위치(파일/함수)를 대세요.
   직접 안 읽은 동작은 "추정(검증 필요)"으로 표시하고, 코드↔의도 괴리 지점을 별도 표시하세요.
7. 기존 테스트를 실제 실행해 baseline(pass/fail/absent)을 history/YYYY/MM/HIST-*.md 에 기록하세요.
8. 남은/미구현 작업을 workitems/WI-*.md(proposed)로 분해하고 touches(contracts/modules)를 채우세요.
9. SOURCES/REQUIREMENTS.md 가 있으면 미래 목표·미구현 요구로 사용하고, as-built와 충돌하면 질문하세요.
   채택 완료 시 SOURCES/REQUIREMENTS.meta.md(id: REQUIREMENTS)에 등록하고 applied 로 동결하세요.
10. PLAN.md 에 현재 상태를 done/in-progress/remaining 으로 반영하고, PROGRESS.md 호환 스텁을 작성하세요.
11. AGENTS.md(팀 규약 — KICKOFF 4절 항목)·CLAUDE.md 를 작성/병합하세요. (고정 INDEX 파일·추가 런타임 없음.)
12. 채택 산출물을 commit하세요(문서 전용 — 코드 변경 없음). maintainer가 공유 브랜치에 push할 수 있으면 공유 브랜치에서 직접 수행하고,
    아니면 docs/throughline-adopt 브랜치에서 수행한 뒤 기여자가 claim을 시작하기 전에 PR로 merge하세요.
    빈 디렉토리에는 .gitkeep 을 넣으세요.
13. 채택이 끝나면 아래 형식으로 보고하세요.
# 팀 채택 결과
## 등록한 maintainer
## 읽은 범위 / 안 읽은 범위(→ workitem)
## 역추출한 ARCHITECTURE 요약
## as-built feature 목록 (코드 근거)
## 코드↔의도 괴리 목록
## 테스트 baseline (실행 명령 / 결과)
## 생성한 초기 workitem(touches) / PLAN 반영
## 다음 단계 (DEVELOP.md 안내)
```

> 채택도 다단계라 중단될 수 있습니다. 중단 시 workitems/·history/ 항목 파일 frontmatter를 읽어 이어받습니다.

### C. 기여자 개발 프롬프트 — claim → 검출 → 구현 → PR (DEVELOP · contributor)

초기화(또는 채택)가 공유 브랜치에 커밋된 뒤, 각 기여자가 **하나의 workitem을 수행**할 때 씁니다. 실행 전 자기 `team/<handle>.md`가 등록돼 있어야 합니다(없으면 프롬프트가 먼저 등록).

```text
AGENTS.md 와 THROUGHLINE/DEVELOP.md 를 읽고, DEVELOP.md 절차에 따라 workitem 하나를 claim해서 개발하세요.
규약은 THROUGHLINE/CONVENTIONS.md 가 우선합니다. 이 킷은 markdown + git만 씁니다.

반드시 다음 순서로 진행하세요.

0. 신원 확인: git config user.email 을 team/*.md 의 emails 와 매칭해 내 handle·role 을 확인하세요.
   미등록이면 team/<handle>.md 를 먼저 등록(templates/team-TEMPLATE.md)한 뒤 진행하세요.
   그다음 git fetch 하고, 최신 공유 브랜치의 workitems/*.md frontmatter를 읽어 in-flight(claimed/in_progress) 작업과 그 touches를 파악하세요.
1. 항상 로드: AGENTS.md(루트), THROUGHLINE/ARCHITECTURE.md(횡단 계약), THROUGHLINE/PLAN.md, in-flight workitems frontmatter.
   내 작업에 필요한 features/*.md·ADR·qa·notes 는 선택적으로 읽으세요. 공통 규칙은 항상 ARCHITECTURE.md 를 기준으로 따르세요.
2. workitem claim:
   - 기존 항목: status: proposed|ready 인 WI를 골라 owner를 내 handle로, status를 claimed로, branch를 feat/<WI-id>로 바꾸고
     공유 브랜치에 이 변경만 커밋·push하세요(코드 작업 전 — 발행).
   - 새 항목: templates/WI-TEMPLATE.md 를 복사해 workitems/WI-<YYYYMMDD>-<slug>.md 를 만들고 touches(contracts/modules)를 반드시 채운 뒤
     공유 브랜치에 커밋·push하세요.
3. 충돌 검출(claim 직후 필수): git fetch 후 최신 공유 브랜치의 workitems/*.md 중 status ∈ {claimed, in_progress} 를 읽어 내 touches와 교차하세요.
   - contracts 겹침 = STOP: 진행하지 말고 maintainer에게 직렬화를 요청하세요(아래 7). 계약 변경이면 ADR 경유.
   - modules 겹침 = WARN: conflicts/CF-*.md 에 등재(templates/CF-TEMPLATE.md)하고 상대 owner와 순서를 합의하세요.
   - 독립 = OK: 진행.
4. 개발(feature 브랜치): git checkout -b feat/<WI-id>. sessions/<handle>--<WI-id>.md 를 만들고 "다음 첫 명령"을 갱신하세요.
   - WI status를 in_progress로 바꿔 공유 브랜치에 커밋·push하세요(WI 파일은 공유 브랜치에서만 편집).
   - features/*.md 명세와 ARCHITECTURE.md 계약을 확인하고(없으면 명세부터, 비자명 기능은 personas/+discussion/ 리뷰) 구현하세요.
   - 자동 테스트를 작성하고 실제 실행하세요(명령·결과 캡처). 실행 없이 통과를 주장하지 마세요.
   - 코드↔명세 불일치는 권위 진단 후 처리하세요(어느 쪽이 권위인지 먼저 판단, 임의로 명세를 고쳐 불일치를 지우지 않음).
   - 자율 판단은 assumptions/ASM-*.md 새 파일로, 학습한 사실은 notes/<topic>.md 에 기록하세요(추측은 assumptions로).
   - 전역 계약(ARCHITECTURE.md)을 바꿔야 하면 직접 고치지 말고 STOP 사유로 7번을 따르세요.
5. 원자 커밋: 코드 + 그 workitem의 작업층 파일(features/qa/assumptions/notes/sessions)만 하나의 커밋으로 묶으세요.
   ARCHITECTURE/PLAN(maintainer)·history(INTEGRATE)·workitems/WI-*(조율층)는 제외합니다.
   커밋 메시지에 Session-Id: <YYYY-MM-DDThhmm>-<handle>-<WI-id> 와 Co-Authored-By: <에이전트 런타임> 트레일러를 넣으세요.
   코드는 main/master·공유 브랜치에 직접 push하지 마세요(PR로만). 단 조율층 파일은 공유 브랜치에 직접 push합니다. .env·Secret 커밋 금지.
6. review 제출: WI status를 review로 바꿔 공유 브랜치에 커밋·push하고, feat/<WI-id> 를 push한 뒤 PR을 생성하세요.
   PR 본문에 WI-id, 변경 요약, 테스트 결과, touches, 미해소 conflicts/ 를 명시하세요. merge는 maintainer가 INTEGRATE에서 합니다.
7. STOP/직렬화가 필요하면: 계약 변경 의도를 touches.contracts 로 선언한 전용 workitem + adr/ADR-*.md(Proposed)를 작성하고
   maintainer에게 직렬화를 요청하세요. maintainer가 계약을 먼저 merge하고 ARCHITECTURE를 갱신한 뒤, 내 workitem을 새 계약으로 rebase합니다.

완료 후 아래 형식으로 보고하세요.
# 개발 결과 (WI-<id>)
## 수행한 작업 / 변경 파일
## 테스트 결과 (실행 명령 / 통과·실패)
## touches (contracts / modules) 와 검출 결과
## 등재한 conflicts / assumptions / notes
## Git (브랜치 / commit / PR)
## 다음 첫 명령 (= sessions/<handle>--<WI-id>.md 갱신 내용)
```

### D. 이어서 개발하는 프롬프트 — 세션 재개 (DEVELOP · contributor)

같은 workitem을 다음 세션에 이어서 할 때 씁니다. 세션 커서(`sessions/<handle>--<WI-id>.md`)의 "다음 첫 명령"이 기준입니다.

```text
AGENTS.md 와 THROUGHLINE/DEVELOP.md 를 읽고, 진행 중이던 내 workitem을 이어서 개발하세요.

1. git config user.email 로 신원을 확인하고, git fetch 하세요.
2. sessions/<handle>--<WI-id>.md 의 "다음 첫 명령"을 읽어 끊긴 지점을 확인하세요.
3. 최신 공유 브랜치의 workitems/*.md(claimed/in_progress) touches를 다시 읽어, 내가 자리를 비운 사이 생긴 충돌을 재검출하세요
   (contracts 겹침=STOP, modules 겹침=conflicts/CF 확인·등재).
4. ARCHITECTURE.md / PLAN.md 로 횡단 계약을 다시 맞추고, 이미 끝난 작업은 반복하지 마세요.
5. feat/<WI-id> 브랜치에서 DEVELOP.md 4절부터 이어서 구현하세요(테스트 실제 실행, 원자 커밋, 세션 커서 갱신).
6. 작업이 일단락되면 DEVELOP.md 8절 형식으로 보고하고 sessions/<handle>--<WI-id>.md 를 갱신하세요.
```

### E. 통합 프롬프트 — review 완료분 합류 (INTEGRATE · maintainer)

기여자들이 PR을 올린 뒤, maintainer가 feature 브랜치들을 공유 브랜치로 합류시킬 때 씁니다. `role: maintainer`만 실행합니다.

```text
AGENTS.md 와 THROUGHLINE/INTEGRATE.md 를 읽고, INTEGRATE.md 절차에 따라 review 완료 workitem들을 통합하세요.
규약은 THROUGHLINE/CONVENTIONS.md 가 우선합니다. 이 프롬프트는 role: maintainer 만 실행합니다.

반드시 다음 순서로 진행하세요.

0. 신원 확인: git config user.email 을 team/*.md 와 매칭. role이 maintainer가 아니면 중단하고 maintainer에게 위임하세요.
   git fetch 후 최신 공유 브랜치의 workitems/*.md 중 status: review 인 항목과 그 PR/브랜치를 모으세요.
1. 통합 대상 수집: 각 workitem의 touches(contracts/modules)와 depends_on 을 확인하세요.
2. 충돌 재검출(merge 전 필수): 통합 후보 + 다른 in-flight(claimed/in_progress) workitem 전체의 touches를 전수 교차하세요.
   - contracts 겹침 = STOP: 동시에 merge하지 말고 3번 직렬화로 처리.
   - modules 겹침 = WARN: conflicts/CF-*.md 에 해소 결정이 있는지 확인, 없으면 등재하고 owner들과 순서 합의.
   - 식별 검증: 각 후보 feature 브랜치의 commit author email이 WI.owner의 등록 email과 일치하는지 확인(불일치 = claim한 사람 ≠ 작업한 사람 → 보고).
3. 전역 계약 직렬화: touches.contracts 가 있는 workitem을 먼저 처리하세요.
   해당 ADR이 Accepted인지 확인 → 계약 변경 workitem을 먼저 merge → maintainer가 ARCHITECTURE.md(필요 시 PLAN.md)를 갱신
   → 같은 contract를 건드리던 나머지 workitem은 새 계약으로 rebase하도록 owner에게 통지(rebase 전 merge 금지).
4. Merge: 직렬화 순서(계약 변경 → 의존 → 독립)대로 PR을 merge하세요. git 충돌은 일반 절차로 해소.
   merge 후 각 WI status를 done으로 바꾸고 같은 커밋에서 파일을 workitems/archive/로 이동해 공유 브랜치에 커밋하세요(WI single-writer의 공인된 예외 — CONVENTIONS §9).
5. 이력 기록: merge된 workitem마다 history/YYYY/MM/HIST-<YYYYMMDD-hhmm>-<slug>.md 를 새 파일로 생성하세요
   (완료 workitem, commit, 테스트 결과, source, QA, 영향 범위, follow-up). history는 INTEGRATE만 기록합니다.
6. SOURCES 상태 갱신: merge로 반영 완료된 source는 SRC-*.meta.md status를 applied로 바꾸고 반영 산출물을 링크하세요
   (모든 항목 반영 시에만 applied, 부분 반영은 under_review 유지).
7. 전체 회귀 & PROGRESS: 전체 회귀 테스트를 실제 실행하고 결과를 history에 기록하세요.
   ARCHITECTURE 계약이 최근 코드에서 지켜지는지 표본 점검(어긋나면 conflicts/ 또는 후속 workitem).
   PROGRESS.md 스텁이 항목 파일을 가리키도록 유지하세요(진행 상태의 진실은 workitems frontmatter).

완료 후 아래 형식으로 보고하세요.
# 통합 결과 (INTEGRATE)
## merge한 workitem (순서와 사유)
## 전역 계약 변경 (ARCHITECTURE/ADR)
## 재검출 결과 (STOP/WARN 및 해소)
## 식별 검증 (owner ↔ commit author 불일치 여부)
## 기록한 history 이벤트
## SOURCES 상태 변화 (applied 처리)
## 전체 회귀 결과 (실행 명령 / 통과·실패)
## 남은 review/blocked workitem
```

### F. 문서 감사 프롬프트 — 표류 + 조율 무결성 (AUDIT · maintainer)

Phase 완료 직후 / 릴리즈 전 / 오랜만의 재개 / 마지막 감사 후 ~10세션 누적 / 여러 기여자가 동시에 활동 중일 때 정기적으로 실행합니다.

```text
THROUGHLINE/AUDIT.md 를 읽고, 그 지시에 따라 팀 문서·코드의 표류와 조율 구조의 무결성을 감사하세요.
규약은 THROUGHLINE/CONVENTIONS.md 가 우선합니다. INTEGRATE는 합류 정합, AUDIT는 점진 표류 회수를 담당합니다.

반드시 다음을 지키세요.

1. 기능 코드를 수정하지 않습니다. 점검·기록 단계입니다.
2. 기계적 불일치(끊어진 링크, 명백한 상태 오기)는 즉시 수정하고 감사 commit에 포함하세요. 고정 INDEX가 없으므로 인덱스 재생성 단계는 없습니다.
3. 의미적 표류는 수정하지 말고 기록만 하세요(코드↔명세는 DEVELOP 권위 진단, touches 겹침은 conflicts/로).
4. 고정 INDEX 부재 확인: 누군가 INDEX.md 같은 고정 인덱스 파일을 만들어 커밋했으면 삭제 후보로 보고하세요.
5. workitem 위생: claimed/in_progress 로 장기 방치(예: 14일+)된 항목, owner가 team/에 등록된 active handle인지,
   done인데 history/ 이벤트가 없는 항목(archive/ 포함), done인데 workitems/archive/로 옮겨지지 않은 항목,
   feature/source_refs 링크가 끊어진 항목, 고아 workitem을 점검하세요.
6. 미검출 touches 겹침(핵심): git fetch 후 최신 공유 브랜치에서 in-flight(claimed/in_progress) workitem 전체의 touches를 쌍별 교차하세요.
   - contracts 겹침인데 conflicts/CF도 없고 직렬화도 안 된 쌍 → 즉시 보고(maintainer 직렬화 필요).
   - modules 겹침인데 conflicts/CF 미등재 → CF 등재를 후속 작업으로.
7. 식별/권한 무결성: 최근 commit author email이 모두 team/에 등록돼 있는가, WI.owner와 feature 브랜치 commit author가 일치하는가,
   contributor가 ARCHITECTURE.md/PLAN.md 를 직접 수정했는가(single-writer 위반, git 이력), 전역 계약 변경에 ADR이 있는가.
8. conflicts/sessions/SOURCES: open으로 장기 방치된 CF, done인데 active로 남은 세션(→ archive/ 후보),
   not_applied/under_review 로 방치된 SRC-*.meta(사용자 의도 미반영), applied 이후 수정된 원본(불변 위반)을 점검하세요.
9. 후속 작업은 workitems/(proposed) 또는 PLAN에 등재하고, 감사 전체를 history/YYYY/MM/HIST-*.md 에 audit 이벤트로 기록하세요.

완료 후 아래 형식으로 보고하세요.
# 팀 문서 감사 결과
## 감사 범위 / 샘플링 기준
## 즉시 수정(기계적)
## 미검출 touches 겹침 (contracts STOP / modules WARN)
## workitem 위생 (방치 / 미등록 owner / 고아 / 끊어진 링크)
## 식별·권한 무결성 (미등록 author / owner≠author / single-writer 위반)
## conflicts·sessions·SOURCES 상태
## 일반 표류 (계획↔실제 / 가정 수명 / 명세↔코드 표본)
## 사용자 확인 필요 사항
## 후속 작업 (workitems/PLAN 반영)
```

### G. 킷 업그레이드 프롬프트 — 새 버전 반영 (maintainer)

템플릿 저장소의 THROUGHLINE Team 킷이 업데이트되어, 이미 KICKOFF/ADOPT를 마친 프로젝트에 새 버전을 반영할 때 씁니다. **KICKOFF나 ADOPT를 다시 실행하지 마세요** — 재초기화/재채택 가드가 막을 뿐 아니라, 우회하면 조율층 내용을 덮어씁니다. `role: maintainer`만 실행합니다(킷 소유 파일과 루트 규칙 파일 모두 maintainer 전용 영역이기 때문입니다).

처리 원칙:

| 구분 | 대상 | 처리 |
|---|---|---|
| 킷 소유(프로젝트 콘텐츠 없음) | `KICKOFF.md`·`ADOPT.md`·`DEVELOP.md`·`INTEGRATE.md`·`AUDIT.md`·`CONVENTIONS.md`·`SCHEMAS.md`·`README.md`·`templates/`·`reference/` | 원래 사용한 언어 폴더의 **동일 버전으로 덮어쓰기 복사** |
| 조율/작업 산출물(프로젝트 콘텐츠 있음) | `ARCHITECTURE.md`, `PLAN.md`, `workitems/`, `conflicts/`, `team/`, `sessions/`, `history/`, `assumptions/`, `notes/`, `SOURCES/` 원본, `features/`, `personas/`, `discussion/`, `adr/`, `docs/`, `qa/` | **내용 보존** — 건드리지 않음 |
| 루트 규칙 파일 | `AGENTS.md` | **병합 갱신** — 누락된 팀 규약 블록만 추가 |
| | `CLAUDE.md` | 새 KICKOFF.md 템플릿(오작동 방지 전용)으로 **교체** — 무손실 게이트 |
| 신규 구조(구버전에 없던 것) | 예: `workitems/archive/` | **새로 생성**(빈 폴더면 `.gitkeep`) + **기존 데이터 중 해당하는 것을 이관** |

**1단계(사람, maintainer):** 템플릿 저장소를 pull하고, 위 킷 소유 파일들을 **원래 사용한 언어 폴더**(`en/THROUGHLINE-TEAM/` 또는 `ko/THROUGHLINE-TEAM/`)에서 동일 버전으로 프로젝트의 `THROUGHLINE/`에 덮어쓰기 복사합니다. 조율층 파일이므로 공유 브랜치에서 직접 수행하세요(공유 브랜치가 push 보호 중이면 작업 브랜치+PR로 먼저 처리한 뒤, 기여자가 claim을 재개하기 전에 merge).

**2단계(Agent):**

```text
THROUGHLINE Team 킷이 업데이트되어 킷 소유 파일들이 새 버전으로 교체되었습니다.
이 프로젝트의 산출물 구조를 새 버전 표준으로 업그레이드하세요.
KICKOFF나 ADOPT를 다시 실행하지 마세요(재초기화/재채택 금지). 기존 조율/작업 산출물의 내용은 보존하세요.
이 프롬프트는 role: maintainer만 실행합니다.

0. 신원 확인: git config user.email 을 team/*.md 와 매칭. role이 maintainer가 아니면 중단하고 maintainer에게 위임하세요.
   구조 비교 전에 git fetch로 최신 공유 브랜치를 읽으세요.
1. 새 KICKOFF.md 1절의 구조와 현재 THROUGHLINE/ 를 비교해 누락된 파일/폴더를 확인하세요.
2. 누락된 빈 구조를 생성하세요(KICKOFF 1절 기준 .gitkeep) — 예: 이 프로젝트가 workitems/archive/ 도입 이전 버전이면 새로 만드세요.
3. 1회성 아카이브 스윕(workitems/archive/ 가 새로 생긴 경우에만 의미 있음): 루트의 workitems/WI-*.md 중 status: done 인 항목마다
   대응하는 history/ 이벤트가 있는지 확인한 뒤, 같은 커밋에서 workitems/archive/ 로 이동하세요(CONVENTIONS §9).
   대응 history/ 이벤트가 없는 done 항목은 이동하지 말고 목록화해 AUDIT로 넘기세요(임의로 아카이브하지 않음).
4. 루트 AGENTS.md를 새 KICKOFF.md §4(팀 규약) 기준으로 병합 갱신하세요 — 기존 프로젝트 고유 내용은 보존하고
   누락된 원칙 블록(식별/공유 브랜치/충돌 검출/원자 커밋 등)만 추가하세요. 기존 내용이 다른 언어면 언어를 섞지 말고 번역 병합하세요.
5. 루트 CLAUDE.md를 새 KICKOFF.md 템플릿(오작동 방지 전용)으로 교체하세요.
   무손실 게이트: 규칙을 제거하기 전에 AGENTS.md에 그 규칙이 있는지 먼저 확인하고(없으면 먼저 추가), 프로젝트 고유 커스텀 규칙은
   지정 언어로 번역해 보존하세요.
6. 기존 산출물(ARCHITECTURE/PLAN/workitems/features 등)의 내용은 수정하지 마세요. 스키마가 바뀐 경우에만 형식을 맞추되
   내용은 보존하세요(예: SCHEMAS.md에 추가된 선택 필드를 기존 파일에 강제로 채워 넣지 않음).
7. history/YYYY/MM/HIST-<YYYYMMDD-hhmm>-kit-upgrade.md 를 chore | Framework upgrade 이벤트로 새 파일 생성하세요 —
   갱신/생성한 파일 목록과 스윕으로 아카이브한 workitem 목록을 남기세요.
8. 전체 변경을 조율층 파일로서 공유 브랜치(또는 1단계에서 쓴 작업 브랜치)에서 하나의 커밋으로 묶으세요.
   이 커밋에 코드 변경을 함께 넣지 마세요.
9. 갱신/생성/이관한 파일 목록, 스윕으로 아카이브한 workitem, 수동 확인이 필요한 충돌을 보고하세요.

완료 후 아래 형식으로 보고하세요.
# 킷 업그레이드 결과
## 갱신/생성한 파일
## workitems 아카이브 스윕 결과 (이동 개수 / 미이동 예외)
## AGENTS.md 병합 내용 / CLAUDE.md 교체 여부
## 새로 생성된 구조
## 기록한 history 이벤트
## 수동 확인이 필요한 충돌
```

**3단계(검증):** 업그레이드 직후 F. 문서 감사 프롬프트(AUDIT)를 실행하면, 새 표준 대비 마이그레이션 누락(미아카이브 done 항목, 고정 INDEX 파일, 끊어진 링크 등)을 잡아낼 수 있습니다.

### 프롬프트 선택 기준

| 상황 | 사용할 프롬프트 | 실행 주체 |
|---|---|---|
| 신규 팀 프로젝트를 처음 시작할 때 | A. 초기화 (KICKOFF) | maintainer |
| 이미 개발 중인 프로젝트에 적용할 때 | B. 채택 (ADOPT) | maintainer |
| workitem을 claim해 개발을 시작할 때 | C. 기여자 개발 (DEVELOP) | contributor |
| 진행 중이던 workitem을 이어서 할 때 | D. 이어서 개발 | contributor |
| review 완료 workitem을 합류시킬 때 | E. 통합 (INTEGRATE) | maintainer |
| Phase 완료 / 릴리즈 전 / 표류가 의심될 때 | F. 문서 감사 (AUDIT) | maintainer |
| 킷을 새 버전으로 업그레이드할 때(이미 초기화된 프로젝트) | G. 킷 업그레이드 | maintainer |

> 규칙 세부(파일 등급·식별·충돌·공유 브랜치·커밋)는 [CONVENTIONS.md](ko/THROUGHLINE-TEAM/CONVENTIONS.md), frontmatter 형식은 [SCHEMAS.md](ko/THROUGHLINE-TEAM/SCHEMAS.md)가 정본입니다.

---

## 프롬프트 없이 쓰기

명세 주도 개발을 하려고 프롬프트를 붙여넣어야 하는 것은 아닙니다. 초기화가 프로젝트 루트의 `AGENTS.md`에 상시 규약을 — 팀 규약(식별·공유 브랜치·충돌 검출·원자 커밋)까지 포함해 — 써두고, 에이전트가 **매 실행마다** 그것을 로드합니다. 그래서 Claude Code · Codex · Cursor와 평범하게 대화만 해도 `ARCHITECTURE.md`의 횡단 계약을 읽고, `git config user.email`로 내 handle을 확인하고, 바뀐 것을 기록합니다.

다만 팀 모드에서는 걸린 것이 하나 더 큽니다. **충돌 검출은 claim 시점에 `touches`가 공유 브랜치에 게시되어야만 작동합니다** — 곧바로 코드로 들어가는 대화는 아무것도 claim하지 않으므로 게시되는 것도 없고, 다른 기여자들은 계속 보지 못합니다. 재개도 마찬가지입니다: [D](#d-이어서-개발하는-프롬프트--세션-재개-develop--contributor)가 존재하는 이유가 자리를 비운 사이 생긴 충돌을 재검출하기 위해서입니다.

기준선: **claim한 workitem 안에서는 자유롭게 대화하고, 경계에서 프롬프트를 쓰세요.** 셋업은 [A](#a-초기화-프롬프트--신규-팀-프로젝트-kickoff--maintainer)/[B](#b-채택-프롬프트--이미-개발-중인-프로젝트-adopt--maintainer), claim은 [C](#c-기여자-개발-프롬프트--claim--검출--구현--pr-develop--contributor), 재개는 [D](#d-이어서-개발하는-프롬프트--세션-재개-develop--contributor), 합류는 [E](#e-통합-프롬프트--review-완료분-합류-integrate--maintainer), 주기적 그물은 [F](#f-문서-감사-프롬프트--표류--조율-무결성-audit--maintainer).

---

## 프롬프트·참조 ([`ko/THROUGHLINE-TEAM/`](ko/THROUGHLINE-TEAM/) 안)

| 파일 | 역할 |
|---|---|
| [README.md](ko/THROUGHLINE-TEAM/README.md) | 프레임워크 전체 개요·명세 |
| [KICKOFF.md](ko/THROUGHLINE-TEAM/KICKOFF.md) · [ADOPT.md](ko/THROUGHLINE-TEAM/ADOPT.md) | 신규 / 기존 팀 프로젝트 초기화 |
| [DEVELOP.md](ko/THROUGHLINE-TEAM/DEVELOP.md) · [INTEGRATE.md](ko/THROUGHLINE-TEAM/INTEGRATE.md) | 기여자 / 메인테이너 프롬프트 |
| [AUDIT.md](ko/THROUGHLINE-TEAM/AUDIT.md) | 팀 문서 감사 (드리프트 + 조정 정합성) |
| [CONVENTIONS.md](ko/THROUGHLINE-TEAM/CONVENTIONS.md) · [SCHEMAS.md](ko/THROUGHLINE-TEAM/SCHEMAS.md) | 구조 규약 & frontmatter 스키마 |
| [reference/](ko/THROUGHLINE-TEAM/reference/README.md) | 팀 프롬프트가 인용하는 솔로 킷 참조 사본(동봉) |

> THROUGHLINE Team은 Solo의 철학을 그대로 유지합니다 — markdown + git, 도구 독립성(Claude Code · Codex · Cursor), 세션 간 기억, 추적성, 멀티 페르소나 리뷰 하네스. 충돌 탐지 모델·개발 흐름·정직한 한계(탐지 ≠ 강제, 거버넌스 ≠ 도구)는 **[전체 가이드](ko/THROUGHLINE-TEAM/README.md)**를 참고하세요.
