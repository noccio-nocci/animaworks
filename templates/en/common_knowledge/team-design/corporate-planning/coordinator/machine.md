# Strategy Coordinator — machine usage patterns

## Ground rules

1. **Write the plan document first** — Do not run on a short inline prompt string. Pass a plan file.
2. **Output is draft** — Always validate machine output yourself before `status: approved` for the next step.
3. **Save location**: `state/plans/{YYYY-MM-DD}_{summary}.{type}.md` (no `/tmp/`)
4. **Rate limits**: chat 5/session, heartbeat 2
5. **Machine has no infra access** — Put memory, messaging, org context into the plan document.

---

## Overview

The Coordinator **delegates verification scans to machine and meta-validates those results**.

- Verification focus design → Coordinator judgment
- Assumption checks, KPI alignment, Tracker cross-check execution → delegate to machine
- Validity of findings → Coordinator judgment
- Final feasibility judgment → Coordinator judgment

Machine can quickly check data consistency, logic of assumptions, and Tracker alignment;
holistic feasibility and organizational constraints stay with the Coordinator.

---

## Workflow

### Step 1: Create the verification plan (Coordinator writes)

Create a plan that states verification lenses, targets, and criteria.

```bash
write_memory_file(path="state/plans/{date}_{topic}.verification.md", content="...")
```

Prepare on the Anima side before writing:
- Strategist’s `strategy-report.md` and `strategic-plan.md`
- Strategic Initiative Tracker (for comparison vs last time)
- Related KPI data (from departments)

### Step 2: Run verification scan on machine

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{verification.md})" \
  -d /path/to/workspace
```

Save as `state/plans/{date}_{topic}.verification-result.md` (`status: draft`).

### Step 3: Meta-validate verification results

Read `verification-result.md` and confirm:

- [ ] Assumption-challenge results are logical (machine hits the mark)
- [ ] KPI alignment checks use accurate data sources
- [ ] Tracker cross-check has no gaps
- [ ] No false positives
- [ ] Nothing missing from the Coordinator’s own lens

Edit and supplement yourself; add final feasibility judgment.

### Step 4: Create `verification-report.md`

Consolidate meta-validated results into `verification-report.md` and set `status: approved`.
Send approved `verification-report.md` to the Strategist.

---

## Template: verification plan (`verification-plan.md`)

```markdown
# Verification plan: {verification target summary}

status: draft
author: {anima-name}
date: {YYYY-MM-DD}
type: verification-plan

## Verification lenses

- [ ] Assumption challenge: adversarial check of Strategist premises
- [ ] KPI alignment: gap between departmental KPI reality and strategic targets
- [ ] Tracker cross-check: every Strategic Initiative Tracker row updated
- [ ] Source validation: trustworthiness of market analysis sources
- [ ] Feasibility: fit with resources, timeline, org structure

## Targets

- strategy-report.md: {path}
- strategic-plan.md: {path}
- Strategic Initiative Tracker: {path}
- KPI data: {source / location}

## Required output format

Use the following format for results. **Output that does not follow this format is invalid.**

- **Critical**: must-fix (assumption failure, KPI gap, silent drop)
- **Warning**: should-fix (weak evidence, stale data)
- **Info**: information and improvement ideas
```

## Template: verification report (`verification-report.md`)

```markdown
# Verification report: {topic}

status: draft
author: {anima-name}
date: {YYYY-MM-DD}
type: verification-report

## Overall outcome

{APPROVE / REQUEST_CHANGES / COMMENT}

## Assumption challenge results

| # | Assumption | Strategist basis | Finding | Worst case if wrong | Recommendation |
|---|------------|------------------|---------|---------------------|----------------|
| 1 | {assumption} | {basis} | {sound / weak / failed} | {if assumption breaks} | {fix} |

## KPI alignment check

| # | KPI | Strategic target | Actual | Gap | Verdict |
|---|-----|------------------|--------|-----|---------|
| 1 | {KPI name} | {target} | {actual} | {delta} | {OK / NG} |

## Tracker cross-check

| # | Initiative | Prior stage | Current stage | Stalled | Verdict |
|---|------------|-------------|---------------|---------|---------|
| 1 | {name} | {prior} | {current} | {Y/N} | {OK / action needed} |

## Coordinator notes

{Coordinator analysis, extra observations, recommendations}
- Overall feasibility assessment
- Organizational constraints
- Notes when communicating initiatives to departments
```

---

## Constraints

- Verification plan (what to verify) MUST be written by the Coordinator
- NEVER forward machine verification results to the Strategist without Coordinator meta-validation
- NEVER send `verification-report.md` without `status: approved`
- Final feasibility judgment MUST be made by the Coordinator, not machine
