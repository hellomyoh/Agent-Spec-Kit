# Realistic Midscale App Benchmark (OpsBoard) — B7

> 방법론: [METHODOLOGY.md](METHODOLOGY.md) · 이 문서는 [MIDSCALE_DESIGN.md](MIDSCALE_DESIGN.md)의 합성 "교차절단 계약(B4)"을 **대체**한다(B4는 좋은 설계로 자명해져 변별 실패 — M-pilot).
> 출발점: ASK가 이기게 만드는 함정이 아니라, **문서 없이 중규모 앱을 오래 개발할 때 실제로 망가지는 지점**(기억·일관성·연동 비용)을 측정한다.

## 0. 가설

> 중규모 앱을 여러 세션에 걸쳐 개발할 때, SSOT/구조화 문서 없이도 **초기 제품 의도·데이터 모델·API 계약·캐시 정책·FE/BE 연동·예외/권한/상태 전이 규칙**을 일관되게 유지할 수 있는가?

검증 명제: **세션이 길어지고 FE/BE/DB/cache 연동면이 넓어질수록, 구조화 SSOT를 유지한 그룹은 제품 일관성·cross-layer completeness·회귀·rework 비용에서 일반 개발보다 *덜 무너진다*** — 또는 못 그런다(반증). 일부 뛰어난 개발자는 머릿속으로 버티지만(강 모델), 대다수는 못 버틴다(약·중 모델/대형 코드).

## 1. 반-조작 원칙 (제1 규칙) + 감사 체크리스트

ASK를 위해 규칙을 발명하지 않는다. 측정하는 일관성은 **동작하는 SaaS라면 본질적으로 성립해야 하는 것**뿐이며, **앱의 실제 동작·불변식으로만 채점**한다(문서 갱신 여부 채점 금지). 감사:
- [ ] 모든 숨김 테스트는 *실제 QA가 할 법한* 동작/불변식 검증인가(낚시 함정 아님).
- [ ] 어떤 테스트도 ASK 산출물(문서)을 참조하지 않는가.
- [ ] 최소 공유 인터페이스(아래 §5)는 세 그룹에 *동일* 제공되는가.
- [ ] 티켓은 모호하되(현실), 정답은 비공개 oracle 불변식으로 고정돼 있는가.

## 2. 앱 — OpsBoard (팀 기반 작업 운영 SaaS)

도메인: 조직/팀/멤버 · 프로젝트 · 작업 요청 · 승인 워크플로우 · 일정/예약 · 댓글/알림 · 첨부 메타 · 권한 · 대시보드 · 검색/필터 · 감사 로그 · 캐시 · optimistic UI · background job. (인위적 계산기/DSL 회피.)

**초기 PRD(짧게 — 실제 제품팀처럼 의도만):**
- 팀은 여러 프로젝트를 가진다. 프로젝트엔 작업 요청이 있다.
- 작업 요청 상태: `draft → submitted → approved/rejected → scheduled → completed`.
- 승인자 = 팀 관리자 또는 프로젝트 소유자. **승인 후 핵심 필드 임의 수정 불가.**
- 일정 충돌 금지. 목록 화면은 빠르게. **권한 없는 사용자는 존재 여부도 알 수 없어야.** 변경 이력은 추적 가능해야.
- (세부 구현은 주지 않는다 — 구현하며 구체화.)

## 3. 비교군 (토큰 예산 통제가 핵심)

| 그룹 | 인계 | 현실 대응 |
|---|---|---|
| **B** | 코드+테스트만(세션마다 fresh, 기획 의도 문서 없음) | 아무것도 안 적음 — 기획이 머릿속에만 |
| **P** | 코드 + 자유 노트(TODO) | 계획·메모는 하나 비구조 |
| **ASK** | 코드 + SSOT 7종 | 계약을 적어두는 팀 |

ASK SSOT: `PRODUCT.md`(의도·흐름) · `DATA_MODEL.md`(스키마·관계·상태전이) · `API_CONTRACTS.md`(FE/BE 계약) · `CACHE_POLICY.md`(키·TTL·무효화) · `ARCHITECTURE.md`(FE/BE/cache/db 책임경계) · `DECISIONS.md`(유지해야 할 결정) · `PROGRESS.md`.

