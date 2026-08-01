# Realistic Midscale App Benchmark (OpsBoard) — B7

> 방법론: [METHODOLOGY.ko.md](METHODOLOGY.ko.md) · 이 문서는 [MIDSCALE_DESIGN.md](MIDSCALE_DESIGN.md)의 합성 "교차절단 계약(B4)"을 **대체**한다(B4는 좋은 설계로 자명해져 변별 실패 — M-pilot).
> 출발점: THROUGHLINE이 이기게 만드는 함정이 아니라, **문서 없이 중규모 앱을 오래 개발할 때 실제로 망가지는 지점**(기억·일관성·연동 비용)을 측정한다.

## 0. 가설

> 중규모 앱을 여러 세션에 걸쳐 개발할 때, SSOT/구조화 문서 없이도 **초기 제품 의도·데이터 모델·API 계약·캐시 정책·FE/BE 연동·예외/권한/상태 전이 규칙**을 일관되게 유지할 수 있는가?

검증 명제: **세션이 길어지고 FE/BE/DB/cache 연동면이 넓어질수록, 구조화 SSOT를 유지한 그룹은 제품 일관성·cross-layer completeness·회귀·rework 비용에서 일반 개발보다 *덜 무너진다*** — 또는 못 그런다(반증). 일부 뛰어난 개발자는 머릿속으로 버티지만(강 모델), 대다수는 못 버틴다(약·중 모델/대형 코드).

## 1. 반-조작 원칙 (제1 규칙) + 감사 체크리스트

THROUGHLINE을 위해 규칙을 발명하지 않는다. 측정하는 일관성은 **동작하는 SaaS라면 본질적으로 성립해야 하는 것**뿐이며, **앱의 실제 동작·불변식으로만 채점**한다(문서 갱신 여부 채점 금지). 감사:
- [ ] 모든 숨김 테스트는 *실제 QA가 할 법한* 동작/불변식 검증인가(낚시 함정 아님).
- [ ] 어떤 테스트도 THROUGHLINE 산출물(문서)을 참조하지 않는가.
- [ ] 최소 공유 인터페이스(아래 §5)는 모든 그룹에 *동일* 제공되는가.
- [ ] 티켓은 모호하되(현실), 정답은 비공개 oracle 불변식으로 고정돼 있는가.
- [ ] 고정 oracle 불변식은 (a) 동작하는 SaaS라면 필수인 규칙이거나 (b) 초기 PRD/티켓에서 한 번 명시된 결정인가. 그 외 임의 결정은 자기 과거 결정과의 일관성(self-consistency)으로만 채점하는가.
- [ ] 의도적으로 틀린 구현(negative control)이 cache stale·tenant leak·state violation·permission bypass 검사에 걸리는가.
- [ ] 에이전트 작업공간에서 `oracle/`, hidden tests, scoring harness, negative controls, expected invariants가 물리적으로 차단되는가(P8 격리).
- [ ] 각 세션 시작 전 공유 인터페이스 계약이 import/호출 가능한 stub으로 고정되고, interface-conformance 실패가 제품 로직 점수와 분리 보고되는가.
- [ ] 티켓 모호도, B-limited `N/K`, memory 산출물 soft cap, chain-death 처리 규칙이 Stage 0 전에 사전등록되는가.

## 2. 앱 — OpsBoard (팀 기반 작업 운영 SaaS)

도메인: 조직/팀/멤버 · 프로젝트 · 작업 요청 · 승인 워크플로우 · 일정/예약 · 댓글/알림 · 첨부 메타 · 권한 · 대시보드 · 검색/필터 · 감사 로그 · 캐시 · optimistic UI · background job. (인위적 계산기/DSL 회피.)

**초기 PRD(짧게 — 실제 제품팀처럼 의도만):**
- 팀은 여러 프로젝트를 가진다. 프로젝트엔 작업 요청이 있다.
- 작업 요청 상태: `draft → submitted → approved/rejected → scheduled → completed`.
- 승인자 = 팀 관리자 또는 프로젝트 소유자. **승인 후 핵심 필드 임의 수정 불가.**
- 일정 충돌 금지. 목록 화면은 빠르게. **권한 없는 사용자는 존재 여부도 알 수 없어야.** 변경 이력은 추적 가능해야.
- 이 벤치마크에서는 승인 후 핵심 필드를 `title, scope, owner`로 고정한다. 이 값은 PRD/티켓에서 한 번 명시된 결정으로 취급하므로, 해당 규칙은 `conformance`로 채점한다.
- (세부 구현은 주지 않는다 — 구현하며 구체화.)

## 3. 비교군 (손실적 기억 vs 문서화된 기억을 공정하게)

