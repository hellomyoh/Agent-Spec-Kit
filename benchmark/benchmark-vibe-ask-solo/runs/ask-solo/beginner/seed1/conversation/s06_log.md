# CONVERSATION — S6 (seed1, ask-solo)

## Request (user, verbatim)
> 아 그리고 검색창 비었을 때는 그냥 전체 다 보여주자. 그게 더 자연스럽잖아. 평범한 목록처럼.

Translation: "Oh, and when the search box is empty, let's just show everything.
That's more natural, isn't it? Like an ordinary list."

Net ask: a criterion-less search (empty/blank search box) should return the whole
catalog, not nothing.

## Conflict check (vs recorded decisions)
This directly REVERSES **D10 (S3)**, which made a criterion-less search return `[]`
("검색창 비어 있을 때 전체를 다 쏟아내지 마 ... 뭐라도 입력하기 전엔 아무것도 안
보이게 해줘" / don't dump everything when empty; show nothing until I type).

Classification — INTENTIONAL supersede (not ambiguous/forgetting drift):
- The request is explicit and decisive ("그냥 전체 다 보여주자") and carries its own
  affirmative rationale ("더 자연스럽잖아. 평범한 목록처럼" — more natural, like an
  ordinary list). That is a reasoned change of mind, not a vague slip.
- It is the same form as the original D10 ask, and as D12's reasoned reversal of D8
  ("실제로 써보니 짜증나네") — both of which this SSOT records as legitimate
  intentional supersedes after real use. This codebase's pattern is that a clearly
  reasoned directive conflicting with a prior decision is an intentional supersede.
- D10 itself pre-authorised this exact move: its contract note said "If a future
  session needs `search(query=None) == all()`, revisit here." This is that session.
- The contract (provided/contract.py) does NOT pin list mode; it delegates blank
  handling to the user prompts. Returning the full catalog for `query=None`/blank is
  within that delegation, so the fixed surface is respected.

Decision per the conflict rule: intentional change -> SUPERSEDE D10 + update
FEATURES, then implement. (We do NOT preserve D10 / flag-for-confirmation; that path
is for ambiguous drift that would silently break a policy the user still wants — not
the case here, where the user is explicitly and reasonably changing that exact
policy.) `all()` and every other policy are preserved.

## Plan
1. Remove the D10 early `return []` show-nothing guard in `search` so a blank/None
   query simply applies no text filter; with no `where`, the full pipeline runs over
   the whole catalog (insertion order).
2. Keep everything else intact: `where` equality + forgiving unknown field (D7/D12),
   `sort_by` stable + loud-on-unknown (D9/D13), `limit` validation (D11), copies (D3).
3. Record consequence: `sort_by`/`limit` now act on the full catalog for a
   criterion-less search (was moot when the result was `[]`).
4. Update SSOT (DECISIONS D14+D15, FEATURES, PRODUCT, PROGRESS) and verify.

## SSOT updates
- **DECISIONS.md**: added **D14 (S6)** — empty search shows everything again;
  supersedes D10 entirely (restores D6's net effect via list-mode framing, not D6's
  mechanism). Added **D15 (S6)** — `sort_by`/`limit` now apply to a criterion-less
  full-catalog search; supersedes D11's "criterion-less `search(limit=5)` is `[]`"
  clause (rest of D11 stands).
- **FEATURES.md**: rewrote the empty-search bullet (now "shows everything"), the
  blank-query note, and the `limit` clause (criterion-less `limit` returns first N).
- **PRODUCT.md**: updated the S3 scope line and added an S6 line.
- **PROGRESS.md**: added the S6 entry; marked the old D10 "revisit" note resolved.

## Implementation (catalog.py)
Single behavioural change: deleted the D10 guard
`if where is None and query_is_blank: return []`. `query_is_blank` is still computed
and still gates the text filter, so a blank query means "no text filter" and a fully
criterion-less search now falls through to return the whole catalog. Module docstring
and the `search`/`all` docstrings updated to current behaviour (no history in code).

## Test run
`python -c "import catalog"` -> OK.
Ran a 37-check suite (scratchpad, outside the work dir). Highlights:
- `search()` / `search(None)` / `search("")` / `search("   ")` == `all()` (full
  catalog, insertion order).
- empty search + `sort_by` orders the full catalog (missing-field last); empty
  search + `limit=2` -> first two; + `sort_by`+`limit=3` -> top 3 by field;
  `limit=0` -> `[]`; empty catalog -> `[]`.
- Full S1–S5 regression: query substring/case/missing-name; where equality/multi-
  key/forgiving-unknown/empty-catalog; sort stable/missing-last/unknown-raises/
  empty-result-no-raise; limit caps/over-length/None/negative/non-int/bool; copy-
  safety (add, search, all, where-dict-untouched).
Result: ALL 37 CHECKS PASSED.

## Summary
Reversed D10 per an explicit, reasoned user request: a blank/empty search now
returns the whole catalog (an ordinary list) instead of `[]`. Recorded it as an
intentional supersede (D14), with D15 capturing the consequent `sort_by`/`limit`
behaviour on a criterion-less search. All prior behaviour (where/sort/limit/copy-
safety, `all()`) preserved; import + 37-check suite green.