**통제(중요):** ASK만 정보 과다 금지. **P도 비슷한 토큰 예산**으로 노트 작성 가능. 차이는 *정보량*이 아니라 **구조화된 일관성 관리**. (토큰·문서 분량 기록·보고.)

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
| 12 | 회귀 수정/완성도 (QA가 찾은 버그 묶음) | rework |

S9–S11은 **초기 결정·캐시 키·권한이 누적 상호작용**하는 지점 — 현실의 붕괴가 일어나는 곳(발명한 함정 아님).

## 5. 트랙터블 구현 (보완 — 외부 서비스 없이 결정적)

진짜 브라우저/Redis/DB/E2E는 고비용·플래키. 네 계층을 **인프로세스 순수 파이썬 모듈**로 모의:
- `db`: SCHEMA 선언형 인메모리 저장소(미선언 컬럼/타입 위반 = 에러).
- `cache`: TTL dict + get/set/invalidate(키 관례, 무효화 누락 시 stale).
- `backend`: `handle(request)->response` 디스패처(엔드포인트→핸들러; db·cache 사용).
- `frontend`: `render(view, backend)->dict`(엔드포인트 호출, 특정 응답 필드 소비).
- optimistic UI/background job = **결정적 훅**(즉시 실행 큐)으로 모의.

**최소 공유 인터페이스(반-조작·결착 동시 해결):** 엔드포인트 이름·요청 형태와 `render(view,...)` 진입점은 **세 그룹에 동일 제공**(현실의 API 합의). 하네스 테스트는 이 공유 표면을 통해 *동작*을 검증. ASK의 차별점은 그 위의 **깊은 정책**(데이터모델·캐시 무효화·상태기계·권한·tenant)이며, 이는 공유 표면이 강제하지 않는다.

## 6. 측정 지표 (객관 우선)

| 분류 | 지표 |
|---|---|
| **객관(1차)** | Functional correctness, **Schema/API/FE 일치**(필드 불일치 수), **Cache correctness**(stale·키 오류·무효화 누락), **Permission consistency**(FE 숨김 but API 접근 가능), **State-machine integrity**(불가능 전이 허용), **Multi-tenant isolation**(org 누출), **Cross-layer completeness**(일부 계층만 구현된 기능 수), **Regression rate**(이전 세션 기능 깨짐), **Rework cost**(버그수정 토큰·변경라인), **Implementation drift**(의존 사이클·경계 위반·명명 발산 등 구조 괴리), Operational readiness(migration·seed·config·logging 누락) |
| **정성(2차)** | Product consistency rubric(초기 PRD 규칙 위반·UX 산만·동일 개념의 화면별 불일치), UX completeness(loading/error/empty/disabled 누락) |

**헤드라인 = 세션 수에 따른 (불변식 위반·cross-layer completeness·regression·rework)의 *추세*.**

## 7. 3층 채점 (judge 신뢰도 보정)

1. **자동 테스트(1차)**: unit·integration·API contract·E2E(인프로세스)·migration·cache invalidation·permission matrix.
2. **정적/구조 검사(1차)**: API 응답↔FE 소비 필드, model↔migration, 캐시 키에 tenant/org 포함, 권한 체크가 service boundary에 있는지, 상태 전이가 단일 경로인지.
3. **제품 일관성 rubric(2차)**: 초기 PRD 핵심 규칙 위반, UX 흐름 산만, 개념 표현 불일치. → **judge는 cross-family 3인·위치교차·IRR(κ) 보고, κ<0.40 비공개.** 가능한 항목은 ①②의 객관 불변식으로 변환해 rubric 의존 최소화.

> 자동 테스트만으론 "원래 만들려던 제품에서 멀어졌다"를 못 잡으므로 rubric이 필요하나, 신뢰도 한계상 **보조**로만.

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

## 9. 현실적 티켓 + 현실 QA 숨김 테스트