> **B-fresh 단독은 금지.** 매 세션 새 에이전트는 머릿속 기억조차 없어 "기억상실 vs 문서화"를 재게 되고 THROUGHLINE 효과를 과장한다. 반대로 무제한 long-context `B-continuing`은 현대 모델이 전체 이력을 완벽 회상해 다시 천장을 만들 수 있다. 따라서 **최근 일부 맥락만 가진 `B-limited`가 1차 baseline**이다.

| 그룹 | 인계 | 현실 대응 |
|---|---|---|
| **B-fresh** | 매 세션 새 에이전트, 코드+테스트만 | 매번 새 개발자 투입, 제품 문서 0 (바닥 기준점) |
| **B-limited** | 최근 N세션 또는 최근 K토큰 맥락만 유지, 구조화 문서 없음 | **대다수 개발자 — 손실적 머릿속 기억** ← 1차 baseline |
| **B-continuing** | fresh 에이전트 + 이전 전체 세션 맥락 concat, 구조화 문서 없음 | long-context 상한/천장 진단 |
| **P** | fresh + 자유 노트(TODO), soft cap | 계획·메모는 하나 비구조 |
| **THROUGHLINE** | fresh + SSOT 7종 | 계약을 적어두는 팀 |

THROUGHLINE SSOT: `PRODUCT.md`(의도·흐름) · `DATA_MODEL.md`(스키마·관계·상태전이) · `API_CONTRACTS.md`(FE/BE 계약) · `CACHE_POLICY.md`(키·TTL·무효화) · `ARCHITECTURE.md`(FE/BE/cache/db 책임경계) · `DECISIONS.md`(유지해야 할 결정) · `PROGRESS.md`.

**각 대비가 분리하는 것:** `B-limited − B-fresh` = 손실적 지속 기억의 유무 / **`THROUGHLINE − B-limited` = 구조화 SSOT가 손실적 머릿속 기억을 이기는가(1차)** / `THROUGHLINE − P` = 구조 vs 비구조 노트 / `B-continuing − B-limited` = long-context 완벽 회상 천장.

**통제·구현:**
- THROUGHLINE만 정보 과다 금지. 단, **P와 THROUGHLINE 토큰을 하드 동일화하지 않는다.** 자유 노트를 억지로 늘리거나 THROUGHLINE 문서를 억지로 줄이면 비현실적이다. 대신 기억 산출물 크기, 문서 갱신 토큰, 총 프롬프트 토큰, 세션별 입력 토큰을 기록하고 soft cap 초과를 보고한다.
- THROUGHLINE 기억 산출물 토큰이 P보다 크게 초과하면 구조 효과와 분량 효과가 교란된 것으로 보고한다. 이 경우 결론을 약화하고, 필요하면 `P-verbose` 보조 arm(자유 노트를 THROUGHLINE과 비슷한 분량까지 허용)을 추가해 구조 효과와 볼륨 효과를 분리한다.
- B-limited = 세션마다 fresh 에이전트 + 최근 `N`세션 티켓/결과 또는 최근 `K`토큰 대화 요약만 제공. `N/K`는 THROUGHLINE 격차를 키우기 위해 조정하지 않는다. 독립 정당화는 "개발자는 최근 2–3개 기능은 또렷하지만 오래된 세부 결정은 흐릿해진다"는 작업기억 근사다.
- `N/K`는 본실행 전 사전등록하고, 단일 값만으로 결론 내지 않는다. 1차 값은 `N=2` 또는 `N=3` 중 Stage -1에서 정한 하나로 고정하되, Stage 1부터 최소 1개 보조 값으로 민감도(sensitivity)를 보고한다. THROUGHLINE 우위가 특정 N/K에서만 나타나면 "메모리 예산 의존"으로 해석하고 일반 결론을 보류한다.
- B-continuing = 세션마다 fresh 에이전트를 띄우되 이전 전체 세션 대화/티켓/결과를 누적 concat해 제공한다. 특정 런타임의 agent resume이나 대화 재개 API 지원에 의존하지 않는다. concat 결과가 문맥창을 넘으면 별도 cap으로 잘라내지 말고 자연 붕괴를 허용하되, 최초 초과 세션과 성능 변화를 로그에 남긴다. 이는 실제 대다수 개발자보다 강하므로 1차 baseline이 아니라 **천장/상한 진단**이다.
- THROUGHLINE/P = 세션마다 fresh + 디스크 기억 산출물. THROUGHLINE은 구조화 SSOT, P는 자유 노트.
- **비용 해석은 baseline별로 분리한다.** B-limited는 최근 맥락만 제공하므로 THROUGHLINE이 세션당 더 비쌀 수 있다. 이 대비의 헤드라인은 "더 비싸지만 덜 무너지는가"다. B-continuing 대비에서만 THROUGHLINE이 전체 대화 concat보다 싸면서 덜 무너지는 문맥 압축 효과를 주장할 수 있다.

