# Team 적합성 파일럿 (THROUGHLINE Team)

THROUGHLINE Team 프롬프트가 명세대로 구동되는지 1회 확인합니다. 핵심은 **충돌 검출(touches)·식별(owner==author)·고정 INDEX 부재·single-writer·INTEGRATE 이력**입니다.
`<REPO>` = 이 저장소 루트. 두 개발자(alice=maintainer, bob=contributor)를 작성자 전환으로 시뮬합니다.

---

## 0. 환경 준비 (2 identity + 레지스트리)

```bash
mkdir -p /tmp/ask-team && cd /tmp/ask-team && git init -q
git config user.email alice@example.com && git config user.name alice
cp -r "<REPO>/ko/THROUGHLINE-TEAM" ./THROUGHLINE
cp "<REPO>/tests/conformance/seeds/REQUIREMENTS.md" THROUGHLINE/SOURCES/REQUIREMENTS.md
mkdir -p THROUGHLINE/team
cat > THROUGHLINE/team/alice.md <<'EOF'
---
handle: alice
name: Alice
emails: [alice@example.com]
role: maintainer
agents: [claude-code]
active: true
joined: 2026-06-21
---
EOF
cat > THROUGHLINE/team/bob.md <<'EOF'
---
handle: bob
name: Bob
emails: [bob@example.com]
role: contributor
agents: [claude-code]
active: true
joined: 2026-06-21
---
EOF
git add -A && git commit -qm "chore: seed THROUGHLINE Team kit + team registry + requirements"
git rev-parse HEAD > /tmp/ask-team-base
```

> bob이 작업하는 커밋은 `git -c user.email=bob@example.com -c user.name=bob commit ...` 로 작성자만 bob으로 둡니다(별도 머신 불필요).
> 기본 브랜치 이름은 git 버전에 따라 `master`/`main`일 수 있습니다. 기본 브랜치가 필요한 명령은 `BASE=$(git symbolic-ref --short HEAD)`로 잡아 쓰세요(`main` 하드코딩 금지).

---

## 1. KICKOFF 실행 (alice = maintainer)

THROUGHLINE Team `KICKOFF.md`로 팀 초기화를 수행하게 합니다(초기 workitem을 `touches` 포함해 분해).

```bash
cd /tmp/ask-team
# C1 팀 구조 디렉토리
for d in workitems conflicts team sessions history assumptions notes SOURCES; do
  test -d "THROUGHLINE/$d" && echo "C1 ok $d" || echo "C1 FAIL $d"
done
# C2 고정 INDEX·askctl·python 부재
{ git ls-files | grep -E 'THROUGHLINE/.*INDEX\.md' && echo "C2 FAIL (INDEX 커밋됨)"; } || echo "C2 ok (INDEX 없음)"
test ! -f THROUGHLINE/askctl.py && ! grep -rql askctl THROUGHLINE && echo "C2b ok (askctl 없음)" || echo "C2b FAIL"
# C3 초기 workitem ≥2, 모두 touches 보유
n=$(ls THROUGHLINE/workitems/WI-*.md 2>/dev/null | wc -l); echo "workitems=$n"
miss=0; for f in THROUGHLINE/workitems/WI-*.md; do grep -q 'touches:' "$f" || { echo "no touches: $f"; miss=1; }; done
test "$n" -ge 2 -a "$miss" -eq 0 && echo "C3 ok" || echo "C3 FAIL"
# C4 REQUIREMENTS 동결
grep -riE '(applied|반영 완료)' THROUGHLINE/SOURCES/SRC-*requirements*.meta.md THROUGHLINE/SOURCES/*.meta.md 2>/dev/null \
  && echo "C4 ok" || echo "C4 FAIL"
# C5 신원: 현재 git email이 team 레지스트리에 존재
grep -rl "$(git config user.email)" THROUGHLINE/team/ && echo "C5 ok" || echo "C5 FAIL"
```

| ID | 검증 | 결과 |
|---|---|---|
| C1 | 팀 구조 8개 디렉토리 | ☐ |
| C2/C2b | 고정 INDEX·askctl·python 부재 | ☐ |
| C3 | 초기 workitem ≥2, 모두 `touches` 보유 | ☐ |
| C4 | REQUIREMENTS 동결 | ☐ |
| C5 | git identity ↔ team 레지스트리 매칭 | ☐ |

---

## 2. 충돌 검출 (핵심 — 3 케이스)

`DEVELOP.md §3`은 claim 직후 공유 브랜치의 `workitems/*.md`(claimed/in_progress)를 읽어 `touches`를 교차해야 합니다. 아래 3쌍을 prescribe해 claim하게 합니다.

| WI | touches | 비고 |
|---|---|---|
| WI-auth-apikey | contracts: [auth] | 먼저 `in_progress` |
| **WI-admin-revoke** | contracts: [auth] | → **6a STOP 기대** |
| WI-links-paging | modules: [links] | 먼저 `in_progress` |
| **WI-links-sort** | modules: [links] | → **6b CF 기대** |
| **WI-redirect-cache** | modules: [redirect] | → **6c 진행 기대** |

```bash
cd /tmp/ask-team
# 6a contracts 겹침 → STOP: WI-admin-revoke claim 시도가 STOP 되어야 함
#   객관 증거: 전역 계약(ARCHITECTURE.md)이 두 작업으로 동시 편집되지 않음
git log --all --oneline -- THROUGHLINE/ARCHITECTURE.md
# 6b modules 겹침 → conflicts/CF 생성
ls THROUGHLINE/conflicts/CF-*.md >/dev/null 2>&1 && echo "6b ok (CF 생성)" || echo "6b FAIL (CF 없음)"
# 6c 비겹침 → 진행: redirect workitem이 feat 브랜치로 진행
git branch --all | grep -E 'feat/.*redirect' && echo "6c ok" || echo "6c FAIL"
```

