# Solo 적합성 파일럿 (Solo 에디션 · THROUGHLINE 킷)

Solo 에디션 프롬프트가 명세대로 구동되는지 1회 확인합니다. 각 단계 실행 후 **체크 명령**을 돌려 PASS/FAIL을 기입하세요.
`<REPO>` = 이 저장소 루트.

---

## 0. 환경 준비

```bash
mkdir -p /tmp/throughline-solo && cd /tmp/throughline-solo && git init -q
git config user.email dev@example.com && git config user.name dev
cp -r "<REPO>/ko/THROUGHLINE" ./THROUGHLINE
cp "<REPO>/tests/conformance/seeds/REQUIREMENTS.md" THROUGHLINE/SOURCES/REQUIREMENTS.md
git add -A && git commit -qm "chore: seed THROUGHLINE kit + requirements"
git rev-parse HEAD > /tmp/throughline-solo-base   # 기준 커밋 기록
```

---

## 1. KICKOFF 실행

에이전트에 **루트 README의 §2 초기화 프롬프트**를 입력(REQUIREMENTS.md + KICKOFF.md 기준)해 초기화를 수행하게 합니다.

체크 (모두 MUST):

```bash
cd /tmp/throughline-solo
# C1 핵심 운영 문서 생성
for f in ARCHITECTURE.md PLAN.md PROGRESS.md HISTORY.md ASSUMPTIONS.md NOTES.md TODO.md; do
  test -f "THROUGHLINE/$f" && echo "C1 ok $f" || echo "C1 FAIL $f"
done
# C2 기능명세 + 인덱스
test -f THROUGHLINE/features/README.md && ls THROUGHLINE/features/feature-*.md >/dev/null 2>&1 && echo "C2 ok" || echo "C2 FAIL"
# C3 산출물이 THROUGHLINE/ + 루트3파일 밖으로 새지 않음
#   주의: 접두 매칭이라 `^THROUGHLINE/` 와 루트3파일을 각각 제외한다
#   (anchor를 한 alternation에 묶으면 'THROUGHLINE/' 정확일치만 돼 모든 산출물이 leak로 오판됨)
git diff --name-only "$(cat /tmp/throughline-solo-base)" HEAD \
  | grep -vE '^THROUGHLINE/' \
  | grep -vE '^(README|AGENTS|CLAUDE)\.md$' \
  | grep . && echo "C3 FAIL (위 파일이 범위 밖)" || echo "C3 ok"
# C4 REQUIREMENTS 동결 (반영 완료 / Applied)
grep -iE 'REQUIREMENTS.*(반영 완료|Applied)' THROUGHLINE/SOURCES/INDEX.md && echo "C4 ok" || echo "C4 FAIL"
# C5 PROGRESS 다음 명령
grep -iE '다음 세션 첫 명령|first command' THROUGHLINE/PROGRESS.md && echo "C5 ok" || echo "C5 FAIL"
# C6 초기화가 commit 됨
test "$(git rev-list --count HEAD)" -gt 1 && echo "C6 ok" || echo "C6 FAIL"
```

| ID | 검증 | 결과 |
|---|---|---|
| C1 | 운영 문서 7종 생성 | ☐ |
| C2 | features/README.md + feature 문서 ≥1 | ☐ |
| C3 | `THROUGHLINE/`·루트3파일 밖 산출물 없음 | ☐ |
| C4 | REQUIREMENTS 동결(반영 완료) | ☐ |
| C5 | PROGRESS "다음 세션 첫 명령" 존재 | ☐ |
| C6 | 초기화 commit 존재 | ☐ |

---

## 2. DEVELOP 실행 (기능 1개 구현)

**루트 README §5 개발 프롬프트**로 첫 Phase(예: 링크 생성 API)를 구현·테스트하게 합니다.

