# Secretary — machine 활용 패턴

## 기본 규칙

1. **사람 지시가 먼저** — 문서 작성은 사람의 의뢰를 기점으로 한다. 자체적인 문서 작성은 원칙적으로 하지 않는다
2. **출력은 초안** — machine 출력은 반드시 직접 검증하고, 사람에게 제시한 뒤 배포한다
3. **저장 위치**: `state/plans/{YYYY-MM-DD}_{개요}.{type}.md`(`/tmp/` 금지)
4. **레이트 제한**: chat 5회/session, heartbeat 2회
5. **machine은 인프라에 접근 불가** — 필요한 정보(수신자, 회사 정보 등)를 지시문에 포함할 것

---

## 개요

Secretary는 정보 트리아지·대행 전송이 주 업무이며, 문서 작성·PDF 변환은 machine에 위임한다.

- 비즈니스 문서 작성 → machine이 생성, Secretary가 검증
- 보고서 정형·PDF 변환 → machine이 변환, Secretary가 품질 확인
- 사람에게 제시하고, 승인 후 배포

---

## Phase A: 비즈니스 문서 작성

### Step 1: 사람 지시 확인

사람으로부터 문서 작성 의뢰를 받고 다음을 명확히 한다:
- 문서 종류(계약서·레터·보고서·회의록 등)
- 수신자·필요 정보
- 기한·형식 요건

불명확한 점이 있으면 채팅으로 사람에게 확인(추측으로 진행하지 않음).

### Step 2: machine에 문서 작성 위임

지시문을 작성하고 machine에 위임한다.

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{지시문 파일})" \
  -d /path/to/workspace
```

결과를 `state/plans/{date}_{개요}.document.md`로 저장한다.

**지시문에 포함할 정보**:
- 문서 종류·목적
- 수신자 정식 명칭·경칭
- 본문에 포함할 사항
- 형식 지정(비즈니스 레터, 보고서 형식 등)
- 서명란 정보

### Step 3: 품질 확인

Secretary가 `checklist.md` 섹션 C에 따라 검증한다:

- [ ] 사실 오기가 없는가(이름·회사명·법인 형태·날짜·금액)
- [ ] 수신자·경칭이 올바른가
- [ ] 의뢰 내용이 빠짐없이 반영되었는가
- [ ] 부적절한 표현이 없는가

문제가 있으면 Secretary가 직접 수정한다.

### Step 4: 사람에게 제시

검증 완료된 문서를 사람에게 채팅으로 제시하고 승인을 요청한다.

---

## Phase B: 보고서 정형·PDF 변환

### Step 5: 입력 준비

Markdown / 텍스트를 입력으로 machine에 정형·레이아웃 조정을 의뢰한다.

### Step 6: machine에 정형 위임

정형 지시를 작성하고 machine에 위임한다.

결과를 `state/plans/{date}_{개요}.formatted.md`로 저장한다.

### Step 7: PDF 변환

정형 완료된 문서를 PDF로 변환한다.

**docx 생성의 경우**:
```bash
python3 -c "
from docx import Document
doc = Document()
# ... 문서 생성 코드
doc.save('/path/to/output.docx')
"
```

**MD → HTML → PDF의 경우**:
```bash
pandoc input.md -o output.html --standalone
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file:///path/to/output.html')
    page.pdf(path='/path/to/output.pdf')
    browser.close()
"
```

### Step 8: PDF 품질 확인

생성된 PDF를 전 페이지 확인한다(MUST):
- [ ] 레이아웃이 무너지지 않았는가
- [ ] 글자 깨짐·폰트 누락이 없는가
- [ ] 페이지 분할이 적절한가
- [ ] 헤더·푸터가 올바른가

### Step 9: 사람에게 제시·배포

품질 확인 완료된 PDF를 사람에게 제시하고, 승인 후 URL을 배포한다.

---

## 문서 템플릿

### 비즈니스 레터

```markdown
# {문서 제목}

status: draft
author: {anima명}
date: {YYYY-MM-DD}
type: business-letter

## 수신자

{수신자 정식 명칭}
{부서·직위}
{담당자명} 님

## 본문

{본문}

## 서명

{서명란}
```

### 보고서

```markdown
# {보고서 제목}

status: draft
author: {anima명}
date: {YYYY-MM-DD}
type: report

## 개요

{1~3문 요지}

## 상세

{본문}

## 첨부 자료

{첨부가 있는 경우}
```

---

## 제약 사항

- 기밀 정보를 포함하는 문서의 외부 배포는 사람 승인 없이 하지 않는다(NEVER)
- 법인 정보(주소·대표자명·법인 번호 등)는 사전에 사람에게 확인 후 기재(MUST)
- PDF 생성 후 반드시 전 페이지 읽기 확인(MUST)
- 사람 승인 전에 문서를 외부 배포하지 않는다(NEVER)
