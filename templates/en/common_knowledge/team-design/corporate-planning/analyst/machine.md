# Business Analyst — machine usage patterns

## Ground rules

1. **Write the plan document first** — Do not run on a short inline prompt string. Pass a plan file.
2. **Output is draft** — Always validate machine output yourself before `status: approved` for the next step.
3. **Save location**: `state/plans/{YYYY-MM-DD}_{summary}.{type}.md` (no `/tmp/`)
4. **Rate limits**: chat 5/session, heartbeat 2
5. **Machine has no infra access** — Put memory, messaging, and org context into the plan document.

---

## Overview

Business Analyst structures and analyzes raw data collected via external tools (`web_search`, `x_search`, etc.) on machine.

- Structuring plan → Analyst writes
- Data collection via external tools → Analyst runs
- Structuring and analysis of collected data → delegate to machine; Analyst validates
- Source citations → Analyst final check

---

## Phase A: Data structuring

### Step 1: Collect raw data

Per the Strategist’s request, collect raw data with `web_search` / `x_search` or other external tools.

### Step 2: Create the structuring plan (Analyst writes)

Create a plan that states structuring purpose, target data, and classification axes.

```bash
write_memory_file(path="state/plans/{date}_{topic}.structuring-plan.md", content="...")
```

### Step 3: Run data structuring on machine

Pass collected raw data + structuring plan as input and ask machine to structure the data.

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{structuring-plan.md})" \
  -d /path/to/workspace
```

Machine runs:
- Classification and bucketing
- Trend extraction
- Statistical summary

Save as `state/plans/{date}_{topic}.market-analysis.md` (`status: draft`).

### Step 4: Validate `market-analysis.md`

Read `market-analysis.md` against `analyst/checklist.md`:

- [ ] Every item has a source (URL, date)
- [ ] Facts vs interpretation are separated
- [ ] No machine-invented gap-filling

Fix yourself, then set `status: approved`.

---

## Phase B: Competitor analysis

### Step 5: Collect competitor information

Gather fragmentary data on multiple competitors (product, pricing, features, org, etc.).

### Step 6: Run competitor analysis on machine

Pass collected competitor data as input and ask machine for structured competitor analysis.

Machine produces:
- Comparison matrix (features, pricing, market position)
- Strengths/weaknesses per competitor
- Positioning map

Save as `state/plans/{date}_{topic}.competitive-report.md` (`status: draft`).

### Step 7: Validate `competitive-report.md`

Read `competitive-report.md` against `analyst/checklist.md`.
Confirm accuracy and source quality, then set `status: approved`.

---

## Template: market analysis report (`market-analysis.md`)

```markdown
# Market analysis report: {topic}

status: draft
author: {anima-name}
date: {YYYY-MM-DD}
type: market-analysis
source: {path to Strategist research request}

## Research summary

- Items researched: {N}
- High-confidence sources: {N} / medium: {N} / unverified: {N}

## Sources

| # | Source | URL | Retrieved | Confidence |
|---|--------|-----|-----------|------------|
| 1 | {name} | {URL} | {date} | High/Med/Low |

## Market trends

{Overall market trend analysis}

## Segment analysis

{Per-segment analysis}

## Key findings

{Important findings that affect Strategist judgment}

## Open items

| # | Item | Why open | Recommended next step |
|---|------|----------|-------------------------|
| 1 | {item} | {reason} | {next step} |

## Self-check

- [ ] All items sourced
- [ ] Facts vs interpretation separated
- [ ] Data freshness stated
```

## Template: competitor analysis report (`competitive-report.md`)

```markdown
# Competitor analysis report: {topic}

status: draft
author: {anima-name}
date: {YYYY-MM-DD}
type: competitive-report

## Comparison matrix

| Item | Us | Competitor A | Competitor B | Competitor C |
|------|-----|--------------|----------------|--------------|
| {feature 1} | {rating} | {rating} | {rating} | {rating} |

## Per-company analysis

### {competitor name}

- **Strengths**: {analysis}
- **Weaknesses**: {analysis}
- **Market position**: {analysis}
- **Recent moves**: {analysis}
- **Sources**: {URL, date}

## Positioning

{Positioning analysis in the market}

## Key findings

{Competitor dynamics that affect Strategist judgment}
```

---

## Constraints

- NEVER deliver machine output to the Strategist without Analyst validation
- MUST include source-citation instructions to machine
- NEVER fill unknowns with guesses — make open items explicit
- NEVER send `market-analysis.md` to the Strategist without `status: approved`
