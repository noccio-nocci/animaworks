# CS Lead — machine 활용 패턴

## 기본 규칙

1. **계획서를 먼저 작성** — 인라인 짧은 지시 문자열로 실행 금지. 계획서 파일을 전달
2. **출력은 드래프트** — machine 출력은 반드시 직접 검증하고 `status: approved`로 바꾼 후 다음 단계로
3. **저장 위치**: `state/plans/{YYYY-MM-DD}_{개요}.{type}.md`(`/tmp/` 금지)
4. **레이트 제한**: chat 5회/session, heartbeat 2회
5. **machine은 인프라에 접근 불가** — 기억·메시지·조직 정보를 계획서에 포함할 것

---

## 개요

CS Lead는 PdM(계획·판단)과 Engineer(실행)를 겸임합니다. 4개 페이즈로 machine을 활용합니다.

- Phase A: cs-handoff.md를 분석하고 온보딩 계획 수립 → CS Lead가 검증
- Phase B: Health Tracker + 문의 이력을 분석하고 이탈 예측·개입 권고 → CS Lead가 판단
- Phase C: 리텐션 시책·대응 콘텐츠 제작 → CS Lead가 검증
- Phase D: VoC(고객의 소리) 집약 및 프로덕트 피드백 리포트 작성 → CS Lead가 확정

---

## Phase A: 온보딩 분석·계획

### Step 1: cs-handoff.md를 받아 확인

영업 Director로부터 `cs-handoff.md`(`status: draft`)를 받습니다. 전 섹션(고객 개요, 영업 프로세스 요약, 합의 사항, 미해결 사항, 커뮤니케이션 특성)을 확인합니다.

### Step 2: 온보딩 계획 지시서 작성(CS Lead 직접 작성)

온보딩 목적·고객 특성에 기반한 중점 사항·스코프를 명확히 한 지시서를 작성합니다.

```bash
write_memory_file(path="state/plans/{date}_{기업명}.onboarding-request.md", content="...")
```

**지시서의 「온보딩 목적」「중점 사항」「스코프」는 CS Lead의 판단 핵심이며, machine에 작성시켜서는 안 됩니다(NEVER).**

### Step 3: machine에 온보딩 계획 의뢰

지시서 + cs-handoff.md 내용을 입력으로 온보딩 계획 수립을 machine에 의뢰합니다.

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{onboarding-request.md})" \
  -d /path/to/workspace
