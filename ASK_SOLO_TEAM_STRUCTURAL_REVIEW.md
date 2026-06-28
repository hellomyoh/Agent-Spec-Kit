# ASK Solo / Team 프롬프트 구조 검토

작성일: 2026-06-28

## 검토 범위

이 문서는 저장소의 ASK 프롬프트 체계를 `ASK Solo`와 `ASK Team`으로 해석해, 구조적 설계 결함, 오작동 가능성, 의도와 다르게 동작할 여지를 검토한 것이다.

검토 대상:

- `README.md` / `README.ko.md`의 사용 흐름과 기능 추가 검토 프롬프트
- `en/AGENTSPECKIT/KICKOFF.md`
- `en/AGENTSPECKIT/DEVELOPINIT.md`
- `en/AGENTSPECKIT/ADOPT.md`
- `en/AGENTSPECKIT/AUDIT.md`
- 기존 검토 초안 `benchmark/ASK_PROMPT_AND_BENCHMARK_REVIEW.md`

저장소에는 `ask solo`, `ask team`이라는 독립 프롬프트 파일이 직접 존재하지 않는다. 이 문서에서는 다음처럼 정의한다.

| 구분 | 해석 |
|---|---|
| ASK Solo | `DEVELOPINIT.md` 기반의 단일 에이전트 개발 루프. AGENTS/ARCHITECTURE/PLAN/PROGRESS를 항상 읽고, 필요한 feature/ADR/QA/NOTES/SOURCES를 선택 로드해 구현, 테스트, 문서 갱신, 커밋까지 수행한다. |
| ASK Team | KICKOFF/DEVELOPINIT/README 5.3에 있는 Multi-Agent/persona 검토 루프. 단일 모델 역할극 또는 실제 서브에이전트 병렬 검토를 통해 feature/ADR/QA에 설계 결론을 반영한다. |

## 요약

현재 ASK 설계는 “문서화된 단일 진실 공급원(SSOT)을 유지해 장기 개발에서 drift를 줄인다”는 방향은 타당하다. 그러나 프롬프트만으로 강제되는 체계이므로, 실제 에이전트가 절차를 건너뛰거나 문서만 그럴듯하게 맞추는 상황을 충분히 막지는 못한다.

가장 큰 위험은 다음 네 가지다.

1. Solo는 필수 확인 문서와 갱신 문서가 많아, 작은 작업에서 절차 피로와 토큰 비용이 구현 품질을 잠식할 수 있다.
2. Team은 실제 독립 검토와 단일 모델 역할극의 차이를 인정하지만, 산출물 형식이 같아 “독립 검토를 한 것처럼 보이는 로그”가 만들어질 수 있다.
3. SOURCES, ARCHITECTURE, features, ADR, PLAN, PROGRESS, TODO, ASSUMPTIONS 사이의 권위 관계가 복잡해 최신 채팅 지시나 부분 적용 요청과 충돌할 여지가 있다.
4. AUDIT는 사후 복구 장치라서 유용하지만, 프롬프트 실행 중의 누락을 예방하지는 못한다.

## 공통 구조 결함

### 1. 프롬프트 규칙이 실행 강제 장치가 아니다

ASK는 “읽어라”, “업데이트하라”, “실제로 테스트하라”, “로그를 남겨라”를 강하게 지시하지만, 이를 시스템적으로 검증하는 체크포인트는 부족하다. 에이전트가 다음을 생략해도 산출물만 보면 즉시 드러나지 않을 수 있다.

- `SOURCES/INDEX.md`의 미적용 변경요청 확인
- 실제 테스트 실행
- 코드-명세 불일치의 권위 진단
- ADR 작성 트리거 판단
- discussion 로그의 근거/출처 검증
- PROGRESS의 선기록과 종료 기록

AUDIT가 이를 사후 점검하도록 설계되어 있으나, 문제 발생 시점에는 이미 잘못된 코드나 문서가 커밋될 수 있다.

개선 방향:

- 개발 루프 시작 시 `required preflight checklist`를 고정 형식으로 남기게 한다.
- 종료 시 `completion gate`를 체크박스가 아니라 “근거 파일/명령/결과”와 함께 쓰게 한다.
- 테스트 실행 결과, ADR 필요 여부, SOURCES 상태는 보고서에 필수 필드로 두고 누락 시 작업 미완료로 간주한다.

### 2. 권위 체계가 강력하지만 복잡하다

문서별 역할은 잘 분리되어 있다.

