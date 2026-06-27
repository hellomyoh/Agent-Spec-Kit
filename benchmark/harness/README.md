# ASK-QBench 하네스 (B3 Revert-to-Origin)

유지보수자측 평가 도구. ASK 런타임 키트(`en/`,`ko/`)와 분리됨. 방법론: [../METHODOLOGY.md](../METHODOLOGY.md).

## 구성
- `tracks/rank/` — **B3 검증 트랙**. tie-break 정책이 변하는 라이브러리.
  - `ref_base.py`(알파벳) `ref_R1.py`(길이) `ref_R2.py`(역알파벳) — 정책별 오라클.
  - `tests.py` — `get_core()`(전 정책 불변식=P2P), `get_policy(name)`(정책별 동작).
  - `change_requests/step{0..3}.md` — 에이전트 입력. step0=Base, step1=R1, step2=R2, **step3=Revert**(R1 미서술).
- `tracks/clean_tags/` — 동일 패턴이나 **R1=알파벳정렬(모델 기본추측) → B3 변별 부적합**(참고용).
- `score.py` — 채점기. `score_revert(track_dir, solution.py, step)` → 복원 충실도/회귀/core.

## 검증 (테스트·정책 변별 확인)
```
PYTHONIOENCODING=utf-8 python score.py
# -> "ALL REFERENCES VALID & POLICIES DISCRIMINATE"
```

## B3 실행 절차 (요약)
1. **Base→R1→R2 체인 생성**: 각 그룹(L0/L1/L-ASK)이 step0→1→2를 순차 개발(이전 step 코드 + 그 그룹의 기억 인계). L-ASK는 SPEC+HISTORY(append-only)+PROGRESS 유지.
2. **격리 작업공간 구성(필수, P8)**: 각 체인의 step2 산출(현재=R2 코드 + 그 그룹 기억 파일)만 빈 디렉토리에 복사. 이전 step·change_request 접근 차단.
3. **Revert 실행**: 에이전트에게 "이 디렉토리만 사용, R2를 롤백해 R1 복구"(R1 내용 미제공). 무기억은 R1을 알 수 없어야 함.
4. **채점**: `score.get_policy("R1")` 통과율 = 복원 충실도. `get_policy("R2")` 잔존 = 미복구.

신규 실행 결과: [../results/B3_results.json](../results/B3_results.json) (L0 0/2, L1 2/2, L-ASK 2/2).

## 누수 주의 (핵심)
파일시스템을 격리하지 않으면 무기억 에이전트가 `change_requests/step1.md`(R1 사양)나 이전 단계 코드를 검색·열람해 **R1을 직접 읽어 변별이 사라진다**. 반드시 되돌리기(step3) 작업공간을 자기완결로 격리하고 외부 접근을 금지할 것(방법론 P8).
