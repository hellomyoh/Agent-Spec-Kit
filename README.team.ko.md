<div align="center">

# ASK-Team — 팀 개발용 Agent-Spec-Kit

🌐 [English](README.team.md) · **한국어**

**[Agent-Spec-Kit](README.ko.md)의 Team 버전.** 여러 개발자와 AI 에이전트가 *같은* 코드베이스를 **동시에** 개발할 때, ASK-Team은 **markdown + git만으로** 단일 `PROGRESS.md` / `HISTORY.md`가 가려버리는 Git 충돌·의미(semantic) 충돌·의도(intent) 충돌을 드러냅니다.

Solo 가이드: [README.ko.md](README.ko.md) · 팀 전체 가이드·프롬프트: [ko/ASK-TEAM/](ko/ASK-TEAM/) · [English kit](en/ASK-TEAM/)

</div>

---

## Solo와 Team 중 무엇을?

| | **Solo (ASK)** — [README.ko.md](README.ko.md) | **Team (ASK-Team)** — 이 문서 |
|---|---|---|
| 대상 | 1인 / 순차·자율 개발 | 다수 개발자·AI 에이전트 **동시** 개발 |
| 진행 상태 | 단일 `PROGRESS.md` 커서 | `workitems/` + `sessions/<handle>--<WI>` |
| 이력 / 가정 / 노트 | 단일 파일 | `history/` · `assumptions/` · `notes/` 디렉토리 |
| 인덱스 | 손으로 갱신 | 없음 — frontmatter 직접 읽기 |
| 충돌 | 해당 없음 | `touches` + `conflicts/` (에이전트가 교차 점검) |
| 식별 | 불필요 | `team/` + git identity (`git config user.email`) |
| 런타임 | 없음 | 없음 (markdown + git만) |
| 키트 폴더 | `ko/AGENTSPECKIT/` · `en/AGENTSPECKIT/` | `ko/ASK-TEAM/` · `en/ASK-TEAM/` |

1인 개발이면 Solo가 더 가볍습니다 — 실제로 N명이 동시에 개발할 때만 Team을 쓰세요.

## 핵심 아이디어

- **git 브랜치 격리가 근본 사실.** 기여자는 서로의 *커밋되지 않은* 파일을 볼 수 없으므로, 워크아이템의 조정 메타데이터(`touches`)를 **claim 시점에 공유 브랜치로 게시**합니다 → 충돌이 머지 때가 아니라 조기에 드러납니다.
- **산출물 2계층.** *Coordination*(workitems·conflicts·`ARCHITECTURE.md`/`PLAN.md`)은 공유 브랜치에, *Work*(코드·기능명세·qa·노트·가정)는 격리된 피처 브랜치에 둡니다.
- **역할.** **Maintainer**가 전역 계약을 소유하고 `INTEGRATE`를 수행하며 의도 충돌을 ADR로 중재합니다. **Contributor**는 워크아이템을 claim하고 자기 범위 파일만 씁니다.
- **고정 INDEX 파일 없음.** 각 항목 파일의 frontmatter가 진실의 출처이고 에이전트가 디렉토리를 직접 읽으므로, 인덱스 동시 편집 충돌이 아예 없습니다.
- **식별 = git identity.** `git config user.email`을 `team/<handle>.md` 레지스트리로 검증 — 추가 런타임 없음.

## 빠른 시작

1. 이 저장소를 클론하고 [`ko/ASK-TEAM/`](ko/ASK-TEAM/)(또는 [`en/ASK-TEAM/`](en/ASK-TEAM/))의 내용을 프로젝트 루트의 `AGENTSPECKIT/`로 복사합니다.
2. **maintainer**가 `role: maintainer`로 자기 `team/<handle>.md`를 먼저 등록하고(`templates/team-TEMPLATE.md` 복사), 각 **contributor**도 자기 것을 등록합니다.
3. Contributor는 [`DEVELOP.md`](ko/ASK-TEAM/DEVELOP.md) 프롬프트로, maintainer는 [`INTEGRATE.md`](ko/ASK-TEAM/INTEGRATE.md)로 작업합니다. 초기화는 [`KICKOFF.md`](ko/ASK-TEAM/KICKOFF.md)(신규) / [`ADOPT.md`](ko/ASK-TEAM/ADOPT.md)(기존 코드), 주기 점검은 [`AUDIT.md`](ko/ASK-TEAM/AUDIT.md)를 사용합니다.

## 프롬프트·참조 ([`ko/ASK-TEAM/`](ko/ASK-TEAM/) 안)

| 파일 | 역할 |
|---|---|
| [README.md](ko/ASK-TEAM/README.md) | 프레임워크 전체 개요·명세 |
| [KICKOFF.md](ko/ASK-TEAM/KICKOFF.md) · [ADOPT.md](ko/ASK-TEAM/ADOPT.md) | 신규 / 기존 팀 프로젝트 초기화 |
| [DEVELOP.md](ko/ASK-TEAM/DEVELOP.md) · [INTEGRATE.md](ko/ASK-TEAM/INTEGRATE.md) | 기여자 / 메인테이너 프롬프트 |
| [AUDIT.md](ko/ASK-TEAM/AUDIT.md) | 팀 문서 감사 (드리프트 + 조정 정합성) |
| [CONVENTIONS.md](ko/ASK-TEAM/CONVENTIONS.md) · [SCHEMAS.md](ko/ASK-TEAM/SCHEMAS.md) | 구조 규약 & frontmatter 스키마 |

> ASK-Team은 Solo의 철학을 그대로 유지합니다 — markdown + git, 도구 독립성(Claude Code · Codex · Cursor), 세션 간 기억, 추적성, 멀티 페르소나 리뷰 하네스. 충돌 탐지 모델·개발 흐름·정직한 한계(탐지 ≠ 강제, 거버넌스 ≠ 도구)는 **[전체 가이드](ko/ASK-TEAM/README.md)**를 참고하세요.
