# THROUGHLINE 프롬프트 구조 검토 및 중급 이상 벤치마크 제안

작성일: 2026-06-28

검토 대상:

- `ko/THROUGHLINE/KICKOFF.md`
- `ko/THROUGHLINE/DEVELOPINIT.md`
- `ko/THROUGHLINE/ADOPT.md`
- `ko/THROUGHLINE/AUDIT.md`
- `README.ko.md`의 기능 추가 검토 프롬프트 3종
- 기존 벤치마크 문서 `benchmark/RESULTS_SUMMARY.md`, `benchmark-realapp/REPORT_STAGE0.md`

## 1. 요약

현재 THROUGHLINE 프롬프트는 "문서화된 단일 출처(SSOT)를 유지해 장기 개발 중 목표·계약·결정의 표류를 줄인다"는 방향은 잘 잡고 있다. 특히 `ARCHITECTURE.md`, `PLAN.md`, `PROGRESS.md`를 항상 로드하고, feature/ADR/QA/NOTES/SOURCES를 선택 로드하도록 나눈 구조는 타당하다.

그러나 실제 코딩 에이전트에서 의도와 다르게 동작할 여지는 있다. 가장 큰 위험은 다음 네 가지다.

1. **문서 운영 절차가 너무 많아 에이전트가 절차 준수에 토큰을 쓰고 코딩 품질은 오히려 흔들릴 수 있다.**
2. **Multi-Agent/team 모드는 실제 독립 검토가 아니라 단일 모델의 역할극으로 축소될 수 있다.**
3. **항상 로드 문서와 선택 로드 문서의 경계가 현실에서는 흐려져, 중요한 결정 누락 또는 과도한 로딩이 발생할 수 있다.**
4. **SOURCES, feature, ARCHITECTURE, ADR, PLAN, PROGRESS 사이 권위 체계가 복잡해 충돌 시 에이전트가 임의 정당화하거나 멈출 가능성이 있다.**

따라서 THROUGHLINE의 효과를 증명하려면 단발 구현 벤치가 아니라, **중급 이상 규모의 다세션·다모듈·장기 목표 유지 벤치마크**가 필요하다. 기존 `benchmark-realapp` Stage 0는 이 방향을 잡았지만, 코드가 작고 B-limited 노트가 전체 요약처럼 작동해 변별에 실패했다.

## 2. Solo 에디션 / Team 프롬프트 해석

저장소에는 파일명상 `Solo`, `Team`이 직접 분리되어 있지는 않다. 실제 구조상 다음처럼 볼 수 있다.

| 구분 | 해당 프롬프트/흐름 | 의미 |
|---|---|---|
| Solo 에디션 | `DEVELOPINIT.md` 기본 개발 절차 | 단일 코딩 에이전트가 항상 로드 문서와 선택 로드 문서를 읽고 구현·테스트·문서 갱신까지 수행 |
| THROUGHLINE Team | `KICKOFF.md`의 Multi-Agent 기능명세 작성, `DEVELOPINIT.md` 6절, `README.ko.md` 5.3의 방식 1/2/3 | 여러 페르소나 또는 실제 서브에이전트를 통해 설계 검토를 수행하고 feature/ADR에 반영 |

중요한 차이는 "코딩을 누가 하느냐"보다 **검토와 의사결정이 단일 관점인지, 복수 관점인지**다.

## 3. 구조적 설계 결함 및 오작동 가능성

### 3.1 공통 문제: 프롬프트는 강제가 아니라 권고다

`README.ko.md`도 "프롬프트는 강제가 아니라서 검토를 건너뛸 수 있다"고 인정한다. 이 말은 THROUGHLINE 전체에도 적용된다. 에이전트가 다음을 생략할 수 있다.

- `ARCHITECTURE.md`와 feature 문서 실제 확인
- `SOURCES/INDEX.md`의 미반영 변경요청 확인
- 테스트 실제 실행
- HISTORY/PROGRESS/ASSUMPTIONS 갱신
- Multi-Agent 검토 로그 작성

