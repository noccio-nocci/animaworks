# COO — machine 활용 패턴

## 기본 규칙

1. **계획서를 먼저 작성** — 분석 목적을 명확히 한 후 machine에 투입한다. 목적 없는 분석 금지
2. **출력은 드래프트** — machine 출력은 분석 소재이며 최종 판단이 아니다. COO가 판단을 추가한 후 보고
3. **저장 위치**: `state/plans/{YYYY-MM-DD}_{개요}.{type}.md`(`/tmp/` 금지)
4. **레이트 제한**: chat 5회/session, heartbeat 2회
5. **machine은 인프라에 접근 불가** — 필요한 정보(org_dashboard 출력, activity_log 데이터 등)는 지시문에 포함

---

## 개요

COO는 위임 판단·부문 감시·경영 보고를 주된 업무로 하며, 조직 분석·KPI 집계·보고서 드래프트 작성을 machine에 위탁한다.

- 조직 상황의 구조화 분석 → machine이 분석, COO가 판단
- KPI 집계·통계 정보 추출 → machine이 집약, COO가 검증
- 사람 대상 보고서 작성 → machine이 드래프트, COO가 판단 코멘트 추가

**COO 자신이 판단을 수행하는 것이 필수(MUST). machine 출력을 그대로 사람에게 보고하지 않는다.**

---

## Phase A: 조직 분석

### Step 1: 분석 대상 특정

org_dashboard / audit_subordinate의 출력을 취득하고 분석 범위를 결정:
- 전체 개황의 정기 분석(일별·주별)
- 특정 부문의 이상 감지(STALE 태스크, 에러율 상승 등)
- 부문 간 병목 특정

### Step 2: 분석 계획서 작성

```markdown
# 조직 분석 계획서

status: draft
author: {anima명}
date: {YYYY-MM-DD}
type: org-analysis

## 분석 목적
{무엇을 밝히려 하는가}

## 대상 부문
{전체 / 특정 부문명}

## 분석 기간
{최근 24h / 최근 1주 / 특정 날짜 범위}

## 입력 데이터
{org_dashboard 출력, audit_subordinate 결과, activity_log 발췌 등}

## 분석 관점
- 태스크 소화 상황(STALE / OVERDUE 유무)
- 에러·장애 유무와 영향 범위
- 부문 간 의존·블로킹
- 리소스 편중(특정 멤버에 부하 집중 등)
```

### Step 3: machine에 분석 의뢰

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{계획서_파일})" \
  -d /path/to/workspace
```

결과를 `state/plans/{date}_{개요}.org-analysis.md`로 저장.

### Step 4: COO가 결과 확인·판단

machine 분석 결과를 확인하고 다음을 추가:
- 이상 감지 시 액션 판단(위임 / 에스컬레이션 / 경과 관찰)
- 판단 근거 명기
- 필요 시 직속 부하에게 지시(delegate_task / send_message)

---

## Phase B: KPI 집계

### Step 5: 집계 지시서 작성

```markdown
# KPI 집계 지시서

status: draft
author: {anima명}
date: {YYYY-MM-DD}
type: kpi-summary

## 집계 목적
{정기 보고 / 특정 과제 분석}

## 집계 기간
{최근 24h / 최근 1주 / 월별}

## 입력 데이터
{activity_log 발췌, task_queue 통계, org_dashboard 수치 등}

## 집계 항목
- 부문별 활동량(tool_use 횟수, 메시지 송수신 수)
- 태스크 소화율(완료 / 진행 중 / STALE / OVERDUE)
- 에러율(error 타입 액티비티 수 / 전체 액티비티 수)
- 부문별 응답 시간(DM 수신→응답 평균 소요 시간)
- {추가 조직 고유 KPI}
```

### Step 6: machine에 집계 의뢰

지시서에 기반하여 machine에 집계를 의뢰.
결과를 `state/plans/{date}_{개요}.kpi-summary.md`로 저장.

### Step 7: COO가 검증

machine 집계 결과를 검증:
- [ ] 집계 대상 기간이 정확한가
- [ ] 수치에 명백한 이상(자릿수 오류, 마이너스 값 등)이 없는가
- [ ] 전 부문이 포함되어 있는가

---

## Phase C: 보고서 드래프트

### Step 8: 보고서 지시 작성

Phase A + B 결과를 입력으로 사람 대상 보고서의 드래프트 작성을 지시.

```markdown
# 보고서 드래프트 지시

status: draft
author: {anima명}
date: {YYYY-MM-DD}
type: report-draft

## 보고 종별
{일일 다이제스트 / 주간 회고 / 월간 전략 리뷰 / 임시 보고}

## 입력
- 조직 분석 결과: state/plans/{org-analysis 파일}
- KPI 집계 결과: state/plans/{kpi-summary 파일}

## 보고 포맷
### 경영 요약(3~5줄)
{전체 상황을 간결하게}

### 부문별 상세
{부문별 주요 토픽}

### 주의 사항·리스크
{주의가 필요한 안건, 에스컬레이션이 필요한 사항}

### 액션 아이템
{COO로서 실행하는 / 실행 예정인 액션}
```

### Step 9: machine에 드래프트 작성 의뢰

결과를 `state/plans/{date}_{개요}.report-draft.md`로 저장.

### Step 10: COO가 판단 코멘트 추가

machine 드래프트에 다음을 추가(MUST):
- COO 자신의 상황 판단·소견
- 사람에 대한 액션 아이템 제안
- 에스컬레이션이 필요한 사항의 명시

### Step 11: 보고·배포

- `call_human`으로 사람에게 보고
- 공식 서류가 필요한 경우 비서에게 PDF화 의뢰(`send_message`)

---

## 제약 사항

- 조직 분석의 「판단」은 COO 자신이 수행(MUST). machine 출력을 그대로 판단으로 취급하지 않음
- 사람에 대한 보고에는 COO 자신의 판단 코멘트를 반드시 추가(MUST)
- machine 출력에 개인 정보·기밀 정보가 포함된 경우 외부 배포 시 삭제·마스킹(MUST)
- 감사 결과를 변경하여 보고하지 않음(NEVER). 내부 감사의 독립성을 보장