해석상 `B-limited`는 실제 사람 기억의 거친 근사다. 최근-N 윈도우는 오래된 핵심 의도까지 잃을 수 있지만, 사람은 오히려 핵심 의도는 유지하고 세부 구현 결정을 잃는 경우가 많다. 따라서 `THROUGHLINE − B-limited`는 "손실적 기억 대비" 신호이고, 현실적 개발 방식의 핵심 비교는 `THROUGHLINE − P`(비구조 메모 vs 구조화 SSOT)도 함께 본다.

## 3.1 파일시스템 격리 (P8 — 하드 요구)

에이전트 작업공간에는 **현재 코드, 해당 그룹의 기억 산출물, 현재 세션 티켓, 공개 공유 인터페이스**만 둔다. `oracle/`, hidden tests, scoring harness, `negative_controls/`, expected invariants, reference implementation, 이전 세션의 비공개 티켓/검사 결과는 별도 평가 프로세스에만 존재하며 에이전트가 읽을 수 없어야 한다.

이 격리는 권장사항이 아니라 유효성 조건이다. 누수가 확인된 run은 폐기한다. 특히 `rg --files`, `Get-ChildItem -Recurse`, IDE 검색, 테스트 실패 메시지, 로그 산출물로 oracle 세부 규칙이 노출되지 않도록 평가 작업공간과 에이전트 작업공간을 물리적으로 분리한다.

실행 규칙:
- 에이전트는 평가 레포 전체가 아니라 세션별 격리 worktree/작업 디렉터리에서만 실행한다.
- `oracle/`, hidden tests, scoring harness, `negative_controls/`, reference implementation은 에이전트 작업공간의 부모/형제 경로가 아니라 에이전트가 알지도 접근하지도 못하는 평가 전용 경로에 둔다.
- 실행 후 도구 호출 로그를 감사해 작업공간 밖 파일 read/list 시도가 있으면 해당 run을 폐기한다.
- 테스트 실패 메시지는 oracle 세부 기대값을 노출하지 않고, 에이전트에게는 공개 QA 실패 요약만 제공한다.

## 3.2 인계 무결성 및 연쇄 붕괴

세션은 이전 세션의 현재 코드 상태를 그대로 물려받는다. 중간 세션이 빌드를 깨도 evaluator가 임의 수리하지 않으며, 다음 세션도 같은 조건에서 진행한다. 수리는 S12의 공개 QA rework로만 허용한다.

채점은 세션별 현재 상태에 대해 독립적으로 기록한다. 기능 점수는 해당 세션의 공개/숨김 계약이 실행 가능한 경우에만 의미 있게 보고하고, `F2P`(feature-to-product) 점수는 이전 핵심 `P2P`(product-to-product) 불변식이 통과한 경우에만 주지표로 해석한다. 빌드 붕괴·공유 인터페이스 붕괴·핵심 P2P 붕괴로 이후 세션이 구조적으로 실패하는 비율은 `chain-death rate`로 별도 보고한다. 이 값은 메모리 드리프트와 단순 구현 실패를 구분하기 위한 1차 진단 지표다.

## 4. 세션 구조 (≥12 — 짧으면 머리로 버팀)

| S | 기능 | 연동면 |
|---|---|---|
| 0 | 스캐폴드: FE/BE/DB schema/인증 mock, 프로젝트·작업 목록 | 전 계층 기초 |
| 1 | 작업 요청 생성/수정 (migration·API·FE form·validation) | db,be,fe |
| 2 | 상태 전이 draft/submitted/approved/rejected (FE 버튼·BE guard·DB enum) | 전 계층 |
| 3 | 권한 모델 (org admin/project owner/member; API+FE visibility) | be,fe |
| 4 | 일정 예약 (approved만 scheduled, 충돌 방지) | be,db |
| 5 | Redis 캐시 (대시보드/목록, 무효화 정책) | be,cache |
| 6 | 댓글/알림 (상태변경 시 생성, 권한·읽음) | 전 계층 |
| 7 | 감사 로그 (상태/권한/일정 변경 추적) | be,db |
| 8 | 검색/필터 (FE query state·BE params·DB index·cache key) | 전 계층 |
| 9 | 승인 후 수정 제한 강화 (기존과 충돌: FE disabled·BE validation·audit·cache invalidate) | 전 계층 |
| 10 | multi-tenant isolation 강화 (org 누출 금지: API·query·cache key·FE route) | 전 계층 |
| 11 | 대시보드 통계 (DB 집계·cache·stale 정책·FE loading/error) | 전 계층 |
| 12 | 회귀 수정/완성도 (앞선 hidden invariant 실패 일부를 공개 QA 이슈로 전환) | rework |