현재는 AUDIT가 사후에 잡는 구조다. 즉 THROUGHLINE은 **예방 장치**라기보다 **절차 준수를 유도하고 사후 감사로 회수하는 장치**에 가깝다. 벤치마크에서는 "프롬프트를 읽었다"가 아니라 실제 산출물과 코드가 규칙을 지켰는지 채점해야 한다.

### 3.2 Solo 모드: 항상 로드 문서가 커지면 역효과 가능

`DEVELOPINIT.md`는 매 세션 `AGENTS.md`, `ARCHITECTURE.md`, `PLAN.md`, `PROGRESS.md`를 항상 읽게 한다. 초기에는 좋지만 프로젝트가 커지면 문제가 생긴다.

- `ARCHITECTURE.md`가 계약 선언뿐 아니라 배경·폐기 결정·상세 설명까지 포함하면 노이즈가 된다.
- `PLAN.md`가 완료 Phase를 계속 누적하면 현재 작업과 무관한 정보가 많아진다.
- `PROGRESS.md`의 "다음 세션 첫 명령"이 낡으면 에이전트가 잘못된 작업을 시작할 수 있다.

`AUDIT.md` 3.9가 문서 비대화를 관찰하도록 한 점은 좋다. 다만 관찰만으로는 부족하다. 운영 규칙에 "항상 로드 문서 최대 크기", "계약/배경/이력 분리", "완료 Phase 아카이브 기준"을 더 명확히 둘 필요가 있다.

### 3.3 Solo 모드: 권위 체계가 복잡하다

THROUGHLINE은 여러 문서의 역할을 구분한다.

- 현재 의도: `ARCHITECTURE.md`, `features/*.md`, `PLAN.md`
- 입력 근거: `SOURCES/`
- 결정 이력: `adr/`
- 진행 상태: `PROGRESS.md`
- 코드 작업 이력: `HISTORY.md`
- 가정: `ASSUMPTIONS.md`
- 확인된 사실: `NOTES.md`
- 백로그: `TODO.md`

이 구조는 잘 쓰면 강력하지만, 에이전트 입장에서는 충돌 가능성이 많다. 예를 들어 `SOURCES/` 변경요청이 "검토 중"인데 feature 문서에는 반영되지 않았고, 사용자가 채팅에서 "그거 해줘"라고 말하면 어느 쪽을 권위로 볼지 흔들릴 수 있다.

현재 `DEVELOPINIT.md`는 "반영 완료 전 요청 문서는 권위가 없다"고 명시하지만, 실제 코딩 세션에서는 사용자의 최신 채팅 지시가 이 규칙을 덮어쓸 수 있다. 이 경우를 위한 명시 규칙이 필요하다.

권장 보완:

- 사용자의 채팅 지시가 `SOURCES/` 절차와 충돌할 때의 우선순위 정의
- "긴급 패치" 예외 절차 정의
- `SOURCES/INDEX.md` 상태 전이 검증 스크립트 제공

### 3.4 Solo 모드: 문서 갱신이 코드 품질을 방해할 수 있다

`DEVELOPINIT.md`는 구현, 테스트, README, PLAN, PROGRESS, HISTORY, NOTES, ASSUMPTIONS, 인덱스, SOURCES 상태, TODO 상태, Git commit/push까지 한 세션에 요구한다. 이는 실제 에이전트에 큰 부담이다.

오작동 양상:

- 코드 수정은 작지만 문서 갱신이 과도해 토큰 비용 증가
- 테스트 실패 원인 분석보다 문서 형식 맞추기에 집중
- 문서 갱신 누락을 피하려고 실제로 확인하지 않은 내용을 기록
- commit/push를 자동으로 하라는 규칙이 현재 도구 환경이나 사용자 의도와 충돌

특히 "의미 있는 작업 단위가 끝나면 사용자에게 묻지 않고 commit/push"는 모든 사용 환경에 맞지 않는다. Codex/CI/사내 repo에서는 push 권한, 브랜치 정책, PR 정책이 다양하다. 기본값은 commit까지만, push는 사용자 또는 환경 설정에 따르는 편이 안전하다.

### 3.5 Team 모드: 역할극과 실제 독립 검토가 섞인다

