# CS Lead — Machine Usage Patterns

## Ground rules

1. **Write a plan first** — Do not run machine with inline short instructions. Pass a plan document
2. **Output is a draft** — Always verify machine output yourself; set `status: approved` before passing downstream
3. **Save location**: `state/plans/{YYYY-MM-DD}_{summary}.{type}.md` (`/tmp/` forbidden)
4. **Rate limit**: chat 5 calls/session, heartbeat 2 calls
5. **Machine cannot access infrastructure** — Include memory, messages, and org info in the plan document

---

## Overview

CS Lead combines PdM (planning & judgment) and Engineer (execution). Machine is used in four phases.

- Phase A: Analyze cs-handoff.md and draft onboarding plan → CS Lead verifies
- Phase B: Analyze Health Tracker + inquiry history, predict churn & recommend intervention → CS Lead decides
- Phase C: Produce retention actions & response content → CS Lead verifies
- Phase D: Aggregate VoC (Voice of Customer) and produce product feedback report → CS Lead finalizes

---

## Phase A: Onboarding Analysis & Planning

### Step 1: Receive and review cs-handoff.md

Receive `cs-handoff.md` (`status: draft`) from Sales Director. Review all sections (customer overview, sales process summary, agreements, unresolved items, communication characteristics).

### Step 2: Write the onboarding request (CS Lead writes this)

Create a request document specifying onboarding goals, customer-specific focus areas, and scope.

```bash
write_memory_file(path="state/plans/{date}_{company}.onboarding-request.md", content="...")
```

**The "goals", "focus areas", and "scope" are the CS Lead's judgment core and must NEVER be written by machine.**

### Step 3: Send onboarding planning to machine

Pass the request + cs-handoff.md content as input; ask machine to draft the onboarding plan.

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{onboarding-request.md})" \
  -d /path/to/workspace
```

Save as `state/plans/{date}_{company}.onboarding-plan.md` (`status: draft`).

### Step 4: Verify onboarding-plan.md

CS Lead verifies using checklist section A:
- [ ] All cs-handoff.md items covered
- [ ] Agreements/requests translated into concrete steps
- [ ] Unresolved items have response plans
- [ ] Communication characteristics considered

Fix issues yourself and set `status: approved`.

### Step 5: Delegate to Support

Pass `onboarding-plan.md` (`status: approved`) to Support via `delegate_task`.

---

## Phase B: Customer Health Analysis

### Step 6: Write the health analysis request (CS Lead writes this)

Create a request document with current Health Tracker state + recent inquiry history.

```bash
write_memory_file(path="state/plans/{date}_health-analysis-request.md", content="...")
```

### Step 7: Send health analysis to machine

Pass the request as input; ask machine to compute health scores, predict churn, and recommend interventions.

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{health-analysis-request.md})" \
  -d /path/to/workspace
```

Save as `state/plans/{date}_health-analysis.md` (`status: draft`).

### Step 8: Decide based on analysis

CS Lead reviews the analysis and decides:
- Green → Monitor. Update Health Tracker
- Yellow → Draft retention action in Phase C
- Red → Immediately proceed to Phase C + escalate upward

**Final health score determination is made by CS Lead (machine output is verified as a draft).**

---

## Phase C: Response Content Production

### Step 9: Write the response request (CS Lead writes this)

Create a request specifying the customer, situation, and objective.

```bash
write_memory_file(path="state/plans/{date}_{company}.retention-request.md", content="...")
```

**Response approach, tone, and objectives are the CS Lead's judgment core and must NEVER be written by machine.**

### Step 10: Send content production to machine

Pass the request as input; ask machine to draft customized response content.

Target content examples:
- Retention strategy proposals
- Customer-facing improvement reports
- Escalation response summaries & proposals
- Custom support guides

### Step 11: Verify the output