티켓은 이슈처럼 모호하게(좋은 예: "승인된 작업만 일정에 올릴 수 있고 충돌 금지, 대시보드 숫자도 맞아야"). 정답은 §8 oracle로 고정. 숨김 테스트 = 실제 QA 조합 검증(낚시 아님):
- 다른 org의 task id로 API 호출(거부?) · 승인 후 title 수정(거부?) · 일정 변경 후 대시보드 캐시 갱신? · rejected→scheduled 시도(거부?) · FE 숨김 버튼을 API 직접 호출 우회 · 오래된 import 데이터가 상태규칙 위반? · 검색 필터 변경 후 캐시 오재사용?

## 10. 분석 — 세션별 추세 + 규모 교차 + 사전등록

- **추세**(예상): S0–S3 차이 작음 → S4–S7 cache·permission·state에서 발생 → S8–S12 제품 의도 drift 확대.
- **1차 비교**: `그룹 × 세션(또는 규모)` 상호작용 — 후반으로 갈수록 ASK의 (불변식 위반↓·regression↓·rework↓) 우위가 *증가*하는가. + 동일 시점 `ASK − max(B, P)`.
- 혼합효과 `지표 ~ 그룹 × 세션 + (1|앱) + (1|시드)`; cluster bootstrap.
- **입증**: 후반 세션에서 ASK가 P 대비 (제품 일관성·cross-layer·regression·rework)에서 유의, 토큰 통제 후 유지, ≥앱 다수, 초반 null 재현. **미주장**: P≈ASK(적어두기 일반효과로 충분) / 추세 격차 없음 / 천장 / judge 미달.

## 11. 단계적 실행 (보완 — 확장 전 변별 확인)

- **Stage 0 — 마이크로 파일럿(먼저)**: 1앱·**B vs ASK**·1시드·**6세션**(S0–S5). 목표: *무-SSOT(B)에서 불변식 위반·stale·regression이 실제로 누적되는지*(천장 점검) + 인프로세스 스택·oracle·검사기 검증. **천장이면 설계 수정 후 확장**(M-pilot 교훈).
- **Stage 1 — 파일럿**: 1앱·B/P/ASK·3시드·12세션 = 108 runs.
- **Stage 2 — 정식**: 2앱·B/P/ASK·5시드·12세션 = 360 runs + 강·약 모델 교차.

## 12. 산출물 구조
```
benchmark-realapp/
  initial_prd.md
  sessions/s00.md … s12.md
  harness/  run_tests.py  score.py  product_rubric.py  contract_checks.py  cache_checks.py  app_stack/(db,cache,backend,frontend 모의 + 공유 인터페이스)
  oracle/   expected_invariants.yaml  permission_matrix.yaml  state_machine.yaml
  runs/     B|P|ASK / seedN / s00 … s12
  logs/     run_log.jsonl  scores.json  aggregate.md
```

## 13. 타당성·비용·한계 (정직)
- 인프로세스 모의로 브라우저·Redis 플래키 회피하되, 여전히 고비용(108→360 runs + oracle·검사기·rubric 제작). Stage 0부터.
- **결착 vs 자유도 긴장**: 공유 인터페이스는 최소로(엔드포인트·요청 형태), 내부·정책은 자유 → 테스트 결착과 반-조작 양립. 다만 "최소 인터페이스"를 너무 많이 주면 ASK 이점이 줄고, 너무 적게 주면 테스트가 못 붙음 — 이 경계 설정이 설계의 핵심 난점.
- rubric(judge) 신뢰도 한계 → 객관 불변식 1차, rubric 2차.
- 모의 스택은 실서비스의 단순화 — 외부 타당성은 제한(진짜 SWE 벤치 수치 아님).

## 14. 이중 해석 (어느 결과든 가치)
- **ASK 우위** → "SSOT가 중규모 앱의 일관성 비용을 줄인다"의 근거.
- **ASK 비우위** → "문서 구조만으로는 부족하고 **자동 contract/test/codegen**까지 필요하다"는 결론. (즉 ASK 키트에 자동 계약검증·코드젠을 더해야 한다는 방향 제시.)

> 핵심 원칙: ASK가 이기도록 만든 문제가 아니라, **문서 없이 중규모 앱을 오래 개발할 때 실제로 망가지는 지점**을 *앱의 실제 동작*으로 측정한다. 결과는 세션별 추세로 본다.
