# AUDIT.md — 팀 문서 감사 (ASK-Team)

팀 동시 개발에서 누적되는 표류와 **조율 구조의 무결성**을 주기적으로 점검합니다.
solo 킷 AUDIT.md([reference/SOLO-AUDIT.md](reference/SOLO-AUDIT.md))의 일반 표류 점검(계획↔실제, 가정 수명, 명세↔코드, 링크, 이력 위생)에 더해, **팀 전용 점검**을 추가합니다.

> 규약은 [CONVENTIONS.md](CONVENTIONS.md)가 우선합니다. INTEGRATE는 *합류 정합*, AUDIT는 *점진 표류 회수*를 담당합니다.

---

# 1. 실행 시점

* Phase 완료 직후 / 릴리즈 전 / 오랜만에 재개 / 마지막 감사 후 세션 ~10회 누적 / 표류 의심 시
* **여러 기여자가 동시에 활동 중일 때 정기적으로**(in-flight workitem이 많을수록 자주)

---

# 2. 감사 원칙

1. 기능 코드를 수정하지 않습니다.
2. **기계적 불일치는 즉시 수정**(끊어진 링크, 명백한 상태 오기). 고정 INDEX 파일이 없으므로 인덱스 재생성 단계는 없습니다.
3. **의미적 표류는 기록만**(코드↔명세는 DEVELOP 권위 진단, touches 겹침은 conflicts/로).
4. 감사 결과는 `history/YYYY/MM/HIST-*.md`에 `audit` 이벤트로 기록(maintainer).

---

# 3. 감사 항목

## 3.1 일반 (solo AUDIT 3.1~3.12 계승 — [reference/SOLO-AUDIT.md](reference/SOLO-AUDIT.md))
계획↔실제, 가정 수명, 명세↔코드 표본, 링크/고아, README, 항상로드 비대화(ARCHITECTURE/PLAN), 검토 로그(출처 실재), 산출물 언어 일관성.
**팀 재매핑** (아래 solo 항목은 팀 등가물로 대체 — 문자 그대로 적용하지 않습니다):
* 인덱스 무결성(solo 3.4) → 해당 없음: 고정 INDEX 없음(§3.2). 대신 항목 파일 frontmatter가 정형인지(필수 필드 존재) 표본 점검.
* 백로그 TODO.md(solo 3.11) → `proposed`/`ready` workitem 위생(§3.3).
* HISTORY 회전(solo 3.6) → `history/YYYY/MM/`는 날짜 분할이라 회전 불필요(CONVENTIONS §9); 형식 점검은 `HIST-*.md` 이벤트에 적용.
* SOURCES INDEX(solo 3.8) → `SRC-*.meta.md`·`REQUIREMENTS.meta.md` 상태 점검(§3.6).
* 단일 ASSUMPTIONS/HISTORY/NOTES 파일 → `assumptions/`·`history/`·`notes/` 디렉토리.

## 3.2 고정 INDEX 부재 확인
* 누군가 `INDEX.md` 같은 고정 인덱스 파일을 만들어 커밋하지 않았는가 — 이 킷은 고정 INDEX를 두지 않습니다(발견 시 삭제 후보로 보고). 목록·상태는 항상 항목 파일 frontmatter에서 직접 읽습니다.

## 3.3 workitem 위생
* `claimed`/`in_progress` 상태로 장기 방치된(예: 14일+) workitem — owner에게 상태 재확인.
* `owner`가 `team/`에 등록된 active handle인가(미등록·inactive → flag).
* `done`인데 대응 `history/` 이벤트가 없는 workitem / `feature`·`source_refs` 링크가 끊어진 workitem.
* 고아 workitem(어떤 PLAN Phase·source와도 연결 안 됨).

## 3.4 미검출 touches 겹침 (핵심)
* `git fetch` 후(CONVENTIONS §4.5) 최신 공유 브랜치에서 in-flight(`claimed`/`in_progress`) workitem 전체의 `touches`를 읽어 쌍별로 교차합니다(에이전트가 직접 수행).
  * **contracts 겹침인데 `conflicts/CF`도 없고 직렬화도 안 된 쌍** → 즉시 보고(maintainer 직렬화 필요).
  * **modules 겹침인데 `conflicts/CF` 미등재** → CF 등재를 후속 작업으로.

## 3.5 식별 / 권한 무결성
* 최근 commit author email이 모두 `team/`에 등록돼 있는가(미등록 author = 귀속 오염).
* `WI.owner`와 해당 feature 브랜치 commit author가 일치하는가(claim한 사람 ≠ 작업한 사람).
* **single-writer 위반:** contributor가 `ARCHITECTURE.md`/`PLAN.md`를 직접 수정했는가(git 이력으로). 전역 계약 변경에 ADR이 있는가.

## 3.6 conflicts / sessions / SOURCES
* `conflicts/CF-*.md` 중 `open`으로 장기 방치된 것.
* `sessions/`의 `active` 세션이 실제로는 끝난 작업(done workitem)에 매달려 있는가 → `archive/`로 이동 후보.
* `SRC-*.meta.md`가 `not_applied`/`under_review`로 방치된 변경요청(사용자 의도 미반영) / 원본(`SRC-*.md`)이 `applied` 이후 수정되지 않았는가(불변 위반, git 이력).

---

# 4. 처리 규칙

| 발견 | 처리 |
|---|---|
| 끊어진 링크 / 상태 오기 | 즉시 수정 |
| 고정 INDEX 파일이 커밋됨 | 삭제 후보로 보고(고정 INDEX 금지) |
| 미검출 contracts 겹침 | 즉시 보고 → maintainer 직렬화(INTEGRATE §3) |
| 미검출 modules 겹침 | `conflicts/CF` 등재를 후속 작업으로 |
| 방치 workitem / 미등록 owner | owner·maintainer에게 재확인, 보고서에 명시 |
| single-writer 위반(ARCHITECTURE 직접수정) | 되돌리지 말고 기록 → ADR 소급 또는 maintainer 검토 |
| 미등록 author commit | team/ 등록 요청, 보고서에 명시 |
| 방치 미반영 SRC / 불변 위반 | PROGRESS·보고서에 명시, 불변 위반은 새 SRC로 분리할지 maintainer 확인 |

후속 작업은 `workitems/`(proposed) 또는 PLAN에 등재하고, 감사 전체를 `history/`에 `audit` 이벤트로 기록합니다.

---

# 5. 출력 형식

```md
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

---

# 6. 완료 조건

* 3절 점검 완료(샘플링은 기준 명시), in-flight workitem `touches` 쌍별 교차 검출 수행
* 기계적 불일치 즉시 수정
* 미검출 겹침·single-writer 위반·미등록 author가 보고서와 후속 작업에 정리됨
* `history/`에 `audit` 이벤트 기록
