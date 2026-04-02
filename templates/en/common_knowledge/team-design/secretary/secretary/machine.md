# Secretary — Machine Usage Patterns

## Ground Rules

1. **Human instruction first** — Document creation starts from a human request. Do not create documents proactively
2. **Output is a draft** — Always verify machine output yourself and present it to the human before delivery
3. **Save location**: `state/plans/{YYYY-MM-DD}_{summary}.{type}.md` (`/tmp/` forbidden)
4. **Rate limit**: chat 5 times/session, heartbeat 2 times
5. **Machine has no infrastructure access** — Include all necessary information (recipients, company details, etc.) in the instruction

---

## Overview

Secretary's primary duties are information triage and proxy sending; document creation and PDF conversion are delegated to machine.

- Business document creation → machine generates, Secretary verifies
- Report formatting / PDF conversion → machine converts, Secretary quality-checks
- Present to human; deliver only after approval

---

## Phase A: Business Document Creation

### Step 1: Confirm human's instruction

Receive a document creation request from the human and clarify:
- Document type (contract, letter, report, meeting minutes, etc.)
- Recipient and required information
- Deadline and format requirements

If anything is unclear, ask the human via chat (do not proceed on assumptions).

### Step 2: Delegate to machine

Write the instruction and delegate to machine.

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{instruction_file})" \
  -d /path/to/workspace
```

Save the result as `state/plans/{date}_{summary}.document.md`.

**Information to include in the instruction**:
- Document type and purpose
- Recipient's formal name and honorifics
- Content to include in the body
- Format specification (business letter, report format, etc.)
- Signature block information

### Step 3: Quality check

Secretary verifies against `checklist.md` Section C:

- [ ] No factual errors (names, company names, corporate type, dates, amounts)
- [ ] Recipient and honorifics are correct
- [ ] All requested content is reflected
- [ ] No inappropriate expressions

Fix any issues directly.

### Step 4: Present to human

Present the verified document to the human via chat and request approval.

---

## Phase B: Report Formatting & PDF Conversion

### Step 5: Prepare input

Prepare Markdown/text input and request formatting/layout from machine.

### Step 6: Delegate formatting to machine

Write formatting instructions and delegate to machine.

Save the result as `state/plans/{date}_{summary}.formatted.md`.

### Step 7: PDF conversion

Convert the formatted document to PDF.

**For docx generation**:
```bash
python3 -c "
from docx import Document
doc = Document()
# ... document generation code
doc.save('/path/to/output.docx')
"
```

**For MD → HTML → PDF**:
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

### Step 8: PDF quality check

Verify the generated PDF page by page (MUST):
- [ ] Layout is intact
- [ ] No garbled text or missing fonts
- [ ] Page breaks are appropriate
- [ ] Headers and footers are correct

### Step 9: Present and deliver

Present the quality-checked PDF to the human; deliver the URL after approval.

---

## Document Templates

### Business Letter

```markdown
# {Document Title}

status: draft
author: {anima_name}
date: {YYYY-MM-DD}
type: business-letter

## Recipient

{Recipient formal name}
{Department / Title}
{Contact name}

## Body

{Body text}

## Signature

{Signature block}
```

### Report

```markdown
# {Report Title}

status: draft
author: {anima_name}
date: {YYYY-MM-DD}
type: report

## Summary

{1–3 sentence abstract}

## Details

{Body text}

## Attachments

{If applicable}
```

---

## Constraints

- NEVER deliver documents containing confidential information externally without human approval
- MUST confirm corporate information (address, representative name, registration number, etc.) with the human before including it
- MUST verify every page after PDF generation
- NEVER deliver documents externally before human approval