`README.ko.md` 5.3은 방식 1을 "표준 검토(역할극)", 방식 2를 "실제 서브에이전트 병렬 토론"으로 나눈다. 이 구분은 좋다. 하지만 실무에서는 다음 문제가 생긴다.

- 서브에이전트 도구가 없는 환경에서 방식 2를 지시하면 에이전트가 역할극으로 대체할 수 있다.
- "서로의 출력을 보지 않은 상태"를 실제로 보장하기 어렵다.
- Research Agent가 실제 검색을 해야 하는지, 로컬 문서만 읽으면 되는지 기준이 부족하다.
- review 로그가 실제 검토가 아니라 그럴듯한 사후 합성물이 될 수 있다.

`AUDIT.md` 3.10이 출처와 연극성 로그를 표본 점검하게 한 것은 좋은 안전장치다. 다만 벤치마크에서는 로그가 아니라 **검토 결과가 숨겨진 결함을 실제로 줄였는지**를 봐야 한다.

### 3.6 Team 모드: 다수 페르소나가 합의 편향을 만들 수 있다

Multi-Agent 검토는 위험을 넓게 보는 장점이 있지만, 다음 편향도 만든다.

- 초기 잘못된 해석이 모든 페르소나의 전제가 됨
- 에이전트가 충돌을 실제로 유지하지 않고 "합의안"으로 부드럽게 봉합
- 보안/DB/QA 페르소나가 일반론만 반복하고 프로젝트 특화 근거를 제시하지 않음
- feature 문서가 안전한 표현으로 길어지지만 테스트 가능한 계약은 약함

따라서 Team 모드는 "페르소나 수"가 아니라 다음을 강제해야 한다.

- 각 페르소나는 최소 1개 이상의 **검증 가능한 실패 모드**를 제시
- QA/Security/DB 관점은 가능하면 테스트나 체크리스트 항목으로 환원
- 합의 불가 쟁점은 feature 문서에 숨기지 말고 ADR 또는 사용자 확인 항목으로 분리

### 3.7 ADOPT 모드: 코드 정독 요구가 현실적으로 과대할 수 있다

`ADOPT.md`는 "코드를 실제로 읽고, 읽은 범위와 읽지 못한 범위를 명시"하라고 한다. 원칙은 좋지만 중급 이상 코드베이스에서는 한 세션에 불가능하다.

오작동 양상:

- 에이전트가 파일명/폴더 구조만 보고 as-built 명세를 추정
- 읽은 범위가 과장됨
- 근거 코드 위치가 없는 기능 설명 생성
- 기존 README/AGENTS/CLAUDE 병합 중 사용자 규칙 손상

권장 보완:

- ADOPT를 "1회 완료"가 아니라 "coverage-driven adoption"으로 나누기
- 파일/기능별 `read_coverage` 표를 두고 직접 읽은 파일만 체크
- as-built 명세의 각 동작 주장에 코드 위치 또는 테스트 근거 필수화

### 3.8 AUDIT 모드: 표류 발견 후 처리 연결이 약하다

`AUDIT.md`는 의미적 표류를 수정하지 않고 기록만 하도록 한다. 이는 안전하지만, 후속 처리로 연결되지 않으면 발견 목록이 누적될 수 있다.

권장 보완:

- AUDIT 결과를 `PLAN.md` 또는 `TODO.md`로 자동 라우팅하는 규칙 강화
- 발견 유형별 심각도(`blocker`, `major`, `minor`) 추가
- 다음 개발 세션에서 반드시 처리할 "audit follow-up queue" 추가

## 4. 현재 벤치마크 결과와 프롬프트 결함의 연결

기존 결과는 프롬프트 구조의 장단점을 잘 보여준다.