CS Lead verifies using checklist section C:
- [ ] Customized appropriately for the customer's situation
- [ ] Tone is appropriate (considering communication characteristics)
- [ ] No compliance issues

Fix issues yourself.

---

## Phase D: VoC Aggregation & Product Feedback

### Step 12: Write the VoC request (CS Lead writes this)

Compile inquiry patterns, customer feedback, and Support reports for the target period.

```bash
write_memory_file(path="state/plans/{date}_voc-request.md", content="...")
```

### Step 13: Send VoC analysis to machine

Pass the request as input; ask machine to perform trend analysis, extract insights, and propose improvements.

Save as `state/plans/{date}_voc-report.md` (`status: draft`).

### Step 14: Finalize the VoC report

CS Lead verifies using checklist section D:
- [ ] Inquiry trends accurately reflected
- [ ] Improvement proposals backed by evidence
- [ ] COO report properly formatted

Set `status: approved` and send to COO via `send_message (intent: report)`.

---

## Document Templates

### onboarding-plan.md

```markdown
# Onboarding plan: {company name}

status: draft
author: {anima name}
date: {YYYY-MM-DD}
type: onboarding-plan
source: cs-handoff.md

## Customer overview (from cs-handoff.md)

{Summary of cs-handoff.md}

## Onboarding goals

{Goals to achieve — 1–3 items}

## Steps

| # | Step | Owner | Deadline | Completion criteria |
|---|------|-------|----------|---------------------|
| 1 | {description} | {Support/CS Lead} | {date} | {criteria} |

## Focus areas

{Focus areas based on agreements/requests from cs-handoff.md}

## Handling unresolved items

{Plans for unresolved items from cs-handoff.md}

## Communication approach

{Approach based on key person's characteristics}
```

### health-analysis.md

```markdown
# Customer health analysis: {period}

status: draft
author: {anima name}
date: {YYYY-MM-DD}
type: health-analysis

## Scope

| # | Company | Current score | Previous score | Change |
|---|---------|--------------|----------------|--------|
| CS-1 | {name} | {Green/Yellow/Red} | {previous} | {↑/→/↓} |

## Customers requiring attention

{Analysis and recommended actions for Yellow/Red customers}

## Churn prediction

{High churn-risk customers and supporting evidence}

## Recommended actions

| Priority | Company | Action | Rationale |
|----------|---------|--------|-----------|
| High | {name} | {specific action} | {rationale} |
```

### retention-action.md

```markdown
# Retention action: {company name}

status: draft
author: {anima name}
date: {YYYY-MM-DD}
type: retention-action
health_score: {Yellow/Red}

## Current situation

{Customer's current situation and challenges}

## Action plan

{Specific retention actions}

## Expected outcome

{Expected results after execution}

## Customer communication draft

{Draft email/proposal}
```

### voc-report.md

```markdown
# VoC report: {period}

status: draft
author: {anima name}
date: {YYYY-MM-DD}
type: voc-report
period: {YYYY-MM-DD} ~ {YYYY-MM-DD}

## Summary

{Key trends — 3–5 points}

## Inquiry trends

| Category | Count | Period-over-period | Representative content |
|----------|-------|-------------------|----------------------|
| {category} | {N} | {↑/→/↓} | {content} |

## Customer feedback analysis

### Positive

{Well-received points}

### Negative

{Complaints & issues}

## Improvement proposals

| # | Proposal | Rationale | Impact scope | Priority |
|---|----------|-----------|-------------|----------|
| 1 | {proposal} | {VoC data evidence} | {affected customers/segment} | {High/Medium/Low} |

## Next actions

{Actions requested from COO / dev team}
```

---

## Constraints

- CS Lead decides whether to accept cs-handoff.md (MUST)
- Final health score determination is made by CS Lead (machine output is verified as a draft)
- Response approach, tone, and objectives must NEVER be written by machine
- Health Tracker items must NEVER disappear without mention (NEVER — silent drop forbidden)