S9–S11은 **초기 결정·캐시 키·권한이 누적 상호작용**하는 지점 — 현실의 붕괴가 일어나는 곳(발명한 함정 아님).

**티켓 작성 규칙:** 세션 티켓은 실제 이슈처럼 의도 중심으로 쓴다. 예: "승인된 작업만 일정에 올릴 수 있고 충돌 금지, 대시보드 숫자도 맞아야." 단, 하네스 내부에는 각 티켓이 어떤 oracle 불변식·공개 API·QA 조합과 연결되는지 사전 고정한다. 티켓에는 내부 서비스 경계, 캐시 키 형식, DB 테이블 분해 방식처럼 THROUGHLINE이 유지해야 할 심층 정책을 직접 알려주지 않는다.

티켓 모호도는 `N/K`와 같은 자유 변수다. 각 티켓은 Stage 0 전에 `explicit`(공개 명시), `latent`(PRD에서 합리적으로 도출), `open`(여러 합리적 선택 가능)으로 태깅하고 사전등록한다. `explicit/latent`는 conformance로, `open`은 self-consistency로 채점한다. Stage 0에서 모호도가 노이즈를 과도하게 만들면 티켓을 수정한 뒤 다시 사전등록하고, 수정 전 run은 본결론에 쓰지 않는다.

**S12 rework 정의:** S12는 주관적 "품질 개선"이 아니라, S0–S11 hidden 검사에서 실제로 드러난 실패 유형 중 일부를 공개 QA 버그로 바꿔 수정하게 한다. 측정값은 (a) 수정 성공률, (b) 추가 토큰/도구 호출, (c) 변경 라인, (d) 수정 중 새로 만든 회귀다.

## 5. 트랙터블 구현 (보완 — 외부 서비스 없이 결정적)

진짜 브라우저/Redis/DB/E2E는 고비용·플래키. 네 계층을 **인프로세스 순수 파이썬 모듈**로 모의:
- `db`: SCHEMA 선언형 인메모리 저장소(미선언 컬럼/타입 위반 = 에러).
- `cache`: TTL dict + get/set/invalidate(키 관례, 무효화 누락 시 stale).
- `backend`: `handle(request)->response` 디스패처(엔드포인트→핸들러; db·cache 사용).
- `frontend`: `render(view, backend, client_state)->dict`(엔드포인트 호출, 특정 응답 필드 소비, route/query/form/local 상태 반영).
- optimistic UI/background job = **결정적 훅**(즉시 실행 큐)으로 모의.

`frontend`는 단순 dict 변환기가 아니라 상태적 클라이언트 모의다. 최소 상태는 `route_params`, `query_params`, `form_state`, `view_cache`, `pending_optimistic_actions`, `last_error`를 포함한다. 이 정도는 순수 Python으로 결정적으로 유지하면서도 실제 FE에서 흔한 stale local state, disabled/action visibility, loading/error/empty 누락을 잡을 수 있다.

**최소 공유 인터페이스(반-조작·결착 동시 해결):** 엔드포인트 이름·요청 형태와 `render(view,...)` 진입점은 **모든 그룹에 동일 제공**(현실의 API 합의). 하네스 테스트는 이 공유 표면을 통해 *동작*을 검증. THROUGHLINE의 차별점은 그 위의 **깊은 정책**(데이터모델·캐시 무효화·상태기계·권한·tenant)이며, 이는 공유 표면이 강제하지 않는다.

공유 인터페이스는 문서가 아니라 import 가능한 stub/contract package로 제공한다. 각 세션 채점 전 `interface-conformance` 사전체크를 실행해 endpoint 이름, request/response shape, `render(view, backend, client_state)` 진입점이 붙는지 확인한다. 이 실패는 제품 로직 실패와 분리 보고하며, interface가 붙지 않는 세션의 hidden logic 점수는 별도 `not attachable`로 표시한다.

공유/비공개 경계:
- **공개 제공**: endpoint 이름, request shape, view 진입점, seed data format, 공통 테스트 실행법.
- **비공개 oracle**: 상태 전이, 권한 매트릭스, cache invalidation, tenant scoping, 승인 후 수정 제한, 제품 불변식.
- **공개 금지**: 내부 service boundary, cache key 구체 형식, DB table 분해 방식, 권한/상태/캐시를 어느 모듈에 둘지에 대한 모범 답안.

공개 인터페이스는 테스트 결착을 위한 외부 계약일 뿐이다. 내부 파일을 많이 만졌는지, `cache.py`를 편집했는지, 특정 service layer를 만들었는지는 1차 점수에 쓰지 않는다.

