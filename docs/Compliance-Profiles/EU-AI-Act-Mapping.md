# Compliance Profile: EU AI Act Mapping

**Version**: AIZP V0.6 (new chapter)
**EU AI Act Effective Date**: August 2, 2026 (high-risk AI systems obligations under Annex III)

This document maps AIZP capabilities to the EU AI Act's requirements for high-risk AI systems.

---

## 0. Regulatory Landscape (as of 2026-05)

AIZP is jurisdiction-neutral, but deployers should note the 2026 timing:

| Regime | Status (May 2026) | Relevance to AIZP |
|---|---|---|
| **EU AI Act** — high-risk obligations (Annex III) | **Effective 2026-08-02** | Art 12 logging, Art 14 human oversight, Art 15 robustness — AIZP events map directly (this document) |
| **Colorado AI Act (SB 24-205)** | **In flux** — original 2026-06-30 date; enforcement stayed 2026-04; replacement **SB 189** (notice-and-transparency only) passed 2026-05 | AIZP does **not** ship a Colorado profile while the law is being replaced; revisit once SB 189's final form is settled |
| **NIST AI RMF / ISO 42001** | Voluntary, stable | See [NIST-AI-RMF-Mapping.md](NIST-AI-RMF-Mapping.md), [ISO-42001-Mapping.md](ISO-42001-Mapping.md) |

**Honest note**: regulatory text changes faster than this protocol. Treat these dates as pointers, verify the current statute before relying on them, and prefer the stable EU AI Act and NIST/ISO mappings as the durable compliance anchors.

---

## 1. EU AI Act Articles Most Relevant to AIZP

| Article | Topic | AIZP Relevance |
|---|---|---|
| **Art 12** | Automatic event logging (high-risk AI) | ⭐⭐⭐⭐⭐ Direct: AIZP events are the log primitive |
| **Art 14** | Human oversight obligations | ⭐⭐⭐⭐⭐ Direct: `GRAVITY_LOCK` → human authorization |
| **Art 15** | Accuracy, robustness, cybersecurity | ⭐⭐⭐⭐ Indirect: drift + forecasting support |
| **Art 16** | Provider obligations | ⭐⭐⭐ Standardized via AIZP compliance levels |
| **Art 26** | Deployer obligations | ⭐⭐⭐⭐ Deployers use AIZP events for traceability |
| Annex III | High-risk system classification | ⭐⭐ Context-dependent |

Penalties for non-compliance: up to €15M or 3% of worldwide annual turnover.

---

## 2. Article 12 — Automatic Event Logging

**Requirement**: High-risk AI systems MUST automatically log events to enable traceability and post-market monitoring. Deployers MUST retain logs for at least 6 months.

### 2.1 AIZP capability mapping

| Art 12 requirement | AIZP capability |
|---|---|
| Automatic event logging | All 12 AIZP events are automatically emitted |
| Event traceability | `event_id`, `session_id`, `trigger_event_id` chain |
| 6-month retention | G4 compliance — auditable time-series store |
| Tamper resistance | G4 compliance — hash chain over events |
| Format standardization | AIZP events conform to JSON Schemas |

### 2.2 Concrete deployment guidance

For EU AI Act Art 12 compliance, the deployer MUST:

1. Enable AIZP at G3 or higher compliance level.
2. Configure event sink with 6+ month retention.
3. Enable tamper-resistance (hash chain, append-only storage).
4. Ensure events include all MUST fields per `AIZP_Protocol.md` for each event type.
5. Provide query API to AIZP event log for regulator inspection on request.

### 2.3 Logging configuration sample

```yaml
aizp:
  art12_compliance:
    enabled: true
    retention_months: 18  # exceeds 6-month minimum
    tamper_resistance:
      hash_chain: true
      signed_checkpoints: every_1000_events
    storage_backend: "object_storage_with_lock"
    query_api:
      enabled: true
      regulator_access_role: "auditor_external"
```

---

## 3. Article 14 — Human Oversight

**Requirement**: High-risk AI MUST be designed to allow effective human supervision. Deployers MUST assign human oversight to natural persons with necessary competence, training, authority, and support.

### 3.1 AIZP capability mapping

| Art 14 requirement | AIZP capability |
|---|---|
| Human-in-command | `GRAVITY_LOCK` → `sys.io.confirm` requires human confirmation |
| Meaningful oversight | `confirmation_prompt` shows action context, not just yes/no |
| Override capability | Operator can issue `SAFE_STOP` at any time |
| Effective supervision | `IDENTITY_VERIFICATION` confirms agent identity to operator |