- `ARCHITECTURE.md`: 횡단 계약
- `features/*.md`: 기능 명세
- `adr/*.md`: 장기 결정
- `SOURCES/`: 사용자 제출 원본
- `PLAN.md`: 구현 계획과 상태
- `PROGRESS.md`: 다음 세션 인계
- `ASSUMPTIONS.md`: 미확정 자율 판단
- `NOTES.md`: 확인된 사실
- `TODO.md`: 비공식 백로그

문제는 실제 개발 세션에서 사용자가 채팅으로 “그냥 이대로 해줘”라고 말할 때 생긴다. `DEVELOPINIT.md`는 채팅 지시와 SOURCES 절차의 관계를 설명하지만, 에이전트 입장에서는 “채팅 최신 지시”, “아직 Applied가 아닌 변경요청”, “기존 ARCHITECTURE 계약” 사이에서 어느 쪽을 먼저 따라야 하는지 매번 판단해야 한다.

오작동 가능성:

- 미적용 SOURCES 문서를 사실상 권위 문서처럼 읽고 구현한다.
- 최신 채팅 지시를 이유로 ARCHITECTURE/features/ADR 갱신을 생략한다.
- 부분 반영된 변경요청을 `Applied`로 처리한다.
- TODO 항목을 명세처럼 취급한다.

개선 방향:

- 권위 우선순위를 한 줄로 고정한다: `사용자 최신 명시 지시 > 안전/승인 규칙 > Applied artifacts(ARCHITECTURE/features/ADR/PLAN) > ASSUMPTIONS/NOTES > SOURCES/TODO 초안`.
- 단, 최신 채팅 지시가 횡단 계약을 바꾸면 “구현 전 artifacts 반영”이 필수라는 예외를 더 눈에 띄게 둔다.
- `SOURCES/INDEX.md` 상태 전이를 위한 최소 검증 항목을 표준화한다.

### 3. 문서 유지 비용이 구현 집중을 방해할 수 있다

Solo 개발 루프는 구현 전후로 많은 문서 갱신을 요구한다. 중대형 장기 프로젝트에서는 유리하지만, 작은 변경에서는 다음 부작용이 생길 수 있다.

- 실제 코드 분석보다 문서 형식 맞추기에 집중한다.
- 문서 갱신을 끝내기 위해 확인하지 않은 사실을 기록한다.
- HISTORY/PROGRESS/PLAN/feature 상태가 서로 불일치한다.
- 에이전트가 커밋까지 진행하려다 현재 저장소 정책이나 사용자의 의도와 충돌한다.

개선 방향:

- 작업 규모별 루프를 나눈다.
  - `micro`: 코드/테스트만, 문서 변경 없음 또는 HISTORY 한 줄
  - `normal`: feature/PLAN/PROGRESS/HISTORY 갱신
  - `contract`: ARCHITECTURE/ADR/SOURCES 절차 포함
- 문서 갱신 필수 조건을 “파일 종류”가 아니라 “사용자 영향, 횡단 계약 영향, 상태 변경 여부”로 판정한다.

## ASK Solo 검토

### 1. 항상 로드 문서의 비대화 위험

`DEVELOPINIT.md`는 매 세션 `AGENTS.md`, `ARCHITECTURE.md`, `PLAN.md`, `PROGRESS.md`를 항상 읽게 한다. 이 자체는 올바른 안정장치지만, 프로젝트가 커지면 항상 로드 문서가 배경 설명과 과거 상태를 끌고 들어와 오히려 현재 작업을 흐릴 수 있다.

오작동 가능성:

- `ARCHITECTURE.md`가 계약 선언이 아니라 설명서처럼 비대해진다.
- `PLAN.md`에 완료 Phase가 누적되어 현재 작업을 찾기 어렵다.
- `PROGRESS.md`의 “first command”가 낡으면 잘못된 작업을 재개한다.

개선 방향:

- `ARCHITECTURE.md`는 선언형 계약만 유지하고 배경/폐기 계약은 ADR로 이동한다.
- `PLAN.md` 완료 Phase 4개 초과 아카이브 규칙을 개발 루프에서도 점검한다.
- `PROGRESS.md` 첫 명령은 “현재 코드 상태와 대조 후 실행”이라는 게이트를 더 강하게 둔다.

### 2. 코드-명세 권위 진단은 좋지만 실행 비용이 크다