모든 oracle 불변식은 공개 표면(`handle`, `render`, seed/import/export, client state 결과)으로 관측 가능해야 한다. 예를 들어 cache stale은 dashboard/list 렌더 결과로 드러나야 하고, permission bypass는 FE 숨김뿐 아니라 API 직접 호출 결과로 드러나야 하며, tenant leak은 다른 org 컨텍스트의 공개 응답에서 관측되어야 한다. 캐시가 항상 재계산되어 stale이 관측 불가능하거나, 권한 위반이 내부 구조검사로만 잡히면 해당 불변식은 1차 지표에서 제외하고 하네스를 수정한다.

## 6. 측정 지표 (객관 우선)

| 분류 | 지표 |
|---|---|
| **객관(1차)** | Functional correctness, **Schema/API/FE 일치**(필드 불일치 수), **Cache correctness**(stale·키 오류·무효화 누락), **Permission consistency**(FE 숨김 but API 접근 가능), **State-machine integrity**(불가능 전이 허용), **Multi-tenant isolation**(org 누출), **Cross-layer completeness(E2E 행동 기준)**, **Regression rate**(이전 세션 기능 깨짐), **Rework cost**(버그수정 토큰·변경라인), Operational readiness(migration·seed·config·logging 누락) |
| **정성(2차)** | Product consistency rubric(초기 PRD 규칙 위반·UX 산만·동일 개념의 화면별 불일치), UX completeness(loading/error/empty/disabled 누락) |

**헤드라인 = 세션 수에 따른 (불변식 위반·cross-layer completeness·regression·rework)의 *추세*.**

**1차 헤드라인 지표(사전등록):**
- `Invariant violations`: state/permission/cache/tenant/product 불변식 위반 수.
- `Cross-layer completeness`: 기능이 FE 진입점에서 사용자 행동으로 시작해 backend/API, DB 저장, cache 반영/무효화, 다시 FE 렌더 결과까지 일관되게 완료되는지. 구조 편집 여부나 touched file 수로 채점하지 않는다.
- `Regression rate`: 이전 세션에서 통과한 동작 중 깨진 비율.
- `Rework cost`: S12에서 공개 QA 이슈를 고치는 데 필요한 추가 토큰·도구 호출·변경 라인·2차 회귀.

예: FE 버튼은 보이지만 API가 저장하지 못하면 실패, API는 저장하지만 FE 목록/대시보드가 stale이면 실패, FE는 숨기지만 API 직접 호출이 가능하면 permission failure다.

합산 점수는 보조로만 쓴다. 합산이 필요하면 사전등록 가중치는 `functional 30 / invariants 30 / cross-layer 20 / regression 10 / rework 10`으로 고정한다. `Implementation drift`(의존 사이클·경계 위반·명명 발산), `Operational readiness`, judge rubric은 2차 보조 지표로 보고하고 1차 결론을 뒤집는 데 쓰지 않는다.

`functional` 30점은 기본 구현 역량 확인용이다. 유능한 모델에서는 거의 상수가 될 수 있으므로, 그룹 간 변별 해석은 주로 `invariants + cross-layer + regression + rework`의 약 70점과 세션별 추세에 둔다. functional 차이가 없다면 "THROUGHLINE 효과 없음"이 아니라 "기초 기능은 모두 만들었다"로 해석한다.

## 7. 3층 채점 (judge 신뢰도 보정)

1. **자동 테스트(1차)**: unit·integration·API contract·E2E(인프로세스)·migration·cache invalidation·permission matrix.
2. **정적/구조 검사(진단/보조)**: API 응답↔FE 소비 필드, model↔migration, 캐시 키에 tenant/org 포함, 권한 체크가 service boundary에 있는지, 상태 전이가 단일 경로인지. 가능한 경우 자동 테스트로 환원하고, 구조검사 단독으로 1차 결론을 내리지 않는다.
3. **제품 일관성 rubric(2차)**: 초기 PRD 핵심 규칙 위반, UX 흐름 산만, 개념 표현 불일치. → **judge는 cross-family 3인·위치교차·IRR(κ) 보고, κ<0.40 비공개.** 가능한 항목은 ①②의 객관 불변식으로 변환해 rubric 의존 최소화.

> 자동 테스트만으론 "원래 만들려던 제품에서 멀어졌다"를 못 잡으므로 rubric이 필요하나, 신뢰도 한계상 **보조**로만.

**검사기 검증:** 각 oracle 불변식마다 negative control 구현을 최소 1개 둔다. 예: org_id 없는 cache key, FE만 숨기고 API 권한 체크 누락, `rejected -> scheduled` 허용, 승인 후 title 수정 허용, 일정 변경 후 dashboard cache 무효화 누락. 검사기가 이를 잡지 못하면 해당 불변식은 본실행 전에 수정한다. negative control은 에이전트 작업공간에 절대 포함하지 않는다. 또한 각 negative control은 실패가 공개 표면의 동작 차이로 관측되는지 확인해야 한다.