### 3.2 Effective oversight checklist

For an AIZP deployment to satisfy Art 14:

- [ ] All HIGH and CRITICAL gravity actions route to `GRAVITY_LOCK`.
- [ ] `confirmation_prompt` is human-readable, action-specific, and shows full context (not technical only).
- [ ] Operators have authority to issue `SAFE_STOP` or `QUARANTINE` on any agent.
- [ ] Operators receive notifications for `SAFE_STOP`, critical `GRAVITY_DRIFT`, `IDENTITY_VERIFICATION` failures.
- [ ] `gravity_lock_timeout_seconds` is realistic (5+ minutes) — don't pressure operators.

---

## 4. Article 15 — Accuracy, Robustness, Cybersecurity

**Requirement**: High-risk AI MUST be accurate, robust, and cybersecure throughout the lifecycle.

### 4.1 AIZP capability mapping

| Art 15 requirement | AIZP capability |
|---|---|
| Robustness | Drift detection across 11 types catches behavioral degradation |
| Cybersecurity | NHI/DID-based identity verification + Zero Trust integration |
| Accuracy verification | `GRAVITY_FORECAST` predicts trajectory accuracy |
| Adversarial robustness | Threat-Model.md addresses 10+ attack patterns |

---

## 5. Article 26 — Deployer Obligations

**Requirement**: Deployers of high-risk AI MUST keep logs (Art 12), assign human oversight (Art 14), and monitor system operation throughout the lifecycle.

### 5.1 AIZP capability mapping

Deployers using AIZP G3+ satisfy via:

| Art 26 requirement | AIZP feature |
|---|---|
| Operational monitoring | `GRAVITY_CHECK` per action + `GRAVITY_FORECAST` |
| Post-market monitoring | `aizp.*` OTel metrics |
| Incident reporting | `SAFE_STOP` events + AIAP T4 escalation |
| Bias / drift detection | 11-type drift detection over time |

---

## 6. Annex III Categorization

EU AI Act classifies AI as high-risk if it scores credit, filters resumes, decides healthcare benefits, prices insurance, etc.

AIZP **does not** classify systems; it provides controls applicable to any system. Deployer determines Annex III applicability separately, then chooses AIZP compliance level accordingly:

| Annex III category | Recommended AIZP level |
|---|---|
| Credit scoring | G4 |
| Resume filtering | G4 |
| Healthcare benefits | G4+ |
| Insurance pricing | G4 |
| Emergency call triage | G5 |
| Educational admission | G4 |

---

## 7. Compliance Self-Declaration

Deployers MAY include in their EU AI Act conformity assessment:

```yaml
deployer_declaration:
  ai_system: "soulbot-finance-agent-v3"
  annex_iii_category: "Credit scoring"
  aizp_compliance_level: G4
  art_12_logging:
    retention_months: 18
    backend: "object_storage_locked"
    tamper_resistance: "hash_chain_signed"
  art_14_oversight:
    operator_role: "compliance_officer"
    operator_count: 3
    24x7_coverage: true
  art_15_robustness:
    drift_detection_types: 11
    forecast_horizon_K: 5
    adversarial_red_team_last_test: "2026-04-15"
  art_26_monitoring:
    otel_pipeline: "datadog"
    metrics_dashboard: "https://internal/aizp/metrics"
```

---

## 8. Limitations of AIZP for EU AI Act

AIZP does **not** by itself satisfy:

- **Art 9 (Risk Management System)** — broader than AIZP scope.
- **Art 10 (Data Governance)** — training data quality.
- **Art 11 (Technical Documentation)** — separate documentation effort.
- **Art 13 (Transparency / User Information)** — agent disclosure to users.
- **Art 17 (Quality Management)** — organization-wide processes.

AIZP focuses on **runtime alignment dynamics**. Other Articles require complementary controls.

---

## 9. References

- EU AI Act (Regulation (EU) 2024/1689) — full text.
- Article 12 (event logging) — artificialintelligenceact.eu/article/12.
- Article 14 (human oversight) — artificialintelligenceact.eu/article/14.
- Article 26 (deployer obligations) — artificialintelligenceact.eu/article/26.
- Help Net Security (2026-04-16) — What the EU AI Act requires for AI agent logging.
- EU AI Act 2026 Updates: Compliance Requirements and Business Risks.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
