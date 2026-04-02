# Business Analyst — machine 활용 패턴

## 기본 규칙

1. **계획서를 먼저 쓴다** — 인라인 짧은 지시 문자열로의 실행은 금지. 계획서 파일을 넘긴다
2. **출력은 드래프트** — machine 출력은 반드시 스스로 검증하고, `status: approved`로 한 뒤 다음 공정으로 넘긴다
3. **저장 위치**: `state/plans/{YYYY-MM-DD}_{개요}.{type}.md`(`/tmp/` 금지)
4. **레이트 제한**: chat 5회/session, heartbeat 2회
5. **machine은 인프라에 접근할 수 없다** — 기억·메시지·조직 정보는 계획서에 포함한다

---

## 개요

Business Analyst는 외부 도구(web_search, x_search 등)로 수집한 원시 데이터를 machine으로 구조화·분석한다.

- 조사 계획 작성 → Analyst 본인이 작성
- 외부 도구에 의한 데이터 수집 → Analyst 본인이 실행
- 수집 데이터의 구조화·분석 → machine에 위임하고 Analyst가 검증
- 정보 소스 명기 → Analyst가 최종 확인

---

## Phase A: 데이터 구조화

### Step 1: 원시 데이터를 수집한다

Strategist의 조사 의뢰에 따라 web_search / x_search 등 외부 도구로 원시 데이터를 수집한다.

### Step 2: 구조화 계획서를 작성한다(Analyst 본인이 작성)

구조화 목적·대상 데이터·분류 축을 명확히 한 계획서를 만든다.

```bash
write_memory_file(path="state/plans/{date}_{테마}.structuring-plan.md", content="...")
```

### Step 3: machine에 데이터 구조화를 던진다

수집한 원시 데이터 + 구조화 계획서를 입력으로 machine에 데이터 구조화를 의뢰한다.

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{structuring-plan.md})" \
  -d /path/to/workspace
```

machine이 실행하는 처리:
- 데이터 분류·카테고리화
- 트렌드 추출
- 통계 요약

결과를 `state/plans/{date}_{테마}.market-analysis.md`로 저장한다(`status: draft`).

### Step 4: market-analysis.md를 검증한다

Analyst가 market-analysis.md를 읽고 `analyst/checklist.md`에 따라 검증한다:

- [ ] 전 정보에 소스(URL, 날짜)가 붙어 있는가
- [ ] 사실과 해석이 분리되어 있는가
- [ ] machine이 추측으로 보완한 부분이 없는가

문제가 있으면 Analyst 본인이 수정하고 `status: approved`로 변경한다.

---

## Phase B: 경쟁 분석

### Step 5: 경쟁 정보를 수집한다

복수 경쟁에 대해 단편 정보(제품 정보, 가격, 기능, 조직 정보 등)를 수집한다.

### Step 6: machine에 경쟁 분석을 던진다

수집한 경쟁 정보를 입력으로 구조화된 경쟁 분석을 machine에 의뢰한다.

machine이 생성하는 내용:
- 비교 매트릭스(기능·가격·시장 포지션)
- 각사 강점·약점 분석
- 포지셔닝 맵

결과를 `state/plans/{date}_{테마}.competitive-report.md`로 저장한다(`status: draft`).

### Step 7: competitive-report.md를 검증한다

Analyst가 competitive-report.md를 읽고 `analyst/checklist.md`에 따라 검증한다.
정확성·소스 신뢰성을 확인하고 `status: approved`로 변경한다.

---

## 시장 분석 보고서 템플릿(market-analysis.md)

```markdown
# 시장 분석 보고서: {테마}

status: draft
author: {anima 이름}
date: {YYYY-MM-DD}
type: market-analysis
source: {Strategist 조사 의뢰 경로}

## 조사 요약

- 조사 항목 수: {N}
- 신뢰도 높은 소스: {N} / 신뢰도 중간: {N} / 미확인: {N}

## 정보 소스

| # | 소스 | URL | 취득일 | 신뢰도 |
|---|--------|-----|--------|--------|
| 1 | {소스명} | {URL} | {날짜} | 고/중/저 |

## 시장 동향

{시장 전체 트렌드 분석}

## 세그먼트 분석

{시장 세그먼트별 분석}

## 주요 발견

{Strategist 전략 판단에 영향을 주는 중요 발견 요약}

## 미확인 사항

| # | 항목 | 미확인 사유 | 권장 액션 |
|---|------|------------|-------------|
| 1 | {항목} | {사유} | {다음 스텝} |

## 셀프 체크 결과

- [ ] 전 정보에 소스 부착
- [ ] 사실과 해석 분리
- [ ] 데이터 신선도 명기
```

## 경쟁 분석 보고서 템플릿(competitive-report.md)

```markdown
# 경쟁 분석 보고서: {테마}

status: draft
author: {anima 이름}
date: {YYYY-MM-DD}
type: competitive-report

## 비교 매트릭스

| 항목 | 자사 | 경쟁A | 경쟁B | 경쟁C |
|------|------|-------|-------|-------|
| {기능1} | {평가} | {평가} | {평가} | {평가} |

## 각사 분석

### {경쟁사명}

- **강점**: {분석}
- **약점**: {분석}
- **시장 포지션**: {분석}
- **최근 동향**: {분석}
- **소스**: {URL, 날짜}

## 포지셔닝

{시장 내 포지셔닝 분석}

## 주요 발견

{Strategist 전략 판단에 영향을 주는 경쟁 동향}
```

---

## 제약 사항

- machine 출력을 그대로 Strategist에 납품해서는 안 된다(NEVER) — 반드시 Analyst가 검증한다
- 정보 소스 명기는 machine 지시에 포함한다(MUST)
- 추측으로 정보를 보완해서는 안 된다(NEVER) — 미확인 사항은 명시한다
- `status: approved`가 아닌 market-analysis.md를 Strategist에 피드백해서는 안 된다(NEVER)
