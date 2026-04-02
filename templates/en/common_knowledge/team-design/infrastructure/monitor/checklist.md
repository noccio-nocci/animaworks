# Infrastructure Monitor — Quality Checklist

Since machine is not used, this checklist ensures quality of monitoring execution, report accuracy, and anomaly detection.

---

## A. Monitoring Execution

- [ ] Executed all monitoring items defined in cron
- [ ] No failed items (if any failed, reported as anomaly)
- [ ] Detected any monitoring command timeouts or connection errors

---

## B. Report Quality

- [ ] All check items have recorded values and thresholds (not just "no issues")
- [ ] Report follows the regular monitoring report template format
- [ ] Summary overall status (✅ / ⚠️ / 🔴) is consistent with monitoring results

---

## C. Previously Unresolved Items

- [ ] All previously unresolved items carried forward (zero silent drops)
- [ ] Status updated for each unresolved item (resolved / continuing / deteriorated)
- [ ] Resolved items include basis for resolution

---

## D. Anomaly Detection

- [ ] No threshold exceedances overlooked
- [ ] Severity assessments (INFO / WARNING / CRITICAL) comply with escalation threshold table
- [ ] Sent anomaly detection report to Director immediately on WARNING / CRITICAL detection

---

## E. Initial Response

- [ ] If recovery procedure was executed, results are included in the anomaly detection report
- [ ] Did not attempt self-recovery on anomalies with unknown procedures (reporting to Director only is the rule)
- [ ] Clearly stated whether initial response was performed and its outcome
