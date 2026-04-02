# COO (Chief Operating Officer) Team — Overview

## Single-Role Composition (team-of-one / human-supervised)

| Role | Responsibility | Recommended `--role` | `speciality` example | Details |
|------|---------------|---------------------|---------------------|---------|
| **COO** | Delegation decisions, department monitoring (machine), KPI aggregation (machine), executive reporting (machine), cross-department coordination | `manager` | `coo` | `coo/coo/` |

**Fundamental characteristic: The COO is the command tower of the Anima organization, responsible for two axes — "subordinate management" and "aggregated executive reports to the human."**

Unlike other team templates (development, legal, finance, etc.) that own specific business domains, the COO's domain is "organizational operations itself." Rather than executing specific tasks, the COO's primary duties are cross-department coordination, delegation decisions, performance monitoring, and reporting to the human.

The role directory contains `injection.template.md` (injection.md template), `machine.md` (organizational analysis & KPI aggregation pipeline), and `checklist.md` (quality checklist).

> Core principles: `team-design/guide.md`

## Operational Scale

- Current: Solo operation (1 person)
- Span of control: Up to {max_direct_reports} direct reports (default guideline: 10)
- Scale trigger: When direct reports exceed {max_direct_reports}, or when the number of departments grows beyond what one person can monitor
- Scaled composition: COO + VP (sharing oversight of department groups)

## Operational Modes

### Governance mode (subordinate management)

```
Assess situation via org_dashboard / audit_subordinate
  → machine performs organizational analysis (saves context)
    → On anomaly detection:
      Instruct direct reports via delegate_task / send_message
      Escalate critical issues to human via call_human
    → Normal:
      Wait until next review cycle
```

### Reporting mode (executive reporting)

```
Collect statistics from activity_log / org_dashboard
  → machine aggregates KPIs + drafts report
    → COO verifies and adds judgment commentary
      → Report to human via call_human
      → Request PDF formatting from secretary if needed
```

### Coordination mode (cross-department coordination)

```
Detect cross-department issues (heartbeat / subordinate reports)
  → COO decides:
    Finance-related → Coordinate with finance leader via send_message
    Legal-related → Coordinate with legal leader via send_message
    Overall policy → Escalate to human
    Execution tasks → delegate_task to appropriate department leader
```

## Communication Paths

```
Human ←── call_human ──── COO (Anima)
                            ├── Direct reports (department leaders)
                            │     ├── {Dev Lead} → Dev team
                            │     ├── {CS Lead} → CS team
                            │     └── ...
                            ├── Top-level peers
                            │     ├── Secretary (PDF requests, info sharing)
                            │     ├── CFO / Finance (financial reports, budget approval)
                            │     └── Legal Director (compliance checks)
                            └── Internal Audit (independent: receive audit reports only)
```

| Direction | Method | Purpose |
|-----------|--------|---------|
| Human → COO | Chat (Web UI) | Executive directives, policy confirmation |
| COO → Human | `call_human` | Executive reports, approval requests, escalation |
| COO → Direct reports | `delegate_task` / `send_message` | Task delegation, progress checks, instructions |
| Direct reports → COO | `send_message` (Inbox) | Progress reports, escalation |
| COO → Top-level peers | `send_message` | Cross-department coordination, info sharing |
| COO → Secretary | `send_message` | PDF formatting requests, info sharing |
| COO → All | `post_channel` | Organization-wide announcements (Board) |

## Delegation Criteria

| Impact \ Urgency | High (same-day) | Medium (within days) | Low (weekly) |
|------------------|-----------------|---------------------|--------------|
| **High** (executive / financial / legal impact) | Escalate to human | COO decides, negotiate with top members (finance/legal) | COO decides, delegate to relevant department |
| **Medium** (cross-department / multi-team) | COO coordinates directly | Delegate to department leader | Delegate to department leader |
| **Low** (single department) | Delegate to department leader | Delegate to department leader | Review at next cycle |

**Decision principles:**
- Decisions affecting the human must be escalated via call_human
- Issues involving finance or legal require consensus with top-level members
- Issues contained within a single department are delegated to the department leader (skip-level instructions prohibited)

## Span of Control Management

| Parameter | Default | Notes |
|-----------|---------|-------|
| max_direct_reports | 10 | Upper limit for direct reports. Propose org restructuring to human when exceeded |

- Automatically check direct report count during heartbeat
- On exceeding: Propose organizational restructuring (e.g., adding VP) to human via `call_human`
- Temporary exceeding (e.g., during onboarding) is acceptable, but sustained exceeding should be avoided

## Routing Rules

Never issue instructions directly to members under direct reports (NEVER). Always route through department leaders.

| Category | Route to | Notes |
|----------|----------|-------|
| Development / Technical | {Dev Lead name} | Direct instructions to engineers prohibited |
| CS / Customer-facing | {CS Lead name} | |
| Infrastructure / Monitoring | {Infra Lead name} | |
| {Category} | {Leader name} | Configure at deployment |

## Top-Level Peer Collaboration

| Peer | Collaboration Pattern | Purpose |
|------|----------------------|---------|
| Secretary | COO → Secretary: PDF formatting, external send requests / Secretary → COO: triage result distribution | Human-facing documents go through secretary for formatting & delivery |
| CFO / Finance Leader | COO ↔ Finance: budget approval, settlement review, investment decisions | Consensus required for financially impactful decisions |
| Legal Director | COO ↔ Legal: compliance checks, contract review | Consensus required for legally risky decisions |
| Internal Audit | Audit → COO: receive audit reports only (COO intervention in audit prohibited) | Independence guarantee |

## Scaling

| Scale | Composition | Notes |
|-------|-------------|-------|
| Solo | COO × 1 (this template) | Up to {max_direct_reports} direct reports |
| COO + VP | COO + 1–2 VPs | VPs share oversight of department groups. COO focuses on overall policy & human reporting |

## Cron Configuration Examples

Reference examples for deployment. Adjust to organizational scale and business cycles.

| Task | Schedule example | Type | Summary |
|------|-----------------|------|---------|
| Morning activity digest | `0 9 * * *` | llm | Aggregate all Anima activity for the past 24h, report to human via call_human |
| Daily subordinate audit | `0 15 * * *` | llm | Check all direct reports via org_dashboard + audit_subordinate, record in knowledge/ |
| Board meeting open | `0 9 * * *` | llm | Post agenda to #board |
| Board meeting summary | `0 11 * * *` | llm | Summarize #board discussions, escalate to human if needed |
| Evening priority triage | `30 21 * * *` | llm | Triage incomplete tasks, organize next-day priorities |
| Weekly org retrospective | `0 17 * * 5` | llm | Create weekly summary from episodes/, record in knowledge/ |

## Cross-Team Role Mapping

| Dev Team Role | Legal Team Role | COO Role | Reason |
|---------------|----------------|----------|--------|
| PdM (planning & decisions) | Director (analysis planning & decisions) | COO (delegation decisions & monitoring) | Judgment + planning as primary duties |
| — | Director + machine | COO + machine (org analysis, KPIs, reports) | Machine handles analysis & aggregation |
| — | — | COO (cross-department coordination) | **COO-specific. No counterpart in other teams** |
| — | — | COO (executive reporting) | **COO-specific. No counterpart in other teams** |