하네스 저자 단일문화(author monoculture)를 줄인다. Reference, negative control, checker/rubric 중 최소 하나는 다른 사람 또는 다른 모델 패밀리로 독립 생성하거나, 별도 적대적 리뷰를 통과시킨다. 한 작성자가 reference와 checker와 negative control을 모두 만들면 같은 맹점을 공유할 수 있으므로 Stage -1 완료로 인정하지 않는다.

## 8. Oracle = 유지해야 할 제품 불변식 (정답 구현 아님)

`oracle/`에 불변식을 선언(예):
```yaml
state_machine:
  task: {draft: [submitted], submitted: [approved, rejected], approved: [scheduled], rejected: [], scheduled: [completed], completed: []}
permissions:
  approve_task: {allowed_roles: [org_admin, project_owner]}
  post_approval_edit: forbidden_fields: [title, scope, owner]
cache:
  dashboard: {must_include_keys: [org_id, user_role], invalidate_on: [task_created, task_status_changed, schedule_changed]}
multi_tenant: {every_query_scoped_by: org_id, cache_key_includes: org_id}
```
정적/동작 검사가 이 불변식을 앱에 대해 확인 → 어느 그룹의 구현이든 채점 가능(레퍼런스 구현 불필요).

채점은 `conformance`와 `consistency`를 분리한다. 상태 전이, tenant 격리, 권한 우회 금지, 일정 충돌 금지처럼 SaaS 동작상 필수이거나 PRD/티켓에 명시된 규칙은 고정 oracle에 대한 `conformance`로 채점한다. 반면 "승인 후 핵심 필드"처럼 PRD가 일부러 열어 둔 결정에서 `[title, scope, owner]`와 `[title, scope, budget]`이 모두 합리적이면, 고정 oracle 정답 맞히기로 벌점 주지 않고 초기 구현/결정 이후 같은 정책을 후속 세션에서도 유지했는지 `self-consistency`로 채점한다. 임의 결정을 고정 oracle로 채점하려면 해당 결정이 초기 티켓이나 공개 산출물에서 한 번 관측 가능하게 seed되어야 한다.

## 9. 현실적 티켓 + 현실 QA 숨김 테스트

티켓은 이슈처럼 모호하게(좋은 예: "승인된 작업만 일정에 올릴 수 있고 충돌 금지, 대시보드 숫자도 맞아야"). 정답은 §8 oracle로 고정하되, §8의 `conformance`/`consistency` 구분을 따른다. 숨김 테스트 = 실제 QA 조합 검증(낚시 아님):
- 다른 org의 task id로 API 호출(거부?) · 승인 후 title 수정(거부?) · 일정 변경 후 대시보드 캐시 갱신? · rejected→scheduled 시도(거부?) · FE 숨김 버튼을 API 직접 호출 우회 · 오래된 import 데이터가 상태규칙 위반? · 검색 필터 변경 후 캐시 오재사용?

## 10. 분석 — 세션별 추세 + 규모 교차 + 사전등록

- **추세**(예상): S0–S3 차이 작음 → S4–S7 cache·permission·state에서 발생 → S8–S12 제품 의도 drift 확대.
- **1차 비교**: `그룹 × 세션(또는 규모)` 상호작용 — 후반으로 갈수록 **`THROUGHLINE − B-limited`**(구조화 문서 vs 손실적 머릿속 기억) 우위가 *증가*하는가. 보조: `THROUGHLINE − P`(구조 vs 노트), `B-continuing − B-limited`(long-context 천장), `B-limited − B-fresh`(손실적 기억 유무).
- 혼합효과 `지표 ~ 그룹 × 세션 + (1|앱) + (1|시드)`; cluster bootstrap. 비용은 그룹별 세션당 토큰 추세(B-continuing 증가 vs THROUGHLINE 일정)도 함께. 앱 클러스터 수가 적은 Stage 1/2에서는 p-value보다 효과크기·방향·세션별 궤적을 우선 보고한다.
- **입증**: Stage 3 이상에서 후반 세션의 THROUGHLINE이 **B-limited** 대비 (제품 일관성·cross-layer·regression·rework)에서 일관된 효과크기 우위와 통계적 지지를 보이고, 비용 회계 후 유지되며, 복수 앱에서 방향이 재현되고, 초반 null도 재현되는가. Stage 1/2에서는 이 항목을 확증이 아니라 방향적 증거로만 본다. **미주장**: **B-limited≈THROUGHLINE(손실적 머릿속 기억으로 충분)** / B-continuing≈THROUGHLINE(천장 가능성) / P≈THROUGHLINE(적어두기 일반효과로 충분) / 추세 격차 없음 / 천장 / judge 미달.

