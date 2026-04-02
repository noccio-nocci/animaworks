# Infrastructure / SRE Monitoring Team — Team Overview

## Two-Role Structure

| Role | Responsibility | Recommended `--role` | `speciality` example | Details |
|------|---------------|---------------------|---------------------|---------|
| **Infra Director** | Report aggregation, anomaly assessment, escalation decisions, consolidated reporting | `ops` | `infra-director` | `infrastructure/director/` |
| **Monitor** | Periodic monitoring execution, anomaly detection, regular reporting, initial response (known procedures only) | `ops` | `infra-monitor-{target}` | `infrastructure/monitor/` |

This team **does not use machine (external agents)**. Quality assurance relies on periodic checks via cron/heartbeat and report templates. Based on the NOC (Network Operations Center) structure: L1 (Monitor) + L2/Manager (Director).

Each role directory contains `injection.template.md` (injection.md template) and `checklist.md` (quality checklist). There is no machine.md.

> Core principles: `team-design/guide.md` (see "Monitoring Team Pattern" section)

## Handoff Chain

```
Monitor (runs periodic checks via cron/heartbeat)
  → Normal: Regular monitoring report → Director via send_message (intent: report)
  → Anomaly: Anomaly detection report → Director via send_message (intent: report)
      ↓
Director (aggregates all Monitor reports)
  → False positive: Log only (record in knowledge/)
  → Action needed:
    ├─ Minor (WARNING): Record + verify at next monitoring cycle
    ├─ Severe (CRITICAL): Escalate to COO / dev team
    └─ Immediate: Notify human via call_human
      ↓
Director → Consolidated report to COO / human (periodic)
```

### Handoff Documents

| From → To | Document | Condition | Communication |
|-----------|----------|-----------|---------------|
| Monitor → Director | Regular monitoring report | Every cron cycle | `send_message (intent: report)` |
| Monitor → Director | Anomaly detection report | On anomaly detection (immediate) | `send_message (intent: report)` |
| Director → COO / human | Consolidated report | Periodic (daily, etc.) | `send_message (intent: report)` or `call_human` |
| Director → Dev team | Incident escalation | On CRITICAL assessment | `send_message (intent: report)` |

### Escalation Criteria (3 Levels)

| Level | Condition | Monitor Action | Director Action |
|-------|-----------|---------------|-----------------|
| **INFO** | `{within normal range}` | Include in regular report | Log only |
| **WARNING** | `{requires attention}` | Send anomaly detection report to Director immediately | Record + monitor at next cycle. Consider escalation if recurring |
| **CRITICAL** | `{immediate action required}` | Send anomaly detection report to Director immediately | Escalate to COO / dev team + notify human via call_human |

Specific thresholds are set at deployment time via the `{escalation thresholds}` parameter.

### Operational Rules

- **Silent drop prevention**: Carry forward all unresolved items in the "Previously Unresolved Items" section of report templates. Items that were WARNING/CRITICAL in the previous report must not disappear without mention
- **Recovery confirmation**: CRITICAL incidents must continue to be reported as unresolved until recovery is confirmed
- **False positive logging**: Even when Director judges a false positive, record it in knowledge/ as reference for threshold adjustments

## Monitor Parameterization

The Monitor template can create multiple instances with these parameters:

| Parameter | Description | Examples |
|-----------|-------------|---------|
| `{monitoring target}` | System/domain the Monitor is responsible for | AWS cloud infrastructure, internal network, application |
| `{monitoring items table}` | List of check targets (item, method, threshold, criteria) | EC2 status, disk usage, SSL certificate expiry |
| `{escalation thresholds}` | Specific conditions for INFO/WARNING/CRITICAL | 80% WARNING / 95% CRITICAL |

By substituting parameters in `injection.md` from the same template, you can create domain-specific Monitors for cloud, network, application, etc.

## Report Templates

### Regular Monitoring Report Template (Monitor → Director)