- B1/B2에서는 THROUGHLINE이 추가 비용만 만들고 우위가 불명확했다. 이는 절차 오버헤드가 작은 과제에서 손해가 될 수 있다는 신호다.
- B3에서는 기록이 없으면 과거 결정을 복원하지 못했다. 이는 `DECISIONS`/`HISTORY`류 산출물이 필요한 좁은 조건을 보여준다.
- `benchmark-realapp` Stage 0에서는 B-limited도 전부 통과했다. 이는 코드가 작고 현재 코드 재독해가 충분하면 THROUGHLINE의 SSOT가 필요 없다는 뜻이다.
- Stage 0의 THROUGHLINE 실패는 S4 `slot` 타입 버그 하나가 누적된 것이다. 이는 문서 구조가 있어도 일반 코딩 실수는 막지 못하고, 오히려 세션 후반에 해당 영역을 건드리지 않으면 버그가 오래 남을 수 있음을 보여준다.

결론: THROUGHLINE의 가설을 증명하려면 "기능 하나 잘 만들기"가 아니라 **장기 목표 유지, 과거 결정 보존, 교차모듈 계약 준수, 대화/세션 누적으로 인한 drift 억제**를 직접 측정해야 한다.

## 5. 타 논문·벤치마크 사례

### 5.1 SWE-bench / SWE-bench Verified

SWE-bench는 실제 GitHub issue와 PR에서 추출한 문제를 주고, 모델이 패치를 만들어 테스트를 통과하는지 평가한다. 원 논문은 12개 Python 저장소의 실제 issue/PR 기반 2,294개 문제를 제시한다. SWE-bench Verified는 그중 사람이 검증한 500개 subset으로 신뢰도를 높였다.

참고:

- [SWE-bench GitHub](https://github.com/swe-bench/SWE-bench)
- [SWE-bench paper](https://arxiv.org/abs/2310.06770)
- [SWE-bench Verified](https://www.swebench.com/verified.html)
- [OpenAI: Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)

THROUGHLINE 벤치마크에 적용할 점:

- 실제 repo/issue/patch/test 기반으로 외부 타당성을 높인다.
- human validation 또는 negative control로 테스트 품질을 검증한다.
- 단일 점수가 아니라 patch correctness, regression, cost를 함께 본다.

한계:

- 대부분 단일 issue 해결이다. THROUGHLINE이 주장하는 "긴 대화·다세션 표류 억제"는 직접 측정하지 않는다.

### 5.2 RepoBench / RepoCoder 계열

RepoBench는 단일 파일이 아니라 repository-level code completion을 평가한다. retrieval, completion, pipeline을 나누어 cross-file context 사용 능력을 본다.

참고:

- [RepoBench arXiv](https://arxiv.org/abs/2306.03091)
- [RepoBench ICLR paper PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/d191ba4c8923ed8fd8935b7c98658b5f-Paper-Conference.pdf)
- [RepoCoder OpenReview](https://openreview.net/forum?id=q09vTY1Cqh)

THROUGHLINE 벤치마크에 적용할 점:

- "필요한 정보가 다른 파일에 흩어져 있음"을 과제로 만든다.
- 검색/선택/코딩을 분리 측정한다.
- `ARCHITECTURE.md`와 `PROGRESS.md`가 orientation cost와 context retrieval을 줄이는지 측정할 수 있다.

### 5.3 LongCodeBench / LoCoBench

LongCodeBench는 실제 GitHub 기반의 긴 컨텍스트 coding task를 구성해 최대 1M 토큰 맥락에서 code comprehension/repair 성능을 평가한다. LoCoBench도 10K~1M 토큰 범위를 두고 long-context 성능 저하를 측정하는 방향이다.

참고:

- [LongCodeBench arXiv HTML](https://arxiv.org/html/2505.07897v2)
- [LongCodeBench dataset](https://huggingface.co/datasets/Steefano/LCB)
- [LoCoBench arXiv HTML](https://arxiv.org/html/2509.09614v1)

THROUGHLINE 벤치마크에 적용할 점:

- 코드베이스 크기를 단계적으로 키워 "전체 재독해가 가능한 구간"과 "불가능한 구간"을 분리한다.
- 컨텍스트 길이가 길어질수록 성능이 떨어지는지, THROUGHLINE 문서가 이를 완화하는지 본다.
- 단순 long-context 투입과 구조화 SSOT 투입을 비교한다.

### 5.4 Lost in the Middle / long-context instruction following

Lost in the Middle는 긴 컨텍스트에서 관련 정보의 위치에 따라 모델 성능이 크게 달라질 수 있음을 보였다. long-context instruction-following 연구들은 긴 입력이 오히려 지시 준수와 제약 유지에 악영향을 줄 수 있음을 평가한다.

참고:

- [Lost in the Middle arXiv](https://arxiv.org/abs/2307.03172)
- [Lost in the Middle TACL](https://aclanthology.org/2024.tacl-1.9/)
- [EvolIF: multi-turn instruction following](https://arxiv.org/html/2511.03508v1)
- [Improving Long Context Instruction Following](https://aclanthology.org/2026.findings-eacl.254.pdf)

THROUGHLINE 벤치마크에 적용할 점:

- 초기 목표/결정/금지사항을 대화 중간에 묻히게 하고 후반 작업에서 지켜지는지 본다.
- 관련 정보 위치를 조작한다: 초반, 중간, 최근, SSOT 요약.
- "대화가 길어질수록 처음 목표에서 벗어나는 현상"을 직접 측정한다.

### 5.5 ChatDev / MetaGPT / AgentCoder

ChatDev는 여러 전문 에이전트가 설계·코딩·테스트 단계에서 소통하는 개발 프레임워크다. MetaGPT는 SOP와 구조화된 산출물을 multi-agent workflow에 넣어 일관성과 중간 산출물 검증을 강화한다. AgentCoder는 programmer, test designer, test executor를 분리해 테스트 기반 반복 개선을 한다.

참고:

- [ChatDev arXiv](https://arxiv.org/abs/2307.07924)
- [ChatDev ACL](https://aclanthology.org/2024.acl-long.810/)
- [MetaGPT arXiv](https://arxiv.org/abs/2308.00352)
- [MetaGPT ICLR PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/6507b115562bb0a305f1958ccc87355a-Paper-Conference.pdf)
- [AgentCoder arXiv HTML](https://arxiv.org/html/2312.13010v3)

THROUGHLINE 벤치마크에 적용할 점:

- Team 모드는 "에이전트 수"가 아니라 역할별 산출물과 검증 루프의 품질을 측정해야 한다.
- QA/Test 역할이 실제 hidden failure를 줄이는지 별도 ablation이 필요하다.
- SOP/문서화가 cascade hallucination을 줄이는지, 아니면 형식적 로그만 늘리는지 봐야 한다.

## 6. THROUGHLINE 가설을 증명하기 위한 벤치마크 제안

검증할 전제:

> THROUGHLINE은 중급 이상 코딩 규모에서 코딩 에이전트의 코딩 일관성을 높이고, 대화·세션이 길어질수록 처음 목표에서 벗어나는 현상을 제어한다.

이 전제는 다음 세 하위 가설로 나눠야 한다.

1. **목표 유지 가설**: 초기 PRD/제품 목표가 후반 기능에서도 보존된다.
2. **계약 유지 가설**: 데이터 모델, API, 권한, 캐시, 상태 전이 같은 횡단 계약이 후반 변경에서도 깨지지 않는다.
3. **비용-규모 전환 가설**: 소규모에서는 THROUGHLINE이 비용만 늘리지만, 일정 규모 이상에서는 회귀 감소·재탐색 비용 감소가 문서 유지 비용을 상쇄한다.

### 6.1 벤치마크 이름: THROUGHLINE-DriftBench

목표: 다세션 repo-level development에서 구조화 문서가 drift와 regression을 줄이는지 측정한다.

단위 과제:

- 1개 과제 = 하나의 중급 앱 또는 라이브러리
- 12~16개 세션
- 각 세션은 새 에이전트로 시작
- 이전 세션 코드와 그룹별 memory artifact만 전달
- hidden tests는 매 세션 누적 실행

### 6.2 비교군

| 그룹 | 제공 정보 | 목적 |
|---|---|---|
| B-code | 현재 코드 + 현재 ticket만 | 코드 재독해만으로 충분한지 |
| B-limited | 현재 코드 + 최근 N세션 짧은 notes, K-token cap | 손실적 사람 기억 근사 |
| P-notes | 현재 코드 + 자유형 notes, THROUGHLINE과 유사 토큰 budget | "기록 일반효과" 통제 |
| throughline-solo | 현재 코드 + THROUGHLINE SSOT 문서 + 단일 에이전트 | 구조화 SSOT 효과 |
| throughline-team | throughline-solo + 실제 서브에이전트 검토/QA 역할 | team 검토 추가 효과 |
| B-full-context | 전체 이전 대화 concat | long-context ceiling 진단 |

핵심 비교:

- `throughline-solo − max(B-limited, P-notes)`
- `throughline-team − throughline-solo`
- `throughline-solo − B-full-context`는 비용/압축 관점의 보조 비교

### 6.3 과제 설계

과제는 최소 4개 앱/라이브러리로 구성한다.

1. OpsBoard류 운영 SaaS: 권한, 상태 전이, 캐시, 감사 로그, 검색, UI render 계약
2. Billing/Subscription 서비스: plan, invoice, proration, refund, tax, idempotency
3. Workflow engine: DAG, retry, schedule, event log, permission, migration
4. Repository-level library: parser/evaluator/formatter/typechecker 같은 cross-file visitor 계약

각 과제는 S/M/L 세 크기로 만든다.

| 크기 | 대략 규모 | 목적 |
|---|---:|---|
| S | 300~700 LOC, 4~6 모듈, 6~8 세션 | 소규모 null 재현 |
| M | 1,500~3,000 LOC, 8~12 모듈, 12세션 | THROUGHLINE 목표 영역 |
| L | 5,000+ LOC, 15+ 모듈, 16세션 | 전체 재독해 불가능 영역 |

### 6.4 Drift를 유발하는 세션 구조

각 과제는 다음 패턴을 포함한다.

1. S0: 초기 목표/제품 원칙/핵심 금지사항 도입
2. S1~S4: 기본 기능 구축
3. S5~S8: 횡단 관심사 추가, 예: 권한, 캐시, 감사, 검색
4. S9~S12: 초기 결정과 충돌하기 쉬운 요구 추가
5. S13~S16: 과거 결정으로 rollback 또는 policy restoration 수행

중요한 규칙:

- 모든 scored invariant는 처음 등장할 때 한 번만 명시한다.
- 후반 티켓에서는 해당 규칙을 다시 말하지 않는다.
- 하지만 hidden test는 계속 누적한다.
- B-limited notes에는 K-token cap을 둬 rolling full summary를 막는다.
- S0 front-loading을 막기 위해 "이번 세션 기능만 구현"을 공개 규칙과 채점 규칙으로 둔다.

### 6.5 측정 지표

1차 지표:

- **Goal drift violations**: 초기 PRD 목표와 모순되는 후반 구현 수
- **Invariant violations**: 상태 전이, 권한, tenant, cache, schema, API 계약 위반
- **Regression rate**: 이전 세션에서 통과한 hidden/public behavior가 후반에 깨지는 비율
- **Cross-layer completeness**: FE/API/DB/cache/render 경로가 끝까지 일관되는지
- **Decision restoration fidelity**: 과거 정책으로 되돌릴 때 정확히 복원하는지

2차 지표:

- 첫 편집 전 orientation token/tool cost
- 전체 token/cost
- touched files/churn
- 테스트 추가율
- 문서-코드 불일치율
- AUDIT에서 발견된 semantic drift 수

THROUGHLINE이 이겼다고 주장하려면:

- M/L 규모에서 `throughline-solo`가 `P-notes`보다 regression 또는 invariant violation을 유의하게 줄여야 한다.
- `throughline-team`은 `throughline-solo`보다 설계 결함 또는 hidden failure를 줄여야 한다.
- 비용 증가를 품질 개선 또는 orientation cost 감소가 일부라도 상쇄해야 한다.
- S 규모에서는 null 또는 비용 손해가 재현돼야 한다. 그래야 "규모 임계점" 주장이 가능하다.

### 6.6 통계 설계

- 최소: 앱 4개 × 크기 3개 × 그룹 5개 × seed 3개
- 권장: 앱 6~8개 × seed 5개
- 분석: mixed-effects 또는 cluster bootstrap

모형 예:

```text
metric ~ group * size * session + (1 | app) + (1 | seed)
```

사전등록 1차 비교:

```text
M/L 후반 세션에서
throughline-solo < max(B-limited, P-notes) 의 invariant violation / regression
throughline-team < throughline-solo 의 design-review-related hidden failures
```

해석 기준:

- `P-notes ≈ throughline-solo`이면 구조 효과가 아니라 기록 일반효과다.
- `B-full-context ≈ throughline-solo`이면 long-context ceiling일 수 있다.
- 모든 그룹이 0 regression이면 과제가 천장이다.
- 모든 그룹이 chain-dead이면 과제가 바닥이다.

### 6.7 하네스 요구사항

SWE-bench와 SWE-bench Verified의 교훈을 적용해 다음을 둔다.

- reference implementation
- hidden tests
- negative controls
- human review 또는 독립 모델 review
- agent workspace와 evaluator workspace 물리 분리
- out-of-workspace read audit
- 테스트 실패 메시지에서 oracle 누수 방지

RepoBench/LongCodeBench의 교훈을 적용해 다음도 둔다.

- cross-file context가 필요한 과제
- repo 크기별 scale curve
- 관련 정보 위치 조작: 초반/중간/최근/SSOT
- 전체 repo 재독해 비용 측정

### 6.8 THROUGHLINE Team 전용 평가

Team 모드의 효과는 별도로 ablation해야 한다.

비교:

- `throughline-solo`: SSOT만 사용
- `throughline-team-roleplay`: 단일 에이전트가 페르소나 역할극
- `throughline-team-parallel`: 실제 서브에이전트 독립 검토
- `throughline-team+QA`: QA/Test 에이전트가 hidden과 독립적인 public tests를 작성

Team 효과 지표:

- 설계 전 발견된 risk 중 실제 hidden failure와 연결된 비율
- team 검토 후 feature 문서에 추가된 테스트 가능 계약 수
- 후속 regression 감소량
- false-positive 설계 복잡도 증가량

중요: review 로그 자체를 점수화하지 않는다. 로그는 감사 자료이고, 점수는 코드 동작과 테스트로 준다.

## 7. 실행 우선순위

1. 현재 `benchmark-realapp`을 Stage 1로 확장한다.
   - S0 front-loading 금지
   - B-limited notes K-token cap
   - `render()` output contract 고정
   - seed 3개 이상
   - P-notes 그룹 추가
2. OpsBoard 외 앱 1개를 추가한다.
   - Billing 또는 Workflow engine 권장
3. M 규모에서 변별이 생기는지 먼저 확인한다.
4. 변별이 생기면 L 규모와 throughline-team ablation으로 확장한다.
5. 변별이 계속 없으면 "THROUGHLINE-as-agent-memory의 효과는 약하다"는 결론을 받아들인다.

## 8. 최종 권고

프롬프트 자체는 방향이 좋지만, 지금 형태만으로는 "중급 이상에서 drift를 제어한다"는 전제를 증명하지 못한다. 증명하려면 프롬프트 평가가 아니라 **장기 다세션 코드 진화 평가**가 필요하다.

프롬프트 개선 측면에서는 다음을 먼저 반영하는 것이 좋다.

1. 항상 로드 문서 크기와 회전 기준을 명시한다.
2. Bounded memory 조건에서도 살아남는 핵심 결정만 `ARCHITECTURE/ADR/PROGRESS`에 남기도록 문서 역할을 더 압축한다.
3. Team 모드는 역할극/실제 서브에이전트/QA 포함을 명확히 분리한다.
4. review 로그보다 테스트 가능한 계약과 hidden regression 감소를 중시한다.
5. commit/push 자동 규칙은 환경별로 완화한다.

벤치마크 측면에서는 기존 `benchmark-realapp`의 Stage 0를 폐기할 필요는 없다. 오히려 좋은 파일럿이다. 다만 Stage 0는 "천장에 걸리는 조건"을 발견한 실험이므로, Stage 1은 손실적 기억이 실제로 작동하고 전체 코드 재독해가 불리해지는 조건으로 재설계해야 한다.