Stage 0의 해석은 별도 사전등록한다. Stage 0가 S9까지 갔더라도 차이가 작으면, 이는 전체 가설의 반증이 아니라 "겨우 발산 구간에 도달한 파일럿"으로 해석한다. 본 주장에는 S10–S12와 S12 rework를 포함한 Stage 1 이상의 후반 추세가 필요하다.

모델 선택은 "앱을 만들 수 있는 충분히 유능한 모델"을 기본으로 한다. 약한 모델로 빌드 역량 자체를 떨어뜨려 변별을 만들지 않는다. 약한 모델 조건은 보조 robustness 실험일 뿐이며, 1차 변별 레버는 모델 약화가 아니라 `B-limited`의 사전등록된 문맥 절단이다. 전 그룹이 scaffold/API/DB/FE 기본 구현에서 바닥 실패하면 메모리 효과를 해석하지 않는다.

Stage 1/2는 통계적 확증 단계가 아니다. Stage 1은 앱이 1개라 `(1|앱)` 분산을 추정할 수 없고, Stage 2도 앱 2개라 앱-수준 일반화와 group×session 상호작용 검정력이 낮다. Stage 1/2에서는 p-value나 "유의한 상호작용"을 단정하지 않고 방향, 효과크기, 세션별 궤적, 실패 유형 재현성만 보고한다. 통계적 단정은 Stage 3 이상의 다중 앱/다중 시드에서만 검토한다.

## 11. 단계적 실행 (보완 — 확장 전 변별 확인)

- **Stage -1 — 하네스 검증(에이전트 실행 전)**: reference implementation 1개와 intentionally broken implementations를 만든다. 각 oracle 불변식·검사기별 negative control이 반드시 실패하고, reference는 모든 공개/숨김 검사를 통과해야 한다. 각 불변식이 공개 표면으로 관측되는지도 확인한다. 파일시스템 격리 dry-run으로 에이전트 작업공간에서 `oracle/`, hidden tests, scoring harness, negative controls를 찾을 수 없음을 확인한다. 공유 stub/contract, interface-conformance 체크, 티켓 모호도 태그, chain-death 규칙도 이 단계에서 고정한다. 이 단계가 실패하면 Stage 0 금지.
- **Stage 0 — 마이크로 파일럿(먼저)**: 1앱·**B-limited vs THROUGHLINE**·1시드·**10세션**(S0–S9). S5에서 캐시를 "추가"하고 끝내면 붕괴가 보이지 않고, S9가 승인 후 수정 제한과 기존 일정/권한/감사/cache 결정이 처음 정면충돌하는 지점이므로 최소 S9까지 밟는다. 목표: 하네스 정합성, interface attachability, 티켓 모호도, 기능 완성도, chain-death, 비용 추세, 그리고 *B-limited에서 불변식 위반·stale·regression이 후반으로 누적되는지*를 확인하는 것이다. Stage 0는 결과가 아니라 변별 가능성/하네스 정합 점검이다. 세션당 기능 완성도 평균이 0.8 미만이거나 전 그룹이 바닥 실패하면 과제를 축소/분할한 뒤 다시 Stage 0를 수행한다. 보조로 B-continuing 1시드를 추가해 long-context 천장 여부를 본다. **천장이면 B-limited의 N/K 또는 앱 규모를 조정 후 확장**(M-pilot 교훈).
- **Stage 1 — 파일럿**: 1앱·핵심 3그룹(**B-limited/P/THROUGHLINE**)·3시드·13세션(S0–S12) = 117 runs. 진단용 **B-fresh/B-continuing**은 각 1시드만 돌려 26 runs를 추가한다. 총 143 runs. `B-limited` 민감도 N/K 보조값은 전체 세션 또는 후반 세션 subset으로 별도 보고한다.
- **Stage 2 — 확장 파일럿**: 2앱·핵심 3그룹·5시드·13세션 = 390 runs. 진단용 B-fresh/B-continuing은 앱당 각 1시드(52 runs)를 추가한다. 총 약 442 runs + 필요 시 보조 모델/민감도 subset. 앱 1–2개로는 앱-수준 일반화가 약하므로 "정식 증명"이 아니라 강한 증거로 해석한다.
- **Stage 3 — 일반화 검증(선택)**: 4–8앱·5그룹·복수 모델. 이 단계에서만 "중규모 운영 SaaS 전반"에 대한 일반화 주장을 검토한다.