코드와 명세가 다를 때 바로 고치지 않고 권위를 진단하라는 규칙은 매우 중요하다. 그러나 실제 세션에서는 작은 불일치마다 이 절차를 수행하면 비용이 커지고, 반대로 에이전트가 귀찮아서 명세를 코드에 맞춰 덮어쓸 수 있다.

오작동 가능성:

- 구현 버그가 사후에 “명세였던 것”으로 둔갑한다.
- 명세가 오래됐다는 이유만으로 사용자의 원래 의도가 삭제된다.
- 권위 진단 결과가 HISTORY/ASSUMPTIONS에 남지 않는다.

개선 방향:

- 불일치를 `typo/mechanical`, `behavioral`, `contract` 세 등급으로 나눈다.
- `behavioral` 이상은 권위 진단 기록을 필수로 한다.
- “명세 수정만으로 해결”하는 경우 커밋 메시지와 HISTORY에 사유를 남기게 한다.

### 3. 테스트 실행 규칙은 충분하지만 증거 형식이 약하다

프롬프트는 “실제로 실행한 테스트만 통과로 인정”한다고 명시한다. 다만 보고서의 실행 명령과 pass/fail 요약만으로는, 에이전트가 부분 테스트를 전체 테스트처럼 표현하는 문제를 완전히 막기 어렵다.

오작동 가능성:

- 일부 테스트만 실행하고 전체 품질이 검증된 것처럼 보고한다.
- 실패한 테스트를 “환경 문제”로 뭉뚱그린다.
- 테스트를 실행하지 않고 QA 문서만 갱신한다.

개선 방향:

- 테스트 결과에 `scope`, `command`, `exit status`, `not run reason`을 분리해 기록한다.
- 전체 테스트를 못 돌렸다면 “미검증 영역”을 PROGRESS의 remaining work에 넣게 한다.

## ASK Team 검토

### 1. 역할극과 실제 병렬 검토가 혼동될 수 있다

README 5.3과 KICKOFF 4.1은 역할극과 실제 병렬 서브에이전트 검토를 구분하고, 실제 수행 방식을 로그에 쓰라고 한다. 이 구분은 타당하지만, 산출물 형식이 같으므로 사용자가 결과만 보면 독립 검토였는지 알기 어렵다.

오작동 가능성:

- 서브에이전트 도구가 없는데 “parallel review”라고 기록한다.
- 단일 모델이 여러 persona 의견을 만든 뒤 독립 검토처럼 요약한다.
- Research Agent가 실제 조사 없이 일반론을 출처 있는 결론처럼 쓴다.

개선 방향:

- discussion 로그의 `Execution mode`에 `role-play`, `parallel-subagents`, `parallel-external`처럼 제한된 enum을 사용한다.
- 실제 병렬 검토라면 각 서브에이전트의 입력 범위, 출력 요약, 실행 시각 또는 식별자를 남긴다.
- Research Agent는 출처가 없으면 결론을 “조사 실패/미확정”으로만 반영한다.

### 2. persona 인스턴스가 형식화될 위험

KICKOFF는 persona 파일이 카탈로그 복사가 아니라 프로젝트별 체크리스트와 링크를 가져야 한다고 요구한다. 그러나 초기화 시 에이전트가 빠르게 진행하면 일반론 체크리스트만 생성할 수 있다.

오작동 가능성:

- Security/QA/DB persona가 모든 프로젝트에서 거의 같은 문구를 반복한다.
- persona가 ARCHITECTURE/NOTES 내용을 복사해 SSOT가 깨진다.
- feature와 무관한 persona가 참여해 로그만 길어진다.

개선 방향:

- persona 파일에는 최소 3개 이상의 프로젝트 고유 링크를 요구한다.
- review 로그에는 “왜 이 persona가 필요한지”와 “왜 제외한 persona가 있는지”를 짧게 남긴다.
- persona별 출력은 일반 의견이 아니라 검증 가능한 실패 조건 또는 테스트/체크리스트 항목을 최소 1개 이상 포함하게 한다.

### 3. 합의 요약이 갈등을 지울 수 있다

Team의 최종 산출물은 feature 문서에 합의된 명세만 남기고, 상세 토의는 discussion에 둔다. 구현자가 읽기에는 좋지만, 합의되지 않은 위험이나 보류된 갈등이 feature 문서에서 사라질 수 있다.

오작동 가능성:

- 치명적 반대 의견이 “합의됨”으로 정리된다.
- ADR이나 사용자 확인이 필요한 결정을 feature 내부 문장으로 묻어둔다.
- QA/Security가 제기한 실패 조건이 테스트 시나리오로 연결되지 않는다.