```

결과를 `state/plans/{date}_{기업명}.onboarding-plan.md`로 저장(`status: draft`).

### Step 4: onboarding-plan.md 검증

CS Lead가 checklist 섹션 A에 따라 검증:
- [ ] cs-handoff.md의 전 항목이 커버되었는가
- [ ] 합의 사항·요망이 구체적 단계로 반영되었는가
- [ ] 미해결 사항에 대한 대응 방침이 포함되었는가
- [ ] 커뮤니케이션 특성이 고려되었는가

문제가 있으면 CS Lead가 직접 수정하고 `status: approved`로 변경.

### Step 5: Support에 위임

`delegate_task`로 `onboarding-plan.md`(`status: approved`)를 Support에 전달.

---

## Phase B: 고객 헬스 분석

### Step 6: 헬스 분석 지시서 작성(CS Lead 직접 작성)

Health Tracker 현황 + 최근 문의 이력을 정리한 지시서를 작성합니다.

### Step 7: machine에 헬스 분석 의뢰

지시서를 입력으로 헬스 스코어 산출·이탈 예측·개입 권고를 machine에 의뢰합니다.

결과를 `state/plans/{date}_health-analysis.md`로 저장(`status: draft`).

### Step 8: 분석 결과에 기반한 판단

CS Lead가 machine의 분석 결과를 확인하고 액션을 결정:
- Green → 경과 관찰. Health Tracker 갱신
- Yellow → Phase C에서 리텐션 시책 수립
- Red → 즉시 Phase C + 상위에 에스컬레이션

**헬스 스코어의 최종 판정은 CS Lead가 확정(machine 출력은 드래프트로 검증).**

---

## Phase C: 대응 콘텐츠 제작

### Step 9: 대응 지시서 작성(CS Lead 직접 작성)

대응이 필요한 고객·상황·목적을 명확히 한 지시서를 작성합니다.

**대응 방침·톤·목적은 CS Lead의 판단 핵심이며, machine에 작성시켜서는 안 됩니다(NEVER).**

### Step 10: machine에 대응 콘텐츠 제작 의뢰

지시서를 입력으로 커스터마이즈 대응 드래프트 작성을 machine에 의뢰합니다.

대상 콘텐츠 예:
- 리텐션 전략 제안서
- 고객 대상 개선 보고 이메일
- 에스컬레이션 대응 요약·제안
- 커스터마이즈 지원 가이드

### Step 11: 성과물 검증

CS Lead가 checklist 섹션 C에 따라 검증:
- [ ] 고객 상황에 맞는 커스터마이즈가 되었는가
- [ ] 톤이 적절한가(커뮤니케이션 특성 고려)
- [ ] 컴플라이언스 문제가 없는가

---

## Phase D: VoC 집약·프로덕트 피드백

### Step 12: VoC 집약 지시서 작성(CS Lead 직접 작성)

대상 기간의 문의 패턴·고객 피드백·Support 보고를 정리한 지시서를 작성합니다.

### Step 13: machine에 VoC 분석 의뢰

지시서를 입력으로 추세 분석·인사이트 추출·개선 제안을 machine에 의뢰합니다.

결과를 `state/plans/{date}_voc-report.md`로 저장(`status: draft`).

### Step 14: VoC 리포트 확정

CS Lead가 checklist 섹션 D에 따라 검증:
- [ ] 문의 추세가 정확히 반영되었는가
- [ ] 개선 제안에 근거가 있는가
- [ ] COO 보고 체재가 갖추어졌는가

확인 후 `status: approved`로 변경하고 COO에 `send_message (intent: report)`로 전송.

---

## 문서 템플릿

### onboarding-plan.md

```markdown
# 온보딩 계획: {기업명}

status: draft
author: {anima명}
date: {YYYY-MM-DD}
type: onboarding-plan
source: cs-handoff.md

## 고객 개요(cs-handoff.md에서)

{cs-handoff.md 요약}

## 온보딩 목표

{달성 목표 — 1~3항목}

## 단계

| # | 단계 | 담당 | 기한 | 완료 조건 |
|---|------|------|------|----------|
| 1 | {내용} | {Support/CS Lead} | {날짜} | {조건} |

## 중점 사항

{cs-handoff.md의 합의 사항·요망에 기반한 중점}

## 미해결 사항 대응

{cs-handoff.md의 미해결 사항에 대한 방침}

## 커뮤니케이션 방침

{키 퍼슨의 특성에 기반한 대응 방침}
```

### voc-report.md

```markdown
# VoC 리포트: {대상 기간}

status: draft
author: {anima명}
date: {YYYY-MM-DD}
type: voc-report
period: {YYYY-MM-DD} ~ {YYYY-MM-DD}

## 서머리

{주요 트렌드 요약 — 3~5항목}

## 문의 추세

| 카테고리 | 건수 | 전기 대비 | 대표 내용 |
|---------|------|---------|----------|
| {카테고리} | {N} | {↑/→/↓} | {내용} |

## 고객 피드백 분석

### 긍정적

{호평 포인트}

### 부정적

{불만·과제}

## 개선 제안

| # | 제안 | 근거 | 영향 범위 | 우선순위 |
|---|------|------|----------|---------|
| 1 | {제안} | {VoC 데이터 근거} | {영향 고객수/세그먼트} | {높음/중간/낮음} |

## 다음 액션

{COO·개발 팀에 요청하는 액션}
```

---

## 제약 사항

- cs-handoff.md의 수령 판단은 CS Lead 본인이 수행(MUST)
- 헬스 스코어의 최종 판정은 CS Lead가 확정(machine 출력은 드래프트로 검증)
- 대응 방침·톤·목적은 machine에 작성시켜서는 안 됨(NEVER)
- Health Tracker의 항목을 언급 없이 소멸시켜서는 안 됨(NEVER — silent drop 금지)