## 12. 산출물 구조
아래는 논리적 산출물 구조다. 실제 에이전트 worktree에는 `public_contract/`, 현재 코드, 해당 그룹의 기억 산출물, 현재 세션 티켓만 복사하고, `harness/`, `oracle/`, `negative_controls/`, 평가 로그는 평가 전용 경로에 둔다.

```
benchmark-realapp/
  initial_prd.md
  sessions/s00.md … s12.md
  public_contract/  stubs.py  interface_conformance.py  public_api.md
  harness/  run_tests.py  score.py  product_rubric.py  contract_checks.py  cache_checks.py  app_stack/(db,cache,backend,frontend 모의 + 공유 인터페이스)
  oracle/   expected_invariants.yaml  permission_matrix.yaml  state_machine.yaml
  negative_controls/ cache_no_tenant_key/ api_permission_bypass/ invalid_state_transition/ ...
  runs/     B-fresh|B-limited|B-continuing|P|THROUGHLINE / seedN / s00 … s12
  logs/     run_log.jsonl  tool_audit.jsonl  scores.json  aggregate.md
```

## 13. 타당성·비용·한계 (정직)
- 인프로세스 모의로 브라우저·Redis 플래키 회피하되, 여전히 고비용(Stage -1 하네스 제작/검증 + Stage 1 약 143 runs + Stage 2 약 442 runs + oracle·검사기·rubric·negative control 제작). Stage -1부터 증분 구축한다.
- 가까운 MVP 산출물은 **Stage -1 + Stage 0 core 20 runs**(B-limited/THROUGHLINE × 1시드 × S0–S9)이다. 보조 B-continuing을 포함하면 10 runs가 더해진다. Stage -1은 4계층 상태형 스택, oracle, 검사기, negative controls, reference, rubric, 격리/감사 장치가 필요하므로 주 단위 엔지니어링으로 본다. Stage 1–3은 Stage 0에서 하네스가 붙고 변별 가능성이 보일 때만 진행하는 조건부 확장이다.
- **결착 vs 자유도 긴장**: 공유 인터페이스는 최소로(엔드포인트·요청 형태), 내부·정책은 자유 → 테스트 결착과 반-조작 양립. 다만 "최소 인터페이스"를 너무 많이 주면 THROUGHLINE 이점이 줄고, 너무 적게 주면 테스트가 못 붙음 — 이 경계 설정이 설계의 핵심 난점.
- **하네스가 최대 리스크**: oracle/checker 버그 하나가 전체 결과를 무효화할 수 있다. 검사기별 negative control 통과와 reference 통과가 에이전트 실행의 선행조건이다.
- rubric(judge) 신뢰도 한계 → 객관 불변식 1차, rubric 2차.
- 모의 스택은 실서비스의 단순화 — 외부 타당성은 제한(진짜 SWE 벤치 수치 아님).
- B-continuing은 LLM 문맥이 유지되는 동안 실제 대다수 개발자보다 강할 수 있다. 그래서 1차 baseline은 B-limited다. B-continuing 동률은 "문서 무용"이 아니라 long-context 천장 가능성으로 해석한다.
- B-limited의 N/K는 결과에 영향을 주는 자유 변수다. 그래서 독립 정당화, 사전등록, 민감도 보고 없이는 THROUGHLINE 우위를 주장하지 않는다.
- `THROUGHLINE − P`는 실제 개발 방식 해석에서 중요하다. P가 THROUGHLINE과 같으면 구조화 SSOT의 고유효과가 아니라 "기록/메모 일반효과"로 해석한다.
- Stage 2의 앱 2개도 일반화에는 부족하다. 결론은 "OpsBoard류 중규모 운영 SaaS에서의 증거"로 제한하고, 앱-수준 일반화는 Stage 3 또는 추가 도메인 변형 이후에만 주장한다.
- 이 벤치의 측정 대상은 **에이전트가 자가 유지하는 SSOT**다. 사람이 사양을 쓰고 검토하는 human-in-the-loop THROUGHLINE의 효과와 동일시하지 않는다.

## 14. 이중 해석 (어느 결과든 가치)
- **THROUGHLINE 우위** → "SSOT가 중규모 앱의 일관성 비용을 줄인다"의 근거.
- **THROUGHLINE 비우위** → "문서 구조만으로는 부족하고 **자동 contract/test/codegen**까지 필요하다"는 결론. (즉 THROUGHLINE 키트에 자동 계약검증·코드젠을 더해야 한다는 방향 제시.)

> 핵심 원칙: THROUGHLINE이 이기도록 만든 문제가 아니라, **문서 없이 중규모 앱을 오래 개발할 때 실제로 망가지는 지점**을 *앱의 실제 동작*으로 측정한다. 결과는 세션별 추세로 본다.