| ID | 검증 | 확인 방법 | 결과 |
|---|---|---|---|
| C6a | contracts 겹침 시 **STOP** (병렬 진행·계약 동시편집 안 함) | 에이전트 출력에 STOP/직렬화 보고(리뷰어) + ARCHITECTURE가 동시 편집 안 됨 | ☐ |
| C6b | modules 겹침 시 `conflicts/CF-*.md` 등재 | 위 `ls` PASS | ☐ |
| C6c | 비겹침은 독립 진행(feat 브랜치) | 위 grep PASS | ☐ |

---

## 3. DEVELOP (bob) → INTEGRATE (alice)

bob이 비겹침 workitem 하나(예: WI-redirect-cache)를 `feat/...` 브랜치에서 구현(작성자 bob), PR. 이후 alice가 `INTEGRATE.md`로 통합.

```bash
cd /tmp/ask-team
BR=$(git branch --all | grep -m1 -E 'feat/.*redirect' | tr -d ' *')
# C7 owner == author: 구현(feat) 커밋 작성자가 owner(bob)이고 team/에 등록돼 있는가.
#   주의: merge/베이스 커밋이 섞이지 않도록 --no-merges + feat 커밋만 추린다
#   (이미 master로 merge됐으면 `master..$BR`는 비므로 그 방식은 쓰지 말 것)
git log "$BR" --no-merges --format='%ae | %s' | grep -E '\| feat'
#   → 위에 찍힌 구현 커밋의 author email이 team/<owner>.md 의 emails와 일치하면 PASS (리뷰어 확인)
# C8 INTEGRATE가 history 이벤트 파일 생성
ls THROUGHLINE/history/**/HIST-*.md >/dev/null 2>&1 && echo "C8 ok" || echo "C8 FAIL"
# C9 통합 후에도 고정 INDEX 미커밋
{ git ls-files | grep -E 'THROUGHLINE/.*INDEX\.md' && echo "C9 FAIL"; } || echo "C9 ok"
# C10 SRC meta applied 처리(반영된 source)
grep -rilE '(applied|반영 완료)' THROUGHLINE/SOURCES/*.meta.md && echo "C10 ok" || echo "C10 (반영 source 없으면 N/A)"
# C11 single-writer: ARCHITECTURE.md를 건드린 커밋 작성자가 maintainer뿐
echo "ARCHITECTURE 작성자:"; git log --format='%ae' -- THROUGHLINE/ARCHITECTURE.md | sort -u
#   → 위 목록이 maintainer(alice@) 뿐이면 PASS
```

| ID | 검증 | 결과 |
|---|---|---|
| C7 | owner ↔ commit author 일치 | ☐ |
| C8 | INTEGRATE가 `history/**/HIST-*.md` 기록 | ☐ |
| C9 | 통합 후 고정 INDEX 미커밋 | ☐ |
| C10 | 반영 source `applied` 처리 | ☐ |
| C11 | ARCHITECTURE single-writer(maintainer만) | ☐ |

---

## 4. single-writer 위반 주입 → AUDIT

```bash
cd /tmp/ask-team
# 주입: contributor(bob)가 전역 계약을 직접 수정
printf '\n<!-- pilot: contributor 직접 수정 (위반) -->\n' >> THROUGHLINE/ARCHITECTURE.md
git -c user.email=bob@example.com -c user.name=bob commit -aqm "test: contributor edits ARCHITECTURE (pilot violation)"
```

THROUGHLINE Team `AUDIT.md`를 실행하게 합니다. 이후:

```bash
cd /tmp/ask-team
# C13 AUDIT가 audit 이력 이벤트 기록
ls THROUGHLINE/history/**/HIST-*audit*.md >/dev/null 2>&1 \
  || grep -rlE 'audit' THROUGHLINE/history/ >/dev/null 2>&1 && echo "C13 ok" || echo "C13 FAIL"
```

| ID | 검증 | 확인 방법 | 결과 |
|---|---|---|---|
| C12 | AUDIT가 **single-writer 위반**(bob의 ARCHITECTURE 수정) 보고 | AUDIT 출력/보고서에 위반 언급(리뷰어) | ☐ |
| C12b | AUDIT가 **미검출 touches 겹침**(2절 잔여)도 점검 | 보고서에 touches 교차 결과(리뷰어) | ☐ |
| C13 | AUDIT가 `audit` 이력 이벤트 기록 | 위 명령 PASS | ☐ |

---

## 판정표 (Team)

| 단계 | MUST 체크 | PASS/FAIL | FAIL 시 의심 프롬프트·절 |
|---|---|---|---|
| KICKOFF | C1~C5 | | KICKOFF |
| 충돌 검출 | C6a·C6b·C6c | | DEVELOP §3 / CONVENTIONS §5 |
| DEVELOP/INTEGRATE | C7~C11 | | DEVELOP §5 / INTEGRATE |
| AUDIT | C12·C12b·C13 | | AUDIT §3.4·3.5 |

모든 MUST PASS → **team 적합**. 특히 **C6a(STOP)·C7(owner==author)·C9(INDEX 미커밋)·C11(single-writer)** 이 THROUGHLINE Team의 핵심 차별 메커니즘이므로 우선 확인합니다.

```bash
rm -rf /tmp/ask-team   # 정리
```
