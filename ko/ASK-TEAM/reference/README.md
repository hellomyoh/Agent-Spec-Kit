# reference/ — 동봉된 솔로 킷 참조 사본

이 폴더의 파일들은 **솔로 Agent-Spec-Kit 프롬프트의 원문 사본(이 킷과 동일 버전)**입니다. 팀 프롬프트가 인용하는 참조 — "솔로 §6.1", "솔로 DEVELOPINIT §3.4", "솔로 AUDIT 3.1~3.12" 등 — 가 킷을 프로젝트로 복사한 뒤(솔로 킷이 없는 환경)에도 열리도록 동봉한 것입니다.

| 사본 | 원본 (템플릿 저장소) | 인용하는 곳 |
|---|---|---|
| [SOLO-KICKOFF.md](SOLO-KICKOFF.md) | `ko/AGENTSPECKIT/KICKOFF.md` | KICKOFF §2·§6, CONVENTIONS §6·§8 |
| [SOLO-DEVELOPINIT.md](SOLO-DEVELOPINIT.md) | `ko/AGENTSPECKIT/DEVELOPINIT.md` | DEVELOP §4 |
| [SOLO-ADOPT.md](SOLO-ADOPT.md) | `ko/AGENTSPECKIT/ADOPT.md` | ADOPT 머리말 |
| [SOLO-AUDIT.md](SOLO-AUDIT.md) | `ko/AGENTSPECKIT/AUDIT.md` | AUDIT §3.1 |

## 가드 (중요)

* 이 파일들은 팀 프로젝트에서 **참조 문서이지 실행 프롬프트가 아닙니다.** 실행은 팀 프롬프트(`AGENTSPECKIT/`의 `KICKOFF.md` / `ADOPT.md` / `DEVELOP.md` / `INTEGRATE.md` / `AUDIT.md`)만 사용합니다.
* 솔로 규칙이 팀 킷과 충돌하면 **`CONVENTIONS.md`·팀 프롬프트가 우선**합니다. 대표적인 충돌:
  * 단일 `PROGRESS.md`/`HISTORY.md`/`ASSUMPTIONS.md`/`NOTES.md`/`TODO.md` 파일 → 팀은 `workitems/`·`sessions/`·`history/`·`assumptions/`·`notes/`(백로그는 `proposed` workitem)를 사용
  * 고정 INDEX 파일(`features/README.md`, `docs/README.md`, `adr/INDEX.md`, `personas/INDEX.md`)과 "같은 commit에서 인덱스 갱신" 규칙 → 팀은 **고정 INDEX를 두지 않음**(CONVENTIONS §3); 목록은 항목 파일 frontmatter에서 직접 읽음
  * 솔로 git/commit 규칙 → 팀은 CONVENTIONS §4.5(공유 브랜치 발행)·§7(workitem 범위 원자 commit)을 따름
* 사본 본문에 언급되는 파일명(`KICKOFF.md`, `DEVELOPINIT.md`, `ADOPT.md`, `AUDIT.md`)은 동명의 팀 프롬프트가 아니라 **이 폴더의 `SOLO-*.md` 사본**을 가리킵니다.
* **킷 업그레이드:** 킷을 업그레이드할 때 이 4개 파일을 **동일 버전** 솔로 킷(`ko/AGENTSPECKIT/`)에서 다시 복사하고, 각 파일 맨 위의 한 줄 배너를 다시 붙입니다.
