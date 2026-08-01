# INTEGRATE.md — Maintainer 통합 프롬프트

여러 기여자의 feature 브랜치를 공유 브랜치로 합류시키는 **maintainer 전용** 절차입니다.
의미 충돌 재검출, 전역 계약 직렬화, 이력 기록, 전체 회귀를 담당합니다.
규약은 [CONVENTIONS.md](CONVENTIONS.md)가 우선합니다.

> 이 킷은 markdown + git만 씁니다. "신원 확인"·"검출"은 에이전트가 `git`·파일 읽기로 직접 수행합니다.
> 이 프롬프트는 `role: maintainer`만 실행합니다.

---

## 0. 세션 시작 (필수)

1. **신원 확인** — `git config user.email`을 `team/*.md`와 매칭. `role`이 `maintainer`가 아니면 중단하고 maintainer에게 위임합니다.
2. **현황 파악** — 먼저 `git fetch`한 뒤, 최신 공유 브랜치(CONVENTIONS §4.5)의 `workitems/*.md` 중 `status: review`인 항목과 그 PR/브랜치를 모읍니다.

---

## 1. 통합 대상 수집

* `workitems/*.md`에서 `status: review`인 workitem과 그 PR/브랜치를 모읍니다.
* 각 workitem의 `touches`(contracts/modules)와 `depends_on`을 확인합니다.

---

## 2. 충돌 재검출 (merge 전 — 필수, 에이전트가 수행)

`git fetch` 후(CONVENTIONS §4.5), 통합 후보 + 다른 in-flight(`claimed`/`in_progress`) workitem 전체의 `touches`를 전수 교차합니다.

* **contracts 겹침(STOP):** 두 개 이상이 같은 전역 계약을 건드림 → §3 직렬화로 처리. 동시에 merge하지 않습니다.
* **modules 겹침(WARN):** `conflicts/CF-*.md`에 해소 결정이 있는지 확인. 없으면 등재하고 owner들과 순서를 합의한 뒤 진행.
* **식별 검증:** 각 후보의 feature 브랜치 commit author email이 `WI.owner`의 등록 email과 일치하는지 확인(불일치 = "claim한 사람 ≠ 작업한 사람" → 보고).

---

## 3. 전역 계약 직렬화 (계약 변경 workitem 우선)

`touches.contracts`가 있는 workitem이 있으면 **그것을 먼저** 처리합니다.

1. 해당 ADR이 `Accepted`인지 확인(아니면 검토·승인).
2. 계약 변경 workitem을 merge합니다.
3. **maintainer가** `ARCHITECTURE.md`(필요 시 `PLAN.md`)를 갱신합니다 — 이것은 maintainer single-writer 영역입니다.
4. 같은 contract를 `touches`하던 나머지 workitem은 **새 계약으로 rebase**하도록 owner에게 통지합니다(rebase 전에는 merge하지 않음).

---

## 4. Merge

직렬화 순서(계약 변경 → 의존 workitem → 독립 workitem)대로 PR을 merge합니다.

* git 충돌은 일반 절차로 해소합니다.
* 고정 INDEX 파일이 없으므로 INDEX merge 충돌은 발생하지 않습니다.
* merge 후 각 `WI-*.md` status를 `done`으로 바꾸고, 같은 공유 브랜치 커밋에서 파일을 `workitems/archive/WI-*.md`로 이동합니다 (maintainer가 커밋 — WI single-writer 규칙의 공인된 예외, CONVENTIONS §4.1/§9). 이로써 `workitems/`는 활성 작업만 남아 이후 검출(§2)과 AUDIT §3.4가 지난 workitem을 전부 열어보지 않아도 됩니다.

---

## 5. 이력 기록 (maintainer single-writer)

merge된 workitem마다 `history/YYYY/MM/HIST-<YYYYMMDD-hhmm>-<slug>.md`를 **새 파일로** 생성합니다(`templates/` 형식). 포함: 완료된 workitem, 관련 commit, 실행한 테스트 결과, 관련 source, QA, 영향 범위, follow-up.

> `history/`는 INTEGRATE만 기록합니다. 기여자는 `history`에 쓰지 않습니다(append 경합 제거).

---

## 6. SOURCES 상태 갱신

merge로 요구가 반영 완료된 source는 `SOURCES/SRC-*.meta.md`의 `status`를 `applied`로 바꾸고 반영 산출물을 링크합니다. 모든 항목이 반영됐을 때만 `applied`(부분 반영은 `under_review` 유지).

---

## 7. 전체 회귀 & PROGRESS

* **전체 회귀 테스트를 실제로 실행**합니다 — 개별 기여자는 자기 부분만 봤으므로 통합 시점에 전체를 확인합니다. 결과를 history에 기록합니다.
* `ARCHITECTURE.md` 계약이 최근 코드에서 지켜지는지 표본 점검(어긋나면 `conflicts/` 또는 후속 workitem).
* `PROGRESS.md`(호환 스텁)가 항목 파일을 가리키도록 유지합니다 — 진행 상태의 진실은 `workitems/*.md` frontmatter임을 명시(고정 INDEX 없음).

---

## 8. 완료 보고 형식

```md
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

---

## 9. 주기적 audit과의 관계

INTEGRATE는 *합류 정합*을, AUDIT는 *점진 표류 회수*를 담당합니다. Phase 완료/릴리즈 전에는 AUDIT을 별도로 실행해 고아 workitem, 미검출 `touches` 겹침, 방치된 `SRC-*.meta`(미반영), 끊어진 링크, stale 세션을 점검합니다.
