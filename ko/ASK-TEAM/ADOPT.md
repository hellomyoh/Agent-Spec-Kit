# ADOPT.md — 기존 프로젝트 채택 (ASK-Team)

이미 코드가 있는 프로젝트에 ASK-Team을 적용합니다. 요구사항이 아니라 **기존 코드를 분석해 현재 상태를 역문서화**하고, 팀 동시 개발 구조를 세웁니다.
산출물 구조는 [KICKOFF.md](KICKOFF.md)와 동일하므로, 채택이 끝나면 곧바로 [DEVELOP.md](DEVELOP.md)로 개발을 잇습니다.

> 규약은 [CONVENTIONS.md](CONVENTIONS.md), 스키마는 [SCHEMAS.md](SCHEMAS.md)가 우선합니다.
> 코드 역문서화의 **세부 방식**(읽은 범위 명시·as-built 명세·추정 표기)은 solo 킷 [ADOPT.md](../AGENTSPECKIT/ADOPT.md)를 따릅니다 — 여기서는 **팀 구조 차이만** 규정합니다.
> **이 프롬프트는 maintainer가 실행**합니다. 이 단계에서 **코드를 수정하지 않습니다.**

---

# 1. 선행 확인

1. `AGENTSPECKIT/`에 기존 산출물이 있으면 **이미 채택됨** → 재채택하지 말고 보고만.
2. 루트 `README`/`AGENTS.md`/`CLAUDE.md`/`.gitignore` 존재 여부 인벤토리. 기존 파일은 덮어쓰지 말고 merge하거나 확인 후 진행.
3. **maintainer 등록** — 실행자를 `team/<handle>.md`(`role: maintainer`)로. `git config user.email`이 그 파일의 `emails`에 들어가는지 확인(신원 매칭).

---

# 2. 채택 작업 순서

1. **코드 스캔** — 스택·빌드/실행/테스트 명령·구조·진입점·의존성·환경변수 **이름**(값/Secret 수집 금지).
2. **실제 동작 추적** — 진입점부터 핵심 경로를 직접 읽습니다. 파일명·구조만으로 추측하지 않습니다. 읽은 범위/안 읽은 범위를 명시하고, 안 읽은 영역은 workitem(`status: proposed`, `title: "미독파 영역 ..."`)으로 남깁니다.
3. **횡단 계약 역추출 → `ARCHITECTURE.md`** (maintainer single-writer). 코드에서 못 정하는 항목은 `assumptions/ASM-*.md`(active, needs verification).
4. **as-built 명세 → `features/*.md`** — 각 동작 주장은 코드 위치(파일/함수) 근거. 직접 안 읽은 동작은 단정하지 말고 "추정(검증 필요)". 코드↔의도 괴리 지점을 별도 표시.
5. **기존 테스트 실제 실행 → `history/YYYY/MM/HIST-*.md`** 에 baseline(pass/fail/absent) 기록.
6. **남은/미구현 작업 → `workitems/WI-*.md`(proposed)** 로 분해, `touches` 채움. 이미 구현된 것은 feature as-built로, 앞으로 할 것은 workitem으로.
7. `SOURCES/REQUIREMENTS.md`가 있으면 미래 목표/미구현 요구로 사용. as-built와 충돌하면 질문. 채택 완료 시 `SRC-*.meta.md`에 등록하고 `applied`로 동결.
8. `PLAN.md`(안정 로드맵)에 현재 상태를 done/in-progress/remaining으로 반영. `PROGRESS.md` 호환 스텁 작성([KICKOFF.md](KICKOFF.md) 5절).
9. `AGENTS.md`(팀 규약 — KICKOFF 4절)·`CLAUDE.md` 작성/merge. (고정 INDEX 파일·추가 런타임 없음.)
10. 채택 완료 보고(아래).

---

# 3. 완료 조건 / 보고

* `team/`에 maintainer 등록, `git config user.email` 매칭 성공
* `ARCHITECTURE.md`(역추출)·as-built `features/*.md`(코드 근거)·테스트 baseline(`history/`) 생성
* 미구현/미독파 작업이 `workitems/`(proposed, `touches` 포함)에 등재
* 코드↔의도 괴리 목록 정리

보고 형식:

```md
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

> 채택도 다단계라 중단될 수 있습니다. 중단 시 `workitems/`·`history/`의 항목 파일 frontmatter를 읽어 이어받습니다(고정 INDEX 없음).