개선 방향:

- review 로그 결론에 `resolved`, `deferred`, `requires user decision`, `requires ADR` 상태를 둔다.
- feature 문서의 리뷰 요약에는 “남은 쟁점 없음/있음”을 명시한다.
- QA/Security/DB persona가 제기한 위험은 반드시 feature test scenario 또는 qa 문서 항목으로 추적한다.

## ADOPT / AUDIT와의 상호작용 문제

### ADOPT

ADOPT는 기존 코드를 실제로 읽고 as-built 명세를 만들도록 설계되어 있다. 하지만 대형 코드베이스에서는 한 세션에 충분히 읽기 어렵다.

오작동 가능성:

- 파일명과 폴더 구조만 보고 동작을 추정한다.
- 읽지 않은 영역을 “estimated”로 표시하지 않는다.
- as-built 명세가 현재 코드의 버그를 제품 의도로 오인한다.

개선 방향:

- `read coverage table`을 필수화한다.
- 각 feature의 주요 동작 주장에는 코드 위치 또는 테스트 근거를 요구한다.
- adoption을 1회 완료 이벤트가 아니라 coverage-driven 단계 작업으로 운영한다.

### AUDIT

AUDIT는 drift 복구에 유용하지만, 발견 후 처리 연결이 약하면 “문제 목록”만 쌓인다.

오작동 가능성:

- semantic drift를 기록만 하고 다음 개발에서 처리하지 않는다.
- review 로그 위조/부실을 찾아도 재검토 작업으로 이어지지 않는다.
- ASSUMPTIONS active 항목이 계속 남는다.

개선 방향:

- AUDIT finding에 severity와 owner 문서를 부여한다.
- `major/blocker` finding은 PLAN 또는 PROGRESS에 follow-up task로 자동 반영하게 한다.
- 다음 DEVELOPINIT 세션은 audit follow-up을 먼저 확인하도록 한다.

## 우선순위별 개선 권고

### P0: 즉시 보완 권고

1. Solo 시작/종료 게이트를 고정 형식으로 추가한다.
2. 권위 우선순위와 최신 채팅 지시의 처리 규칙을 더 명확히 한다.
3. Team 로그의 실행 모드를 enum으로 제한하고, 실제 병렬 검토 증거를 요구한다.
4. 테스트 결과 기록에 `scope`, `command`, `exit status`, `not run reason`을 추가한다.

### P1: 다음 버전 보완 권고

1. 작업 규모별 `micro / normal / contract` 루프를 만든다.
2. persona 인스턴스의 프로젝트 고유성 기준을 추가한다.
3. Team 리뷰의 위험 항목이 QA/test 항목으로 연결되는 추적 필드를 추가한다.
4. AUDIT finding을 PLAN/PROGRESS follow-up으로 연결하는 큐를 만든다.

### P2: 벤치마크에서 검증할 항목

1. ASK Solo가 일반 notes 방식보다 장기 regression과 invariant violation을 줄이는지 측정한다.
2. ASK Team role-play와 실제 parallel subagents를 분리해 효과를 비교한다.
3. review 로그 품질이 아니라 실제 hidden failure 감소율을 주요 지표로 둔다.
4. 문서 유지 비용이 작은 작업에서 성능을 떨어뜨리는 임계점을 찾는다.

## 결론

ASK Solo는 장기 프로젝트의 기억 보존과 횡단 계약 유지에 유리하지만, 절차가 무거워질수록 에이전트가 핵심 확인을 건너뛰거나 문서 형식만 맞출 위험이 있다. 따라서 Solo에는 사전/사후 게이트와 작업 규모별 경량화가 필요하다.

ASK Team은 설계 검토의 품질을 높일 가능성이 있지만, 현재 구조만으로는 역할극과 실제 독립 검토가 쉽게 섞일 수 있다. Team의 신뢰성은 persona 수나 로그 길이가 아니라, 검토에서 나온 위험이 검증 가능한 실패 조건, 테스트, ADR, 사용자 확인 항목으로 얼마나 연결되는지로 판단해야 한다.

전체적으로 ASK의 방향은 유효하지만, “프롬프트가 말한 절차”와 “실제로 수행된 절차”를 구분해 검증하는 장치가 더 필요하다. 다음 개선의 핵심은 더 많은 문서를 만드는 것이 아니라, 권위 관계를 단순화하고, 검토/테스트/갱신의 증거를 작고 명확한 형식으로 남기는 것이다.