```bash
cd /tmp/throughline-solo
DEV=$(git rev-parse HEAD)   # 개발 작업 후의 HEAD (구현 커밋)
# C7 HISTORY 고정 접두사 항목
grep -E '^## \[[0-9]{4}-[0-9]{2}-[0-9]{2}\] (init|adopt|feat|fix|docs|test|qa|audit|chore) \|' THROUGHLINE/HISTORY.md \
  && echo "C7 ok" || echo "C7 FAIL"
# C8 원자 커밋: 한 커밋에 코드 + THROUGHLINE 문서가 함께
git show --name-only --pretty=format: "$DEV" | grep -q 'THROUGHLINE/' \
  && git show --name-only --pretty=format: "$DEV" | grep -qvE 'THROUGHLINE/|^$' \
  && echo "C8 ok" || echo "C8 FAIL (코드+문서 동시 커밋 아님)"
# C9 테스트 실제 실행 흔적 (실행 명령 + 통과/실패 기록)
grep -iE '실행 명령|(npm|pytest|go test|cargo|jest|vitest).*' THROUGHLINE/HISTORY.md \
  && echo "C9 ok(명령 기록 확인)" || echo "C9 FAIL(테스트 실행 명령 미기록)"
# C10 PROGRESS '다음 명령'이 KICKOFF 대비 갱신됨
git log -p -- THROUGHLINE/PROGRESS.md | grep -iE '^\+.*다음.*명령' \
  && echo "C10 ok" || echo "C10 FAIL"
# C11 main 직접 작업 아님
test "$(git branch --show-current)" != "main" -a "$(git branch --show-current)" != "master" \
  && echo "C11 ok ($(git branch --show-current))" || echo "C11 FAIL (main에서 작업)"
```

| ID | 검증 | 결과 |
|---|---|---|
| C7 | HISTORY 고정 접두사 항목 | ☐ |
| C8 | 원자 커밋(코드+문서 동시) | ☐ |
| C9 | 테스트 실행 명령·결과 기록 | ☐ |
| C10 | PROGRESS 다음 명령 갱신 | ☐ |
| C11 | 작업 브랜치(main 직접 아님) | ☐ |

> C9는 "명령 문자열이 기록됐는가"를 봅니다. 리뷰어가 그 명령이 실제 테스트 실행인지 1줄 확인합니다(실행 없이 "통과" 주장 = FAIL).
> **false-green 주의:** `python -m unittest`가 테스트를 못 찾으면 `Ran 0 tests ... OK`로 *통과처럼* 보입니다. 기록된 결과에 **실행 테스트 수 > 0**인지 확인하세요(0이면 미발견 — `tests/__init__.py` 등 디스커버리 문제).

---

## 3. 드리프트 주입 → AUDIT 실행

표류를 일부러 만들고 AUDIT이 잡는지 봅니다.

```bash
cd /tmp/throughline-solo
# 주입: 인덱스에 등재되지 않은 고아 feature 문서
printf '# Feature: Orphan (파일럿 주입)\n' > THROUGHLINE/features/feature-orphan.md
git add -A && git commit -qm "test: inject orphan feature (pilot)"
```

**루트 README §9.1 AUDIT 프롬프트**를 실행하게 합니다. 이후:

```bash
cd /tmp/throughline-solo
# C12 AUDIT가 audit 이력 항목을 남김
grep -E '^## \[[0-9-]+\] audit \|' THROUGHLINE/HISTORY.md && echo "C12 ok" || echo "C12 FAIL"
```

| ID | 검증 | 확인 방법 | 결과 |
|---|---|---|---|
| C12 | 주입한 고아 feature를 AUDIT이 **발견·보고** | AUDIT 출력/보고서에 `feature-orphan` 또는 "인덱스 누락/고아" 언급 (리뷰어 확인) | ☐ |
| C13 | AUDIT이 `audit` 이력 항목 기록 | 위 grep PASS | ☐ |

---

## 판정표 (Solo)

| 단계 | MUST 체크 | PASS/FAIL | FAIL 시 의심 프롬프트·절 |
|---|---|---|---|
| KICKOFF | C1~C6 | | KICKOFF |
| DEVELOP | C7~C11 | | DEVELOPINIT |
| AUDIT | C12~C13 | | AUDIT |

모든 MUST PASS → **solo 적합**. FAIL → 해당 절 결함 기록·수정 후 재실행.

```bash
rm -rf /tmp/throughline-solo   # 정리
```
