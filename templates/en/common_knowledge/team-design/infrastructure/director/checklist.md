# Infra Director — Quality Checklist

Since machine is not used, this checklist ensures quality of report aggregation, assessment, and escalation.

---

## A. Report Aggregation

- [ ] Reviewed all reports from all Monitors without omission
- [ ] No unreceived Monitor reports (detected report delays)
- [ ] Each Monitor's reporting period is correct (no gaps from previous report)

---

## B. Anomaly Assessment

- [ ] Made true/false positive determination for each anomaly detection report
- [ ] Recorded the basis for each determination (including knowledge/ logging)
- [ ] Severity assessments (INFO / WARNING / CRITICAL) comply with escalation criteria
- [ ] Checked progress on items that were WARNING in previous cycle (deterioration / improvement / stable)

---

## C. Escalation

- [ ] No CRITICAL items overlooked
- [ ] Escalation targets are correct (COO / dev team / human)
- [ ] call_human sent where required (CRITICAL incidents, simultaneous multi-target anomalies)
- [ ] Escalation includes impact scope and recommended actions

---

## D. Consolidated Report Quality

- [ ] All unresolved items carried forward (zero silent drops)
- [ ] Status updated for all previously unresolved items
- [ ] Director's own observations (trend analysis, risk evaluation, threshold adjustment proposals) included
- [ ] Incident summary includes resolution results and duration

---

## E. False Positive Management

- [ ] False positives recorded in knowledge/
- [ ] Aware of items requiring threshold adjustment consideration
- [ ] If recurring false positive patterns exist, considered proposing threshold changes to Monitors
