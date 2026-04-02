# COO — Machine Usage Patterns

## Ground Rules

1. **Write the plan first** — Clarify the analysis purpose before submitting to machine. Analysis without purpose is prohibited
2. **Output is a draft** — Machine output is analytical material, not a final decision. COO must add judgment before reporting
3. **Save location**: `state/plans/{YYYY-MM-DD}_{summary}.{type}.md` (`/tmp/` prohibited)
4. **Rate limit**: chat 5 calls/session, heartbeat 2 calls
5. **Machine cannot access infrastructure** — Include required data (org_dashboard output, activity_log data, etc.) in the instruction

---

## Overview

The COO's primary duties are delegation decisions, department monitoring, and executive reporting. Organizational analysis, KPI aggregation, and report drafting are delegated to machine.

- Structured analysis of organizational status → machine analyzes, COO decides
- KPI aggregation and statistics extraction → machine aggregates, COO verifies
- Human-facing report creation → machine drafts, COO adds judgment commentary

**COO must make the judgment themselves (MUST). Never report machine output directly to the human.**

---

## Phase A: Organizational Analysis

### Step 1: Identify analysis targets

Obtain org_dashboard / audit_subordinate output and determine the scope:
- Periodic overall status analysis (daily/weekly)
- Anomaly detection in specific departments (STALE tasks, rising error rates, etc.)
- Cross-department bottleneck identification

### Step 2: Write analysis plan

```markdown
# Organizational Analysis Plan

status: draft
author: {anima_name}
date: {YYYY-MM-DD}
type: org-analysis

## Analysis Purpose
{What do you want to clarify?}

## Target Departments
{All / specific department names}

## Analysis Period
{Past 24h / past week / specific date range}

## Input Data
{org_dashboard output, audit_subordinate results, activity_log excerpts, etc.}

## Analysis Perspectives
- Task completion status (STALE / OVERDUE presence)
- Errors/incidents and their impact scope
- Cross-department dependencies and blocking
- Resource imbalance (load concentrated on specific members, etc.)
```

### Step 3: Submit to machine

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{plan_file})" \
  -d /path/to/workspace
```

Save results as `state/plans/{date}_{summary}.org-analysis.md`.

### Step 4: COO reviews and decides

Review machine analysis results and add:
- Action decisions for anomalies (delegate / escalate / observe)
- Explicit reasoning for each decision
- Instructions to direct reports if needed (delegate_task / send_message)

---

## Phase B: KPI Aggregation

### Step 5: Write aggregation instructions

```markdown
# KPI Aggregation Instructions

status: draft
author: {anima_name}
date: {YYYY-MM-DD}
type: kpi-summary

## Aggregation Purpose
{Periodic report / specific issue analysis}

## Aggregation Period
{Past 24h / past week / monthly}

## Input Data
{activity_log excerpts, task_queue statistics, org_dashboard figures, etc.}

## Metrics
- Activity volume by department (tool_use count, message send/receive count)
- Task completion rate (done / in-progress / STALE / OVERDUE)
- Error rate (error-type activities / total activities)
- Response time by department (average DM receive-to-reply time)
- {Additional organization-specific KPIs}
```

### Step 6: Submit to machine

Submit aggregation based on instructions.
Save results as `state/plans/{date}_{summary}.kpi-summary.md`.

### Step 7: COO verifies

Verify machine aggregation results:
- [ ] Aggregation period is correct
- [ ] No obvious anomalies in numbers (wrong magnitude, negative values, etc.)
- [ ] All departments are covered

---

## Phase C: Report Drafting

### Step 8: Write report instructions

Using Phase A + B results as input, instruct drafting of a human-facing report.

```markdown
# Report Draft Instructions

status: draft
author: {anima_name}
date: {YYYY-MM-DD}
type: report-draft

## Report Type
{Daily digest / weekly retrospective / monthly strategic review / ad-hoc report}

## Input
- Organizational analysis: state/plans/{org-analysis file}
- KPI summary: state/plans/{kpi-summary file}

## Report Format
### Executive Summary (3–5 lines)
{Overall status, concise}

### Department Details
{Key topics per department}

### Concerns & Risks
{Issues requiring attention, items needing escalation}

### Action Items
{Actions COO will take or plans to take}
```

### Step 9: Submit to machine

Save results as `state/plans/{date}_{summary}.report-draft.md`.

### Step 10: COO adds judgment commentary

Add the following to the machine draft (MUST):
- COO's own situational assessment and observations
- Action item proposals for the human
- Explicit notation of items requiring escalation

### Step 11: Report and distribute

- Report to human via `call_human`
- Request PDF formatting from secretary (`send_message`) when formal documents are needed

---

## Constraints

- Organizational analysis "judgment" must be made by the COO (MUST). Do not treat machine output as final decisions
- Human reports must always include COO's own judgment commentary (MUST)
- Redact or mask personal/confidential information in machine output before external distribution (MUST)
- Never alter audit results before reporting (NEVER). Maintain internal audit independence