```markdown
# Regular Monitoring Report: {monitoring target} — {datetime}

## Summary
- Overall status: ✅ Normal / ⚠️ Caution / 🔴 Anomaly
- Check items: {N} / Anomalies detected: {M}

## Previously Unresolved Items (carry-forward)
| # | First detected | Target | Severity | Current status | Notes |
|---|---------------|--------|----------|---------------|-------|
(If none, state "No unresolved items")

## Current Monitoring Results
| Check item | Result | Value | Threshold | Assessment |
|-----------|--------|-------|-----------|------------|

## Newly Detected Issues
(Describe anomalies if any. Otherwise "No new detections")

## Actions
- Escalation: {target and reason} (if applicable)
- Next check items: {details} (if applicable)
```

### Anomaly Detection Report Template (Monitor → Director, immediate)

```markdown
# Anomaly Detection Report: {monitoring target} — {detection datetime}

## Overview
- Detected item: {item name}
- Severity: WARNING / CRITICAL
- Detected value: {value} (threshold: {threshold})

## Impact Scope
{Overview of affected services/systems}

## Actions Taken
{Initial response performed by Monitor. "None" if not applicable}

## Recommended Actions
{Recommended response for Director. Suggested escalation targets, etc.}
```

### Consolidated Report Template (Director → COO / human)

```markdown
# Infrastructure Consolidated Report — {reporting period}

## Overall Status
- ✅ Normal: {N} targets
- ⚠️ Caution: {N} targets
- 🔴 Anomaly: {N} targets

## Unresolved Items
| # | First detected | Target | Monitor | Severity | Status | Next action |
|---|---------------|--------|---------|----------|--------|-------------|
(If none, "All targets normal")

## Incident Summary for Period
| Datetime | Target | Severity | Resolution | Duration |
|----------|--------|----------|-----------|----------|
(If none, "No incidents")

## Observations
{Director's assessment: trend analysis, threshold adjustment proposals, risk evaluation, etc.}
```

## Cron/Heartbeat Configuration Examples

Specific monitoring commands and targets are configured at deployment. Below are structural examples:

### Monitor Cron Examples

| Task | Schedule example | Type | Description |
|------|-----------------|------|-------------|
| Periodic monitoring check | `*/30 * * * *` | command | Execute monitoring items and log results |
| Regular report | `0 */6 * * *` | llm | Aggregate recent monitoring results and send regular report to Director |
| Certificate expiry check | `0 9 * * 1` | command | Check remaining days for SSL/TLS certificates |

### Director Cron Examples

| Task | Schedule example | Type | Description |
|------|-----------------|------|-------------|
| Morning consolidated report | `0 9 * * *` | llm | Aggregate latest reports from all Monitors and send consolidated report to COO/human |
| Afternoon status check | `0 17 * * *` | llm | Check progress on unresolved items, organize notes for next day |
| Weekly trend analysis | `0 10 * * 1` | llm | Analyze weekly anomaly trends and determine if threshold adjustments are needed |

## Scaling

| Scale | Composition | Notes |
|-------|-------------|-------|
| Solo | Single Monitor also serves as Director (quality ensured by checklist) | When monitoring targets are few; reports directly to COO |
| Pair | Director + 1 Monitor (minimum composition for this template) | Base configuration. Monitor covers one domain |
| Team | Director + multiple Monitors (by domain) | Add Monitors as monitoring targets expand. e.g. cloud, network, app |
| Scaled | Director + many Monitors (subdivided by service) | e.g. cloud-1 (AWS), cloud-2 (GCP), app-frontend, app-backend, etc. |

## Role Mapping to Other Teams

| Development Team | Legal Team | Finance Team | Infrastructure Team | Rationale |
|-----------------|------------|-------------|-------------------|-----------|
| PdM (planning/decisions) | Director (analysis planning/decisions) | Director (analysis planning/decisions) | Infra Director (decisions/aggregation) | Command center that aggregates reports and makes judgments |
| Engineer (implementation) | Director + machine | Director + machine | — | **Infrastructure team does not use machine** |
| Reviewer (static verification) | Verifier (independent verification) | Auditor (independent verification) | — | Independent verification role unnecessary for monitoring team |
| Tester (dynamic verification) | Researcher (evidence verification) | Analyst/Collector | Monitor (monitoring execution) | Retrieves external data and reports |
