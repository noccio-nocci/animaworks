# Corporate Strategist — machine usage patterns

## Ground rules

1. **Write the plan document first** — Do not run on a short inline prompt string. Pass a plan file.
2. **Output is draft** — Always validate machine output yourself before `status: approved` for the next step.
3. **Save location**: `state/plans/{YYYY-MM-DD}_{summary}.{type}.md` (no `/tmp/`)
4. **Rate limits**: chat 5/session, heartbeat 2
5. **Machine has no infra access** — Put memory, messaging, and org context into the plan document.

---

## Overview

Corporate Strategist combines PdM (planning and judgment) and Engineer (execution).

- Analysis plan (`strategic-plan.md`) → Strategist writes
- Business environment analysis execution → delegate to machine; Strategist validates
- Risk judgment finalization → Strategist decides
- Two validation passes: machine analysis output, then Coordinator feedback integration

---

## Phase A: Business environment analysis

### Step 1: Review the Analyst’s market analysis report

Receive `market-analysis.md` (`status: approved`) from the Analyst and understand the content.

### Step 2: Create `strategic-plan.md` (Strategist writes)

Create a plan that states purpose, subject, framework choice, and where internal data lives.

```bash
write_memory_file(path="state/plans/{date}_{topic}.strategic-plan.md", content="...")
```

**The “analysis purpose,” “framework selection,” and “scope” sections in `strategic-plan.md` are core Strategist judgment — NEVER have machine write them.**

### Step 3: Run business environment analysis on machine

Pass `strategic-plan.md` + `market-analysis.md` as input and ask machine for structured business environment analysis.

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{strategic-plan.md})" \
  -d /path/to/workspace
```

Analysis machine runs:
- Framework analysis (PEST, SWOT, Five Forces, etc.)
- Extraction of “winnable areas”
- Prioritization of opportunities and threats

Save the result as `state/plans/{date}_{topic}.strategy-report.md` (`status: draft`).

### Step 4: Validate `strategy-report.md`

Read `strategy-report.md` and check against `strategist/checklist.md` section A.
Fix issues yourself, then set `status: reviewed`.

---

## Phase B: Strategic proposal draft

### Step 5: Ask machine for a strategic proposal draft

Pass Phase A results + OKRs as input and ask machine for a strategic proposal draft.

Machine produces:
- Goals and initiative list
- Resource allocation proposal
- Risk analysis

Save as `state/plans/{date}_{topic}.strategic-proposal.md` (`status: draft`).

### Step 6: Validate the strategic proposal

Read `strategic-proposal.md` against `strategist/checklist.md` section B.
Check alignment with OKRs, feasibility of initiatives, and soundness of resource allocation.

---

## Phase C: Initiative progress analysis

### Step 7: Ask machine for progress analysis

Pass Strategic Initiative Tracker data as input and ask machine for progress analysis.

Machine runs:
- Detect stalled initiatives (no stage change for 1+ month)
- Assess KPI attainment outlook
- Bottleneck analysis

### Step 8: Validate progress analysis and decide

Read the analysis and decide per initiative:
- **Continue**: on track
- **Revise**: change initiatives
- **Cancel**: record rationale and remove from Tracker

Confirm full Tracker updates per `strategist/checklist.md` section C.

---

## Template: strategic plan (`strategic-plan.md`)

```markdown
# Strategic analysis plan: {topic}

status: draft
author: {anima-name}
date: {YYYY-MM-DD}
type: strategic-plan

## Analysis purpose

{What to clarify — 1–3 sentences}

## Input data

| Data | Source | Notes |
|------|--------|-------|
| Market analysis report | Analyst: market-analysis.md | {path} |
| Internal data | {source} | {summary} |

## Framework selection

{Chosen by Strategist judgment}

- {framework 1: e.g. PEST}
- {framework 2: e.g. SWOT}

## Analysis scope

{What is in scope and what is excluded}

## Deliverable format

- Extraction and prioritization of “winnable areas”
- Opportunity/threat assessment matrix
- Strategic options

## Deadline

{deadline}
```

## Template: strategy report (`strategy-report.md`)

```markdown
# Strategy analysis report: {topic}

status: draft
author: {anima-name}
date: {YYYY-MM-DD}
type: strategy-report
source: state/plans/{source strategic-plan.md}

## Executive summary

{Business environment assessment — 1–3 sentences}

## Framework analysis results

### {framework name}

{Findings}

## “Winnable areas”

| # | Area | Basis | Priority | Risk |
|---|------|-------|----------|------|
| 1 | {area} | {basis} | High/Med/Low | {risk summary} |

## Opportunity / threat assessment

| # | Item | Type | Impact | Response |
|---|------|------|--------|----------|
| 1 | {item} | Opportunity/Threat | High/Med/Low | {approach} |

## Additional comments

{Strategist notes and supplements}
```

## Template: strategic proposal (`strategic-proposal.md`)

```markdown
# Strategic proposal: {topic}

status: draft
author: {anima-name}
date: {YYYY-MM-DD}
type: strategic-proposal

## Alignment with OKRs

{Relationship between target OKRs and this proposal}

## Initiative list

| # | Initiative | Goal | Resources | Due | Risk |
|---|------------|------|-----------|-----|------|
| 1 | {name} | {target} | {resources needed} | {due} | {risk summary} |

## Resource allocation

{Overall resource allocation approach}

## Risk analysis

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|------------|------------|
| 1 | {risk} | High/Med/Low | High/Med/Low | {mitigation} |
```

---

## Constraints

- `strategic-plan.md` MUST be written by the Strategist
- Risk judgments in `strategy-report.md` MUST be finalized by the Strategist (treat machine output as draft)
- NEVER hand `strategy-report.md` to the Coordinator without `status: reviewed`
- NEVER let a tracked initiative disappear without mention (NEVER — silent drop forbidden)
