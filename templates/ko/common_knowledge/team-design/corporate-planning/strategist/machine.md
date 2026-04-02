# Corporate Strategist — machine 활용 패턴

## 기본 규칙

1. **계획서를 먼저 쓴다** — 인라인 짧은 지시 문자열로의 실행은 금지. 계획서 파일을 넘긴다
2. **출력은 드래프트** — machine 출력은 반드시 스스로 검증하고, `status: approved`로 한 뒤 다음 공정으로 넘긴다
3. **저장 위치**: `state/plans/{YYYY-MM-DD}_{개요}.{type}.md`(`/tmp/` 금지)
4. **레이트 제한**: chat 5회/session, heartbeat 2회
5. **machine은 인프라에 접근할 수 없다** — 기억·메시지·조직 정보는 계획서에 포함한다

---

## 개요

Corporate Strategist는 PdM(계획·판단)과 Engineer(실행)를 겸한다.

- 분석 계획(strategic-plan.md) 작성 → Strategist 본인이 작성
- 사업 환경 분석 실행 → machine에 위임하고 Strategist가 검증
- 리스크 판단 확정 → Strategist 본인이 판단
- 검증은 2회: machine 분석 결과 확인 시와 Coordinator로부터의 피드백 통합 시

---

## Phase A: 사업 환경 분석

### Step 1: Analyst의 시장 분석 보고를 확인한다

Analyst로부터 `market-analysis.md`(`status: approved`)를 받아 내용을 파악한다.

### Step 2: strategic-plan.md를 작성한다(Strategist 본인이 작성)

분석 목적·대상·프레임워크 선택·내부 데이터 소재를 명확히 한 계획서를 만든다.

```bash
write_memory_file(path="state/plans/{date}_{테마}.strategic-plan.md", content="...")
```

**strategic-plan.md의 「분석 목적」「프레임워크 선택」「스코프」는 Strategist 판단의 핵이며, machine에게 쓰게 해서는 안 된다(NEVER).**

### Step 3: machine에 사업 환경 분석을 던진다

strategic-plan.md + market-analysis.md를 입력으로 사업 환경의 구조 분석을 machine에 의뢰한다.

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{strategic-plan.md})" \
  -d /path/to/workspace
```

machine이 실행하는 분석:
- PEST / SWOT / 5Forces 등 프레임워크 분석
- 「이길 수 있는 영역」추출
- 기회/위협의 우선순위 부여

결과를 `state/plans/{date}_{테마}.strategy-report.md`로 저장한다(`status: draft`).

### Step 4: strategy-report.md를 검증한다

Strategist가 strategy-report.md를 읽고 `strategist/checklist.md` 섹션 A에 따라 검증한다.
문제가 있으면 Strategist 본인이 수정하고 `status: reviewed`로 변경한다.

---

## Phase B: 전략 제안서 드래프트

### Step 5: machine에 전략 제안서를 의뢰한다

Phase A의 분석 결과 + OKR을 입력으로 전략 제안서 드래프트를 machine에 의뢰한다.

machine이 생성하는 내용:
- 목표와 조치 목록
- 리소스 배분안
- 리스크 분석

결과를 `state/plans/{date}_{테마}.strategic-proposal.md`로 저장한다(`status: draft`).

### Step 6: 전략 제안서를 검증한다

Strategist가 strategic-proposal.md를 읽고 `strategist/checklist.md` 섹션 B에 따라 검증한다.
OKR과의 정합성, 조치의 실행 가능성, 리소스 배분의 타당성을 확인한다.

---

## Phase C: 이니셔티브 진행 분석

### Step 7: machine에 진행 분석을 의뢰한다

Strategic Initiative Tracker 데이터를 입력으로 진행 분석을 machine에 의뢰한다.

machine이 실행하는 분석:
- 정체 이니셔티브 검지(1개월 이상 스테이지 변화 없음)
- KPI 달성 전망 평가
- 병목 분석

### Step 8: 진행 분석을 검증하고 판단한다

Strategist가 분석 결과를 읽고 각 이니셔티브에 대해 판단한다:
- **계속**: 계획대로 진행
- **수정**: 조치 변경
- **중단**: 사유를 기록하고 Tracker에서 제외

`strategist/checklist.md` 섹션 C에 따라 Tracker 전건 갱신을 확인한다.

---

## 분석 계획서 템플릿(strategic-plan.md)

```markdown
# 전략 분석 계획서: {테마}

status: draft
author: {anima 이름}
date: {YYYY-MM-DD}
type: strategic-plan

## 분석 목적

{무엇을 밝힐지 — 1~3문}

## 입력 데이터

| 데이터 | 소스 | 비고 |
|--------|--------|------|
| 시장 분석 보고 | Analyst: market-analysis.md | {경로} |
| 내부 데이터 | {소스} | {개요} |

## 프레임워크 선택

{Strategist 판단으로 선택}

- {프레임워크1: 예 — PEST 분석}
- {프레임워크2: 예 — SWOT 분석}

## 분석 스코프

{무엇을 포함하고 무엇을 제외할지}

## 출력 형식

- 「이길 수 있는 영역」추출과 우선순위
- 기회/위협 평가 매트릭스
- 전략 옵션 제시

## 기한

{deadline}
```

## 분석 보고서 템플릿(strategy-report.md)

```markdown
# 전략 분석 보고서: {테마}

status: draft
author: {anima 이름}
date: {YYYY-MM-DD}
type: strategy-report
source: state/plans/{원본 strategic-plan.md}

## 종합 평가

{사업 환경 평가 요약 — 1~3문}

## 프레임워크 분석 결과

### {프레임워크명}

{분석 결과}

## 「이길 수 있는 영역」

| # | 영역 | 근거 | 우선도 | 리스크 |
|---|------|------|--------|--------|
| 1 | {영역명} | {근거} | 고/중/저 | {리스크 개요} |

## 기회/위협 평가

| # | 항목 | 유형 | 영향도 | 대응 방침 |
|---|------|------|--------|---------|
| 1 | {항목} | 기회/위협 | 고/중/저 | {방침} |

## 추가 코멘트

{Strategist 본인의 소견·보충}
```

## 전략 제안서 템플릿(strategic-proposal.md)

```markdown
# 전략 제안서: {테마}

status: draft
author: {anima 이름}
date: {YYYY-MM-DD}
type: strategic-proposal

## OKR과의 정합성

{대상 OKR과 본 제안의 관계}

## 조치 목록

| # | 조치 | 목표 | 리소스 | 기한 | 리스크 |
|---|------|------|---------|------|--------|
| 1 | {조치명} | {달성 목표} | {필요 리소스} | {기한} | {리스크 개요} |

## 리소스 배분

{전체 리소스 배분 방침}

## 리스크 분석

| # | 리스크 | 영향도 | 발생 가능성 | 완화책 |
|---|--------|--------|-----------|--------|
| 1 | {리스크} | 고/중/저 | 고/중/저 | {완화책} |
```

---

## 제약 사항

- strategic-plan.md는 MUST: Strategist 본인이 작성한다
- strategy-report의 리스크 판단은 MUST: Strategist 본인이 확정한다(machine 출력은 드래프트로 검증한다)
- `status: reviewed`가 붙지 않은 strategy-report.md를 Coordinator에게 넘겨서는 안 된다(NEVER)
- Strategic Initiative Tracker에 기록된 이니셔티브를 언급 없이 소멸시켜서는 안 된다(NEVER — silent drop 금지)
