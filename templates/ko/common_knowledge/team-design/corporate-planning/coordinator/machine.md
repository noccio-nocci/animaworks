# Strategy Coordinator — machine 활용 패턴

## 기본 규칙

1. **계획서를 먼저 쓴다** — 인라인 짧은 지시 문자열로의 실행은 금지. 계획서 파일을 넘긴다
2. **출력은 드래프트** — machine 출력은 반드시 스스로 검증하고, `status: approved`로 한 뒤 다음 공정으로 넘긴다
3. **저장 위치**: `state/plans/{YYYY-MM-DD}_{개요}.{type}.md`(`/tmp/` 금지)
4. **레이트 제한**: chat 5회/session, heartbeat 2회
5. **machine은 인프라에 접근할 수 없다** — 기억·메시지·조직 정보는 계획서에 포함한다

---

## 개요

Coordinator는 **machine에 검증 스캔을 위임하고, 그 스캔 결과의 정당성을 검증한다(메타 검증)**.

- 검증 관점 설계 → Coordinator 본인이 판단
- 가정 검증·KPI 정합 체크·Tracker 대조 실행 → machine에 위임
- 검출 결과의 정당성 검증 → Coordinator 본인이 판단
- 실행 가능성 최종 판단 → Coordinator 본인이 판단

machine은 데이터 정합 체크·가정의 논리 검증·Tracker 대조를 고속으로 수행할 수 있으나,
실행 가능성의 종합 판단이나 조직적 제약 평가는 Coordinator의 책임이다.

---

## 워크플로

### Step 1: 검증 계획서를 작성한다(Coordinator 본인이 작성)

검증 관점·대상·기준을 명확히 한 계획서를 만든다.

```bash
write_memory_file(path="state/plans/{date}_{테마}.verification.md", content="...")
```

작성 전에 Anima 측에서 아래 정보를 준비한다:
- Strategist의 `strategy-report.md`와 `strategic-plan.md`
- Strategic Initiative Tracker(전회 대비용)
- 관련 KPI 데이터(부서에서 수집)

### Step 2: machine에 검증 스캔을 던진다

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{verification-plan.md})" \
  -d /path/to/workspace
```

결과를 `state/plans/{date}_{테마}.verification-result.md`에 저장한다(`status: draft`).

### Step 3: 검증 결과를 메타 검증한다

Coordinator가 verification-result.md를 읽고 아래를 확인한다:

- [ ] 가정 챌린지 결과가 논리적인가(machine 지적이 요점을 찌르는가)
- [ ] KPI 정합 체크의 데이터 소스가 정확한가
- [ ] Tracker 대조에 누락이 없는가
- [ ] 오검출(False Positive)이 없는가
- [ ] Coordinator 본인 관점에서 추가할 지적이 없는가

Coordinator 본인이 수정·보충하고 실행 가능성 최종 판단을 더한다.

### Step 4: verification-report.md를 작성한다

메타 검증된 결과를 verification-report.md로 정리하고 `status: approved`로 변경한다.
approved인 verification-report.md를 Strategist에게 송부한다.

---

## 검증 계획서 템플릿(verification-plan.md)

```markdown
# 검증 계획서: {검증 대상 개요}

status: draft
author: {anima 이름}
date: {YYYY-MM-DD}
type: verification-plan

## 검증 관점

- [ ] 가정 챌린지: Strategist 전제 가정에 대한 반증적 검증
- [ ] KPI 정합: 각 부서 KPI 실태와 전략 목표의 괴리 확인
- [ ] Tracker 대조: Strategic Initiative Tracker 전건 status 갱신 확인
- [ ] 데이터 소스 검증: 시장 분석 보고 소스 신뢰성 체크
- [ ] 실행 가능성: 리소스·기간·조직 체제 제약과의 정합

## 대상

- strategy-report.md: {경로}
- strategic-plan.md: {경로}
- Strategic Initiative Tracker: {경로}
- KPI 데이터: {소스 / 저장 위치}

## 출력 형식(필수)

아래 형식으로 검증 결과를 출력할 것. **이 형식을 따르지 않은 출력은 무효로 한다.**

- **Critical**: 수정 필수 문제(가정 붕괴·KPI 괴리·silent drop)
- **Warning**: 수정 권장 문제(근거 부족·데이터 신선도)
- **Info**: 정보 제공·개선 제안
```

## 검증 보고서 템플릿(verification-report.md)

```markdown
# 검증 보고서: {테마}

status: draft
author: {anima 이름}
date: {YYYY-MM-DD}
type: verification-report

## 종합 판정

{APPROVE / REQUEST_CHANGES / COMMENT}

## 가정 챌린지 결과

| # | 가정 | Strategist 근거 | 검증 결과 | 최악 시나리오 | 권장 |
|---|------|-----------------|---------|------------|------|
| 1 | {가정} | {근거} | {타당/근거 부족/붕괴} | {가정이 무너진 경우} | {수정안} |

## KPI 정합 체크

| # | KPI | 전략 목표 | 실태값 | 괴리 | 판정 |
|---|-----|---------|--------|------|------|
| 1 | {KPI명} | {목표} | {실태} | {괴리 폭} | {OK / NG} |

## Tracker 대조

| # | 이니셔티브 | 전회 스테이지 | 금회 스테이지 | 정체 | 판정 |
|---|------------|------------|------------|------|------|
| 1 | {명칭} | {전회} | {금회} | {Y/N} | {OK / 대응 필요} |

## Coordinator 소견

{Coordinator 본인 분석·추가 관찰·권장 사항}
- 실행 가능성 종합 평가
- 조직적 제약 고려
- 각 부서에 조치 전달 시 유의점
```

---

## 제약 사항

- 검증 계획서(무엇을 관점으로 검증할지)는 MUST: Coordinator 본인이 작성한다
- machine 검증 결과를 그대로 Strategist에게 넘겨서는 안 된다(NEVER) — 반드시 Coordinator가 메타 검증한다
- `status: approved`가 아닌 verification-report.md를 Strategist에게 피드백해서는 안 된다(NEVER)
- 실행 가능성 최종 판단은 machine에 맡기지 않고 Coordinator 본인이 수행한다(MUST)
